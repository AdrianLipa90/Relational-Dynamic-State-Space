from rdss.gaussian_bombelli import (
    GaussianPair,
    bombelli_cubic_root_certificate,
    bombelli_ladder,
    collatz_coefficients_from_gaussian_generator,
    gaussian_l_constant_closure_crosscheck,
    gaussian_recurrence_residual,
    gaussian_recurrence_term,
    l_constants_from_gaussian_and_root_extension,
    minimal_relation_role_gaussian_generator,
)


def test_minimal_gaussian_generator_and_powers_are_exact() -> None:
    g = minimal_relation_role_gaussian_generator()
    assert g == GaussianPair(2, 1)
    assert g.conjugate() == GaussianPair(2, -1)
    assert g.norm() == 5

    assert bombelli_ladder() == (
        GaussianPair(2, 1),
        GaussianPair(3, 4),
        GaussianPair(2, 11),
        GaussianPair(-7, 24),
    )


def test_collatz_coefficients_are_generated_by_same_gaussian_source() -> None:
    association, repair, dissociation = collatz_coefficients_from_gaussian_generator()
    assert association == 2
    assert repair == 1
    assert dissociation == 3


def test_l_constants_use_gaussian_source_plus_existing_root_extension_rule() -> None:
    assert l_constants_from_gaussian_and_root_extension() == (7, 2, 5)

    receipt = gaussian_l_constant_closure_crosscheck()
    assert receipt["L3"] == 7
    assert receipt["L4"] == 2
    assert receipt["L5"] == 5
    assert receipt["pythagorean_345"] is True
    assert receipt["g4_real_matches_minus_L3"] is True
    assert receipt["g4_imag_matches_24"] is True
    assert receipt["g4_norm_matches_L5_sq"] is True
    assert receipt["bombelli_radical_pair"] is True


def test_bombelli_cubic_is_recovered_without_float_arithmetic() -> None:
    receipt = bombelli_cubic_root_certificate()
    assert receipt["pass"] is True
    assert receipt["x"] == 4
    assert receipt["uv"] == 5
    assert receipt["u3_plus_v3"] == 4
    assert receipt["cubic_value"] == 0
    assert receipt["u3_real"] == 2
    assert receipt["u3_imag"] == 11
    assert receipt["v3_real"] == 2
    assert receipt["v3_imag"] == -11


def test_gaussian_characteristic_recurrence_is_exact() -> None:
    expected = (
        GaussianPair(1, 0),
        GaussianPair(2, 1),
        GaussianPair(3, 4),
        GaussianPair(2, 11),
        GaussianPair(-7, 24),
    )
    assert tuple(gaussian_recurrence_term(n) for n in range(5)) == expected
    for n in range(12):
        assert gaussian_recurrence_residual(n) == GaussianPair(0, 0)


def test_gaussian_power_fails_closed_on_invalid_exponents() -> None:
    g = minimal_relation_role_gaussian_generator()

    try:
        _ = g ** -1
    except ValueError:
        pass
    else:
        raise AssertionError("negative Gaussian exponent must fail closed")

    try:
        gaussian_recurrence_term(True)
    except TypeError:
        pass
    else:
        raise AssertionError("boolean recurrence index must fail closed")
