from pathlib import Path

from rdss import (
    CANONICAL_FOUNDATIONAL_CONTRACT,
    FIRST_LAW_OF_EXISTENCE,
    FOUNDATIONAL_PROVENANCE,
    IMPLEMENTATION_PROVENANCE,
    claim_map,
    provenance_for_surface,
)


def test_canonical_foundational_contract_is_present_and_named() -> None:
    assert "not a realizable state" in FIRST_LAW_OF_EXISTENCE.lower()
    root = Path(__file__).resolve().parents[1]
    contract = root / CANONICAL_FOUNDATIONAL_CONTRACT
    assert contract.is_file()
    text = contract.read_text(encoding="utf-8")
    assert "First Law of Existence" in text
    assert "law of reality" in text.lower()
    assert "not names, aliases" in text.lower()
    assert "0_R" in text
    assert "J^2=-I" in text or "J^2 = -I" in text
    assert "Do not use GitHub Actions" in text


def test_foundational_provenance_claim_ids_are_real() -> None:
    claims = claim_map()
    for note in FOUNDATIONAL_PROVENANCE:
        assert note.claim_ids
        for claim_id in note.claim_ids:
            assert claim_id in claims


def test_implementation_surfaces_have_authoritative_claim_ids() -> None:
    claims = claim_map()
    assert IMPLEMENTATION_PROVENANCE
    for surface, ids in IMPLEMENTATION_PROVENANCE.items():
        assert surface
        assert ids
        assert provenance_for_surface(surface) == ids
        for claim_id in ids:
            assert claim_id in claims


def test_key_surfaces_are_permanently_cited() -> None:
    required = {
        "existence_chain.FIRST_LAW_OF_EXISTENCE",
        "existence_chain.hamlet_complex_structure",
        "primitive_persistence.source_minimal_parity_step",
        "relational_collatz.relational_collatz_step",
        "gaussian_bombelli.minimal_relation_role_gaussian_generator",
        "orbital_fractal_hilbert_moire.idt_phase_dynamics_step",
        "orbital_fractal_hilbert_moire.phase_coherence_overlap",
        "orbital_fractal_hilbert_moire.CountableBranchAddress.hilbert_hotel_successor",
    }
    assert required <= set(IMPLEMENTATION_PROVENANCE)
