from __future__ import annotations

from cmath import exp
from fractions import Fraction
from math import pi

from .primitive_persistence import source_minimal_parity_step


_TERMINAL_PHASE = {
    1: Fraction(4, 7),
    2: Fraction(2, 7),
    4: Fraction(1, 7),
}


def _positive_integer(value: int, name: str = "state") -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def collatz_parity(state: int) -> int:
    """Parity symbol of one positive integer state."""

    return _positive_integer(state) & 1


def collatz_parity_prefix(state: int, length: int) -> tuple[int, ...]:
    """Finite parity itinerary of the source-minimal Collatz map."""

    n = _positive_integer(state)
    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError("length must be an integer")
    if length < 0:
        raise ValueError("length must be non-negative")

    word: list[int] = []
    for _ in range(length):
        word.append(n & 1)
        n = source_minimal_parity_step(n)
    return tuple(word)


def collatz_no_adjacent_odd_prefix(state: int, length: int) -> bool:
    """Check the exact local Collatz grammar: the word 11 is forbidden."""

    word = collatz_parity_prefix(state, length)
    return all(not (a == 1 and b == 1) for a, b in zip(word, word[1:]))


def terminal_collatz_phase_fraction(state: int, *, max_steps: int = 10000) -> Fraction:
    """Exact q_C(state) for a trajectory that reaches the terminal 4-2-1 cycle.

    The function is fail-closed: it makes no global Collatz-convergence claim.
    If a terminal anchor is not reached within max_steps, it raises.
    """

    n = _positive_integer(state)
    if isinstance(max_steps, bool) or not isinstance(max_steps, int):
        raise TypeError("max_steps must be an integer")
    if max_steps < 0:
        raise ValueError("max_steps must be non-negative")

    prefix: list[int] = []
    for _ in range(max_steps + 1):
        if n in _TERMINAL_PHASE:
            q = _TERMINAL_PHASE[n]
            break
        prefix.append(n & 1)
        n = source_minimal_parity_step(n)
    else:
        raise RuntimeError("terminal Collatz cycle not reached within max_steps")

    for bit in reversed(prefix):
        q = Fraction(bit, 2) + q / 2
    return q % 1


def collatz_phase_doubling_fraction(state: int, *, max_steps: int = 10000) -> Fraction:
    """Return 2*q_C(state) mod 1 as an exact rational."""

    return (2 * terminal_collatz_phase_fraction(state, max_steps=max_steps)) % 1


def collatz_phase_factor(state: int, *, max_steps: int = 10000) -> complex:
    """U(1) phase zeta_C=exp(2*pi*i*q_C) for a terminal-reaching trajectory."""

    q = terminal_collatz_phase_fraction(state, max_steps=max_steps)
    return exp(2j * pi * float(q))


def collatz_phase_square_residual(state: int, *, max_steps: int = 10000) -> float:
    """Numerical residual of zeta_C(Cn)=zeta_C(n)^2."""

    n = _positive_integer(state)
    current = collatz_phase_factor(n, max_steps=max_steps)
    nxt = collatz_phase_factor(source_minimal_parity_step(n), max_steps=max_steps)
    return abs(nxt - current * current)
