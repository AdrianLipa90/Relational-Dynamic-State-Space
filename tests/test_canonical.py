from dataclasses import dataclass

import pytest

from rdss.canonical import (
    AmbiguousReductionError,
    EquivalenceKind,
    InformationEffect,
    LossyReductionError,
    ReductionCycleError,
    ReductionEngine,
    ReductionRule,
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
