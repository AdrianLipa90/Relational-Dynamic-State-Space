from __future__ import annotations

from cmath import exp
from fractions import Fraction
from math import pi

from .relational_collatz import relational_collatz_step, relational_l_constant_certificate


def terminal_collatz_cycle() -> tuple[int, int, int]:
    """Canonical nontrivial terminal cycle of the derived Collatz map."""

    cycle = (4, 2, 1)
    if tuple(relational_collatz_step(n) for n in cycle) != (2, 1, 4):
        raise AssertionError("derived Collatz map does not realize the 4-2-1 cycle")
    return cycle


def terminal_phase_denominator() -> int:
    """Primitive denominator forced by phase doubling around the 3-cycle."""

    length = len(terminal_collatz_cycle())
    return 2**length - 1


def terminal_phase_anchors() -> dict[int, Fraction]:
    """Derive q(4)=1/7, q(2)=2/7, q(1)=4/7 from the cycle itself.

    Up to orientation/conjugation, the minimal positive nonzero normalized
    phase on the terminal 3-cycle is 1/(2^3-1).
    """

    cycle = terminal_collatz_cycle()
    denominator = terminal_phase_denominator()
    q = Fraction(1, denominator)
    anchors: dict[int, Fraction] = {}
    for state in cycle:
        anchors[state] = q
        q = (2 * q) % 1

    if q != anchors[cycle[0]]:
        raise AssertionError("terminal phase did not close after one cycle")
    return anchors


def _positive_integer(value: int, name: str = "state") -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def collatz_parity(state: int) -> int:
    """Parity symbol of one positive integer state."""

    return _positive_integer(state) & 1


def parity_word_is_unreduced_collatz_admissible(bits: tuple[int, ...]) -> bool:
    """Exact local grammar: consecutive odd symbols 11 are forbidden."""

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("parity bits must be 0 or 1")
    return all(not (a == 1 and b == 1) for a, b in zip(bits, bits[1:]))


def fibonacci(index: int) -> int:
    if isinstance(index, bool) or not isinstance(index, int):
        raise TypeError("index must be an integer")
    if index < 0:
        raise ValueError("index must be non-negative")
    a, b = 0, 1
    for _ in range(index):
        a, b = b, a + b
    return a


def admissible_word_count(length: int) -> int:
    """Number of binary length-k words with no 11: F_{k+2}."""

    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError("length must be an integer")
    if length < 0:
        raise ValueError("length must be non-negative")

    end0, end1 = 1, 0
    for _ in range(length):
        end0, end1 = end0 + end1, end0
    return end0 + end1


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
        n = relational_collatz_step(n)
    return tuple(word)


def collatz_no_adjacent_odd_prefix(state: int, length: int) -> bool:
    """Check the exact local Collatz grammar: the word 11 is forbidden."""

    return parity_word_is_unreduced_collatz_admissible(
        collatz_parity_prefix(state, length)
    )


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
        if n in terminal_phase_anchors():
            q = terminal_phase_anchors()[n]
            break
        prefix.append(n & 1)
        n = relational_collatz_step(n)
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
    nxt = collatz_phase_factor(relational_collatz_step(n), max_steps=max_steps)
    return abs(nxt - current * current)

def terminal_phase_l3_closure() -> bool:
    """Exact crosscheck: terminal phase denominator equals relational L3."""

    return terminal_phase_denominator() == relational_l_constant_certificate()["L3"]


def collatz_phase_exact_sanity(limit: int = 256, prefix_length: int = 16) -> bool:
    """Finite exact sanity check; no global convergence claim."""

    m = _positive_integer(limit, "limit")
    if isinstance(prefix_length, bool) or not isinstance(prefix_length, int):
        raise TypeError("prefix_length must be an integer")
    if prefix_length < 1:
        raise ValueError("prefix_length must be positive")

    anchors = terminal_phase_anchors()
    if anchors != {4: Fraction(1, 7), 2: Fraction(2, 7), 1: Fraction(4, 7)}:
        return False
    if not terminal_phase_l3_closure():
        return False

    for n in range(1, m + 1):
        if not collatz_no_adjacent_odd_prefix(n, prefix_length):
            return False

    return all(
        admissible_word_count(k) == fibonacci(k + 2)
        for k in range(prefix_length + 1)
    )

