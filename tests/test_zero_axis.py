from cmath import exp
from math import pi

import pytest

from rdss.zero_axis import ZeroAxisPoint, finite_zero_axis_lift


def test_zero_axis_projective_coordinate_lies_on_unit_circle():
    point = ZeroAxisPoint(t=14.134725)

    assert point.s.real == pytest.approx(0.5)
    assert abs(point.omega) == pytest.approx(1.0)
    assert point.unit_circle_residual == pytest.approx(0.0, abs=1e-14)


def test_finite_u1_phase_lifts_to_zero_axis():
    u = exp(0.4j)
    point = finite_zero_axis_lift(u)

    assert point.s.real == pytest.approx(0.5)
    assert point.omega == pytest.approx(u)


def test_zero_axis_lift_rejects_nonunit_phase():
    with pytest.raises(ValueError):
        finite_zero_axis_lift(2.0 + 0.0j)


def test_minus_one_phase_is_compactified_infinity():
    with pytest.raises(ValueError):
        finite_zero_axis_lift(exp(1j * pi))
