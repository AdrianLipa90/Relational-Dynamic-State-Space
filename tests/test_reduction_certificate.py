from dataclasses import replace

import pytest

from rdss import (
    RelationalPoint,
    TypedRelation,
)
from rdss.corpus import rdss_reference_corpus
from rdss.operations import RelationOccurrence
from rdss.reduction_certificate import (
    ReductionCertificateError,
    certify_forgetful_reduction,
    validate_reduction_certificate,
)
from rdss.rewrite import rdss_forgetful_rewrite_system


def assert_topological(graph):
    position = {
        claim_id: index
        for index, claim_id
        in enumerate(graph.ordered_claim_ids)
    }
    for edge in graph.edges:
        assert position[edge.depends_on] < position[edge.claim_id]


def test_rewritten_object_certificate_binds_full_reduction_evidence():
    point = RelationalPoint()
    relation = TypedRelation(point, point, "r")
    occurrence = RelationOccurrence(
        relation,
        (),
        (-1,),
    )

    certificate = certify_forgetful_reduction(
        occurrence
    )

    assert certificate.verified
    assert certificate.rewritten
    assert certificate.lossy
    assert not certificate.global_canonical
    assert certificate.scope == "rdss-reference-forgetful-v1"
    assert certificate.source_family == "relation_occurrence"
    assert certificate.target_family == "typed_relation"
    assert certificate.rewrite_trace.rule_names == (
        "rewrite:forget_relation_occurrence",
    )
    assert certificate.verified_invariants == (
        "typed relation value",
    )
    assert "REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE" in (
        certificate.root_claim_ids
    )
    assert "REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE" in (
        certificate.root_claim_ids
    )
    assert "REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE" in (
        certificate.root_claim_ids
    )
    assert_topological(certificate.claim_graph)


def test_fixed_point_certificate_records_no_rewrite_and_no_loss():
    point = RelationalPoint((-1,))

    certificate = certify_forgetful_reduction(
        point
    )

    assert certificate.verified
    assert not certificate.rewritten
    assert not certificate.lossy
    assert certificate.rewrite_trace.steps == ()
    assert certificate.verified_invariants == ()
    assert certificate.source.factorization == (
        certificate.target.factorization
    )
    assert certificate.normal_form.source_key == (
        certificate.normal_form.target_key
    )


def test_every_reference_corpus_value_receives_verified_certificate():
    system = rdss_forgetful_rewrite_system()
    rewritten = 0
    fixed = 0

    for item in rdss_reference_corpus():
        certificate = certify_forgetful_reduction(
            item.value
        )

        assert certificate.verified
        assert not certificate.global_canonical
        assert system.irreducible(
            certificate.rewrite_trace.value
        )
        assert certificate.claim_graph.roots == (
            certificate.root_claim_ids
        )
        assert_topological(certificate.claim_graph)

        if certificate.rewritten:
            rewritten += 1
            assert certificate.lossy
        else:
            fixed += 1
            assert not certificate.lossy

    assert rewritten == 5
    assert fixed == 31


def test_certificate_claim_graph_contains_source_target_and_scope_evidence():
    point = RelationalPoint()
    relation = TypedRelation(point, point, "r")
    occurrence = RelationOccurrence(
        relation,
        (),
        (-1,),
    )

    certificate = certify_forgetful_reduction(
        occurrence
    )
    claims = set(
        certificate.claim_graph.ordered_claim_ids
    )

    assert "DEF_RELATION_OCCURRENCE" in claims
    assert "DEF_BINARY_REL" in claims
    assert "DEF_OCCURRENCE_FORGETFUL_PROJECTION" in claims
    assert "REF_FORGETFUL_SCOPED_NORMAL_FORM" in claims
    assert "THM_REFERENCE_FORGETFUL_REWRITE_TERMINATES" in claims
    assert "THM_REFERENCE_FORGETFUL_REWRITE_CONFLUENT" in claims
    assert "REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE" in claims


def test_tampered_certificate_fails_executable_validation():
    certificate = certify_forgetful_reduction(
        RelationalPoint()
    )
    bad_normal_form = replace(
        certificate.normal_form,
        target_key=("tampered",),
    )
    bad = replace(
        certificate,
        normal_form=bad_normal_form,
    )

    assert not bad.verified

    with pytest.raises(ReductionCertificateError):
        validate_reduction_certificate(bad)
