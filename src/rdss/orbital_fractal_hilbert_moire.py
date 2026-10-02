"""General orbital-fractal Hilbert-Moire executable layer.

In-repo proof status: docs/GENERAL_ORBITAL_FRACTAL_HILBERT_MOIRE_ALGEBRA.md
and src/rdss/axioms.py claim IDs DEF_OFHM_*, BRIDGE_OFHM_*, DER_OFHM_*.

External frozen sources are listed in SOURCE_REFERENCES below. The source
commit and path are part of the executable provenance contract; do not
replace them with uncited recollection.
"""
from __future__ import annotations

from dataclasses import dataclass
import cmath
from math import atan2, cos, isfinite, pi, sin, sqrt
from typing import Sequence


TWO_PI = 2.0 * pi
HILBERT_HOTEL_FREDHOLM_INDEX = 1

SOURCE_REFERENCES = (
    (
        "AdrianLipa90/Infinities",
        "339d6c58f3e7d86c67a4f758cd7416692f8f8280",
        "research/EULERS_INFINITY_V0_1.md",
    ),
    (
        "AdrianLipa90/Infinities",
        "339d6c58f3e7d86c67a4f758cd7416692f8f8280",
        "research/TIR_E6_FOURIER_HILBERT_HOTEL_CORE_V0_1.md",
    ),
    (
        "AdrianLipa90/GREMLIN",
        "b0000828238e0cd244f5eb1fb679155315df372f",
        "spec/GREMLIN_HOLOGRAPHIC_ORBITAL_MEMORY_V0_1.md",
    ),
    (
        "AdrianLipa90/Informational-Dynamics-of-Metatime",
        "31f1a74d65aeb5e107840fa9971b335c7f339504",
        "CIEL-_SOT_Agent-main/docs/science/RELATIONAL_SEED_ORBIT_SOLVER_V0.md",
    ),
)

OFHM_RULE_DEPENDENCIES = {
    "symbolic_fractal_boundary": (
        "euler_symbolic_branch_space",
        "hilbert_hotel_shift",
    ),
    "moire_cocycle": (
        "bees_relative_phase_coherence",
    ),
    "hilbert_transport": (
        "moire_cocycle",
    ),
    "phase_dynamics": (
        "bees_local_coupling",
        "idt_phase_update",
    ),
}


def _require_finite(value: float, *, name: str) -> float:
    out = float(value)
    if not isfinite(out):
        raise ValueError(f"{name} must be finite")
    return out


def normalize_angle(theta: float) -> float:
    return _require_finite(theta, name="theta") % TWO_PI


def circular_delta(left: float, right: float) -> float:
    a = _require_finite(left, name="left")
    b = _require_finite(right, name="right")
    return atan2(sin(a - b), cos(a - b))


def zigzag_encode(value: int) -> int:
    n = int(value)
    return 2 * n if n >= 0 else -2 * n - 1


def zigzag_decode(code: int) -> int:
    n = int(code)
    if n < 0:
        raise ValueError("zigzag code must be non-negative")
    return n // 2 if n % 2 == 0 else -(n // 2) - 1


def cantor_pair(left: int, right: int) -> int:
    a = int(left)
    b = int(right)
    if a < 0 or b < 0:
        raise ValueError("Cantor pairing inputs must be non-negative")
    s = a + b
    return (s * (s + 1)) // 2 + b


def cantor_unpair(code: int) -> tuple[int, int]:
    z = int(code)
    if z < 0:
        raise ValueError("Cantor pairing code must be non-negative")
    w = (int(sqrt(8 * z + 1)) - 1) // 2
    while ((w + 1) * (w + 2)) // 2 <= z:
        w += 1
    while (w * (w + 1)) // 2 > z:
        w -= 1
    t = (w * (w + 1)) // 2
    right = z - t
    left = w - right
    return left, right


def countable_word_rank(address: Sequence[int]) -> int:
    """Bijection from finite integer words Z^{<omega} to N.

    Provenance: DEF_OFHM_COUNTABLE_BRANCH_ADDRESS and the frozen Infinities
    Hilbert-Hotel source in SOURCE_REFERENCES. The encoding is an enumeration
    coordinate only; it does not replace the prefix/tree relation.
    """
    code = 0
    for branch in reversed(tuple(int(x) for x in address)):
        code = 1 + cantor_pair(zigzag_encode(branch), code)
    return code


def countable_word_unrank(rank: int) -> tuple[int, ...]:
    code = int(rank)
    if code < 0:
        raise ValueError("rank must be non-negative")
    out: list[int] = []
    while code:
        head, tail = cantor_unpair(code - 1)
        out.append(zigzag_decode(head))
        code = tail
    return tuple(out)


