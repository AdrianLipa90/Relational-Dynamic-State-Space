from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from math import isfinite, pi

from .orbital_information import KAPPA_PHI
from .phase import U1Phase, wrap_phase


CUBE_VERTEX_COUNT = 8
CUBE_FACE_COUNT = 6
TETRAHEDRON_VERTEX_COUNT = 4
OCTAHEDRAL_CORE_VERTEX_COUNT = 6

SPIN_HALF = 0.5
SPINOR_SIGN_RETURN = 2.0 * pi
SPINOR_FULL_RETURN = 4.0 * pi

CubeVertex = tuple[int, int, int]
CoreVertex = tuple[int, int, int]

CUBE_VERTICES: tuple[CubeVertex, ...] = tuple(
    (x, y, z)
    for x in (-1, 1)
    for y in (-1, 1)
    for z in (-1, 1)
)
CUBE_FACES: tuple[str, ...] = ("x-", "x+", "y-", "y+", "z-", "z+")

TETRAHEDRON_POSITIVE_VERTICES: tuple[CubeVertex, ...] = tuple(
    vertex
    for vertex in CUBE_VERTICES
    if vertex[0] * vertex[1] * vertex[2] == 1
)
TETRAHEDRON_NEGATIVE_VERTICES: tuple[CubeVertex, ...] = tuple(
    vertex
    for vertex in CUBE_VERTICES
    if vertex[0] * vertex[1] * vertex[2] == -1
)

OCTAHEDRAL_CORE_VERTICES: tuple[CoreVertex, ...] = (
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1),
)


class Polarization(IntEnum):
    NEGATIVE = -1
    POSITIVE = 1


@dataclass(frozen=True)
class CubicFrame:
    """Static local cage for the Stella Octangula support geometry.

    The canonical local embedding is the cube with vertices
    (±1, ±1, ±1). The frame is structural and does not move when local
    tetrahedral state variables change.
    """

    cell_id: str
    vertices: tuple[CubeVertex, ...] = CUBE_VERTICES
    faces: tuple[str, ...] = CUBE_FACES

    def __post_init__(self) -> None:
        if not self.cell_id.strip():
            raise ValueError("cell_id must be non-empty")
        if tuple(self.vertices) != CUBE_VERTICES:
            raise ValueError("cubic frame must use the canonical 8 cube vertices")
        if tuple(self.faces) != CUBE_FACES:
            raise ValueError("cubic frame must use the canonical 6 cube faces")


@dataclass(frozen=True)
class DynamicTetrahedronState:
    """Dynamic state carried by one fixed tetrahedral support.

    The support vertices are fixed cube vertices. Dynamics are carried by
    polarization, U(1) phase and angular state; this object does not move the
    support geometry.
    """

    label: str
    polarization: Polarization
    phase: U1Phase
    angular_offset: float = 0.0

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("tetrahedron label must be non-empty")
        if not isinstance(self.phase, U1Phase):
            raise TypeError("tetrahedron phase must be U1Phase")
        if not isfinite(float(self.angular_offset)):
            raise ValueError("angular_offset must be finite")

    @property
    def spin(self) -> float:
        return SPIN_HALF

    @property
    def support_vertices(self) -> tuple[CubeVertex, ...]:
        if self.polarization is Polarization.POSITIVE:
            return TETRAHEDRON_POSITIVE_VERTICES
        if self.polarization is Polarization.NEGATIVE:
            return TETRAHEDRON_NEGATIVE_VERTICES
        raise ValueError("unsupported polarization")


