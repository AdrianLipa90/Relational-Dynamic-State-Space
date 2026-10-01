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
    DEFINITIONAL = "definitional"
    DERIVATION_GATE = "derivation_gate"
    EXACT_IDENTITY = "exact_identity"
    STANDARD_GEOMETRY = "standard_geometry"
    CONDITIONAL_STANDARD_RESULT = "conditional_standard_result"
    MODEL_THEOREM = "model_theorem"
    CONDITIONAL_EXACT = "conditional_exact"


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
        ExistenceChainStatus.DEFINITIONAL,
        "not N -> P_E",
        "P_E is the modal/admissible complement of absolute nothingness; no physical potential is implied.",
    ),
    ExistenceChainStep(
        "L1_MODEL_TO_MINIMAL_POINT",
        "First-Law/META0 admitted model",
        "one-carrier minimal point realization",
        ExistenceChainStatus.MODEL_THEOREM,
        "min |Adm| = 1",
        "This is a bare model-formation minimum, not a physical collapse of P_E.",
    ),
    ExistenceChainStep(
        "POINT_TO_INFORMATIONALITY",
        "minimal realized point carrier",
        "non-trivial information state",
        ExistenceChainStatus.DERIVATION_GATE,
        "point -> information-bearing distinction",
        "This is now the single upstream Hamlet gate: why must bare existence be informationally non-trivial?",
    ),
    ExistenceChainStep(
        "INFORMATIONALITY_TO_BINARY",
        "non-trivial finite information state",
        "minimal two-alternative carrier",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "min |Omega| = 2",
        "Exact from the definition of non-trivial finite information once informationality is admitted.",
    ),
    ExistenceChainStep(
        "BINARY_TO_Z2_AUTOMORPHISM",
        "unlabelled two-alternative carrier",
        "swap symmetry Z2",
        ExistenceChainStatus.EXACT_IDENTITY,
        "Aut({a,b}) = S2 ~= Z2",
    ),
    ExistenceChainStep(
        "EXISTENCE_POTENTIAL_TO_HAMLET",
        "existence potential P_E through an informationally non-trivial minimal realization",
        "Hamlet Z2 uncertainty",
        ExistenceChainStatus.DERIVATION_GATE,
        "P_E -> point -> information -> 2 outcomes -> Z2",
        "Only the point-to-informationality arrow remains genuinely open in this factorization.",
    ),
    ExistenceChainStep(
        "HAMLET_TO_HALF_HALF",
        "Z2-symmetric Hamlet carrier",
        "balanced probabilities",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "swap-invariant normalized weighting -> p_+=p_-=1/2",
        "The unique normalized weighting invariant under the non-trivial swap is uniform.",
    ),
    ExistenceChainStep(
        "HALF_HALF_TO_LN2",
        "balanced binary probabilities",
        "one-bit Shannon information in nats",
        ExistenceChainStatus.EXACT_IDENTITY,
        "H(1/2,1/2)=ln(2)",
    ),
    ExistenceChainStep(
        "Z2_TO_SIGN_CHARACTER",
        "Hamlet symmetry Z2",
        "normalized real sign character {-1,+1}",
        ExistenceChainStatus.STANDARD_GEOMETRY,
        "rho(nontrivial element)=-1, rho(identity)=+1",
        "The sign opposition is structural; its overall numerical scale is a normalization choice.",
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
        "CP1_GEOMETRY_TO_BERRY_PHASE",
        "CP1 projective geometry with parallel transport",
        "Berry geometric holonomy phase",
        ExistenceChainStatus.STANDARD_GEOMETRY,
        "gamma_B = holonomy(connection) on a closed projective-state loop",
        "The geometric phase is the holonomy of the natural line-bundle connection.",
    ),
    ExistenceChainStep(
        "BERRY_PHASE_TO_CONNECTION_POTENTIAL_CLASS",
        "Berry phase / holonomy",
        "local phase-connection potential class",
        ExistenceChainStatus.CONDITIONAL_STANDARD_RESULT,
        "gamma_B[C] = integral_C A_B  (mod 2*pi)",
        "A_B is a local representative defined only up to gauge; one phase value does not determine a unique potential.",
    ),
    ExistenceChainStep(
        "HAMLET_TO_PROJECTIVE_SIGN_CLOSURE",
        "Hamlet binary non-triviality",
        "primitive projective sign closure",
        ExistenceChainStatus.DERIVATION_GATE,
        "non-trivial branch closure -> exp(i*gamma)=-1",
        "Mega-audit must derive, not assume, why one primitive closed cycle carries the non-trivial sign.",
    ),
    ExistenceChainStep(
        "BERRY_EULER_HAMLET_TO_SPIN_HALF",
        "Berry geometric phase plus Hamlet projective sign closure",
        "minimal non-trivial spin sector",
        ExistenceChainStatus.CONDITIONAL_STANDARD_RESULT,
        "exp(i 2*pi*s)=-1 -> s_min=1/2",
        "Spin one half is selected once the Berry law and Hamlet-derived non-trivial sign closure are both supplied.",
    ),
)


def branch_swap(branch: int) -> int:
    """Canonical involution of the primitive binary alphabet {-1,+1}."""

    if branch not in (-1, 1):
        raise ValueError("branch must be -1 or +1")
    return -branch


def branch_word_swap(word: tuple[int, ...]) -> tuple[int, ...]:
    """Extend branch swap letterwise to the finite-word address space."""

    return tuple(branch_swap(branch) for branch in word)


def hamlet_distribution() -> tuple[float, float]:
    """Unique normalized depth-one weights invariant under branch swap."""

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
            branch_swap(branch_swap(-1)) == -1,
            branch_swap(branch_swap(1)) == 1,
            branch_word_swap(branch_word_swap((-1, 1, -1))) == (-1, 1, -1),
            isclose(hamlet_information_nats(), LN2),
            isclose(relational_zero_center(), RELATIONAL_ZETA_ZERO),
            IMAGINARY_GENERATOR * IMAGINARY_GENERATOR == -1,
            isclose(abs(u1_phase(0.731)), 1.0),
            spin_half_sign_return(),
            spin_half_full_return(),
        )
    )
