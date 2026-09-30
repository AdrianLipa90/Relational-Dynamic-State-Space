import math

import pytest

from rdss import (
    U1Phase,
    ZeroAxisPoint,
    finite_zero_axis_lift_u1,
    finite_zero_axis_phase,
)
from rdss.bridges import (
    UnsupportedBridgeError,
    rdss_bridge_registry,
)


def test_u1_phase_from_angle_and_turns_agree():
    from_angle = U1Phase.from_angle(math.pi / 2.0)
    from_turns = U1Phase.from_turns(0.25)

    assert abs(from_angle.value - 1j) <= 1e-12
    assert abs(from_turns.value - 1j) <= 1e-12
    assert abs(from_angle.value - from_turns.value) <= 1e-12


def test_u1_phase_rejects_zero_and_nonunit_values():
    with pytest.raises(ValueError):
        U1Phase(0j)

    with pytest.raises(ValueError):
        U1Phase(2 + 0j)


def test_u1_phase_group_inverse_and_composition():
    phase = U1Phase.from_angle(0.73)
    identity = phase.compose(phase.inverse())

    assert abs(identity.value - (1 + 0j)) <= 1e-12
    assert abs(identity.angle) <= 1e-12


def test_typed_zero_axis_roundtrip_is_numerically_lossless():
    point = ZeroAxisPoint(0.123)
    phase = finite_zero_axis_phase(point)
    recovered = finite_zero_axis_lift_u1(phase)

    assert abs(recovered.t - point.t) <= 1e-12


def test_bridge_registry_accepts_u1_zero_axis_numerical_roundtrip():
    registry = rdss_bridge_registry()
    point = ZeroAxisPoint(0.123)

    forward = registry.direct(
        finite_zero_axis_phase(point),
        "zero_axis_point",
    )
    backward = registry.direct(
        point,
        "u1_phase",
    )

    assert forward.fully_reversible
    assert backward.fully_reversible
    assert abs(forward.value.t - point.t) <= 1e-12
    assert abs(
        backward.value.value - point.omega
    ) <= 1e-12


def test_exceptional_minus_one_phase_has_no_finite_zero_axis_bridge():
    registry = rdss_bridge_registry()
    exceptional = U1Phase(-1 + 0j)

    with pytest.raises(UnsupportedBridgeError):
        registry.direct(
            exceptional,
            "zero_axis_point",
        )
