from math import log, pi, sin

import pytest

from rdss.alternating_phase_dynamics import (
    BINARY_INFORMATION_NATS,
    CANONICAL_PAIR_POTENTIAL_AMPLITUDE,
    DIRECTED_CHANNEL_COUNT,
    DIRECTED_CHANNEL_INFORMATION_NATS,
    KAPPA,
    UNDIRECTED_EXCHANGE_PAIR_COUNT,
    UNDIRECTED_PAIR_INFORMATION_NATS,
    MoireEdge,
    StellaHalfOccurrence,
    bipolar_pair_forces_from_delta,
    canonical_kuramoto_lyapunov_rate,
    canonical_kuramoto_velocity,
    canonical_moire_gradient,
    canonical_moire_information_potential,
    canonical_pair_gradient_from_delta,
    canonical_pair_information_potential_from_delta,
    center_phase_residual,
    chordal_mismatch_cost,
    closure_certificate,
    pendulum_frame_residual,
    pendulum_frame_successor,
    phase_mismatch,
    relative_pendulum_residual,
    second_frame_difference,
)


def test_half_successor_is_exact_square_root_of_full_successor() -> None:
    state = StellaHalfOccurrence(0, 1)
    half = state.half_successor()
    full = half.half_successor()

    assert state.grade == pytest.approx(0.0)
    assert half.grade == pytest.approx(0.5)
    assert full.grade == pytest.approx(1.0)
    assert half == StellaHalfOccurrence(0, -1)
    assert full == StellaHalfOccurrence(1, 1)


def test_frame_order_is_discrete_but_phase_carrier_remains_continuous() -> None:
    state = StellaHalfOccurrence(7, -1)
    assert state.grade == pytest.approx(7.5)

    # Arbitrary real phases remain admissible between discrete occurrence grades.
    assert phase_mismatch(0.123456789, -1.987654321) == pytest.approx(
        phase_mismatch(0.123456789 + 2.0 * pi, -1.987654321)
    )


def test_kappa_and_channel_information_normalizations_are_exact_to_float_tolerance() -> None:
    assert DIRECTED_CHANNEL_COUNT == 24
    assert UNDIRECTED_EXCHANGE_PAIR_COUNT == 12
    assert BINARY_INFORMATION_NATS == pytest.approx(log(2.0))
    assert KAPPA == pytest.approx(log(2.0) / (24.0 * pi))
    assert DIRECTED_CHANNEL_INFORMATION_NATS == pytest.approx(log(2.0) / 24.0)
    assert UNDIRECTED_PAIR_INFORMATION_NATS == pytest.approx(log(2.0) / 12.0)
    assert CANONICAL_PAIR_POTENTIAL_AMPLITUDE == pytest.approx(log(2.0) / 24.0)
    assert CANONICAL_PAIR_POTENTIAL_AMPLITUDE == pytest.approx(pi * KAPPA)


def test_chordal_cost_zero_alignment_and_unit_half_turn() -> None:
    assert chordal_mismatch_cost(0.0) == pytest.approx(0.0)
    assert chordal_mismatch_cost(pi) == pytest.approx(1.0)
    assert canonical_pair_information_potential_from_delta(0.0) == pytest.approx(0.0)
    assert canonical_pair_information_potential_from_delta(pi) == pytest.approx(
        log(2.0) / 12.0
    )


def test_twelve_half_turn_pairs_saturate_binary_information_budget() -> None:
    total = UNDIRECTED_EXCHANGE_PAIR_COUNT * canonical_pair_information_potential_from_delta(pi)
    assert total == pytest.approx(log(2.0))


def test_pair_gradient_is_sine_and_forces_cancel_at_relational_center() -> None:
    delta = 0.83
    expected_gradient = (log(2.0) / 24.0) * sin(delta)
    assert canonical_pair_gradient_from_delta(delta) == pytest.approx(expected_gradient)

    force_plus, force_minus = bipolar_pair_forces_from_delta(delta)
    assert force_plus == pytest.approx(-expected_gradient)
    assert force_minus == pytest.approx(expected_gradient)
    assert force_plus + force_minus == pytest.approx(0.0)


