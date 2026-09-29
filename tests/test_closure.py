import pytest

from rdss.closure import (
    BinaryDistinction,
    GenerativeRelationModel,
    requires_novelty,
    two_cycle_ra0_star_model,
)


def test_ra0_star_forces_recursive_binary_unfolding_to_any_tested_depth():
    model = two_cycle_ra0_star_model()

    assert model.satisfies_ra0_star()
    for depth in range(8):
        assert model.rr1_holds_through_depth("a", depth)


def test_unfolding_has_exact_binary_address_count():
    model = two_cycle_ra0_star_model()
    tree = model.unfold("a", 5)

    expected = sum(2 ** level for level in range(6))
    assert len(tree) == expected


def test_path_occurrences_remain_distinct_even_when_carrier_labels_repeat():
    model = two_cycle_ra0_star_model()
    tree = model.unfold("a", 2)

    assert tree[(-1,)] == "a"
    assert tree[(1, -1)] == "a"
    assert (-1,) != (1, -1)


def test_ra0_star_does_not_imply_ontic_novelty():
    model = two_cycle_ra0_star_model()

    assert not requires_novelty(model, "a", 2)


def test_missing_distinction_breaks_ra0_star_and_recursive_closure():
    model = GenerativeRelationModel(
        admitted=frozenset({"a", "b"}),
        distinctions=(BinaryDistinction("a", "a", "b"),),
    )

    assert not model.satisfies_ra0_star()
    assert not model.rr1_holds_through_depth("a", 1)
    with pytest.raises(ValueError):
        model.unfold("a", 1)


def test_endpoints_must_be_admitted():
    with pytest.raises(ValueError):
        GenerativeRelationModel(
            admitted=frozenset({"a"}),
            distinctions=(BinaryDistinction("a", "a", "b"),),
        )
