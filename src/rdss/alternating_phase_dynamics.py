from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, log, pi, sin
from typing import Sequence

from .bipolar_tetrahedral_exchange import forced_kappa_closed_form


# REF: TIR main @ 9783782570a2ccfa1fc42c99b605dad48e02aa78
#       TIR/foundations/TIR_PRESPACETIME_STELLA_HALF_SUCCESSOR_V0_1.md
#       exact H(n,+)=(n,-), H(n,-)=(n+1,+), hence H^2=S and Delta nu=1/2.
# REF: TIR main @ 9783782570a2ccfa1fc42c99b605dad48e02aa78
#       TIR/foundations/TIR_STELLA_ALTERNATING_ROTATION_INFERENCE_V0_1.md
#       one half-step transforms one Stella sector; the next transforms the other.
# REF: TIR main @ 9783782570a2ccfa1fc42c99b605dad48e02aa78
#       TIR/foundations/TIR_RELATIONAL_PHASE_LAGRANGIAN_CORE_V0_1.md
#       exact U(1) phase coordinate and positive phase inertia.
# REF: TIR main @ 9783782570a2ccfa1fc42c99b605dad48e02aa78
#       TIR/foundations/TIR_WHITE_THREAD_SPIN_LIFT_LYAPUNOV_V0_1.md
#       1-cos phase-mismatch potential, Euler-Lagrange-Rayleigh equations,
#       overdamped gauge-twisted Kuramoto limit and Lyapunov identity.
# REF: TIR main @ 9783782570a2ccfa1fc42c99b605dad48e02aa78
#       TIR/foundations/TIR_KAPPA_FLAVOUR_MIXING_NORMALIZATION_V0_1.md
#       24 directed half-turn channels and kappa=ln(2)/(24*pi).
# REF: RDSS parent main @ e1d2dda2ffbcbb38392869f94012cea03fffd751
#       THM_BIPOLAR_KAPPA_FORCED and the 24-directed / 12-paired exchange orbit.


DIRECTED_CHANNEL_COUNT = 24
UNDIRECTED_EXCHANGE_PAIR_COUNT = 12
BINARY_INFORMATION_NATS = log(2.0)
KAPPA = forced_kappa_closed_form()

# One directed channel carries ln(2)/24 = pi*kappa.
DIRECTED_CHANNEL_INFORMATION_NATS = BINARY_INFORMATION_NATS / DIRECTED_CHANNEL_COUNT

# One undirected exchange pair contains two opposite directed incidences.
UNDIRECTED_PAIR_INFORMATION_NATS = (
    BINARY_INFORMATION_NATS / UNDIRECTED_EXCHANGE_PAIR_COUNT
)

# The normalized chordal mismatch c(delta)=(1-cos(delta))/2 reaches one at
# the canonical half-turn delta=pi. Therefore the unique coefficient in
# V_pair=A*(1-cos(delta)) that saturates one pair information budget at pi is
# A=(ln(2)/12)/2 = ln(2)/24 = pi*kappa.
CANONICAL_PAIR_POTENTIAL_AMPLITUDE = (
    UNDIRECTED_PAIR_INFORMATION_NATS / 2.0
)


def signed_angle(angle: float) -> float:
    """Principal signed representative in (-pi, pi]."""

    return atan2(sin(float(angle)), cos(float(angle)))


@dataclass(frozen=True)
class StellaHalfOccurrence:
    """Exact pretime half-successor carrier.

    sector=+1 represents the plus Stella occurrence at integer grade n.
    sector=-1 represents the complementary occurrence at grade n+1/2.
    The phase state itself remains U(1)-continuous; only the occurrence order
    is discrete.
    """

    frame: int
    sector: int

    def __post_init__(self) -> None:
        if self.frame < 0:
            raise ValueError("frame must be non-negative")
        if self.sector not in (-1, 1):
            raise ValueError("sector must be +/-1")

    @property
    def grade(self) -> float:
        return float(self.frame) if self.sector == 1 else self.frame + 0.5

    def half_successor(self) -> "StellaHalfOccurrence":
        if self.sector == 1:
            return StellaHalfOccurrence(self.frame, -1)
        return StellaHalfOccurrence(self.frame + 1, 1)

    def full_successor(self) -> "StellaHalfOccurrence":
        return self.half_successor().half_successor()


def phase_mismatch(
    theta_left: float,
    theta_right: float,
    *,
    holonomy: float = 0.0,
) -> float:
    """Gauge-covariant projected U(1) mismatch."""

    return signed_angle(float(theta_left) - float(theta_right) - float(holonomy))


def chordal_mismatch_cost(delta: float) -> float:
    """Normalized U(1) chordal mismatch in [0,1].

    c(delta)=|e^(i delta)-1|^2/4=(1-cos(delta))/2.
    It vanishes at relational alignment and equals one at the half-turn.
    """

    return 0.5 * (1.0 - cos(float(delta)))


