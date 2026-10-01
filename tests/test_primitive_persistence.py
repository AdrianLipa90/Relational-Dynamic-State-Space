from math import isclose

import pytest

from rdss.primitive_persistence import (
    asymptotic_distinction,
    distinction_flow,
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
