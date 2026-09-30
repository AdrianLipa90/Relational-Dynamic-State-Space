from rdss.certificate_scan import (
    scan_reference_reduction_certificates,
)


def test_reference_reduction_certificate_scan_summary():
    scan = scan_reference_reduction_certificates()
    summary = scan.summary

    assert summary.records == 36
    assert summary.verified == 36
    assert summary.rewritten == 5
    assert summary.fixed_points == 31
    assert summary.lossy == 5
    assert summary.global_canonical_true == 0
    assert summary.distinct_source_families == 22
    assert summary.distinct_target_families == 18


def test_reference_reduction_certificate_scan_items_match_certificates():
    scan = scan_reference_reduction_certificates()

    assert len(scan.items) == len(scan.certificates) == 36

    for item, certificate in zip(
        scan.items,
        scan.certificates,
        strict=True,
    ):
        assert item.source_family == certificate.source_family
        assert item.target_family == certificate.target_family
        assert item.rewritten == certificate.rewritten
        assert item.lossy == certificate.lossy
        assert item.rule_names == certificate.rewrite_trace.rule_names
        assert (
            item.verified_invariants
            == certificate.verified_invariants
        )
        assert item.claim_count == certificate.claim_graph.claim_count
        assert (
            item.claim_edge_count
            == certificate.claim_graph.edge_count
        )
        assert (
            item.foundational_claim_ids
            == certificate.claim_graph.foundational_claim_ids
        )
        assert not item.global_canonical


def test_rewritten_scan_items_cover_exact_reference_names():
    scan = scan_reference_reduction_certificates()

    rewritten = {
        item.name
        for item in scan.items
        if item.rewritten
    }

    assert rewritten == {
        "relation-occurrence-down",
        "relation-occurrence-up",
        "occurrence-cycle",
        "relational-binary-distinction",
        "relational-generative-relation-model",
    }


def test_every_rewritten_scan_item_carries_executable_invariant_evidence():
    scan = scan_reference_reduction_certificates()

    for item in scan.items:
        if item.rewritten:
            assert item.verified_invariants
        else:
            assert item.verified_invariants == ()


def test_scan_claim_graphs_are_nonempty_for_every_reference_value():
    scan = scan_reference_reduction_certificates()

    assert all(
        item.claim_count > 0
        for item in scan.items
    )
    assert all(
        item.claim_edge_count >= 0
        for item in scan.items
    )
