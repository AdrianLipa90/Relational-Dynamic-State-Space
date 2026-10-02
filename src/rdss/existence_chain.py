"""Executable existence-chain reference for RDSS/RTOFA.

Canonical naming/provenance:
- foundational law name: First Law of Existence;
- legacy executable claim id: A0;
- descriptive phrases such as "law of reality" are status descriptions, not aliases;
- DISPERSION/STRUCTURE are First-Hamlet persistence outcomes;
- N/S are downstream durable relation roles;
- J=SP, J^2=-I is derived on the durable N/S role basis.

Authoritative claim dependencies live in src/rdss/axioms.py and
docs/CANONICAL_FOUNDATIONAL_CONTRACT.md.
"""

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


class FirstHamletOutcome(str, Enum):
    """First persistence bifurcation of primitive indistinction."""

    DISPERSION = "dispersion"
    STRUCTURE = "structure"


class RelationRole(str, Enum):
    """Persistent orientation roles of one non-self-collapsed relation."""

    NORTH = "N"
    SOUTH = "S"


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
        "POTENTIAL_TO_PRIMITIVE_INDISTINCTION",
        "existence potential P_E before any persistent distinction",
        "primitive indistinction I_0",
        ExistenceChainStatus.DEFINITIONAL,
        "P_E with no established persistent distinction := I_0",
        "I_0 is not nothingness; existence potential is already present.",
    ),
    ExistenceChainStep(
        "INDISTINCTION_TO_FIRST_HAMLET",
        "P_E in primitive indistinction I_0 with a persistence predicate",
        "Boolean persistence partition schema {DISPERSION, STRUCTURE}",
        ExistenceChainStatus.EXACT_IDENTITY,
        "Persist or not Persist",
        "The predicate supplies two exhaustive labels/classes but does not alone prove that both preimages are non-empty.",
    ),
    ExistenceChainStep(
        "CANONICAL_FIRST_HAMLET_NONDEGENERATE",
        "Boolean persistence partition schema",
        "first Hamlet with both DISPERSION and STRUCTURE admissible",
        ExistenceChainStatus.DEFINITIONAL,
        "canonical RDSS first Hamlet := non-degenerate persistence bifurcation",
    ),
    ExistenceChainStep(
        "STRICT_FIRST_HAMLET_NONDEGENERACY_GATE",
        "P_E + I_0",
        "both persistence branches dynamically admissible",
        ExistenceChainStatus.DERIVATION_GATE,
        "derive non-empty Dispersion and Structure preimages from dynamics",
    ),
    ExistenceChainStep(
        "FIRST_HAMLET_META_Z2",
        "non-degenerate first Hamlet {DISPERSION, STRUCTURE}",
        "meta complement action Z2",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "complement^2 = identity",
        "This classifies persistence outcomes only. It is not the durable two-state carrier used by the projective geometry.",
    ),
    ExistenceChainStep(
        "FIRST_HAMLET_META_LN2",
        "two non-empty admissible first-Hamlet classes",
        "meta Hartley information ln(2)",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "H_meta = ln(2)",
        "A valid meta count, but not the canonical downstream structural ln(2).",
    ),
    ExistenceChainStep(
        "DISPERSION_TO_INDISTINCTION",
        "DISPERSION branch",
        "primitive indistinction I_0",
        ExistenceChainStatus.DEFINITIONAL,
        "not Persist -> no stable distinction -> I_0",
        "Dispersion is not absolute nothingness and supplies no persistent projective basis state.",
    ),
    ExistenceChainStep(
        "STRUCTURE_TO_INFORMATION_POINT",
        "STRUCTURE branch",
        "minimal non-trivial information point",
        ExistenceChainStatus.MODEL_THEOREM,
        "Persist + min |Adm|=1 -> minimal information-point realization",
        "Retained carrier result; the durable binary geometry is derived from the persistent relation, not from this point alone.",
    ),
    ExistenceChainStep(
        "STRUCTURE_TO_PERSISTENT_RELATION",
        "STRUCTURE branch with persistent distinction",
        "minimal persistent non-trivial relation R",
        ExistenceChainStatus.MODEL_THEOREM,
        "STRUCTURE + TIR minimum-structure bridge -> ordered relation R:s->t",
        "Imported TIR bridge: minimum non-trivial persistent structure is relation. This is not a fresh RDSS definition.",
    ),
    ExistenceChainStep(
        "RELATION_TO_ORIENTATION_ROLE_DYAD",
        "non-self-collapsed persistent relation R",
        "orientation roles {N,S}",
        ExistenceChainStatus.EXACT_IDENTITY,
        "J_R(s,t;R)=(t,s;R^-1), J_R^2=id",
        "The two durable roles belong to one relation and are distinct from DISPERSION/STRUCTURE.",
    ),
    ExistenceChainStep(
        "RELATION_ROLE_TO_Z2",
        "persistent orientation roles {N,S}",
        "durable orientation Z2",
        ExistenceChainStatus.EXACT_IDENTITY,
        "{id,J_R} ~= Z2",
    ),
    ExistenceChainStep(
        "RELATION_ROLE_TO_LN2",
        "two persistent orientation roles",
        "structural Hartley information ln(2)",
        ExistenceChainStatus.EXACT_IDENTITY,
        "H_role = ln |{N,S}| = ln(2)",
        "This is the canonical structural ln(2) for the durable downstream algebra.",
    ),
    ExistenceChainStep(
        "BARE_POINT_NOT_FIRST_HAMLET",
        "bare singleton non-vacuity witness",
        "no forced internal binary distinction",
        ExistenceChainStatus.MODEL_THEOREM,
        "bare point != first Hamlet",
        "The point supplies minimum object cardinality only.",
    ),
    ExistenceChainStep(
        "Z2_TO_SIGN_CHARACTER",
        "persistent relation-role symmetry Z2",
        "normalized real sign character {-1,+1}",
        ExistenceChainStatus.EXACT_IDENTITY,
        "chi(g)^2=1 and chi nontrivial => chi(g)=-1",
        "No upstream U(1) structure is assumed.",
    ),
    ExistenceChainStep(
        "ORIENTATION_TO_RELATIONAL_ZERO",
        "persistent relation-role signs {-1,+1}",
        "relational centre zeta=0",
        ExistenceChainStatus.EXACT_IDENTITY,
        "zeta=(-1+1)/2=0",
        "Relational zero is represented and therefore is not absolute nothingness.",
    ),
    ExistenceChainStep(
        "ORIENTATION_TO_IMAGINARY_GENERATOR",
        "ordered persistent relation-role span with swap S and polarity P",
        "real complex-structure generator J",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "J=SP, S^2=P^2=I, SP=-PS => J^2=-I",
        "Exact on the durable two-role real span. DISPERSION/STRUCTURE are not used as the vector-space basis.",
    ),
    ExistenceChainStep(
        "RELATION_ROLE_TO_MINIMAL_GAUSSIAN_GENERATOR",
        "durable role cardinality 2 plus J^2=-I",
        "primitive Gaussian generator g=2+J up to conjugation",
        ExistenceChainStatus.MODEL_THEOREM,
        "G_k=2+kJ, k in Z\\{0}; min |k|=1 => 2+/-J",
        "Minimality is inside the explicitly declared integral Gaussian lift class.",
    ),
    ExistenceChainStep(
        "GAUSSIAN_TO_COLLATZ_COEFFICIENTS",
        "g=2+J",
        "coefficient triple (2,1,3)",
        ExistenceChainStatus.EXACT_IDENTITY,
        "Re(g)=2; ImCoeff(g)=1; Re(g^2)=3 because g^2=3+4J",
        "This derives the numerical coefficients independently of the parity-minimal route; it does not yet choose divide/multiply/add semantics.",
    ),
    ExistenceChainStep(
        "GAUSSIAN_TO_L45",
        "g=2+J",
        "Gaussian L-values L4=2 and L5=5",
        ExistenceChainStatus.EXACT_IDENTITY,
        "L4=Re(g)=2; L5=N(g)=g*g_bar=5",
        "Crosswalk to the independently established TIR L4 and L5 values.",
    ),
    ExistenceChainStep(
        "ROOT_EXTENSION_TO_L3",
        "Gaussian L4=2, L5=5 plus TIR tetrahedral root-extension closure",
        "L3=7",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "L3=L4+L5=2+5=7",
        "The addition rule is the existing TIR root-extension closure, not inferred from Bombelli.",
    ),
    ExistenceChainStep(
        "GAUSSIAN_BOMBELLI_CLOSURE",
        "g=2+J",
        "3-4-5, Bombelli radicals, and -7+24J closure",
        ExistenceChainStatus.EXACT_IDENTITY,
        "g^2=3+4J; g^3=2+11J; g^4=-7+24J",
        "The fourth power independently reproduces -L3 and 24; this is a closure check, not the definition of L3 or kappa.",
    ),
    ExistenceChainStep(
        "SOURCE_MINIMAL_PARITY_LAW_TO_COLLATZ",
        "declared source-minimal parity-law signature on the durable dyad",
        "Collatz branch operators E:n->n/2 and O:n->3n+1",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "|{N,S}|=2; min odd a>1 is 3; min positive odd parity repair is 1",
        "Independent coefficient route inside the declared operation class.",
    ),
    ExistenceChainStep(
        "COLLATZ_COEFFICIENT_PROVENANCE_DOUBLE_CLOSED",
        "Gaussian closure + source-minimal parity closure",
        "same coefficient triple (2,1,3)",
        ExistenceChainStatus.EXACT_IDENTITY,
        "(2,1,3)_Gaussian = (2,1,3)_parity",
        "Numerical coefficient provenance is no longer the open Collatz problem.",
    ),
    ExistenceChainStep(
        "ASSOCIATION_AS_DYAD_QUOTIENT",
        "finite carrier with free durable-role Z2 pairing",
        "association cardinality n/2",
        ExistenceChainStatus.EXACT_IDENTITY,
        "|X/Z2|=|X|/2",
        "Complete association is admissible exactly for even finite cardinality.",
    ),
    ExistenceChainStep(
        "DISSOCIATION_AS_THREE_FIBRE",
        "finite carrier X and generated dissociation multiplicity 3",
        "dissociation cardinality 3n",
        ExistenceChainStatus.EXACT_IDENTITY,
        "|X x F3|=3|X|",
    ),
    ExistenceChainStep(
        "REPAIR_AS_SINGLETON_COPRODUCT",
        "dissociated finite carrier",
        "minimal repair cardinality n+1",
        ExistenceChainStatus.EXACT_IDENTITY,
        "|X sqcup {star}|=|X|+1",
    ),
    ExistenceChainStep(
        "PARITY_TO_RELATIONAL_COLLATZ",
        "dyad quotient + three-fibre dissociation + singleton repair",
        "deterministic Collatz cardinality normalization",
        ExistenceChainStatus.EXACT_IDENTITY,
        "even n -> n/2; odd n -> 3n+1",
        "Odd cardinality cannot be completely paired; 3n remains odd and +1 reopens the even association quotient.",
    ),
    ExistenceChainStep(
        "PRIMITIVE_NATURAL_DYNAMICS_BINDING_GATE",
        "exact relational-cardinality Collatz normalization",
        "primitive natural dynamics",
        ExistenceChainStatus.DERIVATION_GATE,
        "establish that the intended natural system instantiates this exact normalization",
        "This is now the only remaining Collatz-level foundational/physical binding gate.",
    ),
    ExistenceChainStep(
        "COLLATZ_BRANCHES_TO_PSL2",
        "admitted Collatz affine branches E and O",
        "PSL(2,R) branch representation",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "M_E~diag(1,2), M_O~[[3,1],[0,1]]; determinant normalization -> SL(2,R)",
        "Exact once the operation semantics select the Collatz branch maps.",
    ),
    ExistenceChainStep(
        "COLLATZ_BRANCHES_TO_LOG_SIGNATURE",
        "admitted Collatz affine branches",
        "signed local scale signatures",
        ExistenceChainStatus.EXACT_IDENTITY,
        "sigma_E=-ln(2), sigma_O=+ln(3)",
        "Association/dissociation scale signatures.",
    ),
    ExistenceChainStep(
        "IMAGINARY_GENERATOR_TO_U1",
        "imaginary generator J",
        "phase orbit U(1)",
        ExistenceChainStatus.EXACT_IDENTITY,
        "u(phi)=exp(phi J), |u|=1",
    ),
    ExistenceChainStep(
        "BINARY_PHASE_TO_CP1",
        "full persistent relation-role operator algebra A_H=M2(R)=C_J direct-sum S C_J",
        "CP1 / Bloch sphere",
        ExistenceChainStatus.STANDARD_GEOMETRY,
        "unit(A_H)=S3; S3/right-U(1) ~= CP1 ~= S2",
        "Canonical route: complex dimension two is the right C_J-module rank of the full S/P operator algebra, avoiding a second independent copy of the binary degree of freedom.",
    ),
    ExistenceChainStep(
        "HAMLET_S3_TO_SU2",
        "unit persistent relation-role operator module S3",
        "SU(2)",
        ExistenceChainStatus.STANDARD_GEOMETRY,
        "(z0,z1) gives the canonical SU(2) matrix",
        "The unit spinor pair parametrizes SU(2) bijectively.",
    ),
    ExistenceChainStep(
        "HAMLET_SU2_QUOTIENT_TO_S2",
        "SU(2) with common right U(1) phase",
        "CP1 / potential sphere S2",
        ExistenceChainStatus.STANDARD_GEOMETRY,
        "SU(2)/U(1) ~= CP1 ~= S2",
        "The projective sphere and the SU(2) homogeneous-space sphere are the same quotient geometry.",
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
        "relation-role J-orbit in the symmetry-fixed CP1 branch geometry",
        "canonical Berry loop realizes holonomy -1",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "psi(theta)=exp(theta J)psi_0, theta:0->pi; psi(pi)=-psi_0",
        "The orbit is horizontal in the reference Hopf connection and the first projective return therefore carries the non-trivial -1 holonomy.",
    ),
    ExistenceChainStep(
        "HAMLET_PAULI_TO_SU2",
        "relation-role swap/polarity/complex structure",
        "standard su(2) defining generators",
        ExistenceChainStatus.CONDITIONAL_EXACT,
        "sigma_x=S, sigma_z=-P, sigma_y=-iJ; T_k=sigma_k/2",
        "The commutators close exactly as [T_i,T_j]=i epsilon_ijk T_k.",
    ),
    ExistenceChainStep(
        "SU2_CASIMIR_TO_HALF",
        "relation-role defining su(2) representation",
        "representation label j=1/2",
        ExistenceChainStatus.CONDITIONAL_STANDARD_RESULT,
        "sum T_k^2=3I/4=j(j+1)I -> j=1/2",
        "This is representation-theoretic half-spin. Identifying it with physical angular momentum is a downstream bridge.",
    ),
    ExistenceChainStep(
        "BERRY_EULER_HAMLET_TO_SPIN_HALF",
        "relation-role su(2) half representation plus Berry/Euler closure",
        "consistent half-spin / 2pi-sign / 4pi-return structure",
        ExistenceChainStatus.CONDITIONAL_STANDARD_RESULT,
        "j=1/2; U(2*pi)=-I; U(4*pi)=I; Hol_Berry=-1",
        "The half label is fixed by the su(2) Casimir; Berry/Euler supplies an independent geometric consistency check.",
    ),
)


