from math import log, pi

import pytest

from rdss import (
    CANONICAL_MIXING_CHANNELS,
    CANONICAL_MIXING_TURN_MEASURE,
    CenterHalfTurnBridge,
    HilbertMoireFibreState,
    KAPPA_PHI,
    KAPPA_Q,
    OccurrenceAddress,
    canonical_mixing_channels,
    centered_relational_coordinate,
    external_relational_coordinate,
    information_increment_radians,
    information_increment_turns,
    moire_pair_factored,
    moire_pair_sum,
    normalized_information_operator,
    phase_from_normalized_turn,
    radian_information_operator,
)


def test_relational_center_coordinate_identity():
    assert centered_relational_coordinate(0.5) == pytest.approx(0.0)
    assert external_relational_coordinate(0.0) == pytest.approx(0.5)
    assert centered_relational_coordinate(0.25) == pytest.approx(-0.5)
    assert centered_relational_coordinate(0.75) == pytest.approx(0.5)


def test_center_half_turn_bridge_is_explicit_and_maps_to_minus_one():
    bridge = CenterHalfTurnBridge()
    assert bridge.center == pytest.approx(0.0)
    assert bridge.half_turn == pytest.approx(0.5)
    assert bridge.phase.real == pytest.approx(-1.0)
    assert bridge.phase.imag == pytest.approx(0.0, abs=1e-12)


def test_canonical_kappa_normalization():
    assert canonical_mixing_channels(3) == 24
    assert CANONICAL_MIXING_CHANNELS == 24
    assert CANONICAL_MIXING_TURN_MEASURE == pytest.approx(12.0)
    assert KAPPA_Q == pytest.approx(log(2.0) / 12.0)
    assert KAPPA_PHI == pytest.approx(log(2.0) / (24.0 * pi))
    assert normalized_information_operator() == pytest.approx(KAPPA_Q)
    assert radian_information_operator() == pytest.approx(KAPPA_PHI)


def test_information_one_form_is_coordinate_covariant():
    for dq in (-2.5, -0.5, 0.0, 0.25, 1.75):
        dphi = 2.0 * pi * dq
        assert information_increment_turns(dq) == pytest.approx(
            information_increment_radians(dphi)
        )


def test_hilbert_moire_relative_phase():
    left = HilbertMoireFibreState(
        OccurrenceAddress((-1,)),
        "orbit-a",
        0.125,
        (1.0 + 0.0j, 1.0j),
    )
    right = HilbertMoireFibreState(
        OccurrenceAddress((1,)),
        "orbit-b",
        -0.125,
        (1.0 + 0.0j,),
    )
    expected = phase_from_normalized_turn(0.25)
    assert left.relative_phase(right) == pytest.approx(expected)
    assert left.norm == pytest.approx(2.0**0.5)


def test_two_layer_moire_factorization():
    for qi, qj in ((0.1, 0.2), (-0.25, 0.75), (0.5, 0.0), (2.25, -1.5)):
        assert moire_pair_sum(1.25 - 0.5j, qi, qj) == pytest.approx(
            moire_pair_factored(1.25 - 0.5j, qi, qj)
        )


def test_invalid_center_bridge_rejected():
    with pytest.raises(ValueError):
        CenterHalfTurnBridge(balance_coordinate=0.4)
