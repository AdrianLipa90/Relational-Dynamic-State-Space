from rdss.canonical import strict_normal_form
from rdss.corpus import rdss_reference_corpus
from rdss.normal_form import (
    rdss_forgetful_normal_form,
)
from rdss.rewrite import rdss_forgetful_rewrite_system


def test_reference_forgetful_normal_form_is_scoped_not_global():
    for item in rdss_reference_corpus():
        result = rdss_forgetful_normal_form(
            item.value
        )

        assert result.scope == "rdss-reference-forgetful-v1"
        assert not result.global_canonical


def test_reference_forgetful_normal_form_is_irreducible():
    system = rdss_forgetful_rewrite_system()

    for item in rdss_reference_corpus():
        result = rdss_forgetful_normal_form(
            item.value
        )

        assert system.irreducible(result.value)


def test_reference_forgetful_normal_form_is_idempotent():
    for item in rdss_reference_corpus():
        first = rdss_forgetful_normal_form(
            item.value
        )
        second = rdss_forgetful_normal_form(
            first.value
        )

        assert second.rule_names == ()
        assert second.target_key == first.target_key
        assert strict_normal_form(
            second.value
        ).same_key(
            strict_normal_form(first.value)
        )


def test_reference_corpus_has_five_lossy_rewrites_and_thirty_one_fixed_points():
    rewritten = []
    fixed = []

    for item in rdss_reference_corpus():
        result = rdss_forgetful_normal_form(
            item.value
        )
        if result.rewritten:
            rewritten.append(
                (item.name, result)
            )
        else:
            fixed.append(
                (item.name, result)
            )

    assert len(rewritten) == 5
    assert len(fixed) == 31
    assert all(result.lossy for _, result in rewritten)
    assert all(not result.lossy for _, result in fixed)


def test_reference_forgetful_normal_form_preserves_certificate_provenance():
    for item in rdss_reference_corpus():
        result = rdss_forgetful_normal_form(
            item.value
        )

        assert (
            result.termination_certificate
            == "rdss-forgetful-family-rank-v1"
        )
        assert (
            result.confluence_certificate
            == "rdss-forgetful-distinct-source-family-v1"
        )
        assert result.claim_ids == (
            "REF_FORGETFUL_SCOPED_NORMAL_FORM",
            "THM_REFERENCE_FORGETFUL_UNIQUE_IRREDUCIBLE",
        )