def relation_roles() -> tuple[RelationRole, RelationRole]:
    """Persistent orientation-role dyad of one non-self-collapsed relation."""

    return (RelationRole.NORTH, RelationRole.SOUTH)


def relation_role_reverse(role: RelationRole) -> RelationRole:
    """Orientation reversal on the persistent relation-role dyad."""

    return RelationRole.SOUTH if role is RelationRole.NORTH else RelationRole.NORTH


def relation_role_hartley_nats() -> float:
    """Probability-free information of the durable two-role orbit."""

    return hartley_information_nats(len(relation_roles()))


def relation_role_swap_invariant_unit_vector() -> tuple[float, float]:
    """Normalized +1 eigenvector of persistent role reversal."""

    scale = 1.0 / sqrt(2.0)
    return (scale, scale)


def first_hamlet_outcomes() -> tuple[FirstHamletOutcome, FirstHamletOutcome]:
    """Exhaustive first-Hamlet persistence classes."""

    return (FirstHamletOutcome.DISPERSION, FirstHamletOutcome.STRUCTURE)


def first_hamlet_classify(persists: bool) -> FirstHamletOutcome:
    """Classify a candidate differentiation by persistence."""

    return FirstHamletOutcome.STRUCTURE if bool(persists) else FirstHamletOutcome.DISPERSION


