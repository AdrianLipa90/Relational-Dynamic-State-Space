from rdss.corpus import (
    rdss_reference_corpus,
    scan_rdss_reference_corpus,
)
from rdss.signature import NoveltyKind
from rdss.axioms import claim_map


def test_reference_corpus_has_stable_named_inventory():
    corpus = rdss_reference_corpus()

    assert len(corpus) == 34
    names = tuple(item.name for item in corpus)
    assert len(names) == len(set(names))

    assert "occ-root" in names
    assert "tensor-scalar-one" in names
    assert "tensor-scalar-zero" in names
    assert "occurrence-cycle" in names
    assert "hilbert-moire-q-quarter" in names
    assert "cp1-north" in names
    assert "moire-base" in names
    assert "typed-zero" in names
    assert "zero-axis-point" in names
    assert "generative-relation-model" in names


def test_reference_corpus_claim_provenance_resolves_in_ledger():
    claims = claim_map()

    missing = {
        claim_id
        for item in rdss_reference_corpus()
        for claim_id in item.source_claim_ids
        if claim_id not in claims
    }

    assert missing == set()


def test_reference_corpus_scan_has_complete_signature_coverage():
    result = scan_rdss_reference_corpus()

    assert len(result.items) == 34
    assert len(result.supported_items) == 34
    assert result.coverage_gaps == ()
    assert result.coverage_complete


def test_reference_corpus_novelty_counts_separate_redundancy_state_and_structure():
    result = scan_rdss_reference_corpus()
    counts = result.novelty_counts

    assert counts[NoveltyKind.EXACT_REPEAT] == 1
    assert counts[NoveltyKind.SIGNATURE_EQUIVALENT] == 1
    assert counts[NoveltyKind.REPRESENTATION_ONLY] == 0
    assert counts[NoveltyKind.NEW_STATE] == 6
    assert counts[NoveltyKind.NEW_STRUCTURE] == 6
    assert counts[NoveltyKind.NEW_FAMILY] == 20


def test_reference_corpus_catalog_summary_quantifies_compression_layers():
    summary = scan_rdss_reference_corpus().catalog_summary

    assert summary.records == 34
    assert summary.families == 20
    assert summary.structures == 26
    assert summary.semantic_states == 32
    assert summary.strict_values == 33


def test_reference_corpus_graph_keeps_lossy_projection_out_of_components():
    graph = scan_rdss_reference_corpus().equivalence_graph
    summary = graph.summary()

    assert summary.records == 34
    assert summary.equivalence_components == 29
    assert summary.strong_edges == 6
    assert summary.lossy_projection_edges == 4
    assert summary.unknown_bridge_edges == 0


def test_reference_corpus_known_reference_bridges_compress_expected_records():
    result = scan_rdss_reference_corpus()
    index = {
        item.name: ordinal
        for ordinal, item in enumerate(result.supported_items)
    }
    graph = result.equivalence_graph

    assert graph.component_of(index["occ-root"]) == graph.component_of(
        index["point-root"]
    )
    assert graph.component_of(index["occ-left"]) == graph.component_of(
        index["point-left"]
    )
    assert graph.component_of(
        index["occ-left-repeat"]
    ) == graph.component_of(index["point-left"])

    assert graph.component_of(
        index["relation-occurrence-down"]
    ) != graph.component_of(index["relation-down"])

    assert graph.component_of(
        index["occurrence-cycle"]
    ) != graph.component_of(index["relation-cycle"])


def test_reference_corpus_moire_common_shift_is_signature_redundancy():
    result = scan_rdss_reference_corpus()
    novelty = {item.name: item.novelty for item in result.novelty}

    assert novelty["moire-base"] is NoveltyKind.NEW_FAMILY
    assert (
        novelty["moire-common-shift"]
        is NoveltyKind.SIGNATURE_EQUIVALENT
    )
    assert novelty["moire-new-delta"] is NoveltyKind.NEW_STATE


def test_reference_corpus_gap_report_is_nonempty_and_record_level():
    report = scan_rdss_reference_corpus().bridge_gap_report

    assert report.family_pairs > 0
    assert report.unresolved_pairs > 0



def test_reference_corpus_zero_descriptor_and_zero_element_share_lossless_component():
    result = scan_rdss_reference_corpus()
    index = {
        item.name: ordinal
        for ordinal, item in enumerate(result.supported_items)
    }
    graph = result.equivalence_graph

    assert graph.component_of(
        index["typed-zero"]
    ) == graph.component_of(
        index["tensor-scalar-zero"]
    )


def test_reference_corpus_relational_distinction_projection_is_lossy_nonunion():
    result = scan_rdss_reference_corpus()
    index = {
        item.name: ordinal
        for ordinal, item in enumerate(result.supported_items)
    }
    graph = result.equivalence_graph

    assert graph.component_of(
        index["relational-binary-distinction"]
    ) != graph.component_of(
        index["binary-distinction"]
    )

    matching = [
        edge
        for edge in graph.lossy_projection_edges
        if edge.source == index["relational-binary-distinction"]
        and edge.target == index["binary-distinction"]
    ]
    assert len(matching) == 1
