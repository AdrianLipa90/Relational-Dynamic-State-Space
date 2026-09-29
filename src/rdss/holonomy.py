from __future__ import annotations

from cmath import exp as cexp
from dataclasses import dataclass
from math import isfinite, pi
from typing import Sequence


def wrap_phase(angle: float) -> float:
    """Wrap a real angle to the interval (-pi, pi]."""
    if not isfinite(angle):
        raise ValueError("phase must be finite")
    wrapped = (angle + pi) % (2.0 * pi) - pi
    return pi if wrapped == -pi else wrapped


def _finite_complex(z: complex) -> bool:
    return isfinite(z.real) and isfinite(z.imag)


def _distance(a: Sequence[complex], b: Sequence[complex]) -> float:
    if len(a) != len(b):
        raise ValueError("projected states must have equal dimensions")
    return sum(abs(complex(x) - complex(y)) ** 2 for x, y in zip(a, b)) ** 0.5


@dataclass(frozen=True)
class RelationalHolonomyPath:
    """RDSS path whose closure is tested only after choosing a representation.

    The canonical carrier remains Hilbert-Moire. projected_start and
    projected_end are coordinates produced by any chosen representation.
    A representation may close while the transported internal state changes.
    """

    representation_name: str
    projected_start: tuple[complex, ...]
    projected_end: tuple[complex, ...]
    edge_phases: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.representation_name.strip():
            raise ValueError("representation name must be non-empty")
        if not self.projected_start or len(self.projected_start) != len(self.projected_end):
            raise ValueError("projected endpoints must have equal non-zero dimensions")
        if not all(_finite_complex(complex(v)) for v in self.projected_start + self.projected_end):
            raise ValueError("projected endpoints must be finite")
        if not self.edge_phases:
            raise ValueError("at least one holonomic phase increment is required")
        if not all(isfinite(float(x)) for x in self.edge_phases):
            raise ValueError("edge phases must be finite")

    @property
    def total_phase(self) -> float:
        return sum(float(x) for x in self.edge_phases)

    @property
    def winding(self) -> int:
        return round(self.total_phase / (2.0 * pi))

    @property
    def residual_phase(self) -> float:
        return wrap_phase(self.total_phase)

    @property
    def holonomy(self) -> complex:
        return cexp(1j * self.total_phase)

    def representation_closed(self, tolerance: float = 1e-12) -> bool:
        if tolerance <= 0 or not isfinite(tolerance):
            raise ValueError("tolerance must be positive and finite")
        return _distance(self.projected_start, self.projected_end) <= tolerance


@dataclass(frozen=True)
class HolonomyTransport:
    start_internal: complex
    end_internal: complex
    holonomy: complex
    residual_phase: float
    winding: int
    representation_closed: bool
    same_total_state: bool


def transport_holonomy(
    path: RelationalHolonomyPath,
    start_internal: complex = 1.0 + 0.0j,
    *,
    tolerance: float = 1e-12,
) -> HolonomyTransport:
    """Transport one reference internal degree around an RDSS path."""
    if tolerance <= 0 or not isfinite(tolerance):
        raise ValueError("tolerance must be positive and finite")
    if not _finite_complex(start_internal):
        raise ValueError("internal state must be finite")

    h = path.holonomy
    end = h * start_internal
    rep_closed = path.representation_closed(tolerance)
    same_internal = abs(end - start_internal) <= tolerance

    return HolonomyTransport(
        start_internal=start_internal,
        end_internal=end,
        holonomy=h,
        residual_phase=path.residual_phase,
        winding=path.winding,
        representation_closed=rep_closed,
        same_total_state=rep_closed and same_internal,
    )
