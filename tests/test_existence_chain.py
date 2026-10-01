from math import isclose, log

from rdss.existence_chain import (
    CANONICAL_EXISTENCE_CHAIN,
    FIRST_LAW_OF_EXISTENCE,
    IMAGINARY_GENERATOR,
    LN2,
    RELATIONAL_ZETA_ZERO,
    ExistenceChainStatus,
    binary_entropy_nats,
    branch_swap,
    branch_word_swap,
    branch_swap_vector,
    branch_polarity_vector,
    hamlet_complex_structure,
    hamlet_j_orbit,
    hamlet_j_orbit_derivative,
    hamlet_horizontal_residual,
    hamlet_projective_return_phase,
    hamlet_operator_module_coordinates,
    hamlet_operator_module_norm,
    hamlet_operator_balanced_orbit,
    hamlet_operator_balanced_orbit_derivative,
    hamlet_operator_horizontal_residual,
    hamlet_operator_to_real_branch_chart,
    hamlet_pauli_matrices,
    hamlet_su2_generators,
    hamlet_su2_commutator_residual,
    hamlet_su2_casimir_value,
    hamlet_su2_representation_label,
    hamlet_spinor_z_rotation,
    exact_chain_sanity,
    hamlet_distribution,
    hamlet_information_nats,
    relational_zero_center,
    spin_half_full_return,
    spin_half_sign_return,
    u1_phase,
    z2_nontrivial_real_character,
)


def test_first_law_does_not_reify_nothingness() -> None:
    text = FIRST_LAW_OF_EXISTENCE.lower()
    assert "not a realizable state" in text
    assert "object" in text
    assert "relation" in text


def test_pre_audit_chain_keeps_open_causal_arrows_explicit() -> None:
    by_id = {step.id: step for step in CANONICAL_EXISTENCE_CHAIN}

    assert by_id["L1_TO_EXISTENCE_POTENTIAL"].status is ExistenceChainStatus.DEFINITIONAL
    assert by_id["L1_MODEL_TO_MINIMAL_POINT"].status is ExistenceChainStatus.MODEL_THEOREM
    assert by_id["POINT_TO_INFORMATIONALITY"].status is ExistenceChainStatus.DERIVATION_GATE
    assert by_id["CANONICAL_REALIZED_EXISTENCE_INFORMATIONALITY"].status is ExistenceChainStatus.DEFINITIONAL
    assert by_id["INFORMATIONALITY_TO_BINARY"].status is ExistenceChainStatus.CONDITIONAL_EXACT
    assert by_id["BINARY_TO_Z2_AUTOMORPHISM"].status is ExistenceChainStatus.EXACT_IDENTITY
    assert by_id["CANONICAL_REALIZED_EXISTENCE_TO_HAMLET"].status is ExistenceChainStatus.CONDITIONAL_EXACT
    assert by_id["CANONICAL_HAMLET_RELATIONAL_REALIZATION"].status is ExistenceChainStatus.DEFINITIONAL
    assert by_id["EXISTENCE_POTENTIAL_TO_HAMLET"].status is ExistenceChainStatus.DERIVATION_GATE
    assert by_id["HAMLET_TO_HALF_HALF"].status is ExistenceChainStatus.CONDITIONAL_EXACT
    assert by_id["Z2_TO_SIGN_CHARACTER"].status is ExistenceChainStatus.EXACT_IDENTITY
    assert by_id["ORIENTATION_TO_IMAGINARY_GENERATOR"].status is ExistenceChainStatus.CONDITIONAL_EXACT

    assert by_id["HALF_HALF_TO_LN2"].status is ExistenceChainStatus.EXACT_IDENTITY
    assert by_id["IMAGINARY_GENERATOR_TO_U1"].status is ExistenceChainStatus.EXACT_IDENTITY
    assert by_id["BINARY_PHASE_TO_CP1"].status is ExistenceChainStatus.STANDARD_GEOMETRY
    assert by_id["CP1_GEOMETRY_TO_BERRY_PHASE"].status is ExistenceChainStatus.STANDARD_GEOMETRY
    assert (
        by_id["BERRY_PHASE_TO_CONNECTION_POTENTIAL_CLASS"].status
        is ExistenceChainStatus.CONDITIONAL_STANDARD_RESULT
    )
    assert by_id["HAMLET_TO_PROJECTIVE_SIGN_CLOSURE"].status is ExistenceChainStatus.CONDITIONAL_EXACT
    assert by_id["HAMLET_PAULI_TO_SU2"].status is ExistenceChainStatus.CONDITIONAL_EXACT
    assert by_id["SU2_CASIMIR_TO_HALF"].status is ExistenceChainStatus.CONDITIONAL_STANDARD_RESULT
    assert (
        by_id["BERRY_EULER_HAMLET_TO_SPIN_HALF"].status
        is ExistenceChainStatus.CONDITIONAL_STANDARD_RESULT
    )


def test_hamlet_symmetry_gives_half_half_and_ln2() -> None:
    assert branch_swap(-1) == 1
    assert branch_swap(1) == -1
    assert branch_swap(branch_swap(-1)) == -1
    assert branch_word_swap((-1, 1, -1)) == (1, -1, 1)
    assert branch_word_swap(branch_word_swap((-1, 1, -1))) == (-1, 1, -1)
    assert hamlet_distribution() == (0.5, 0.5)
    assert isclose(binary_entropy_nats(0.5), log(2.0), abs_tol=1e-15)
    assert isclose(hamlet_information_nats(), LN2, abs_tol=1e-15)


