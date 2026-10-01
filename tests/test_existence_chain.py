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
    assert by_id["INFORMATIONALITY_TO_BINARY"].status is ExistenceChainStatus.CONDITIONAL_EXACT
    assert by_id["BINARY_TO_Z2_AUTOMORPHISM"].status is ExistenceChainStatus.EXACT_IDENTITY
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

