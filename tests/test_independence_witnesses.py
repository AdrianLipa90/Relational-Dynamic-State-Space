from rdss.witnesses import (
    FiniteRelationModel,
    witness_meta0_not_ra0,
    witness_ra0_not_rr1,
    witness_ra0_star_not_ra0,
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



def test_ra0_plus_rr1_do_not_force_existence_on_raw_presentations():
    model = witness_ra0_rr1_without_ex0()

    assert model.satisfies_ra0()
    assert model.satisfies_rr1()
    assert not model.satisfies_ex0()
    assert not model.is_admissible_rtofa_model()


def test_meta0_nonvacuity_does_not_force_ra0_when_adm_is_primitive():
    model = witness_meta0_not_ra0()

    assert model.is_admissible_rtofa_model()
    assert model.satisfies_ex0()
    assert not model.satisfies_ra0()



def test_ra0_accepts_target_only_relational_incidence():
    model = FiniteRelationModel(
        points=frozenset({"a", "b"}),
        admitted=frozenset({"b"}),
        relations=frozenset({("a", "b")}),
    )

    assert model.satisfies_ra0()



def test_singleton_self_relation_and_same_label_refinement_satisfy_ra0_rr1():
    model = FiniteRelationModel(
        points=frozenset({"a"}),
        admitted=frozenset({"a"}),
        relations=frozenset({("a", "a")}),
        refinements=(
            ("a", "a", "a"),
        ),
    )

    assert model.is_admissible_rtofa_model()
    assert model.satisfies_ra0()
    assert model.satisfies_rr1()



def test_ra0_star_without_relation_binding_does_not_force_ra0():
    model = witness_ra0_star_not_ra0()

    assert model.is_admissible_rtofa_model()
    assert model.satisfies_ra0_star()
    assert not model.satisfies_ra0()
