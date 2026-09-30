import pytest

from rdss.bridges import (
    UnsupportedBridgeError,
    rdss_bridge_registry,
)
from rdss.loss_witness import (
    rdss_forgetful_loss_witnesses,
    summarize_forgetful_loss_witnesses,
)


def test_reference_forgetful_loss_witness_summary():
    summary = summarize_forgetful_loss_witnesses()

    assert summary.witnesses == 4
    assert summary.verified == 4
    assert summary.distinct_source_pairs == 4
    assert summary.collapsed_target_pairs == 4
    assert summary.irreducible_targets == 4


def test_each_reference_forgetful_rule_has_one_noninjectivity_witness():
    witnesses = rdss_forgetful_loss_witnesses()

    assert {
        witness.rule_name
        for witness in witnesses
    } == {
        "rewrite:forget_relation_occurrence",
        "rewrite:forget_occurrence_path",
        "rewrite:forget_relational_distinction_binding",
        "rewrite:forget_relational_generative_binding",
    }

    assert all(witness.verified for witness in witnesses)
    assert all(
        witness.sources_distinct
        for witness in witnesses
    )
    assert all(
        witness.targets_equal
        for witness in witnesses
    )


def test_loss_witnesses_carry_executable_invariant_evidence():
    for witness in rdss_forgetful_loss_witnesses():
        assert witness.left_step.verified_invariants
        assert witness.right_step.verified_invariants
        assert witness.left_step.lossy
        assert witness.right_step.lossy


def test_noninjectivity_witnesses_have_no_global_reverse_bridge():
    registry = rdss_bridge_registry()

    for witness in rdss_forgetful_loss_witnesses():
        with pytest.raises(UnsupportedBridgeError):
            registry.direct(
                witness.left_target,
                witness.source_family,
            )


def test_loss_witness_targets_are_strictly_the_same_for_each_pair():
    for witness in rdss_forgetful_loss_witnesses():
        assert witness.left_target == witness.right_target
        assert witness.target_key is not None
