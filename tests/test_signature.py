from dataclasses import dataclass

import pytest

from rdss import (
    HilbertMoireFibreState,
    OccurrenceAddress,
    RelationalPoint,
    SemanticScale,
    TensorScalarElement,
    TypedRelation,
)
from rdss.realizations import MoireRotation
from rdss.signature import (
    AmbiguousSignatureError,
    NoveltyKind,
    RDSSSignature,
    SignatureAxis,
    SignatureComparisonKind,
    SignatureEngine,
    SignatureExtractor,
    UnsupportedSignatureError,
    rdss_signature_engine,
)


def element(value, *, rank=(0, 0), carrier=None, scale=None):
    return TensorScalarElement(
        (complex(value),),
        rank,
        carrier or RelationalPoint(),
        scale or SemanticScale("object"),
    )


def test_carrier_and_occurrence_are_incomparable_without_bridge():
    engine = rdss_signature_engine()

    result = engine.compare(
        OccurrenceAddress((-1, 1)),
        RelationalPoint((-1, 1)),
    )

    assert result.kind is SignatureComparisonKind.INCOMPARABLE
    assert result.novelty is NoveltyKind.NEW_FAMILY


def test_tensor_scalar_same_sector_different_components_is_new_state():
    engine = rdss_signature_engine()
    carrier = RelationalPoint((-1,))
    scale = SemanticScale("object")

    left = element(1, carrier=carrier, scale=scale)
    right = element(2, carrier=carrier, scale=scale)

    result = engine.compare(left, right)

    assert result.kind is SignatureComparisonKind.SAME_STRUCTURE_DIFFERENT_STATE
    assert result.novelty is NoveltyKind.NEW_STATE
    assert not result.strict_equal


def test_tensor_scalar_rank_change_is_structural_difference():
    engine = rdss_signature_engine()
    carrier = RelationalPoint()
    scale = SemanticScale("object")

    left = element(1, rank=(0, 0), carrier=carrier, scale=scale)
    right = element(1, rank=(1, 0), carrier=carrier, scale=scale)

    result = engine.compare(left, right)

    assert result.kind is SignatureComparisonKind.STRUCTURAL_DIFFERENCE
    assert result.novelty is NoveltyKind.NEW_STRUCTURE


def test_relation_occurrence_and_relation_value_need_projection_not_signature_equality():
    from rdss.operations import RelationOccurrence

    engine = rdss_signature_engine()
    carrier = RelationalPoint()
    relation = TypedRelation(carrier, carrier, "r")
    occurrence = RelationOccurrence(relation, (), (-1,))

    result = engine.compare(occurrence, relation)

    assert result.kind is SignatureComparisonKind.INCOMPARABLE
    assert result.novelty is NoveltyKind.NEW_FAMILY


def test_hilbert_moire_phase_change_is_state_change_not_structure_change():
    engine = rdss_signature_engine()
    left = HilbertMoireFibreState(
        OccurrenceAddress((-1,)),
        "orbital-A",
        0.25,
        (1 + 0j, 0 + 1j),
    )
    right = HilbertMoireFibreState(
        OccurrenceAddress((-1,)),
        "orbital-A",
        0.5,
        (1 + 0j, 0 + 1j),
    )

    result = engine.compare(left, right)

    assert result.kind is SignatureComparisonKind.SAME_STRUCTURE_DIFFERENT_STATE
    assert result.novelty is NoveltyKind.NEW_STATE


def test_hilbert_moire_orbit_change_is_structural_difference():
    engine = rdss_signature_engine()
    left = HilbertMoireFibreState(
        OccurrenceAddress(),
        "orbital-A",
        0.25,
        (1 + 0j,),
    )
    right = HilbertMoireFibreState(
        OccurrenceAddress(),
        "orbital-B",
        0.25,
        (1 + 0j,),
    )

    result = engine.compare(left, right)

    assert result.kind is SignatureComparisonKind.STRUCTURAL_DIFFERENCE


def test_moire_common_angle_shift_collapses_to_same_relative_signature():
    engine = rdss_signature_engine()
    left = MoireRotation(1.0, 0.25)
    right = MoireRotation(2.0, 1.25)

    result = engine.compare(left, right)

    assert result.kind is SignatureComparisonKind.EXACT_SIGNATURE
    assert not result.strict_equal
    assert result.novelty is NoveltyKind.SIGNATURE_EQUIVALENT


@dataclass(frozen=True)
class RepA:
    value: int


@dataclass(frozen=True)
class RepB:
    value: int


def test_same_semantic_state_can_be_marked_representation_only():
    def make_signature(value):
        return RDSSSignature(
            family="toy",
            axes=((SignatureAxis.STATE, value.value),),
            representation=type(value).__name__,
        )

    engine = SignatureEngine(
        (
            SignatureExtractor(
                "rep-a",
                lambda value: isinstance(value, RepA),
                make_signature,
            ),
            SignatureExtractor(
                "rep-b",
                lambda value: isinstance(value, RepB),
                make_signature,
            ),
        )
    )

    result = engine.compare(RepA(7), RepB(7))

    assert (
        result.kind
        is SignatureComparisonKind
        .SAME_SEMANTIC_STATE_DIFFERENT_REPRESENTATION
    )
    assert result.novelty is NoveltyKind.REPRESENTATION_ONLY


def test_unsupported_signature_fails_closed():
    with pytest.raises(UnsupportedSignatureError):
        rdss_signature_engine().signature(object())


def test_competing_signature_extractors_fail_closed():
    extractor_a = SignatureExtractor(
        "a",
        lambda value: isinstance(value, int),
        lambda value: RDSSSignature(
            "int",
            ((SignatureAxis.STATE, value),),
            "int",
        ),
    )
    extractor_b = SignatureExtractor(
        "b",
        lambda value: isinstance(value, int),
        lambda value: RDSSSignature(
            "int",
            ((SignatureAxis.STATE, value),),
            "int",
        ),
    )

    with pytest.raises(AmbiguousSignatureError):
        SignatureEngine((extractor_a, extractor_b)).signature(3)


def test_duplicate_signature_axis_is_rejected():
    with pytest.raises(ValueError):
        RDSSSignature(
            "bad",
            (
                (SignatureAxis.STATE, 1),
                (SignatureAxis.STATE, 2),
            ),
            "bad",
        )


def test_signature_records_extractor_and_claim_provenance():
    signature = rdss_signature_engine().signature(
        OccurrenceAddress((1,))
    )

    assert signature.provenance == (
        "occurrence_address_signature",
    )
    assert "DEF_OCCURRENCE_ADDRESS_SPACE" in signature.claim_ids
    assert "DEF_RDSS_CANONICAL_SIGNATURE" in signature.claim_ids