def test_relational_zero_is_midpoint_not_absolute_nothingness_marker() -> None:
    assert relational_zero_center(-1.0, 1.0) == RELATIONAL_ZETA_ZERO == 0.0


def test_z2_nontrivial_real_character_fixes_minus_one_sign() -> None:
    assert z2_nontrivial_real_character(1) == 1.0
    assert z2_nontrivial_real_character(-1) == -1.0
    assert z2_nontrivial_real_character(-1) ** 2 == 1.0


def test_swap_and_polarity_generate_real_complex_structure() -> None:
    vector = (2.0, -3.0)
    assert branch_swap_vector(vector) == (-3.0, 2.0)
    assert branch_polarity_vector(vector) == (-2.0, -3.0)
    assert hamlet_complex_structure(vector) == (-3.0, -2.0)
    assert hamlet_complex_structure(hamlet_complex_structure(vector)) == (-2.0, 3.0)


def test_imaginary_generator_and_u1_phase_are_exact() -> None:
    assert IMAGINARY_GENERATOR * IMAGINARY_GENERATOR == -1
    for angle in (0.0, 0.1, 1.0, 3.141592653589793, -2.7):
        assert isclose(abs(u1_phase(angle)), 1.0, abs_tol=1e-15)


def test_spin_half_has_2pi_sign_return_and_4pi_full_return() -> None:
    assert spin_half_sign_return()
    assert spin_half_full_return()


def test_exact_chain_sanity_does_not_claim_open_gates_closed() -> None:
    assert exact_chain_sanity()

def test_canonical_hamlet_j_orbit_is_horizontal_and_returns_with_minus_one() -> None:
    start = hamlet_j_orbit(0.0)
    mid = hamlet_j_orbit(3.141592653589793 / 2.0)
    end = hamlet_j_orbit(3.141592653589793)

    assert isclose(start[0], 1.0, abs_tol=1e-12)
    assert isclose(start[1], 0.0, abs_tol=1e-12)
    assert isclose(mid[0], 0.0, abs_tol=1e-12)
    assert isclose(abs(mid[1]), 1.0, abs_tol=1e-12)
    assert isclose(end[0], -1.0, abs_tol=1e-12)
    assert isclose(end[1], 0.0, abs_tol=1e-12)

    for theta in (0.0, 0.17, 0.73, 1.31, 2.2, 3.0):
        psi = hamlet_j_orbit(theta)
        dpsi = hamlet_j_orbit_derivative(theta)
        assert isclose(psi[0] * dpsi[0] + psi[1] * dpsi[1], 0.0, abs_tol=1e-12)
        assert isclose(hamlet_horizontal_residual(theta), 0.0, abs_tol=1e-12)

    assert hamlet_projective_return_phase() == -1.0

def test_operator_algebra_module_realizes_c2_without_duplicate_branch_copy() -> None:
    coords = hamlet_operator_module_coordinates(1.2, -0.7, 0.3, 2.1)
    assert coords == (complex(1.2, 2.1), complex(-0.7, 0.3))
    assert isclose(
        hamlet_operator_module_norm(coords),
        1.2**2 + 2.1**2 + (-0.7)**2 + 0.3**2,
        abs_tol=1e-12,
    )

    for theta in (0.0, 0.17, 0.73, 1.31, 2.2, 3.0):
        psi = hamlet_operator_balanced_orbit(theta)
        dpsi = hamlet_operator_balanced_orbit_derivative(theta)
        assert isclose(hamlet_operator_module_norm(psi), 1.0, abs_tol=1e-12)
        direct = psi[0].conjugate() * dpsi[0] + psi[1].conjugate() * dpsi[1]
        assert abs(direct) <= 1e-12
        assert abs(hamlet_operator_horizontal_residual(theta)) <= 1e-12

        chart = hamlet_operator_to_real_branch_chart(psi)
        real_chart = tuple(complex(v) for v in hamlet_j_orbit(theta))
        assert all(abs(a - b) <= 1e-12 for a, b in zip(chart, real_chart))

    start = hamlet_operator_balanced_orbit(0.0)
    end = hamlet_operator_balanced_orbit(3.141592653589793)
    assert all(abs(e + a) <= 1e-12 for a, e in zip(start, end))

def test_hamlet_pauli_su2_casimir_forces_half_representation_label() -> None:
    sigma_x, sigma_y, sigma_z = hamlet_pauli_matrices()
    assert sigma_x == ((0j, 1 + 0j), (1 + 0j, 0j))
    assert sigma_z == ((1 + 0j, 0j), (0j, -1 + 0j))
    assert sigma_y == ((0j, -1j), (1j, 0j))

    assert len(hamlet_su2_generators()) == 3
    assert hamlet_su2_commutator_residual() <= 1e-12
    assert isclose(hamlet_su2_casimir_value(), 0.75, abs_tol=1e-12)
    assert isclose(hamlet_su2_representation_label(), 0.5, abs_tol=1e-12)

    rot_2pi = hamlet_spinor_z_rotation(2.0 * 3.141592653589793)
    rot_4pi = hamlet_spinor_z_rotation(4.0 * 3.141592653589793)
    assert all(abs(value + 1.0) <= 1e-12 for value in rot_2pi)
    assert all(abs(value - 1.0) <= 1e-12 for value in rot_4pi)

