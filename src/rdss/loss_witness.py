from __future__ import annotations

from dataclasses import dataclass

from .algebra import RelationalPoint, TypedRelation
from .canonical import strict_normal_form
from .closure import (
    RelationalBinaryDistinction,
    RelationalGenerativeModel,
)
from .operations import (
    OccurrenceRelationPath,
    RelationOccurrence,
)
from .rewrite import (
    RewriteStep,
    rdss_forgetful_rewrite_system,
)


class LossWitnessError(RuntimeError):
    pass


@dataclass(frozen=True)
class LossWitness:
    rule_name: str
    source_family: str
    target_family: str
    left: object
    right: object
    left_target: object
    right_target: object
    left_step: RewriteStep
    right_step: RewriteStep
    claim_ids: tuple[str, ...]

    @property
    def sources_distinct(self) -> bool:
        return not strict_normal_form(self.left).same_key(
            strict_normal_form(self.right)
        )

    @property
    def targets_equal(self) -> bool:
        return strict_normal_form(self.left_target).same_key(
            strict_normal_form(self.right_target)
        )

    @property
    def target_key(self) -> object:
        return strict_normal_form(self.left_target).key

    @property
    def verified(self) -> bool:
        try:
            validate_loss_witness(self)
        except LossWitnessError:
            return False
        return True


@dataclass(frozen=True)
class LossWitnessSummary:
    witnesses: int
    verified: int
    distinct_source_pairs: int
    collapsed_target_pairs: int
    irreducible_targets: int


def validate_loss_witness(
    witness: LossWitness,
) -> None:
    system = rdss_forgetful_rewrite_system()

    if not witness.sources_distinct:
        raise LossWitnessError(
            "loss witness sources are not distinct"
        )
    if not witness.targets_equal:
        raise LossWitnessError(
            "loss witness targets do not collapse"
        )

    for source, target, step in (
        (
            witness.left,
            witness.left_target,
            witness.left_step,
        ),
        (
            witness.right,
            witness.right_target,
            witness.right_step,
        ),
    ):
        source_signature = system.signature_engine.signature(
            source
        )
        target_signature = system.signature_engine.signature(
            target
        )
        if source_signature.family != witness.source_family:
            raise LossWitnessError(
                "loss witness source family mismatch"
            )
        if target_signature.family != witness.target_family:
            raise LossWitnessError(
                "loss witness target family mismatch"
            )
        if step.rule_name != witness.rule_name:
            raise LossWitnessError(
                "loss witness rule mismatch"
            )
        if not step.lossy:
            raise LossWitnessError(
                "loss witness step is not LOSSY"
            )
        if not step.verified_invariants:
            raise LossWitnessError(
                "loss witness has no executable invariant evidence"
            )
        if not system.irreducible(target):
            raise LossWitnessError(
                "loss witness target is not irreducible"
            )


def _make_witness(
    rule_name: str,
    left: object,
    right: object,
    *,
    claim_ids: tuple[str, ...],
) -> LossWitness:
    system = rdss_forgetful_rewrite_system()

    left_target, left_step = system.apply(
        left,
        rule_name,
    )
    right_target, right_step = system.apply(
        right,
        rule_name,
    )

    witness = LossWitness(
        rule_name=rule_name,
        source_family=left_step.source_family,
        target_family=left_step.target_family,
        left=left,
        right=right,
        left_target=left_target,
        right_target=right_target,
        left_step=left_step,
        right_step=right_step,
        claim_ids=claim_ids,
    )
    validate_loss_witness(witness)
    return witness


def rdss_forgetful_loss_witnesses(
) -> tuple[LossWitness, ...]:
    root = RelationalPoint()
    left_point = RelationalPoint((-1,))
    relation = TypedRelation(
        root,
        left_point,
        "r",
    )

    occurrence_left = RelationOccurrence(
        relation,
        (),
        (-1,),
    )
    occurrence_right = RelationOccurrence(
        relation,
        (1,),
        (-1,),
    )

    path_left = OccurrenceRelationPath(
        (occurrence_left,)
    )
    path_right = OccurrenceRelationPath(
        (occurrence_right,)
    )

    distinction_left = RelationalBinaryDistinction(
        "a",
        "b",
        "c",
        "r-left",
        "r-right",
    )
    distinction_right = RelationalBinaryDistinction(
        "a",
        "b",
        "c",
        "s-left",
        "s-right",
    )

    generative_left = RelationalGenerativeModel(
        frozenset({"a"}),
        (
            RelationalBinaryDistinction(
                "a",
                "a",
                "a",
                "r-left",
                "r-right",
            ),
        ),
    )
    generative_right = RelationalGenerativeModel(
        frozenset({"a"}),
        (
            RelationalBinaryDistinction(
                "a",
                "a",
                "a",
                "s-left",
                "s-right",
            ),
        ),
    )

    return (
        _make_witness(
            "rewrite:forget_relation_occurrence",
            occurrence_left,
            occurrence_right,
            claim_ids=(
                "DEF_OCCURRENCE_FORGETFUL_PROJECTION",
            ),
        ),
        _make_witness(
            "rewrite:forget_occurrence_path",
            path_left,
            path_right,
            claim_ids=(
                "DEF_OCCURRENCE_FORGETFUL_PROJECTION",
                "THM_OCCURRENCE_COMPOSABILITY_PROJECTS",
            ),
        ),
        _make_witness(
            "rewrite:forget_relational_distinction_binding",
            distinction_left,
            distinction_right,
            claim_ids=(
                "DEF_RELATIONAL_DISTINCTION_FORGETFUL_PROJECTION",
            ),
        ),
        _make_witness(
            "rewrite:forget_relational_generative_binding",
            generative_left,
            generative_right,
            claim_ids=(
                "DEF_RELATIONAL_GENERATIVE_FORGETFUL_PROJECTION",
            ),
        ),
    )


def summarize_forgetful_loss_witnesses(
) -> LossWitnessSummary:
    witnesses = rdss_forgetful_loss_witnesses()
    system = rdss_forgetful_rewrite_system()

    return LossWitnessSummary(
        witnesses=len(witnesses),
        verified=sum(
            witness.verified
            for witness in witnesses
        ),
        distinct_source_pairs=sum(
            witness.sources_distinct
            for witness in witnesses
        ),
        collapsed_target_pairs=sum(
            witness.targets_equal
            for witness in witnesses
        ),
        irreducible_targets=sum(
            system.irreducible(witness.left_target)
            and system.irreducible(witness.right_target)
            for witness in witnesses
        ),
    )
