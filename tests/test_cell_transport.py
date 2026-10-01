from math import isclose, pi

import pytest

from rdss.algebraic_geometry_cell import (
    CubicFrame,
    DynamicTetrahedronState,
    Polarization,
    RelationalCubicCell,
)
from rdss.cell_transport import (
    FaceFrameTransport,
    TransportedFaceAdjacency,
    moire_edge_state,
    stella_relative_state,
)
from rdss.phase import U1Phase, wrap_phase


def cell(
    cell_id: str,
    *,
    plus_phase: float = 0.0,
    minus_phase: float = 0.0,
    plus_angle: float = 0.0,
    minus_angle: float = 0.0,
) -> RelationalCubicCell:
    return RelationalCubicCell(
        frame=CubicFrame(cell_id),
        positive=DynamicTetrahedronState(
            f"{cell_id}:T+",
            Polarization.POSITIVE,
            U1Phase.from_angle(plus_phase),
            angular_offset=plus_angle,
        ),
        negative=DynamicTetrahedronState(
            f"{cell_id}:T-",
            Polarization.NEGATIVE,
            U1Phase.from_angle(minus_phase),
            angular_offset=minus_angle,
        ),
    )


def swap_x_faces() -> FaceFrameTransport:
    return FaceFrameTransport(
        permutation=(0, 1, 2),
        signs=(-1, 1, 1),
    )


def preserve_x_faces_quarter_turn() -> FaceFrameTransport:
    return FaceFrameTransport(
        permutation=(0, 2, 1),
        signs=(-1, -1, 1),
    )


def adjacency(transport: FaceFrameTransport) -> TransportedFaceAdjacency:
    return TransportedFaceAdjacency(
        left_cell="left",
        left_face="x+",
        right_cell="right",
        right_face="x-",
        transport=transport,
    )


def test_same_face_pair_does_not_determine_stella_sector_transport() -> None:
    swap = swap_x_faces()
    preserve = preserve_x_faces_quarter_turn()

    assert swap.map_face("x-") == "x+"
    assert preserve.map_face("x-") == "x+"

    assert swap.sector_character == -1
    assert preserve.sector_character == 1

    assert (
        swap.transport_polarization(Polarization.POSITIVE)
        is Polarization.NEGATIVE
    )
    assert (
        preserve.transport_polarization(Polarization.POSITIVE)
        is Polarization.POSITIVE
    )


def test_face_transport_exposes_induced_d4_orientation() -> None:
    quarter_turn = preserve_x_faces_quarter_turn()
    reflection = FaceFrameTransport(
        permutation=(0, 2, 1),
        signs=(-1, 1, 1),
    )

    assert quarter_turn.tangent_orientation("x-") == 1
    assert reflection.tangent_orientation("x-") == -1


def test_transported_adjacency_fails_closed_on_wrong_face_map() -> None:
    with pytest.raises(ValueError):
        TransportedFaceAdjacency(
            left_cell="left",
            left_face="x+",
            right_cell="right",
            right_face="x-",
            transport=FaceFrameTransport(
                permutation=(0, 1, 2),
                signs=(1, 1, 1),
            ),
        )


def test_stella_relative_state_removes_common_u1_phase() -> None:
    base = cell(
        "c0",
        plus_phase=pi / 2.0,
        minus_phase=pi / 7.0,
        plus_angle=0.4,
        minus_angle=-0.2,
    )
    shifted = cell(
        "c0",
        plus_phase=pi / 2.0 + 0.731,
        minus_phase=pi / 7.0 + 0.731,
        plus_angle=0.4,
        minus_angle=-0.2,
    )

    left = stella_relative_state(base)
    right = stella_relative_state(shifted)

    assert isclose(
        wrap_phase(left.phase_angle - right.phase_angle),
        0.0,
        abs_tol=1e-12,
    )
    assert isclose(left.angular_offset, right.angular_offset, abs_tol=1e-12)


def test_moire_edge_phase_uses_forced_sector_character() -> None:
    left = cell("left", plus_phase=pi / 2.0, minus_phase=0.0)
    right = cell("right", plus_phase=pi / 4.0, minus_phase=0.0)

    swapped = moire_edge_state(left, right, adjacency(swap_x_faces()))
    preserved = moire_edge_state(
        left,
        right,
        adjacency(preserve_x_faces_quarter_turn()),
    )

    assert swapped.sector_character == -1
    assert isclose(swapped.phase_angle, 3.0 * pi / 4.0, abs_tol=1e-12)

    assert preserved.sector_character == 1
    assert isclose(preserved.phase_angle, pi / 4.0, abs_tol=1e-12)


def test_moire_edge_is_invariant_under_independent_common_cell_phase_shifts() -> None:
    left = cell("left", plus_phase=0.8, minus_phase=-0.2)
    right = cell("right", plus_phase=-0.1, minus_phase=0.35)
    edge = adjacency(preserve_x_faces_quarter_turn())

    shifted_left = cell(
        "left",
        plus_phase=0.8 + 1.17,
        minus_phase=-0.2 + 1.17,
    )
    shifted_right = cell(
        "right",
        plus_phase=-0.1 - 0.63,
        minus_phase=0.35 - 0.63,
    )

    base = moire_edge_state(left, right, edge)
    shifted = moire_edge_state(shifted_left, shifted_right, edge)

    assert isclose(
        wrap_phase(base.phase_angle - shifted.phase_angle),
        0.0,
        abs_tol=1e-12,
    )


def test_angular_mismatch_uses_sector_and_face_orientation_signs() -> None:
    left = cell("left", plus_angle=0.15, minus_angle=-0.05)
    right = cell("right", plus_angle=0.4, minus_angle=-0.2)

    swapped = moire_edge_state(left, right, adjacency(swap_x_faces()))
    preserved = moire_edge_state(
        left,
        right,
        adjacency(preserve_x_faces_quarter_turn()),
    )

    assert isclose(swapped.angular_mismatch, 0.8, abs_tol=1e-12)
    assert isclose(preserved.angular_mismatch, -0.4, abs_tol=1e-12)
