from __future__ import annotations

from dataclasses import dataclass
import cmath
from math import cos, isfinite, log, pi

from .algebra import OccurrenceAddress


LN2 = log(2.0)
CANONICAL_FLAVOUR_DIMENSION = 3
CANONICAL_LIE_DIMENSION = CANONICAL_FLAVOUR_DIMENSION**2 - 1
CANONICAL_MIXING_CHANNELS = (
    CANONICAL_FLAVOUR_DIMENSION * CANONICAL_LIE_DIMENSION
)
RELATIONAL_HALF_TURN = 0.5
CANONICAL_MIXING_TURN_MEASURE = (
    CANONICAL_MIXING_CHANNELS * RELATIONAL_HALF_TURN
)
KAPPA_Q = LN2 / CANONICAL_MIXING_TURN_MEASURE
KAPPA_PHI = KAPPA_Q / (2.0 * pi)


def centered_relational_coordinate(p: float) -> float:
    """Map normalized external coordinate p in [0,1] to Z=2p-1.

    Z=0 is the self-dual midpoint p=1/2. This is a coordinate identity;
    it is not the arithmetic statement 1/2 == 0.
    """
    value = float(p)
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError("p must be finite and lie in [0,1]")
    return 2.0 * value - 1.0


def external_relational_coordinate(z: float) -> float:
    """Inverse centered chart p=(1+Z)/2 for Z in [-1,1]."""
    value = float(z)
    if not isfinite(value) or not -1.0 <= value <= 1.0:
        raise ValueError("Z must be finite and lie in [-1,1]")
    return 0.5 * (1.0 + value)


def phase_from_normalized_turn(q: float) -> complex:
    """Return the U(1) phase exp(2*pi*i*q) for a finite normalized turn."""
    value = float(q)
    if not isfinite(value):
        raise ValueError("normalized turn must be finite")
    return cmath.exp(2j * pi * value)


@dataclass(frozen=True)
class CenterHalfTurnBridge:
    """Explicit bridge from the balanced coordinate to a U(1) half-turn class.

    This object records bridge data. RDSS does not infer a phase-circle
    displacement solely from the numerical equality p=1/2.
    """

    balance_coordinate: float = 0.5
    half_turn: float = 0.5
    tolerance: float = 1e-12

    def __post_init__(self) -> None:
        if self.tolerance <= 0 or not isfinite(self.tolerance):
            raise ValueError("tolerance must be positive and finite")
        if abs(centered_relational_coordinate(self.balance_coordinate)) > self.tolerance:
            raise ValueError("balance_coordinate must represent relational center")
        if abs(float(self.half_turn) - 0.5) > self.tolerance:
            raise ValueError("half_turn must represent q=1/2 in the normalized chart")

    @property
    def center(self) -> float:
        return centered_relational_coordinate(self.balance_coordinate)

    @property
    def phase(self) -> complex:
        return phase_from_normalized_turn(self.half_turn)


@dataclass(frozen=True)
class HilbertMoireFibreState:
    """Finite executable chart of one Hilbert-Moire fibre state.

    The abstract carrier may be modeled as a direct integral over refinement
    data. This class is only a finite fibre coordinate: occurrence address,
    orbital label, normalized U(1) phase and a non-zero Hilbert vector.
    """

    occurrence: OccurrenceAddress
    orbit_label: str
    phase_turn: float
    vector: tuple[complex, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "occurrence", OccurrenceAddress(self.occurrence))
        if not self.orbit_label.strip():
            raise ValueError("orbit_label must be non-empty")
        q = float(self.phase_turn)
        if not isfinite(q):
            raise ValueError("phase_turn must be finite")
        object.__setattr__(self, "phase_turn", q)
        values = tuple(complex(v) for v in self.vector)
        if not values:
            raise ValueError("Hilbert-Moire fibre vector must be non-empty")
        if any(not (isfinite(v.real) and isfinite(v.imag)) for v in values):
            raise ValueError("Hilbert-Moire fibre vector must be finite")
        if sum(abs(v) ** 2 for v in values) <= 0.0:
            raise ValueError("Hilbert-Moire fibre vector must be non-zero")
        object.__setattr__(self, "vector", values)

    @property
    def phase(self) -> complex:
        return phase_from_normalized_turn(self.phase_turn)

    @property
    def norm(self) -> float:
        return sum(abs(v) ** 2 for v in self.vector) ** 0.5

    def relative_phase(self, other: "HilbertMoireFibreState") -> complex:
        """Relative Moire phase U_i U_j^{-1} on the U(1) fibre."""
        if not isinstance(other, HilbertMoireFibreState):
            raise TypeError("other must be a HilbertMoireFibreState")
        return self.phase * other.phase.conjugate()


def moire_pair_sum(amplitude: complex, q_i: float, q_j: float) -> complex:
    """Two equal-amplitude U(1) fibre contributions in normalized turns."""
    a = complex(amplitude)
    if not (isfinite(a.real) and isfinite(a.imag)):
        raise ValueError("amplitude must be finite")
    return a * phase_from_normalized_turn(q_i) + a * phase_from_normalized_turn(q_j)


def moire_pair_factored(amplitude: complex, q_i: float, q_j: float) -> complex:
    """Exact mean-phase / half-difference factorization of moire_pair_sum."""
    a = complex(amplitude)
    if not (isfinite(a.real) and isfinite(a.imag)):
        raise ValueError("amplitude must be finite")
    qi = float(q_i)
    qj = float(q_j)
    if not (isfinite(qi) and isfinite(qj)):
        raise ValueError("phase turns must be finite")
    mean_phase = phase_from_normalized_turn(0.5 * (qi + qj))
    return 2.0 * a * mean_phase * cos(pi * (qi - qj))


def canonical_mixing_channels(n_flavour: int = 3) -> int:
    """Reference incidence count n * dim(su(n)) = n*(n^2-1)."""
    n = int(n_flavour)
    if n < 2:
        raise ValueError("n_flavour must be at least 2")
    return n * (n * n - 1)


def normalized_information_operator(
    *,
    information_nats: float = LN2,
    channel_count: int = CANONICAL_MIXING_CHANNELS,
    turn_per_channel: float = RELATIONAL_HALF_TURN,
) -> float:
    """Information density per normalized orbital turn."""
    info = float(information_nats)
    channels = int(channel_count)
    turn = float(turn_per_channel)
    if not isfinite(info) or info < 0.0:
        raise ValueError("information_nats must be finite and non-negative")
    if channels <= 0:
        raise ValueError("channel_count must be positive")
    if not isfinite(turn) or turn <= 0.0:
        raise ValueError("turn_per_channel must be positive and finite")
    return info / (channels * turn)


def radian_information_operator(kappa_q: float = KAPPA_Q) -> float:
    """Coordinate transform from normalized turns q to radians phi=2*pi*q."""
    value = float(kappa_q)
    if not isfinite(value):
        raise ValueError("kappa_q must be finite")
    return value / (2.0 * pi)


def information_increment_turns(delta_q: float) -> float:
    """Canonical information increment dI = kappa_q dq."""
    value = float(delta_q)
    if not isfinite(value):
        raise ValueError("delta_q must be finite")
    return KAPPA_Q * value


def information_increment_radians(delta_phi: float) -> float:
    """Canonical radian-chart increment dI = kappa_phi dphi."""
    value = float(delta_phi)
    if not isfinite(value):
        raise ValueError("delta_phi must be finite")
    return KAPPA_PHI * value
