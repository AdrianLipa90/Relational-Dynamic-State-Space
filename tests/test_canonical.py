from dataclasses import dataclass

import pytest

from rdss.canonical import (
    AmbiguousReductionError,
    EquivalenceKind,
    InformationEffect,
    FiniteConfluenceStatus,
    LexicographicReductionOrder,
    LossyReductionError,
    NonDescendingReductionError,
    ReductionCycleError,
    ReductionEngine,
    ReductionRule,
    audit_finite_confluence,
    rdss_projection_engine,
    roundtrip_check,
    strict_normal_form,
)


@dataclass(frozen=True)
class A:
    value: int


@dataclass(frozen=True)
class B:
    value: int


class Address(tuple):
    pass


def test_strict_normal_form_is_idempotent():
    normal = strict_normal_form(A(3))
    assert strict_normal_form(normal) is normal


def test_type_tag_keeps_distinct_representations_distinct():
    assert not strict_normal_form(A(3)).same_key(
        strict_normal_form(B(3))
    )


def test_tuple_subclass_keeps_its_representation_tag():
    assert not strict_normal_form(Address((-1, 1))).same_key(
        strict_normal_form((-1, 1))
    )


def test_lossless_rule_requires_inverse():
    with pytest.raises(ValueError):
        ReductionRule(
            "bad",
            lambda x: isinstance(x, A),
            lambda x: B(x.value),
            EquivalenceKind.REFERENCE_REPRESENTATION,
            InformationEffect.LOSSLESS,
        )


def test_isomorphism_roundtrip_and_compare():
    rule = ReductionRule(
        "a_to_b",
        lambda x: isinstance(x, A),
        lambda x: B(x.value),
        EquivalenceKind.ISOMORPHISM,
        InformationEffect.LOSSLESS,
        inverse=lambda x: A(x.value),
        preserves=("value",),
        claim_ids=("DEF_TEST",),
    )

    assert roundtrip_check(rule, A(7))

    result = ReductionEngine((rule,)).compare(
        A(7),
        B(7),
    )

    assert result.equivalent
    assert result.comparison_is_lossless
    assert result.left.trace.provenance == ("a_to_b",)


def test_lossy_projection_requires_explicit_opt_in_for_equivalence():
    rule = ReductionRule(
        "drop_sign",
        lambda x: isinstance(x, A),
        lambda x: abs(x.value),
        EquivalenceKind.FORGETFUL_PROJECTION,
        InformationEffect.LOSSY,
    )
    engine = ReductionEngine((rule,))

    with pytest.raises(LossyReductionError):
        engine.compare(A(-3), 3)

    assert engine.compare(
        A(-3),
        3,
        allow_lossy=True,
    ).equivalent


def test_competing_rules_fail_closed():
    first = ReductionRule(
        "first",
        lambda x: isinstance(x, A),
        lambda x: B(x.value),
        EquivalenceKind.APPROXIMATION,
        InformationEffect.UNKNOWN,
    )
    second = ReductionRule(
        "second",
        lambda x: isinstance(x, A),
        lambda x: x.value,
        EquivalenceKind.FORGETFUL_PROJECTION,
        InformationEffect.LOSSY,
    )

    with pytest.raises(AmbiguousReductionError):
        ReductionEngine((first, second)).reduce(A(2))


def test_cycle_is_rejected():
    forward = ReductionRule(
        "a_to_b",
        lambda x: isinstance(x, A),
        lambda x: B(x.value),
        EquivalenceKind.APPROXIMATION,
        InformationEffect.UNKNOWN,
    )
    backward = ReductionRule(
        "b_to_a",
        lambda x: isinstance(x, B),
        lambda x: A(x.value),
        EquivalenceKind.APPROXIMATION,
        InformationEffect.UNKNOWN,
    )

    with pytest.raises(ReductionCycleError):
        ReductionEngine((forward, backward)).reduce(A(2))


def test_nonfinite_values_fail_closed():
    with pytest.raises(ValueError):
        strict_normal_form(float("nan"))


def test_rdss_strict_form_keeps_carrier_and_occurrence_as_distinct_sorts():
    from rdss import OccurrenceAddress, RelationalPoint

    occurrence = OccurrenceAddress((-1, 1))
    carrier = RelationalPoint((-1, 1))

    assert not strict_normal_form(occurrence).same_key(
        strict_normal_form(carrier)
    )


def test_rdss_relation_occurrence_projection_is_explicitly_lossy():
    from rdss import RelationalPoint, TypedRelation
    from rdss.operations import RelationOccurrence

    carrier = RelationalPoint()
    relation = TypedRelation(carrier, carrier, "r")
    occurrence = RelationOccurrence(
        relation,
        (),
        (-1,),
    )
    engine = rdss_projection_engine()

    reduced = engine.reduce(occurrence)

    assert reduced.value == relation
    assert reduced.trace.lossy
    assert reduced.trace.steps[0].kind is EquivalenceKind.FORGETFUL_PROJECTION
    assert reduced.trace.steps[0].claim_ids == (
        "DEF_OCCURRENCE_FORGETFUL_PROJECTION",
    )

    with pytest.raises(LossyReductionError):
        engine.compare(occurrence, relation)

    assert engine.compare(
        occurrence,
        relation,
        allow_lossy=True,
    ).equivalent


