from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class InfoHolonomicCoordinate:
    """Complex informational-holonomic fibre coordinate zeta = I + i*Theta.

    I is an informational coordinate and Theta is a holonomic coordinate.
    This is an internal RDSS fibre coordinate, not an asserted extra
    spacetime dimension.
    """

    information: float
    holonomic: float

    def __post_init__(self) -> None:
        if not (isfinite(self.information) and isfinite(self.holonomic)):
            raise ValueError("informational-holonomic coordinates must be finite")

    @property
    def zeta(self) -> complex:
        return complex(self.information, self.holonomic)


@dataclass(frozen=True)
class MinkowskiMoirePoint:
    """One event of the Lorentzian Hilbert-Moire base plus fibre state."""

    t: float
    x: float
    y: float
    z: float
    fibre: InfoHolonomicCoordinate

    def __post_init__(self) -> None:
        if not all(isfinite(v) for v in (self.t, self.x, self.y, self.z)):
            raise ValueError("Minkowski coordinates must be finite")


def minkowski_interval_sq(
    p: MinkowskiMoirePoint,
    q: MinkowskiMoirePoint,
    *,
    c: float = 299_792_458.0,
) -> float:
    """Return eta(Delta x, Delta x) for signature (-,+,+,+)."""
    if c <= 0 or not isfinite(c):
        raise ValueError("c must be positive and finite")
    dt = q.t - p.t
    dx = q.x - p.x
    dy = q.y - p.y
    dz = q.z - p.z
    return -(c * dt) ** 2 + dx * dx + dy * dy + dz * dz


@dataclass(frozen=True)
class CosmicRelationalStep:
    """One cosmic RDSS step with separate base, semantic, and context phases.

    No physical example value is canonical here. Context phase is a generic
    slot for any explicitly defined external or environmental relation.
    """

    base_phase: float
    semantic_phase: float
    context_phase: float = 0.0

    def __post_init__(self) -> None:
        if not all(isfinite(v) for v in (self.base_phase, self.semantic_phase, self.context_phase)):
            raise ValueError("all phase contributions must be finite")

    @property
    def total_phase(self) -> float:
        return self.base_phase + self.semantic_phase + self.context_phase


def accumulated_holonomic_phase(steps: tuple[CosmicRelationalStep, ...]) -> float:
    return sum(step.total_phase for step in steps)
