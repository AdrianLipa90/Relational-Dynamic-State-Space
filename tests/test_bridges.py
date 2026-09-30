from dataclasses import dataclass

import pytest

from rdss import (
    OccurrenceAddress,
    RelationalPoint,
    SemanticScale,
    TensorScalarElement,
    TypedRelation,
    TypedZero,
)
from rdss.closure import (
    BinaryDistinction,
    RelationalBinaryDistinction,
)
from rdss.bridges import (
    AmbiguousBridgeError,
    BridgeRegistry,
    BridgeSpec,
    LossyBridgeError,
    UnsupportedBridgeError,
    rdss_bridge_registry,
)
from rdss.canonical import EquivalenceKind, InformationEffect
from rdss.operations import (
    OccurrenceRelationPath,
    RelationOccurrence,
    RelationPath,
)
from rdss.signature import (
    RDSSSignature,
    SignatureAxis,
    SignatureEngine,
    SignatureExtractor,
)


def test_occurrence_reference_point_bridge_is_lossless_but_not_identity():
    registry = rdss_bridge_registry()
    occurrence = OccurrenceAddress((-1, 1))

    route = registry.direct(
        occurrence,
        "relational_carrier",
    )

    assert route.value == RelationalPoint((-1, 1))
    assert route.fully_reversible
    assert not route.lossy
    assert route.steps[0].kind is EquivalenceKind.REFERENCE_REPRESENTATION
    assert route.steps[0].roundtrip_verified
    assert route.steps[0].claim_ids == (
        "DEF_CARRIER_OCCURRENCE_SEPARATION",
        "REF_RELATIONAL_POINT_BINARY_COORDINATE",
    )


def test_reference_point_bridge_has_explicit_reverse_edge():
    registry = rdss_bridge_registry()
    point = RelationalPoint((1, -1))

    route = registry.direct(
        point,
        "occurrence_address",
    )

    assert route.value == OccurrenceAddress((1, -1))
    assert route.fully_reversible
    assert route.steps[0].direction.value == "inverse"


def test_bridge_compare_can_match_reference_representation_without_identity():
    registry = rdss_bridge_registry()
    occurrence = OccurrenceAddress((-1,))
    point = RelationalPoint((-1,))

    result = registry.compare(occurrence, point)

    assert result.equivalent_after_bridge
    assert result.route.fully_reversible
    assert result.comparison.strict_equal
    assert occurrence is not point


def test_relation_occurrence_projection_requires_lossy_opt_in():
    registry = rdss_bridge_registry()
    carrier = RelationalPoint()
    relation = TypedRelation(carrier, carrier, "r")
    occurrence = RelationOccurrence(relation, (), (-1,))

    with pytest.raises(LossyBridgeError):
        registry.compare(occurrence, relation)

    result = registry.compare(
        occurrence,
        relation,
        allow_lossy=True,
    )

    assert result.equivalent_after_bridge
    assert result.route.lossy
    assert not result.route.fully_reversible


def test_occurrence_path_projection_has_no_reverse_route():
    registry = rdss_bridge_registry()
    carrier = RelationalPoint()
    down = TypedRelation(carrier, carrier, "down")
    up = TypedRelation(carrier, carrier, "up")
    occurrence_path = OccurrenceRelationPath(
        (
            RelationOccurrence(down, (), (-1,)),
            RelationOccurrence(up, (-1,), ()),
        )
    )

    projected = registry.direct(
        occurrence_path,
        "relation_path",
    )

    assert projected.value == RelationPath((down, up))
    assert projected.lossy

    with pytest.raises(UnsupportedBridgeError):
        registry.direct(
            projected.value,
            "occurrence_relation_path",
        )


@dataclass(frozen=True)
class A:
    value: int


@dataclass(frozen=True)
class B:
    value: int


@dataclass(frozen=True)
class C:
    value: int


def toy_signature_engine():
    def signature(value):
        return RDSSSignature(
            family=type(value).__name__,
            axes=((SignatureAxis.STATE, value.value),),
            representation=type(value).__name__,
        )

    return SignatureEngine(
        (
            SignatureExtractor("A", lambda x: isinstance(x, A), signature),
            SignatureExtractor("B", lambda x: isinstance(x, B), signature),
            SignatureExtractor("C", lambda x: isinstance(x, C), signature),
        )
    )


