import cmath
from math import pi, sqrt

from rdss.corpus import rdss_reference_corpus
from rdss.cp1_projective import (
    CP1ProjectivePoint,
    compare_cp1_projective,
    cp1_projective_determinant_residual,
    cp1_projective_point,
    cp1_projectively_equivalent,
    quotient_cp1_states,
)
from rdss.factorization import (
    FactorizationRelation,
    compare_factorizations,
)
from rdss.realizations import CP1State


def test_global_phase_changes_raw_state_but_not_projective_point():
    left = CP1State(1 + 0j, 0 + 0j)
    right = CP1State(0 + 1j, 0 + 0j)

    raw = compare_factorizations(left, right)
    projective = compare_cp1_projective(
        left,
        right,
    )

    assert raw.relation is FactorizationRelation.DIFFERENT_STATE
    assert projective.equivalent
    assert projective.left == CP1ProjectivePoint(
        "alpha",
        0j,
    )
    assert projective.right == projective.left
    assert projective.determinant_residual == 0.0
    assert projective.coordinate_residual == 0.0
    assert projective.fubini_study_distance == 0.0


def test_generic_global_phase_is_projectively_equivalent():
    scale = 1.0 / sqrt(2.0)
    phase = cmath.exp(1j * 0.731)
    left = CP1State(
        scale,
        1j * scale,
    )
    right = CP1State(
        phase * scale,
        phase * 1j * scale,
    )

    comparison = compare_cp1_projective(
        left,
        right,
    )

    assert comparison.equivalent
    assert comparison.determinant_residual <= 1e-12
    assert comparison.coordinate_residual <= 1e-12


def test_orthogonal_cp1_states_remain_projectively_distinct():
    north = CP1State(1 + 0j, 0 + 0j)
    south = CP1State(0 + 0j, 1 + 0j)

    comparison = compare_cp1_projective(
        north,
        south,
    )

    assert not comparison.equivalent
    assert comparison.determinant_residual == 1.0
    assert abs(
        comparison.fubini_study_distance
        - (pi / 2.0)
    ) <= 1e-12


def test_projective_chart_is_global_phase_invariant():
    phase = cmath.exp(1j * 1.234)
    left = CP1State(
        0.2 + 0j,
        sqrt(0.96) + 0j,
    )
    right = CP1State(
        phase * 0.2,
        phase * sqrt(0.96),
    )

    left_point = cp1_projective_point(left)
    right_point = cp1_projective_point(right)

    assert left_point.chart == "beta"
    assert right_point.chart == "beta"
    assert left_point.equivalent_to(right_point)


def test_projective_determinant_is_zero_for_common_phase():
    phase = cmath.exp(-1j * 0.4)
    left = CP1State(
        0.6 + 0j,
        0.8 + 0j,
    )
    right = CP1State(
        phase * 0.6,
        phase * 0.8,
    )

    assert (
        cp1_projective_determinant_residual(
            left,
            right,
        )
        <= 1e-12
    )
    assert cp1_projectively_equivalent(
        left,
        right,
    )


def test_reference_corpus_cp1_quotient_collapses_one_global_phase_copy():
    states = tuple(
        item.value
        for item in rdss_reference_corpus()
        if isinstance(item.value, CP1State)
    )

    quotient = quotient_cp1_states(states)

    assert quotient.summary.records == 3
    assert quotient.summary.strict_representatives == 3
    assert quotient.summary.projective_classes == 2
    assert quotient.summary.collapsed_representatives == 1
    assert sorted(
        cls.member_count
        for cls in quotient.classes
    ) == [1, 2]


def test_empty_cp1_quotient_is_well_defined():
    quotient = quotient_cp1_states(())

    assert quotient.points == ()
    assert quotient.classes == ()
    assert quotient.summary.records == 0
    assert quotient.summary.projective_classes == 0
