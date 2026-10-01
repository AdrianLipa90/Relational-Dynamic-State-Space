from rdss.relational_collatz_generator import (
    GaussianPair,
    bombelli_ladder,
    cardano_bombelli_coefficients,
    collatz_coefficients_from_relation_algebra,
    derived_constants,
    durable_role_count,
    exact_generator_sanity,
    full_operator_dimension,
    minimal_universal_repair,
    nonidentity_operator_dimension,
    relational_collatz_depth_to_one,
    relational_collatz_step,
    relational_generator,
)


def test_binary_relation_algebra_fixes_2_3_1() -> None:
    q = durable_role_count()
    assert q == 2
    assert full_operator_dimension(q) == 4
    assert nonidentity_operator_dimension(q) == 3
    assert minimal_universal_repair(q) == 1
    assert collatz_coefficients_from_relation_algebra() == (2, 3, 1)


def test_binary_case_is_unique_for_residue_independent_constant_repair() -> None:
    assert minimal_universal_repair(2) == 1
    for q in range(3, 12):
        try:
            minimal_universal_repair(q)
        except ValueError:
            pass
        else:
            raise AssertionError(f"q={q} unexpectedly admitted a universal repair")


def test_generated_collatz_map_is_exact_standard_map() -> None:
    expected = {
        1: 4,
        2: 1,
        3: 10,
        4: 2,
        5: 16,
        6: 3,
        7: 22,
        8: 4,
        9: 28,
        10: 5,
    }
    for n, image in expected.items():
        assert relational_collatz_step(n) == image


def test_active_seed_and_l_constants_close_exactly() -> None:
    c = derived_constants()
    assert c.active_seed == 3
    assert c.l4 == 2
    assert c.l5 == 5
    assert c.l3 == 7
    assert relational_collatz_depth_to_one(c.active_seed) == c.l3
    assert relational_collatz_step(c.active_seed) == 10
    assert relational_collatz_step(10) == c.l5
    assert c.l3 == c.l4 + c.l5


def test_bombelli_generator_is_unique_up_to_conjugation() -> None:
    g = relational_generator(+1)
    gc = relational_generator(-1)
    assert g == GaussianPair(2, 1)
    assert gc == g.conjugate
    assert g.norm == gc.norm == 5


def test_bombelli_ladder_reproduces_3_4_5_and_7_24_25() -> None:
    g1, g2, g3, g4 = bombelli_ladder()
    assert g1 == GaussianPair(2, 1)
    assert g2 == GaussianPair(3, 4)
    assert g3 == GaussianPair(2, 11)
    assert g4 == GaussianPair(-7, 24)
    assert g2.norm == 25
    assert 3**2 + 4**2 == 5**2
    assert 7**2 + 24**2 == 25**2


def test_cardano_bombelli_polynomial_is_generated_exactly() -> None:
    linear, constant = cardano_bombelli_coefficients()
    assert (linear, constant) == (15, 4)

    x = 4
    assert x**3 - linear * x - constant == 0

    g = relational_generator()
    assert g**3 == GaussianPair(2, 11)
    assert g.conjugate**3 == GaussianPair(2, -11)


def test_generator_fourth_power_crosschecks_l3_and_24() -> None:
    c = derived_constants()
    g4 = relational_generator() ** full_operator_dimension()
    assert abs(g4.real) == c.l3
    assert abs(g4.imag) == 24


def test_exact_generator_sanity() -> None:
    assert exact_generator_sanity()