def test_relative_pair_equations_split_into_inertial_center_and_pendulum() -> None:
    inertia = 2.3
    damping = 0.0
    delta = 0.61
    delta_acceleration = -(
        2.0 * CANONICAL_PAIR_POTENTIAL_AMPLITUDE * sin(delta) / inertia
    )

    assert relative_pendulum_residual(
        delta,
        0.4,
        delta_acceleration,
        phase_inertia=inertia,
        damping=damping,
    ) == pytest.approx(0.0)

    # Conservative center has no interaction acceleration.
    assert center_phase_residual(
        1.7,
        0.0,
        phase_inertia=inertia,
        damping=0.0,
    ) == pytest.approx(0.0)


def test_second_frame_difference_is_unique_expected_stencil_behavior() -> None:
    # Constants and affine drift are annihilated.
    assert second_frame_difference(3.0, 3.0, 3.0) == pytest.approx(0.0)
    assert second_frame_difference(4.0, 7.0, 10.0) == pytest.approx(0.0)

    # A quadratic n^2 has constant second difference 2.
    assert second_frame_difference(0.0, 1.0, 4.0) == pytest.approx(2.0)


def test_frame_native_pendulum_successor_has_zero_residual() -> None:
    previous = 0.2
    current = 0.35
    inertia = 1.7
    step = 1.0
    following = pendulum_frame_successor(
        previous,
        current,
        phase_inertia=inertia,
        full_step=step,
    )
    assert pendulum_frame_residual(
        previous,
        current,
        following,
        phase_inertia=inertia,
        full_step=step,
    ) == pytest.approx(0.0)


def test_two_node_moire_gradient_is_same_pair_sine_force() -> None:
    phases = (0.7, -0.2)
    edges = (MoireEdge(0, 1),)
    delta = phase_mismatch(phases[0], phases[1])

    gradient = canonical_moire_gradient(phases, edges)
    g = canonical_pair_gradient_from_delta(delta)

    assert gradient == pytest.approx((g, -g))
    assert sum(gradient) == pytest.approx(0.0)


def test_overdamped_moire_is_kuramoto_gradient_flow() -> None:
    phases = (0.2, 1.1, -0.6)
    edges = (
        MoireEdge(0, 1),
        MoireEdge(1, 2),
        MoireEdge(2, 0),
    )
    damping = (1.0, 2.0, 3.0)

    gradient = canonical_moire_gradient(phases, edges)
    velocity = canonical_kuramoto_velocity(phases, edges, damping=damping)

    for g, v, eta in zip(gradient, velocity, damping):
        assert eta * v == pytest.approx(-g)

    rate = canonical_kuramoto_lyapunov_rate(
        phases,
        edges,
        damping=damping,
    )
    assert rate <= 0.0
    assert rate == pytest.approx(
        -sum(g * g / eta for g, eta in zip(gradient, damping))
    )


def test_moire_potential_is_gauge_shift_invariant() -> None:
    phases = (0.2, 0.7, 1.8)
    edges = (
        MoireEdge(0, 1, 0.1),
        MoireEdge(1, 2, -0.3),
    )
    base = canonical_moire_information_potential(phases, edges)
    shifted = canonical_moire_information_potential(
        tuple(x + 4.23 for x in phases),
        edges,
    )
    assert shifted == pytest.approx(base)


def test_closure_certificate_is_consistent() -> None:
    receipt = closure_certificate()
    assert receipt["directed_channels"] == 24
    assert receipt["undirected_pairs"] == 12
    assert receipt["pair_amplitude_equals_pi_kappa"] is True
    assert receipt["half_grade"] == pytest.approx(0.5)
    assert receipt["full_grade"] == pytest.approx(1.0)
    assert receipt["half_squared_is_full_successor"] is True
    assert receipt["pair_force_sum_zero"] is True
    assert receipt["half_turn_pair_potential"] == pytest.approx(log(2.0) / 12.0)
    assert receipt["full_binary_budget_at_all_12_half_turn_pairs"] == pytest.approx(log(2.0))