@dataclass(frozen=True, order=True)
class CountableBranchAddress:
    """Finite symbolic address with countable integer branch alphabet."""

    word: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "word", tuple(int(x) for x in self.word))

    @property
    def depth(self) -> int:
        return len(self.word)

    @property
    def rank(self) -> int:
        return countable_word_rank(self.word)

    def child(self, branch: int) -> "CountableBranchAddress":
        return CountableBranchAddress(self.word + (int(branch),))

    def hilbert_hotel_successor(self) -> "CountableBranchAddress":
        return CountableBranchAddress(countable_word_unrank(self.rank + 1))

    def hilbert_hotel_predecessor(self) -> "CountableBranchAddress | None":
        if self.rank == 0:
            return None
        return CountableBranchAddress(countable_word_unrank(self.rank - 1))


def binary_occurrence_to_countable(address: Sequence[int]) -> CountableBranchAddress:
    word = tuple(int(x) for x in address)
    if any(x not in (-1, 1) for x in word):
        raise ValueError("binary RDSS occurrence branches must be -1 or +1")
    return CountableBranchAddress(word)


def euler_phase(z: complex) -> complex:
    value = complex(z)
    if not (isfinite(value.real) and isfinite(value.imag)):
        raise ValueError("z must be finite")
    return cmath.exp(1j * pi * value)


def euler_inverse_branch(w: complex, branch: int) -> complex:
    """One Euler inverse branch using Python's principal complex Log.

    Provenance: BRIDGE_OFHM_EULER_SYMBOLIC_BRANCH_SPACE and the frozen
    Infinities Euler source in SOURCE_REFERENCES. This is the declared-Log-
    branch realization of
    E_k^{-1}(w) = 2k - (i/pi) Log(w).
    """
    value = complex(w)
    if value == 0:
        raise ValueError("Euler inverse branch is undefined at w=0")
    if not (isfinite(value.real) and isfinite(value.imag)):
        raise ValueError("w must be finite")
    return 2 * int(branch) - (1j / pi) * cmath.log(value)


def euler_branch_preimage(
    seed: complex,
    address: CountableBranchAddress | Sequence[int],
) -> complex:
    current = complex(seed)
    word = (
        address.word
        if isinstance(address, CountableBranchAddress)
        else tuple(int(x) for x in address)
    )
    for branch in word:
        current = euler_inverse_branch(current, branch)
    return current


def relative_moire_phase(theta_i: float, theta_j: float) -> complex:
    """U(1) relative phase M_ij = U_i U_j^{-1}.

    Provenance: DER_OFHM_MOIRE_COCYCLE. The phase data, not the scalar
    coherence magnitude alone, determines this U(1) cocycle.
    """
    return cmath.exp(1j * circular_delta(theta_i, theta_j))


def moire_cocycle_error(theta_i: float, theta_j: float, theta_k: float) -> float:
    left = relative_moire_phase(theta_i, theta_j) * relative_moire_phase(
        theta_j,
        theta_k,
    )
    right = relative_moire_phase(theta_i, theta_k)
    return abs(left - right)


def phase_coherence_overlap(left: Sequence[float], right: Sequence[float]) -> float:
    """BEES/GREMLIN relative-phase coherence generalized to any finite dimension."""
    a = tuple(_require_finite(x, name="left phase") for x in left)
    b = tuple(_require_finite(x, name="right phase") for x in right)
    if not a or len(a) != len(b):
        raise ValueError("phase vectors must be non-empty and have equal length")
    z = sum(
        cmath.exp(1j * circular_delta(x, y))
        for x, y in zip(a, b)
    ) / len(a)
    return abs(z)


def hilbert_norm(vector: Sequence[complex]) -> float:
    values = tuple(complex(v) for v in vector)
    if not values:
        raise ValueError("Hilbert vector must be non-empty")
    if any(not (isfinite(v.real) and isfinite(v.imag)) for v in values):
        raise ValueError("Hilbert vector must be finite")
    return sqrt(sum(abs(v) ** 2 for v in values))


def moire_transport(
    vector: Sequence[complex],
    *,
    theta_target: float,
    theta_source: float,
) -> tuple[complex, ...]:
    """Transport a fibre vector from source chart to target chart.

    Provenance: DER_OFHM_HILBERT_TRANSPORT.
    T_ij v = M_ij v, with M_ij=U_i U_j^{-1}.
    """
    values = tuple(complex(v) for v in vector)
    hilbert_norm(values)
    phase = relative_moire_phase(theta_target, theta_source)
    return tuple(phase * v for v in values)


