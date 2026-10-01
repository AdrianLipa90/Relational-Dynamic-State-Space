from math import isclose, log

from rdss.existence_chain import (
    CANONICAL_EXISTENCE_CHAIN,
    FIRST_LAW_OF_EXISTENCE,
    IMAGINARY_GENERATOR,
    LN2,
    RELATIONAL_ZETA_ZERO,
    ExistenceChainStatus,
    FirstHamletOutcome,
    binary_entropy_nats,
    first_hamlet_outcomes,
    first_hamlet_classify,
    first_hamlet_complement,
    hartley_information_nats,
    first_hamlet_hartley_nats,
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
    hamlet_spinor_to_su2,
    hamlet_bloch_coordinates,
    hamlet_pauli_matrices,
    hamlet_su2_generators,
    hamlet_su2_commutator_residual,
    hamlet_su2_casimir_value,
    hamlet_su2_representation_label,
    hamlet_spinor_z_rotation,
    exact_chain_sanity,
    first_hamlet_swap_invariant_unit_vector,
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
    assert by_id["POTENTIAL_TO_PRIMITIVE_INDISTINCTION"].status is ExistenceChainStatus.DEFINITIONAL
    assert by_id["INDISTINCTION_TO_FIRST_HAMLET"].status is ExistenceChainStatus.EXACT_IDENTITY
    assert by_id["CANONICAL_FIRST_HAMLET_NONDEGENERATE"].status is ExistenceChainStatus.DEFINITIONAL
    assert by_id["STRICT_FIRST_HAMLET_NONDEGENERACY_GATE"].status is ExistenceChainStatus.DERIVATION_GATE
    assert by_id["FIRST_HAMLET_TO_Z2"].status is ExistenceChainStatus.CONDITIONAL_EXACT
    assert by_id["FIRST_HAMLET_TO_LN2"].status is ExistenceChainStatus.CONDITIONAL_EXACT
    assert by_id["DISPERSION_TO_INDISTINCTION"].status is ExistenceChainStatus.DEFINITIONAL
    assert by_id["STRUCTURE_TO_INFORMATION_POINT"].status is ExistenceChainStatus.MODEL_THEOREM
    assert by_id["BARE_POINT_NOT_FIRST_HAMLET"].status is ExistenceChainStatus.MODEL_THEOREM
    assert by_id["CANONICAL_HAMLET_RELATIONAL_REALIZATION"].status is ExistenceChainStatus.DEFINITIONAL
    assert by_id["HAMLET_TO_HALF_HALF"].status is ExistenceChainStatus.CONDITIONAL_EXACT
    assert by_id["SHANNON_LN2_CONSISTENCY"].status is ExistenceChainStatus.EXACT_IDENTITY
    assert by_id["Z2_TO_SIGN_CHARACTER"].status is ExistenceChainStatus.EXACT_IDENTITY
    assert by_id["ORIENTATION_TO_IMAGINARY_GENERATOR"].status is ExistenceChainStatus.CONDITIONAL_EXACT
    assert by_id["IMAGINARY_GENERATOR_TO_U1"].status is ExistenceChainStatus.EXACT_IDENTITY
    assert by_id["BINARY_PHASE_TO_CP1"].status is ExistenceChainStatus.STANDARD_GEOMETRY
    assert by_id["HAMLET_S3_TO_SU2"].status is ExistenceChainStatus.STANDARD_GEOMETRY
    assert by_id["HAMLET_SU2_QUOTIENT_TO_S2"].status is ExistenceChainStatus.STANDARD_GEOMETRY
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


def test_first_hamlet_is_dispersion_or_structure_and_hartley_ln2() -> None:
    assert first_hamlet_outcomes() == (
        FirstHamletOutcome.DISPERSION,
        FirstHamletOutcome.STRUCTURE,
    )
    assert first_hamlet_classify(False) is FirstHamletOutcome.DISPERSION
    assert first_hamlet_classify(True) is FirstHamletOutcome.STRUCTURE
    assert (
        first_hamlet_complement(FirstHamletOutcome.DISPERSION)
        is FirstHamletOutcome.STRUCTURE
    )
    assert (
        first_hamlet_complement(first_hamlet_complement(FirstHamletOutcome.DISPERSION))
        is FirstHamletOutcome.DISPERSION
    )
    assert isclose(hartley_information_nats(2), log(2.0), abs_tol=1e-15)
    assert isclose(first_hamlet_hartley_nats(), LN2, abs_tol=1e-15)


def test_swap_invariant_unit_vector_is_amplitude_geometry_not_probability() -> None:
    vector = first_hamlet_swap_invariant_unit_vector()
    scale = 1.0 / (2.0 ** 0.5)
    assert all(isclose(value, scale, abs_tol=1e-15) for value in vector)
    assert isclose(vector[0] ** 2 + vector[1] ** 2, 1.0, abs_tol=1e-15)


def test_probability_half_half_is_downstream_consistency_not_ln2_premise() -> None:
    assert branch_swap(-1) == 1
    assert branch_swap(1) == -1
    assert branch_swap(branch_swap(-1)) == -1
    assert branch_word_swap((-1, 1, -1)) == (1, -1, 1)
    assert branch_word_swap(branch_word_swap((-1, 1, -1))) == (-1, 1, -1)
    assert hamlet_distribution() == (0.5, 0.5)
    assert isclose(binary_entropy_nats(0.5), log(2.0), abs_tol=1e-15)
    assert isclose(hamlet_information_nats(), LN2, abs_tol=1e-15)
    assert isclose(hamlet_information_nats(), first_hamlet_hartley_nats(), abs_tol=1e-15)


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

def test_spinor_s3_maps_to_su2_and_balanced_orbit_projects_to_equator() -> None:
    for theta in (0.0, 0.17, 0.73, 1.31, 2.2, 3.0):
        coords = hamlet_operator_balanced_orbit(theta)
        matrix = hamlet_spinor_to_su2(coords)
        z0, z1 = coords

        assert abs(matrix[0][0] - z0) <= 1e-12
        assert abs(matrix[1][0] - z1) <= 1e-12

        col0_norm = abs(matrix[0][0]) ** 2 + abs(matrix[1][0]) ** 2
        col1_norm = abs(matrix[0][1]) ** 2 + abs(matrix[1][1]) ** 2
        inner = matrix[0][0].conjugate() * matrix[0][1] + matrix[1][0].conjugate() * matrix[1][1]
        determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        assert isclose(col0_norm, 1.0, abs_tol=1e-12)
        assert isclose(col1_norm, 1.0, abs_tol=1e-12)
        assert abs(inner) <= 1e-12
        assert abs(determinant - 1.0) <= 1e-12

        x, y, z = hamlet_bloch_coordinates(coords)
        assert isclose(x, __import__("math").cos(2.0 * theta), abs_tol=1e-12)
        assert isclose(y, -__import__("math").sin(2.0 * theta), abs_tol=1e-12)
        assert isclose(z, 0.0, abs_tol=1e-12)

