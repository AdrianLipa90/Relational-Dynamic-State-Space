from __future__ import annotations

from cmath import exp
from dataclasses import dataclass
from enum import Enum
from math import isclose, log, pi


LN2 = log(2.0)
RELATIONAL_ZETA_ZERO = 0.0
IMAGINARY_GENERATOR = 1j


class ExistenceChainStatus(str, Enum):
    """Epistemic status for one arrow in the pre-audit existence chain."""

    FOUNDATIONAL_LAW = "foundational_law"
    DERIVATION_GATE = "derivation_gate"
    EXACT_IDENTITY = "exact_identity"
    STANDARD_GEOMETRY = "standard_geometry"
    CONDITIONAL_STANDARD_RESULT = "conditional_standard_result"


@dataclass(frozen=True)
class ExistencePotential:
    """Symbolic non-null possibility left after absolute nothingness is excluded.

    This type deliberately carries no magnitude, force law, energy scale or
    spacetime interpretation. Those would be additional structure and are not
    part of the pre-audit causal skeleton.
    """

    symbol: str = "P_E"


@dataclass(frozen=True)
class ExistenceChainStep:
    id: str
    source: str
    target: str
    status: ExistenceChainStatus
    formula: str
    audit_note: str = ""


FIRST_LAW_OF_EXISTENCE = (
    "Absolute nothingness is not a realizable state because it contains no "
    "object, distinction or relation by which it could be established as a state."
)


CANONICAL_EXISTENCE_CHAIN: tuple[ExistenceChainStep, ...] = (
    ExistenceChainStep(
        "L1_TO_EXISTENCE_POTENTIAL",
        "not absolute nothingness",
        "existence potential P_E",
        ExistenceChainStatus.DERIVATION_GATE,
        "not N -> P_E",
        "Mega-audit must test whether P_E is genuinely forced rather than renamed non-vacuity.",
    ),
    ExistenceChainStep(
        "EXISTENCE_POTENTIAL_TO_HAMLET",
        "existence potential P_E",
        "unresolved binary orientation",
        ExistenceChainStatus.DERIVATION_GATE,
        "P_E -> {+1,-1} with no preferred sign",
        "This is the relational 'to be / not to be' uncertainty step, not yet the Heisenberg x-p relation.",
    ),
    ExistenceChainStep(
        "HAMLET_TO_HALF_HALF",
        "unresolved symmetric binary orientation",
        "balanced probabilities",
        ExistenceChainStatus.EXACT_IDENTITY,
        "p_+=p_-=1/2",
        "Exact once binary exhaustivity and no preferred orientation are admitted.",
    ),
    ExistenceChainStep(
        "HALF_HALF_TO_LN2",
        "balanced binary probabilities",
        "one-bit Shannon information in nats",
        ExistenceChainStatus.EXACT_IDENTITY,
        "H(1/2,1/2)=ln(2)",
    ),
    ExistenceChainStep(
        "ORIENTATION_TO_RELATIONAL_ZERO",
        "normalized orientations {-1,+1}",
        "relational centre zeta=0",
        ExistenceChainStatus.EXACT_IDENTITY,
        "zeta=(-1+1)/2=0",
        "Relational zero is represented and therefore is not absolute nothingness.",
    ),
    ExistenceChainStep(
        "ORIENTATION_TO_IMAGINARY_GENERATOR",
        "real opposition {-1,+1}",
        "orthogonal generator i",
        ExistenceChainStatus.DERIVATION_GATE,
        "i^2=-1",
        "Mega-audit must test whether orthogonal complex structure is uniquely forced.",
    ),
    ExistenceChainStep(
        "IMAGINARY_GENERATOR_TO_U1",
        "imaginary generator i",
        "phase orbit U(1)",
        ExistenceChainStatus.EXACT_IDENTITY,
        "u(phi)=exp(i phi), |u|=1",
    ),
    ExistenceChainStep(
        "BINARY_PHASE_TO_CP1",
        "normalized complex two-state carrier modulo common U(1) phase",
        "CP1 / Bloch sphere",
        ExistenceChainStatus.STANDARD_GEOMETRY,
        "CP1 ~= S2",
        "The bridge requires the normalized complex two-state carrier; U(1) alone is insufficient.",
    ),
    ExistenceChainStep(
        "CP1_BERRY_EULER_TO_SPIN_HALF",
        "CP1 equatorial Berry loop plus Euler sign closure",
        "minimal non-trivial spin sector",
        ExistenceChainStatus.CONDITIONAL_STANDARD_RESULT,
        "exp(i 2*pi*s)=-1 -> s_min=1/2",
        "Conditional on the Berry phase law and primitive non-trivial sign closure.",
    ),
)


def hamlet_distribution() -> tuple[float, float]:
    """Canonical unbiased two-orientation distribution."""

    return (0.5, 0.5)


def binary_entropy_nats(p: float) -> float:
    """Binary Shannon entropy in nats."""

    q = 1.0 - float(p)
    if not (0.0 <= p <= 1.0):
        raise ValueError("p must lie in [0,1]")
    if p == 0.0 or p == 1.0:
        return 0.0
    return -(p * log(p) + q * log(q))


def hamlet_information_nats() -> float:
    return binary_entropy_nats(0.5)


def relational_zero_center(negative: float = -1.0, positive: float = 1.0) -> float:
    """Midpoint of the normalized opposite orientations."""

    return (float(negative) + float(positive)) / 2.0


def u1_phase(phi: float) -> complex:
    return exp(1j * float(phi))


def berry_equatorial_phase_factor(spin: float) -> complex:
    """Reference phase factor exp(i 2*pi*s) for a hemisphere Berry loop."""

    return exp(1j * 2.0 * pi * float(spin))


def spin_half_sign_return(tolerance: float = 1e-12) -> bool:
    return abs(berry_equatorial_phase_factor(0.5) + 1.0) <= tolerance


def spin_half_full_return(tolerance: float = 1e-12) -> bool:
    return abs(exp(1j * 4.0 * pi * 0.5) - 1.0) <= tolerance


def exact_chain_sanity() -> bool:
    """Check only exact/standard numerical identities, not open causal arrows."""

    p_minus, p_plus = hamlet_distribution()
    return all(
        (
            isclose(p_minus, 0.5),
            isclose(p_plus, 0.5),
            isclose(hamlet_information_nats(), LN2),
            isclose(relational_zero_center(), RELATIONAL_ZETA_ZERO),
            IMAGINARY_GENERATOR * IMAGINARY_GENERATOR == -1,
            isclose(abs(u1_phase(0.731)), 1.0),
            spin_half_sign_return(),
            spin_half_full_return(),
        )
    )
