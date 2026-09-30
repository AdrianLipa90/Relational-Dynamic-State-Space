import pytest

from rdss import RelationalPoint, TypedRelation
from rdss.bridges import (
    UnsupportedBridgeError,
    rdss_bridge_registry,
)
from rdss.closure import BranchRelationOccurrence
from rdss.canonical import EquivalenceKind, InformationEffect
from rdss.contextual_bridges import (
    CarrierMapContext,
    ContextualBridgeInvariant,
    ContextualBridgeInvariantError,
    ContextualBridgeRegistry,
    ContextualBridgeSpec,
    UnsupportedContextualBridgeError,
    materialize_branch_relation_occurrence,
    rdss_contextual_bridge_registry,
)


def test_carrier_map_context_resolves_symbolic_labels():
    context = CarrierMapContext.from_mapping(
        {
            "a": RelationalPoint(),
            "b": RelationalPoint((-1,)),
        }
    )

    assert context.resolve("a") == RelationalPoint()
    assert context.resolve("b") == RelationalPoint((-1,))


def test_carrier_map_context_rejects_duplicate_labels():
    with pytest.raises(ValueError):
        CarrierMapContext(
            (
                ("a", RelationalPoint()),
                ("a", RelationalPoint((-1,))),
            )
        )


def test_contextual_materialization_requires_all_endpoint_labels():
    occurrence = BranchRelationOccurrence(
        -1,
        "r",
        "a",
        "b",
    )
    context = CarrierMapContext.from_mapping(
        {"a": RelationalPoint()}
    )

    with pytest.raises(KeyError):
        materialize_branch_relation_occurrence(
            occurrence,
            context,
        )


def test_contextual_branch_relation_materialization_is_lossy():
    occurrence = BranchRelationOccurrence(
        -1,
        "r",
        "a",
        "b",
    )
    source = RelationalPoint()
    target = RelationalPoint((-1,))
    context = CarrierMapContext.from_mapping(
        {
            "a": source,
            "b": target,
        }
    )

    result = rdss_contextual_bridge_registry().direct(
        occurrence,
        "typed_relation",
        context=context,
    )

    assert result.value == TypedRelation(
        source,
        target,
        "r",
    )
    assert result.lossy
    assert result.step.context_name == "carrier_label_map"
    assert result.step.claim_ids == (
        "DEF_CONTEXTUAL_BRANCH_RELATION_MATERIALIZATION",
        "DEF_RELATIONAL_DISTINCTION",
    )
    assert result.step.verified_invariants == (
        "relation label",
        "source endpoint through supplied carrier map",
        "target endpoint through supplied carrier map",
    )


def test_branch_slot_is_not_present_after_contextual_projection():
    left = BranchRelationOccurrence(
        -1,
        "r",
        "a",
        "b",
    )
    right = BranchRelationOccurrence(
        1,
        "r",
        "a",
        "b",
    )
    context = CarrierMapContext.from_mapping(
        {
            "a": RelationalPoint(),
            "b": RelationalPoint((-1,)),
        }
    )
    registry = rdss_contextual_bridge_registry()

    left_result = registry.direct(
        left,
        "typed_relation",
        context=context,
    )
    right_result = registry.direct(
        right,
        "typed_relation",
        context=context,
    )

    assert left_result.value == right_result.value
    assert left != right


def test_contextual_bridge_is_not_available_in_global_bridge_registry():
    occurrence = BranchRelationOccurrence(
        -1,
        "r",
        "a",
        "b",
    )

    with pytest.raises(UnsupportedBridgeError):
        rdss_bridge_registry().direct(
            occurrence,
            "typed_relation",
        )


def test_wrong_context_type_fails_closed():
    occurrence = BranchRelationOccurrence(
        -1,
        "r",
        "a",
        "b",
    )

    with pytest.raises(UnsupportedContextualBridgeError):
        rdss_contextual_bridge_registry().direct(
            occurrence,
            "typed_relation",
            context={"a": RelationalPoint()},
        )



def test_contextual_invariant_failure_is_fail_closed():
    point = RelationalPoint()
    occurrence = BranchRelationOccurrence(
        -1,
        "r",
        "a",
        "a",
    )
    context = CarrierMapContext.from_mapping(
        {"a": point}
    )
    bad = ContextualBridgeSpec(
        name="bad-contextual-invariant",
        source_family="branch_relation_occurrence",
        target_family="typed_relation",
        context_name="carrier_label_map",
        source_check=lambda value: isinstance(
            value,
            BranchRelationOccurrence,
        ),
        context_check=lambda value: isinstance(
            value,
            CarrierMapContext,
        ),
        target_check=lambda value: isinstance(
            value,
            TypedRelation,
        ),
        transform=lambda value, ctx: TypedRelation(
            ctx.resolve(value.source),
            ctx.resolve(value.target),
            value.relation_label,
        ),
        kind=EquivalenceKind.FORGETFUL_PROJECTION,
        information_effect=InformationEffect.LOSSY,
        invariants=(
            ContextualBridgeInvariant(
                "deliberately false",
                source_context_projection=lambda value, ctx: (
                    value.relation_label
                ),
                target_projection=lambda value: (
                    value.label + "-wrong"
                ),
            ),
        ),
    )

    registry = ContextualBridgeRegistry((bad,))

    with pytest.raises(ContextualBridgeInvariantError):
        registry.direct(
            occurrence,
            "typed_relation",
            context=context,
        )