def test_rdss_occurrence_path_projection_preserves_order_but_loses_addresses():
    from rdss import RelationalPoint, TypedRelation
    from rdss.operations import OccurrenceRelationPath, RelationOccurrence

    carrier = RelationalPoint()
    down = TypedRelation(carrier, carrier, "down")
    up = TypedRelation(carrier, carrier, "up")
    path = OccurrenceRelationPath(
        (
            RelationOccurrence(down, (), (-1,)),
            RelationOccurrence(up, (-1,), ()),
        )
    )

    reduced = rdss_projection_engine().reduce(path)

    assert tuple(reduced.value.relations) == (down, up)
    assert reduced.trace.lossy
    assert reduced.trace.steps[0].preserves == (
        "ordered relation values",
        "carrier composability",
    )



def test_well_founded_order_accepts_strict_descent():
    rule = ReductionRule(
        "decrement",
        lambda value: isinstance(value, int) and value > 0,
        lambda value: value - 1,
        EquivalenceKind.EXACT_EQUIVALENCE,
        InformationEffect.UNKNOWN,
    )
    order = LexicographicReductionOrder(
        "natural-number",
        lambda value: (value,),
        1,
    )

    result = ReductionEngine(
        (rule,),
        ordering=order,
    ).reduce(3)

    assert result.value == 0
    assert len(result.trace.steps) == 3


def test_well_founded_order_rejects_non_descent():
    rule = ReductionRule(
        "increment",
        lambda value: isinstance(value, int),
        lambda value: value + 1,
        EquivalenceKind.APPROXIMATION,
        InformationEffect.UNKNOWN,
    )
    order = LexicographicReductionOrder(
        "natural-number",
        lambda value: (value,),
        1,
    )

    with pytest.raises(NonDescendingReductionError):
        ReductionEngine(
            (rule,),
            ordering=order,
        ).reduce(1)


def test_reduction_order_requires_fixed_measure_dimension():
    order = LexicographicReductionOrder(
        "fixed-one",
        lambda value: (value,) if value else (0, 0),
        1,
    )

    assert order.key(2) == (2,)
    with pytest.raises(ValueError):
        order.key(0)


def test_finite_confluence_audit_finds_unique_join():
    rules = (
        ReductionRule(
            "start-left",
            lambda value: value == "start",
            lambda value: "left",
            EquivalenceKind.EXACT_EQUIVALENCE,
            InformationEffect.UNKNOWN,
        ),
        ReductionRule(
            "start-right",
            lambda value: value == "start",
            lambda value: "right",
            EquivalenceKind.EXACT_EQUIVALENCE,
            InformationEffect.UNKNOWN,
        ),
        ReductionRule(
            "left-end",
            lambda value: value == "left",
            lambda value: "end",
            EquivalenceKind.EXACT_EQUIVALENCE,
            InformationEffect.UNKNOWN,
        ),
        ReductionRule(
            "right-end",
            lambda value: value == "right",
            lambda value: "end",
            EquivalenceKind.EXACT_EQUIVALENCE,
            InformationEffect.UNKNOWN,
        ),
    )

    report = audit_finite_confluence(
        "start",
        rules,
        max_depth=3,
    )

    assert report.status is FiniteConfluenceStatus.UNIQUE_NORMAL_FORM
    assert report.confluent_on_explored_graph
    assert len(report.terminal_keys) == 1


def test_finite_confluence_audit_detects_multiple_normal_forms():
    rules = (
        ReductionRule(
            "start-left",
            lambda value: value == "start",
            lambda value: "left",
            EquivalenceKind.APPROXIMATION,
            InformationEffect.UNKNOWN,
        ),
        ReductionRule(
            "start-right",
            lambda value: value == "start",
            lambda value: "right",
            EquivalenceKind.APPROXIMATION,
            InformationEffect.UNKNOWN,
        ),
    )

    report = audit_finite_confluence(
        "start",
        rules,
        max_depth=2,
    )

    assert report.status is FiniteConfluenceStatus.MULTIPLE_NORMAL_FORMS
    assert len(report.terminal_keys) == 2


def test_finite_confluence_audit_detects_cycle():
    rules = (
        ReductionRule(
            "a-b",
            lambda value: value == "a",
            lambda value: "b",
            EquivalenceKind.APPROXIMATION,
            InformationEffect.UNKNOWN,
        ),
        ReductionRule(
            "b-a",
            lambda value: value == "b",
            lambda value: "a",
            EquivalenceKind.APPROXIMATION,
            InformationEffect.UNKNOWN,
        ),
    )

    report = audit_finite_confluence(
        "a",
        rules,
        max_depth=4,
    )

    assert report.status is FiniteConfluenceStatus.CYCLE_DETECTED
    assert report.cycle_edges


def test_finite_confluence_audit_reports_depth_truncation():
    rule = ReductionRule(
        "decrement",
        lambda value: isinstance(value, int) and value > 0,
        lambda value: value - 1,
        EquivalenceKind.EXACT_EQUIVALENCE,
        InformationEffect.UNKNOWN,
    )

    report = audit_finite_confluence(
        3,
        (rule,),
        max_depth=1,
    )

    assert report.status is FiniteConfluenceStatus.BOUNDED_INCOMPLETE
    assert report.truncated_keys
