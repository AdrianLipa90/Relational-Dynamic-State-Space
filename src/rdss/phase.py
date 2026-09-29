from __future__ import annotations

from math import isfinite, pi
from typing import Iterable


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