def canonical_pair_information_potential_from_delta(delta: float) -> float:
    """Information potential of one undirected bipolar exchange pair.

    V_pair(pi)=ln(2)/12, exactly the information budget of two opposite
    directed incidences from the canonical 24-channel orbit.
    """

    return UNDIRECTED_PAIR_INFORMATION_NATS * chordal_mismatch_cost(delta)


def canonical_pair_information_potential(
    theta_left: float,
    theta_right: float,
    *,
    holonomy: float = 0.0,
) -> float:
    return canonical_pair_information_potential_from_delta(
        phase_mismatch(theta_left, theta_right, holonomy=holonomy)
    )


def canonical_pair_gradient_from_delta(delta: float) -> float:
    """dV/d(delta)=pi*kappa*sin(delta)=ln(2)/24*sin(delta)."""

    return CANONICAL_PAIR_POTENTIAL_AMPLITUDE * sin(float(delta))


def bipolar_pair_forces_from_delta(delta: float) -> tuple[float, float]:
    """Opposite gradient forces on the two Stella sectors.

    For V(theta_+,theta_-)=A*(1-cos(theta_+-theta_-)),
    F_+=-dV/dtheta_+ and F_-=-dV/dtheta_-.
    Their sum is identically zero.
    """

    gradient = canonical_pair_gradient_from_delta(delta)
    return (-gradient, gradient)


def bipolar_pair_forces(
    theta_plus: float,
    theta_minus: float,
    *,
    holonomy: float = 0.0,
) -> tuple[float, float]:
    return bipolar_pair_forces_from_delta(
        phase_mismatch(theta_plus, theta_minus, holonomy=holonomy)
    )


def relative_pendulum_residual(
    delta: float,
    delta_velocity: float,
    delta_acceleration: float,
    *,
    phase_inertia: float,
    damping: float = 0.0,
) -> float:
    """Residual of the exact two-sector relative pendulum equation.

    Equal sector inertia I and equal Rayleigh coefficient eta give

        I*delta_ddot + eta*delta_dot + 2*A*sin(delta) = 0,

    where A=ln(2)/24=pi*kappa is fixed by the paired information budget.
    """

    inertia = float(phase_inertia)
    eta = float(damping)
    if inertia <= 0.0:
        raise ValueError("phase_inertia must be positive")
    if eta < 0.0:
        raise ValueError("damping must be non-negative")
    return (
        inertia * float(delta_acceleration)
        + eta * float(delta_velocity)
        + 2.0 * CANONICAL_PAIR_POTENTIAL_AMPLITUDE * sin(float(delta))
    )


def center_phase_residual(
    center_velocity: float,
    center_acceleration: float,
    *,
    phase_inertia: float,
    damping: float = 0.0,
) -> float:
    """Center-sector equation: I*c_ddot + eta*c_dot = 0.

    The interaction contributes no center force because the pair gradients are
    exactly opposite. In the conservative core (eta=0), the center is inertial.
    """

    inertia = float(phase_inertia)
    eta = float(damping)
    if inertia <= 0.0:
        raise ValueError("phase_inertia must be positive")
    if eta < 0.0:
        raise ValueError("damping must be non-negative")
    return inertia * float(center_acceleration) + eta * float(center_velocity)


def second_frame_difference(previous: float, current: float, following: float) -> float:
    """Unique local symmetric second-difference up to overall scale.

    Translation invariance plus annihilation of constant and uniform-drift
    sequences force coefficients proportional to (1,-2,1).
    """

    return float(following) - 2.0 * float(current) + float(previous)


def pendulum_frame_residual(
    previous_delta: float,
    current_delta: float,
    following_delta: float,
    *,
    phase_inertia: float,
    full_step: float = 1.0,
) -> float:
    """Frame-native conservative pendulum residual on the full successor S=H^2."""

    inertia = float(phase_inertia)
    h = float(full_step)
    if inertia <= 0.0:
        raise ValueError("phase_inertia must be positive")
    if h <= 0.0:
        raise ValueError("full_step must be positive")
    discrete_acceleration = (
        second_frame_difference(previous_delta, current_delta, following_delta)
        / (h * h)
    )
    return (
        inertia * discrete_acceleration
        + 2.0 * CANONICAL_PAIR_POTENTIAL_AMPLITUDE * sin(float(current_delta))
    )


def pendulum_frame_successor(
    previous_delta: float,
    current_delta: float,
    *,
    phase_inertia: float,
    full_step: float = 1.0,
) -> float:
    """Solve the frame-native conservative pendulum law for delta_(n+1).

    The result is an unwrapped phase lift. Projection to U(1) may be applied
    afterwards with signed_angle; keeping the lift avoids branch artefacts in
    the second difference.
    """

    inertia = float(phase_inertia)
    h = float(full_step)
    if inertia <= 0.0:
        raise ValueError("phase_inertia must be positive")
    if h <= 0.0:
        raise ValueError("full_step must be positive")
    acceleration_term = (
        2.0 * CANONICAL_PAIR_POTENTIAL_AMPLITUDE
        * sin(float(current_delta))
        / inertia
    )
    return (
        2.0 * float(current_delta)
        - float(previous_delta)
        - h * h * acceleration_term
    )


