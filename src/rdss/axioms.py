from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ClaimKind(str, Enum):
    AXIOM = "axiom"
    DEFINITION = "definition"
    STRUCTURAL_PRIMITIVE = "structural_primitive"
    REFERENCE_REALIZATION = "reference_realization"
    DERIVED = "derived"
    BRIDGE = "bridge"
    CANDIDATE_AXIOM = "candidate_axiom"
    THEOREM = "theorem"
    FORMATION_RULE = "formation_rule"


@dataclass(frozen=True)
class Claim:
    id: str
    kind: ClaimKind
    statement: str
    depends_on: tuple[str, ...] = ()


CLAIMS: tuple[Claim, ...] = (
    Claim(
        "META0",
        ClaimKind.FORMATION_RULE,
        "Non-reification/non-vacuity rule: absolute nothingness has no denotation in the RTOFA object language, and admissible RTOFA models have a non-empty admitted carrier domain.",
    ),
    Claim(
        "EX0",
        ClaimKind.THEOREM,
        "Model non-vacuity: every admissible RTOFA model contains at least one admitted relational carrier.",
        ("META0",),
    ),
    Claim(
        "RA0",
        ClaimKind.AXIOM,
        "Relational admissibility: every admitted observable is incident to at least one primitive relation, as source or target.",
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
        ClaimKind.AXIOM,
        "Recursive relational closure: at every admitted path-labelled occurrence, a selected endpoint may itself carry a further non-degenerate binary distinction, so the rule re-applies at each finite refinement depth.",
        ("DEF_POINT", "DEF_BINARY_DISTINCTION"),
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
        "A minimal complex binary distinction may be represented by two projectively distinct CP^1 states with Fubini-Study metric.",
        ("DEF_POINT", "DEF_BINARY_DISTINCTION"),
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
        ClaimKind.CANDIDATE_AXIOM,
        "Every admitted carrier hosts an admitted non-degenerate binary distinction whose endpoint occurrences are admitted carriers.",
        ("DEF_POINT", "DEF_BINARY_DISTINCTION"),
    ),
    Claim(
        "RA0_REL_STAR",
        ClaimKind.CANDIDATE_AXIOM,
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


def foundational_axioms() -> tuple[Claim, ...]:
    return tuple(claim for claim in CLAIMS if claim.kind is ClaimKind.AXIOM)



def formation_rules() -> tuple[Claim, ...]:
    return tuple(
        claim for claim in CLAIMS if claim.kind is ClaimKind.FORMATION_RULE
    )
