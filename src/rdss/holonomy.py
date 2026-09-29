from __future__ import annotations

from cmath import exp as cexp
from dataclasses import dataclass
from math import isfinite, pi


def wrap_phase(angle: float) -> float:
    """Wrap a real angle to the interval (-pi, pi]."""
    if not isfinite(angle):
        raise ValueError("phase must be finite")
    wrapped = (angle + pi) % (2.0 * pi) - pi
    return pi if wrapped == -pi else wrapped


@dataclass(frozen=True)
class RelationalLoop:
    """Closed base-space path with semantic phase increments on its edges."""

    base_path: tuple[str, ...]
    edge_phases: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.base_path) < 2:
            raise ValueError("loop requires at least a start and end point")
        if self.base_path[0] != self.base_path[-1]:
            raise ValueError("base path must be closed")
        if len(self.edge_phases) != len(self.base_path) - 1:
            raise ValueError("one edge phase is required for each path edge")
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


@dataclass(frozen=True)
class ExperienceHolonomy:
    start_fibre: complex
    end_fibre: complex
    holonomy: complex
    residual_phase: float
    winding: int
    same_base_point: bool
    same_total_state: bool


def transport_experience(
    loop: RelationalLoop,
    start_fibre: complex = 1.0 + 0.0j,
    *,
    tolerance: float = 1e-12,
) -> ExperienceHolonomy:
    """Transport a U(1) reference fibre around a closed relational loop."""
    if tolerance <= 0 or not isfinite(tolerance):
        raise ValueError("tolerance must be positive and finite")
    if not (isfinite(start_fibre.real) and isfinite(start_fibre.imag)):
        raise ValueError("start fibre must be finite")

    h = loop.holonomy
    end = h * start_fibre
    same_fibre = abs(end - start_fibre) <= tolerance

    return ExperienceHolonomy(
        start_fibre=start_fibre,
        end_fibre=end,
        holonomy=h,
        residual_phase=loop.residual_phase,
        winding=loop.winding,
        same_base_point=True,
        same_total_state=same_fibre,
    )
