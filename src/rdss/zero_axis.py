from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


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
