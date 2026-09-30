from rdss.axioms import claim_map
from rdss.triage import (
    BridgeTriageStatus,
    rdss_reference_bridge_triage,
)


def test_reference_bridge_triage_has_stable_status_counts():
    report = rdss_reference_bridge_triage()
    summary = report.summary()

    assert summary.entries == 11
    assert summary.implemented_lossless == 2
    assert summary.implemented_lossy == 4
    assert summary.context_required == 1
    assert summary.missing_intermediate_family == 1
    assert summary.composite_not_equivalent == 2
    assert summary.no_bridge_claim == 1


def test_reference_bridge_triage_claim_provenance_resolves():
    claims = claim_map()
    missing = {
        claim_id
        for entry in rdss_reference_bridge_triage().entries
        for claim_id in entry.claim_ids
        if claim_id not in claims
    }

    assert missing == set()


def test_context_required_bridge_is_branch_occurrence_to_typed_relation():
    entries = rdss_reference_bridge_triage().by_status(
        BridgeTriageStatus.CONTEXT_REQUIRED
    )

    assert len(entries) == 1
    assert entries[0].source_family == "branch_relation_occurrence"
    assert entries[0].target_family == "typed_relation"


def test_zero_axis_gap_requires_intermediate_u1_family():
    entries = rdss_reference_bridge_triage().by_status(
        BridgeTriageStatus.MISSING_INTERMEDIATE_FAMILY
    )

    assert len(entries) == 1
    assert entries[0].source_family == "zero_axis_point"
    assert entries[0].target_family == "u1_phase"


def test_composite_objects_are_not_promoted_to_state_equivalence():
    entries = rdss_reference_bridge_triage().by_status(
        BridgeTriageStatus.COMPOSITE_NOT_EQUIVALENT
    )
    pairs = {
        (entry.source_family, entry.target_family)
        for entry in entries
    }

    assert pairs == {
        ("cp1_distinction", "cp1_state"),
        ("semantic_scale_graph", "semantic_scale"),
    }


def test_implemented_lossy_triage_contains_relational_projection_layers():
    entries = rdss_reference_bridge_triage().by_status(
        BridgeTriageStatus.IMPLEMENTED_LOSSY
    )
    pairs = {
        (entry.source_family, entry.target_family)
        for entry in entries
    }

    assert (
        "relational_binary_distinction",
        "binary_distinction",
    ) in pairs
    assert (
        "relational_generative_model",
        "generative_relation_model",
    ) in pairs
