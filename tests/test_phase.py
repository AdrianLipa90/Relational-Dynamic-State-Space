from math import pi

import pytest

from rdss.phase import closed_path_winding, winding_and_residual, wrap_phase


def test_wrap_phase_maps_to_principal_interval():
    assert wrap_phase(0.0) == pytest.approx(0.0)
    assert wrap_phase(3.0 * pi) == pytest.approx(pi)
    assert wrap_phase(-3.0 * pi) == pytest.approx(pi)


def test_phase_decomposition_keeps_nonzero_residual_for_open_path():
    turn_count, residual = winding_and_residual((pi, pi, 0.2))

    assert turn_count == 1
    assert residual == pytest.approx(0.2)


def test_topological_winding_requires_phase_closure():
    assert closed_path_winding((pi, pi)) == 1

    with pytest.raises(ValueError):
        closed_path_winding((pi, pi, 0.2))
