from __future__ import annotations

from dataclasses import dataclass
import cmath
from math import isfinite, pi
from typing import Iterable


U1_TOLERANCE = 1e-10


@dataclass(frozen=True)
class U1Phase:
    """Explicit normalized point on the unit circle U(1)."""

    value: complex

    def __post_init__(self) -> None:
        raw = complex(self.value)
        if not (isfinite(raw.real) and isfinite(raw.imag)):
            raise ValueError("U1 phase must be finite")
        modulus = abs(raw)
        if modulus == 0.0:
            raise ValueError("zero is not a U1 phase")
        if abs(modulus - 1.0) > U1_TOLERANCE:
            raise ValueError("U1 phase must lie on the unit circle")
        object.__setattr__(self, "value", raw / modulus)

    @classmethod
    def from_angle(cls, angle: float) -> "U1Phase":
        value = float(angle)
        if not isfinite(value):
            raise ValueError("phase angle must be finite")
        return cls(cmath.exp(1j * value))

    @classmethod
    def from_turns(cls, turns: float) -> "U1Phase":
        value = float(turns)
        if not isfinite(value):
            raise ValueError("phase turns must be finite")
        return cls(cmath.exp(2j * pi * value))

    @property
    def angle(self) -> float:
        return wrap_phase(cmath.phase(self.value))

    @property
    def turns(self) -> float:
        return (self.angle / (2.0 * pi)) % 1.0

    def inverse(self) -> "U1Phase":
        return U1Phase(self.value.conjugate())

    def compose(self, other: "U1Phase") -> "U1Phase":
        if not isinstance(other, U1Phase):
            raise TypeError("other must be U1Phase")
        return U1Phase(self.value * other.value)


def wrap_phase(angle: float) -> float:
    """Wrap a finite real phase to (-pi, pi]."""
    if not isfinite(angle):
        raise ValueError("phase must be finite")
    wrapped = (angle + pi) % (2.0 * pi) - pi
    return pi if wrapped == -pi else wrapped


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
