from math import isclose

import pytest

from rdss.primitive_persistence import (
    asymptotic_distinction,
    collatz_associate,
    collatz_association_balance,
    collatz_association_cycle,
    collatz_complete,
    collatz_dissociate,
    collatz_log_gain,
    collatz_persistence_regime,
    minimal_nontrivial_odd_multiplier,
    minimal_positive_odd_repair,
    source_minimal_association_divisor,
    source_minimal_collatz_coefficients,
    source_minimal_parity_step,
    distinction_flow,
    distinction_flow_from_collatz,
    distinction_potential,
    distinction_potential_dissipation,
    distinction_potential_gradient,
    distinction_solution,
    equilibrium_linear_rate,
    persistence_equilibria,
    persistence_regime,
)


def test_reference_flow_is_negative_gradient() -> None:
    for d, mu in ((0.2, -1.0), (0.7, 0.0), (0.3, 1.2), (1.7, 1.2)):
        assert isclose(
            distinction_flow(d, mu),
            -distinction_potential_gradient(d, mu),
            abs_tol=1e-15,
        )
        assert distinction_potential_dissipation(d, mu) <= 0.0


def test_dispersion_regime_has_zero_as_stable_nonnegative_equilibrium() -> None:
    mu = -0.75
    assert persistence_regime(mu) == "dispersion"
    assert persistence_equilibria(mu) == (0.0,)
    assert equilibrium_linear_rate(0.0, mu) < 0.0
    assert asymptotic_distinction(mu) == 0.0

    values = [distinction_solution(0.4, mu, t) for t in (0.0, 1.0, 4.0, 20.0)]
    assert all(value >= 0.0 for value in values)
    assert values == sorted(values, reverse=True)
    assert values[-1] < 1e-6


def test_structure_regime_has_positive_stable_equilibrium() -> None:
    mu = 1.25
    assert persistence_regime(mu) == "structure"
    assert persistence_equilibria(mu) == (0.0, mu)
    assert equilibrium_linear_rate(0.0, mu) > 0.0
    assert equilibrium_linear_rate(mu, mu) < 0.0
    assert asymptotic_distinction(mu) == mu

    assert isclose(distinction_solution(0.2, mu, 20.0), mu, rel_tol=0.0, abs_tol=1e-9)
    assert isclose(distinction_solution(2.0, mu, 20.0), mu, rel_tol=0.0, abs_tol=1e-9)


def test_critical_boundary_decays_algebraically_to_indistinction() -> None:
    assert persistence_regime(0.0) == "critical"
    assert persistence_equilibria(0.0) == (0.0,)
    assert equilibrium_linear_rate(0.0, 0.0) == 0.0
    assert distinction_solution(0.5, 0.0, 1000.0) < 1e-3


def test_reference_potential_orders_dispersion_and_structure_minima() -> None:
    assert distinction_potential(0.0, -1.0) == 0.0
    assert distinction_potential(0.0, 1.0) == 0.0
    assert distinction_potential(1.0, 1.0) < distinction_potential(0.0, 1.0)


def test_reference_flow_fails_closed_on_invalid_domain() -> None:
    with pytest.raises(ValueError):
        distinction_flow(-0.1, 1.0)
    with pytest.raises(ValueError):
        distinction_solution(0.1, 1.0, -1.0)
    with pytest.raises(ValueError):
        distinction_potential(float("nan"), 1.0)

def test_collatz_association_dissociation_cycle_is_exact() -> None:
    assert collatz_dissociate(3) == 9
    assert collatz_complete(9) == 10
    assert collatz_associate(10) == (5, 1)

    assert collatz_association_cycle(1) == (1, 2)
    assert collatz_association_cycle(3) == (5, 1)
    assert collatz_association_cycle(5) == (1, 4)
    assert collatz_association_cycle(7) == (11, 1)
    assert collatz_association_cycle(9) == (7, 2)


def test_collatz_balance_is_negative_local_log_gain() -> None:
    for n in (1, 3, 5, 7, 9, 15, 21, 27):
        assert isclose(
            collatz_association_balance(n),
            -collatz_log_gain(n),
            rel_tol=0.0,
            abs_tol=1e-15,
        )


def test_collatz_balance_classifies_association_and_dissociation_dominance() -> None:
    assert collatz_persistence_regime(1) == "critical"
    assert collatz_persistence_regime(3) == "dispersion"
    assert collatz_persistence_regime(5) == "structure"
    assert collatz_persistence_regime(7) == "dispersion"
    assert collatz_persistence_regime(9) == "structure"

    assert collatz_association_balance(3) < 0.0
    assert collatz_association_balance(5) > 0.0
    assert isclose(collatz_association_balance(1), 0.0, abs_tol=1e-15)


def test_collatz_derived_control_drives_reference_persistence_flow() -> None:
    d = 0.25
    assert distinction_flow_from_collatz(d, 3) < distinction_flow(d, 0.0)
    assert distinction_flow_from_collatz(d, 5) > distinction_flow(d, 0.0)


def test_collatz_local_balance_makes_no_global_convergence_claim() -> None:
    # Local exact identity only: mu_C(n) = ln(n / T_C(n)).
    from math import log

    for n in (3, 5, 7, 9, 11, 13):
        next_state, _ = collatz_association_cycle(n)
        assert isclose(
            collatz_association_balance(n),
            log(n / next_state),
            rel_tol=0.0,
            abs_tol=1e-15,
        )


def test_collatz_helpers_fail_closed() -> None:
    with pytest.raises(ValueError):
        collatz_dissociate(2)
    with pytest.raises(ValueError):
        collatz_association_cycle(0)
    with pytest.raises(ValueError):
        collatz_associate(9)
    with pytest.raises(TypeError):
        collatz_association_cycle(True)

def test_source_minimal_coefficients_are_exactly_two_three_one() -> None:
    assert source_minimal_association_divisor(2) == 2
    assert minimal_nontrivial_odd_multiplier() == 3
    assert minimal_positive_odd_repair() == 1
    assert source_minimal_collatz_coefficients(2) == (2, 3, 1)


def test_source_minimal_parity_step_equals_unreduced_collatz_on_positive_integers() -> None:
    for n in range(1, 1001):
        expected = n // 2 if n % 2 == 0 else 3 * n + 1
        assert source_minimal_parity_step(n) == expected


def test_existing_collatz_helpers_use_source_minimal_coefficients() -> None:
    divisor, multiplier, repair = source_minimal_collatz_coefficients()
    for n in (1, 3, 5, 7, 9, 11, 27):
        assert collatz_dissociate(n) == multiplier * n
        assert collatz_complete(collatz_dissociate(n)) == multiplier * n + repair
    assert divisor == 2


def test_source_minimal_signature_fails_closed_outside_canonical_dyad() -> None:
    with pytest.raises(ValueError):
        source_minimal_collatz_coefficients(1)
    with pytest.raises(ValueError):
        source_minimal_collatz_coefficients(3)
    with pytest.raises(ValueError):
        source_minimal_parity_step(5, role_count=3)
    with pytest.raises(ValueError):
        source_minimal_parity_step(0)
    with pytest.raises(TypeError):
        source_minimal_parity_step(True)

