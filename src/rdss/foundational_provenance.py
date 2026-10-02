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
        role="DEF+THM+GATE",
        claim_ids=(
            "DEF_DISTINCTION_PERSISTENCE_PREDICATE",
            "THM_FIRST_HAMLET_DISPERSION_STRUCTURE",
            "GATE_FIRST_HAMLET_NONDEGENERACY_FROM_PE_I0",
        ),
        sources=(CANONICAL_FOUNDATIONAL_CONTRACT,),
        note=(
            "DISPERSION/STRUCTURE classify persistence and are not the durable "
            "N/S projective carrier. Dynamic non-degeneracy remains explicit."
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
        surface="kappa reference normalization",
        role="REFERENCE+DERIVED",
        claim_ids=(
            "REF_KAPPA_MIXING_NORMALIZATION",
            "REF_KAPPA_UNIFORM_INFORMATION_DENSITY",
            "DER_KAPPA_NORMALIZED_TURN",
            "DER_KAPPA_RADIAN_CHART",
        ),
        sources=(CANONICAL_FOUNDATIONAL_CONTRACT,),
        note=(
            "kappa=ln(2)/(24*pi) is derived only inside the declared reference "
            "normalization including constant information density; total information "
            "and total turn measure alone do not force a constant density."
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
