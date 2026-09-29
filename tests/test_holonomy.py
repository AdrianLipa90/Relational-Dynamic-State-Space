from math import pi

import pytest

from rdss import RelationalLoop, transport_experience


def test_closed_base_loop_can_return_to_same_place_with_changed_fibre():
    loop = RelationalLoop(
        base_path=("home", "school", "park", "home"),
        edge_phases=(0.20, 0.35, 0.10),
    )

    result = transport_experience(loop)

    assert result.same_base_point
    assert not result.same_total_state
    assert result.residual_phase == pytest.approx(0.65)
    assert result.end_fibre != result.start_fibre


def test_trivial_holonomy_returns_same_total_state():
    loop = RelationalLoop(
        base_path=("home", "destination", "home"),
        edge_phases=(pi, pi),
    )

    result = transport_experience(loop)

    assert result.same_base_point
    assert result.same_total_state
    assert result.residual_phase == pytest.approx(0.0)
    assert result.winding == 1


def test_open_path_is_rejected():
    with pytest.raises(ValueError):
        RelationalLoop(
            base_path=("home", "destination"),
            edge_phases=(0.4,),
        )
