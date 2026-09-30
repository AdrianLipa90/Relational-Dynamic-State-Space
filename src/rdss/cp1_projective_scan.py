from __future__ import annotations

from dataclasses import dataclass

from .corpus import (
    CorpusItem,
    rdss_reference_corpus,
)
from .cp1_projective import (
    CP1ProjectivePoint,
    quotient_cp1_states,
)
from .factorization import (
    factorize_value,
    summarize_factorizations,
)
from .realizations import CP1State


@dataclass(frozen=True)
class CP1ProjectiveScanItem:
    name: str
    raw_semantic_key: object
    projective_point: CP1ProjectivePoint
    projective_class: int


@dataclass(frozen=True)
class CP1ProjectiveScanSummary:
    corpus_records: int
    raw_semantic_states: int
    cp1_records: int
    cp1_raw_semantic_states: int
    cp1_projective_classes: int
    collapsed_cp1_representatives: int
    cp1_projective_adjusted_semantic_states: int


@dataclass(frozen=True)
class CP1ProjectiveScan:
    items: tuple[CP1ProjectiveScanItem, ...]
    summary: CP1ProjectiveScanSummary


def scan_reference_cp1_projective_quotient(
    corpus: tuple[CorpusItem, ...] | None = None,
) -> CP1ProjectiveScan:
    items = corpus or rdss_reference_corpus()
    factor_summary = summarize_factorizations(
        tuple(item.value for item in items)
    )

    cp1_items = tuple(
        item
        for item in items
        if isinstance(item.value, CP1State)
    )
    cp1_states = tuple(
        item.value
        for item in cp1_items
    )
    quotient = quotient_cp1_states(cp1_states)

    class_by_index: dict[int, int] = {}
    for class_index, projective_class in enumerate(
        quotient.classes
    ):
        for member_index in projective_class.member_indices:
            class_by_index[member_index] = class_index

    scan_items = tuple(
        CP1ProjectiveScanItem(
            name=item.name,
            raw_semantic_key=(
                factorize_value(item.value).semantic_key
            ),
            projective_point=quotient.points[index],
            projective_class=class_by_index[index],
        )
        for index, item in enumerate(cp1_items)
    )

    cp1_raw_semantic_states = len(
        {
            item.raw_semantic_key
            for item in scan_items
        }
    )
    collapse = (
        cp1_raw_semantic_states
        - quotient.summary.projective_classes
    )

    return CP1ProjectiveScan(
        items=scan_items,
        summary=CP1ProjectiveScanSummary(
            corpus_records=len(items),
            raw_semantic_states=(
                factor_summary.semantic_states
            ),
            cp1_records=len(cp1_items),
            cp1_raw_semantic_states=(
                cp1_raw_semantic_states
            ),
            cp1_projective_classes=(
                quotient.summary.projective_classes
            ),
            collapsed_cp1_representatives=collapse,
            cp1_projective_adjusted_semantic_states=(
                factor_summary.semantic_states - collapse
            ),
        ),
    )
