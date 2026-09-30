import pytest

from rdss import (
    OccurrenceAddress,
    RelationalPoint,
)
from rdss.canonical import (
    EquivalenceKind,
    InformationEffect,
)
from rdss.confluence import (
    ConfluenceCertificateError,
    DistinctSourceFamilyConfluenceCertificate,
    certified_irreducible_result,
    critical_pairs_for_value,
    rdss_forgetful_confluence_certificate,
    source_family_overlap_audit,
)
from rdss.corpus import rdss_reference_corpus
from rdss.realizations import reference_point_from_occurrence
from rdss.rewrite import (
    RewriteRule,
    RewriteSystem,
    rdss_forgetful_rewrite_system,
    rdss_forgetful_termination_certificate,
)


def occurrence_to_point_rule(name: str) -> RewriteRule:
    return RewriteRule(
        name=name,
        source_family="occurrence_address",
        target_family="relational_carrier",
        transform=reference_point_from_occurrence,
        source_check=lambda value: isinstance(
            value,
            OccurrenceAddress,
        ),
        target_check=lambda value: isinstance(
            value,
            RelationalPoint,
        ),
        kind=EquivalenceKind.REFERENCE_REPRESENTATION,
        information_effect=InformationEffect.LOSSLESS,
    )


def test_reference_forgetful_rules_have_no_source_family_overlap():
    system = rdss_forgetful_rewrite_system()

    audit = source_family_overlap_audit(system)

    assert audit.overlap_free
    assert audit.overlaps == ()
    assert len(audit.checked_rules) == 4


def test_reference_forgetful_confluence_certificate_verifies():
    system = rdss_forgetful_rewrite_system()
    certificate = rdss_forgetful_confluence_certificate()

    audit = certificate.require_valid(system)

    assert audit.overlap_free


def test_reference_corpus_has_no_concrete_forgetful_critical_pairs():
    system = rdss_forgetful_rewrite_system()

    for item in rdss_reference_corpus():
        assert critical_pairs_for_value(
            system,
            item.value,
        ) == ()


def test_same_source_family_rules_are_reported_as_overlap_candidates():
    system = RewriteSystem(
        (
            occurrence_to_point_rule("left"),
            occurrence_to_point_rule("right"),
        )
    )

    audit = source_family_overlap_audit(system)

    assert not audit.overlap_free
    assert len(audit.overlaps) == 1
    assert audit.overlaps[0].source_family == "occurrence_address"
    assert {
        audit.overlaps[0].left_rule,
        audit.overlaps[0].right_rule,
    } == {"left", "right"}


def test_confluence_certificate_fails_closed_on_source_family_overlap():
    system = RewriteSystem(
        (
            occurrence_to_point_rule("left"),
            occurrence_to_point_rule("right"),
        )
    )
    certificate = DistinctSourceFamilyConfluenceCertificate(
        "bad-overlap-certificate"
    )

    with pytest.raises(ConfluenceCertificateError):
        certificate.require_valid(system)


def test_concrete_critical_pair_records_both_immediate_targets():
    system = RewriteSystem(
        (
            occurrence_to_point_rule("left"),
            occurrence_to_point_rule("right"),
        )
    )
    value = OccurrenceAddress((-1,))

    pairs = critical_pairs_for_value(system, value)

    assert len(pairs) == 1
    assert pairs[0].source_family == "occurrence_address"
    assert {
        pairs[0].left_rule,
        pairs[0].right_rule,
    } == {"left", "right"}
    assert pairs[0].targets_strict_equal


def test_termination_and_confluence_certificates_yield_unique_irreducible_result():
    system = rdss_forgetful_rewrite_system()
    termination = rdss_forgetful_termination_certificate()
    confluence = rdss_forgetful_confluence_certificate()

    for item in rdss_reference_corpus():
        result = certified_irreducible_result(
            system,
            item.value,
            termination=termination,
            confluence=confluence,
        )

        assert system.irreducible(result.value)
        assert (
            result.termination_certificate
            == termination.name
        )
        assert (
            result.confluence_certificate
            == confluence.name
        )
