from __future__ import annotations

from dataclasses import dataclass
from math import acos, isfinite, pi
from typing import Callable, Iterable, Sequence, TypeVar

T = TypeVar("T")


def _finite_complex(z: complex) -> bool:
    return isfinite(z.real) and isfinite(z.imag)


def wrap_phase(angle: float) -> float:
    """Wrap a real phase to (-pi, pi]."""
    if not isfinite(angle):
        raise ValueError("phase must be finite")
    wrapped = (angle + pi) % (2.0 * pi) - pi
    return pi if wrapped == -pi else wrapped


@dataclass(frozen=True, order=True)
class RelationalPoint:
    """Minimal relational carrier.

    The root has an empty binary address. Refinement appends +1 or -1.
    No physical length scale is built into the point.
    """

    address: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if any(bit not in (-1, 1) for bit in self.address):
            raise ValueError("relational addresses use only -1/+1")

    @property
    def level(self) -> int:
        return len(self.address)

    def refine(self) -> tuple["RelationalPoint", "RelationalPoint"]:
        return (
            RelationalPoint(self.address + (-1,)),
            RelationalPoint(self.address + (1,)),
        )


@dataclass(frozen=True)
class CP1State:
    """Normalized representative of one point in CP^1.

    Global phase is not removed numerically; all invariant operations below
    depend only on the projective ray.
    """

    alpha: complex
    beta: complex

    def __post_init__(self) -> None:
        a = complex(self.alpha)
        b = complex(self.beta)
        if not (_finite_complex(a) and _finite_complex(b)):
            raise ValueError("CP1 amplitudes must be finite")
        norm2 = abs(a) ** 2 + abs(b) ** 2
        if norm2 <= 0.0:
            raise ValueError("the zero vector does not define a CP1 point")
        norm = norm2 ** 0.5
        object.__setattr__(self, "alpha", a / norm)
        object.__setattr__(self, "beta", b / norm)

    def overlap_abs(self, other: "CP1State") -> float:
        inner = self.alpha.conjugate() * other.alpha + self.beta.conjugate() * other.beta
        return min(1.0, max(0.0, abs(inner)))

    def fubini_study_distance(self, other: "CP1State") -> float:
        return acos(self.overlap_abs(other))

    def orthogonal_partner(self) -> "CP1State":
        return CP1State(-self.beta.conjugate(), self.alpha.conjugate())


@dataclass(frozen=True)
class MinimalDistinction:
    """A relation selecting two projective states over one relational point."""

    carrier: RelationalPoint
    left: CP1State
    right: CP1State
    label: str = "distinction"

    @property
    def separation(self) -> float:
        return self.left.fubini_study_distance(self.right)

    def is_maximal(self, tolerance: float = 1e-12) -> bool:
        if tolerance <= 0 or not isfinite(tolerance):
            raise ValueError("tolerance must be positive and finite")
        return abs(self.separation - (pi / 2.0)) <= tolerance


@dataclass(frozen=True)
class SemanticScale:
    label: str

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("semantic scale label must be non-empty")


@dataclass(frozen=True)
class SemanticScaleGraph:
    """A finite semantic coarse-graining relation.

    Each edge (child, parent) means that child may be coarsened to parent.
    The graph is a partial-order candidate; cycles are rejected.
    """

    edges: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if any(not a.strip() or not b.strip() for a, b in self.edges):
            raise ValueError("semantic scale labels must be non-empty")
        nodes = {x for edge in self.edges for x in edge}
        for node in nodes:
            if self._reachable(node, node, allow_zero=False):
                raise ValueError("semantic scale graph must be acyclic")

    def _parents(self, child: str) -> tuple[str, ...]:
        return tuple(parent for c, parent in self.edges if c == child)

    def _reachable(self, child: str, parent: str, *, allow_zero: bool = True) -> bool:
        if allow_zero and child == parent:
            return True
        frontier = list(self._parents(child))
        seen: set[str] = set()
        while frontier:
            current = frontier.pop()
            if current == parent:
                return True
            if current in seen:
                continue
            seen.add(current)
            frontier.extend(self._parents(current))
        return False

    def can_coarsen(self, child: str, parent: str) -> bool:
        return self._reachable(child, parent)

    def common_scale(self, labels: Sequence[str]) -> str | None:
        labels = tuple(labels)
        if not labels:
            raise ValueError("at least one semantic label is required")
        nodes = {x for edge in self.edges for x in edge} | set(labels)
        candidates = [n for n in nodes if all(self.can_coarsen(label, n) for label in labels)]
        if not candidates:
            return None
        minimal = [
            c for c in candidates
            if not any(c != d and self.can_coarsen(d, c) for d in candidates)
        ]
        return minimal[0] if len(minimal) == 1 else None


