import pytest

from rdss.cosmic import (
    CosmicRelationalStep,
    InfoHolonomicCoordinate,
    MinkowskiMoirePoint,
    PlanetaryRelationalLoad,
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


def test_planetary_relational_load_7_8_is_an_explicit_input_not_universal_g():
    load = PlanetaryRelationalLoad(7.8)
    phase = load.phase_increment(duration_s=2.0, coupling_s_per_m=0.05)

    assert phase == pytest.approx(0.78)


def test_cosmic_phase_accumulates_all_relational_channels():
    load = PlanetaryRelationalLoad(7.8)
    planet = load.phase_increment(duration_s=1.0, coupling_s_per_m=0.1)
    steps = (
        CosmicRelationalStep(0.1, 0.2, planet),
        CosmicRelationalStep(0.3, -0.1, 0.0),
    )

    assert accumulated_holonomic_phase(steps) == pytest.approx(1.28)
