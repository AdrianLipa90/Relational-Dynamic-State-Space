import pytest

from rdss.cosmic import (
    CosmicRelationalStep,
    InfoHolonomicCoordinate,
    MinkowskiMoirePoint,
    accumulated_holonomic_phase,
    minkowski_interval_sq,
)


def test_flat_minkowski_base_does_not_erase_fibre_information():
    p = MinkowskiMoirePoint(0.0, 0.0, 0.0, 0.0, InfoHolonomicCoordinate(1.0, 0.0))
    q = MinkowskiMoirePoint(0.0, 0.0, 0.0, 0.0, InfoHolonomicCoordinate(2.0, 0.7))

    assert minkowski_interval_sq(p, q) == 0.0
    assert p.fibre.zeta != q.fibre.zeta


def test_semantics_can_change_holonomy_without_changing_base_step():
    a = CosmicRelationalStep(base_phase=0.2, semantic_phase=0.1)
    b = CosmicRelationalStep(base_phase=0.2, semantic_phase=0.8)

    assert a.base_phase == b.base_phase
    assert a.total_phase != b.total_phase


def test_context_is_generic_and_has_no_built_in_physical_value():
    no_context = CosmicRelationalStep(base_phase=0.2, semantic_phase=0.3)
    with_context = CosmicRelationalStep(base_phase=0.2, semantic_phase=0.3, context_phase=0.4)

    assert no_context.context_phase == 0.0
    assert with_context.total_phase == pytest.approx(0.9)


def test_cosmic_phase_accumulates_explicit_channels_only():
    steps = (
        CosmicRelationalStep(0.1, 0.2, 0.3),
        CosmicRelationalStep(0.3, -0.1, 0.0),
    )

    assert accumulated_holonomic_phase(steps) == pytest.approx(0.8)
