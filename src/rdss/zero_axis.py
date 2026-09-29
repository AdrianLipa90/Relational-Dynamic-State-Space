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



def finite_zero_axis_lift(
    phase: complex,
    *,
    tolerance: float = 1e-10,
) -> ZeroAxisPoint:
    """Lift a verified finite U(1) phase through Omega^{-1}(u)=u/(1+u).

    The exceptional phase u=-1 is the compactified point at infinity and has
    no finite ZeroAxisPoint representative.
    """
    if tolerance <= 0 or not isfinite(tolerance):
        raise ValueError("tolerance must be positive and finite")
    u = complex(phase)
    if not (isfinite(u.real) and isfinite(u.imag)):
        raise ValueError("phase must be finite")
    modulus = abs(u)
    if modulus == 0.0 or abs(modulus - 1.0) > tolerance:
        raise ValueError("Zero-Axis lift requires a U(1) phase")
    u /= modulus
    if abs(1.0 + u) <= tolerance:
        raise ValueError("phase u=-1 corresponds to compactified Zero-Axis infinity")
    s = u / (1.0 + u)
    if abs(s.real - 0.5) > 10.0 * tolerance:
        raise ValueError("inverse projective image left the Zero Axis")
    return ZeroAxisPoint(float(s.imag))
