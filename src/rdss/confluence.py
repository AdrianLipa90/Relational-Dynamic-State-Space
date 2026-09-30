from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .canonical import strict_normal_form
from .rewrite import (
    RewriteRule,
    RewriteSystem,
    RewriteTerminationCertificateError,
    FamilyRankTerminationCertificate,
)


class ConfluenceError(RuntimeError):
    pass


class ConfluenceCertificateError(ConfluenceError):
    pass


@dataclass(frozen=True)
class RuleOverlapCandidate:
    source_family: str
    left_rule: str
    right_rule: str


@dataclass(frozen=True)
class RuleOverlapAudit:
    checked_rules: tuple[str, ...]
    overlaps: tuple[RuleOverlapCandidate, ...]

    @property
    def overlap_free(self) -> bool:
        return not self.overlaps


@dataclass(frozen=True)
class ConcreteCriticalPair:
    source_key: object
    source_family: str
    left_rule: str
    right_rule: str
    left_target_key: object
    right_target_key: object
    targets_strict_equal: bool


@dataclass(frozen=True)
class DistinctSourceFamilyConfluenceCertificate:
    """Certificate that at most one rule can apply by semantic family."""

    name: str
    claim_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError(
                "confluence certificate name must be non-empty"
            )
        if any(not claim.strip() for claim in self.claim_ids):
            raise ValueError(
                "confluence certificate claim ids must be non-empty"
            )

    def audit(
        self,
        system: RewriteSystem,
    ) -> RuleOverlapAudit:
        return source_family_overlap_audit(system)

    def require_valid(
        self,
        system: RewriteSystem,
    ) -> RuleOverlapAudit:
        audit = self.audit(system)
        if not audit.overlap_free:
            details = ", ".join(
                (
                    f"{item.source_family}:"
                    f"{item.left_rule}|{item.right_rule}"
                )
                for item in audit.overlaps
            )
            raise ConfluenceCertificateError(
                "source-family confluence certificate failed: "
                + details
            )
        return audit


@dataclass(frozen=True)
class CertifiedIrreducibleResult:
    value: object
    rule_names: tuple[str, ...]
    lossy: bool
    termination_certificate: str
    confluence_certificate: str


def source_family_overlap_audit(
    system: RewriteSystem,
) -> RuleOverlapAudit:
    overlaps: list[RuleOverlapCandidate] = []

    for left, right in combinations(system.rules, 2):
        if left.source_family != right.source_family:
            continue
        overlaps.append(
            RuleOverlapCandidate(
                source_family=left.source_family,
                left_rule=left.name,
                right_rule=right.name,
            )
        )

    return RuleOverlapAudit(
        checked_rules=tuple(rule.name for rule in system.rules),
        overlaps=tuple(overlaps),
    )


def critical_pairs_for_value(
    system: RewriteSystem,
    value: object,
) -> tuple[ConcreteCriticalPair, ...]:
    rules = system.applicable_rules(value)
    if len(rules) < 2:
        return ()

    source_signature = system.signature_engine.signature(value)
    source_key = strict_normal_form(value).key
    pairs: list[ConcreteCriticalPair] = []

    for left, right in combinations(rules, 2):
        left_target, _ = system.apply(value, left.name)
        right_target, _ = system.apply(value, right.name)
        left_key = strict_normal_form(left_target).key
        right_key = strict_normal_form(right_target).key

        pairs.append(
            ConcreteCriticalPair(
                source_key=source_key,
                source_family=source_signature.family,
                left_rule=left.name,
                right_rule=right.name,
                left_target_key=left_key,
                right_target_key=right_key,
                targets_strict_equal=left_key == right_key,
            )
        )

    return tuple(pairs)


def certified_irreducible_result(
    system: RewriteSystem,
    value: object,
    *,
    termination: FamilyRankTerminationCertificate,
    confluence: DistinctSourceFamilyConfluenceCertificate,
) -> CertifiedIrreducibleResult:
    termination.require_valid(system)
    confluence.require_valid(system)

    try:
        trace = system.trace_certified(
            value,
            termination,
        )
    except RewriteTerminationCertificateError:
        raise

    return CertifiedIrreducibleResult(
        value=trace.value,
        rule_names=trace.rule_names,
        lossy=trace.lossy,
        termination_certificate=termination.name,
        confluence_certificate=confluence.name,
    )


def rdss_forgetful_confluence_certificate(
) -> DistinctSourceFamilyConfluenceCertificate:
    return DistinctSourceFamilyConfluenceCertificate(
        name="rdss-forgetful-distinct-source-family-v1",
        claim_ids=(
            "REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE",
        ),
    )
