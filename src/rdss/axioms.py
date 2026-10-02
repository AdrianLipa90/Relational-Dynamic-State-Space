from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ClaimKind(str, Enum):
    AXIOM = "axiom"  # legacy compatibility; no canonical RDSS claim uses this kind
    FOUNDATIONAL_LAW = "foundational_law"
    DEFINITION = "definition"
    STRUCTURAL_PRIMITIVE = "structural_primitive"
    REFERENCE_REALIZATION = "reference_realization"
    DERIVED = "derived"
    BRIDGE = "bridge"
    THEOREM = "theorem"
    FORMATION_RULE = "formation_rule"
    DERIVATION_GATE = "derivation_gate"


@dataclass(frozen=True)
class Claim:
    id: str
    kind: ClaimKind
    statement: str
    depends_on: tuple[str, ...] = ()


# Canonical provenance notes are deliberately machine-readable.
# They prevent descriptive prose from silently renaming or retyping the theory.
CANONICAL_PROVENANCE: dict[str, str] = {
    "A0": (
        "Canonical name: First Law of Existence. Legacy claim id: A0. "
        "Do not rename this law from descriptive prose; phrases such as "
        "'law of reality' describe its intended status and are not aliases."
    ),
    "THM_FIRST_HAMLET_DISPERSION_STRUCTURE": (
        "First Hamlet is the persistence dichotomy DISPERSION/STRUCTURE. "
        "These transient logical outcomes are not the downstream durable role carrier N/S."
    ),
    "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT": (
        "Durable binary carrier provenance: STRUCTURE -> TIR minimum-relation bridge -> "
        "orientation-role orbit N/S. N/S may be distinct occurrences/roles on one carrier."
    ),
    "THM_HAMLET_IMAGINARY_GENERATOR": (
        "J=SP and J^2=-I are derived from swap/polarity on the durable N/S role basis; "
        "complex scalars are not an upstream premise."
    ),
    "THM_RELATION_ALGEBRA_DETERMINISTICALLY_GENERATES_COLLATZ_MAP": (
        "Collatz operation provenance: /2 from free Z2 association quotient; "
        "x3 from the three distinguished non-identity basis directions {S,P,J} of "
        "{I,S,P,J}; +1 from restoration of the omitted identity direction I. "
        "The set {S,P,J} is a basis-direction set, not the set of all non-identity operators."
    ),
    "THM_L_CONSTANTS_SINGLE_GENERATOR_CLOSURE": (
        "Gaussian-Bombelli provenance: q=|{N,S}|=2 and J^2=-I give g=q+J=2+J; "
        "L4=2 and L5=N(g)=5, while L3=7 uses the separately identified TIR root-extension bridge."
    ),
}


