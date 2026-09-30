from rdss import (
    OccurrenceAddress,
    RelationalPoint,
    SemanticScale,
    TensorScalarElement,
)
from rdss.corpus import (
    rdss_reference_corpus,
    scan_rdss_reference_corpus,
)
from rdss.factorization import (
    FactorizationRelation,
    compare_factorizations,
    factorize_value,
    summarize_factorizations,
)
from rdss.realizations import (
    CP1State,
    MoireRotation,
)


def element(value, *, rank=(0, 0)):
    return TensorScalarElement(
        (complex(value),),
        rank,
        RelationalPoint(),
        SemanticScale("object"),
    )


def test_tensor_scalar_value_change_is_state_not_structure():
    comparison = compare_factorizations(
        element(1),
        element(2),
    )

    assert comparison.same_family
    assert comparison.same_structure
    assert not comparison.same_state
    assert comparison.same_representation
    assert (
        comparison.relation
        is FactorizationRelation.DIFFERENT_STATE
    )


def test_tensor_rank_change_is_structural():
    comparison = compare_factorizations(
        element(1, rank=(0, 0)),
        element(1, rank=(1, 0)),
    )

    assert comparison.same_family
    assert not comparison.same_structure
    assert (
        comparison.relation
        is FactorizationRelation.DIFFERENT_STRUCTURE
    )


def test_moire_common_shift_has_same_factorization():
    comparison = compare_factorizations(
        MoireRotation(1.0, 0.25),
        MoireRotation(2.0, 1.25),
    )

    assert comparison.same_family
    assert comparison.same_structure
    assert comparison.same_state
    assert comparison.same_representation
    assert (
        comparison.relation
        is FactorizationRelation.SAME_FACTORIZATION
    )


def test_cp1_global_phase_is_currently_a_state_difference():
    comparison = compare_factorizations(
        CP1State(1 + 0j, 0 + 0j),
        CP1State(0 + 1j, 0 + 0j),
    )

    assert comparison.same_family
    assert comparison.same_structure
    assert not comparison.same_state
    assert (
        comparison.relation
        is FactorizationRelation.DIFFERENT_STATE
    )


def test_bridgeable_cross_family_values_remain_different_families():
    comparison = compare_factorizations(
        OccurrenceAddress((-1,)),
        RelationalPoint((-1,)),
    )

    assert not comparison.same_family
    assert not comparison.same_structure
    assert (
        comparison.relation
        is FactorizationRelation.DIFFERENT_FAMILY
    )


def test_factorization_reconstructs_signature_keys_and_provenance():
    value = MoireRotation(1.0, 0.25)
    factor = factorize_value(value)

    assert factor.family == "moire_relative_rotation"
    assert factor.structure_key == (
        factor.family,
        tuple(
            (
                axis,
                __import__(
                    "rdss.canonical",
                    fromlist=["strict_normal_form"],
                ).strict_normal_form(raw).key,
            )
            for axis, raw in factor.structure_axes
        ),
    )
    assert factor.semantic_key == (
        factor.structure_key,
        factor.state_key,
    )
    assert factor.representation.endswith(
        ".MoireRotation"
    )
    assert factor.provenance == (
        "moire_rotation_signature",
    )


def test_reference_corpus_factorization_summary_matches_signature_catalog():
    corpus = rdss_reference_corpus()
    factor_summary = summarize_factorizations(
        tuple(item.value for item in corpus)
    )
    catalog_summary = (
        scan_rdss_reference_corpus()
        .catalog_summary
    )

    assert factor_summary.records == 36
    assert factor_summary.families == 22
    assert factor_summary.structures == 28
    assert factor_summary.semantic_states == 34
    assert factor_summary.representations == 22

    assert (
        factor_summary.records
        == catalog_summary.records
    )
    assert (
        factor_summary.families
        == catalog_summary.families
    )
    assert (
        factor_summary.structures
        == catalog_summary.structures
    )
    assert (
        factor_summary.semantic_states
        == catalog_summary.semantic_states
    )