def first_hamlet_complement(outcome: FirstHamletOutcome) -> FirstHamletOutcome:
    """Boolean complement on the first Hamlet."""

    return (
        FirstHamletOutcome.STRUCTURE
        if outcome is FirstHamletOutcome.DISPERSION
        else FirstHamletOutcome.DISPERSION
    )


def hartley_information_nats(cardinality: int) -> float:
    """Hartley information ln(N) for a finite non-empty outcome space."""

    if cardinality < 1:
        raise ValueError("cardinality must be positive")
    return log(float(cardinality))


def first_hamlet_hartley_nats() -> float:
    return hartley_information_nats(len(first_hamlet_outcomes()))


def branch_swap(branch: int) -> int:
    """Canonical involution of the primitive binary alphabet {-1,+1}."""

    if branch not in (-1, 1):
        raise ValueError("branch must be -1 or +1")
    return -branch


def branch_word_swap(word: tuple[int, ...]) -> tuple[int, ...]:
    """Extend branch swap letterwise to the finite-word address space."""

    return tuple(branch_swap(branch) for branch in word)


def first_hamlet_swap_invariant_unit_vector() -> tuple[float, float]:
    """Legacy API alias for the durable relation-role swap-invariant vector."""

    return relation_role_swap_invariant_unit_vector()


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
    """Canonical swap-invariant left-J orbit in the right C_J-module chart."""

    phase = exp(1j * float(theta))
    inv_phase = exp(-1j * float(theta))
    left, right = relation_role_swap_invariant_unit_vector()
    return (left * phase, right * inv_phase)


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


