from rdss.witnesses import (
    witness_ra0_not_rr1,
    witness_ra0_rr1_without_cp1,
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