def lossless_bridge(name, source, target):
    return BridgeSpec(
        name=name,
        source_family=source.__name__,
        target_family=target.__name__,
        forward=lambda value: target(value.value),
        inverse=lambda value: source(value.value),
        source_check=lambda value: isinstance(value, source),
        target_check=lambda value: isinstance(value, target),
        kind=EquivalenceKind.ISOMORPHISM,
        information_effect=InformationEffect.LOSSLESS,
        preserves=("value",),
        claim_ids=("TEST_BRIDGE",),
    )


def test_bridge_route_composes_multiple_explicit_lossless_edges():
    registry = BridgeRegistry(
        (
            lossless_bridge("a-b", A, B),
            lossless_bridge("b-c", B, C),
        ),
        signature_engine=toy_signature_engine(),
    )

    route = registry.route(A(7), "C")

    assert route.value == C(7)
    assert len(route.steps) == 2
    assert route.fully_reversible
    assert route.provenance == (
        "a-b:forward",
        "b-c:forward",
    )


def test_multiple_shortest_bridge_routes_fail_closed():
    first = lossless_bridge("a-c-1", A, C)
    second = lossless_bridge("a-c-2", A, C)
    registry = BridgeRegistry(
        (first, second),
        signature_engine=toy_signature_engine(),
    )

    with pytest.raises(AmbiguousBridgeError):
        registry.route(
            A(1),
            "C",
            max_hops=2,
        )


def test_duplicate_bridge_names_are_rejected():
    bridge = lossless_bridge("same", A, B)

    with pytest.raises(ValueError):
        BridgeRegistry(
            (bridge, bridge),
            signature_engine=toy_signature_engine(),
        )


def test_lossless_bridge_requires_inverse():
    with pytest.raises(ValueError):
        BridgeSpec(
            name="bad",
            source_family="A",
            target_family="B",
            forward=lambda value: B(value.value),
            source_check=lambda value: isinstance(value, A),
            target_check=lambda value: isinstance(value, B),
            kind=EquivalenceKind.REFERENCE_REPRESENTATION,
            information_effect=InformationEffect.LOSSLESS,
        )


def test_identity_cannot_be_smuggled_in_as_cross_family_bridge():
    with pytest.raises(ValueError):
        BridgeSpec(
            name="bad-identity",
            source_family="A",
            target_family="B",
            forward=lambda value: B(value.value),
            inverse=lambda value: A(value.value),
            source_check=lambda value: isinstance(value, A),
            target_check=lambda value: isinstance(value, B),
            kind=EquivalenceKind.IDENTITY,
            information_effect=InformationEffect.LOSSLESS,
        )



def test_typed_zero_bridge_is_lossless_on_zero_subspace():
    registry = rdss_bridge_registry()
    point = RelationalPoint()
    scale = SemanticScale("object")
    zero = TypedZero((0, 0), point, scale, 2)

    route = registry.direct(
        zero,
        "tensor_scalar_element",
    )

    assert route.value == TensorScalarElement(
        (0j, 0j),
        (0, 0),
        point,
        scale,
    )
    assert route.fully_reversible
    assert route.steps[0].kind is EquivalenceKind.REFERENCE_REPRESENTATION


def test_zero_tensor_element_has_explicit_reverse_bridge_to_typed_zero():
    registry = rdss_bridge_registry()
    point = RelationalPoint()
    scale = SemanticScale("object")
    zero_element = TensorScalarElement(
        (0j, 0j),
        (1, 1),
        point,
        scale,
    )

    route = registry.direct(
        zero_element,
        "typed_zero",
    )

    assert route.value == TypedZero(
        (1, 1),
        point,
        scale,
        2,
    )
    assert route.fully_reversible


def test_nonzero_tensor_element_cannot_use_typed_zero_reverse_bridge():
    registry = rdss_bridge_registry()
    nonzero = TensorScalarElement(
        (1 + 0j,),
        (0, 0),
        RelationalPoint(),
        SemanticScale("object"),
    )

    with pytest.raises(UnsupportedBridgeError):
        registry.direct(nonzero, "typed_zero")


def test_relational_distinction_forgetful_bridge_is_lossy():
    registry = rdss_bridge_registry()
    relational = RelationalBinaryDistinction(
        "a",
        "b",
        "c",
        "r-left",
        "r-right",
    )
    binary = BinaryDistinction("a", "b", "c")

    with pytest.raises(LossyBridgeError):
        registry.compare(relational, binary)

    result = registry.compare(
        relational,
        binary,
        allow_lossy=True,
    )

    assert result.equivalent_after_bridge
    assert result.route.lossy
    assert not result.route.fully_reversible
