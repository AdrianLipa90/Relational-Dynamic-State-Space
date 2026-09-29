from math import pi

import pytest

from rdss import RelationalHolonomyPath, transport_holonomy


def test_representation_can_close_while_total_state_changes():
    path = RelationalHolonomyPath(
        representation_name="home-chart",
        projected_start=(0.0 + 0j,),
        projected_end=(0.0 + 0j,),
        edge_phases=(0.20, 0.35, 0.10),
    )

    result = transport_holonomy(path)

    assert result.representation_closed
    assert not result.same_total_state
    assert result.residual_phase == pytest.approx(0.65)
    assert result.end_internal != result.start_internal


def test_trivial_holonomy_can_close_total_state():
    path = RelationalHolonomyPath(
        representation_name="closed-chart",
        projected_start=(1.0 + 0j,),
        projected_end=(1.0 + 0j,),
        edge_phases=(pi, pi),
    )

    result = transport_holonomy(path)

    assert result.representation_closed
    assert result.same_total_state
    assert result.residual_phase == pytest.approx(0.0)
    assert result.winding == 1


def test_open_representation_does_not_claim_total_closure():
    path = RelationalHolonomyPath(
        representation_name="open-chart",
        projected_start=(0.0 + 0j,),
        projected_end=(1.0 + 0j,),
        edge_phases=(0.0,),
    )

    result = transport_holonomy(path)

    assert not result.representation_closed
    assert not result.same_total_state
