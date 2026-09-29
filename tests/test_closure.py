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



def test_ra0_star_allows_multiple_distinctions_per_host():
    model = GenerativeRelationModel(
        admitted=frozenset({"a", "b", "c"}),
        distinctions=(
            BinaryDistinction("a", "b", "c"),
            BinaryDistinction("a", "a", "b"),
            BinaryDistinction("b", "a", "c"),
            BinaryDistinction("c", "a", "b"),
        ),
    )

    assert model.satisfies_ra0_star()
    assert len(model.distinctions_by_host["a"]) == 2

    selected = model.selected_distinction_by_host["a"]
    assert (selected.left, selected.right) == ("a", "b")

    tree = model.unfold("a", 1)
    assert tree[(-1,)] == "a"
    assert tree[(1,)] == "b"


def test_ra0_star_multiple_distinctions_do_not_break_recursive_closure():
    model = GenerativeRelationModel(
        admitted=frozenset({"a", "b"}),
        distinctions=(
            BinaryDistinction("a", "a", "b"),
            BinaryDistinction("a", "b", "a"),
            BinaryDistinction("b", "a", "b"),
        ),
    )

    assert model.satisfies_ra0_star()
    for depth in range(6):
        assert model.rr1_holds_through_depth("a", depth)



def test_empty_raw_presentation_is_not_an_admissible_rtofa_model():
    model = GenerativeRelationModel(
        admitted=frozenset(),
        distinctions=(),
    )

    # Formula-level RA0* is vacuously true on the raw empty presentation.
    assert model.satisfies_ra0_star()

    # META0 excludes that presentation from the intended model class.
    assert not model.is_admissible_rtofa_model()

    with pytest.raises(ValueError):
        model.unfold("a", 1)


def test_nonempty_presentation_satisfies_meta0_model_nonvacuity():
    model = two_cycle_ra0_star_model()

    assert model.is_admissible_rtofa_model()
