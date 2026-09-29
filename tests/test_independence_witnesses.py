from rdss.witnesses import (
    FiniteRelationModel,
    witness_ra0_not_rr1,
    witness_ra0_rr1_without_cp1,
    witness_ra0_rr1_without_ex0,
    witness_rr1_not_ra0,
)


def test_ra0_does_not_force_recursive_refinement():
    model = witness_ra0_not_rr1()

    assert model.satisfies_ra0()
    assert not model.satisfies_rr1()


def test_recursive_refinement_does_not_force_ra0():
    model = witness_rr1_not_ra0()

    assert model.satisfies_rr1()
    assert not model.satisfies_ra0()


def test_ra0_plus_rr1_do_not_force_cp1_realization():
    model = witness_ra0_rr1_without_cp1()

    assert model.satisfies_ra0()
    assert model.satisfies_rr1()
    assert not hasattr(model, "cp1_state")



def test_one_level_refinement_is_not_recursive_rr1():
    model = FiniteRelationModel(
        points=frozenset({"a", "b", "a-", "a+", "b-", "b+"}),
        admitted=frozenset({"a", "b"}),
        relations=frozenset({("a", "b"), ("b", "a")}),
        refinements=(
            ("a", "a-", "a+"),
            ("b", "b-", "b+"),
        ),
    )

    assert not model.satisfies_rr1()


def test_rr1_not_ra0_witness_is_recursively_closed():
    model = witness_rr1_not_ra0()

    assert model.satisfies_rr1()
    assert not model.satisfies_ra0()
    refinement_map = {
        parent: (left, right)
        for parent, left, right in model.refinements
    }
    assert refinement_map["a"] == ("a", "b")
    assert refinement_map["b"] == ("a", "b")



def test_ra0_plus_rr1_do_not_force_existence():
    model = witness_ra0_rr1_without_ex0()

    assert model.satisfies_ra0()
    assert model.satisfies_rr1()
    assert not model.satisfies_ex0()