@dataclass(frozen=True)
class MoireEdge:
    """One undirected Moire exchange pair.

    holonomy is the oriented left->right phase offset; path reversal changes
    its sign. Each undirected edge already represents the two opposite
    directed incidences, so its canonical information budget is ln(2)/12.
    """

    left: int
    right: int
    holonomy: float = 0.0

    def __post_init__(self) -> None:
        if self.left < 0 or self.right < 0:
            raise ValueError("edge endpoints must be non-negative")
        if self.left == self.right:
            raise ValueError("Moire edge requires distinct endpoints")


def canonical_moire_information_potential(
    phases: Sequence[float],
    edges: Sequence[MoireEdge],
) -> float:
    """Sum the canonical paired information potential over undirected edges."""

    values = tuple(float(x) for x in phases)
    total = 0.0
    for edge in edges:
        if edge.left >= len(values) or edge.right >= len(values):
            raise ValueError("edge endpoint outside phase vector")
        delta = phase_mismatch(
            values[edge.left],
            values[edge.right],
            holonomy=edge.holonomy,
        )
        total += canonical_pair_information_potential_from_delta(delta)
    return total


def canonical_moire_gradient(
    phases: Sequence[float],
    edges: Sequence[MoireEdge],
) -> tuple[float, ...]:
    """Exact gradient of the canonical Moire information potential."""

    values = tuple(float(x) for x in phases)
    gradient = [0.0 for _ in values]
    for edge in edges:
        if edge.left >= len(values) or edge.right >= len(values):
            raise ValueError("edge endpoint outside phase vector")
        delta = phase_mismatch(
            values[edge.left],
            values[edge.right],
            holonomy=edge.holonomy,
        )
        g = canonical_pair_gradient_from_delta(delta)
        gradient[edge.left] += g
        gradient[edge.right] -= g
    return tuple(gradient)


def canonical_kuramoto_velocity(
    phases: Sequence[float],
    edges: Sequence[MoireEdge],
    *,
    damping: float | Sequence[float] = 1.0,
) -> tuple[float, ...]:
    """Overdamped gradient flow of the canonical Moire potential.

    eta_i * theta_dot_i = -dV/dtheta_i.

    This is the Kuramoto sine flow generated by the same potential that gives
    the inertial pendulum before the overdamped reduction.
    """

    gradient = canonical_moire_gradient(phases, edges)
    if isinstance(damping, (int, float)):
        eta = tuple(float(damping) for _ in gradient)
    else:
        eta = tuple(float(x) for x in damping)
        if len(eta) != len(gradient):
            raise ValueError("damping length mismatch")
    if any(x <= 0.0 for x in eta):
        raise ValueError("all damping coefficients must be positive")
    return tuple(-g / e for g, e in zip(gradient, eta))


def canonical_kuramoto_lyapunov_rate(
    phases: Sequence[float],
    edges: Sequence[MoireEdge],
    *,
    damping: float | Sequence[float] = 1.0,
) -> float:
    """Exact overdamped Lyapunov derivative dV/dtau <= 0."""

    gradient = canonical_moire_gradient(phases, edges)
    if isinstance(damping, (int, float)):
        eta = tuple(float(damping) for _ in gradient)
    else:
        eta = tuple(float(x) for x in damping)
        if len(eta) != len(gradient):
            raise ValueError("damping length mismatch")
    if any(x <= 0.0 for x in eta):
        raise ValueError("all damping coefficients must be positive")
    return -sum((g * g) / e for g, e in zip(gradient, eta))


def closure_certificate() -> dict[str, float | int | bool]:
    """Machine-readable receipt for the pendulum / Moire-Kuramoto closure."""

    start = StellaHalfOccurrence(0, 1)
    half = start.half_successor()
    full = half.half_successor()
    f_plus, f_minus = bipolar_pair_forces_from_delta(0.73)
    return {
        "kappa": KAPPA,
        "directed_channels": DIRECTED_CHANNEL_COUNT,
        "undirected_pairs": UNDIRECTED_EXCHANGE_PAIR_COUNT,
        "directed_channel_information_nats": DIRECTED_CHANNEL_INFORMATION_NATS,
        "undirected_pair_information_nats": UNDIRECTED_PAIR_INFORMATION_NATS,
        "pair_potential_amplitude": CANONICAL_PAIR_POTENTIAL_AMPLITUDE,
        "pair_amplitude_equals_pi_kappa": abs(
            CANONICAL_PAIR_POTENTIAL_AMPLITUDE - pi * KAPPA
        ) <= 1e-15,
        "half_grade": half.grade,
        "full_grade": full.grade,
        "half_squared_is_full_successor": (
            full.frame == 1 and full.sector == 1
        ),
        "pair_force_sum_zero": abs(f_plus + f_minus) <= 1e-15,
        "half_turn_pair_potential": canonical_pair_information_potential_from_delta(pi),
        "full_binary_budget_at_all_12_half_turn_pairs": (
            UNDIRECTED_EXCHANGE_PAIR_COUNT
            * canonical_pair_information_potential_from_delta(pi)
        ),
    }
