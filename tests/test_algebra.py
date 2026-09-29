from math import pi

import pytest

from rdss import (
    CP1State,
    MinimalDistinction,
    MoireRotation,
    RelationalPoint,
    SemanticScale,
    SemanticScaleGraph,
    TensorScalarElement,
    TypedZero,
    ZeroAxisPoint,
    associator,
    closed_path_winding,
    commutator,
    refinement_residual,
    winding_and_residual,
)


def test_minimal_point_refines_recursively_without_physical_scale():
    root = RelationalPoint()
    minus, plus = root.refine()
    mm, mp = minus.refine()

    assert root.level == 0
    assert minus.address == (-1,)
    assert plus.address == (1,)
    assert mm.address == (-1, -1)
    assert mp.address == (-1, 1)


def test_cp1_fubini_study_maximal_distinction_is_pi_over_two():
    p = CP1State(1.0, 0.0)
    q = p.orthogonal_partner()
    distinction = MinimalDistinction(RelationalPoint(), p, q)

    assert distinction.separation == pytest.approx(pi / 2.0)
    assert distinction.is_maximal()


def test_cp1_nonmaximal_relation_has_smaller_fs_separation():
    p = CP1State(1.0, 0.0)
    q = CP1State(1.0, 1.0)

    assert 0.0 < p.fubini_study_distance(q) < pi / 2.0


def test_scalar_sector_is_tensor_rank_zero():
    scalar = TensorScalarElement(
        components=(3.0,),
        rank=(0, 0),
        carrier=RelationalPoint(),
        scale=SemanticScale("object"),
    )

    assert scalar.is_scalar


def test_typed_zero_is_not_empty_relation():
    zero = TypedZero(rank=(1, 1), scale=SemanticScale("object"), level=2)

    assert zero.rank == (1, 1)
    assert zero.level == 2


def test_semantic_scale_is_partial_order_like_coarse_graining():
    graph = SemanticScaleGraph(
        edges=(
            ("granny-smith", "apple"),
            ("apple", "fruit"),
            ("fruit", "food"),
            ("vegetable", "food"),
            ("food", "object"),
        )
    )

    assert graph.can_coarsen("granny-smith", "fruit")
    assert graph.common_scale(("fruit", "vegetable")) == "food"


def test_moire_is_relative_rotation_not_absolute_angle():
    a = MoireRotation(theta_i=0.75, theta_j=0.25)
    b = MoireRotation(theta_i=1.75, theta_j=1.25)

    assert a.delta == pytest.approx(0.5)
    assert b.delta == pytest.approx(0.5)


def test_zero_axis_projective_coordinate_lies_on_unit_circle():
    point = ZeroAxisPoint(t=14.134725)

    assert point.s.real == pytest.approx(0.5)
    assert abs(point.omega) == pytest.approx(1.0)
    assert point.unit_circle_residual == pytest.approx(0.0, abs=1e-14)


def test_phase_decomposition_keeps_nonzero_residual_for_open_path():
    turn_count, residual = winding_and_residual((pi, pi, 0.2))

    assert turn_count == 1
    assert residual == pytest.approx(0.2)


def test_topological_winding_requires_phase_closure():
    assert closed_path_winding((pi, pi)) == 1

    with pytest.raises(ValueError):
        closed_path_winding((pi, pi, 0.2))


def test_commutator_and_associator_are_diagnostics_not_axioms():
    product = lambda x, y: x * y

    assert commutator(product, 2.0, 3.0) == pytest.approx(0.0)
    assert associator(product, 2.0, 3.0, 4.0) == pytest.approx(0.0)


def test_refinement_residual_detects_exact_and_broken_self_similarity():
    product = lambda x, y: x + y
    exact_refine = lambda x: 2.0 * x
    broken_refine = lambda x: x * x

    assert refinement_residual(exact_refine, product, 2.0, 3.0) == pytest.approx(0.0)
    assert refinement_residual(broken_refine, product, 2.0, 3.0) > 0.0
