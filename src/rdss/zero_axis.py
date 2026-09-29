from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, pi
from typing import Iterable

from .algebra import wrap_phase


@dataclass(frozen=True)
class ZeroAxisPoint:
    """Finite point s=1/2+it and its projective unit-circle coordinate Omega(s)."""

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
    """Decompose an accumulated U(1) phase lift into turn count and residual.

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
    """Return topological winding only when the lifted U(1) path closes."""
    if closure_tolerance <= 0 or not isfinite(closure_tolerance):
        raise ValueError("closure_tolerance must be positive and finite")
    winding, residual = winding_and_residual(phases)
    if abs(residual) > closure_tolerance:
        raise ValueError(
            f"phase path is not closed: residual={residual!r} exceeds tolerance"
        )
    return winding
