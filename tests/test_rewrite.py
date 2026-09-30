import pytest

from rdss import (
    OccurrenceAddress,
    RelationalPoint,
    TypedRelation,
)
from rdss.bridges import BridgeInvariant
from rdss.canonical import (
    EquivalenceKind,
    InformationEffect,
)
from rdss.operations import RelationOccurrence
from rdss.realizations import reference_point_from_occurrence
from rdss.rewrite import (
    AmbiguousRewriteError,
    NoRewriteRuleError,
    RewriteCycleError,
    RewriteInvariantError,
    RewriteRule,
    RewriteSystem,
    rdss_forgetful_rewrite_rules,
    rdss_forgetful_rewrite_system,
)


def test_reference_forgetful_rewrite_rules_are_explicitly_oriented():
    rules = rdss_forgetful_rewrite_rules()

    assert tuple(rule.name for rule in rules) == (
        "rewrite:forget_relation_occurrence",
        "rewrite:forget_relational_generative_binding",
        "rewrite:forget_relational_distinction_binding",
        "rewrite:forget_occurrence_path",
    )
    assert all(
        rule.kind is EquivalenceKind.FORGETFUL_PROJECTION
        for rule in rules
    )
    assert all(
        rule.information_effect is InformationEffect.LOSSY
        for rule in rules
    )


def test_relation_occurrence_rewrites_to_typed_relation_with_invariant():
    point = RelationalPoint()
    relation = TypedRelation(point, point, "r")
    occurrence = RelationOccurrence(
        relation,
        (),
        (-1,),
    )

    target, step = rdss_forgetful_rewrite_system().step(
        occurrence
    )

    assert target == relation
    assert step.lossy
    assert step.source_bridge_name == "forget_relation_occurrence"
    assert step.verified_invariants == (
        "typed relation value",
    )


def test_irreducible_value_has_no_automatic_rewrite():
    system = rdss_forgetful_rewrite_system()
    point = RelationalPoint()

    assert system.irreducible(point)

    with pytest.raises(NoRewriteRuleError):
        system.step(point)


def test_trace_until_irreducible_stops_after_unique_forgetful_step():
    point = RelationalPoint()
    relation = TypedRelation(point, point, "r")
    occurrence = RelationOccurrence(
        relation,
        (),
        (-1,),
    )

    trace = rdss_forgetful_rewrite_system().trace_until_irreducible(
        occurrence
    )

    assert trace.value == relation
    assert trace.rule_names == (
        "rewrite:forget_relation_occurrence",
    )
    assert trace.lossy


def test_multiple_applicable_rules_fail_closed_without_priority():
    rule_a = RewriteRule(
        name="a",
        source_family="occurrence_address",
        target_family="relational_carrier",
        transform=reference_point_from_occurrence,
        source_check=lambda value: isinstance(
            value,
            OccurrenceAddress,
        ),
        target_check=lambda value: isinstance(
            value,
            RelationalPoint,
        ),
        kind=EquivalenceKind.REFERENCE_REPRESENTATION,
        information_effect=InformationEffect.LOSSLESS,
    )
    rule_b = RewriteRule(
        name="b",
        source_family="occurrence_address",
        target_family="relational_carrier",
        transform=reference_point_from_occurrence,
        source_check=lambda value: isinstance(
            value,
            OccurrenceAddress,
        ),
        target_check=lambda value: isinstance(
            value,
            RelationalPoint,
        ),
        kind=EquivalenceKind.REFERENCE_REPRESENTATION,
        information_effect=InformationEffect.LOSSLESS,
    )
    system = RewriteSystem((rule_a, rule_b))

    with pytest.raises(AmbiguousRewriteError):
        system.step(OccurrenceAddress((-1,)))


def test_explicit_rule_selection_does_not_depend_on_registration_priority():
    rule_a = RewriteRule(
        name="a",
        source_family="occurrence_address",
        target_family="relational_carrier",
        transform=reference_point_from_occurrence,
        source_check=lambda value: isinstance(
            value,
            OccurrenceAddress,
        ),
        target_check=lambda value: isinstance(
            value,
            RelationalPoint,
        ),
        kind=EquivalenceKind.REFERENCE_REPRESENTATION,
        information_effect=InformationEffect.LOSSLESS,
    )
    rule_b = RewriteRule(
        name="b",
        source_family="occurrence_address",
        target_family="relational_carrier",
        transform=reference_point_from_occurrence,
        source_check=lambda value: isinstance(
            value,
            OccurrenceAddress,
        ),
        target_check=lambda value: isinstance(
            value,
            RelationalPoint,
        ),
        kind=EquivalenceKind.REFERENCE_REPRESENTATION,
        information_effect=InformationEffect.LOSSLESS,
    )
    system = RewriteSystem((rule_b, rule_a))

    target, step = system.apply(
        OccurrenceAddress((1,)),
        "a",
    )

    assert target == RelationalPoint((1,))
    assert step.rule_name == "a"


def test_rewrite_invariant_failure_is_fail_closed():
    point = RelationalPoint()
    relation = TypedRelation(point, point, "r")
    occurrence = RelationOccurrence(
        relation,
        (),
        (-1,),
    )
    bad = RewriteRule(
        name="bad",
        source_family="relation_occurrence",
        target_family="typed_relation",
        transform=lambda value: TypedRelation(
            value.relation.source,
            value.relation.target,
            "wrong",
        ),
        source_check=lambda value: isinstance(
            value,
            RelationOccurrence,
        ),
        target_check=lambda value: isinstance(
            value,
            TypedRelation,
        ),
        kind=EquivalenceKind.FORGETFUL_PROJECTION,
        information_effect=InformationEffect.LOSSY,
        invariants=(
            BridgeInvariant(
                "typed relation value",
                source_projection=lambda value: value.relation,
                target_projection=lambda value: value,
            ),
        ),
    )

    with pytest.raises(RewriteInvariantError):
        RewriteSystem((bad,)).step(occurrence)


def test_automatic_trace_detects_rewrite_cycle():
    forward = RewriteRule(
        name="to-point",
        source_family="occurrence_address",
        target_family="relational_carrier",
        transform=reference_point_from_occurrence,
        source_check=lambda value: isinstance(
            value,
            OccurrenceAddress,
        ),
        target_check=lambda value: isinstance(
            value,
            RelationalPoint,
        ),
        kind=EquivalenceKind.REFERENCE_REPRESENTATION,
        information_effect=InformationEffect.LOSSLESS,
    )
    backward = RewriteRule(
        name="to-occurrence",
        source_family="relational_carrier",
        target_family="occurrence_address",
        transform=lambda value: OccurrenceAddress(value.address),
        source_check=lambda value: isinstance(
            value,
            RelationalPoint,
        ),
        target_check=lambda value: isinstance(
            value,
            OccurrenceAddress,
        ),
        kind=EquivalenceKind.REFERENCE_REPRESENTATION,
        information_effect=InformationEffect.LOSSLESS,
    )
    system = RewriteSystem((forward, backward))

    with pytest.raises(RewriteCycleError):
        system.trace_until_irreducible(
            OccurrenceAddress((-1,)),
            max_steps=4,
        )
