from itertools import combinations
from math import isclose, pi

import pytest

from rdss.algebraic_geometry_cell import (
    CUBE_FACE_COUNT,
    CUBE_VERTEX_COUNT,
    CUBE_VERTICES,
    OCTAHEDRAL_CORE_VERTEX_COUNT,
    OCTAHEDRAL_CORE_VERTICES,
    SPIN_HALF,
    TETRAHEDRON_NEGATIVE_VERTICES,
    TETRAHEDRON_POSITIVE_VERTICES,
    CubicCellComplex,
    CubicFrame,
    DynamicTetrahedronState,
    FaceAdjacency,
    Polarization,
    RelationalCubicCell,
    spin_half_phase_sign,
    squared_distance,
)
from rdss.orbital_information import KAPPA_PHI
from rdss.phase import U1Phase


def frame(cell_id: str) -> CubicFrame:
    return CubicFrame(cell_id=cell_id)


def cell(cell_id: str, plus: float = 0.0, minus: float = 0.0) -> RelationalCubicCell:
    return RelationalCubicCell(
        frame=frame(cell_id),
        positive=DynamicTetrahedronState(
            f"{cell_id}:T+",
            Polarization.POSITIVE,
            U1Phase.from_angle(plus),
            angular_offset=0.125,
        ),
        negative=DynamicTetrahedronState(
            f"{cell_id}:T-",
            Polarization.NEGATIVE,
            U1Phase.from_angle(minus),
            angular_offset=-0.125,
        ),
    )


def test_cubic_frame_is_exact_static_eight_vertex_six_face_cage() -> None:
    item = frame("c0")
    assert len(item.vertices) == CUBE_VERTEX_COUNT == 8
    assert len(item.faces) == CUBE_FACE_COUNT == 6
    assert item.vertices == CUBE_VERTICES


def test_stella_support_partitions_all_cube_vertices() -> None:
    item = cell("c0")
    positive = set(item.positive.support_vertices)
    negative = set(item.negative.support_vertices)

    assert len(positive) == 4
    assert len(negative) == 4
    assert positive.isdisjoint(negative)
    assert positive | negative == set(item.frame.vertices)
    assert item.stella_octangula_vertices == frozenset(item.frame.vertices)


def test_each_fixed_support_is_a_regular_tetrahedron() -> None:
    for support in (
        TETRAHEDRON_POSITIVE_VERTICES,
        TETRAHEDRON_NEGATIVE_VERTICES,
    ):
        pairwise = {
            squared_distance(left, right)
            for left, right in combinations(support, 2)
        }
        assert pairwise == {8}


def test_dynamic_tetrahedral_pair_carries_opposite_polarization_and_spin_half() -> None:
    item = cell("c0")
    assert item.positive.polarization == 1
    assert item.negative.polarization == -1
    assert item.positive.spin == SPIN_HALF
    assert item.negative.spin == SPIN_HALF
    assert item.stella_octangula_pair == (item.positive, item.negative)


def test_static_vertex_support_is_unchanged_when_dynamic_state_changes() -> None:
    before = cell("c0", 0.0, 0.0)
    after = RelationalCubicCell(
        frame=before.frame,
        positive=DynamicTetrahedronState(
            "c0:T+",
            Polarization.POSITIVE,
            U1Phase.from_angle(pi / 3.0),
            angular_offset=0.25,
        ),
        negative=DynamicTetrahedronState(
            "c0:T-",
            Polarization.NEGATIVE,
            U1Phase.from_angle(-pi / 5.0),
            angular_offset=-0.25,
        ),
    )

    assert before.frame == after.frame
    assert before.positive.support_vertices == after.positive.support_vertices
    assert before.negative.support_vertices == after.negative.support_vertices
    assert before.positive != after.positive
    assert before.negative != after.negative


def test_standard_stella_exposes_regular_octahedral_core() -> None:
    item = cell("c0")
    core = item.octahedral_core_vertices

    assert len(core) == OCTAHEDRAL_CORE_VERTEX_COUNT == 6
    assert core == OCTAHEDRAL_CORE_VERTICES

    for vertex in core:
        distances = sorted(
            squared_distance(vertex, other)
            for other in core
            if other != vertex
        )
        assert distances == [2, 2, 2, 2, 4]


def test_cell_action_is_canonical_information_action() -> None:
    item = cell("c0")
    assert isclose(item.information_action, KAPPA_PHI, rel_tol=0.0, abs_tol=1e-15)


def test_relative_phase_is_dynamic_not_structural() -> None:
    item = cell("c0", pi / 2.0, 0.0)
    assert isclose(item.relative_phase, pi / 2.0, abs_tol=1e-12)


def test_face_adjacency_builds_static_cubic_complex() -> None:
    left = cell("left")
    right = cell("right")
    adjacency = FaceAdjacency("left", "x+", "right", "x-")
    complex_ = CubicCellComplex((left, right), (adjacency,))

    assert complex_.static_frames == (left.frame, right.frame)
    assert len(complex_.dynamic_tetrahedra) == 4


def test_face_may_not_be_glued_twice() -> None:
    a = cell("a")
    b = cell("b")
    c = cell("c")

    with pytest.raises(ValueError):
        CubicCellComplex(
            (a, b, c),
            (
                FaceAdjacency("a", "x+", "b", "x-"),
                FaceAdjacency("a", "x+", "c", "x-"),
            ),
        )


def test_unknown_cube_face_fails_closed() -> None:
    a = cell("a")
    b = cell("b")

    with pytest.raises(ValueError):
        CubicCellComplex(
            (a, b),
            (FaceAdjacency("a", "not-a-face", "b", "x-"),),
        )


def test_spin_half_sign_requires_double_turn_for_full_return() -> None:
    assert spin_half_phase_sign(0.0) == 1
    assert spin_half_phase_sign(2.0 * pi) == -1
    assert spin_half_phase_sign(4.0 * pi) == 1


def test_spin_half_sign_rejects_non_integral_2pi_rotation() -> None:
    with pytest.raises(ValueError):
        spin_half_phase_sign(pi)
