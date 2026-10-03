"""Machine-readable provenance for canonical RDSS/RTOFA results.

This module exists so future edits do not depend on chat memory.

Canonical contract:
    docs/CANONICAL_FOUNDATIONAL_CONTRACT.md

The authoritative theorem dependency graph remains src/rdss/axioms.py.
This module is a citation/provenance index, not a second claim ledger.
"""

from __future__ import annotations

from dataclasses import dataclass


CANONICAL_FOUNDATIONAL_CONTRACT = "docs/CANONICAL_FOUNDATIONAL_CONTRACT.md"


@dataclass(frozen=True)
class ProvenanceNote:
    surface: str
    role: str
    claim_ids: tuple[str, ...]
    sources: tuple[str, ...]
    note: str


FOUNDATIONAL_PROVENANCE: tuple[ProvenanceNote, ...] = (
    ProvenanceNote(
        surface="First Law of Existence",
        role="FOUNDATIONAL_LAW",
        claim_ids=("A0",),
        sources=(CANONICAL_FOUNDATIONAL_CONTRACT,),
        note=(
            "Canonical author-defined name. A0 is the legacy executable identifier. "
            "Descriptive phrases such as 'law of reality' are not aliases."
        ),
    ),
    ProvenanceNote(
        surface="carrier/occurrence separation",
        role="DEF+REFERENCE",
        claim_ids=(
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_RELATIONAL_DISTINCTION",
            "REF_META0_SINGLETON_POINT_PRESENTATION",
        ),
        sources=(CANONICAL_FOUNDATIONAL_CONTRACT,),
        note="Distinct occurrences may share one singleton carrier.",
    ),
    ProvenanceNote(
        surface="First Hamlet persistence dichotomy",
        role="DEF+THM+BRIDGE",
        claim_ids=(
            "DEF_DISTINCTION_PERSISTENCE_PREDICATE",
            "THM_FIRST_HAMLET_DISPERSION_STRUCTURE",
            "GATE_FIRST_HAMLET_NONDEGENERACY_FROM_PE_I0",
        ),
        sources=(CANONICAL_FOUNDATIONAL_CONTRACT,),
        note=(
            "DISPERSION/STRUCTURE classify persistence and are not the durable "
            "N/S projective carrier. Physical realization of both regimes is an "
            "optional downstream bridge, not an upstream foundational gate."
        ),
    ),
    ProvenanceNote(
        surface="non-circular relational root typing",
        role="BRIDGE+PROOF_HYGIENE",
        claim_ids=(
            "BRIDGE_TIR_RELATIONAL_EXISTENCE_TYPING",
            "RA0",
        ),
        sources=(
            CANONICAL_FOUNDATIONAL_CONTRACT,
            "TIR@9783782570a2ccfa1fc42c99b605dad48e02aa78:"
            "TIR/foundations/TIR_CANONICAL_DERIVATION_SPINE_V0_1.md",
        ),
        note=(
            "TIR relational existence typing Exist(x)->exists R_x is a proof parent "
            "of the First Law contradiction. RA0 is therefore imported as root typing "
            "rather than derived from A0, avoiding a circular dependency."
        ),
    ),
    ProvenanceNote(
        surface="relational generativity gate basis",
        role="THM+GATE",
        claim_ids=(
            "THM_CANONICAL_ROOT_LOCAL_RA0_REL_STAR",
            "RA0_REL_STAR",
            "THM_RA0_STAR_FROM_RA0_REL_STAR",
            "THM_RR1_FROM_RA0_REL_STAR",
            "RA0_STAR",
            "RR1",
        ),
        sources=(CANONICAL_FOUNDATIONAL_CONTRACT,),
        note=(
            "Local RA0_REL_STAR is closed at the canonical root. Global RA0_REL_STAR "
            "is the strongest unresolved generativity target and, if closed, discharges "
            "the weaker RA0_STAR and RR1 obligations."
        ),
    ),
    ProvenanceNote(
        surface="durable relation roles",
        role="BRIDGE+THM",
        claim_ids=(
            "BRIDGE_TIR_MIN_NONTRIVIAL_STRUCTURE_IS_RELATION",
            "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT",
            "THM_RELATION_ROLE_HARTLEY_LN2",
        ),
        sources=(
            CANONICAL_FOUNDATIONAL_CONTRACT,
            "TIR: minimum non-trivial persistent structure = relation",
        ),
        note="N/S are roles of one persistent relation, not two primitive substances.",
    ),
    ProvenanceNote(
        surface="J=SP complex structure",
        role="THM",
        claim_ids=(
            "THM_HAMLET_SWAP_POLARITY_ANTICOMMUTE",
            "THM_HAMLET_IMAGINARY_GENERATOR",
            "THM_IMAGINARY_GENERATOR_U1",
        ),
        sources=(CANONICAL_FOUNDATIONAL_CONTRACT,),
        note="J^2=-I is derived on the durable N/S real span.",
    ),
    ProvenanceNote(
        surface="relational Collatz operations",
        role="THM",
        claim_ids=(
            "THM_ASSOCIATION_QUOTIENT_CARDINALITY",
            "THM_ACTIVE_OPERATOR_PRODUCT_CARDINALITY",
            "THM_IDENTITY_REPAIR_CARDINALITY",
            "THM_RELATION_ALGEBRA_DETERMINISTICALLY_GENERATES_COLLATZ_MAP",
        ),
        sources=(CANONICAL_FOUNDATIONAL_CONTRACT,),
        note="2/3/1 are role count, active basis-direction count, and identity repair.",
    ),
    ProvenanceNote(
        surface="Gaussian-Bombelli generator",
        role="THM+BRIDGE",
        claim_ids=(
            "THM_RELATION_ROLE_GAUSSIAN_INTEGER_LATTICE",
            "THM_MINIMAL_RELATION_ROLE_GAUSSIAN_GENERATOR",
            "THM_GAUSSIAN_BOMBELLI_LADDER",
            "BRIDGE_TIR_ROOT_EXTENSION_L3_FROM_GAUSSIAN_L45",
        ),
        sources=(
            CANONICAL_FOUNDATIONAL_CONTRACT,
            "TIR root-extension closure",
        ),
        note="g=q+J with q=|{N,S}|=2; L3 bridge remains separately sourced.",
    ),
    ProvenanceNote(
        surface="kappa theorem from bipolar exchange",
        role="BRIDGE+THM+DERIVED",
        claim_ids=(
            "THM_BINARY_Z2_MAXIMUM_ENTROPY_LN2",
            "THM_BIPOLAR_UNIQUE_INVARIANT_CHANNEL_WEIGHT",
            "THM_BIPOLAR_CHANNEL_INFORMATION_UNIFORMIZATION",
            "THM_BIPOLAR_HALF_TURN_MEASURE_EQUALS_TWELVE",
            "THM_BIPOLAR_KAPPA_FORCED",
            "DER_KAPPA_NORMALIZED_TURN",
            "DER_KAPPA_RADIAN_CHART",
        ),
        sources=(
            CANONICAL_FOUNDATIONAL_CONTRACT,
            "docs/BIPOLAR_TETRAHEDRAL_EXCHANGE_BINDING.md",
            "TIR@9783782570a2ccfa1fc42c99b605dad48e02aa78:"
            "TIR/foundations/TIR_COEFFICIENT_MAGNITUDE_PARENT_EVALUATION_V0_1.md",
        ),
        note=(
            "Binary Z2 symmetry fixes maximum source entropy ln(2); the transitive "
            "24-channel bipolar tetrahedral face-flavour orbit forces channel weight "
            "1/24; the non-trivial Z2 phase is the half-turn pi. Therefore "
            "kappa=ln(2)/(24*pi). Historical REF_KAPPA_* surfaces are retained only "
            "for backward-compatible provenance."
        ),
    ),
    ProvenanceNote(
        surface="OFHM phase/coherence separation",
        role="BRIDGE+DERIVED",
        claim_ids=(
            "BRIDGE_OFHM_BEES_PHASE_DATA",
            "BRIDGE_OFHM_BEES_RELATIVE_PHASE_COHERENCE",
            "DER_OFHM_MOIRE_COCYCLE",
        ),
        sources=(CANONICAL_FOUNDATIONAL_CONTRACT,),
        note=(
            "Relative U(1) phase is built from sourced phase coordinates. "
            "The coherence magnitude is lossy and is never inverted to recover phase."
        ),
    ),
    ProvenanceNote(
        surface="OFHM Hilbert-Hotel enumeration",
        role="BRIDGE",
        claim_ids=("BRIDGE_OFHM_HILBERT_HOTEL_SHIFT",),
        sources=(CANONICAL_FOUNDATIONAL_CONTRACT,),
        note=(
            "The executable zigzag/Cantor ranking is one explicit enumeration; "
            "the induced successor is enumeration-dependent and no commutation "
            "with local refinement is assumed."
        ),
    ),
    ProvenanceNote(
        surface="OFHM symbolic prefix completion",
        role="THM+CROSSCHECK",
        claim_ids=(
            "DEF_OFHM_PREFIX_ULTRAMETRIC",
            "THM_OFHM_PREFIX_ULTRAMETRIC",
            "THM_OFHM_PREFIX_CHAIN_CAUCHY",
            "THM_OFHM_SYMBOLIC_COMPLETION_BAIRE_BOUNDARY",
            "THM_OFHM_PREFIX_COMPLETION_NONCOMPACT",
            "THM_OFHM_PREFIX_BOUNDARY_INFINITE_HAUSDORFF_DIMENSION",
            "THM_OFHM_NO_UNIFORM_COUNTABLE_BRANCH_PROBABILITY",
            "THM_OFHM_NO_UNIQUE_CONTINUUM_MEASURE",
            "BRIDGE_OFHM_GEOMETRIC_EMBEDDING",
            "GATE_OFHM_GEOMETRIC_FRACTAL_LIMIT",
        ),
        sources=(
            CANONICAL_FOUNDATIONAL_CONTRACT,
            "docs/OFHM_PREFIX_COMPLETION.md",
            "src/rdss/ofhm_prefix_completion.py",
            "On-Primes@372125962a42e1b225337bf31416233da4ca436b:"
            "proofs/ARPL_PROCYCLIC_PHASE_REFINEMENT_TOWER_V0_1.md",
            "On-Primes@372125962a42e1b225337bf31416233da4ca436b:"
            "proofs/ARPL_CANONICAL_PHASE_ULTRAMETRIC_DIMENSION_V0_1.md",
        ),
        note=(
            "The OFHM completion is proved from the countably branching prefix tree "
            "Z^{<omega}: its boundary is Z^omega, noncompact, and has infinite "
            "Hausdorff dimension for every fixed exponential prefix metric base beta>1. "
            "On-Primes supplies an independent arithmetic refinement crosscheck: its "
            "procyclic inverse-limit phase hull is compact and 1-dimensional in its "
            "canonical arithmetic ultrametric. The contrast is deliberate evidence "
            "that compactness/dimension belong to the declared refinement system and "
            "metric; On-Primes is not a proof parent of the OFHM claims."
        ),
    ),
    ProvenanceNote(
        surface="OFHM prefix-ultrametric symbolic completion",
        role="DEF+THM+BRIDGE+NO_GO",
        claim_ids=(
            "DEF_OFHM_PREFIX_ULTRAMETRIC",
            "THM_OFHM_PREFIX_ULTRAMETRIC",
            "THM_OFHM_PREFIX_CHAIN_CAUCHY",
            "THM_OFHM_SYMBOLIC_COMPLETION_BAIRE_BOUNDARY",
            "THM_OFHM_PREFIX_COMPLETION_NONCOMPACT",
            "THM_OFHM_PREFIX_BOUNDARY_INFINITE_HAUSDORFF_DIMENSION",
            "THM_OFHM_NO_UNIFORM_COUNTABLE_BRANCH_PROBABILITY",
            "THM_OFHM_NO_UNIQUE_CONTINUUM_MEASURE",
            "BRIDGE_OFHM_GEOMETRIC_EMBEDDING",
            "GATE_OFHM_GEOMETRIC_FRACTAL_LIMIT",
        ),
        sources=(
            CANONICAL_FOUNDATIONAL_CONTRACT,
            "docs/OFHM_PREFIX_COMPLETION.md",
            "src/rdss/ofhm_prefix_completion.py",
            "RDSS_OFHM_PARENT_MAIN@3fe6ed391d374a09c0b077b8bdedb3aabe16a28e",
            "Infinities@339d6c58f3e7d86c67a4f758cd7416692f8f8280:research/EULERS_INFINITY_V0_1.md",
            "Infinities@339d6c58f3e7d86c67a4f758cd7416692f8f8280:research/TIR_E6_FOURIER_HILBERT_HOTEL_CORE_V0_1.md",
        ),
        note=(
            "The canonical completion uses only the countably branching prefix tree: "
            "d_beta(a,b)=beta^{-LCP(a,b)} for beta>1. Its metric completion adds "
            "Z^omega, is noncompact, and has infinite Hausdorff dimension in this "
            "declared prefix-ultrametric family. No uniform countable branch "
            "probability or unique continuum measure is forced. Any Euclidean, "
            "complex, manifold or physical image is a separately typed bridge."
        ),
    ),
    ProvenanceNote(
        surface="operator tetrahedral binding",
        role="THM+CROSSCHECK",
        claim_ids=(
            "THM_HAMLET_OPERATOR_BASIS_REGULAR_TETRAHEDRON",
            "THM_HAMLET_OPERATOR_TETRAHEDRON_STELLA_ISOMETRY",
            "THM_STELLA_TETRAHEDRON_KLEIN_FOUR_123_BINDING",
            "THM_TETRAHEDRAL_ONE_PLUS_THREE_SPLIT",
            "THM_TETRAHEDRAL_GEOMETRY_MATCHES_COLLATZ_ODD_CARDINALITY",
            "THM_TETRAHEDRAL_BINDING_IS_DOWNSTREAM_NOT_UPSTREAM_CLOSURE",
        ),
        sources=(
            CANONICAL_FOUNDATIONAL_CONTRACT,
            "docs/TETRAHEDRAL_BINDING_AUDIT.md",
        ),
        note=(
            "The Frobenius-orthonormal basis {I,S,P,J} forms an exact regular "
            "tetrahedron and geometrizes the existing 1+3 / 3n+1 structure. "
            "This is downstream and does not close the primitive-dynamics gate."
        ),
    ),
    ProvenanceNote(
        surface="alternating half-time pendulum and Moire-Kuramoto closure",
        role="BRIDGE+THM+DERIVED",
        claim_ids=(
            "BRIDGE_TIR_PRETIME_STELLA_HALF_SUCCESSOR",
            "BRIDGE_TIR_WHITE_THREAD_PHASE_ACTION",
            "THM_FRAME_FUZZY_HALF_SUCCESSOR",
            "THM_CANONICAL_PAIR_INFORMATION_POTENTIAL",
            "THM_BIPOLAR_PAIR_FORCE_ANTISYMMETRY",
            "THM_BIPOLAR_RELATIVE_PENDULUM",
            "THM_FRAME_SECOND_DIFFERENCE_UNIQUE",
            "THM_FRAME_PENDULUM_SUCCESSOR",
            "THM_MOIRE_INFORMATION_POTENTIAL",
            "THM_MOIRE_KURAMOTO_CLOSURE",
            "THM_PENDULUM_KURAMOTO_COMMON_PARENT",
            "GATE_MOIRE_DYNAMICAL_LAW",
        ),
        sources=(
            CANONICAL_FOUNDATIONAL_CONTRACT,
            "docs/ALTERNATING_HALF_TIME_PENDULUM_MOIRE_KURAMOTO.md",
            "TIR@9783782570a2ccfa1fc42c99b605dad48e02aa78:"
            "TIR/foundations/TIR_PRESPACETIME_STELLA_HALF_SUCCESSOR_V0_1.md",
            "TIR@9783782570a2ccfa1fc42c99b605dad48e02aa78:"
            "TIR/foundations/TIR_STELLA_ALTERNATING_ROTATION_INFERENCE_V0_1.md",
            "TIR@9783782570a2ccfa1fc42c99b605dad48e02aa78:"
            "TIR/foundations/TIR_RELATIONAL_PHASE_LAGRANGIAN_CORE_V0_1.md",
            "TIR@9783782570a2ccfa1fc42c99b605dad48e02aa78:"
            "TIR/foundations/TIR_WHITE_THREAD_SPIN_LIFT_LYAPUNOV_V0_1.md",
            "TIR@9783782570a2ccfa1fc42c99b605dad48e02aa78:"
            "TIR/foundations/TIR_KAPPA_FLAVOUR_MIXING_NORMALIZATION_V0_1.md",
            "RDSS@e1d2dda2ffbcbb38392869f94012cea03fffd751",
        ),
        note=(
            "H is the exact structural half-successor and H^2=S. The canonical "
            "12 undirected pairs inherit two directed information shares each; "
            "normalizing the U(1) chordal mismatch at the half-turn fixes "
            "V_pair=pi*kappa*(1-cos Delta). Opposite gradients give zero center "
            "force and the relative pendulum; the same network potential gives "
            "Kuramoto in the overdamped limit."
        ),
    ),
)