@dataclass(frozen=True)
class RelationalCubicCell:
    """Closed local cell: static cube, Stella pair, octahedral core."""

    frame: CubicFrame
    positive: DynamicTetrahedronState
    negative: DynamicTetrahedronState

    def __post_init__(self) -> None:
        if self.positive.polarization is not Polarization.POSITIVE:
            raise ValueError("positive tetrahedron must carry + polarization")
        if self.negative.polarization is not Polarization.NEGATIVE:
            raise ValueError("negative tetrahedron must carry - polarization")
        if self.positive.label == self.negative.label:
            raise ValueError("the two tetrahedral states must have distinct labels")
        if set(self.positive.support_vertices) & set(self.negative.support_vertices):
            raise ValueError("Stella tetrahedral supports must be disjoint")
        if (
            set(self.positive.support_vertices)
            | set(self.negative.support_vertices)
        ) != set(self.frame.vertices):
            raise ValueError("Stella vertices must exhaust the cubic frame vertices")

    @property
    def information_action(self) -> float:
        return KAPPA_PHI

    @property
    def stella_octangula_pair(
        self,
    ) -> tuple[DynamicTetrahedronState, DynamicTetrahedronState]:
        return (self.positive, self.negative)

    @property
    def stella_octangula_vertices(self) -> frozenset[CubeVertex]:
        return frozenset(
            self.positive.support_vertices + self.negative.support_vertices
        )

    @property
    def octahedral_core_vertices(self) -> tuple[CoreVertex, ...]:
        """Canonical central octahedral core of the standard Stella embedding."""
        return OCTAHEDRAL_CORE_VERTICES

    @property
    def relative_phase(self) -> float:
        return wrap_phase(self.positive.phase.angle - self.negative.phase.angle)

    @property
    def static_cell_id(self) -> str:
        return self.frame.cell_id


@dataclass(frozen=True)
class FaceAdjacency:
    """Face-to-face adjacency of two distinct static cubic frames."""

    left_cell: str
    left_face: str
    right_cell: str
    right_face: str

    def __post_init__(self) -> None:
        if not self.left_cell.strip() or not self.right_cell.strip():
            raise ValueError("adjacent cell ids must be non-empty")
        if self.left_cell == self.right_cell:
            raise ValueError("face adjacency requires two distinct cells")
        if not self.left_face.strip() or not self.right_face.strip():
            raise ValueError("adjacent face ids must be non-empty")


@dataclass(frozen=True)
class CubicCellComplex:
    """Static face-adjacency complex of cubic information cells."""

    cells: tuple[RelationalCubicCell, ...]
    adjacencies: tuple[FaceAdjacency, ...]

    def __post_init__(self) -> None:
        by_id = {cell.static_cell_id: cell for cell in self.cells}
        if len(by_id) != len(self.cells):
            raise ValueError("cell ids must be unique")

        used_faces: set[tuple[str, str]] = set()
        for adjacency in self.adjacencies:
            if adjacency.left_cell not in by_id or adjacency.right_cell not in by_id:
                raise ValueError("face adjacency references an unknown cell")
            left_frame = by_id[adjacency.left_cell].frame
            right_frame = by_id[adjacency.right_cell].frame
            if adjacency.left_face not in left_frame.faces:
                raise ValueError("left adjacency references an unknown cube face")
            if adjacency.right_face not in right_frame.faces:
                raise ValueError("right adjacency references an unknown cube face")

            left_key = (adjacency.left_cell, adjacency.left_face)
            right_key = (adjacency.right_cell, adjacency.right_face)
            if left_key in used_faces or right_key in used_faces:
                raise ValueError("a static face may participate in at most one glued pair")
            used_faces.add(left_key)
            used_faces.add(right_key)

    @property
    def static_frames(self) -> tuple[CubicFrame, ...]:
        return tuple(cell.frame for cell in self.cells)

    @property
    def dynamic_tetrahedra(self) -> tuple[DynamicTetrahedronState, ...]:
        return tuple(
            tetra
            for cell in self.cells
            for tetra in (cell.positive, cell.negative)
        )


def squared_distance(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
) -> int:
    return sum((a - b) ** 2 for a, b in zip(left, right))


def spin_half_phase_sign(rotation: float, tolerance: float = 1e-12) -> int:
    """Reference spin-1/2 sign under integral 2*pi turns."""

    value = float(rotation)
    tol = float(tolerance)
    if not isfinite(value):
        raise ValueError("rotation must be finite")
    if not isfinite(tol) or tol <= 0.0:
        raise ValueError("tolerance must be positive and finite")

    turns = value / SPINOR_SIGN_RETURN
    nearest = round(turns)
    if abs(turns - nearest) > tol:
        raise ValueError("rotation must be an integral multiple of 2*pi")
    return -1 if nearest % 2 else 1