CLAIMS: tuple[Claim, ...] = (
    # Canonical source: docs/CANONICAL_FOUNDATIONAL_CONTRACT.md §1.
    # The public name is Law of Reality / Prawo Rzeczywistości. "A0" is only
    # the legacy executable identifier and must not be used to rename the law.
    Claim(
        "A0",
        ClaimKind.FOUNDATIONAL_LAW,
        "Law of Reality (Prawo Rzeczywistosci; legacy executable id A0): absolute nothingness is not a realizable state because it has no object, carrier, occurrence, distinction, relation or denotation by which it could be established as a state. Algebraic/relational zero is not absolute nothingness.",
    ),
    # Canonical source: docs/CANONICAL_FOUNDATIONAL_CONTRACT.md §2.
    Claim(
        "DEF_LR_OCCURRENCE_CARRIER_SEPARATION",
        ClaimKind.DEFINITION,
        "In an LR-admissible realization, occurrence identity and carrier identity are distinct sorts. A carrier projection pi maps admitted relational occurrences to carriers, and two distinct occurrences may project to the same singleton carrier.",
        ("A0",),
    ),
    Claim(
        "THM_LR_SINGLETON_CAN_SUPPORT_BINARY_DISTINCTION",
        ClaimKind.THEOREM,
        "A binary relational distinction requires two distinct occurrences, not two distinct primitive carriers: omega_- != omega_+ may satisfy pi(omega_-)=pi(omega_+)=a. Therefore the minimum carrier support may be one while the distinction remains binary at occurrence level.",
        ("DEF_LR_OCCURRENCE_CARRIER_SEPARATION",),
    ),
    Claim(
        "DEF_EXISTENCE_POTENTIAL",
        ClaimKind.DEFINITION,
        "Existence potential P_E is the modal/admissible possibility remaining after absolute nothingness is excluded by the Law of Reality. P_E is not a material object, energy, force, field, spacetime quantity or Berry/gauge connection.",
        ("A0",),
    ),
    Claim(
        "DEF_NONTRIVIAL_INFORMATION_STATE",
        ClaimKind.DEFINITION,
        "A non-trivial finite information state is a state with a finite outcome set containing at least two distinguishable alternatives; a one-outcome state has no internal distinction capacity.",
    ),
    Claim(
        "DEF_PRIMITIVE_INDISTINCTION",
        ClaimKind.DEFINITION,
        "Primitive indistinction I_0 is the existence-potential condition in which no persistent internal distinction has yet been established. I_0 is not absolute nothingness: the modal existence potential P_E is already present.",
        ("DEF_EXISTENCE_POTENTIAL",),
    ),
    Claim(
        "DEF_DISTINCTION_PERSISTENCE_PREDICATE",
        ClaimKind.DEFINITION,
        "For any candidate differentiation of the primitive existence potential, Persist is the Boolean predicate that is true exactly when the differentiation remains a stable distinction under the chosen closure/update criterion and false when no stable distinction remains.",
        ("DEF_PRIMITIVE_INDISTINCTION",),
    ),
    Claim(
        "THM_FIRST_HAMLET_DISPERSION_STRUCTURE",
        ClaimKind.THEOREM,
        "The persistence predicate has Boolean codomain {DISPERSION, STRUCTURE}: every candidate differentiation is classified exhaustively and exclusively as not-Persist or Persist. This theorem establishes the two-class partition schema before any non-trivial point carrier is selected; it does not by itself prove that both preimages are non-empty.",
        ("DEF_DISTINCTION_PERSISTENCE_PREDICATE",),
    ),
    Claim(
        "DEF_CANONICAL_FIRST_HAMLET_NONDEGENERATE",
        ClaimKind.DEFINITION,
        "Canonical RDSS first-Hamlet semantics uses the non-degenerate persistence bifurcation: both DISPERSION and STRUCTURE are admitted possibilities, so both Boolean preimages are non-empty.",
        ("THM_FIRST_HAMLET_DISPERSION_STRUCTURE",),
    ),
    Claim(
        "THM_CANONICAL_FIRST_HAMLET_TWO_BRANCHES",
        ClaimKind.THEOREM,
        "Under canonical non-degenerate first-Hamlet semantics, the actual admissible outcome space has exactly two non-empty elements/classes, DISPERSION and STRUCTURE.",
        ("DEF_CANONICAL_FIRST_HAMLET_NONDEGENERATE",),
    ),
    Claim(
        "GATE_FIRST_HAMLET_NONDEGENERACY_FROM_PE_I0",
        ClaimKind.DERIVATION_GATE,
        "Strict dynamics gate: derive from primitive existence potential plus indistinction, without adopting the canonical non-degeneracy definition, that both DISPERSION and STRUCTURE are dynamically admissible/non-empty possibilities.",
        ("DEF_PRIMITIVE_INDISTINCTION", "DEF_DISTINCTION_PERSISTENCE_PREDICATE"),
    ),
    Claim(
        "THM_RELATIONAL_DEFORMATION_POTENTIAL_IS_DOWNSTREAM",
        ClaimKind.THEOREM,
        "The existing RDSS relational deformation potential cannot serve as an upstream derivation of the first Hamlet: by definition it requires a supplied semantic weighting on an already explicit residual signature. Using it to derive DISPERSION/STRUCTURE would import downstream residual and weighting structure into the primitive persistence bifurcation.",
        ("DEF_RELATIONAL_POTENTIAL", "PRIM_SEMANTIC_WEIGHTING"),
    ),
    Claim(
        "THM_BINARY_CLOSURE_MODEL_IS_DOWNSTREAM",
        ClaimKind.THEOREM,
        "The existing occurrence/closure machinery cannot serve as an upstream derivation of the first Hamlet because its occurrence-address space is already the free-word construction over the binary alphabet B={-1,+1}. It therefore presupposes a binary branch structure rather than deriving one.",
        ("DEF_OCCURRENCE_ADDRESS_SPACE",),
    ),
    Claim(
        "DEF_REFERENCE_DISTINCTION_AMPLITUDE",
        ClaimKind.DEFINITION,
        "Reference dynamics uses a non-negative scalar distinction amplitude d>=0 measuring only the magnitude of persistent differentiation. This amplitude carries no prior +/- branch sign and therefore does not presuppose the first-Hamlet Z2 polarity.",
        ("DEF_PRIMITIVE_INDISTINCTION",),
    ),
    Claim(
        "REF_PRIMITIVE_PERSISTENCE_GRADIENT_FLOW",
        ClaimKind.REFERENCE_REALIZATION,
        "A minimal noncircular persistence envelope is d_dot=d(mu-d)=-dW/dd on d>=0 with W(d;mu)=-mu*d^2/2+d^3/3. Here mu is only an effective signed balance coordinate; it is not treated as a primitive external control.",
        ("DEF_REFERENCE_DISTINCTION_AMPLITUDE",),
    ),
    Claim(
        "THM_REF_PERSISTENCE_FLOW_DISPERSION",
        ClaimKind.THEOREM,
        "For the reference persistence flow with mu<0, d=0 is the unique non-negative equilibrium, its linear rate is mu<0, every positive initial d remains non-negative and converges to zero, and W decreases monotonically. This realizes DISPERSION without assuming a binary sign alphabet.",
        ("REF_PRIMITIVE_PERSISTENCE_GRADIENT_FLOW",),
    ),
    Claim(
        "THM_REF_PERSISTENCE_FLOW_STRUCTURE",
        ClaimKind.THEOREM,
        "For the reference persistence flow with mu>0, d=0 is unstable and d=mu>0 is a stable equilibrium attracting every positive initial d. This realizes STRUCTURE without assuming a binary sign alphabet.",
        ("REF_PRIMITIVE_PERSISTENCE_GRADIENT_FLOW",),
    ),
    Claim(
        "THM_REF_PERSISTENCE_FLOW_REALIZES_BOTH_HAMLET_REGIMES",
        ClaimKind.THEOREM,
        "The single parameterized reference flow realizes both first-Hamlet persistence regimes on the same non-negative amplitude space: mu<0 gives DISPERSION and mu>0 gives STRUCTURE, with mu=0 the critical boundary. This proves algebraic/dynamical consistency of non-degeneracy but not its derivation from P_E alone.",
        ("THM_REF_PERSISTENCE_FLOW_DISPERSION", "THM_REF_PERSISTENCE_FLOW_STRUCTURE", "THM_CANONICAL_FIRST_HAMLET_TWO_BRANCHES"),
    ),
    Claim(
        "DEF_COLLATZ_ASSOCIATION_DISSOCIATION_CYCLE",
        ClaimKind.DEFINITION,
        "Downstream canonical definition after the conditional source-minimal theorem: for a positive odd state n, D:n->3n (dissociation), R:3n->3n+1 (minimal parity repair), followed by maximal association A:(3n+1)->(3n+1)/2^nu2(3n+1). The resulting accelerated odd map is T_C(n)=(3n+1)/2^nu2(3n+1). No global Collatz-convergence claim is assumed.",
        ("THM_SOURCE_MINIMAL_AFFINE_PARITY_DYNAMICS_IS_COLLATZ",),
    ),
    Claim(
        "THM_COLLATZ_ASSOCIATION_BALANCE",
        ClaimKind.THEOREM,
        "For one accelerated odd Collatz cycle, the exact local association-minus-dissociation balance is mu_C(n)=nu2(3n+1)*ln(2)-ln((3n+1)/n)=ln(n/T_C(n)). Positive mu_C means net association/contraction, negative mu_C means net dissociation/expansion, and zero is locally critical.",
        ("DEF_COLLATZ_ASSOCIATION_DISSOCIATION_CYCLE",),
    ),
    Claim(
        "REF_COLLATZ_DERIVED_PERSISTENCE_CONTROL",
        ClaimKind.REFERENCE_REALIZATION,
        "In the primitive persistence envelope, set the effective balance coordinate mu equal to the exact Collatz association balance mu_C(n). Then the sign of the continuous persistence envelope is derived from discrete association/dissociation rather than supplied as a free control parameter.",
        ("THM_COLLATZ_ASSOCIATION_BALANCE", "REF_PRIMITIVE_PERSISTENCE_GRADIENT_FLOW"),
    ),
    Claim(
        "THM_COLLATZ_BALANCE_MATCHES_HAMLET_REGIMES",
        ClaimKind.THEOREM,
        "Under the Collatz-derived persistence realization, mu_C(n)>0 drives the STRUCTURE regime of the reference envelope, mu_C(n)<0 drives DISPERSION, and mu_C(n)=0 is critical. Examples are exact locally: n=3 gives dispersion, n=5 gives structure, and n=1 is critical for the accelerated odd cycle.",
        ("REF_COLLATZ_DERIVED_PERSISTENCE_CONTROL", "THM_REF_PERSISTENCE_FLOW_DISPERSION", "THM_REF_PERSISTENCE_FLOW_STRUCTURE"),
    ),
    Claim(
        "GATE_BIND_PRIMITIVE_INDISTINCTION_TO_COLLATZ_STATE",
        ClaimKind.DERIVATION_GATE,
        "LEGACY/SUPERSEDED target: directly binding primitive indistinction to a Collatz integer skips the persistent-relation layer and is not canonical after the TIR/RDSS causal audit.",
        ("DEF_PRIMITIVE_INDISTINCTION", "THM_FIRST_HAMLET_NOT_PROJECTIVE_BINARY_CARRIER"),
    ),
    Claim(
        "DEF_SOURCE_MINIMAL_PARITY_DYNAMICS_SIGNATURE",
        ClaimKind.FORMATION_RULE,
        "Defined source-minimal arithmetic law signature on positive integers: (i) the primitive association branch removes exactly one factor equal to the cardinality b of the durable relation-role dyad; (ii) the primitive dissociation/repair branch is affine O(n)=a*n+r on odd n, with integer a>1 chosen odd so multiplication preserves odd parity before repair, and positive integer r chosen odd so repair flips parity and reopens association; (iii) no larger unsourced integer coefficient is admitted when a smaller coefficient satisfies the same typed role.",
        ("THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT",),
    ),
    Claim(
        "THM_DYAD_FORCES_ASSOCIATION_DIVISOR_TWO",
        ClaimKind.THEOREM,
        "The durable relation-role orbit has cardinality b=2. Under the source-minimal parity-dynamics signature, one primitive association step therefore divides by b and is uniquely E(n)=n/2 on even n.",
        ("THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT", "DEF_SOURCE_MINIMAL_PARITY_DYNAMICS_SIGNATURE"),
    ),
    Claim(
        "THM_MINIMAL_ODD_DISSOCIATION_MULTIPLIER_THREE",
        ClaimKind.THEOREM,
        "Among positive odd integers strictly greater than one, the least element is 3. Therefore the source-minimal nontrivial multiplicative odd-preserving dissociation coefficient is uniquely a=3.",
        ("DEF_SOURCE_MINIMAL_PARITY_DYNAMICS_SIGNATURE",),
    ),
    Claim(
        "THM_MINIMAL_POSITIVE_ODD_REPAIR_ONE",
        ClaimKind.THEOREM,
        "For odd n and odd multiplier a, a*n is odd. An additive repair changes parity exactly when r is odd; among positive odd integers the least is r=1. Therefore the source-minimal positive parity repair is uniquely +1.",
        ("DEF_SOURCE_MINIMAL_PARITY_DYNAMICS_SIGNATURE", "THM_MINIMAL_ODD_DISSOCIATION_MULTIPLIER_THREE"),
    ),
    Claim(
        "THM_SOURCE_MINIMAL_AFFINE_PARITY_DYNAMICS_IS_COLLATZ",
        ClaimKind.THEOREM,
        "Conditional on DEF_SOURCE_MINIMAL_PARITY_DYNAMICS_SIGNATURE, the unique primitive parity-local branches are E(n)=n/2 for even n and O(n)=3n+1 for odd n. Thus the standard unreduced Collatz map is the exact source-minimal member of this declared law class.",
        ("THM_DYAD_FORCES_ASSOCIATION_DIVISOR_TWO", "THM_MINIMAL_ODD_DISSOCIATION_MULTIPLIER_THREE", "THM_MINIMAL_POSITIVE_ODD_REPAIR_ONE"),
    ),
    Claim(
        "BRIDGE_TIR_CLOSED_PHASE_WINDING_INTEGERS",
        ClaimKind.BRIDGE,
        "TIR General Orbital Algebra proves that every closed U(1) orbit has winding n=(1/2pi) integral dphi in Z, with orientation reversal n->-n. RDSS imports this only after its own U(1) phase circle has been derived.",
        ("THM_IMAGINARY_GENERATOR_U1",),
    ),
    Claim(
        "THM_RELATION_ROLE_GAUSSIAN_INTEGER_LATTICE",
        ClaimKind.THEOREM,
        "The derived complex scalar algebra C_J=span_R{I,J} together with the integer winding subgroup canonically contains the rank-two lattice ZI direct-sum ZJ, isomorphic to the Gaussian integers Z[i]. Thus integral coefficients on I and J need not be inserted as an unrelated arithmetic primitive.",
        ("THM_HAMLET_COMPLEX_SCALAR_ALGEBRA", "BRIDGE_TIR_CLOSED_PHASE_WINDING_INTEGERS"),
    ),
    Claim(
        "DEF_RELATION_ROLE_GAUSSIAN_LIFT_CLASS",
        ClaimKind.DEFINITION,
        "Let q=|{N,S}|=2. Inside the derived Gaussian lattice ZI direct-sum ZJ, the non-real lifts with fixed scalar part q are G_k=qI+kJ for nonzero integer k. Primitive/minimal lift means minimizing |k|.",
        ("THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT", "THM_RELATION_ROLE_GAUSSIAN_INTEGER_LATTICE"),
    ),
    Claim(
        "THM_MINIMAL_RELATION_ROLE_GAUSSIAN_GENERATOR",
        ClaimKind.THEOREM,
        "Within DEF_RELATION_ROLE_GAUSSIAN_LIFT_CLASS, the minimal non-real integral lifts are uniquely G_+=2I+J and G_-=2I-J, exchanged by conjugation/orientation reversal. Up to conjugation the canonical primitive generator is g=2+J.",
        ("DEF_RELATION_ROLE_GAUSSIAN_LIFT_CLASS",),
    ),
    Claim(
        "THM_GAUSSIAN_GENERATES_COLLATZ_COEFFICIENTS",
        ClaimKind.THEOREM,
        "For g=2+J, Re(g)=2, the primitive imaginary coefficient is 1, and g^2=3+4J so Re(g^2)=3. Thus the numerical coefficient triple (association divisor, repair unit, dissociation multiplier)=(2,1,3) is generated algebraically by the same durable dyad and complex structure.",
        ("THM_MINIMAL_RELATION_ROLE_GAUSSIAN_GENERATOR",),
    ),
    Claim(
        "THM_GAUSSIAN_BOMBELLI_LADDER",
        ClaimKind.THEOREM,
        "The exact powers of g=2+J are g^2=3+4J, g^3=2+11J, and g^4=-7+24J. With conjugate g_bar=2-J, the Cardano-Bombelli relations g*g_bar=5, g^3+g_bar^3=4 and x=g+g_bar=4 reproduce x^3-15x-4=0 exactly.",
        ("THM_MINIMAL_RELATION_ROLE_GAUSSIAN_GENERATOR",),
    ),
    Claim(
        "THM_GAUSSIAN_L45_SOURCE",
        ClaimKind.THEOREM,
        "The primitive Gaussian generator recovers the two TIR L-constant values L4=Re(g)=2 and L5=N(g)=g*g_bar=5 without using Collatz depth or twin-prime assignments.",
        ("THM_MINIMAL_RELATION_ROLE_GAUSSIAN_GENERATOR",),
    ),
    Claim(
        "BRIDGE_TIR_ROOT_EXTENSION_L3_FROM_GAUSSIAN_L45",
        ClaimKind.BRIDGE,
        "Using the independently established TIR tetrahedral root-extension closure rule L3=L4+L5, the Gaussian source values L4=2 and L5=5 imply L3=7. Hence the TIR structural triple (L3,L4,L5)=(7,2,5) has a Gaussian/Bombelli provenance independent of the historical Collatz/twin-prime route.",
        ("THM_GAUSSIAN_L45_SOURCE",),
    ),
    Claim(
        "THM_GAUSSIAN_L3_24_CLOSURE_CROSSCHECK",
        ClaimKind.THEOREM,
        "The next dyadic square gives g^4=-7+24J, so |Re(g^4)|=7 reproduces L3 while Im(g^4)=24 supplies an independent integer closure occurrence. This is a crosscheck, not the definition of L3 and not by itself a derivation of kappa.",
        ("THM_GAUSSIAN_BOMBELLI_LADDER", "BRIDGE_TIR_ROOT_EXTENSION_L3_FROM_GAUSSIAN_L45"),
    ),
    Claim(
        "THM_COLLATZ_COEFFICIENT_PROVENANCE_DOUBLE_CLOSED",
        ClaimKind.THEOREM,
        "The Collatz coefficient values 2,3,+1 are obtained independently from the source-minimal parity-law route and from the minimal Gaussian relation-role generator. Their agreement closes numerical coefficient provenance inside the declared law class; it does not by itself prove that primitive dynamics must use division/multiplication/additive-repair semantics.",
        ("THM_SOURCE_MINIMAL_AFFINE_PARITY_DYNAMICS_IS_COLLATZ", "THM_GAUSSIAN_GENERATES_COLLATZ_COEFFICIENTS"),
    ),
    Claim(
        "THM_RELATION_OPERATOR_DIMENSION_COEFFICIENT_ROUTE",
        ClaimKind.THEOREM,
        "The persistent relation-role carrier has q=2 roles and its full real operator algebra is M_2(R) of dimension q^2=4. Removing the one-dimensional identity line leaves q^2-1=3 non-identity operator directions. Therefore the same durable relation algebra independently supplies association divisor 2 and dissociation multiplicity 3.",
        ("THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT", "THM_HAMLET_FULL_OPERATOR_ALGEBRA_M2R"),
    ),
    Claim(
        "THM_BINARY_UNIVERSAL_REPAIR_ONE",
        ClaimKind.THEOREM,
        "For q roles and multiplier m=q^2-1, modulo q one has m congruent to -1. A residue-independent repair that maps every nonzero residue class into the divisible class can exist only when q=2, which has one nonzero residue class. The minimal positive repair is then uniquely r=1.",
        ("THM_RELATION_OPERATOR_DIMENSION_COEFFICIENT_ROUTE",),
    ),
    Claim(
        "THM_COLLATZ_COEFFICIENT_PROVENANCE_TRIPLE_CLOSED",
        ClaimKind.THEOREM,
        "The coefficient triple (2,3,1) is recovered independently by source-minimal parity arithmetic, the primitive Gaussian/Bombelli generator g=2+J, and the persistent relation-role operator dimension plus universal binary repair.",
        ("THM_COLLATZ_COEFFICIENT_PROVENANCE_DOUBLE_CLOSED", "THM_RELATION_OPERATOR_DIMENSION_COEFFICIENT_ROUTE", "THM_BINARY_UNIVERSAL_REPAIR_ONE"),
    ),
    Claim(
        "THM_L_CONSTANTS_SINGLE_GENERATOR_CLOSURE",
        ClaimKind.THEOREM,
        "Let q=2 be the durable relation-role cardinality and g=q+J=2+J the primitive Gaussian generator. Then L4=q=2, L5=N(g)=q^2+1=5, and under the independently established TIR root-extension closure L3=L4+L5=q^2+q+1=7. The same generator gives Re(g^2)=3, g^4=-7+24J and the Bombelli cubic certificate, while the relational Collatz route independently reproduces the same triple.",
        ("THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT", "THM_MINIMAL_RELATION_ROLE_GAUSSIAN_GENERATOR", "THM_GAUSSIAN_L45_SOURCE", "BRIDGE_TIR_ROOT_EXTENSION_L3_FROM_GAUSSIAN_L45"),
    ),
    Claim(
        "DEF_MINIMAL_NONTRIVIAL_DISSOCIATION_SEED",
        ClaimKind.DEFINITION,
        "Define the source-minimal dissociation seed as the least positive finite cardinality n>1 for which the complete free durable-role Z2 association quotient is unavailable.",
        ("THM_ASSOCIATION_QUOTIENT_CARDINALITY",),
    ),
    Claim(
        "THM_MINIMAL_NONTRIVIAL_DISSOCIATION_SEED_IS_THREE",
        ClaimKind.THEOREM,
        "For the durable dyad q=2, complete association exists exactly at even cardinality. After excluding the unit n=1, n=2 associates immediately while n=3 is the least cardinality that cannot. Therefore the source-minimal dissociation seed is uniquely n_0=3.",
        ("DEF_MINIMAL_NONTRIVIAL_DISSOCIATION_SEED", "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT"),
    ),
    Claim(
        "DEF_ACTIVE_SEED_AS_NONIDENTITY_OPERATOR_COUNT",
        ClaimKind.DEFINITION,
        "The active operator sector is the canonical real operator basis with the identity direction removed. Since the full basis is {I,S,P,J}, the active sector is {S,P,J}; its cardinality defines the active arithmetic seed n_0. No independent numerical seed is selected.",
        ("THM_RELATION_OPERATOR_DIMENSION_COEFFICIENT_ROUTE",),
    ),
    Claim(
        "THM_ACTIVE_SEED_IS_THREE",
        ClaimKind.THEOREM,
        "Under the active-seed rule, dim_R(M_2(R))=4 with one identity direction, so n_0=4-1=3.",
        ("DEF_ACTIVE_SEED_AS_NONIDENTITY_OPERATOR_COUNT",),
    ),
    Claim(
        "THM_ACTIVE_SEED_PROVENANCE_DOUBLE_CLOSED",
        ClaimKind.THEOREM,
        "The arithmetic seed n_0=3 is obtained independently as the least non-unit cardinality that cannot immediately associate and as the cardinality of the non-identity operator sector {S,P,J}. The two routes agree exactly.",
        ("THM_MINIMAL_NONTRIVIAL_DISSOCIATION_SEED_IS_THREE", "THM_ACTIVE_SEED_IS_THREE"),
    ),
    Claim(
        "THM_RELATIONAL_COLLATZ_L_CONSTANT_CERTIFICATE",
        ClaimKind.THEOREM,
        "For the derived Collatz map and active seed n_0=3, define L4 as the durable role count 2, L5 as the first completed dissociation-repair-association successor 3->10->5, and L3 as the exact finite depth of the same seed from 3 to 1, namely 7. Thus the relational Collatz core derives (L3,L4,L5)=(7,2,5) directly. The Gaussian/root-extension route is an independent crosscheck rather than a premise of these values.",
        ("THM_ACTIVE_SEED_PROVENANCE_DOUBLE_CLOSED", "THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ"),
    ),
    Claim(
        "THM_L_CONSTANT_PROVENANCE_CROSSCHECK",
        ClaimKind.THEOREM,
        "The relational Collatz derivation (depth, role count, first completed odd cycle) and the independent Gaussian/root-extension derivation produce the identical triple (L3,L4,L5)=(7,2,5).",
        ("THM_RELATIONAL_COLLATZ_L_CONSTANT_CERTIFICATE", "BRIDGE_TIR_ROOT_EXTENSION_L3_FROM_GAUSSIAN_L45"),
    ),
    Claim(
        "DEF_ASSOCIATION_AS_FREE_DYAD_QUOTIENT",
        ClaimKind.DEFINITION,
        "Cardinality semantics for association: a finite carrier equipped with a fixed-point-free action of the durable relation-role Z2 is reduced to its orbit quotient. Every orbit has size two, so association identifies each durable role pair into one quotient element.",
        ("THM_RELATION_ORIENTATION_Z2",),
    ),
    Claim(
        "THM_ASSOCIATION_QUOTIENT_CARDINALITY",
        ClaimKind.THEOREM,
        "For a finite free Z2 action, the carrier decomposes into two-element orbits. Therefore the quotient has cardinality n/2 and exists as a complete pairing only for even n.",
        ("DEF_ASSOCIATION_AS_FREE_DYAD_QUOTIENT",),
    ),
    Claim(
        "DEF_DISSOCIATION_AS_THREE_FIBRE_EXTENSION",
        ClaimKind.DEFINITION,
        "Cardinality semantics for dissociation: each admitted element is independently resolved into a three-element labelled fibre F3 whose multiplicity is the independently generated dissociation coefficient 3. The resulting carrier is X times F3.",
        ("THM_COLLATZ_COEFFICIENT_PROVENANCE_TRIPLE_CLOSED",),
    ),
    Claim(
        "THM_DISSOCIATION_FIBRE_CARDINALITY",
        ClaimKind.THEOREM,
        "For finite X and a three-element fibre F3, |X times F3|=3|X|. Thus three-fold dissociation acts on cardinality as n->3n.",
        ("DEF_DISSOCIATION_AS_THREE_FIBRE_EXTENSION",),
    ),
    Claim(
        "DEF_REPAIR_AS_SINGLETON_COPRODUCT",
        ClaimKind.DEFINITION,
        "Cardinality semantics for repair: adjoin one new distinguishable unit by disjoint union with a singleton. This is the minimal positive repair generated by the same coefficient source.",
        ("THM_COLLATZ_COEFFICIENT_PROVENANCE_TRIPLE_CLOSED",),
    ),
    Claim(
        "THM_SINGLETON_REPAIR_CARDINALITY",
        ClaimKind.THEOREM,
        "For finite X, the disjoint union X sqcup {star} has cardinality |X|+1. Thus minimal repair acts as n->n+1.",
        ("DEF_REPAIR_AS_SINGLETON_COPRODUCT",),
    ),
    Claim(
        "DEF_DISSOCIATION_AS_ACTIVE_OPERATOR_PRODUCT",
        ClaimKind.DEFINITION,
        "Canonical dissociation semantics: resolve each carrier element against the three distinguished non-identity basis directions A_*={S,P,J} of the durable two-role operator basis {I,S,P,J}. Thus dissociation is the finite product X times A_*, not a claim about the cardinality of all non-identity operators in M_2(R).",
        ("THM_HAMLET_FULL_OPERATOR_ALGEBRA_M2R", "DEF_ACTIVE_SEED_AS_NONIDENTITY_OPERATOR_COUNT"),
    ),
    Claim(
        "THM_ACTIVE_OPERATOR_PRODUCT_CARDINALITY",
        ClaimKind.THEOREM,
        "The active basis-direction set A_*={S,P,J} has cardinality three, hence |X times A_*|=3|X|. Therefore canonical dissociation is n->3n.",
        ("DEF_DISSOCIATION_AS_ACTIVE_OPERATOR_PRODUCT", "THM_ACTIVE_SEED_IS_THREE"),
    ),
    Claim(
        "DEF_REPAIR_AS_IDENTITY_RESTORATION",
        ClaimKind.DEFINITION,
        "Canonical repair semantics: after active-sector dissociation, restore the unique operator direction omitted from A_*, namely the identity I. This is disjoint union with the one-element identity sector {I}.",
        ("DEF_DISSOCIATION_AS_ACTIVE_OPERATOR_PRODUCT", "THM_HAMLET_FULL_OPERATOR_ALGEBRA_M2R"),
    ),
    Claim(
        "THM_IDENTITY_REPAIR_CARDINALITY",
        ClaimKind.THEOREM,
        "The omitted identity sector has cardinality one, so restoring it changes cardinality n->n+1. The repair unit is therefore the unique missing identity direction, not an anonymous singleton.",
        ("DEF_REPAIR_AS_IDENTITY_RESTORATION",),
    ),
    Claim(
        "THM_PARITY_FORCES_COLLATZ_BRANCH_SELECTION",
        ClaimKind.THEOREM,
        "A complete free two-role pairing requires even cardinality. Hence even n admits immediate association n->n/2. For odd n, three-fold dissociation preserves oddness, and singleton repair gives 3n+1 which is even and therefore reopens association. The parity branch is thus fixed by admissibility of the free dyad quotient.",
        ("THM_ASSOCIATION_QUOTIENT_CARDINALITY", "THM_ACTIVE_OPERATOR_PRODUCT_CARDINALITY", "THM_IDENTITY_REPAIR_CARDINALITY"),
    ),
    Claim(
        "THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ",
        ClaimKind.THEOREM,
        "Under the quotient/product/coproduct semantics, the deterministic cardinality update is C(n)=n/2 for even n and C(n)=3n+1 for odd n. This is exactly the standard unreduced Collatz map, now derived as a finite relational-cardinality normalization.",
        ("THM_PARITY_FORCES_COLLATZ_BRANCH_SELECTION",),
    ),
    Claim(
        "THM_RELATION_ALGEBRA_DETERMINISTICALLY_GENERATES_COLLATZ_MAP",
        ClaimKind.THEOREM,
        "The durable relation-role algebra fixes all three canonical cardinality operations: free Z2 quotient gives /2, product with the three distinguished non-identity basis directions {S,P,J} gives x3, and restoration of the unique omitted identity direction {I} gives +1. Parity admissibility then selects the unique deterministic update n/2 for even n and 3n+1 for odd n.",
        ("THM_ASSOCIATION_QUOTIENT_CARDINALITY", "THM_ACTIVE_OPERATOR_PRODUCT_CARDINALITY", "THM_IDENTITY_REPAIR_CARDINALITY", "THM_PARITY_FORCES_COLLATZ_BRANCH_SELECTION"),
    ),
    Claim(
        "GATE_BIND_RELATIONAL_CARDINALITY_NORMALIZATION_TO_PRIMITIVE_NATURAL_DYNAMICS",
        ClaimKind.DERIVATION_GATE,
        "Remaining foundational/physical bridge: establish that the primitive dynamics of the intended natural system is instantiated by this finite relational-cardinality normalization rather than merely admitting it as an exact algebraic realization.",
        ("THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ", "A0"),
    ),
    Claim(
        "GATE_SOURCE_MINIMALITY_APPLIES_TO_PRIMITIVE_DYNAMICS",
        ClaimKind.DERIVATION_GATE,
        "Legacy/refined inheritance gate: quotient/product/coproduct cardinality semantics now close the divide/multiply/add operation assignment algebraically. The unresolved stronger question is only whether primitive natural dynamics is forced to instantiate that exact relational-cardinality normalization.",
        ("A0", "THM_STRUCTURE_BRANCH_MINIMAL_RELATION", "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT", "DEF_SOURCE_MINIMAL_PARITY_DYNAMICS_SIGNATURE"),
    ),
    Claim(
        "GATE_DERIVE_COLLATZ_BRANCHES_FROM_RELATION_ALGEBRA",
        ClaimKind.DERIVATION_GATE,
        "Refined deterministic gate: numerical coefficients and finite-cardinality operation semantics are now algebraically closed. The remaining burden is the physical/foundational binding asserting that primitive natural dynamics instantiates this relational-cardinality normalization.",
        ("THM_RELATION_ALGEBRA_DETERMINISTICALLY_GENERATES_COLLATZ_MAP", "GATE_BIND_RELATIONAL_CARDINALITY_NORMALIZATION_TO_PRIMITIVE_NATURAL_DYNAMICS"),
    ),
    Claim(
        "REF_COLLATZ_BRANCH_MOBIUS_PSL2_LIFT",
        ClaimKind.REFERENCE_REALIZATION,
        "Once the Collatz branches are admitted, E(x)=x/2 and O(x)=3x+1 have projective matrices diag(1,2) and [[3,1],[0,1]]. Determinant-one normalization places both in SL(2,R), hence their projective actions lie in PSL(2,R). This is downstream of the open branch-derivation gate.",
        ("DEF_COLLATZ_ASSOCIATION_DISSOCIATION_CYCLE", "THM_SOURCE_MINIMAL_AFFINE_PARITY_DYNAMICS_IS_COLLATZ"),
    ),
    Claim(
        "THM_COLLATZ_BRANCH_SIGNED_LOG_JACOBIANS",
        ClaimKind.THEOREM,
        "For the admitted affine Collatz branch maps, the exact signed log-Jacobians are sigma_E=-ln(2) for E(x)=x/2 and sigma_O=+ln(3) for O(x)=3x+1. These are local association/dissociation scale signatures and do not derive the branch maps themselves.",
        ("DEF_COLLATZ_ASSOCIATION_DISSOCIATION_CYCLE",),
    ),
    Claim(
        "DEF_COLLATZ_PARITY_ITINERARY",
        ClaimKind.DEFINITION,
        "For the derived unreduced Collatz map C, define the parity itinerary b_k(n)=C^k(n) mod 2. This is downstream of the relational-cardinality normalization and introduces no new branch law.",
        ("THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ",),
    ),
    Claim(
        "THM_COLLATZ_PARITY_FORBIDS_11",
        ClaimKind.THEOREM,
        "If a Collatz state is odd then C(n)=3n+1 is even. Therefore every parity itinerary obeys b_k=1 => b_{k+1}=0, so the word 11 is forbidden exactly.",
        ("DEF_COLLATZ_PARITY_ITINERARY",),
    ),
    Claim(
        "DEF_COLLATZ_DYADIC_NORMALIZED_PHASE",
        ClaimKind.DEFINITION,
        "A finite parity word b_0...b_{m-1} is encoded as the normalized dyadic turn q_m=sum_{k=0}^{m-1} b_k/2^{k+1} in Q/Z. This phase coordinate is symbolic/projective and uses no numerical pi.",
        ("DEF_COLLATZ_PARITY_ITINERARY",),
    ),
    Claim(
        "THM_COLLATZ_DYADIC_SHIFT_IS_DOUBLING",
        ClaimKind.THEOREM,
        "Dropping the first parity bit of the dyadic normalized phase is exactly the map q->2q mod 1. Hence the Collatz itinerary carries the degree-two normalized phase dynamics q(Cn)=2q(n) mod 1 on finite prefixes and on any admitted terminal-reaching limit code.",
        ("DEF_COLLATZ_DYADIC_NORMALIZED_PHASE",),
    ),
    Claim(
        "THM_COLLATZ_TERMINAL_CYCLE_LENGTH_THREE",
        ClaimKind.THEOREM,
        "The derived Collatz map has the exact nontrivial terminal cycle 4->2->1->4, of length three.",
        ("THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ",),
    ),
    Claim(
        "THM_COLLATZ_TERMINAL_PHASE_DENOMINATOR_SEVEN",
        ClaimKind.THEOREM,
        "For phase doubling q->2q mod 1 around the terminal 3-cycle, closure requires q=2^3 q mod 1, hence 7q is integral. The minimal positive nonzero normalized phase therefore has denominator 2^3-1=7.",
        ("THM_COLLATZ_DYADIC_SHIFT_IS_DOUBLING", "THM_COLLATZ_TERMINAL_CYCLE_LENGTH_THREE"),
    ),
    Claim(
        "THM_COLLATZ_TERMINAL_PHASE_ANCHORS",
        ClaimKind.THEOREM,
        "Choosing the minimal positive orientation on the terminal cycle gives q(4)=1/7, and exact doubling then gives q(2)=2/7 and q(1)=4/7. The conjugate orientation gives the complementary 3-cycle; no numerical fit is used.",
        ("THM_COLLATZ_TERMINAL_PHASE_DENOMINATOR_SEVEN",),
    ),
    Claim(
        "THM_COLLATZ_PHASE_DENOMINATOR_EQUALS_L3",
        ClaimKind.THEOREM,
        "The terminal phase denominator forced by the Collatz 3-cycle is 7, exactly equal to the independently relationally-derived L3 from the active seed depth. Thus L3 is closed simultaneously by orbit depth and dyadic phase periodicity.",
        ("THM_COLLATZ_TERMINAL_PHASE_DENOMINATOR_SEVEN", "THM_RELATIONAL_COLLATZ_L_CONSTANT_CERTIFICATE"),
    ),
    Claim(
        "THM_COLLATZ_ADMISSIBLE_WORD_COUNT_FIBONACCI",
        ClaimKind.THEOREM,
        "Binary parity words of length k with forbidden substring 11 obey the recurrence A_k=A_{k-1}+A_{k-2}, with A_0=1 and A_1=2, hence A_k=F_{k+2}.",
        ("THM_COLLATZ_PARITY_FORBIDS_11",),
    ),
    Claim(
        "BRIDGE_COLLATZ_NORMALIZED_PHASE_TO_U1",
        ClaimKind.BRIDGE,
        "The normalized turn q is embedded in the already-derived phase circle by zeta=exp(2*pi*i*q). Under this embedding q->2q mod 1 becomes zeta->zeta^2. The bridge is downstream of both the Collatz itinerary and the independently-derived U(1) carrier; neither is used to derive the other.",
        ("THM_COLLATZ_DYADIC_SHIFT_IS_DOUBLING", "THM_IMAGINARY_GENERATOR_U1"),
    ),
    Claim(
        "THM_FIRST_HAMLET_Z2",
        ClaimKind.THEOREM,
        "Complementation of the Boolean persistence predicate exchanges DISPERSION and STRUCTURE and squares to the identity. The two first-Hamlet classes therefore carry the canonical Z2 complement action.",
        ("THM_CANONICAL_FIRST_HAMLET_TWO_BRANCHES",),
    ),
    Claim(
        "THM_FIRST_HAMLET_HARTLEY_LN2",
        ClaimKind.THEOREM,
        "The first Hamlet has exactly two exhaustive outcome classes, so Hartley information in nats is H_0=ln|Omega_H|=ln(2). No probability assignment is required.",
        ("THM_CANONICAL_FIRST_HAMLET_TWO_BRANCHES",),
    ),
    Claim(
        "THM_DISPERSION_RETURNS_INDISTINCTION",
        ClaimKind.THEOREM,
        "By the definition of DISPERSION, no stable distinction remains; the resulting state is therefore again primitive indistinction I_0 within existence potential, not absolute nothingness.",
        ("DEF_PRIMITIVE_INDISTINCTION", "THM_CANONICAL_FIRST_HAMLET_TWO_BRANCHES"),
    ),
    Claim(
        "DEF_NONTRIVIAL_INFORMATION_POINT",
        ClaimKind.DEFINITION,
        "A non-trivial information point is a minimal one-carrier realization together with a persistent distinction state. It is typed separately from the bare singleton point used only as a non-vacuity witness.",
        ("DEF_POINT", "DEF_NONTRIVIAL_INFORMATION_STATE"),
    ),
    Claim(
        "THM_STRUCTURE_BRANCH_MINIMAL_INFORMATION_POINT",
        ClaimKind.THEOREM,
        "On the STRUCTURE branch, a persistent distinction exists. Combining that persistent distinction with the exact one-carrier minimum yields the minimal non-trivial information-point realization. Thus the non-trivial point is downstream of the first Hamlet, not its prerequisite.",
        ("THM_CANONICAL_FIRST_HAMLET_TWO_BRANCHES", "THM_META0_MINIMAL_CARRIER_CARDINALITY", "DEF_NONTRIVIAL_INFORMATION_POINT"),
    ),
    Claim(
        "BRIDGE_TIR_MIN_NONTRIVIAL_STRUCTURE_IS_RELATION",
        ClaimKind.BRIDGE,
        "TIR First Distinction / Canonical Derivation Spine proves the source-clean typing min(object)=point and min(nontrivial structure)=relation, with relation endpoints treated as roles rather than independent primitive substances. The imported minimum-structure theorem is sourced directly from A0 and does not inherit the separate RDSS bare-singleton non-vacuity witness.",
        ("A0",),
    ),
    Claim(
        "DEF_STRUCTURE_AS_PERSISTENT_RELATION",
        ClaimKind.DEFINITION,
        "Legacy/local alias for the bridged TIR result: a persistent non-trivial distinction is represented by an admitted relation R with ordered source and target roles.",
        ("BRIDGE_TIR_MIN_NONTRIVIAL_STRUCTURE_IS_RELATION", "DEF_BINARY_REL"),
    ),
    Claim(
        "THM_STRUCTURE_BRANCH_MINIMAL_RELATION",
        ClaimKind.THEOREM,
        "The STRUCTURE branch supplies a persistent distinction; the TIR minimum-structure theorem fixes the minimal non-trivial structural realization as a relation R. Thus the first persistent relational object is downstream of the first Hamlet without making relational minimality a fresh RDSS definition.",
        ("THM_CANONICAL_FIRST_HAMLET_TWO_BRANCHES", "BRIDGE_TIR_MIN_NONTRIVIAL_STRUCTURE_IS_RELATION"),
    ),
    Claim(
        "DEF_RELATION_ORIENTATION_REVERSAL",
        ClaimKind.DEFINITION,
        "For a non-self-collapsed persistent relation R:s->t, orientation reversal J_R sends (s,t;R) to (t,s;R^{-1}) and satisfies J_R^2=id.",
        ("THM_STRUCTURE_BRANCH_MINIMAL_RELATION", "DEF_BINARY_REL"),
    ),
    Claim(
        "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT",
        ClaimKind.THEOREM,
        "For a non-self-collapsed persistent relation, orientation reversal has exactly two structural roles N=[s->t] and S=[t->s]. These are the persistent binary roles used by the downstream algebra; they are not the earlier DISPERSION/STRUCTURE persistence outcomes.",
        ("DEF_RELATION_ORIENTATION_REVERSAL",),
    ),
    Claim(
        "THM_RELATION_ORIENTATION_Z2",
        ClaimKind.THEOREM,
        "The identity and orientation reversal on the persistent two-role orbit form Z2. This is the canonical durable binary symmetry for the downstream sign, complex-structure and projective geometry chain.",
        ("THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT",),
    ),
    Claim(
        "THM_RELATION_ROLE_HARTLEY_LN2",
        ClaimKind.THEOREM,
        "The persistent orientation-role orbit has exactly two elements, hence its Hartley information in nats is ln(2). This structural ln(2) is exact once the non-self-collapsed relation exists and does not require a probability measure.",
        ("THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT",),
    ),
    Claim(
        "THM_FIRST_HAMLET_NOT_PROJECTIVE_BINARY_CARRIER",
        ClaimKind.THEOREM,
        "The DISPERSION/STRUCTURE first Hamlet is a persistence classification, not the canonical internal two-state carrier of the projective geometry: DISPERSION leaves no persistent distinction. Therefore the downstream linear, complex, U(1), CP1, Berry and spin constructions must use the persistent relation-role orbit {N,S}, not {DISPERSION,STRUCTURE}.",
        ("THM_FIRST_HAMLET_DISPERSION_STRUCTURE", "THM_DISPERSION_RETURNS_INDISTINCTION", "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT"),
    ),
    Claim(
        "DEF_RDSS_REALIZED_EXISTENCE_INFORMATION_STATE",
        ClaimKind.DEFINITION,
        "Canonical RDSS semantics: the STRUCTURE branch of the first Hamlet is the realized non-trivial information state because it contains a persistent distinction; the DISPERSION branch returns to primitive indistinction I_0.",
        ("THM_CANONICAL_FIRST_HAMLET_TWO_BRANCHES", "DEF_NONTRIVIAL_INFORMATION_STATE"),
    ),
    Claim(
        "THM_CANONICAL_REALIZED_EXISTENCE_BINARY",
        ClaimKind.THEOREM,
        "The first-Hamlet outcome space is exactly {DISPERSION, STRUCTURE}; its complement action is Z2. The STRUCTURE branch supplies the minimal realized non-trivial information state while the two-class Hamlet remains the primitive binary state space.",
        ("DEF_RDSS_REALIZED_EXISTENCE_INFORMATION_STATE", "THM_FIRST_HAMLET_Z2", "THM_STRUCTURE_BRANCH_MINIMAL_INFORMATION_POINT"),
    ),
    Claim(
        "GATE_EXISTENCE_POTENTIAL_INFORMATIONALITY",
        ClaimKind.DERIVATION_GATE,
        "Legacy strict-dynamics gate: establish from a physical/dynamical law that primitive existence potential in indistinction actually undergoes a candidate differentiation process. The formal DISPERSION/STRUCTURE partition itself is already exact once persistence is defined; this gate concerns dynamical instantiation, not the algebraic dichotomy.",
        ("DEF_PRIMITIVE_INDISTINCTION", "DEF_DISTINCTION_PERSISTENCE_PREDICATE"),
    ),
    Claim(
        "THM_MINIMAL_INFORMATION_STATE_BINARY",
        ClaimKind.THEOREM,
        "Every non-trivial finite information state has at least two distinguishable alternatives, and the lower bound is attained by a two-element outcome set.",
        ("DEF_NONTRIVIAL_INFORMATION_STATE",),
    ),
    Claim(
        "THM_TWO_STATE_AUTOMORPHISM_Z2",
        ClaimKind.THEOREM,
        "The automorphism group of an unlabelled two-element outcome set consists of identity and swap, hence is S2 congruent to Z2.",
        ("THM_MINIMAL_INFORMATION_STATE_BINARY",),
    ),
    Claim(
        "THM_Z2_UNIQUE_NONTRIVIAL_REAL_CHARACTER",
        ClaimKind.THEOREM,
        "Let g be the non-trivial element of Z2. Any one-dimensional real character satisfies chi(g)^2=1. The non-trivial character cannot send g to +1, therefore uniquely chi(g)=-1 in R^x. No complex phase structure is used in this step.",
        ("THM_RELATION_ORIENTATION_Z2",),
    ),
    Claim(
        "GATE_EXISTENCE_POTENTIAL_HAMLET_BINARY",
        ClaimKind.DERIVATION_GATE,
        "Legacy strict-dynamics gate: physically instantiate the already-defined first Hamlet DISPERSION/STRUCTURE bifurcation from primitive existence potential. The canonical algebraic Hamlet is THM_FIRST_HAMLET_DISPERSION_STRUCTURE plus THM_FIRST_HAMLET_Z2 and does not require this gate.",
        ("GATE_EXISTENCE_POTENTIAL_INFORMATIONALITY", "GATE_FIRST_HAMLET_NONDEGENERACY_FROM_PE_I0", "THM_FIRST_HAMLET_Z2"),
    ),
    Claim(
        "GATE_HAMLET_RELATIONAL_BINDING",
        ClaimKind.DERIVATION_GATE,
        "Strict relational-binding gate: derive from bare foundational structure, rather than canonical RDSS representation semantics, that DISPERSION and STRUCTURE must be realized as distinct relational occurrence identities. Canonical RDSS may represent them this way definitionally while the universal entailment remains open.",
        ("THM_FIRST_HAMLET_Z2", "DEF_RELATIONAL_DISTINCTION"),
    ),
    Claim(
        "DEF_RDSS_RELATIONAL_INFORMATION_REALIZATION",
        ClaimKind.DEFINITION,
        "Canonical RDSS relational-information semantics: distinguishable alternatives of a realized information state are represented as distinct occurrence identities bound to their host by branch relations; carrier labels may coincide while occurrence identities remain distinct.",
        ("DEF_RELATIONAL_DISTINCTION", "DEF_CARRIER_OCCURRENCE_SEPARATION"),
    ),
    Claim(
        "REF_CANONICAL_HAMLET_RELATIONAL_REALIZATION",
        ClaimKind.REFERENCE_REALIZATION,
        "The canonical minimal Hamlet realization uses one admitted host carrier, one underlying relation value if desired, and two distinct +/- branch-relation occurrences. This realizes the semantic shape targeted by RA0_REL_STAR without claiming that bare L1 logically forces that representation.",
        ("DEF_RDSS_REALIZED_EXISTENCE_INFORMATION_STATE", "DEF_RDSS_RELATIONAL_INFORMATION_REALIZATION", "THM_CANONICAL_REALIZED_EXISTENCE_BINARY"),
    ),
    Claim(
        "THM_CANONICAL_REALIZED_EXISTENCE_RELATIONAL_BINARY",
        ClaimKind.THEOREM,
        "Under the canonical RDSS definitions of realized existence and relational-information realization, the minimal realized existence state is binary and its two distinguishable alternatives are represented by two distinct branch-occurrence identities bound relationally to their host. This is a theorem of the chosen semantics, not a proof that bare L1 entails RA0_REL_STAR for every admitted carrier.",
        ("DEF_RDSS_REALIZED_EXISTENCE_INFORMATION_STATE", "DEF_RDSS_RELATIONAL_INFORMATION_REALIZATION", "THM_CANONICAL_REALIZED_EXISTENCE_BINARY", "REF_CANONICAL_HAMLET_RELATIONAL_REALIZATION"),
    ),
    Claim(
        "THM_BINARY_BRANCH_SWAP_INVOLUTION",
        ClaimKind.THEOREM,
        "On the primitive branch alphabet B={-1,+1}, sigma(b)=-b is the unique non-trivial involution. It extends letterwise to an involutive automorphism of the finite-word address space B* and exchanges the two depth-one Hamlet branches.",
        ("DEF_OCCURRENCE_ADDRESS_SPACE", "THM_OCCURRENCE_ADDRESS_FREE_MONOID"),
    ),
    Claim(
        "THM_Z2_UNIQUE_SWAP_INVARIANT_PROBABILITY",
        ClaimKind.THEOREM,
        "On an unlabelled two-element outcome set, the unique normalized non-negative probability invariant under its non-trivial automorphism is uniform: p_-=p_+=1/2. This is an abstract Z2 result and does not depend on the occurrence-address representation.",
        ("THM_RELATION_ORIENTATION_Z2",),
    ),
    Claim(
        "THM_HAMLET_HALF_HALF",
        ClaimKind.THEOREM,
        "Legacy/meta result: if a normalized probability measure is placed on the first-Hamlet persistence classes and required to be complement-invariant, it is uniform. This meta weighting is not used by the durable relation-role geometry.",
        ("THM_FIRST_HAMLET_Z2", "THM_Z2_UNIQUE_SWAP_INVARIANT_PROBABILITY"),
    ),
    Claim(
        "THM_HAMLET_LN2",
        ClaimKind.THEOREM,
        "The fundamental first-Hamlet information is exactly ln(2) by the Hartley count of its two exhaustive classes. If the later complement-invariant probability measure is used, Shannon entropy independently gives the same ln(2), providing a consistency check rather than an upstream premise.",
        ("THM_FIRST_HAMLET_HARTLEY_LN2", "THM_HAMLET_HALF_HALF"),
    ),
    Claim(
        "THM_HAMLET_RELATIONAL_ZETA_ZERO",
        ClaimKind.THEOREM,
        "Under the normalized sign-character chart of the persistent relation roles {-1,+1}, the relational centre is zeta=(-1+1)/2=0. This represented relational zero is not absolute nothingness and does not depend on persistence-class probabilities.",
        ("THM_Z2_UNIQUE_NONTRIVIAL_REAL_CHARACTER",),
    ),
    Claim(
        "THM_BARE_CARRIER_POINT_DISTINCT_FROM_RELATIONAL_ZETA",
        ClaimKind.THEOREM,
        "The bare singleton RelationalPoint used as a model-theoretic non-vacuity witness and the derived relational centre zeta=0 are distinct typed constructions: the former witnesses |Adm|=1 without internal binary structure, while the latter is defined only after the Hamlet sign opposition is available.",
        ("THM_FIRST_LAW_MINIMAL_NONTRIVIAL_CARRIER", "THM_HAMLET_RELATIONAL_ZETA_ZERO"),
    ),
    Claim(
        "DEF_HAMLET_REAL_LINEAR_SPAN",
        ClaimKind.DEFINITION,
        "Legacy identifier, canonical content: for the ordered persistent relation-role basis (e_N,e_S), let V_H=R e_N direct-sum R e_S be the free real linear span. DISPERSION/STRUCTURE are not used as this vector-space basis.",
        ("THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT", "THM_RELATION_ORIENTATION_Z2", "THM_FIRST_HAMLET_NOT_PROJECTIVE_BINARY_CARRIER"),
    ),
    Claim(
        "THM_HAMLET_SWAP_POLARITY_ANTICOMMUTE",
        ClaimKind.THEOREM,
        "On the persistent relation-role span define swap S(e_N)=e_S, S(e_S)=e_N and polarity P(e_N)=-e_N, P(e_S)=+e_S. Then S^2=P^2=I and SP=-PS.",
        ("DEF_HAMLET_REAL_LINEAR_SPAN", "THM_RELATION_ORIENTATION_Z2", "THM_Z2_UNIQUE_NONTRIVIAL_REAL_CHARACTER"),
    ),
    Claim(
        "THM_FIRST_HAMLET_SWAP_INVARIANT_UNIT_VECTOR",
        ClaimKind.THEOREM,
        "Legacy identifier, canonical content: on the persistent relation-role span, the +1 eigenspace of role swap S is one-dimensional and spanned by e_N+e_S. Unit normalization fixes Psi_0=(e_N+e_S)/sqrt(2), unique up to overall sign/phase; no probability premise is used.",
        ("DEF_HAMLET_REAL_LINEAR_SPAN", "THM_HAMLET_SWAP_POLARITY_ANTICOMMUTE"),
    ),
    Claim(
        "THM_HAMLET_IMAGINARY_GENERATOR",
        ClaimKind.THEOREM,
        "The real-linear operator J=SP satisfies J^2=-I. Relative to the ordered durable relation-role basis (e_N,e_S) this is the canonical complex-structure generator, unique up to J->-J under reversal of role orientation; it realizes the algebraic role of i without assuming complex scalars upstream.",
        ("THM_HAMLET_SWAP_POLARITY_ANTICOMMUTE",),
    ),
    Claim(
        "THM_IMAGINARY_GENERATOR_U1",
        ClaimKind.THEOREM,
        "Because J^2=-I, exp(phi J)=cos(phi)I+sin(phi)J forms the standard SO(2) one-parameter rotation group, canonically isomorphic to U(1) after identifying J with multiplication by i.",
        ("THM_HAMLET_IMAGINARY_GENERATOR",),
    ),
    Claim(
        "THM_Z2_SIGN_EMBEDS_U1",
        ClaimKind.THEOREM,
        "After U(1) has been derived, the real sign character embeds as its unique order-two subgroup: +1 maps to phase 0 and the non-trivial Hamlet sign -1 maps to exp(i*pi).",
        ("THM_Z2_UNIQUE_NONTRIVIAL_REAL_CHARACTER", "THM_IMAGINARY_GENERATOR_U1"),
    ),
    Claim(
        "THM_HAMLET_COMPLEX_SCALAR_ALGEBRA",
        ClaimKind.THEOREM,
        "The real operator algebra span_R{I,J} generated by the Hamlet complex structure J with J^2=-I is isomorphic to the complex numbers via aI+bJ <-> a+ib.",
        ("THM_HAMLET_IMAGINARY_GENERATOR",),
    ),
    Claim(
        "THM_HAMLET_FULL_OPERATOR_ALGEBRA_M2R",
        ClaimKind.THEOREM,
        "In the ordered durable relation-role basis (e_N,e_S), I, swap S, polarity P and J=SP are linearly independent and span the full four-real-dimensional matrix algebra M_2(R). Their multiplication closes with S^2=P^2=I, SP=-PS and J^2=-I.",
        ("THM_HAMLET_SWAP_POLARITY_ANTICOMMUTE", "THM_HAMLET_IMAGINARY_GENERATOR"),
    ),
    Claim(
        "THM_HAMLET_OPERATOR_ALGEBRA_C2_MODULE",
        ClaimKind.THEOREM,
        "Let C_J=span_R{I,J}. Because S J=P, the full Hamlet operator algebra decomposes exactly as the right C_J-module A_H=C_J direct-sum S C_J. Hence A_H has complex dimension two and is canonically isomorphic to C_J^2 without introducing a second independent copy of the Hamlet branch degree of freedom.",
        ("THM_HAMLET_COMPLEX_SCALAR_ALGEBRA", "THM_HAMLET_FULL_OPERATOR_ALGEBRA_M2R"),
    ),
    Claim(
        "THM_HAMLET_OPERATOR_FROBENIUS_NORM",
        ClaimKind.THEOREM,
        "With normalized Frobenius form (A,B)=Tr(A^T B)/2, the basis {I,S,P,J} is orthonormal. Under A=z_0+S z_1 with z_0,z_1 in C_J, the induced norm is |z_0|^2+|z_1|^2 and right multiplication by exp(phi J) preserves the norm and acts as common U(1) phase on both complex coordinates.",
        ("THM_HAMLET_OPERATOR_ALGEBRA_C2_MODULE", "THM_IMAGINARY_GENERATOR_U1"),
    ),
    Claim(
        "THM_HAMLET_OPERATOR_PROJECTIVE_CP1",
        ClaimKind.THEOREM,
        "The unit-norm sphere in the Hamlet operator module A_H=C_J^2 is S^3. Quotienting the free right action of exp(phi J) gives S^3/U(1), canonically CP^1 and diffeomorphic to S^2. This is the canonical no-duplication route to the RDSS potential sphere.",
        ("THM_HAMLET_OPERATOR_ALGEBRA_C2_MODULE", "THM_HAMLET_OPERATOR_FROBENIUS_NORM", "DEF_CP1_PROJECTIVE_EQUIVALENCE", "THM_IMAGINARY_GENERATOR_U1"),
    ),
    Claim(
        "THM_HAMLET_S3_SU2_BIJECTION",
        ClaimKind.THEOREM,
        "A unit pair of Hamlet module coordinates determines an SU(2) matrix by taking that pair as the first column and its standard orthogonal conjugate as the second column. This construction is bijective, so the unit module sphere S^3 is canonically identified with SU(2).",
        ("THM_HAMLET_OPERATOR_FROBENIUS_NORM",),
    ),
    Claim(
        "THM_HAMLET_SU2_U1_QUOTIENT_S2",
        ClaimKind.THEOREM,
        "Under the S^3 to SU(2) identification, common Hamlet module phase is the standard right U(1) action in SU(2). Hence the potential sphere is equivalently SU(2)/U(1), CP^1 and S^2.",
        ("THM_HAMLET_S3_SU2_BIJECTION", "THM_HAMLET_OPERATOR_PROJECTIVE_CP1"),
    ),
    Claim(
        "THM_HAMLET_PAULI_TRIPLE",
        ClaimKind.THEOREM,
        "After the complex scalar algebra C_J is available, the Hamlet operators define the Pauli triple sigma_x=S, sigma_z=-P, sigma_y=-iJ. They obey sigma_k^2=I and [sigma_i,sigma_j]=2 i epsilon_ijk sigma_k.",
        ("THM_HAMLET_FULL_OPERATOR_ALGEBRA_M2R", "THM_HAMLET_COMPLEX_SCALAR_ALGEBRA"),
    ),
    Claim(
        "THM_HAMLET_SU2_GENERATORS",
        ClaimKind.THEOREM,
        "With T_k=sigma_k/2, the Hamlet Pauli triple satisfies [T_i,T_j]=i epsilon_ijk T_k and therefore furnishes the defining two-dimensional representation of the standard su(2) Lie algebra.",
        ("THM_HAMLET_PAULI_TRIPLE",),
    ),
    Claim(
        "THM_HAMLET_SU2_CASIMIR_HALF",
        ClaimKind.THEOREM,
        "For the Hamlet su(2) generators, sum_k T_k^2=3I/4. Under the standard non-negative su(2) representation label j defined by the Casimir j(j+1)I, this uniquely gives j=1/2.",
        ("THM_HAMLET_SU2_GENERATORS",),
    ),
    Claim(
        "THM_HAMLET_SPINOR_2PI_4PI_RETURN",
        ClaimKind.THEOREM,
        "Exponentiating any normalized Hamlet su(2) axis gives the defining spinor rotation U(theta)=exp(-i theta n·sigma/2). Consequently U(2*pi)=-I and U(4*pi)=+I.",
        ("THM_HAMLET_SU2_GENERATORS",),
    ),
    Claim(
        "DEF_HAMLET_COMPLEX_BRANCH_SPACE",
        ClaimKind.DEFINITION,
        "Alternative reference presentation: using the derived complex scalar algebra C_J, the free complex vector space on two labelled Hamlet outcomes is H_B=C_J[B]. The mega-audit no longer uses this construction as the canonical derivation of complex dimension two because it can obscure reuse of the same binary degree of freedom; the operator-algebra module A_H supplies the canonical route.",
        ("THM_HAMLET_COMPLEX_SCALAR_ALGEBRA", "THM_MINIMAL_INFORMATION_STATE_BINARY"),
    ),
    Claim(
        "THM_HAMLET_UNIQUE_SYMMETRY_HERMITIAN_FORM",
        ClaimKind.THEOREM,
        "On the two-complex-dimensional Hamlet branch space, any positive-definite Hermitian form invariant under both branch swap S and branch polarity P is a positive scalar multiple of the identity form. The normalized branch-weight convention fixes that scalar, yielding the canonical l2/counting Hermitian form.",
        ("DEF_HAMLET_COMPLEX_BRANCH_SPACE", "THM_HAMLET_SWAP_POLARITY_ANTICOMMUTE", "THM_HAMLET_HALF_HALF"),
    ),
    Claim(
        "REF_HAMLET_COUNTING_HERMITIAN_FORM",
        ClaimKind.REFERENCE_REALIZATION,
        "The executable/reference branch-space Hermitian form is <psi,phi>=sum_{b in B} conjugate(psi_b) phi_b with branch delta-functions orthonormal, realizing THM_HAMLET_UNIQUE_SYMMETRY_HERMITIAN_FORM at unit normalization.",
        ("THM_HAMLET_UNIQUE_SYMMETRY_HERMITIAN_FORM",),
    ),
    Claim(
        "THM_HAMLET_PROJECTIVE_CP1",
        ClaimKind.THEOREM,
        "For the two-complex-dimensional Hamlet branch space with its symmetry-fixed Hermitian form, non-zero vectors modulo non-zero common complex scaling form CP^1. The normalized unit sphere S^3 modulo common U(1) phase is CP^1, diffeomorphic to S^2.",
        ("DEF_HAMLET_COMPLEX_BRANCH_SPACE", "THM_HAMLET_UNIQUE_SYMMETRY_HERMITIAN_FORM", "REF_HAMLET_COUNTING_HERMITIAN_FORM", "DEF_CP1_PROJECTIVE_EQUIVALENCE", "THM_IMAGINARY_GENERATOR_U1"),
    ),
    Claim(
        "REF_EXISTENCE_POTENTIAL_CP1_SPHERE",
        ClaimKind.REFERENCE_REALIZATION,
        "The CP^1 ~= S^2 geometry of the unit Hamlet operator module A_H=C_J^2 modulo common right U(1) phase is the canonical RDSS potential-sphere realization. The older free complex branch-space construction is retained only as an equivalent reference chart.",
        ("THM_HAMLET_OPERATOR_PROJECTIVE_CP1",),
    ),
    Claim(
        "REF_RELATIONAL_ZETA_POTENTIAL_SPHERE_CENTER",
        ClaimKind.REFERENCE_REALIZATION,
        "In the ambient three-coordinate Bloch-sphere chart, relational zeta=0 is the centre of the potential sphere, not a pure-state point on the CP^1 surface and not absolute nothingness.",
        ("THM_HAMLET_RELATIONAL_ZETA_ZERO", "REF_EXISTENCE_POTENTIAL_CP1_SPHERE"),
    ),
    Claim(
        "REF_CP1_BERRY_GEOMETRIC_PHASE",
        ClaimKind.REFERENCE_REALIZATION,
        "On the CP^1 projective-state geometry, parallel transport around a closed loop carries a Berry geometric holonomy phase in U(1). The phase is treated as geometric holonomy, not as a force law.",
        ("REF_EXISTENCE_POTENTIAL_CP1_SPHERE", "REF_U1_PHASE_VALUE"),
    ),
    Claim(
        "REF_BERRY_PHASE_CONNECTION_POTENTIAL_CLASS",
        ClaimKind.REFERENCE_REALIZATION,
        "A Berry holonomy phase admits local representation by a U(1) connection one-form A_B whose closed-loop integral reproduces the phase modulo 2*pi. A_B is gauge-dependent; the phase fixes connection data only up to gauge and does not determine a unique physical potential.",
        ("REF_CP1_BERRY_GEOMETRIC_PHASE",),
    ),
    Claim(
        "BRIDGE_EXISTENCE_POTENTIAL_AHARONOV_BOHM",
        ClaimKind.BRIDGE,
        "Aharonov-Bohm is retained only as an independent physical precedent for the phase-potential relation: gauge-potential data can carry observable loop phase even when the classical local field vanishes along the accessible path. It is downstream evidence and does not derive P_E, i, U(1), or the Berry connection.",
        ("REF_BERRY_PHASE_CONNECTION_POTENTIAL_CLASS",),
    ),
    Claim(
        "THM_FIRST_LAW_MINIMAL_NONTRIVIAL_CARRIER",
        ClaimKind.THEOREM,
        "The First-Law model-formation route gives a non-empty admitted domain, and the explicit bare singleton point presentation attains the lower bound; therefore the exact minimal admitted-carrier cardinality is one. The unscaled point is a reference realization of that minimum, not an extra foundational premise.",
        ("DEF_EXISTENCE_POTENTIAL", "THM_META0_MINIMAL_CARRIER_CARDINALITY", "REF_META0_SINGLETON_POINT_PRESENTATION"),
    ),
    Claim(
        "THM_FIRST_LAW_NONEMPTY_NOT_BINARY",
        ClaimKind.THEOREM,
        "The bare singleton META0-admissible point presentation contains one admitted carrier and no hosted binary distinction. Therefore the First Law, modal existence potential and bare non-empty singleton carrier do not by themselves force Hamlet binary differentiation.",
        ("DEF_EXISTENCE_POTENTIAL", "REF_META0_SINGLETON_POINT_PRESENTATION", "THM_FIRST_LAW_MINIMAL_NONTRIVIAL_CARRIER"),
    ),
    Claim(
        "THM_HAMLET_CANONICAL_PROJECTIVE_LOOP",
        ClaimKind.THEOREM,
        "In A_H=C_J direct-sum S C_J take the normalized balanced state Psi_0=(I+S)/sqrt(2). Left multiplication by exp(theta J) gives complex module coordinates (exp(i theta), exp(-i theta))/sqrt(2). For 0<=theta<=pi this orbit is norm-preserving and horizontal, its projective image is a primitive great-circle loop, and Psi(pi)=-Psi_0. A fixed unitary chart sends it to the earlier real branch orbit (cos theta,-sin theta).",
        ("THM_HAMLET_OPERATOR_PROJECTIVE_CP1", "THM_FIRST_HAMLET_SWAP_INVARIANT_UNIT_VECTOR", "THM_HAMLET_IMAGINARY_GENERATOR"),
    ),
    Claim(
        "THM_HAMLET_BALANCED_ORBIT_BLOCH_EQUATOR",
        ClaimKind.THEOREM,
        "For the balanced canonical module orbit, the Bloch coordinates are (cos(2 theta), -sin(2 theta), 0). Thus theta from 0 to pi traverses the equator exactly once and bounds a hemisphere with solid angle magnitude 2*pi.",
        ("THM_HAMLET_CANONICAL_PROJECTIVE_LOOP", "THM_HAMLET_SU2_U1_QUOTIENT_S2"),
    ),
    Claim(
        "THM_HAMLET_PROJECTIVE_SIGN_CLOSURE",
        ClaimKind.THEOREM,
        "The horizontal lift of the canonical Hamlet projective loop ends at -psi_0, so its Hopf/Berry holonomy is exactly the non-trivial order-two phase -1. This realizes the Hamlet sign character geometrically rather than assuming it.",
        ("THM_HAMLET_CANONICAL_PROJECTIVE_LOOP", "THM_Z2_SIGN_EMBEDS_U1", "REF_CP1_BERRY_GEOMETRIC_PHASE"),
    ),
    Claim(
        "THM_EULER_BERRY_MINIMAL_SPIN_HALF",
        ClaimKind.THEOREM,
        "The Hamlet Pauli algebra gives the defining su(2) representation with Casimir j(j+1)=3/4, hence j=1/2, and its exponentiated rotations satisfy 2*pi -> -I and 4*pi -> +I. The independently derived canonical Berry loop has the same -1 holonomy, with Euler phase exp(i*pi)=-1. Thus representation-theoretic half-spin and Berry/Euler closure agree without using the spin-s Berry formula as an upstream premise. Physical angular-momentum identification remains a separate bridge.",
        ("THM_HAMLET_SU2_CASIMIR_HALF", "THM_HAMLET_SPINOR_2PI_4PI_RETURN", "THM_HAMLET_PROJECTIVE_SIGN_CLOSURE", "THM_HAMLET_BALANCED_ORBIT_BLOCH_EQUATOR"),
    ),
    # Canonical source: docs/CANONICAL_FOUNDATIONAL_CONTRACT.md §§1–2.
    Claim(
        "META0",
        ClaimKind.FORMATION_RULE,
        "Model-formation unpacking of the Law of Reality: absolute nothingness has no denotation in the RTOFA object language, and every admissible RTOFA model has non-empty admitted occurrence support and therefore non-empty carrier support.",
        ("A0", "DEF_LR_OCCURRENCE_CARRIER_SEPARATION"),
    ),
    Claim(
        "EX0",
        ClaimKind.THEOREM,
        "Model non-vacuity: every admissible RTOFA model contains at least one admitted relational carrier.",
        ("META0",),
    ),
    # Canonical source: docs/CANONICAL_FOUNDATIONAL_CONTRACT.md §§1–2.
    Claim(
        "RA0",
        ClaimKind.THEOREM,
        "Relational admissibility is the carrier projection of the relational witness required by the Law of Reality: every admitted observable is incident to at least one primitive relation, as source or target. Endpoint carrier labels may coincide when distinct occurrences share one singleton carrier.",
        ("A0", "THM_LR_SINGLETON_CAN_SUPPORT_BINARY_DISTINCTION", "DEF_RELATIONAL_DISTINCTION"),
    ),
    Claim(
        "DEF_POINT",
        ClaimKind.DEFINITION,
        "The minimal algebraic carrier is an unscaled point.",
    ),
    Claim(
        "DEF_OCCURRENCE_ADDRESS_SPACE",
        ClaimKind.DEFINITION,
        "Occurrence addresses are finite words B* over the binary alphabet B={-1,+1}, with concatenation and the empty word.",
    ),
    Claim(
        "DEF_CARRIER_OCCURRENCE_SEPARATION",
        ClaimKind.DEFINITION,
        "Carrier values and occurrence addresses are distinct sorts: a relation value is typed on carriers, while branch-aware identity is carried separately by OccurrenceAddress.",
        ("DEF_POINT", "DEF_OCCURRENCE_ADDRESS_SPACE"),
    ),
    Claim(
        "REF_RELATIONAL_POINT_BINARY_COORDINATE",
        ClaimKind.REFERENCE_REALIZATION,
        "The reference RelationalPoint implementation retains a binary coordinate for compatibility with existing realizations; that coordinate is not the canonical occurrence identity of occurrence-aware paths.",
        ("DEF_POINT", "DEF_OCCURRENCE_ADDRESS_SPACE"),
    ),
    Claim(
        "THM_OCCURRENCE_ADDRESS_FREE_MONOID",
        ClaimKind.THEOREM,
        "The finite binary address space B* is the free monoid on generators -1 and +1 under concatenation, with the empty word as identity.",
        ("DEF_OCCURRENCE_ADDRESS_SPACE",),
    ),
    Claim(
        "THM_REFINEMENT_RIGHT_ACTION",
        ClaimKind.THEOREM,
        "Appending finite binary words to OccurrenceAddress values defines the regular right action of B*: omega·empty=omega and (omega·u)·v=omega·(uv).",
        ("DEF_OCCURRENCE_ADDRESS_SPACE",),
    ),
    Claim(
        "THM_REFINEMENT_LEVEL_GRADING",
        ClaimKind.THEOREM,
        "The word-length map grades the occurrence-address monoid: |uv|=|u|+|v| and level(omega·u)=level(omega)+|u|.",
        ("THM_REFINEMENT_RIGHT_ACTION",),
    ),
    Claim(
        "DEF_OCCURRENCE_PREFIX_ORDER",
        ClaimKind.DEFINITION,
        "The occurrence-address prefix order is u<=v iff there exists a finite word w with v=uw.",
        ("DEF_OCCURRENCE_ADDRESS_SPACE",),
    ),
    Claim(
        "THM_OCCURRENCE_MEET_SEMILATTICE",
        ClaimKind.THEOREM,
        "Under prefix order, finite binary occurrence addresses form a rooted meet-semilattice whose meet is the longest common prefix.",
        ("DEF_OCCURRENCE_PREFIX_ORDER",),
    ),
    Claim(
        "DEF_OCCURRENCE_TREE_DISTANCE",
        ClaimKind.DEFINITION,
        "The canonical occurrence-tree distance is d_T(u,v)=|u|+|v|-2|u meet v|.",
        ("THM_OCCURRENCE_MEET_SEMILATTICE", "THM_REFINEMENT_LEVEL_GRADING"),
    ),
    Claim(
        "THM_OCCURRENCE_TREE_METRIC",
        ClaimKind.THEOREM,
        "The canonical occurrence-tree distance is a metric on finite path-labelled occurrence addresses.",
        ("DEF_OCCURRENCE_TREE_DISTANCE",),
    ),
    Claim(
        "DEF_BINARY_REL",
        ClaimKind.DEFINITION,
        "A primitive typed relation is binary: r:a->b. Higher arity is constructed separately.",
    ),
    Claim(
        "DEF_RELATION_OCCURRENCE",
        ClaimKind.DEFINITION,
        "A relation occurrence is a typed relation value together with source and target OccurrenceAddress values; distinct occurrences may project to the same relation value.",
        ("DEF_BINARY_REL", "DEF_CARRIER_OCCURRENCE_SEPARATION"),
    ),
    Claim(
        "THM_RELATION_DIRECTION_NOT_BRANCH_DUPLICATION",
        ClaimKind.THEOREM,
        "The source/target direction of a primitive typed relation value does not by itself generate two distinct branch occurrences. In particular, for a singleton self-relation r:a->a, endpoint reversal leaves the relation-value endpoints unchanged; distinct +/- occurrence identity requires explicit occurrence-address or branch-slot data.",
        ("DEF_BINARY_REL", "DEF_RELATION_OCCURRENCE", "DEF_CARRIER_OCCURRENCE_SEPARATION"),
    ),
    Claim(
        "DEF_OCCURRENCE_PATH",
        ClaimKind.DEFINITION,
        "An occurrence-aware relation path is composable in both carrier value and occurrence address, with a consistent carrier assigned to each occurrence address.",
        ("DEF_RELATION_OCCURRENCE",),
    ),
    Claim(
        "DEF_OCCURRENCE_FORGETFUL_PROJECTION",
        ClaimKind.DEFINITION,
        "The forgetful projection pi_occ_to_val removes occurrence addresses from relation occurrences and occurrence-aware paths while retaining their typed relation values and order.",
        ("DEF_OCCURRENCE_PATH",),
    ),
    Claim(
        "THM_OCCURRENCE_COMPOSABILITY_PROJECTS",
        ClaimKind.THEOREM,
        "Every occurrence-composable relation path projects under pi_occ_to_val to a composable relation-value path.",
        ("DEF_OCCURRENCE_FORGETFUL_PROJECTION",),
    ),
    Claim(
        "THM_OCCURRENCE_CLOSED_IMPLIES_VALUE_CLOSED",
        ClaimKind.THEOREM,
        "For a consistent occurrence-to-carrier assignment, occurrence closure implies carrier/value closure after the forgetful projection.",
        ("DEF_OCCURRENCE_FORGETFUL_PROJECTION",),
    ),
    Claim(
        "REF_VALUE_CLOSED_OCCURRENCE_OPEN_COUNTERMODEL",
        ClaimKind.REFERENCE_REALIZATION,
        "A singleton self-relation step from the root occurrence to a child occurrence is value-closed but occurrence-open.",
        ("DEF_OCCURRENCE_FORGETFUL_PROJECTION",),
    ),
    Claim(
        "THM_VALUE_CLOSED_NOT_OCCURRENCE_CLOSED",
        ClaimKind.THEOREM,
        "The explicit singleton countermodel shows that carrier/value closure does not imply occurrence closure.",
        ("REF_VALUE_CLOSED_OCCURRENCE_OPEN_COUNTERMODEL",),
    ),
    Claim(
        "DEF_BINARY_DISTINCTION",
        ClaimKind.DEFINITION,
        "A hosted binary distinction has two ordered branch occurrence slots (-,+). Non-degeneracy is occurrence-level and does not require different carrier labels in the two slots.",
        ("DEF_POINT", "DEF_OCCURRENCE_ADDRESS_SPACE"),
    ),
    Claim(
        "DEF_RELATIONAL_DISTINCTION",
        ClaimKind.DEFINITION,
        "A relationally bound binary distinction consists of two branch-relation occurrences from the host occurrence to the left/right endpoint occurrences; occurrence identity includes the branch slot, so endpoint carrier labels and even underlying relation values may coincide.",
        ("DEF_BINARY_DISTINCTION", "DEF_RELATION_OCCURRENCE"),
    ),
    Claim(
        "RR1",
        ClaimKind.DERIVATION_GATE,
        "Recursive relational closure target: at every admitted path-labelled occurrence, a selected endpoint may itself carry a further non-degenerate binary distinction, so the rule re-applies at each finite refinement depth. This is not an additional axiom; its complete derivation from A0 remains an explicit gate.",
        ("A0", "DEF_POINT", "DEF_BINARY_DISTINCTION"),
    ),
    Claim(
        "THM_RR1_REALIZES_FINITE_WORDS",
        ClaimKind.THEOREM,
        "Under RR1, every finite binary address word from an admitted root is realized by a path-labelled occurrence.",
        ("RR1", "DEF_OCCURRENCE_ADDRESS_SPACE"),
    ),
    Claim(
        "REF_CP1",
        ClaimKind.REFERENCE_REALIZATION,
        "Legacy/reference realization: a minimal complex binary distinction may be represented by projectively distinct CP^1 states with Fubini-Study metric. This realizes the generic projective-equivalence definition and is not a premise of the canonical Hamlet operator-algebra derivation.",
        ("DEF_POINT", "DEF_BINARY_DISTINCTION", "DEF_CP1_PROJECTIVE_EQUIVALENCE"),
    ),
    Claim(
        "REF_CP1_REFINEMENT",
        ClaimKind.REFERENCE_REALIZATION,
        "Recursive refinement may be realized as a tree of local CP^1/Fubini-Study fibres indexed by relational carriers.",
        ("REF_CP1", "RR1"),
    ),
    Claim(
        "REF_SINGLETON_CP1_OCCURRENCE_REALIZATION",
        ClaimKind.REFERENCE_REALIZATION,
        "The minimal singleton relational model is compatible at every finite tested depth with a local CP^1/Fubini-Study fibre on each path-labelled occurrence, while all occurrences may retain the same underlying carrier label.",
        ("REF_MINIMAL_SINGLE_RELATION_VALUE_MODEL", "REF_CP1_REFINEMENT"),
    ),
    Claim(
        "RA0_STAR",
        ClaimKind.DERIVATION_GATE,
        "Every admitted carrier hosts an admitted non-degenerate binary distinction whose endpoint occurrences are admitted carriers.",
        ("DEF_POINT", "DEF_BINARY_DISTINCTION"),
    ),
    Claim(
        "RA0_REL_STAR",
        ClaimKind.DERIVATION_GATE,
        "Every admitted carrier hosts at least one admitted relationally bound binary distinction whose endpoint occurrences are admitted carriers.",
        ("DEF_POINT", "DEF_RELATIONAL_DISTINCTION"),
    ),
    Claim(
        "THM_RA0_STAR_FROM_RA0_REL_STAR",
        ClaimKind.THEOREM,
        "Forgetting explicit branch-relation binding from any RA0_REL_STAR model yields an RA0_STAR model with the same admitted carriers and branch occurrence structure.",
        ("RA0_REL_STAR",),
    ),
    Claim(
        "THM_RA0_FROM_RA0_REL_STAR",
        ClaimKind.THEOREM,
        "RA0_REL_STAR implies orientation-neutral relational admissibility because each admitted host is the source of at least one branch-relation occurrence.",
        ("RA0_REL_STAR",),
    ),
    Claim(
        "THM_RR1_FROM_RA0_REL_STAR",
        ClaimKind.THEOREM,
        "RA0_REL_STAR generates recursive binary refinement to arbitrary finite depth by induction on admitted path-labelled occurrences.",
        ("RA0_REL_STAR",),
    ),
    Claim(
        "THM_META0_CARDINALITY_LOWER_BOUND",
        ClaimKind.THEOREM,
        "META0 implies that every admissible RTOFA model has at least one admitted carrier: |Adm| >= 1.",
        ("META0",),
    ),
    Claim(
        "REF_META0_SINGLETON_POINT_PRESENTATION",
        ClaimKind.REFERENCE_REALIZATION,
        "A bare META0-admissible presentation may contain exactly one admitted unscaled RelationalPoint and no additional relational, geometric or dynamical structure.",
        ("META0", "DEF_POINT"),
    ),
    Claim(
        "THM_META0_MINIMAL_CARRIER_CARDINALITY",
        ClaimKind.THEOREM,
        "The META0 non-empty lower bound together with the singleton-point witness gives the exact bare-model minimum |Adm|=1. This is a model-formation result, not a physical collapse or dynamics claim.",
        ("THM_META0_CARDINALITY_LOWER_BOUND", "REF_META0_SINGLETON_POINT_PRESENTATION"),
    ),
    Claim(
        "REF_SINGLETON_RA0_REL_STAR_MODEL",
        ClaimKind.REFERENCE_REALIZATION,
        "The recursive singleton self-relational model is an explicit admissible model of META0 plus RA0_REL_STAR with |Adm| = 1.",
        ("META0", "RA0_REL_STAR"),
    ),
    Claim(
        "REF_RA0_RR1_UNBOUND_MODEL",
        ClaimKind.REFERENCE_REALIZATION,
        "A singleton self-relational model can satisfy META0, RA0, and recursive RR1 while carrying no explicit branch-slot to primitive-relation binding.",
        ("META0", "RA0", "RR1"),
    ),
    Claim(
        "THM_RA0_RR1_NOT_RA0_REL_STAR",
        ClaimKind.THEOREM,
        "The explicit unbound singleton countermodel shows that RA0 plus RR1 does not imply RA0_REL_STAR.",
        ("REF_RA0_RR1_UNBOUND_MODEL",),
    ),
    Claim(
        "THM_SINGLETON_FOUNDATION_MINIMALITY",
        ClaimKind.THEOREM,
        "Combining the META0 lower bound with the explicit singleton RA0_REL_STAR model shows that the minimum admitted-carrier cardinality is exactly one.",
        ("THM_META0_CARDINALITY_LOWER_BOUND", "REF_SINGLETON_RA0_REL_STAR_MODEL"),
    ),
    Claim(
        "THM_RELATION_VALUE_CARDINALITY_LOWER_BOUND",
        ClaimKind.THEOREM,
        "META0 plus RA0_REL_STAR imply at least one underlying primitive relation value after forgetting branch-occurrence identity.",
        ("META0", "RA0_REL_STAR"),
    ),
    Claim(
        "REF_MINIMAL_SINGLE_RELATION_VALUE_MODEL",
        ClaimKind.REFERENCE_REALIZATION,
        "The minimal singleton RA0_REL_STAR model uses one admitted carrier and one underlying self-relation value while retaining two distinct branch occurrences.",
        ("META0", "RA0_REL_STAR"),
    ),
    Claim(
        "THM_SINGLE_RELATION_VALUE_MINIMALITY",
        ClaimKind.THEOREM,
        "The lower bound and the explicit minimal singleton witness show that the minimum underlying relation-value cardinality under META0 plus RA0_REL_STAR is exactly one.",
        ("THM_RELATION_VALUE_CARDINALITY_LOWER_BOUND", "REF_MINIMAL_SINGLE_RELATION_VALUE_MODEL"),
    ),
    Claim(
        "THM_RELATION_OCCURRENCE_CARDINALITY_LOWER_BOUND",
        ClaimKind.THEOREM,
        "META0 plus RA0_REL_STAR imply at least two branch-relation occurrences.",
        ("META0", "RA0_REL_STAR"),
    ),
    Claim(
        "THM_TWO_RELATION_OCCURRENCE_MINIMALITY",
        ClaimKind.THEOREM,
        "The explicit minimal singleton witness attains the branch-occurrence lower bound, so the exact minimum is two.",
        ("THM_RELATION_OCCURRENCE_CARDINALITY_LOWER_BOUND", "REF_MINIMAL_SINGLE_RELATION_VALUE_MODEL"),
    ),
    Claim(
        "THM_MINIMAL_RELATIONAL_ATOM_SIGNATURE",
        ClaimKind.THEOREM,
        "Under META0 plus RA0_REL_STAR, the minimal cardinality signature is one admitted carrier, one underlying primitive relation value, and two branch-relation occurrences.",
        (
            "THM_SINGLETON_FOUNDATION_MINIMALITY",
            "THM_SINGLE_RELATION_VALUE_MINIMALITY",
            "THM_TWO_RELATION_OCCURRENCE_MINIMALITY",
        ),
    ),
    Claim(
        "THM_BINARY_OCCURRENCE_COUNT",
        ClaimKind.THEOREM,
        "A complete binary occurrence unfolding through finite depth N contains exactly 2^(N+1)-1 path-labelled occurrences.",
        ("RR1", "DEF_BINARY_DISTINCTION"),
    ),
    Claim(
        "THM_FINITE_WORD_OCCURRENCE_COUNTABILITY",
        ClaimKind.THEOREM,
        "The full finite-depth occurrence address space {-1,+1}^{<omega} is countably infinite even when the underlying carrier presentation is finite or singleton.",
        ("THM_BINARY_OCCURRENCE_COUNT",),
    ),
    Claim(
        "DEF_OCCURRENCE_BOUNDARY",
        ClaimKind.DEFINITION,
        "The ideal occurrence boundary is the set {-1,+1}^N of infinite binary branch sequences; boundary points are ideal paths, not additional finite occurrence carriers.",
        ("DEF_OCCURRENCE_ADDRESS_SPACE",),
    ),
    Claim(
        "THM_BOUNDARY_CYLINDER_COUNT",
        ClaimKind.THEOREM,
        "At prefix depth n, the ideal occurrence boundary decomposes into exactly 2^n binary prefix cylinders.",
        ("DEF_OCCURRENCE_BOUNDARY",),
    ),
    Claim(
        "THM_OCCURRENCE_BOUNDARY_CONTINUUM",
        ClaimKind.THEOREM,
        "The ideal occurrence boundary {-1,+1}^N has cardinality 2^aleph_0, equivalently the cardinality of the power set of N.",
        ("DEF_OCCURRENCE_BOUNDARY",),
    ),
    Claim(
        "THM_RR1_REALIZES_BOUNDARY_PREFIX_CHAINS",
        ClaimKind.THEOREM,
        "Under RR1, every infinite binary boundary sequence determines a coherent chain whose every finite prefix is realized by a path-labelled occurrence; no limit carrier is thereby asserted.",
        ("RR1", "DEF_OCCURRENCE_BOUNDARY"),
    ),
    Claim(
        "THM_RR1_FROM_RA0_STAR",
        ClaimKind.THEOREM,
        "RA0* generates recursive binary refinement to arbitrary finite depth by induction on path-labelled occurrences.",
        ("RA0_STAR",),
    ),
    Claim(
        "PRIM_MODULE",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Each typed tensor-scalar sector carries an additive K-module structure; the reference kernel uses complex components.",
    ),
    Claim(
        "DEF_TS",
        ClaimKind.DEFINITION,
        "Tensor-scalar grading uses A^(p,q) with scalars in rank (0,0).",
        ("PRIM_MODULE",),
    ),
    Claim(
        "DEF_TYPED_ZERO",
        ClaimKind.DEFINITION,
        "The additive zero is typed by tensor rank, exact relational carrier, semantic scale, and component dimension; refinement level is derived from the carrier.",
        ("PRIM_MODULE", "DEF_POINT", "PRIM_SCALE"),
    ),
    Claim(
        "PRIM_PRODUCT",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "A typed relational product star_R may be supplied without assuming associativity or commutativity.",
    ),
    Claim(
        "PRIM_TENSOR_PRODUCT",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "A typed tensor product may combine compatible tensor-scalar sectors; concrete component formulas belong to realizations.",
        ("PRIM_MODULE",),
    ),
    Claim(
        "PRIM_CONTRACTION",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Typed contraction lowers one covariant and one contravariant rank when a contraction rule is supplied.",
        ("PRIM_MODULE",),
    ),
    Claim(
        "DEF_TENSOR_MAP_COHERENCE",
        ClaimKind.DEFINITION,
        "Tensor-map residual measures failure of Phi(X tensor Y) = Phi(X) tensor' Phi(Y).",
        ("PRIM_TENSOR_PRODUCT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_TENSOR_MONOIDAL_COHERENCE",
        ClaimKind.DEFINITION,
        "Strict tensor associativity, explicit unit, and supplied braiding are tested by residuals rather than assumed.",
        ("PRIM_TENSOR_PRODUCT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_CONTRACTION_MAP_COHERENCE",
        ClaimKind.DEFINITION,
        "Contraction-map residual measures failure of contraction naturality under a supplied typed map.",
        ("PRIM_CONTRACTION", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_BILINEARITY_RESIDUAL",
        ClaimKind.DEFINITION,
        "Bilinearity residuals measure failure of additivity and scalar-linearity of the relational product.",
        ("PRIM_PRODUCT", "PRIM_MODULE"),
    ),
    Claim(
        "PRIM_SCALE",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Semantic scale is a typed partial-order/category-like structure, not necessarily a real scalar.",
    ),
    Claim(
        "PRIM_SEMANTIC_WEIGHTING",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "A semantic profile may assign explicit non-negative weights to a fixed named residual signature; the weights are supplied rather than inferred from a scale label.",
        ("PRIM_SCALE",),
    ),
    Claim(
        "DEF_RELATIONAL_POTENTIAL",
        ClaimKind.DEFINITION,
        "A relational deformation potential is the weighted p-functional induced by a supplied semantic weighting on an explicit fixed residual signature.",
        ("PRIM_SEMANTIC_WEIGHTING",),
    ),
    Claim(
        "DER_SEMANTIC_POTENTIAL_SHIFT",
        ClaimKind.DERIVED,
        "Semantic potential shift is the difference between two semantic potential profiles evaluated on the same residual signature.",
        ("DEF_RELATIONAL_POTENTIAL",),
    ),
    Claim(
        "DER_RELATIONAL_ATTRACTOR",
        ClaimKind.DERIVED,
        "The relational attractor set is the set of admissible candidates attaining minimum relational potential.",
        ("DEF_RELATIONAL_POTENTIAL",),
    ),
    Claim(
        "PRIM_TRANSPORT",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Typed relation transports T_r may act between carrier sectors along composable relations.",
        ("DEF_BINARY_REL", "PRIM_MODULE"),
    ),
    Claim(
        "DER_HOLONOMY",
        ClaimKind.DERIVED,
        "Value-level relational holonomy is transport around a carrier-closed composable relation-value path, measured against the starting state.",
        ("PRIM_TRANSPORT",),
    ),
    Claim(
        "DER_OCCURRENCE_HOLONOMY",
        ClaimKind.DERIVED,
        "Occurrence-aware holonomy requires a transport path that is closed in both carrier value and occurrence address; carrier closure alone is insufficient.",
        ("PRIM_TRANSPORT", "DEF_OCCURRENCE_PATH"),
    ),
    Claim(
        "DEF_TRANSPORT_RESIDUAL",
        ClaimKind.DEFINITION,
        "Transport composition residual measures failure of direct transport to equal sequential transport.",
        ("PRIM_TRANSPORT",),
    ),
    Claim(
        "DEF_TRANSPORT_PRODUCT_COHERENCE",
        ClaimKind.DEFINITION,
        "Transport-product residual measures failure of T_r(X star Y) = T_r(X) star' T_r(Y).",
        ("PRIM_TRANSPORT", "PRIM_PRODUCT", "PRIM_MODULE"),
    ),
    Claim(
        "PRIM_ORBIT",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Admissible orbital actions U_g may act on algebra elements.",
    ),
    Claim(
        "DEF_SCALE_ORBIT_RESIDUAL",
        ClaimKind.DEFINITION,
        "The semantic-scale/orbital commutator residual measures order dependence of coarse-graining and orbital action.",
        ("PRIM_SCALE", "PRIM_ORBIT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_SCALE_PRODUCT_COHERENCE",
        ClaimKind.DEFINITION,
        "Semantic-product residual measures failure of S(X star Y) = S(X) star' S(Y).",
        ("PRIM_SCALE", "PRIM_PRODUCT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_SCALE_TRANSPORT_COHERENCE",
        ClaimKind.DEFINITION,
        "Semantic-transport residual measures failure of the coarse-graining/transport naturality square.",
        ("PRIM_SCALE", "PRIM_TRANSPORT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_ORBITAL_COHERENCE",
        ClaimKind.DEFINITION,
        "Orbital identity, inverse and composition residuals diagnose exact action-law coherence.",
        ("PRIM_ORBIT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_ORBIT_PRODUCT_COHERENCE",
        ClaimKind.DEFINITION,
        "Orbital-product residual measures failure of U(X star Y) = U(X) star' U(Y).",
        ("PRIM_ORBIT", "PRIM_PRODUCT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_ORBIT_TRANSPORT_COHERENCE",
        ClaimKind.DEFINITION,
        "Orbital-transport residual measures equivariance of typed transport under orbital operators.",
        ("PRIM_ORBIT", "PRIM_TRANSPORT", "PRIM_MODULE"),
    ),
    Claim(
        "DER_MOIRE",
        ClaimKind.DERIVED,
        "Moiré is the relative orbital action M_ij = U_i U_j^{-1} when the inverse exists.",
        ("PRIM_ORBIT",),
    ),
    Claim(
        "PRIM_REFINEMENT_MAP",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Typed branch refinement maps F_-/F_+ send level n sectors to selected child sectors at level n+1.",
        ("RR1", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_REFINEMENT_RESIDUAL",
        ClaimKind.DEFINITION,
        "Delta_F measures failure of exact product preservation under refinement.",
        ("PRIM_REFINEMENT_MAP", "PRIM_PRODUCT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_REFINEMENT_TRANSPORT_COHERENCE",
        ClaimKind.DEFINITION,
        "Refinement-transport residual measures failure of the naturality square between parent transport and child transport.",
        ("PRIM_REFINEMENT_MAP", "PRIM_TRANSPORT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_REFINEMENT_SCALE_COHERENCE",
        ClaimKind.DEFINITION,
        "Refinement-scale residual measures failure of refinement/coarse-graining naturality.",
        ("PRIM_REFINEMENT_MAP", "PRIM_SCALE", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_REFINEMENT_ORBIT_COHERENCE",
        ClaimKind.DEFINITION,
        "Refinement-orbit residual measures equivariance of branch refinement under orbital operators.",
        ("PRIM_REFINEMENT_MAP", "PRIM_ORBIT", "PRIM_MODULE"),
    ),
    Claim(
        "ZA_BRIDGE",
        ClaimKind.BRIDGE,
        "The companion Zero Axis model supplies Omega(s)=s/(1-s) and the critical-axis unit-circle equivalence.",
    ),
    Claim(
        "REF_HOLONOMY_U1",
        ClaimKind.REFERENCE_REALIZATION,
        "A concrete realization may supply a U(1) representation of closed value-level relational holonomy.",
        ("DER_HOLONOMY",),
    ),
    Claim(
        "REF_OCCURRENCE_HOLONOMY_U1",
        ClaimKind.REFERENCE_REALIZATION,
        "A concrete realization may independently supply a U(1) representation of occurrence-closed relational holonomy.",
        ("DER_OCCURRENCE_HOLONOMY",),
    ),
    Claim(
        "DER_OCCURRENCE_WINDING",
        ClaimKind.DERIVED,
        "Occurrence-level topological winding is derived only after occurrence-closed holonomy has an explicit U(1) phase representation.",
        ("REF_OCCURRENCE_HOLONOMY_U1",),
    ),
    Claim(
        "DER_BRANCH_BLIND_OCCURRENCE_PHASE",
        ClaimKind.DERIVED,
        "Composing a value-level U(1) holonomy representation with the occurrence-forgetful transport projection yields a branch-blind occurrence-level U(1) representation.",
        ("REF_HOLONOMY_U1", "REF_OCCURRENCE_HOLONOMY_U1", "DEF_OCCURRENCE_PATH"),
    ),
    Claim(
        "DER_WINDING",
        ClaimKind.DERIVED,
        "Topological winding is derived only after a closed value-level relational holonomy has an explicit U(1) phase representation.",
        ("REF_HOLONOMY_U1",),
    ),
    Claim(
        "REF_HOLONOMY_ZERO_AXIS",
        ClaimKind.REFERENCE_REALIZATION,
        "A verified finite U(1) holonomy phase may be lifted to the companion Zero Axis through Omega^{-1}.",
        ("REF_HOLONOMY_U1", "ZA_BRIDGE"),
    ),
    Claim(
        "DEF_RELATIONAL_CENTER_CHART",
        ClaimKind.DEFINITION,
        "A supplied normalized dual coordinate p in [0,1] may be centered by Z=2p-1, so p=1/2 is represented by relational coordinate Z=0.",
        ("DEF_BINARY_DISTINCTION",),
    ),
    Claim(
        "THM_RELATIONAL_CENTER_SELF_DUAL",
        ClaimKind.THEOREM,
        "Under the involution p->1-p in the normalized dual chart, Z=2p-1 changes sign and the unique fixed point is p=1/2 iff Z=0.",
        ("DEF_RELATIONAL_CENTER_CHART",),
    ),
    Claim(
        "BRIDGE_CENTER_HALF_TURN",
        ClaimKind.BRIDGE,
        "An explicit reference bridge may map the balanced relational coordinate p=1/2 to the normalized U(1) half-turn class q=1/2; RDSS does not infer this displacement solely from their equal numeric value.",
        ("THM_RELATIONAL_CENTER_SELF_DUAL", "REF_HOLONOMY_U1"),
    ),
    Claim(
        "REF_HILBERT_MOIRE_FIBRE",
        ClaimKind.REFERENCE_REALIZATION,
        "A finite Hilbert-Moire fibre chart may combine an occurrence address, orbital label, normalized U(1) phase and non-zero finite Hilbert vector; the abstract direct-integral carrier requires additional measure-theoretic data.",
        ("DEF_OCCURRENCE_ADDRESS_SPACE", "PRIM_ORBIT", "DER_MOIRE", "REF_HOLONOMY_U1"),
    ),
    Claim(
        "REF_KAPPA_MIXING_NORMALIZATION",
        ClaimKind.REFERENCE_REALIZATION,
        "The canonical project normalization uses the reference incidence count 3*(3^2-1)=24 and one normalized half-turn per channel, giving total normalized turn measure 12.",
        ("BRIDGE_CENTER_HALF_TURN",),
    ),
    Claim(
        "DER_KAPPA_NORMALIZED_TURN",
        ClaimKind.DERIVED,
        "With balanced binary information ln(2) and normalized turn measure 12, the normalized-turn information coefficient is kappa_q=ln(2)/12.",
        ("REF_KAPPA_MIXING_NORMALIZATION",),
    ),
    Claim(
        "DER_KAPPA_RADIAN_CHART",
        ClaimKind.DERIVED,
        "Under phi=2*pi*q, the information one-form kappa_q dq is represented by kappa_phi dphi with kappa_phi=ln(2)/(24*pi).",
        ("DER_KAPPA_NORMALIZED_TURN",),
    ),
    Claim(
        "BRIDGE_ORBITAL_COMPLEX_STRUCTURE",
        ClaimKind.BRIDGE,
        "If an oriented two-dimensional real inner-product carrier with compatible K satisfying K^2=-I is supplied, exp(phi K) realizes SO(2) congruent to U(1); derivation of that carrier structure from the minimal RDSS foundation remains open.",
        ("PRIM_ORBIT",),
    ),
    Claim(
        "DEF_CANONICAL_NORMAL_FORM",
        ClaimKind.DEFINITION,
        "A strict canonical normal form is an exact type-tagged finite key for an executable RDSS value together with separate non-authoritative reduction provenance; provenance is not part of strict key equality.",
    ),
    Claim(
        "DEF_REDUCTION_RELATION_KIND",
        ClaimKind.DEFINITION,
        "Every admitted canonical reduction rule declares its semantic relation kind explicitly: identity, exact equivalence, isomorphism, reference representation, forgetful projection, or approximation.",
        ("DEF_CANONICAL_NORMAL_FORM",),
    ),
    Claim(
        "DEF_REDUCTION_INFORMATION_EFFECT",
        ClaimKind.DEFINITION,
        "Every admitted canonical reduction rule declares its information effect as LOSSLESS, LOSSY, or UNKNOWN; a LOSSLESS rule requires an explicit inverse, while forgetful projection and approximation may not be labeled LOSSLESS.",
        ("DEF_REDUCTION_RELATION_KIND",),
    ),
    Claim(
        "DEF_REDUCTION_TRACE",
        ClaimKind.DEFINITION,
        "Canonical reduction records an ordered provenance trace containing rule identity, relation kind, information effect, preserved invariants, claim provenance, and before/after exact keys; competing applicable rules and reduction cycles fail closed.",
        ("DEF_REDUCTION_INFORMATION_EFFECT",),
    ),
    Claim(
        "THM_STRICT_NORMAL_FORM_IDEMPOTENCE",
        ClaimKind.THEOREM,
        "Applying strict canonical normalization to an already constructed CanonicalNormalForm returns that same normal form, so N(N(X))=N(X) by construction.",
        ("DEF_CANONICAL_NORMAL_FORM",),
    ),

    Claim(
        "DEF_RDSS_CANONICAL_SIGNATURE",
        ClaimKind.DEFINITION,
        "An executable RDSS object may expose a finite semantic signature whose axes are recorded separately from concrete representation, provenance, and strict object identity.",
        ("DEF_CANONICAL_NORMAL_FORM",),
    ),
    Claim(
        "DEF_SIGNATURE_AXIS_STRATIFICATION",
        ClaimKind.DEFINITION,
        "Canonical signatures separate structural axes (carrier, occurrence, relations, tensor rank, semantic scale, orbit and dimension) from state axes (phase and state payload), so a state change need not be promoted to a structural change.",
        ("DEF_RDSS_CANONICAL_SIGNATURE",),
    ),
    Claim(
        "DEF_SIGNATURE_COMPARISON",
        ClaimKind.DEFINITION,
        "Signature comparison distinguishes exact semantic signature, representation-only difference, same structure with different state, structural difference, and incomparable semantic families; incomparable families require an explicit bridge before stronger identification.",
        ("DEF_SIGNATURE_AXIS_STRATIFICATION",),
    ),
    Claim(
        "DEF_SIGNATURE_NOVELTY_CLASSIFICATION",
        ClaimKind.DEFINITION,
        "Relative novelty is classified from signature comparison as exact repeat, signature-equivalent redundancy, representation-only variant, new state, new structure, or new semantic family.",
        ("DEF_SIGNATURE_COMPARISON",),
    ),

    Claim(
        "DEF_SIGNATURE_CATALOG",
        ClaimKind.DEFINITION,
        "A signature catalog indexes admitted executable values simultaneously by semantic family, structural key, semantic-state key, and strict canonical payload without deleting source values; catalog novelty is evaluated relative to previously indexed records.",
        ("DEF_SIGNATURE_NOVELTY_CLASSIFICATION",),
    ),

    Claim(
        "DEF_LEXICOGRAPHIC_REDUCTION_ORDER",
        ClaimKind.DEFINITION,
        "A reduction ordering may be supplied by a fixed finite-dimensional measure mu:X->N^k with lexicographic order; every executable reduction step admitted under that order must strictly decrease mu.",
        ("DEF_REDUCTION_TRACE",),
    ),
    Claim(
        "THM_STRICT_LEX_DESCENT_TERMINATES",
        ClaimKind.THEOREM,
        "For fixed finite k, lexicographic order on N^k is well-founded; therefore any reduction sequence whose every step strictly decreases an admitted N^k measure is finite.",
        ("DEF_LEXICOGRAPHIC_REDUCTION_ORDER",),
    ),
    Claim(
        "DEF_FINITE_CONFLUENCE_AUDIT",
        ClaimKind.DEFINITION,
        "A bounded confluence audit explores every admitted reduction branch from a supplied start value up to a finite depth and reports unique normal form, multiple normal forms, detected cycle, or bounded incompleteness; this finite audit is not a general Church-Rosser theorem.",
        ("DEF_REDUCTION_TRACE",),
    ),

    Claim(
        "DEF_BRIDGE_REGISTRY",
        ClaimKind.DEFINITION,
        "An RDSS bridge registry is an explicit typed graph of legal transformations between semantic signature families; every bridge declares source/target families, relation kind, information effect, source/target checks, optional inverse, preserved invariants, and claim provenance.",
        ("DEF_SIGNATURE_COMPARISON", "DEF_REDUCTION_RELATION_KIND", "DEF_REDUCTION_INFORMATION_EFFECT"),
    ),
    Claim(
        "DEF_BRIDGE_ROUTE",
        ClaimKind.DEFINITION,
        "A bridge route is a finite composition of registered directed bridge edges; inverse edges exist only where an explicit inverse is supplied, and multiple distinct shortest routes fail closed as ambiguity.",
        ("DEF_BRIDGE_REGISTRY",),
    ),
    Claim(
        "DEF_BRIDGE_COMPARISON",
        ClaimKind.DEFINITION,
        "Bridge comparison first routes one value into the semantic family of the other and only then applies signature comparison; any LOSSY or UNKNOWN bridge route requires explicit opt-in.",
        ("DEF_BRIDGE_ROUTE", "DEF_SIGNATURE_COMPARISON"),
    ),
    Claim(
        "REF_OCCURRENCE_POINT_BRIDGE",
        ClaimKind.REFERENCE_REALIZATION,
        "The current binary reference realization supplies a reversible coordinate bridge between OccurrenceAddress omega in B* and RelationalPoint with the same binary coordinate word; this bridge is a reference representation and does not identify the two semantic sorts.",
        ("REF_RELATIONAL_POINT_BINARY_COORDINATE", "DEF_CARRIER_OCCURRENCE_SEPARATION", "DEF_BRIDGE_REGISTRY"),
    ),
    Claim(
        "THM_REFERENCE_COORDINATE_ROUNDTRIP",
        ClaimKind.THEOREM,
        "For the explicit binary reference bridge, converting an OccurrenceAddress to its RelationalPoint coordinate and extracting the binary address back returns the original occurrence word, and the reverse coordinate round trip returns the original RelationalPoint value.",
        ("REF_OCCURRENCE_POINT_BRIDGE",),
    ),

    Claim(
        "DEF_BRIDGE_EQUIVALENCE_GRAPH",
        ClaimKind.DEFINITION,
        "A finite bridge-aware equivalence graph has one record per source value, strong undirected equivalence edges generated only by same-family semantic-signature equivalence or fully reversible LOSSLESS bridge matches, and separate directed edges for LOSSY/UNKNOWN bridge matches.",
        ("DEF_BRIDGE_COMPARISON", "DEF_SIGNATURE_COMPARISON"),
    ),
    Claim(
        "DEF_BRIDGE_EQUIVALENCE_COMPONENT",
        ClaimKind.DEFINITION,
        "An equivalence component is a connected component generated only by strong signature-equivalence and fully reversible LOSSLESS bridge edges; it is equivalence under the selected bridge policy, not object identity.",
        ("DEF_BRIDGE_EQUIVALENCE_GRAPH",),
    ),
    Claim(
        "THM_LOSSY_BRIDGE_NONUNION",
        ClaimKind.THEOREM,
        "In the reference bridge-equivalence graph construction, LOSSY projection edges are recorded as directed edges and are never passed to the component-union operation, so a lossy bridge alone cannot collapse two equivalence components.",
        ("DEF_BRIDGE_EQUIVALENCE_COMPONENT",),
    ),

    Claim(
        "DEF_BRIDGE_GAP_REPORT",
        ClaimKind.DEFINITION,
        "A bridge-gap report groups unresolved cross-family record pairs by unordered semantic-family pair; it identifies missing explicit bridge coverage without asserting that a bridge exists or should exist.",
        ("DEF_BRIDGE_EQUIVALENCE_GRAPH",),
    ),

    Claim(
        "DEF_REFERENCE_CORPUS",
        ClaimKind.DEFINITION,
        "The RDSS reference corpus is a finite named collection of executable objects built only from current RDSS core, structural, reference-realization and bridge types; it intentionally includes both signature-supported values and existing values outside current signature coverage.",
        ("DEF_RDSS_CANONICAL_SIGNATURE",),
    ),
    Claim(
        "DEF_REFERENCE_CORPUS_SCAN",
        ClaimKind.DEFINITION,
        "A reference corpus scan partitions corpus items into signature-supported values and explicit coverage gaps, classifies supported values by catalog novelty, constructs their bridge-aware equivalence graph, and reports unresolved bridge gaps without treating unsupported values as false mathematical equivalences.",
        ("DEF_REFERENCE_CORPUS", "DEF_SIGNATURE_CATALOG", "DEF_BRIDGE_EQUIVALENCE_GRAPH", "DEF_BRIDGE_GAP_REPORT"),
    ),

    Claim(
        "REF_TYPED_ZERO_ELEMENT_BRIDGE",
        ClaimKind.REFERENCE_REALIZATION,
        "The reference kernel identifies TypedZero sector metadata with the all-zero TensorScalarElement in the same rank, carrier, semantic scale, and component dimension through an explicit reversible representation bridge restricted to the zero subspace.",
        ("DEF_TYPED_ZERO", "DEF_TS", "DEF_BRIDGE_REGISTRY"),
    ),
    Claim(
        "THM_TYPED_ZERO_ELEMENT_ROUNDTRIP",
        ClaimKind.THEOREM,
        "For the reference zero-sector bridge, TypedZero.as_element followed by TypedZero.from_element returns the original TypedZero, and the reverse round trip returns the original all-zero TensorScalarElement.",
        ("REF_TYPED_ZERO_ELEMENT_BRIDGE",),
    ),
    Claim(
        "DEF_RELATIONAL_DISTINCTION_FORGETFUL_PROJECTION",
        ClaimKind.DEFINITION,
        "The forgetful projection from RelationalBinaryDistinction to BinaryDistinction retains host and left/right endpoint labels while discarding explicit left/right relation labels.",
        ("DEF_RELATIONAL_DISTINCTION", "DEF_BINARY_DISTINCTION", "DEF_BRIDGE_REGISTRY"),
    ),

    Claim(
        "DEF_RELATIONAL_GENERATIVE_FORGETFUL_PROJECTION",
        ClaimKind.DEFINITION,
        "The executable projection RelationalGenerativeModel.as_ra0_star_model forgets explicit branch-relation labels while retaining the admitted carrier set and binary distinction host/endpoint structure, yielding a GenerativeRelationModel.",
        ("THM_RA0_STAR_FROM_RA0_REL_STAR", "DEF_BRIDGE_REGISTRY"),
    ),

    Claim(
        "DEF_BRIDGE_GAP_TRIAGE",
        ClaimKind.DEFINITION,
        "Bridge-gap triage classifies selected semantic-family relations conservatively as implemented lossless, implemented lossy, implemented contextual lossy, context-required, missing-intermediate-family, composite-not-equivalent, or no-bridge-claim, with claim provenance and without inferring new equivalences from similarity.",
        ("DEF_BRIDGE_GAP_REPORT", "DEF_BRIDGE_REGISTRY"),
    ),

    Claim(
        "REF_U1_PHASE_VALUE",
        ClaimKind.REFERENCE_REALIZATION,
        "A finite U(1) phase value may be represented explicitly by a normalized complex number u with |u|=1; the reference U1Phase type rejects zero, non-finite values, and values outside the unit circle tolerance.",
    ),
    Claim(
        "DEF_BRIDGE_ROUNDTRIP_VALIDATOR",
        ClaimKind.DEFINITION,
        "A LOSSLESS executable bridge uses strict canonical round-trip equality by default; a bridge may instead supply an explicit round-trip validator when its numerical representation is mathematically reversible but floating evaluation is not bitwise exact.",
        ("DEF_BRIDGE_REGISTRY",),
    ),
    Claim(
        "REF_U1_ZERO_AXIS_FINITE_BRIDGE",
        ClaimKind.REFERENCE_REALIZATION,
        "On the finite domain U(1) without u=-1, the projective map Omega^{-1}(u)=u/(1+u) and Omega(s)=s/(1-s) provide an explicit reversible bridge between U1Phase and finite ZeroAxisPoint values; u=-1 remains the compactified point at infinity.",
        ("REF_U1_PHASE_VALUE", "ZA_BRIDGE", "DEF_BRIDGE_ROUNDTRIP_VALIDATOR"),
    ),
    Claim(
        "THM_U1_ZERO_AXIS_FINITE_ROUNDTRIP",
        ClaimKind.THEOREM,
        "For finite admitted U1Phase and ZeroAxisPoint values, the explicit Omega/Omega^{-1} bridge returns the starting semantic value within its declared numerical round-trip tolerance; the exceptional phase u=-1 is outside the finite bridge domain.",
        ("REF_U1_ZERO_AXIS_FINITE_BRIDGE",),
    ),

    Claim(
        "DEF_CONTEXTUAL_BRIDGE_REGISTRY",
        ClaimKind.DEFINITION,
        "A contextual bridge registry stores transformations that are invalid without caller-supplied typed context; contextual bridges are kept separate from the global bridge registry so missing context cannot create implicit global equivalence edges.",
        ("DEF_BRIDGE_REGISTRY",),
    ),
    Claim(
        "DEF_CARRIER_MAP_CONTEXT",
        ClaimKind.DEFINITION,
        "CarrierMapContext is a finite explicit map from symbolic carrier labels to RelationalPoint values; the map is external contextual data and is not inferred from BranchRelationOccurrence identity.",
        ("DEF_POINT", "DEF_CONTEXTUAL_BRIDGE_REGISTRY"),
    ),
    Claim(
        "DEF_CONTEXTUAL_BRANCH_RELATION_MATERIALIZATION",
        ClaimKind.DEFINITION,
        "Given BranchRelationOccurrence and an explicit CarrierMapContext resolving its symbolic source and target labels, materialization yields the corresponding TypedRelation and forgets the branch occurrence slot; the transformation is therefore contextual and LOSSY.",
        ("DEF_RELATIONAL_DISTINCTION", "DEF_BINARY_REL", "DEF_CARRIER_MAP_CONTEXT"),
    ),
    Claim(
        "THM_CONTEXTUAL_BRANCH_SLOT_NONINJECTIVE",
        ClaimKind.THEOREM,
        "Two BranchRelationOccurrence values that differ only by branch slot but share relation label and symbolic endpoints materialize through the same CarrierMapContext to the same TypedRelation, so the contextual materialization is not injective on branch occurrences.",
        ("DEF_CONTEXTUAL_BRANCH_RELATION_MATERIALIZATION",),
    ),

    Claim(
        "DEF_EXECUTABLE_BRIDGE_INVARIANT",
        ClaimKind.DEFINITION,
        "An executable bridge invariant consists of named source and target projections plus an explicit comparator; bridge execution fails closed when any declared invariant comparator returns false.",
        ("DEF_BRIDGE_REGISTRY",),
    ),
    Claim(
        "THM_REFERENCE_BRIDGE_INVARIANT_ENFORCEMENT",
        ClaimKind.THEOREM,
        "In the reference BridgeRegistry implementation, every BridgeInvariant attached to a traversed edge is executed before the edge is admitted into the returned route; a failed invariant raises BridgeInvariantError and no BridgeStep is returned.",
        ("DEF_EXECUTABLE_BRIDGE_INVARIANT",),
    ),

    Claim(
        "DEF_EXECUTABLE_CONTEXTUAL_BRIDGE_INVARIANT",
        ClaimKind.DEFINITION,
        "An executable contextual bridge invariant consists of a named projection of source plus supplied context, a target projection, and an explicit comparator; contextual bridge execution fails closed when any declared invariant comparator returns false.",
        ("DEF_CONTEXTUAL_BRIDGE_REGISTRY", "DEF_EXECUTABLE_BRIDGE_INVARIANT"),
    ),
    Claim(
        "THM_REFERENCE_CONTEXTUAL_INVARIANT_ENFORCEMENT",
        ClaimKind.THEOREM,
        "In the reference ContextualBridgeRegistry implementation, every contextual invariant attached to the selected bridge is executed after target typing and before a ContextualBridgeStep is returned; failure raises ContextualBridgeInvariantError.",
        ("DEF_EXECUTABLE_CONTEXTUAL_BRIDGE_INVARIANT",),
    ),

    Claim(
        "DEF_REWRITE_RULE",
        ClaimKind.DEFINITION,
        "An RDSS rewrite rule is an explicitly oriented typed transformation with source and target semantic families, relation kind, information effect, executable invariants and claim provenance; orientation does not by itself declare a canonical representative.",
        ("DEF_EXECUTABLE_BRIDGE_INVARIANT", "DEF_REDUCTION_RELATION_KIND", "DEF_REDUCTION_INFORMATION_EFFECT"),
    ),
    Claim(
        "DEF_PRIORITY_FREE_REWRITE_SYSTEM",
        ClaimKind.DEFINITION,
        "A priority-free rewrite system is a finite set of named rewrite rules in which automatic stepping is admitted only when exactly one rule applies; multiple applicable rules fail closed as ambiguity rather than being resolved by registration order.",
        ("DEF_REWRITE_RULE",),
    ),
    Claim(
        "DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER",
        ClaimKind.DEFINITION,
        "The reference forgetful rewrite system orients each currently registered FORGETFUL_PROJECTION bridge in its declared forward direction and reuses the bridge information effect, executable invariants and claim provenance.",
        ("DEF_PRIORITY_FREE_REWRITE_SYSTEM", "DEF_BRIDGE_REGISTRY"),
    ),
    Claim(
        "THM_NO_IMPLICIT_REWRITE_PRIORITY",
        ClaimKind.THEOREM,
        "In the reference RewriteSystem, step(X) raises AmbiguousRewriteError whenever more than one registered rule applies to X; registration order therefore cannot select an automatic rewrite branch.",
        ("DEF_PRIORITY_FREE_REWRITE_SYSTEM",),
    ),
    Claim(
        "THM_REWRITE_CYCLE_FAIL_CLOSED",
        ClaimKind.THEOREM,
        "The reference automatic rewrite trace records semantic-family plus strict-value states and raises RewriteCycleError when a state repeats, so a detected cycle is not reported as an irreducible result.",
        ("DEF_PRIORITY_FREE_REWRITE_SYSTEM",),
    ),

    Claim(
        "DEF_FAMILY_RANK_TERMINATION_CERTIFICATE",
        ClaimKind.DEFINITION,
        "A family-rank termination certificate assigns non-negative integer ranks to semantic families and is valid for a rewrite system when every registered rule strictly decreases rank from its source family to its target family.",
        ("DEF_PRIORITY_FREE_REWRITE_SYSTEM",),
    ),
    Claim(
        "THM_STRICT_FAMILY_RANK_TERMINATION",
        ClaimKind.THEOREM,
        "If every step of an admitted rewrite system strictly decreases a non-negative integer family rank, no infinite rewrite trace exists because the natural numbers admit no infinite strictly descending chain.",
        ("DEF_FAMILY_RANK_TERMINATION_CERTIFICATE",),
    ),
    Claim(
        "REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE",
        ClaimKind.REFERENCE_REALIZATION,
        "The reference forgetful rewrite system assigns rank 1 to relation_occurrence, relational_generative_model, relational_binary_distinction and occurrence_relation_path, rank 0 to their four target families, and default rank 0 elsewhere.",
        ("DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER", "DEF_FAMILY_RANK_TERMINATION_CERTIFICATE"),
    ),
    Claim(
        "THM_REFERENCE_FORGETFUL_REWRITE_TERMINATES",
        ClaimKind.THEOREM,
        "Every automatic trace in the reference forgetful rewrite system terminates after at most one rewrite step because every applicable source family has rank 1 and every rule target has rank 0, where no reference forgetful rule originates.",
        ("REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE", "THM_STRICT_FAMILY_RANK_TERMINATION"),
    ),

    Claim(
        "DEF_RULE_SOURCE_FAMILY_OVERLAP_AUDIT",
        ClaimKind.DEFINITION,
        "A source-family overlap audit enumerates unordered pairs of registered rewrite rules whose declared source semantic family is the same; such pairs are candidate one-step overlaps, while distinct source families cannot both apply to one value because every value has one admitted signature family.",
        ("DEF_PRIORITY_FREE_REWRITE_SYSTEM", "DEF_RDSS_CANONICAL_SIGNATURE"),
    ),
    Claim(
        "DEF_DISTINCT_SOURCE_FAMILY_CONFLUENCE_CERTIFICATE",
        ClaimKind.DEFINITION,
        "A distinct-source-family confluence certificate is valid when the selected rewrite system has no pair of rules sharing a declared source semantic family.",
        ("DEF_RULE_SOURCE_FAMILY_OVERLAP_AUDIT",),
    ),
    Claim(
        "THM_DISTINCT_SOURCE_FAMILY_DETERMINISM",
        ClaimKind.THEOREM,
        "If a rewrite system has at most one registered rule for each semantic source family, then every admitted value has at most one immediate rewrite successor because its signature assigns exactly one source family.",
        ("DEF_DISTINCT_SOURCE_FAMILY_CONFLUENCE_CERTIFICATE",),
    ),
    Claim(
        "THM_DETERMINISTIC_REWRITE_CONFLUENCE",
        ClaimKind.THEOREM,
        "A deterministic rewrite relation is confluent: any two finite rewrite sequences from one source lie on the same unique successor orbit, so the shorter endpoint rewrites to the longer endpoint.",
        ("THM_DISTINCT_SOURCE_FAMILY_DETERMINISM",),
    ),
    Claim(
        "REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE",
        ClaimKind.REFERENCE_REALIZATION,
        "The four reference forgetful rewrite rules have pairwise distinct source families, so their source-family overlap audit is empty.",
        ("DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER", "DEF_DISTINCT_SOURCE_FAMILY_CONFLUENCE_CERTIFICATE"),
    ),
    Claim(
        "THM_REFERENCE_FORGETFUL_REWRITE_CONFLUENT",
        ClaimKind.THEOREM,
        "The reference forgetful rewrite relation is confluent because its distinct-source-family certificate makes the relation deterministic.",
        ("REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE", "THM_DETERMINISTIC_REWRITE_CONFLUENCE"),
    ),
    Claim(
        "THM_TERMINATING_CONFLUENT_UNIQUE_IRREDUCIBLE",
        ClaimKind.THEOREM,
        "For a rewrite system that is terminating and confluent, every admitted starting value reaches a unique irreducible result under that selected system.",
        ("THM_STRICT_FAMILY_RANK_TERMINATION", "THM_DETERMINISTIC_REWRITE_CONFLUENCE"),
    ),
    Claim(
        "THM_REFERENCE_FORGETFUL_UNIQUE_IRREDUCIBLE",
        ClaimKind.THEOREM,
        "Combining the reference forgetful termination and confluence certificates gives each admitted value a unique irreducible result under the selected forgetful rewrite system; this is not promoted to a global RDSS canonical normal form.",
        ("THM_REFERENCE_FORGETFUL_REWRITE_TERMINATES", "THM_REFERENCE_FORGETFUL_REWRITE_CONFLUENT", "THM_TERMINATING_CONFLUENT_UNIQUE_IRREDUCIBLE"),
    ),

    Claim(
        "DEF_SCOPED_REWRITE_NORMAL_FORM",
        ClaimKind.DEFINITION,
        "A scoped rewrite normal form is the unique irreducible result produced by one explicitly named rewrite system together with explicit termination and confluence certificates; the scope name and certificate provenance are part of the result and no global canonicality is implied.",
        ("THM_TERMINATING_CONFLUENT_UNIQUE_IRREDUCIBLE",),
    ),
    Claim(
        "REF_FORGETFUL_SCOPED_NORMAL_FORM",
        ClaimKind.REFERENCE_REALIZATION,
        "The reference forgetful scoped normal form uses the rdss-reference-forgetful-v1 rewrite system, its family-rank termination certificate and its distinct-source-family confluence certificate; rewritten results may be LOSSY.",
        ("DEF_SCOPED_REWRITE_NORMAL_FORM", "REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE", "REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE"),
    ),
    Claim(
        "THM_REFERENCE_FORGETFUL_NORMAL_FORM_IDEMPOTENT",
        ClaimKind.THEOREM,
        "Applying the reference forgetful scoped normal-form function to its own result performs no further rewrite and returns the same strict target key, because the first result is irreducible under the selected system.",
        ("REF_FORGETFUL_SCOPED_NORMAL_FORM", "THM_REFERENCE_FORGETFUL_UNIQUE_IRREDUCIBLE"),
    ),

    Claim(
        "DEF_SEMANTIC_FACTORIZATION",
        ClaimKind.DEFINITION,
        "The semantic factorization of an admitted RDSS value is the tuple (F,S,sigma,rho) obtained from its existing RDSSSignature, where F is semantic family, S is the structural key built from non-state axes, sigma is the state key built from PHASE/STATE axes, and rho is the concrete representation tag.",
        ("DEF_RDSS_CANONICAL_SIGNATURE", "DEF_SIGNATURE_AXIS_STRATIFICATION"),
    ),
    Claim(
        "THM_FACTORIZATION_RECONSTRUCTS_SEMANTIC_KEY",
        ClaimKind.THEOREM,
        "For every admitted RDSSSignature, the semantic factorization preserves the original structural key, state key and semantic key exactly; it is a view of the existing signature rather than a new semantic quotient.",
        ("DEF_SEMANTIC_FACTORIZATION",),
    ),
    Claim(
        "DEF_FACTORIZATION_COMPARISON",
        ClaimKind.DEFINITION,
        "Factorization comparison classifies two admitted values by family equality, then structural-key equality, then state-key equality, then representation equality, yielding DIFFERENT_FAMILY, DIFFERENT_STRUCTURE, DIFFERENT_STATE, REPRESENTATION_ONLY or SAME_FACTORIZATION.",
        ("DEF_SEMANTIC_FACTORIZATION",),
    ),
    Claim(
        "REF_REFERENCE_CORPUS_FACTORIZATION_SUMMARY",
        ClaimKind.REFERENCE_REALIZATION,
        "The current 36-record reference corpus source contract factors into 22 semantic families, 28 structural keys, 34 semantic-state keys and 22 representation classes.",
        ("DEF_REFERENCE_CORPUS", "DEF_SEMANTIC_FACTORIZATION"),
    ),

    Claim(
        "DEF_CLAIM_DEPENDENCY_PROJECTION",
        ClaimKind.DEFINITION,
        "A claim dependency projection takes an explicit set of existing root claim IDs and returns the induced dependency subgraph of the authoritative RDSS claim ledger; it does not create, promote or rewrite claims.",
        ("DEF_RDSS_CANONICAL_SIGNATURE",),
    ),
    Claim(
        "THM_PROVENANCE_TOPOLOGICAL_ORDER",
        ClaimKind.THEOREM,
        "The reference claim-dependency projection emits a topological ordering in which every included dependency appears before every included claim that depends on it.",
        ("DEF_CLAIM_DEPENDENCY_PROJECTION",),
    ),
    Claim(
        "DEF_VALUE_CLAIM_PROVENANCE",
        ClaimKind.DEFINITION,
        "Value claim provenance combines one admitted value's semantic factorization, signature-extractor provenance, signature root claim IDs and the induced claim dependency graph.",
        ("DEF_CLAIM_DEPENDENCY_PROJECTION", "DEF_SEMANTIC_FACTORIZATION", "DEF_RDSS_CANONICAL_SIGNATURE"),
    ),
    Claim(
        "DEF_TRANSFORMATION_CLAIM_PROVENANCE",
        ClaimKind.DEFINITION,
        "Transformation claim provenance expands the explicit root claim IDs carried by a BridgeRoute, RewriteTrace or ScopedRewriteNormalForm into the induced authoritative claim dependency graph.",
        ("DEF_CLAIM_DEPENDENCY_PROJECTION", "DEF_BRIDGE_ROUTE", "DEF_PRIORITY_FREE_REWRITE_SYSTEM", "DEF_SCOPED_REWRITE_NORMAL_FORM"),
    ),

    Claim(
        "DEF_OBJECT_REDUCTION_CERTIFICATE",
        ClaimKind.DEFINITION,
        "An object-level reduction certificate binds one input value's value provenance, certified rewrite trace, scoped normal form, target value provenance, verified rewrite invariants, explicit termination/confluence certificate identities and the induced claim dependency graph into one auditable scoped result.",
        ("DEF_VALUE_CLAIM_PROVENANCE", "DEF_TRANSFORMATION_CLAIM_PROVENANCE", "DEF_SCOPED_REWRITE_NORMAL_FORM", "DEF_EXECUTABLE_BRIDGE_INVARIANT"),
    ),
    Claim(
        "REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE",
        ClaimKind.REFERENCE_REALIZATION,
        "The reference forgetful object reduction certificate uses the rdss-reference-forgetful-v1 rewrite system together with its family-rank termination certificate, distinct-source-family confluence certificate, scoped forgetful normal form and read-only claim provenance graph; global canonicality is explicitly false.",
        ("DEF_OBJECT_REDUCTION_CERTIFICATE", "REF_FORGETFUL_SCOPED_NORMAL_FORM", "REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE", "REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE"),
    ),
    Claim(
        "THM_REFERENCE_OBJECT_REDUCTION_CERTIFICATE_CONSISTENT",
        ClaimKind.THEOREM,
        "The reference certificate factory returns only after checking agreement of strict source/target keys, full source/target value provenance, rewrite provenance, scoped-normal-form provenance, termination/confluence certificate identities, lossiness, target irreducibility, scoped-normal-form idempotence, verified invariant inventory and the complete authoritative claim dependency projection; any disagreement raises ReductionCertificateError.",
        ("REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE", "THM_REFERENCE_FORGETFUL_NORMAL_FORM_IDEMPOTENT", "THM_PROVENANCE_TOPOLOGICAL_ORDER"),
    ),

    Claim(
        "DEF_REFERENCE_REDUCTION_CERTIFICATE_SCAN",
        ClaimKind.DEFINITION,
        "The reference reduction-certificate scan applies the reference forgetful object certificate factory independently to every named value in the finite RDSS reference corpus and aggregates verification, rewrite, fixed-point, lossiness and family-count diagnostics without changing any certificate.",
        ("DEF_REFERENCE_CORPUS", "DEF_OBJECT_REDUCTION_CERTIFICATE"),
    ),
    Claim(
        "REF_REFERENCE_REDUCTION_CERTIFICATE_SCAN",
        ClaimKind.REFERENCE_REALIZATION,
        "The current 36-record reference corpus source contract expects 36 verified object certificates, 5 rewritten values, 31 fixed points, 5 LOSSY reductions, zero global-canonical results, 22 distinct source families and 18 distinct target families after the selected forgetful reduction.",
        ("DEF_REFERENCE_REDUCTION_CERTIFICATE_SCAN", "REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE"),
    ),

    Claim(
        "DEF_LOSS_WITNESS",
        ClaimKind.DEFINITION,
        "A rewrite loss witness consists of two strict-unequal source values in one rewrite source family that are transformed by the same declared LOSSY rule to strict-equal target values, with executable invariant evidence and an irreducible target.",
        ("DEF_REWRITE_RULE", "DEF_EXECUTABLE_BRIDGE_INVARIANT"),
    ),
    Claim(
        "REF_FORGETFUL_LOSS_WITNESSES",
        ClaimKind.REFERENCE_REALIZATION,
        "The reference forgetful rewrite system contains one executable loss witness for each of its four rules: relation-occurrence forgetting, occurrence-path forgetting, relational-distinction binding forgetting and relational-generative binding forgetting.",
        ("DEF_LOSS_WITNESS", "DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER"),
    ),
    Claim(
        "THM_REFERENCE_FORGETFUL_REWRITES_NONINJECTIVE",
        ClaimKind.THEOREM,
        "Each of the four reference forgetful rewrite rules is noninjective on its source family because an explicit witness pair X!=Y is mapped by that rule to one strict-equal target; therefore none of those rules admits a two-sided inverse on the full source family and the LOSSY classification is independently witnessed.",
        ("REF_FORGETFUL_LOSS_WITNESSES",),
    ),

    Claim(
        "DEF_CP1_PROJECTIVE_EQUIVALENCE",
        ClaimKind.DEFINITION,
        "For nonzero complex two-component representatives psi=(alpha,beta) and phi=(gamma,delta), CP1 projective equivalence is psi~phi iff there exists lambda!=0 with phi=lambda psi; equivalently alpha*delta-beta*gamma=0. For normalized representatives, every such lambda has unit modulus and is a global phase.",
    ),
    Claim(
        "THM_CP1_GLOBAL_PHASE_QUOTIENT",
        ClaimKind.THEOREM,
        "Multiplying a normalized CP1 representative by one common U(1) phase leaves its projective equivalence class unchanged, while projectively distinct normalized representatives have nonzero Fubini-Study separation.",
        ("DEF_CP1_PROJECTIVE_EQUIVALENCE", "REF_U1_PHASE_VALUE"),
    ),
    Claim(
        "REF_CP1_PROJECTIVE_CHART_QUOTIENT",
        ClaimKind.REFERENCE_REALIZATION,
        "The reference CP1 quotient selects the larger-magnitude amplitude as a stable chart pivot and stores the phase-invariant ratio of the other amplitude to that pivot; numerical equivalence requires both determinant and chart-coordinate residuals to lie within an explicit tolerance, while Fubini-Study distance is retained as an independent diagnostic.",
        ("DEF_CP1_PROJECTIVE_EQUIVALENCE",),
    ),
    Claim(
        "REF_REFERENCE_CORPUS_CP1_PROJECTIVE_QUOTIENT",
        ClaimKind.REFERENCE_REALIZATION,
        "The current reference corpus contains three raw CP1State representatives but two projective classes: cp1-north and cp1-north-global-phase collapse to one CP1 point while cp1-south remains distinct.",
        ("DEF_REFERENCE_CORPUS", "REF_CP1_PROJECTIVE_CHART_QUOTIENT"),
    ),

    Claim(
        "DEF_STATIC_CUBIC_FRAME",
        ClaimKind.DEFINITION,
        "The local static cage is the canonical cube with eight vertices (±1,±1,±1) and six faces; its support geometry remains fixed while local tetrahedral state variables change.",
        ("DEF_POINT",),
    ),
    Claim(
        "BRIDGE_TIR_EULER_BERRY_SPIN_HALF_POLARIZATION",
        ClaimKind.BRIDGE,
        "Read-only TIR provenance bridge for the Euler-Berry closure already represented inside RDSS by THM_EULER_BERRY_MINIMAL_SPIN_HALF, including 2*pi sign return, 4*pi full return and closure of the spin polarization pair onto the relational poles. This does not assert a universal physical spin assignment.",
        ("THM_EULER_BERRY_MINIMAL_SPIN_HALF",),
    ),
    Claim(
        "DEF_STELLA_CUBIC_VERTEX_PARTITION",
        ClaimKind.DEFINITION,
        "The eight vertices of the static cube are partitioned into two complementary four-vertex supports by the parity sign xyz=+1 and xyz=-1; the supports are disjoint and exhaust the cube vertices.",
        ("DEF_STATIC_CUBIC_FRAME",),
    ),
    Claim(
        "DEF_DYNAMIC_TETRAHEDRAL_PAIR",
        ClaimKind.DEFINITION,
        "The local dynamic sector is a pair of opposite-polarization spin-1/2 states carried by the two fixed tetrahedral supports of the cubic vertex partition. Dynamics affect U(1) phase and angular state, not the static support vertices.",
        ("DEF_STELLA_CUBIC_VERTEX_PARTITION", "BRIDGE_TIR_EULER_BERRY_SPIN_HALF_POLARIZATION"),
    ),
    Claim(
        "REF_STELLA_OCTANGULA_CUBIC_EMBEDDING",
        ClaimKind.REFERENCE_REALIZATION,
        "In the canonical cube embedding, each parity support is a regular tetrahedron, the two supports are oppositely oriented, and their union uses exactly all eight cube vertices, giving the standard Stella Octangula compound.",
        ("DEF_STELLA_CUBIC_VERTEX_PARTITION", "DEF_DYNAMIC_TETRAHEDRAL_PAIR"),
    ),
    Claim(
        "REF_OCTAHEDRAL_RELATIONAL_CORE",
        ClaimKind.REFERENCE_REALIZATION,
        "In the standard Stella Octangula cubic embedding, the common central intersection is the regular octahedron with vertices (±1,0,0), (0,±1,0), and (0,0,±1); this is the internal relational core, not the external static cage.",
        ("REF_STELLA_OCTANGULA_CUBIC_EMBEDDING",),
    ),
    Claim(
        "DEF_CUBIC_FACE_ADJACENCY_COMPLEX",
        ClaimKind.DEFINITION,
        "A static cubic cell complex is a set of fixed cubic frames joined by one-to-one face adjacencies. Local dynamic tetrahedral states do not move the shared cubic faces.",
        ("DEF_STATIC_CUBIC_FRAME",),
    ),
    Claim(
        "REF_ALGEBRAIC_GEOMETRIC_INFORMATION_CELL",
        ClaimKind.REFERENCE_REALIZATION,
        "The executable algebraic-geometric information cell combines one static cubic frame, the complementary Stella tetrahedral pair, the internal octahedral relational core, and the canonical information action kappa=ln(2)/(24*pi).",
        ("DEF_DYNAMIC_TETRAHEDRAL_PAIR", "REF_OCTAHEDRAL_RELATIONAL_CORE", "DEF_CUBIC_FACE_ADJACENCY_COMPLEX", "DER_KAPPA_RADIAN_CHART"),
    ),
    Claim(
        "DEF_CUBIC_FACE_FRAME_TRANSPORT",
        ClaimKind.DEFINITION,
        "A glued cubic face carries an explicit right-to-left signed-permutation frame transport. The transport maps the source cube to the target cube and must map the declared right face exactly onto the declared left face.",
        ("DEF_CUBIC_FACE_ADJACENCY_COMPLEX",),
    ),
    Claim(
        "DER_STELLA_SECTOR_TRANSPORT",
        ClaimKind.DERIVED,
        "For the cubic Stella partition xyz=+/-1, a signed-permutation face transport acts on the tetrahedral sector by the character eta=product(signs): eta=+1 preserves T+ and T-, while eta=-1 exchanges them.",
        ("DEF_STELLA_CUBIC_VERTEX_PARTITION", "DEF_CUBIC_FACE_FRAME_TRANSPORT"),
    ),
    Claim(
        "DEF_STELLA_RELATIVE_STATE",
        ClaimKind.DEFINITION,
        "The gauge-reduced local Stella state is the relative U(1) phase delta=U+ U-^{-1} together with the within-cell angular offset theta+ - theta-. A common U(1) phase shift of both sectors leaves delta invariant.",
        ("DEF_DYNAMIC_TETRAHEDRAL_PAIR", "REF_U1_PHASE_VALUE"),
    ),
    Claim(
        "DER_CELL_RELATIVE_STATE_TO_MOIRE",
        ClaimKind.DERIVED,
        "For an oriented glued face e=(n,m) with Stella-sector character eta, the phase-edge mismatch is Xi_e=delta_n delta_m^{-eta}. The construction is relational and gauge-reduced and introduces no time-evolution or interaction-energy law.",
        ("DEF_CUBIC_FACE_FRAME_TRANSPORT", "DER_STELLA_SECTOR_TRANSPORT", "DEF_STELLA_RELATIVE_STATE", "DER_MOIRE"),
    ),
    Claim(
        "GATE_MOIRE_DYNAMICAL_LAW",
        ClaimKind.DERIVATION_GATE,
        "A dynamical neighbour-coupling law, interaction energy, continuum field equation, or physical identification of the edge mismatch is not inferred from the geometric Moire edge state and remains an explicit downstream derivation gate.",
        ("DER_CELL_RELATIVE_STATE_TO_MOIRE",),
    ),

    Claim(
        "DEF_OFHM_COUNTABLE_BRANCH_ADDRESS",
        ClaimKind.DEFINITION,
        "The general orbital-fractal symbolic address carrier is the set of finite integer words Z^{<omega}. Existing binary RDSS occurrence words embed by preserving each -1/+1 branch symbol. The symbolic address is not by itself a claim of convergence to a geometric fractal point.",
    ),
    Claim(
        "BRIDGE_OFHM_EULER_SYMBOLIC_BRANCH_SPACE",
        ClaimKind.BRIDGE,
        "Source bridge from Infinities@339d6c58 research/EULERS_INFINITY_V0_1.md: the Euler phase map E(z)=exp(i*pi*z) has countably many declared-Log inverse branches E_k^{-1}(w)=2k-(i/pi)Log(w), giving finite integer branch words and an exact symbolic infinite-address space while leaving geometric convergence and fractal dimension open.",
        ("DEF_OFHM_COUNTABLE_BRANCH_ADDRESS",),
    ),
    Claim(
        "BRIDGE_OFHM_HILBERT_HOTEL_SHIFT",
        ClaimKind.BRIDGE,
        "Source bridge from Infinities@339d6c58 research/TIR_E6_FOURIER_HILBERT_HOTEL_CORE_V0_1.md: the countable address carrier admits a Hilbert-Hotel successor under an explicit enumeration rho:Z^{<omega}<->N, while the imported stable Hilbert-Hotel/Fredholm sector carries index +1. This stabilization shift is distinct from local branch refinement.",
        ("DEF_OFHM_COUNTABLE_BRANCH_ADDRESS",),
    ),
    Claim(
        "DER_OFHM_SYMBOLIC_FRACTAL_BOUNDARY",
        ClaimKind.DERIVED,
        "The OFHM symbolic fractal-boundary algebra is the combination of the Euler integer-branch symbolic space with the Hilbert-Hotel countable enumeration/shift: (Z^{<omega}, R_k, S_HH). It is a symbolic/operator boundary and does not assert convergence of every infinite address to a geometric point.",
        (
            "BRIDGE_OFHM_EULER_SYMBOLIC_BRANCH_SPACE",
            "BRIDGE_OFHM_HILBERT_HOTEL_SHIFT",
        ),
    ),
    Claim(
        "BRIDGE_OFHM_BEES_RELATIVE_PHASE_COHERENCE",
        ClaimKind.BRIDGE,
        "Source bridge from GREMLIN@b0000828 spec/GREMLIN_HOLOGRAPHIC_ORBITAL_MEMORY_V0_1.md: local finite phase states may be compared by dimension-independent relative-phase coherence C=|d^{-1} sum_j exp(i(theta_j^X-theta_j^Y))|. The observable measures compatibility/coherence and does not establish truth or canon authority.",
        ("DER_MOIRE",),
    ),
    Claim(
        "DER_OFHM_MOIRE_COCYCLE",
        ClaimKind.DERIVED,
        "For scalar orbital phases the relative Moire phase M_ij=U_i U_j^{-1}=exp(i(theta_i-theta_j)) obeys M_ij M_jk=M_ik, M_ii=1 and M_ji=M_ij^{-1}.",
        ("BRIDGE_OFHM_BEES_RELATIVE_PHASE_COHERENCE",),
    ),
    Claim(
        "DER_OFHM_HILBERT_TRANSPORT",
        ClaimKind.DERIVED,
        "Multiplication of a finite Hilbert-fibre vector by the relative Moire phase defines transport T_ij v=M_ij v. Because M_ij lies in U(1), the transport preserves Hilbert norm and composes as T_ij T_jk=T_ik.",
        ("DER_OFHM_MOIRE_COCYCLE", "REF_HILBERT_MOIRE_FIBRE"),
    ),
    Claim(
        "DEF_OFHM_STATE",
        ClaimKind.DEFINITION,
        "A finite orbital-fractal Hilbert-Moire state is Psi=(a,l,theta,v,omega), where a is a finite countable branch address, l is an orbital label, theta is a U(1) angle, v is a non-zero finite Hilbert vector and omega is an optional angular-velocity coordinate for the second-order dynamics chart.",
        ("DEF_OFHM_COUNTABLE_BRANCH_ADDRESS", "DER_OFHM_HILBERT_TRANSPORT"),
    ),
    Claim(
        "BRIDGE_OFHM_BEES_IDT_DYNAMICS",
        ClaimKind.BRIDGE,
        "Source bridge from GREMLIN@b0000828 and Informational-Dynamics-of-Metatime@31f1a74d: the local sine-coupling current J_i=sum_j w_ij sin(theta_j-theta_i) supports both the normalized first-order BEES/Kuramoto reduction and the IDT second-order update theta'=theta+dt*omega, omega'=omega+dt*(-dV/dtheta-eta*omega+K*J+drive). This is a relational dynamics realization, not a physical-law claim.",
        ("DEF_OFHM_STATE",),
    ),
    Claim(
        "DER_OFHM_GENERAL_ALGEBRA",
        ClaimKind.DERIVED,
        "The general source-grounded orbital-fractal Hilbert-Moire algebra is the typed structure (A_F,rho,S_HH,R_k,M,H,T,J,D): finite symbolic address space, countable Hilbert-Hotel ranking/shift, local refinement, relative Moire cocycle, Hilbert fibres, norm-preserving transport, local coupling current and selected first- or second-order relational phase dynamics.",
        (
            "DER_OFHM_SYMBOLIC_FRACTAL_BOUNDARY",
            "DER_OFHM_MOIRE_COCYCLE",
            "DER_OFHM_HILBERT_TRANSPORT",
            "BRIDGE_OFHM_BEES_IDT_DYNAMICS",
        ),
    ),
    Claim(
        "GATE_OFHM_GEOMETRIC_FRACTAL_LIMIT",
        ClaimKind.DERIVATION_GATE,
        "The finite symbolic OFHM algebra does not imply convergence of every infinite branch address, a canonical geometric limit set, a Hausdorff dimension or a unique continuum measure. Each stronger geometric-fractal statement requires a separate derivation.",
        ("DER_OFHM_GENERAL_ALGEBRA",),
    ),
    Claim(
        "GATE_OFHM_PHYSICAL_BINDING",
        ClaimKind.DERIVATION_GATE,
        "No specific material, quantum, spacetime or other physical substrate is identified solely by the OFHM algebra or its source bridges; physical binding and parameter calibration remain separate evidence-bearing derivation tasks.",
        ("DER_OFHM_GENERAL_ALGEBRA",),
    ),

)


def claim_map() -> dict[str, Claim]:
    return {claim.id: claim for claim in CLAIMS}


def dependency_closure(claim_id: str) -> frozenset[str]:
    claims = claim_map()
    if claim_id not in claims:
        raise KeyError(claim_id)

    seen: set[str] = set()
    stack = list(claims[claim_id].depends_on)
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        if current not in claims:
            raise KeyError(f"unknown dependency: {current}")
        seen.add(current)
        stack.extend(claims[current].depends_on)
    return frozenset(seen)


def validate_dependency_dag() -> None:
    claims = claim_map()
    if len(claims) != len(CLAIMS):
        raise ValueError("claim ids must be unique")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise ValueError(f"dependency cycle at {node}")
        if node in visited:
            return
        visiting.add(node)
        for dep in claims[node].depends_on:
            if dep not in claims:
                raise ValueError(f"unknown dependency {dep!r} in {node}")
            visit(dep)
        visiting.remove(node)
        visited.add(node)

    for node in claims:
        visit(node)


def foundational_laws() -> tuple[Claim, ...]:
    return tuple(
        claim for claim in CLAIMS if claim.kind is ClaimKind.FOUNDATIONAL_LAW
    )


def foundational_axioms() -> tuple[Claim, ...]:
    """Backward-compatible alias for callers written before the law migration."""

    return foundational_laws()



def formation_rules() -> tuple[Claim, ...]:
    return tuple(
        claim for claim in CLAIMS if claim.kind is ClaimKind.FORMATION_RULE
    )
