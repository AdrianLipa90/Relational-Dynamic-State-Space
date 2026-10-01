from __future__ import annotations

from cmath import exp
from dataclasses import dataclass
from enum import Enum
from math import cos, isclose, log, pi, sin, sqrt


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
        "CANONICAL_REALIZED_EXISTENCE_INFORMATIONALITY",
        "canonical RDSS realized-existence semantics",
        "non-trivial information state",
        ExistenceChainStatus.DEFINITIONAL,
        "RealizedExistence_RDSS := admitted non-trivial information state",
        "This closes the canonical theory path by definition while leaving the strict L1-only entailment gate open.",
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
        "CANONICAL_REALIZED_EXISTENCE_TO_HAMLET",
        "canonical realized non-trivial information state",
        "minimal Hamlet Z2 carrier",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "definition + min |Omega|=2 + Aut(Omega_2)=Z2",
        "Closed inside canonical RDSS semantics; this is distinct from the strict L1-to-informationality question.",
    ),
    ExistenceChainStep(
        "CANONICAL_HAMLET_RELATIONAL_REALIZATION",
        "canonical Hamlet alternatives",
        "two distinct relational branch-occurrence identities",
        ExistenceChainStatus.DEFINITIONAL,
        "distinguishable alternatives -> distinct occurrence identities bound to host",
        "Canonical relational-information semantics; the universal RA0_REL_STAR entailment from bare L1 remains open.",
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
        "Closed on the canonical Hamlet carrier. The strict L1-only informationality gate is tracked separately and is not a dependency of this downstream theorem.",
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
        ExistenceChainStatus.EXACT_IDENTITY,
        "chi(g)^2=1 and chi nontrivial => chi(g)=-1",
        "This is the unique non-trivial one-dimensional real character of Z2; no upstream U(1) structure is assumed.",
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
        "ordered Hamlet real branch span with swap S and polarity P",
        "real complex-structure generator J",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "J=SP, S^2=P^2=I, SP=-PS => J^2=-I",
        "Exact on the free real two-branch span; reversing branch orientation sends J to -J, i.e. complex conjugation.",
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
        "full Hamlet operator algebra A_H=M2(R)=C_J direct-sum S C_J",
        "CP1 / Bloch sphere",
        ExistenceChainStatus.STANDARD_GEOMETRY,
        "unit(A_H)=S3; S3/right-U(1) ~= CP1 ~= S2",
        "Canonical route: complex dimension two is the right C_J-module rank of the full S/P operator algebra, avoiding a second independent copy of the binary degree of freedom.",
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
        "Hamlet J-orbit in the symmetry-fixed CP1 branch geometry",
        "canonical Berry loop realizes holonomy -1",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "psi(theta)=exp(theta J)psi_0, theta:0->pi; psi(pi)=-psi_0",
        "The orbit is horizontal in the reference Hopf connection and the first projective return therefore carries the non-trivial -1 holonomy.",
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


def z2_nontrivial_real_character(element: int) -> float:
    """Unique non-trivial real character of multiplicative Z2={+1,-1}."""

    if element not in (-1, 1):
        raise ValueError("Z2 element must be -1 or +1")
    return float(element)


def branch_swap_vector(vector: tuple[float, float]) -> tuple[float, float]:
    """Swap the ordered (-,+) branch coordinates."""

    minus, plus = map(float, vector)
    return (plus, minus)


def branch_polarity_vector(vector: tuple[float, float]) -> tuple[float, float]:
    """Apply P e_b=b e_b in the ordered (-,+) basis."""

    minus, plus = map(float, vector)
    return (-minus, plus)


def hamlet_complex_structure(vector: tuple[float, float]) -> tuple[float, float]:
    """Apply J=SP, a real-linear complex structure with J^2=-I."""

    return branch_swap_vector(branch_polarity_vector(vector))


def hamlet_j_orbit(
    theta: float,
    vector: tuple[float, float] = (1.0, 0.0),
) -> tuple[float, float]:
    """Apply exp(theta J)=cos(theta)I+sin(theta)J on the real branch span."""

    x, y = map(float, vector)
    jx, jy = hamlet_complex_structure((x, y))
    c = cos(float(theta))
    s = sin(float(theta))
    return (c * x + s * jx, c * y + s * jy)


def hamlet_j_orbit_derivative(
    theta: float,
    vector: tuple[float, float] = (1.0, 0.0),
) -> tuple[float, float]:
    """Derivative of the canonical J orbit."""

    x, y = map(float, vector)
    jx, jy = hamlet_complex_structure((x, y))
    c = cos(float(theta))
    s = sin(float(theta))
    return (-s * x + c * jx, -s * y + c * jy)


def hamlet_horizontal_residual(
    theta: float,
    vector: tuple[float, float] = (1.0, 0.0),
) -> float:
    """Reference value of <psi,dot(psi)> along the canonical J orbit."""

    psi = hamlet_j_orbit(theta, vector)
    dpsi = hamlet_j_orbit_derivative(theta, vector)
    return psi[0] * dpsi[0] + psi[1] * dpsi[1]


def hamlet_projective_return_phase() -> float:
    """Endpoint phase of the first projective return theta=pi."""

    start = hamlet_j_orbit(0.0)
    end = hamlet_j_orbit(pi)
    if not (
        isclose(end[0], -start[0], abs_tol=1e-12)
        and isclose(end[1], -start[1], abs_tol=1e-12)
    ):
        raise AssertionError("canonical Hamlet J orbit did not return with phase -1")
    return -1.0


def hamlet_operator_module_coordinates(
    a: float,
    b: float,
    c: float,
    d: float,
) -> tuple[complex, complex]:
    """Coordinates for A=aI+bS+cP+dJ as A=z0+S z1 over C_J."""

    return (complex(float(a), float(d)), complex(float(b), float(c)))


def hamlet_operator_module_norm(coords: tuple[complex, complex]) -> float:
    """Normalized Frobenius norm squared in C_J^2 coordinates."""

    z0, z1 = coords
    return abs(z0) ** 2 + abs(z1) ** 2


def hamlet_operator_balanced_orbit(theta: float) -> tuple[complex, complex]:
    """Canonical balanced left-J orbit in the right C_J-module chart."""

    phase = exp(1j * float(theta))
    inv_phase = exp(-1j * float(theta))
    scale = 1.0 / sqrt(2.0)
    return (scale * phase, scale * inv_phase)


def hamlet_operator_balanced_orbit_derivative(
    theta: float,
) -> tuple[complex, complex]:
    """Derivative of the canonical balanced operator-module orbit."""

    z0, z1 = hamlet_operator_balanced_orbit(theta)
    return (1j * z0, -1j * z1)


def hamlet_operator_horizontal_residual(theta: float) -> complex:
    """Hermitian horizontal residual <Psi,dot(Psi)>."""

    psi = hamlet_operator_balanced_orbit(theta)
    dpsi = hamlet_operator_balanced_orbit_derivative(theta)
    return psi[0].conjugate() * dpsi[0] + psi[1].conjugate() * dpsi[1]


def hamlet_operator_to_real_branch_chart(
    coords: tuple[complex, complex],
) -> tuple[complex, complex]:
    """Fixed unitary chart mapping operator coordinates to the real J-orbit chart."""

    z0, z1 = coords
    scale = 1.0 / sqrt(2.0)
    return (scale * (z0 + z1), scale * 1j * (z0 - z1))


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
            z2_nontrivial_real_character(1) == 1.0,
            z2_nontrivial_real_character(-1) == -1.0,
            z2_nontrivial_real_character(-1) ** 2 == 1.0,
            hamlet_complex_structure(hamlet_complex_structure((2.0, -3.0))) == (-2.0, 3.0),
            isclose(hamlet_horizontal_residual(0.371), 0.0, abs_tol=1e-12),
            isclose(hamlet_projective_return_phase(), -1.0, abs_tol=1e-12),
            isclose(hamlet_operator_module_norm(hamlet_operator_balanced_orbit(0.731)), 1.0, abs_tol=1e-12),
            abs(hamlet_operator_horizontal_residual(0.731)) <= 1e-12,
            all(
                abs(a - b) <= 1e-12
                for a, b in zip(
                    hamlet_operator_to_real_branch_chart(hamlet_operator_balanced_orbit(0.731)),
                    tuple(complex(v) for v in hamlet_j_orbit(0.731)),
                )
            ),
            IMAGINARY_GENERATOR * IMAGINARY_GENERATOR == -1,
            isclose(abs(u1_phase(0.731)), 1.0),
            spin_half_sign_return(),
            spin_half_full_return(),
        )
    )
