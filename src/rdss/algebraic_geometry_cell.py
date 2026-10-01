from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from math import isfinite, pi

from .orbital_information import KAPPA_PHI
from .phase import U1Phase, wrap_phase


OCTAHEDRON_VERTEX_COUNT = 6
OCTAHEDRON_FACE_COUNT = 8
TETRAHEDRON_VERTEX_COUNT = 4
SPIN_HALF = 0.5
SPINOR_SIGN_RETURN = 2.0 * pi
SPINOR_FULL_RETURN = 4.0 * pi


class Polarization(IntEnum):
    NEGATIVE = -1
    POSITIVE = 1


@dataclass(frozen=True)
class OctahedralFrame:
    """Static local cage used only as a combinatorial/geometric frame.

    Coordinates are intentionally absent. This object records the agreed
    static octahedral frame without imposing an embedding that has not yet
    been derived.
    """

    cell_id: str
    vertices: tuple[str, ...]
    faces: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.cell_id.strip():
            raise ValueError("cell_id must be non-empty")
        if len(self.vertices) != OCTAHEDRON_VERTEX_COUNT:
            raise ValueError("an octahedral frame must expose exactly 6 vertices")
        if len(set(self.vertices)) != len(self.vertices):
            raise ValueError("octahedral frame vertices must be unique")
        if any(not vertex.strip() for vertex in self.vertices):
            raise ValueError("octahedral frame vertices must be non-empty")
        if len(self.faces) != OCTAHEDRON_FACE_COUNT:
            raise ValueError("an octahedral frame must expose exactly 8 faces")
        if len(set(self.faces)) != len(self.faces):
            raise ValueError("octahedral frame faces must be unique")
        if any(not face.strip() for face in self.faces):
            raise ValueError("octahedral frame faces must be non-empty")


@dataclass(frozen=True)
class DynamicTetrahedronState:
    """Dynamic tetrahedral degree of freedom inside one static frame.

    The object records only state variables already fixed by the current
    algebraic-geometric map: polarization, U(1) phase and an angular offset.
    No vertex-to-frame coordinate embedding is assumed here.
    """

    label: str
    polarization: Polarization
    phase: U1Phase
    angular_offset: float = 0.0

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("tetrahedron label must be non-empty")
        if not isfinite(float(self.angular_offset)):
            raise ValueError("angular_offset must be finite")

    @property
    def spin(self) -> float:
        return SPIN_HALF


@dataclass(frozen=True)
class RelationalOctahedralCell:
    """Closed local cell: static octahedral cage plus dynamic tetrahedral pair."""

    frame: OctahedralFrame
    positive: DynamicTetrahedronState
    negative: DynamicTetrahedronState
    def __post_init__(self) -> None:
        if self.positive.polarization is not Polarization.POSITIVE:
            raise ValueError("positive tetrahedron must carry + polarization")
        if self.negative.polarization is not Polarization.NEGATIVE:
            raise ValueError("negative tetrahedron must carry - polarization")
        if self.positive.label == self.negative.label:
            raise ValueError("the two dynamic tetrahedra must have distinct labels")
        if not isinstance(self.positive.phase, U1Phase):
            raise TypeError("positive tetrahedron phase must be U1Phase")
        if not isinstance(self.negative.phase, U1Phase):
            raise TypeError("negative tetrahedron phase must be U1Phase")

    @property
    def information_action(self) -> float:
        return KAPPA_PHI

    @property
    def stella_octangula_pair(
        self,
    ) -> tuple[DynamicTetrahedronState, DynamicTetrahedronState]:
        """Symbolic two-tetrahedron compound before coordinate embedding."""
        return (self.positive, self.negative)

    @property
    def relative_phase(self) -> float:
        return wrap_phase(self.positive.phase.angle - self.negative.phase.angle)

    @property
    def static_cell_id(self) -> str:
        return self.frame.cell_id


@dataclass(frozen=True)
class FaceAdjacency:
    """Face-to-face adjacency of two distinct static octahedral frames."""

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
class OctahedralCellComplex:
    """Static adjacency graph of octahedral frames.

    This is deliberately a face-adjacency complex, not a claim that regular
    octahedra alone tile Euclidean 3-space. Euclidean realization remains a
    separate derivation gate.
    """

    cells: tuple[RelationalOctahedralCell, ...]
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
                raise ValueError("left adjacency references an unknown face")
            if adjacency.right_face not in right_frame.faces:
                raise ValueError("right adjacency references an unknown face")

            left_key = (adjacency.left_cell, adjacency.left_face)
            right_key = (adjacency.right_cell, adjacency.right_face)
            if left_key in used_faces or right_key in used_faces:
                raise ValueError("a static face may participate in at most one glued pair")
            used_faces.add(left_key)
            used_faces.add(right_key)

    @property
    def static_frames(self) -> tuple[OctahedralFrame, ...]:
        return tuple(cell.frame for cell in self.cells)

    @property
    def dynamic_tetrahedra(self) -> tuple[DynamicTetrahedronState, ...]:
        return tuple(
            tetra
            for cell in self.cells
            for tetra in (cell.positive, cell.negative)
        )


def spin_half_phase_sign(rotation: float, tolerance: float = 1e-12) -> int:
    """Reference spin-1/2 sign under integral 2*pi turns.

    Returns +1 for 4*pi-equivalent rotations and -1 for 2*pi-equivalent
    rotations. Non-integral 2*pi rotations are rejected rather than rounded.
    """

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
