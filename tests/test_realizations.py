from cmath import exp
from math import pi

import pytest

from rdss import CP1State, MinimalDistinction, RelationalPoint, RelationTransport, SemanticScale, TensorScalarElement, TransportPath, TypedRelation
from rdss.realizations import (
    CP1RefinementRealization,
    HolonomyPhaseRepresentation,
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



def closed_phase_path(total_phase: float):
    a = RelationalPoint((-1,))
    b = RelationalPoint((1,))
    scale = SemanticScale("object")
    x = TensorScalarElement((1.0,), (0, 0), a, scale)
    half = exp(0.5j * total_phase)

    rab = TypedRelation(a, b, "ab")
    rba = TypedRelation(b, a, "ba")

    def move(target):
        return lambda z: TensorScalarElement(
            tuple(half * c for c in z.components),
            z.rank,
            target,
            z.scale,
        )

    path = TransportPath(
        (
            RelationTransport(rab, move(b)),
            RelationTransport(rba, move(a)),
        )
    )
    return path, x


def scalar_ratio_phase(path, element):
    final = path.apply(element)
    return final.components[0] / element.components[0]


def test_explicit_u1_holonomy_representation_lifts_to_zero_axis():
    path, x = closed_phase_path(0.4)
    rep = HolonomyPhaseRepresentation("scalar-ratio", scalar_ratio_phase)

    u = rep.phase(path, x)
    point = rep.finite_zero_axis_point(path, x)

    assert abs(u) == pytest.approx(1.0)
    assert point.s.real == pytest.approx(0.5)
    assert point.omega == pytest.approx(u)


def test_nonunit_holonomy_representation_is_rejected():
    a = RelationalPoint((-1,))
    b = RelationalPoint((1,))
    scale = SemanticScale("object")
    x = TensorScalarElement((1.0,), (0, 0), a, scale)
    rab = TypedRelation(a, b, "ab")
    rba = TypedRelation(b, a, "ba")

    path = TransportPath(
        (
            RelationTransport(
                rab,
                lambda z: TensorScalarElement(
                    tuple(2.0 * c for c in z.components),
                    z.rank,
                    b,
                    z.scale,
                ),
            ),
            RelationTransport(
                rba,
                lambda z: TensorScalarElement(
                    z.components,
                    z.rank,
                    a,
                    z.scale,
                ),
            ),
        )
    )

    rep = HolonomyPhaseRepresentation("nonunit", scalar_ratio_phase)
    with pytest.raises(ValueError):
        rep.phase(path, x)


def test_phase_representation_requires_closed_path():
    a = RelationalPoint((-1,))
    b = RelationalPoint((1,))
    scale = SemanticScale("object")
    x = TensorScalarElement((1.0,), (0, 0), a, scale)
    rab = TypedRelation(a, b, "ab")
    path = TransportPath(
        (
            RelationTransport(
                rab,
                lambda z: TensorScalarElement(z.components, z.rank, b, z.scale),
            ),
        )
    )

    rep = HolonomyPhaseRepresentation("open", scalar_ratio_phase)
    with pytest.raises(ValueError):
        rep.phase(path, x)


def test_minus_one_phase_is_compactified_zero_axis_infinity():
    path, x = closed_phase_path(pi)
    rep = HolonomyPhaseRepresentation("minus-one", scalar_ratio_phase)

    assert rep.phase(path, x) == pytest.approx(-1.0 + 0.0j)
    with pytest.raises(ValueError):
        rep.finite_zero_axis_point(path, x)
