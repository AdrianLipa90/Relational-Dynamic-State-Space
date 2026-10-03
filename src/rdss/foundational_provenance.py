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
        surface="canonical relational-existence foundation closure",
        role="BRIDGE+THM",
        claim_ids=(
            "BRIDGE_TIR_RELATIONAL_EXISTENCE_TYPING",
            "THM_CANONICAL_EXISTENCE_FORCES_RELATIONAL_WITNESS",
            "THM_CANONICAL_NONTRIVIAL_EXISTENCE_FORCES_DISTINCTION",
            "RA0",
            "THM_FINITE_RELATIONAL_REFINEMENT_AVAILABLE",
            "THM_COLLATZ_STRUCTURAL_DYNAMICS_CLOSED",
        ),
        sources=(
            CANONICAL_FOUNDATIONAL_CONTRACT,
            "docs/FOUNDATIONAL_CLOSURE_FRONTIER.md",
            "TIR@9783782570a2ccfa1fc42c99b605dad48e02aa78:"
            "TIR/foundations/TIR_CANONICAL_DERIVATION_SPINE_V0_1.md",
            "TIR@9783782570a2ccfa1fc42c99b605dad48e02aa78:"
            "TIR/provenance/TIR_FOUNDATION_PROOF_SOURCE_REGISTRY_V0_1.md",
        ),
        note=(
            "TIR relational existence typing supplies Exist(x)->exists R_x and is "
            "imported explicitly rather than attributed to A0 alone. Relational "
            "distinction is theorem-level only in the declared non-self-collapsed "
            "non-trivial relational sector. Historical "
            "First-Hamlet/RA0*/RR1/Collatz structural gates are discharged or "
            "retyped as formation/provenance surfaces. The geometric-fractal limit is "
            "closed by no-go, and physical binding is separately typed EVIDENCE_GATE; "
            "no structural DERIVATION_GATE remains."
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
        role="DEF+THM+HISTORICAL_GATE",
        claim_ids=(
            "DEF_DISTINCTION_PERSISTENCE_PREDICATE",
            "THM_FIRST_HAMLET_DISPERSION_STRUCTURE",
            "GATE_FIRST_HAMLET_NONDEGENERACY_FROM_PE_I0",
        ),
        sources=(CANONICAL_FOUNDATIONAL_CONTRACT,),
        note=(
            "DISPERSION/STRUCTURE classify persistence and are not the durable "
            "N/S projective carrier. The historical dynamic-nondegeneracy gate is "
            "discharged/superseded; canonical non-degeneracy remains an explicit "
            "semantics choice rather than a theorem of A0 alone."
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
            "This theorem is downstream and does not itself perform the dynamics "
            "closure; that historical gate is closed independently by the later "
            "selector-free relational dynamics chain."
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
    ProvenanceNote(
        surface="realization-specific underdetermination boundaries",
        role="THM+NO_GO",
        claim_ids=(
            "THM_SEMANTIC_WEIGHTING_UNDERDETERMINED_BY_SCALE_LABEL",
            "THM_INDEXED_TENSOR_CONTRACTION_UNDERDETERMINED_BY_FLAT_RANK",
            "THM_NONSTRICT_MONOIDAL_COHERENCE_UNDERDETERMINED_BY_FLATTENING",
            "THM_REALIZATION_BOUNDARIES_CLOSED_BY_UNDERDETERMINATION",
        ),
        sources=(
            "docs/SEMANTIC_WEIGHTING_GATE.md",
            "docs/INDEXED_TENSOR_GATE.md",
            "docs/MONOIDAL_COHERENCE_GATE.md",
            "src/rdss/realization_boundaries.py",
        ),
        note=(
            "These historical gate names are closed by exact non-uniqueness or "
            "information-loss witnesses. The general signature does not uniquely "
            "select semantic weights, indexed contraction metadata, or non-strict "
            "coherence morphisms. Concrete realizations may supply those data "
            "explicitly without creating structural derivation debt."
        ),
    ),
    ProvenanceNote(
        surface="OFHM symbolic-boundary no-go and physical evidence frontier",
        role="DEF+THM+EVIDENCE_GATE",
        claim_ids=(
            "DEF_OFHM_IDEAL_BAIRE_BOUNDARY",
            "THM_OFHM_IDEAL_BOUNDARY_IS_NONCOMPACT_BAIRE_SPACE",
            "THM_OFHM_CONTINUUM_MEASURE_IS_NOT_UNIQUE",
            "THM_OFHM_PREFIX_METRIC_SCALE_IS_NOT_CANONICAL",
            "THM_OFHM_EXTERNAL_GEOMETRIC_LIMIT_REQUIRES_EXTRA_EMBEDDING",
            "THM_OFHM_GEOMETRIC_FRACTAL_LIMIT_UNDERDETERMINED",
            "GATE_OFHM_GEOMETRIC_FRACTAL_LIMIT",
            "THM_OFHM_PHYSICAL_BINDING_REQUIRES_EXTERNAL_EVIDENCE",
            "GATE_OFHM_PHYSICAL_BINDING",
        ),
        sources=(
            CANONICAL_FOUNDATIONAL_CONTRACT,
            "docs/GENERAL_ORBITAL_FRACTAL_HILBERT_MOIRE_ALGEBRA.md",
            "docs/FOUNDATIONAL_CLOSURE_FRONTIER.md",
        ),
        note=(
            "The ideal symbolic boundary is Z^N with cylinder topology. It is Baire "
            "space and noncompact. Explicit full-support product measures and compatible "
            "prefix metrics witness that neither measure nor Hausdorff dimension is "
            "selected by the symbolic carrier. External geometric embedding and concrete "
            "physical realization require extra structure/evidence. Structural "
            "DERIVATION_GATE count is zero; physical binding is typed EVIDENCE_GATE."
        ),
    )
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
    "realization_boundaries.semantic_weighting_underdetermination_certificate": (
        "THM_SEMANTIC_WEIGHTING_UNDERDETERMINED_BY_SCALE_LABEL",
    ),
    "realization_boundaries.indexed_tensor_underdetermination_certificate": (
        "THM_INDEXED_TENSOR_CONTRACTION_UNDERDETERMINED_BY_FLAT_RANK",
    ),
    "realization_boundaries.monoidal_coherence_underdetermination_certificate": (
        "THM_NONSTRICT_MONOIDAL_COHERENCE_UNDERDETERMINED_BY_FLATTENING",
    ),
    "realization_boundaries.realization_boundary_no_go_certificate": (
        "THM_REALIZATION_BOUNDARIES_CLOSED_BY_UNDERDETERMINATION",
    ),
    "orbital_fractal_hilbert_moire.countable_word_rank": (
        "DEF_OFHM_COUNTABLE_BRANCH_ADDRESS",
    ),
    "orbital_fractal_hilbert_moire.prefix_ultrametric": (
        "DEF_OFHM_IDEAL_BAIRE_BOUNDARY",
        "THM_OFHM_PREFIX_METRIC_SCALE_IS_NOT_CANONICAL",
    ),
    "orbital_fractal_hilbert_moire.cylinder_product_measure": (
        "THM_OFHM_CONTINUUM_MEASURE_IS_NOT_UNIQUE",
    ),
    "orbital_fractal_hilbert_moire.ofhm_geometric_limit_no_go_certificate": (
        "THM_OFHM_GEOMETRIC_FRACTAL_LIMIT_UNDERDETERMINED",
        "GATE_OFHM_GEOMETRIC_FRACTAL_LIMIT",
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
