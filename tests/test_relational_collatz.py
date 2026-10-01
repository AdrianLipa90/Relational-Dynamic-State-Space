import pytest

from rdss.relational_collatz import (
    active_seed_from_relation_algebra,
    association_quotient_cardinality,
    dissociation_fibre_cardinality,
    durable_role_count,
    nonidentity_operator_dimension,
    operator_algebra_real_dimension,
    relational_collatz_depth_to_one,
    relational_l_constant_certificate,
    odd_branch_reopens_association,
    relational_collatz_equivalence,
    relational_collatz_step,
    singleton_repair_cardinality,
    standard_collatz_step,
    universal_constant_repair,
)


def test_association_is_exact_free_dyad_quotient_cardinality() -> None:
    assert association_quotient_cardinality(2) == 1
    assert association_quotient_cardinality(10) == 5
    assert association_quotient_cardinality(24) == 12

    with pytest.raises(ValueError):
        association_quotient_cardinality(3)


def test_dissociation_is_three_fibre_extension() -> None:
    assert dissociation_fibre_cardinality(1) == 3
    assert dissociation_fibre_cardinality(5) == 15
    assert dissociation_fibre_cardinality(7) == 21


def test_repair_is_singleton_coproduct() -> None:
    assert singleton_repair_cardinality(3) == 4
    assert singleton_repair_cardinality(9) == 10
    assert singleton_repair_cardinality(15) == 16


def test_relational_cardinality_semantics_equals_collatz_formula() -> None:
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
    }
    for n, value in expected.items():
        assert relational_collatz_step(n) == value
        assert relational_collatz_step(n) == standard_collatz_step(n)

    assert relational_collatz_equivalence(1000)


def test_odd_dissociation_repair_always_reopens_association() -> None:
    for n in range(1, 200, 2):
        assert odd_branch_reopens_association(n)


def test_relational_collatz_fails_closed() -> None:
    for value in (0, -1):
        with pytest.raises(ValueError):
            relational_collatz_step(value)

    with pytest.raises(TypeError):
        relational_collatz_step(True)

    with pytest.raises(ValueError):
        dissociation_fibre_cardinality(3, 1)

def test_relation_algebra_derives_operator_count_seed_and_universal_repair() -> None:
    assert durable_role_count() == 2
    assert operator_algebra_real_dimension() == 4
    assert nonidentity_operator_dimension() == 3
    assert active_seed_from_relation_algebra() == 3
    assert universal_constant_repair() == 1

    for q in range(3, 12):
        with pytest.raises(ValueError):
            universal_constant_repair(q)


def test_relation_algebra_seed_closes_l_constants_exactly() -> None:
    receipt = relational_l_constant_certificate()

    assert receipt["role_count"] == 2
    assert receipt["operator_dimension"] == 4
    assert receipt["nonidentity_dimension"] == 3
    assert receipt["universal_repair"] == 1
    assert receipt["active_seed"] == 3
    assert receipt["seed_step_1"] == 10
    assert receipt["seed_step_2"] == 5
    assert receipt["depth_to_one"] == 7
    assert receipt["L3"] == 7
    assert receipt["L4"] == 2
    assert receipt["L5"] == 5
    assert receipt["seed_matches_multiplier"] is True
    assert receipt["first_full_cycle_reaches_L5"] is True
    assert receipt["depth_matches_L3"] is True
    assert receipt["root_extension_matches"] is True

    assert relational_collatz_depth_to_one(3) == 7