@dataclass(frozen=True)
class TensorScalarElement:
    """Typed tensor-scalar element of the relational algebra.

    Rank (0,0) is the scalar sector. Components are intentionally flat in the
    reference kernel; concrete tensor representations may supply richer shapes.
    """

    components: tuple[complex, ...]
    rank: tuple[int, int]
    carrier: RelationalPoint
    scale: SemanticScale

    def __post_init__(self) -> None:
        if not self.components:
            raise ValueError("an algebra element needs at least one component")
        vals = tuple(complex(v) for v in self.components)
        if not all(_finite_complex(v) for v in vals):
            raise ValueError("tensor-scalar components must be finite")
        p, q = self.rank
        if p < 0 or q < 0:
            raise ValueError("tensor ranks must be non-negative")
        object.__setattr__(self, "components", vals)

    @property
    def is_scalar(self) -> bool:
        return self.rank == (0, 0)

    def _require_same_sector(self, other: "TensorScalarElement") -> None:
        if not isinstance(other, TensorScalarElement):
            raise TypeError("operation requires TensorScalarElement")
        if (
            self.rank != other.rank
            or self.carrier != other.carrier
            or self.scale != other.scale
        ):
            raise ValueError("additive operations require the same typed sector")
        if len(self.components) != len(other.components):
            raise ValueError("additive operations require equal component dimensions")

    def __add__(self, other: "TensorScalarElement") -> "TensorScalarElement":
        self._require_same_sector(other)
        return TensorScalarElement(
            tuple(a + b for a, b in zip(self.components, other.components)),
            self.rank,
            self.carrier,
            self.scale,
        )

    def __sub__(self, other: "TensorScalarElement") -> "TensorScalarElement":
        self._require_same_sector(other)
        return TensorScalarElement(
            tuple(a - b for a, b in zip(self.components, other.components)),
            self.rank,
            self.carrier,
            self.scale,
        )

    def scale_by(self, scalar: complex) -> "TensorScalarElement":
        scalar = complex(scalar)
        if not _finite_complex(scalar):
            raise ValueError("scalar must be finite")
        return TensorScalarElement(
            tuple(scalar * value for value in self.components),
            self.rank,
            self.carrier,
            self.scale,
        )

    @property
    def additive_norm(self) -> float:
        return sum(abs(value) ** 2 for value in self.components) ** 0.5


@dataclass(frozen=True)
class TypedZero:
    """Algebraic zero typed by rank, semantic scale and refinement level.

    This is not the same object as absence of a relation or an empty carrier.
    """

    rank: tuple[int, int]
    scale: SemanticScale
    level: int

    def __post_init__(self) -> None:
        if self.rank[0] < 0 or self.rank[1] < 0 or self.level < 0:
            raise ValueError("zero type indices must be non-negative")


@dataclass(frozen=True)
class TypedRelation:
    source: RelationalPoint
    target: RelationalPoint
    label: str

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("relation label must be non-empty")


@dataclass(frozen=True)
class MoireRotation:
    """Relative orbital rotation; only the difference is intrinsic here."""

    theta_i: float
    theta_j: float

    def __post_init__(self) -> None:
        if not (isfinite(self.theta_i) and isfinite(self.theta_j)):
            raise ValueError("rotation angles must be finite")

    @property
    def delta(self) -> float:
        return wrap_phase(self.theta_i - self.theta_j)


@dataclass(frozen=True)
class ZeroAxisPoint:
    """Point s=1/2+it and its projective unit-circle coordinate Omega(s)."""

    t: float

    def __post_init__(self) -> None:
        if not isfinite(self.t):
            raise ValueError("zero-axis coordinate must be finite")

    @property
    def s(self) -> complex:
        return 0.5 + 1j * self.t

    @property
    def omega(self) -> complex:
        s = self.s
        return s / (1.0 - s)

    @property
    def unit_circle_residual(self) -> float:
        return abs(abs(self.omega) - 1.0)


def winding_and_residual(phases: Iterable[float]) -> tuple[int, float]:
    """Decompose an accumulated phase lift into nearest turn count and residual.

    For a non-closed path the integer is only a turn-count candidate, not a
    topological winding invariant. Use closed_path_winding for that claim.
    """
    total = 0.0
    for phase in phases:
        phase = float(phase)
        if not isfinite(phase):
            raise ValueError("phases must be finite")
        total += phase
    turn_count = round(total / (2.0 * pi))
    residual = wrap_phase(total - turn_count * 2.0 * pi)
    return turn_count, residual


def closed_path_winding(
    phases: Iterable[float],
    *,
    closure_tolerance: float = 1e-10,
) -> int:
    """Return topological winding only when the lifted phase path closes."""
    if closure_tolerance <= 0 or not isfinite(closure_tolerance):
        raise ValueError("closure_tolerance must be positive and finite")
    winding, residual = winding_and_residual(phases)
    if abs(residual) > closure_tolerance:
        raise ValueError(
            f"phase path is not closed: residual={residual!r} exceeds tolerance"
        )
    return winding


def commutator(product: Callable[[T, T], T], x: T, y: T) -> T:
    return product(x, y) - product(y, x)  # type: ignore[operator]


def associator(product: Callable[[T, T], T], x: T, y: T, z: T) -> T:
    return product(product(x, y), z) - product(x, product(y, z))  # type: ignore[operator]


def refinement_residual(
    refine: Callable[[T], T],
    product: Callable[[T, T], T],
    x: T,
    y: T,
    *,
    norm: Callable[[T], float] = abs,  # type: ignore[assignment]
) -> float:
    """Measure failure of exact product preservation under refinement."""
    delta = refine(product(x, y)) - product(refine(x), refine(y))  # type: ignore[operator]
    value = float(norm(delta))
    if not isfinite(value) or value < 0:
        raise ValueError("residual norm must be finite and non-negative")
    return value
