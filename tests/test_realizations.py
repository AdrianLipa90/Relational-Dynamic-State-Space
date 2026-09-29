from cmath import exp
from math import pi

import pytest

from rdss import OccurrenceRelationPath, OccurrenceTransportPath, RelationOccurrence, RelationalPoint, RelationTransport, SemanticScale, TensorScalarElement, TransportPath, TypedRelation, minimal_singleton_ra0_rel_star_model
from rdss.realizations import (
    CP1RefinementRealization,
    CP1RelationalUnfolding,
    CP1State,
    HolonomyPhaseRepresentation,
    OccurrenceHolonomyPhaseRepresentation,
    MinimalDistinction,
    MoireRotation,
    reference_cp1_unfolding,
    reference_maximal_cp1_tree,
    lift_value_phase_to_occurrence,
)


def test_cp1_fubini_study_maximal_distinction_is_pi_over_two():
    p = CP1State(1.0, 0.0)
    q = p.orthogonal_partner()
    distinction = MinimalDistinction(RelationalPoint(), p, q)

    assert distinction.separation == pytest.approx(pi / 2.0)
    assert distinction.is_maximal()


def test_cp1_nonmaximal_relation_has_smaller_fs_separation():
    p = CP1State(1.0, 0.0)
    q = CP1State(1.0, 1.0)

    assert 0.0 < p.fubini_study_distance(q) < pi / 2.0


def test_moire_scalar_angle_is_relative_not_absolute():
    a = MoireRotation(theta_i=0.75, theta_j=0.25)
    b = MoireRotation(theta_i=1.75, theta_j=1.25)

    assert a.delta == pytest.approx(0.5)
    assert b.delta == pytest.approx(0.5)


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


def occurrence_closed_phase_path(total_phase: float, branch: int = -1):
    a = RelationalPoint()
    scale = SemanticScale("object")
    x = TensorScalarElement((1.0,), (0, 0), a, scale)
    half = exp(0.5j * total_phase)

    down = TypedRelation(a, a, "down")
    up = TypedRelation(a, a, "up")
    occurrence_path = OccurrenceRelationPath(
        (
            RelationOccurrence(down, (), (branch,)),
            RelationOccurrence(up, (branch,), ()),
        )
    )

    def move(z):
        return TensorScalarElement(
            tuple(half * c for c in z.components),
            z.rank,
            a,
            z.scale,
        )

    path = OccurrenceTransportPath(
        occurrence_path,
        (
            RelationTransport(down, move),
            RelationTransport(up, move),
        ),
    )
    return path, x


def scalar_ratio_phase(path, element):
    final = path.apply(element)
    return final.components[0] / element.components[0]


def test_explicit_u1_holonomy_representation_returns_unit_phase():
    path, x = closed_phase_path(0.4)
    rep = HolonomyPhaseRepresentation("scalar-ratio", scalar_ratio_phase)

    u = rep.phase(path, x)

    assert abs(u) == pytest.approx(1.0)


def test_occurrence_u1_holonomy_representation_returns_unit_phase():
    path, x = occurrence_closed_phase_path(0.4)
    rep = OccurrenceHolonomyPhaseRepresentation(
        "occurrence-scalar-ratio",
        scalar_ratio_phase,
    )

    u = rep.phase(path, x)

    assert abs(u) == pytest.approx(1.0)


def test_occurrence_phase_representation_rejects_carrier_closed_occurrence_open_path():
    a = RelationalPoint()
    x = TensorScalarElement((1.0,), (0, 0), a, SemanticScale("object"))
    relation = TypedRelation(a, a, "r")
    occurrence_path = OccurrenceRelationPath(
        (
            RelationOccurrence(relation, (), (-1,)),
        )
    )
    path = OccurrenceTransportPath(
        occurrence_path,
        (
            RelationTransport(relation, lambda z: z),
        ),
    )
    rep = OccurrenceHolonomyPhaseRepresentation(
        "occurrence-open",
        scalar_ratio_phase,
    )

    assert occurrence_path.carrier_closed
    assert not occurrence_path.occurrence_closed
    with pytest.raises(ValueError):
        rep.phase(path, x)


