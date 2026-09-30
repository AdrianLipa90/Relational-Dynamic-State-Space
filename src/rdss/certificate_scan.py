from __future__ import annotations

from dataclasses import dataclass

from .corpus import CorpusItem, rdss_reference_corpus
from .reduction_certificate import (
    ReductionCertificate,
    certify_forgetful_reduction,
)


@dataclass(frozen=True)
class ReductionCertificateScanItem:
    name: str
    source_family: str
    target_family: str
    rewritten: bool
    lossy: bool
    rule_names: tuple[str, ...]
    verified_invariants: tuple[str, ...]
    claim_count: int
    claim_edge_count: int
    foundational_claim_ids: tuple[str, ...]
    global_canonical: bool


@dataclass(frozen=True)
class ReductionCertificateScanSummary:
    records: int
    verified: int
    rewritten: int
    fixed_points: int
    lossy: int
    global_canonical_true: int
    distinct_source_families: int
    distinct_target_families: int


@dataclass(frozen=True)
class ReductionCertificateScan:
    items: tuple[ReductionCertificateScanItem, ...]
    certificates: tuple[ReductionCertificate, ...]
    summary: ReductionCertificateScanSummary


def _scan_item(
    corpus_item: CorpusItem,
    certificate: ReductionCertificate,
) -> ReductionCertificateScanItem:
    return ReductionCertificateScanItem(
        name=corpus_item.name,
        source_family=certificate.source_family,
        target_family=certificate.target_family,
        rewritten=certificate.rewritten,
        lossy=certificate.lossy,
        rule_names=certificate.rewrite_trace.rule_names,
        verified_invariants=certificate.verified_invariants,
        claim_count=certificate.claim_graph.claim_count,
        claim_edge_count=certificate.claim_graph.edge_count,
        foundational_claim_ids=(
            certificate.claim_graph.foundational_claim_ids
        ),
        global_canonical=certificate.global_canonical,
    )


def scan_reference_reduction_certificates(
    corpus: tuple[CorpusItem, ...] | None = None,
) -> ReductionCertificateScan:
    items = corpus or rdss_reference_corpus()
    certificates = tuple(
        certify_forgetful_reduction(item.value)
        for item in items
    )
    scan_items = tuple(
        _scan_item(item, certificate)
        for item, certificate in zip(
            items,
            certificates,
            strict=True,
        )
    )

    summary = ReductionCertificateScanSummary(
        records=len(scan_items),
        verified=sum(
            certificate.verified
            for certificate in certificates
        ),
        rewritten=sum(
            item.rewritten
            for item in scan_items
        ),
        fixed_points=sum(
            not item.rewritten
            for item in scan_items
        ),
        lossy=sum(
            item.lossy
            for item in scan_items
        ),
        global_canonical_true=sum(
            item.global_canonical
            for item in scan_items
        ),
        distinct_source_families=len(
            {item.source_family for item in scan_items}
        ),
        distinct_target_families=len(
            {item.target_family for item in scan_items}
        ),
    )

    return ReductionCertificateScan(
        items=scan_items,
        certificates=certificates,
        summary=summary,
    )
