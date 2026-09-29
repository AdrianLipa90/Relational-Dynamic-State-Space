import pytest

from rdss.zero_axis import ZeroAxisPoint


def test_zero_axis_projective_coordinate_lies_on_unit_circle():
    point = ZeroAxisPoint(t=14.134725)

    assert point.s.real == pytest.approx(0.5)
    assert abs(point.omega) == pytest.approx(1.0)
    assert point.unit_circle_residual == pytest.approx(0.0, abs=1e-14)
