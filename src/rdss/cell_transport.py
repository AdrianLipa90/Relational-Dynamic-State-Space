from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .algebraic_geometry_cell import CUBE_FACES, CubeVertex, Polarization, RelationalCubicCell
from .phase import U1Phase

_FACE_AXIS = {"x": 0, "y": 1, "z": 2}
_AXIS_FACE = ("x", "y", "z")
_FACE_TANGENT_AXES = {0: (1, 2), 1: (2, 0), 2: (0, 1)}


@dataclass(frozen=True)
class FaceFrameTransport:
    """Signed-permutation transport from a source cube frame to a target frame."""

    permutation: tuple[int, int, int]
    signs: tuple[int, int, int]

    def __post_init__(self) -> None:
        if tuple(sorted(self.permutation)) != (0, 1, 2):
            raise ValueError("permutation must contain each cube axis exactly once")
        if len(self.signs) != 3 or any(sign not in (-1, 1) for sign in self.signs):
            raise ValueError("signs must contain exactly three values in {-1,+1}")

    @property
    def sector_character(self) -> int:
        return self.signs[0] * self.signs[1] * self.signs[2]

    @property
    def determinant(self) -> int:
        inversions = sum(
            self.permutation[i] > self.permutation[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
        permutation_sign = -1 if inversions % 2 else 1
        return permutation_sign * self.sector_character

    def apply_vertex(self, vertex: CubeVertex) -> CubeVertex:
        if len(vertex) != 3 or any(value not in (-1, 1) for value in vertex):
            raise ValueError("vertex must be a canonical cube vertex")
        return tuple(
            self.signs[index] * vertex[self.permutation[index]]
            for index in range(3)
        )

    def map_face(self, source_face: str) -> str:
        if source_face not in CUBE_FACES:
            raise ValueError("source_face must be a canonical cube face")
        source_axis = _FACE_AXIS[source_face[0]]
        source_sign = 1 if source_face[1] == "+" else -1
        target_axis = self.permutation.index(source_axis)
        target_sign = self.signs[target_axis] * source_sign
        suffix = "+" if target_sign == 1 else "-"
        return f"{_AXIS_FACE[target_axis]}{suffix}"

    def transport_polarization(self, polarization: Polarization) -> Polarization:
        if not isinstance(polarization, Polarization):
            raise TypeError("polarization must be Polarization")
        return Polarization(int(polarization) * self.sector_character)

    def tangent_orientation(self, source_face: str) -> int:
        if source_face not in CUBE_FACES:
            raise ValueError("source_face must be a canonical cube face")
        target_face = self.map_face(source_face)
        source_axis = _FACE_AXIS[source_face[0]]
        target_axis = _FACE_AXIS[target_face[0]]
        source_basis = _FACE_TANGENT_AXES[source_axis]
        target_basis = _FACE_TANGENT_AXES[target_axis]

        matrix = [[0, 0], [0, 0]]
        for row, target_coordinate in enumerate(target_basis):
            source_coordinate = self.permutation[target_coordinate]
            if source_coordinate not in source_basis:
                raise AssertionError("face transport failed to preserve tangent plane")
            column = source_basis.index(source_coordinate)
            matrix[row][column] = self.signs[target_coordinate]

        determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        if determinant not in (-1, 1):
            raise AssertionError("induced face transport must have determinant +/-1")
        return determinant


@dataclass(frozen=True)
class TransportedFaceAdjacency:
    """Face gluing with explicit right-to-left cube-frame transport."""

    left_cell: str
    left_face: str
    right_cell: str
    right_face: str
    transport: FaceFrameTransport

    def __post_init__(self) -> None:
        if not self.left_cell.strip() or not self.right_cell.strip():
            raise ValueError("adjacent cell ids must be non-empty")
        if self.left_cell == self.right_cell:
            raise ValueError("face adjacency requires two distinct cells")
        if self.left_face not in CUBE_FACES or self.right_face not in CUBE_FACES:
            raise ValueError("adjacency faces must be canonical cube faces")
        if not isinstance(self.transport, FaceFrameTransport):
            raise TypeError("transport must be FaceFrameTransport")
        mapped = self.transport.map_face(self.right_face)
        if mapped != self.left_face:
            raise ValueError(
                "frame transport must map right_face onto left_face: "
                f"{self.right_face}->{mapped}, expected {self.left_face}"
            )


@dataclass(frozen=True)
class StellaRelativeState:
    """Gauge-reduced state of the two fixed tetrahedral sectors in one cell."""

    phase: U1Phase
    angular_offset: float

    def __post_init__(self) -> None:
        if not isinstance(self.phase, U1Phase):
            raise TypeError("relative Stella phase must be U1Phase")
        if not isfinite(float(self.angular_offset)):
            raise ValueError("relative Stella angular offset must be finite")

    @property
    def phase_angle(self) -> float:
        return self.phase.angle


@dataclass(frozen=True)
class MoireEdgeState:
    """Gauge-reduced relational state carried by one oriented glued face."""

    left_cell: str
    right_cell: str
    sector_character: int
    tangent_orientation: int
    phase_mismatch: U1Phase
    angular_mismatch: float

    def __post_init__(self) -> None:
        if self.sector_character not in (-1, 1):
            raise ValueError("sector_character must be +/-1")
        if self.tangent_orientation not in (-1, 1):
            raise ValueError("tangent_orientation must be +/-1")
        if not isinstance(self.phase_mismatch, U1Phase):
            raise TypeError("phase_mismatch must be U1Phase")
        if not isfinite(float(self.angular_mismatch)):
            raise ValueError("angular_mismatch must be finite")

    @property
    def phase_angle(self) -> float:
        return self.phase_mismatch.angle


def stella_relative_state(cell: RelationalCubicCell) -> StellaRelativeState:
    if not isinstance(cell, RelationalCubicCell):
        raise TypeError("cell must be RelationalCubicCell")
    return StellaRelativeState(
        phase=cell.positive.phase.compose(cell.negative.phase.inverse()),
        angular_offset=(
            float(cell.positive.angular_offset)
            - float(cell.negative.angular_offset)
        ),
    )


def moire_edge_state(
    left: RelationalCubicCell,
    right: RelationalCubicCell,
    adjacency: TransportedFaceAdjacency,
) -> MoireEdgeState:
    """Derive Xi_e = delta_left * delta_right**(-eta) without a dynamics law."""

    if left.static_cell_id != adjacency.left_cell:
        raise ValueError("left cell does not match adjacency")
    if right.static_cell_id != adjacency.right_cell:
        raise ValueError("right cell does not match adjacency")

    left_state = stella_relative_state(left)
    right_state = stella_relative_state(right)
    eta = adjacency.transport.sector_character
    epsilon = adjacency.transport.tangent_orientation(adjacency.right_face)

    transported_right_phase = (
        right_state.phase if eta == 1 else right_state.phase.inverse()
    )
    phase_mismatch = left_state.phase.compose(transported_right_phase.inverse())
    angular_mismatch = (
        left_state.angular_offset
        - eta * epsilon * right_state.angular_offset
    )

    return MoireEdgeState(
        left_cell=left.static_cell_id,
        right_cell=right.static_cell_id,
        sector_character=eta,
        tangent_orientation=epsilon,
        phase_mismatch=phase_mismatch,
        angular_mismatch=angular_mismatch,
    )
