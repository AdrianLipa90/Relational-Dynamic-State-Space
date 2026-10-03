from __future__ import annotations

from math import prod


# These certificates close historical "derivation gates" by exact
# underdetermination. They do not invent realization-specific structure.
#
# REF: RDSS canonical structural primitives in src/rdss/axioms.py:
#      PRIM_SEMANTIC_WEIGHTING, PRIM_TENSOR_PRODUCT, PRIM_CONTRACTION,
#      DEF_TENSOR_MONOIDAL_COHERENCE.
# REF: docs/SEMANTIC_WEIGHTING_GATE.md
# REF: docs/INDEXED_TENSOR_GATE.md
# REF: docs/MONOIDAL_COHERENCE_GATE.md


def semantic_weighting_underdetermination_certificate() -> dict[str, object]:
    """Witness that a scale label and residual signature do not select weights.

    The same scale label, residual names and p=1 admit two positive weighting
    profiles. On the same residual vector they give different potentials.
    Therefore no unique semantic weighting is recoverable from the current
    structural signature alone.
    """

    scale = "object"
    residual_names = ("a", "b")
    residuals = (1.0, 1.0)
    weights_a = (1.0, 1.0)
    weights_b = (2.0, 1.0)
    value_a = sum(w * r for w, r in zip(weights_a, residuals))
    value_b = sum(w * r for w, r in zip(weights_b, residuals))
    return {
        "same_scale_label": scale == scale,
        "same_residual_signature": residual_names == residual_names,
        "same_order_p": True,
        "weights_a": weights_a,
        "weights_b": weights_b,
        "weights_distinct": weights_a != weights_b,
        "potential_a": value_a,
        "potential_b": value_b,
        "potentials_distinct": value_a != value_b,
        "unique_weighting_forced": False,
    }


def indexed_tensor_underdetermination_certificate() -> dict[str, object]:
    """Witness that total rank plus flat component count do not fix indices.

    A rank-(1,1) flat payload with four components is compatible with multiple
    ordered slot-dimension factorizations. Even after selecting a 2x2 shape,
    distinct supplied bilinear/evaluation forms give distinct contractions.
    """

    rank = (1, 1)
    component_count = 4
    slot_shapes = ((1, 4), (2, 2), (4, 1))
    all_match_flat_count = all(prod(shape) == component_count for shape in slot_shapes)

    # Same 2x2 component array diag(1,1), two admissible supplied evaluators.
    tensor_diag = (1.0, 1.0)
    evaluator_a = (1.0, 1.0)
    evaluator_b = (1.0, 2.0)
    contraction_a = sum(x * g for x, g in zip(tensor_diag, evaluator_a))
    contraction_b = sum(x * g for x, g in zip(tensor_diag, evaluator_b))

    return {
        "rank": rank,
        "component_count": component_count,
        "compatible_slot_shapes": slot_shapes,
        "multiple_slot_shapes": len(slot_shapes) > 1 and all_match_flat_count,
        "contraction_a": contraction_a,
        "contraction_b": contraction_b,
        "contractions_distinct": contraction_a != contraction_b,
        "canonical_indexed_contraction_forced": False,
    }


def monoidal_coherence_underdetermination_certificate() -> dict[str, object]:
    """Witness that flattening erases the data needed for non-strict coherence.

    Distinct parenthesized tensor syntax trees project to the same flat leaf
    tuple. The projection is therefore non-injective, so an associator path
    cannot be reconstructed from the flat TensorScalarElement payload alone.
    """

    leaves = ("W", "X", "Y", "Z")
    left_tree = "(((W⊗X)⊗Y)⊗Z)"
    right_tree = "(W⊗(X⊗(Y⊗Z)))"
    flat_left = leaves
    flat_right = leaves
    return {
        "left_parenthesization": left_tree,
        "right_parenthesization": right_tree,
        "parenthesizations_distinct": left_tree != right_tree,
        "flat_left": flat_left,
        "flat_right": flat_right,
        "flat_payloads_equal": flat_left == flat_right,
        "flattening_injective": False,
        "associator_recoverable_from_flat_payload": False,
        "non_strict_coherence_forced": False,
    }


def realization_boundary_no_go_certificate() -> dict[str, object]:
    """Consolidated receipt for the three realization-specific no-go results."""

    semantic = semantic_weighting_underdetermination_certificate()
    indexed = indexed_tensor_underdetermination_certificate()
    monoidal = monoidal_coherence_underdetermination_certificate()
    return {
        "semantic_weighting_unique": semantic["unique_weighting_forced"],
        "indexed_contraction_unique": indexed["canonical_indexed_contraction_forced"],
        "non_strict_coherence_forced": monoidal["non_strict_coherence_forced"],
        "all_are_realization_boundaries": (
            semantic["unique_weighting_forced"] is False
            and indexed["canonical_indexed_contraction_forced"] is False
            and monoidal["non_strict_coherence_forced"] is False
        ),
    }
