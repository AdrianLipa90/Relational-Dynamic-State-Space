from fractions import Fraction

import pytest

from rdss.collatz_phase import (
    collatz_no_adjacent_odd_prefix,
    collatz_parity_prefix,
    collatz_phase_doubling_fraction,
    collatz_phase_square_residual,
    terminal_collatz_phase_fraction,
)
from rdss.primitive_persistence import source_minimal_parity_step


def test_terminal_phase_anchors_are_exact() -> None:
    assert terminal_collatz_phase_fraction(1) == Fraction(4, 7)
    assert terminal_collatz_phase_fraction(2) == Fraction(2, 7)
    assert terminal_collatz_phase_fraction(4) == Fraction(1, 7)


def test_tir_active_center_phase_values_are_exact() -> None:
    assert terminal_collatz_phase_fraction(6) == Fraction(141, 448)
    assert terminal_collatz_phase_fraction(12) == Fraction(141, 896)


def test_phase_doubling_is_exact_on_terminal_reaching_sample() -> None:
    for n in range(1, 501):
        q = terminal_collatz_phase_fraction(n)
        q_next = terminal_collatz_phase_fraction(source_minimal_parity_step(n))
        assert q_next == (2 * q) % 1
        assert collatz_phase_doubling_fraction(n) == q_next


def test_u1_phase_factor_squares_under_one_collatz_step() -> None:
    for n in (1, 2, 3, 4, 5, 6, 7, 9, 12, 27, 54, 97):
        assert collatz_phase_square_residual(n) <= 1e-12


def test_unreduced_collatz_language_forbids_adjacent_odd_symbols() -> None:
    for n in range(1, 501):
        assert collatz_no_adjacent_odd_prefix(n, 64)
        word = collatz_parity_prefix(n, 64)
        assert "11" not in "".join(map(str, word))


def test_phase_interface_fails_closed_without_claiming_global_convergence() -> None:
    with pytest.raises(RuntimeError):
        terminal_collatz_phase_fraction(27, max_steps=1)
    with pytest.raises(ValueError):
        terminal_collatz_phase_fraction(0)
    with pytest.raises(TypeError):
        terminal_collatz_phase_fraction(True)
    with pytest.raises(ValueError):
        collatz_parity_prefix(3, -1)
