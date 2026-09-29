from math import pi

import pytest

from rdss import CP1State, MinimalDistinction, RelationalPoint
from rdss.realizations import (
    CP1RefinementRealization,
    reference_maximal_cp1_tree,
)


def test_maximal_cp1_tree_realizes_recursive_fibres():
    root = RelationalPoint()
    realization = reference_maximal_cp1_tree(2, root=root)

    assert realization.complete_through_depth(root, 2)
    assert len(realization.distinctions) == 7
    assert all(
        value == pytest.approx(pi / 2.0)
        for value in realization.fs_profile(root, 2).values()
    )


def test_parent_branch_state_indexes_child_carrier_without_identifying_fibres():
    root = RelationalPoint()
    realization = reference_maximal_cp1_tree(1, root=root)

    left_state = realization.branch_state(root, -1)
    left_carrier = realization.child_carrier(root, -1)

    assert isinstance(left_state, CP1State)
    assert left_carrier == RelationalPoint((-1,))
    assert realization.distinction_at(left_carrier).carrier == left_carrier


def test_nonmaximal_local_cp1_distinction_is_allowed():
    root = RelationalPoint()
    local = MinimalDistinction(
        root,
        CP1State(1.0, 0.0),
        CP1State(1.0, 1.0),
        label="nonmaximal",
    )
    realization = CP1RefinementRealization((local,))

    assert realization.complete_through_depth(root, 0)
    assert 0.0 < realization.fs_profile(root, 0)[()] < pi / 2.0


def test_incomplete_cp1_tree_fails_recursive_completion():
    root = RelationalPoint()
    realization = reference_maximal_cp1_tree(0, root=root)

    assert not realization.complete_through_depth(root, 1)
    with pytest.raises(ValueError):
        realization.fs_profile(root, 1)


def test_duplicate_fibre_on_same_carrier_is_rejected():
    root = RelationalPoint()
    p = CP1State(1.0, 0.0)
    q = p.orthogonal_partner()
    first = MinimalDistinction(root, p, q, "first")
    second = MinimalDistinction(root, p, q, "second")

    with pytest.raises(ValueError):
        CP1RefinementRealization((first, second))
