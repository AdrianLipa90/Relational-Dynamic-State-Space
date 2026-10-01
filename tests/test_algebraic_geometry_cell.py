from math import isclose, pi

import pytest

from rdss import (
    OCTAHEDRON_FACE_COUNT,
    OCTAHEDRON_VERTEX_COUNT,
    SPIN_HALF,
    DynamicTetrahedronState,
    FaceAdjacency,
    OctahedralCellComplex,
    OctahedralFrame,
    Polarization,
    RelationalOctahedralCell,
    spin_half_phase_sign,
)
from rdss.orbital_information import KAPPA_PHI
from rdss.phase import U1Phase


def frame(cell_id: str) -> OctahedralFrame:
    return OctahedralFrame(
        cell_id=cell_id,
        vertices=tuple(f"{cell_id}:v{i}" for i in range(OCTAHEDRON_VERTEX_COUNT)),
        faces=tuple(f"{cell_id}:f{i}" for i in range(OCTAHEDRON_FACE_COUNT)),
    )


def cell(cell_id: str, plus: float = 0.0, minus: float = 0.0) -> RelationalOctahedralCell:
    return RelationalOctahedralCell(
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


def test_octahedral_frame_is_exact_static_combinatorial_cage() -> None:
    item = frame("c0")
    assert len(item.vertices) == 6
    assert len(item.faces) == 8


def test_dynamic_tetrahedral_pair_carries_opposite_polarization_and_spin_half() -> None:
    item = cell("c0")
    assert item.positive.polarization == 1
    assert item.negative.polarization == -1
    assert item.positive.spin == SPIN_HALF
    assert item.negative.spin == SPIN_HALF
    assert item.stella_octangula_pair == (item.positive, item.negative)


def test_static_frame_is_unchanged_when_dynamic_state_changes() -> None:
    before = cell("c0", 0.0, 0.0)
    after = RelationalOctahedralCell(
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
    assert before.positive != after.positive
    assert before.negative != after.negative


def test_cell_action_is_canonical_information_action() -> None:
    item = cell("c0")
    assert isclose(item.information_action, KAPPA_PHI, rel_tol=0.0, abs_tol=1e-15)


def test_relative_phase_is_dynamic_not_structural() -> None:
    item = cell("c0", pi / 2.0, 0.0)
    assert isclose(item.relative_phase, pi / 2.0, abs_tol=1e-12)


def test_face_adjacency_builds_static_cell_complex() -> None:
    left = cell("left")
    right = cell("right")
    adjacency = FaceAdjacency(
        "left",
        left.frame.faces[0],
        "right",
        right.frame.faces[3],
    )
    complex_ = OctahedralCellComplex((left, right), (adjacency,))
    assert complex_.static_frames == (left.frame, right.frame)
    assert len(complex_.dynamic_tetrahedra) == 4


def test_face_may_not_be_glued_twice() -> None:
    a = cell("a")
    b = cell("b")
    c = cell("c")
    with pytest.raises(ValueError):
        OctahedralCellComplex(
            (a, b, c),
            (
                FaceAdjacency("a", a.frame.faces[0], "b", b.frame.faces[0]),
                FaceAdjacency("a", a.frame.faces[0], "c", c.frame.faces[0]),
            ),
        )


def test_unknown_face_fails_closed() -> None:
    a = cell("a")
    b = cell("b")
    with pytest.raises(ValueError):
        OctahedralCellComplex(
            (a, b),
            (FaceAdjacency("a", "not-a-face", "b", b.frame.faces[0]),),
        )


def test_spin_half_sign_requires_double_turn_for_full_return() -> None:
    assert spin_half_phase_sign(0.0) == 1
    assert spin_half_phase_sign(2.0 * pi) == -1
    assert spin_half_phase_sign(4.0 * pi) == 1


def test_spin_half_sign_rejects_non_integral_2pi_rotation() -> None:
    with pytest.raises(ValueError):
        spin_half_phase_sign(pi)
