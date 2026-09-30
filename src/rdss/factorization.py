from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .signature import (
    RDSSSignature,
    SignatureAxis,
    SignatureEngine,
    rdss_signature_engine,
)


class FactorizationRelation(str, Enum):
    SAME_FACTORIZATION = "same_factorization"
    REPRESENTATION_ONLY = "representation_only"
    DIFFERENT_STATE = "different_state"
    DIFFERENT_STRUCTURE = "different_structure"
    DIFFERENT_FAMILY = "different_family"


@dataclass(frozen=True)
class SemanticFactorization:
    """Explicit family/structure/state/representation factorization."""

    family: str
    structure_axes: tuple[tuple[SignatureAxis, object], ...]
    state_axes: tuple[tuple[SignatureAxis, object], ...]
    structure_key: object
    state_key: object
    semantic_key: object
    representation: str
    provenance: tuple[str, ...]
    claim_ids: tuple[str, ...]

    @classmethod
    def from_signature(
        cls,
        signature: RDSSSignature,
    ) -> "SemanticFactorization":
        return cls(
            family=signature.family,
            structure_axes=signature.structural_axes,
            state_axes=signature.state_axes,
            structure_key=signature.structural_key,
            state_key=signature.state_key,
            semantic_key=signature.semantic_key,
            representation=signature.representation,
            provenance=signature.provenance,
            claim_ids=signature.claim_ids,
        )

    @property
    def tuple4(self) -> tuple[object, ...]:
        return (
            self.family,
            self.structure_key,
            self.state_key,
            self.representation,
        )


@dataclass(frozen=True)
class FactorizationComparison:
    left: SemanticFactorization
    right: SemanticFactorization
    relation: FactorizationRelation
    same_family: bool
    same_structure: bool
    same_state: bool
    same_representation: bool


@dataclass(frozen=True)
class FactorizationSummary:
    records: int
    families: int
    structures: int
    semantic_states: int
    representations: int


def factorize_signature(
    signature: RDSSSignature,
) -> SemanticFactorization:
    return SemanticFactorization.from_signature(signature)


def factorize_value(
    value: object,
    *,
    signature_engine: SignatureEngine | None = None,
) -> SemanticFactorization:
    engine = signature_engine or rdss_signature_engine()
    return factorize_signature(
        engine.signature(value)
    )


def compare_factorizations(
    left: object,
    right: object,
    *,
    signature_engine: SignatureEngine | None = None,
) -> FactorizationComparison:
    engine = signature_engine or rdss_signature_engine()
    left_factor = factorize_value(
        left,
        signature_engine=engine,
    )
    right_factor = factorize_value(
        right,
        signature_engine=engine,
    )

    same_family = (
        left_factor.family
        == right_factor.family
    )
    same_structure = (
        same_family
        and left_factor.structure_key
        == right_factor.structure_key
    )
    same_state = (
        same_structure
        and left_factor.state_key
        == right_factor.state_key
    )
    same_representation = (
        left_factor.representation
        == right_factor.representation
    )

    if not same_family:
        relation = FactorizationRelation.DIFFERENT_FAMILY
    elif not same_structure:
        relation = FactorizationRelation.DIFFERENT_STRUCTURE
    elif not same_state:
        relation = FactorizationRelation.DIFFERENT_STATE
    elif not same_representation:
        relation = FactorizationRelation.REPRESENTATION_ONLY
    else:
        relation = FactorizationRelation.SAME_FACTORIZATION

    return FactorizationComparison(
        left=left_factor,
        right=right_factor,
        relation=relation,
        same_family=same_family,
        same_structure=same_structure,
        same_state=same_state,
        same_representation=same_representation,
    )


def summarize_factorizations(
    values: Iterable[object],
    *,
    signature_engine: SignatureEngine | None = None,
) -> FactorizationSummary:
    engine = signature_engine or rdss_signature_engine()
    factors = tuple(
        factorize_value(
            value,
            signature_engine=engine,
        )
        for value in values
    )

    return FactorizationSummary(
        records=len(factors),
        families=len(
            {factor.family for factor in factors}
        ),
        structures=len(
            {factor.structure_key for factor in factors}
        ),
        semantic_states=len(
            {factor.semantic_key for factor in factors}
        ),
        representations=len(
            {factor.representation for factor in factors}
        ),
    )
