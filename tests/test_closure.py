from rdss.algebra import RelationalPoint, TypedRelation
import pytest

from rdss.closure import (
    BinaryDistinction,
    BranchRelationOccurrence,
    GenerativeRelationModel,
    binary_boundary_cylinder_count,
    binary_occurrence_count_through_depth,
    binary_words_at_depth,
    finite_word_rank,
    finite_word_unrank,
    minimal_singleton_ra0_rel_star_model,
    RelationalBinaryDistinction,
    RelationalGenerativeModel,
    requires_novelty,
    singleton_ra0_rel_star_model,
    singleton_ra0_star_model,
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



def test_singleton_carrier_supports_two_distinct_branch_occurrences():
    model = singleton_ra0_star_model()

    assert model.satisfies_ra0_star()
    assert model.is_admissible_rtofa_model()

    tree = model.unfold("a", 2)

    assert tree[(-1,)] == "a"
    assert tree[(1,)] == "a"
    assert (-1,) != (1,)
    assert tree[(-1, -1)] == "a"
    assert tree[(1, 1)] == "a"
    assert model.rr1_holds_through_depth("a", 5)


def test_singleton_occurrence_distinction_does_not_imply_novelty():
    model = singleton_ra0_star_model()

    assert not requires_novelty(model, "a", 1)



def test_relational_ra0_star_singleton_implies_ra0_and_rr1():
    model = singleton_ra0_rel_star_model()

    assert model.is_admissible_rtofa_model()
    assert model.satisfies_ra0_rel_star()
    assert model.satisfies_ra0()
    for depth in range(8):
        assert model.rr1_holds_through_depth("a", depth)


def test_relational_ra0_star_keeps_two_branch_relation_occurrences():
    model = singleton_ra0_rel_star_model()

    left, right = model.branch_relations_at("a")

    assert left == BranchRelationOccurrence(-1, "r-", "a", "a")
    assert right == BranchRelationOccurrence(1, "r+", "a", "a")
    assert left != right
    assert left.branch == -1
    assert right.branch == 1


def test_relational_ra0_star_requires_every_admitted_host_to_bind_relations():
    model = RelationalGenerativeModel(
        admitted=frozenset({"a", "b"}),
        distinctions=(
            RelationalBinaryDistinction(
                host="a",
                left="a",
                right="b",
                left_relation="r-",
                right_relation="r+",
            ),
        ),
    )

    assert not model.satisfies_ra0_rel_star()
    assert not model.satisfies_ra0()
    assert not model.rr1_holds_through_depth("a", 1)
    with pytest.raises(ValueError):
        model.unfold("a", 1)


def test_relational_ra0_star_endpoints_must_be_admitted():
    with pytest.raises(ValueError):
        RelationalGenerativeModel(
            admitted=frozenset({"a"}),
            distinctions=(
                RelationalBinaryDistinction(
                    host="a",
                    left="a",
                    right="b",
                    left_relation="r-",
                    right_relation="r+",
                ),
            ),
        )



def test_relational_distinction_occurrence_identity_does_not_require_distinct_relation_labels():
    distinction = RelationalBinaryDistinction(
        host="a",
        left="a",
        right="a",
        left_relation="r",
        right_relation="r",
    )

    left, right = distinction.branch_relation_occurrences

    assert left == BranchRelationOccurrence(-1, "r", "a", "a")
    assert right == BranchRelationOccurrence(1, "r", "a", "a")
    assert left != right


def test_relational_distinction_rejects_empty_relation_label():
    with pytest.raises(ValueError):
        RelationalBinaryDistinction(
            host="a",
            left="a",
            right="a",
            left_relation="",
            right_relation="r+",
        )



def test_singleton_relational_candidate_achieves_meta0_cardinality_lower_bound():
    model = singleton_ra0_rel_star_model()
    empty = GenerativeRelationModel(
        admitted=frozenset(),
        distinctions=(),
    )

    assert len(model.admitted) == 1
    assert model.is_admissible_rtofa_model()
    assert model.satisfies_ra0_rel_star()
    assert not empty.is_admissible_rtofa_model()



def test_relational_candidate_forgets_to_plain_ra0_star_model():
    relational = singleton_ra0_rel_star_model()
    plain = relational.as_ra0_star_model()

    assert relational.satisfies_ra0_rel_star()
    assert plain.satisfies_ra0_star()
    assert relational.admitted == plain.admitted
    assert relational.unfold("a", 4) == plain.unfold("a", 4)



def test_branch_relation_occurrence_rejects_invalid_branch():
    with pytest.raises(ValueError):
        BranchRelationOccurrence(0, "r", "a", "a")


def test_branch_relation_occurrence_rejects_empty_endpoint_or_label():
    with pytest.raises(ValueError):
        BranchRelationOccurrence(-1, "", "a", "a")

    with pytest.raises(ValueError):
        BranchRelationOccurrence(1, "r", "", "a")



def test_branch_relation_occurrence_materializes_core_typed_relation():
    occurrence = BranchRelationOccurrence(-1, "r", "a", "b")
    carriers = {
        "a": RelationalPoint(),
        "b": RelationalPoint((1,)),
    }

    relation = occurrence.as_typed_relation(carriers)

    assert relation == TypedRelation(
        carriers["a"],
        carriers["b"],
        "r",
    )


def test_distinct_occurrences_may_share_same_relation_value():
    carriers = {"a": RelationalPoint()}
    left = BranchRelationOccurrence(-1, "r", "a", "a")
    right = BranchRelationOccurrence(1, "r", "a", "a")

    assert left != right
    assert left.as_typed_relation(carriers) == right.as_typed_relation(carriers)


def test_branch_relation_materialization_fails_on_missing_carrier_mapping():
    occurrence = BranchRelationOccurrence(-1, "r", "a", "b")

    with pytest.raises(KeyError):
        occurrence.as_typed_relation({"a": RelationalPoint()})



def test_binary_occurrence_count_matches_complete_unfolding():
    model = singleton_ra0_star_model()

    for depth in range(10):
        tree = model.unfold("a", depth)
        assert len(tree) == binary_occurrence_count_through_depth(depth)
        assert binary_occurrence_count_through_depth(depth) == (2 ** (depth + 1)) - 1


def test_finite_word_rank_unrank_is_bijection_on_initial_segment():
    seen = set()

    for rank in range(512):
        address = finite_word_unrank(rank)
        assert finite_word_rank(address) == rank
        assert address not in seen
        seen.add(address)

    assert len(seen) == 512


def test_finite_word_rank_orders_words_by_level_then_binary_index():
    assert finite_word_rank(()) == 0
    assert finite_word_rank((-1,)) == 1
    assert finite_word_rank((1,)) == 2
    assert finite_word_rank((-1, -1)) == 3
    assert finite_word_rank((-1, 1)) == 4
    assert finite_word_rank((1, -1)) == 5
    assert finite_word_rank((1, 1)) == 6


def test_finite_word_rank_and_count_fail_closed():
    with pytest.raises(ValueError):
        binary_occurrence_count_through_depth(-1)

    with pytest.raises(ValueError):
        finite_word_rank((0,))

    with pytest.raises(ValueError):
        finite_word_unrank(-1)



def test_minimal_singleton_relation_value_cardinality_is_one():
    model = minimal_singleton_ra0_rel_star_model()

    assert model.is_admissible_rtofa_model()
    assert model.satisfies_ra0_rel_star()
    assert len(model.admitted) == 1
    assert model.relation_values == frozenset({("a", "a", "r")})
    assert len(model.relation_values) == 1


def test_minimal_singleton_keeps_two_occurrences_over_one_relation_value():
    model = minimal_singleton_ra0_rel_star_model()
    left, right = model.branch_relations_at("a")

    assert left != right
    assert left.branch == -1
    assert right.branch == 1
    assert (
        left.source,
        left.target,
        left.relation_label,
    ) == (
        right.source,
        right.target,
        right.relation_label,
    ) == ("a", "a", "r")
    assert len(model.relation_values) == 1


def test_nonempty_ra0_rel_star_has_at_least_one_relation_value():
    model = minimal_singleton_ra0_rel_star_model()

    assert model.admitted
    assert model.satisfies_ra0_rel_star()
    assert len(model.relation_values) >= 1



def test_rr1_unfolding_realizes_every_finite_binary_word_through_depth():
    model = singleton_ra0_star_model()

    for depth in range(8):
        tree = model.unfold("a", depth)
        count = binary_occurrence_count_through_depth(depth)
        expected_addresses = {
            finite_word_unrank(rank)
            for rank in range(count)
        }
        assert set(tree) == expected_addresses



def test_minimal_singleton_relation_occurrence_cardinality_is_two():
    model = minimal_singleton_ra0_rel_star_model()

    assert model.is_admissible_rtofa_model()
    assert model.satisfies_ra0_rel_star()
    assert len(model.relation_occurrences) == 2
    assert {occ.branch for occ in model.relation_occurrences} == {-1, 1}


def test_nonempty_ra0_rel_star_has_at_least_two_relation_occurrences():
    model = minimal_singleton_ra0_rel_star_model()

    assert model.admitted
    assert model.satisfies_ra0_rel_star()
    assert len(model.relation_occurrences) >= 2



def test_binary_boundary_prefix_basis_has_exact_cylinder_count():
    for depth in range(9):
        words = binary_words_at_depth(depth)

        assert len(words) == 2 ** depth
        assert len(words) == binary_boundary_cylinder_count(depth)
        assert all(len(word) == depth for word in words)
        assert len(set(words)) == len(words)


def test_binary_boundary_prefix_basis_matches_finite_word_ranking_block():
    for depth in range(7):
        words = binary_words_at_depth(depth)
        expected_start = (1 << depth) - 1
        expected = tuple(
            finite_word_unrank(expected_start + i)
            for i in range(1 << depth)
        )
        assert words == expected


def test_binary_boundary_prefix_helpers_fail_closed():
    with pytest.raises(ValueError):
        binary_words_at_depth(-1)

    with pytest.raises(ValueError):
        binary_boundary_cylinder_count(-1)
