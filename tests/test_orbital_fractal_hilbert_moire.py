from math import pi

import pytest

from rdss.orbital_fractal_hilbert_moire import (
    CountableBranchAddress,
    HILBERT_HOTEL_FREDHOLM_INDEX,
    OFHM_RULE_DEPENDENCIES,
    OrbitalFractalHilbertMoireState,
    bees_overdamped_phase_step,
    binary_occurrence_to_countable,
    countable_word_rank,
    countable_word_unrank,
    euler_branch_preimage,
    euler_inverse_branch,
    euler_phase,
    hilbert_norm,
    idt_phase_dynamics_step,
    moire_cocycle_error,
    moire_transport,
    phase_coherence_overlap,
    phase_coupling_current,
    relative_moire_phase,
)


def test_countable_word_rank_is_bijective_on_reference_window():
    for rank in range(1024):
        word = countable_word_unrank(rank)
        assert countable_word_rank(word) == rank


def test_binary_occurrence_embeds_without_changing_branch_symbols():
    address = binary_occurrence_to_countable((-1, 1, -1))
    assert address.word == (-1, 1, -1)
    assert address.depth == 3


def test_hilbert_hotel_successor_is_rank_successor():
    address = CountableBranchAddress((1, -3, 2))
    successor = address.hilbert_hotel_successor()
    assert successor.rank == address.rank + 1
    assert successor.hilbert_hotel_predecessor() == address
    assert CountableBranchAddress().hilbert_hotel_predecessor() is None
    assert HILBERT_HOTEL_FREDHOLM_INDEX == 1


def test_euler_minus_one_is_exact_fixed_point_to_float_tolerance():
    assert euler_phase(-1).real == pytest.approx(-1.0)
    assert euler_phase(-1).imag == pytest.approx(0.0, abs=1e-12)


def test_euler_inverse_branches_reconstruct_same_phase_image():
    seed = 0.25 + 0.3j
    image = euler_phase(seed)
    for branch in (-3, -1, 0, 2, 5):
        preimage = euler_inverse_branch(image, branch)
        assert euler_phase(preimage) == pytest.approx(image)


def test_euler_branch_address_composes_inverse_branches():
    seed = -1.0 + 0.0j
    address = CountableBranchAddress((0, 1, -1))
    direct = euler_branch_preimage(seed, address)
    step = euler_inverse_branch(seed, 0)
    step = euler_inverse_branch(step, 1)
    step = euler_inverse_branch(step, -1)
    assert direct == pytest.approx(step)


def test_moire_relative_phase_is_exact_cocycle():
    assert moire_cocycle_error(0.2, 1.4, -2.7) < 1e-12
    assert relative_moire_phase(0.7, 0.7) == pytest.approx(1.0 + 0.0j)


def test_hilbert_moire_transport_preserves_norm_and_composes():
    vector = (1.0 + 2.0j, -0.5j, 3.0)
    transported_ji = moire_transport(
        vector,
        theta_target=1.2,
        theta_source=-0.4,
    )
    transported_kj = moire_transport(
        vector,
        theta_target=-0.4,
        theta_source=2.3,
    )
    direct_ki = moire_transport(
        vector,
        theta_target=1.2,
        theta_source=2.3,
    )
    composed = moire_transport(
        transported_kj,
        theta_target=1.2,
        theta_source=-0.4,
    )
    assert hilbert_norm(transported_ji) == pytest.approx(hilbert_norm(vector))
    assert composed == pytest.approx(direct_ki)


def test_bees_overlap_is_invariant_under_common_phase_shift():
    left = (0.1, 0.2, 0.4, 0.7)
    right = (-0.3, 0.5, 0.9, 1.1)
    shift = 7.25
    base = phase_coherence_overlap(left, right)
    shifted = phase_coherence_overlap(
        tuple(x + shift for x in left),
        tuple(x + shift for x in right),
    )
    assert shifted == pytest.approx(base)


def test_state_refinement_and_hotel_shift_are_distinct_operations():
    state = OrbitalFractalHilbertMoireState(
        CountableBranchAddress((0,)),
        "orbit-a",
        0.25,
        (1.0 + 0.0j, 1.0j),
    )
    refined = state.refine(7)
    shifted = state.hotel_successor()
    assert refined.address.word == (0, 7)
    assert shifted.address.rank == state.address.rank + 1
    assert refined.norm == pytest.approx(state.norm)
    assert shifted.norm == pytest.approx(state.norm)


def test_bees_overdamped_step_has_zero_current_at_alignment():
    phase = 1.1
    assert phase_coupling_current(phase, (phase, phase)) == pytest.approx(0.0)
    assert bees_overdamped_phase_step(
        phase,
        (phase, phase),
        coupling=2.0,
        dt=0.1,
    ) == pytest.approx(phase)


def test_idt_second_order_step_matches_declared_discrete_rule():
    state = OrbitalFractalHilbertMoireState(
        CountableBranchAddress((1, -1)),
        "orbit-b",
        0.4,
        (1.0 + 0.0j,),
        angular_velocity=0.3,
    )
    neighbors = (0.7, 1.2)
    dt = 0.05
    damping = 0.2
    gradient = 0.15
    drive = -0.1
    coupling = 1.3
    current = phase_coupling_current(
        state.phase,
        neighbors,
        normalize=False,
    )
    next_state = idt_phase_dynamics_step(
        state,
        neighbors,
        dt=dt,
        damping=damping,
        potential_gradient=gradient,
        drive=drive,
        coupling=coupling,
    )
    assert next_state.phase == pytest.approx(
        (0.4 + dt * 0.3) % (2.0 * pi)
    )
    expected_velocity = 0.3 + dt * (
        -gradient
        - damping * 0.3
        + coupling * current
        + drive
    )
    assert next_state.angular_velocity == pytest.approx(expected_velocity)


def test_ofhm_dependency_graph_matches_source_derivation_order():
    assert OFHM_RULE_DEPENDENCIES["symbolic_fractal_boundary"] == (
        "euler_symbolic_branch_space",
        "hilbert_hotel_shift",
    )
    assert OFHM_RULE_DEPENDENCIES["moire_cocycle"] == (
        "bees_relative_phase_coherence",
    )
    assert OFHM_RULE_DEPENDENCIES["hilbert_transport"] == ("moire_cocycle",)
    assert OFHM_RULE_DEPENDENCIES["phase_dynamics"] == (
        "bees_local_coupling",
        "idt_phase_update",
    )