def test_occurrence_phase_representation_rejects_nonunit_phase():
    path, x = occurrence_closed_phase_path(0.4)
    rep = OccurrenceHolonomyPhaseRepresentation(
        "occurrence-nonunit",
        lambda _path, _element: 2.0 + 0.0j,
    )

    with pytest.raises(ValueError):
        rep.phase(path, x)


def test_value_phase_lift_is_branch_blind_occurrence_representation():
    value_rep = HolonomyPhaseRepresentation(
        "value-scalar-ratio",
        scalar_ratio_phase,
    )
    lifted = lift_value_phase_to_occurrence(value_rep)

    left_path, x = occurrence_closed_phase_path(0.4, branch=-1)
    right_path, _ = occurrence_closed_phase_path(0.4, branch=1)

    left_phase = lifted.phase(left_path, x)
    right_phase = lifted.phase(right_path, x)

    assert left_path.occurrence_path != right_path.occurrence_path
    assert (
        left_path.value_transport_path.relation_path
        == right_path.value_transport_path.relation_path
    )
    assert left_phase == pytest.approx(right_phase)
    assert left_phase == pytest.approx(
        value_rep.phase(left_path.value_transport_path, x)
    )


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


def test_minus_one_is_a_valid_u1_holonomy_phase():
    path, x = closed_phase_path(pi)
    rep = HolonomyPhaseRepresentation("minus-one", scalar_ratio_phase)

    assert rep.phase(path, x) == pytest.approx(-1.0 + 0.0j)



def test_phase_representation_rejects_element_on_wrong_source():
    path, _ = closed_phase_path(0.4)
    wrong = TensorScalarElement(
        (1.0,),
        (0, 0),
        RelationalPoint((1,)),
        SemanticScale("object"),
    )
    rep = HolonomyPhaseRepresentation("scalar-ratio", scalar_ratio_phase)

    with pytest.raises(ValueError):
        rep.phase(path, wrong)



def test_cp1_identical_projective_states_do_not_realize_distinction():
    p = CP1State(1.0, 0.0)

    with pytest.raises(ValueError):
        MinimalDistinction(RelationalPoint(), p, p)


def test_single_carrier_can_support_two_distinct_cp1_branch_states():
    carrier = RelationalPoint()
    left = CP1State(1.0, 0.0)
    right = CP1State(0.0, 1.0)

    distinction = MinimalDistinction(carrier, left, right)

    assert distinction.carrier == carrier
    assert distinction.left != distinction.right
    assert distinction.separation == pytest.approx(pi / 2.0)



def test_singleton_relational_unfolding_matches_cp1_address_tree():
    model = minimal_singleton_ra0_rel_star_model()
    realized = reference_cp1_unfolding(model, "a", 3)

    expected = model.unfold("a", 3)

    assert realized.addresses == frozenset(expected)
    assert len(realized.addresses) == 15
    assert set(realized.label_by_address.values()) == {"a"}
    assert realized.fibres.complete_through_depth(RelationalPoint(), 3)


def test_singleton_carrier_label_reuse_is_independent_of_cp1_branch_separation():
    model = minimal_singleton_ra0_rel_star_model()
    realized = reference_cp1_unfolding(model, "a", 1)
    root = RelationalPoint()

    assert realized.label_by_address[(-1,)] == "a"
    assert realized.label_by_address[(1,)] == "a"
    assert realized.fibres.branch_state(root, -1) != realized.fibres.branch_state(root, 1)
    assert realized.fibres.distinction_at(root).separation == pytest.approx(pi / 2.0)


def test_cp1_relational_unfolding_rejects_address_mismatch():
    fibres = reference_maximal_cp1_tree(1)
    with pytest.raises(ValueError):
        CP1RelationalUnfolding(
            ((RelationalPoint(), "a"),),
            fibres,
        )