IMPLEMENTATION_PROVENANCE: dict[str, tuple[str, ...]] = {
    "existence_chain.FIRST_LAW_OF_EXISTENCE": ("A0",),
    "existence_chain.relation_roles": ("THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT",),
    "existence_chain.relation_role_hartley_nats": ("THM_RELATION_ROLE_HARTLEY_LN2",),
    "existence_chain.hamlet_complex_structure": ("THM_HAMLET_IMAGINARY_GENERATOR",),
    "primitive_persistence.source_minimal_parity_step": (
        "THM_SOURCE_MINIMAL_AFFINE_PARITY_DYNAMICS_IS_COLLATZ",
    ),
    "relational_collatz.relational_collatz_step": (
        "THM_RELATION_ALGEBRA_DETERMINISTICALLY_GENERATES_COLLATZ_MAP",
    ),
    "gaussian_bombelli.minimal_relation_role_gaussian_generator": (
        "THM_MINIMAL_RELATION_ROLE_GAUSSIAN_GENERATOR",
    ),
    "gaussian_bombelli.bombelli_ladder": ("THM_GAUSSIAN_BOMBELLI_LADDER",),
    "tetrahedral_binding.tetrahedral_binding_certificate": (
        "THM_HAMLET_OPERATOR_BASIS_REGULAR_TETRAHEDRON",
        "THM_HAMLET_OPERATOR_TETRAHEDRON_STELLA_ISOMETRY",
        "THM_TETRAHEDRAL_BINDING_IS_DOWNSTREAM_NOT_UPSTREAM_CLOSURE",
    ),
    "tetrahedral_binding.tetrahedral_completion_cardinality": (
        "THM_TETRAHEDRAL_COMPLETION_CARDINALITY_3N_PLUS_1",
        "THM_TETRAHEDRAL_GEOMETRY_MATCHES_COLLATZ_ODD_CARDINALITY",
    ),
    "bipolar_tetrahedral_exchange.bipolar_exchange_counts": (
        "THM_BIPOLAR_STELLA_CENTRAL_INVERSION_PAIRS_ALL_FACES",
        "THM_BIPOLAR_THREE_FLAVOUR_FACE_INCIDENCE_24",
        "THM_BIPOLAR_EXCHANGE_SYMMETRY_IS_TRANSITIVE",
        "THM_BIPOLAR_UNIQUE_INVARIANT_CHANNEL_WEIGHT",
    ),
    "bipolar_tetrahedral_exchange.selector_free_tetrahedral_odd_completion": (
        "THM_TETRAHEDRAL_ACTIVE_FACE_ORBIT_FORCES_THREE",
        "THM_BIPOLAR_SELECTOR_FREE_231_OPERATION_BINDING",
    ),
    "bipolar_tetrahedral_exchange.forced_kappa_from_bipolar_exchange": (
        "THM_BINARY_Z2_MAXIMUM_ENTROPY_LN2",
        "THM_BIPOLAR_CHANNEL_INFORMATION_UNIFORMIZATION",
        "THM_BIPOLAR_KAPPA_FORCED",
    ),
    "bipolar_tetrahedral_exchange.forced_kappa_certificate": (
        "THM_BIPOLAR_KAPPA_FORCED",
    ),
    "alternating_phase_dynamics.StellaHalfOccurrence.half_successor": (
        "BRIDGE_TIR_PRETIME_STELLA_HALF_SUCCESSOR",
        "THM_FRAME_FUZZY_HALF_SUCCESSOR",
    ),
    "alternating_phase_dynamics.canonical_pair_information_potential": (
        "THM_CANONICAL_PAIR_INFORMATION_POTENTIAL",
    ),
    "alternating_phase_dynamics.bipolar_pair_forces": (
        "THM_BIPOLAR_PAIR_FORCE_ANTISYMMETRY",
    ),
    "alternating_phase_dynamics.relative_pendulum_residual": (
        "THM_BIPOLAR_RELATIVE_PENDULUM",
    ),
    "alternating_phase_dynamics.pendulum_frame_successor": (
        "THM_FRAME_SECOND_DIFFERENCE_UNIQUE",
        "THM_FRAME_PENDULUM_SUCCESSOR",
    ),
    "alternating_phase_dynamics.canonical_moire_information_potential": (
        "THM_MOIRE_INFORMATION_POTENTIAL",
    ),
    "alternating_phase_dynamics.canonical_kuramoto_velocity": (
        "THM_MOIRE_KURAMOTO_CLOSURE",
        "THM_PENDULUM_KURAMOTO_COMMON_PARENT",
    ),
    "orbital_fractal_hilbert_moire.countable_word_rank": (
        "DEF_OFHM_COUNTABLE_BRANCH_ADDRESS",
    ),
    "orbital_fractal_hilbert_moire.euler_inverse_branch": (
        "BRIDGE_OFHM_EULER_SYMBOLIC_BRANCH_SPACE",
    ),
    "orbital_fractal_hilbert_moire.relative_moire_phase": (
        "BRIDGE_OFHM_BEES_PHASE_DATA",
        "DER_OFHM_MOIRE_COCYCLE",
    ),
    "orbital_fractal_hilbert_moire.phase_coherence_overlap": (
        "BRIDGE_OFHM_BEES_RELATIVE_PHASE_COHERENCE",
    ),
    "orbital_fractal_hilbert_moire.CountableBranchAddress.hilbert_hotel_successor": (
        "BRIDGE_OFHM_HILBERT_HOTEL_SHIFT",
    ),
    "ofhm_prefix_completion.common_prefix_length": (
        "DEF_OFHM_PREFIX_ULTRAMETRIC",
    ),
    "ofhm_prefix_completion.prefix_ultrametric": (
        "DEF_OFHM_PREFIX_ULTRAMETRIC",
        "THM_OFHM_PREFIX_ULTRAMETRIC",
    ),
    "ofhm_prefix_completion.prefix_chain_cauchy_bound": (
        "THM_OFHM_PREFIX_CHAIN_CAUCHY",
    ),
    "ofhm_prefix_completion.finite_alphabet_boundary_dimension": (
        "THM_OFHM_PREFIX_BOUNDARY_INFINITE_HAUSDORFF_DIMENSION",
    ),
    "ofhm_prefix_completion.countable_boundary_dimension_is_infinite": (
        "THM_OFHM_PREFIX_BOUNDARY_INFINITE_HAUSDORFF_DIMENSION",
    ),
    "ofhm_prefix_completion.countable_prefix_completion_is_totally_bounded": (
        "THM_OFHM_PREFIX_COMPLETION_NONCOMPACT",
    ),
    "ofhm_prefix_completion.uniform_countable_branch_probability_exists": (
        "THM_OFHM_NO_UNIFORM_COUNTABLE_BRANCH_PROBABILITY",
        "THM_OFHM_NO_UNIQUE_CONTINUUM_MEASURE",
    ),
    "ofhm_prefix_completion.symbolic_completion_certificate": (
        "THM_OFHM_SYMBOLIC_COMPLETION_BAIRE_BOUNDARY",
        "THM_OFHM_PREFIX_COMPLETION_NONCOMPACT",
        "THM_OFHM_PREFIX_BOUNDARY_INFINITE_HAUSDORFF_DIMENSION",
        "THM_OFHM_NO_UNIQUE_CONTINUUM_MEASURE",
        "GATE_OFHM_GEOMETRIC_FRACTAL_LIMIT",
    ),
    "orbital_fractal_hilbert_moire.moire_transport": (
        "DER_OFHM_HILBERT_TRANSPORT",
    ),
    "orbital_fractal_hilbert_moire.idt_phase_dynamics_step": (
        "BRIDGE_OFHM_BEES_IDT_DYNAMICS",
    ),
}


def provenance_for_surface(surface: str) -> tuple[str, ...]:
    """Return authoritative claim IDs for one executable surface."""

    try:
        return IMPLEMENTATION_PROVENANCE[surface]
    except KeyError as exc:
        raise KeyError(f"no canonical provenance registered for {surface!r}") from exc
