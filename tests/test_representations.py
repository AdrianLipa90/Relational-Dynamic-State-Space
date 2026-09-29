import pytest

from rdss import (
    DerivedRepresentation,
    HilbertMoireKet,
    InfoHolonomicCoordinate,
    RepresentationMetric,
    representation_displacement,
)


def test_hilbert_state_is_primary_and_representation_is_derived():
    psi = HilbertMoireKet((1.0 + 0j, 2.0 + 0j), InfoHolonomicCoordinate(0.4, 0.7))
    rep = DerivedRepresentation("example-chart", ((1.0, 0.0),))

    assert rep.project(psi) == (1.0 + 0j,)
    assert psi.info_holonomic.zeta == 0.4 + 0.7j


def test_same_hilbert_state_can_support_different_derived_representations():
    psi = HilbertMoireKet((1.0 + 0j, 2.0 + 0j))
    first = DerivedRepresentation("first", ((1.0, 0.0),))
    second = DerivedRepresentation("second", ((0.0, 1.0),))

    assert first.project(psi) == (1.0 + 0j,)
    assert second.project(psi) == (2.0 + 0j,)


def test_metric_belongs_to_representation_not_to_hilbert_primacy_rule():
    metric = RepresentationMetric(((-1.0, 0.0), (0.0, 1.0)))

    assert metric.quadratic_form((2.0, 3.0)).real == pytest.approx(5.0)


def test_representation_displacement_is_computed_after_projection():
    rep = DerivedRepresentation("chart", ((1.0, 0.0),))
    a = HilbertMoireKet((1.0, 9.0))
    b = HilbertMoireKet((4.0, -3.0))

    assert representation_displacement(rep, a, b) == (3.0 + 0j,)