@dataclass(frozen=True)
class OrbitalFractalHilbertMoireState:
    address: CountableBranchAddress
    orbit_label: str
    phase: float
    vector: tuple[complex, ...]
    angular_velocity: float = 0.0

    def __post_init__(self) -> None:
        address = self.address
        if not isinstance(address, CountableBranchAddress):
            address = CountableBranchAddress(tuple(address))
        object.__setattr__(self, "address", address)
        if not str(self.orbit_label).strip():
            raise ValueError("orbit_label must be non-empty")
        object.__setattr__(self, "orbit_label", str(self.orbit_label))
        object.__setattr__(self, "phase", normalize_angle(self.phase))
        values = tuple(complex(v) for v in self.vector)
        hilbert_norm(values)
        object.__setattr__(self, "vector", values)
        object.__setattr__(
            self,
            "angular_velocity",
            _require_finite(self.angular_velocity, name="angular_velocity"),
        )

    @property
    def norm(self) -> float:
        return hilbert_norm(self.vector)

    def refine(self, branch: int) -> "OrbitalFractalHilbertMoireState":
        return OrbitalFractalHilbertMoireState(
            self.address.child(branch),
            self.orbit_label,
            self.phase,
            self.vector,
            self.angular_velocity,
        )

    def hotel_successor(self) -> "OrbitalFractalHilbertMoireState":
        return OrbitalFractalHilbertMoireState(
            self.address.hilbert_hotel_successor(),
            self.orbit_label,
            self.phase,
            self.vector,
            self.angular_velocity,
        )

    def relative_phase(
        self,
        other: "OrbitalFractalHilbertMoireState",
    ) -> complex:
        return relative_moire_phase(self.phase, other.phase)

    def transport_from(
        self,
        other: "OrbitalFractalHilbertMoireState",
    ) -> tuple[complex, ...]:
        return moire_transport(
            other.vector,
            theta_target=self.phase,
            theta_source=other.phase,
        )


def phase_coupling_current(
    phase: float,
    neighbor_phases: Sequence[float],
    *,
    weights: Sequence[float] | None = None,
    normalize: bool = True,
) -> float:
    """Weighted BEES/IDT sine-coupling current."""
    center = _require_finite(phase, name="phase")
    neighbors = tuple(
        _require_finite(x, name="neighbor phase")
        for x in neighbor_phases
    )
    if not neighbors:
        return 0.0
    if weights is None:
        w = tuple(1.0 for _ in neighbors)
    else:
        if len(weights) != len(neighbors):
            raise ValueError("weights length mismatch")
        w = tuple(_require_finite(x, name="weight") for x in weights)
        if any(x < 0.0 for x in w):
            raise ValueError("weights must be non-negative")
    total_weight = sum(w)
    if total_weight <= 0.0:
        raise ValueError("at least one coupling weight must be positive")
    current = sum(
        weight * sin(other - center)
        for other, weight in zip(neighbors, w)
    )
    return current / total_weight if normalize else current


def bees_overdamped_phase_step(
    phase: float,
    neighbor_phases: Sequence[float],
    *,
    weights: Sequence[float] | None = None,
    coupling: float = 1.0,
    dt: float = 0.05,
) -> float:
    """One bounded first-order phase step of the GREMLIN/BEES type."""
    h = _require_finite(dt, name="dt")
    k = _require_finite(coupling, name="coupling")
    if h <= 0.0:
        raise ValueError("dt must be positive")
    if k < 0.0:
        raise ValueError("coupling must be non-negative")
    current = phase_coupling_current(
        phase,
        neighbor_phases,
        weights=weights,
        normalize=True,
    )
    return normalize_angle(phase + h * k * current)


def idt_phase_dynamics_step(
    state: OrbitalFractalHilbertMoireState,
    neighbor_phases: Sequence[float],
    *,
    weights: Sequence[float] | None = None,
    dt: float,
    damping: float = 0.0,
    potential_gradient: float = 0.0,
    drive: float = 0.0,
    coupling: float = 1.0,
) -> OrbitalFractalHilbertMoireState:
    """One explicit IDT-style second-order phase update.

    Provenance: BRIDGE_OFHM_BEES_IDT_DYNAMICS plus the frozen GREMLIN and
    IDT sources in SOURCE_REFERENCES.

    phi_(k+1) = phi_k + dt * omega_k
    omega_(k+1) = omega_k + dt * (-dV/dphi - eta*omega_k + K*J_k + drive)
    """
    h = _require_finite(dt, name="dt")
    eta = _require_finite(damping, name="damping")
    grad = _require_finite(
        potential_gradient,
        name="potential_gradient",
    )
    external = _require_finite(drive, name="drive")
    k = _require_finite(coupling, name="coupling")
    if h <= 0.0:
        raise ValueError("dt must be positive")
    if eta < 0.0:
        raise ValueError("damping must be non-negative")
    if k < 0.0:
        raise ValueError("coupling must be non-negative")
    current = phase_coupling_current(
        state.phase,
        neighbor_phases,
        weights=weights,
        normalize=False,
    )
    next_phase = normalize_angle(
        state.phase + h * state.angular_velocity
    )
    next_velocity = state.angular_velocity + h * (
        -grad
        - eta * state.angular_velocity
        + k * current
        + external
    )
    return OrbitalFractalHilbertMoireState(
        state.address,
        state.orbit_label,
        next_phase,
        state.vector,
        next_velocity,
    )