def hamlet_spinor_to_su2(
    coords: tuple[complex, complex],
) -> tuple[tuple[complex, complex], tuple[complex, complex]]:
    """Map a normalized spinor pair to its canonical SU(2) matrix."""

    z0, z1 = coords
    norm = abs(z0) ** 2 + abs(z1) ** 2
    if not isclose(norm, 1.0, abs_tol=1e-12):
        raise ValueError("spinor coordinates must have unit norm")
    return (
        (z0, -z1.conjugate()),
        (z1, z0.conjugate()),
    )


def hamlet_bloch_coordinates(
    coords: tuple[complex, complex],
) -> tuple[float, float, float]:
    """Bloch/Hopf map from a normalized Hamlet module spinor to S2."""

    z0, z1 = coords
    norm = abs(z0) ** 2 + abs(z1) ** 2
    if not isclose(norm, 1.0, abs_tol=1e-12):
        raise ValueError("spinor coordinates must have unit norm")
    cross = z0.conjugate() * z1
    return (
        float(2.0 * cross.real),
        float(2.0 * cross.imag),
        float(abs(z0) ** 2 - abs(z1) ** 2),
    )


def _matmul2(
    left: tuple[tuple[complex, complex], tuple[complex, complex]],
    right: tuple[tuple[complex, complex], tuple[complex, complex]],
) -> tuple[tuple[complex, complex], tuple[complex, complex]]:
    return (
        (
            left[0][0] * right[0][0] + left[0][1] * right[1][0],
            left[0][0] * right[0][1] + left[0][1] * right[1][1],
        ),
        (
            left[1][0] * right[0][0] + left[1][1] * right[1][0],
            left[1][0] * right[0][1] + left[1][1] * right[1][1],
        ),
    )


