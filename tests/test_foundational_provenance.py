from pathlib import Path

from rdss import (
    CANONICAL_FOUNDATIONAL_CONTRACT,
    FOUNDATIONAL_PROVENANCE,
    IMPLEMENTATION_PROVENANCE,
    LAW_OF_REALITY,
    claim_map,
    provenance_for_surface,
)


def test_canonical_foundational_contract_is_present_and_named() -> None:
    assert "Law of Reality" in LAW_OF_REALITY
    root = Path(__file__).resolve().parents[1]
    contract = root / CANONICAL_FOUNDATIONAL_CONTRACT
    assert contract.is_file()
    text = contract.read_text(encoding="utf-8")
    assert "Law of Reality" in text
    assert "Prawo Rzeczywisto" in text
    assert "0_R" in text
    assert "J^2=-I" in text or "J^2 = -I" in text


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
        "existence_chain.LAW_OF_REALITY",
        "existence_chain.hamlet_complex_structure",
        "primitive_persistence.source_minimal_parity_step",
        "relational_collatz.relational_collatz_step",
        "gaussian_bombelli.minimal_relation_role_gaussian_generator",
        "orbital_fractal_hilbert_moire.idt_phase_dynamics_step",
    }
    assert required <= set(IMPLEMENTATION_PROVENANCE)
