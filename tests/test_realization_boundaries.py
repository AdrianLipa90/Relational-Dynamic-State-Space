from rdss.realization_boundaries import (
    indexed_tensor_underdetermination_certificate,
    monoidal_coherence_underdetermination_certificate,
    realization_boundary_no_go_certificate,
    semantic_weighting_underdetermination_certificate,
)


def test_semantic_weighting_is_not_forced_by_scale_label() -> None:
    receipt = semantic_weighting_underdetermination_certificate()
    assert receipt["same_scale_label"] is True
    assert receipt["same_residual_signature"] is True
    assert receipt["weights_distinct"] is True
    assert receipt["potentials_distinct"] is True
    assert receipt["unique_weighting_forced"] is False


def test_indexed_contraction_is_not_forced_by_rank_and_flat_payload() -> None:
    receipt = indexed_tensor_underdetermination_certificate()
    assert receipt["rank"] == (1, 1)
    assert receipt["component_count"] == 4
    assert receipt["multiple_slot_shapes"] is True
    assert receipt["contractions_distinct"] is True
    assert receipt["canonical_indexed_contraction_forced"] is False


def test_flat_tensor_payload_cannot_reconstruct_nonstrict_associator() -> None:
    receipt = monoidal_coherence_underdetermination_certificate()
    assert receipt["parenthesizations_distinct"] is True
    assert receipt["flat_payloads_equal"] is True
    assert receipt["flattening_injective"] is False
    assert receipt["associator_recoverable_from_flat_payload"] is False
    assert receipt["non_strict_coherence_forced"] is False


def test_realization_boundaries_close_by_no_go_not_hidden_defaults() -> None:
    receipt = realization_boundary_no_go_certificate()
    assert receipt == {
        "semantic_weighting_unique": False,
        "indexed_contraction_unique": False,
        "non_strict_coherence_forced": False,
        "all_are_realization_boundaries": True,
    }