def _matsub2(
    left: tuple[tuple[complex, complex], tuple[complex, complex]],
    right: tuple[tuple[complex, complex], tuple[complex, complex]],
) -> tuple[tuple[complex, complex], tuple[complex, complex]]:
    return tuple(
        tuple(left[i][j] - right[i][j] for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def _matscale2(
    scalar: complex,
    matrix: tuple[tuple[complex, complex], tuple[complex, complex]],
) -> tuple[tuple[complex, complex], tuple[complex, complex]]:
    return tuple(
        tuple(scalar * matrix[i][j] for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def hamlet_pauli_matrices() -> tuple[
    tuple[tuple[complex, complex], tuple[complex, complex]],
    tuple[tuple[complex, complex], tuple[complex, complex]],
    tuple[tuple[complex, complex], tuple[complex, complex]],
]:
    """Pauli triple derived from Hamlet swap S, polarity P and J=SP."""

    sigma_x = ((0j, 1 + 0j), (1 + 0j, 0j))
    j_op = ((0j, 1 + 0j), (-1 + 0j, 0j))
    polarity = ((-1 + 0j, 0j), (0j, 1 + 0j))
    sigma_y = _matscale2(-1j, j_op)
    sigma_z = _matscale2(-1.0, polarity)
    return sigma_x, sigma_y, sigma_z


def hamlet_su2_generators() -> tuple[
    tuple[tuple[complex, complex], tuple[complex, complex]],
    tuple[tuple[complex, complex], tuple[complex, complex]],
    tuple[tuple[complex, complex], tuple[complex, complex]],
]:
    return tuple(_matscale2(0.5, sigma) for sigma in hamlet_pauli_matrices())  # type: ignore[return-value]


def hamlet_su2_commutator_residual() -> float:
    """Maximum residual for [T_i,T_j]=i epsilon_ijk T_k."""

    generators = hamlet_su2_generators()
    triples = (
        (0, 1, 2, 1),
        (1, 2, 0, 1),
        (2, 0, 1, 1),
        (1, 0, 2, -1),
        (2, 1, 0, -1),
        (0, 2, 1, -1),
    )
    residual = 0.0
    for i, j, k, sign in triples:
        comm = _matsub2(
            _matmul2(generators[i], generators[j]),
            _matmul2(generators[j], generators[i]),
        )
        target = _matscale2(1j * sign, generators[k])
        residual = max(
            residual,
            max(
                abs(comm[row][col] - target[row][col])
                for row in range(2)
                for col in range(2)
            ),
        )
    return residual


def hamlet_su2_casimir_value() -> float:
    """Return j(j+1) for the defining Hamlet su(2) representation."""

    generators = hamlet_su2_generators()
    diagonal = 0j
    offdiag = 0.0
    total = ((0j, 0j), (0j, 0j))
    for generator in generators:
        square = _matmul2(generator, generator)
        total = tuple(
            tuple(total[i][j] + square[i][j] for j in range(2))
            for i in range(2)
        )  # type: ignore[assignment]
    diagonal = 0.5 * (total[0][0] + total[1][1])
    offdiag = max(abs(total[0][1]), abs(total[1][0]), abs(total[0][0] - total[1][1]))
    if offdiag > 1e-12 or abs(diagonal.imag) > 1e-12:
        raise AssertionError("Hamlet su(2) Casimir is not scalar")
    return float(diagonal.real)


def hamlet_su2_representation_label() -> float:
    """Non-negative j solving j(j+1)=Casimir."""

    c = hamlet_su2_casimir_value()
    return (-1.0 + sqrt(1.0 + 4.0 * c)) / 2.0


def hamlet_spinor_z_rotation(theta: float) -> tuple[complex, complex]:
    """Diagonal entries of exp(-i theta sigma_z / 2)."""

    half = 0.5 * float(theta)
    return (exp(-1j * half), exp(1j * half))


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
            isclose(first_hamlet_hartley_nats(), LN2),
            relation_role_reverse(relation_role_reverse(RelationRole.NORTH)) is RelationRole.NORTH,
            relation_role_reverse(relation_role_reverse(RelationRole.SOUTH)) is RelationRole.SOUTH,
            isclose(relation_role_hartley_nats(), LN2),
            all(
                isclose(value, 1.0 / sqrt(2.0), abs_tol=1e-12)
                for value in relation_role_swap_invariant_unit_vector()
            ),
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
            isclose(
                abs(hamlet_spinor_to_su2(hamlet_operator_balanced_orbit(0.731))[0][0]) ** 2
                + abs(hamlet_spinor_to_su2(hamlet_operator_balanced_orbit(0.731))[1][0]) ** 2,
                1.0,
                abs_tol=1e-12,
            ),
            isclose(
                hamlet_bloch_coordinates(hamlet_operator_balanced_orbit(0.731))[2],
                0.0,
                abs_tol=1e-12,
            ),
            IMAGINARY_GENERATOR * IMAGINARY_GENERATOR == -1,
            hamlet_su2_commutator_residual() <= 1e-12,
            isclose(hamlet_su2_casimir_value(), 0.75, abs_tol=1e-12),
            isclose(hamlet_su2_representation_label(), 0.5, abs_tol=1e-12),
            all(abs(value + 1.0) <= 1e-12 for value in hamlet_spinor_z_rotation(2.0 * pi)),
            all(abs(value - 1.0) <= 1e-12 for value in hamlet_spinor_z_rotation(4.0 * pi)),
            isclose(abs(u1_phase(0.731)), 1.0),
            spin_half_sign_return(),
            spin_half_full_return(),
        )
    )
