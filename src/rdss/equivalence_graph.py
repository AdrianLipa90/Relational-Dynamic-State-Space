from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .bridges import (
    AmbiguousBridgeError,
    BridgeRegistry,
    UnsupportedBridgeError,
    rdss_bridge_registry,
)
from .canonical import strict_normal_form
from .signature import (
    RDSSSignature,
    SignatureComparisonKind,
)


class GraphEdgeKind(str, Enum):
    SIGNATURE_EQUIVALENCE = "signature_equivalence"
    LOSSLESS_BRIDGE = "lossless_bridge"
    LOSSY_PROJECTION = "lossy_projection"
    UNKNOWN_BRIDGE = "unknown_bridge"


@dataclass(frozen=True)
class EquivalenceGraphRecord:
    ordinal: int
    value: object
    signature: RDSSSignature
    strict_key: object


@dataclass(frozen=True)
class EquivalenceGraphEdge:
    source: int
    target: int
    kind: GraphEdgeKind
    provenance: tuple[str, ...] = ()
    claim_ids: tuple[str, ...] = ()

    @property
    def strong_equivalence(self) -> bool:
        return self.kind in {
            GraphEdgeKind.SIGNATURE_EQUIVALENCE,
            GraphEdgeKind.LOSSLESS_BRIDGE,
        }


@dataclass(frozen=True)
class EquivalenceGraphSummary:
    records: int
    equivalence_components: int
    strong_edges: int
    lossy_projection_edges: int
    unknown_bridge_edges: int
    unresolved_cross_family_pairs: int


@dataclass(frozen=True)
class BridgeGap:
    left_family: str
    right_family: str
    pairs: tuple[tuple[int, int], ...]

    @property
    def count(self) -> int:
        return len(self.pairs)


@dataclass(frozen=True)
class BridgeGapReport:
    gaps: tuple[BridgeGap, ...]

    @property
    def unresolved_pairs(self) -> int:
        return sum(gap.count for gap in self.gaps)

    @property
    def family_pairs(self) -> int:
        return len(self.gaps)


@dataclass(frozen=True)
class BridgeEquivalenceGraph:
    records: tuple[EquivalenceGraphRecord, ...]
    edges: tuple[EquivalenceGraphEdge, ...]
    components: tuple[tuple[int, ...], ...]
    unresolved_cross_family_pairs: tuple[tuple[int, int], ...]

    @property
    def strong_edges(self) -> tuple[EquivalenceGraphEdge, ...]:
        return tuple(
            edge for edge in self.edges
            if edge.strong_equivalence
        )

    @property
    def lossy_projection_edges(self) -> tuple[EquivalenceGraphEdge, ...]:
        return tuple(
            edge for edge in self.edges
            if edge.kind is GraphEdgeKind.LOSSY_PROJECTION
        )

    @property
    def unknown_bridge_edges(self) -> tuple[EquivalenceGraphEdge, ...]:
        return tuple(
            edge for edge in self.edges
            if edge.kind is GraphEdgeKind.UNKNOWN_BRIDGE
        )

    def component_of(self, ordinal: int) -> tuple[int, ...]:
        if ordinal < 0 or ordinal >= len(self.records):
            raise IndexError("record ordinal out of range")
        for component in self.components:
            if ordinal in component:
                return component
        raise RuntimeError("record is missing from equivalence components")

    def bridge_gap_report(self) -> BridgeGapReport:
        grouped: dict[
            tuple[str, str],
            list[tuple[int, int]],
        ] = {}
        for left, right in self.unresolved_cross_family_pairs:
            left_family = self.records[left].signature.family
            right_family = self.records[right].signature.family
            family_pair = tuple(
                sorted(
                    (left_family, right_family)
                )
            )
            grouped.setdefault(
                family_pair,
                [],
            ).append((left, right))

        gaps = tuple(
            BridgeGap(
                left_family=family_pair[0],
                right_family=family_pair[1],
                pairs=tuple(grouped[family_pair]),
            )
            for family_pair in sorted(grouped)
        )
        return BridgeGapReport(gaps)

    def summary(self) -> EquivalenceGraphSummary:
        return EquivalenceGraphSummary(
            records=len(self.records),
            equivalence_components=len(self.components),
            strong_edges=len(self.strong_edges),
            lossy_projection_edges=len(self.lossy_projection_edges),
            unknown_bridge_edges=len(self.unknown_bridge_edges),
            unresolved_cross_family_pairs=len(
                self.unresolved_cross_family_pairs
            ),
        )


class _UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, item: int) -> int:
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(self, left: int, right: int) -> None:
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return
        if self.rank[root_left] < self.rank[root_right]:
            root_left, root_right = root_right, root_left
        self.parent[root_right] = root_left
        if self.rank[root_left] == self.rank[root_right]:
            self.rank[root_left] += 1


def _claim_ids_from_route(route) -> tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            claim_id
            for step in route.steps
            for claim_id in step.claim_ids
        )
    )


def build_bridge_equivalence_graph(
    values: tuple[object, ...],
    *,
    registry: BridgeRegistry | None = None,
    max_hops: int = 4,
) -> BridgeEquivalenceGraph:
    """Build a finite quotient graph without collapsing lossy projections.

    Strong components are generated only by same-family semantic signature
    equivalence or by explicit fully reversible LOSSLESS bridge routes whose
    transformed endpoint matches the target semantic signature.
    """
    if max_hops <= 0:
        raise ValueError("max_hops must be positive")

    bridge_registry = registry or rdss_bridge_registry()
    signature_engine = bridge_registry.signature_engine

    records = tuple(
        EquivalenceGraphRecord(
            ordinal=index,
            value=value,
            signature=signature_engine.signature(value),
            strict_key=strict_normal_form(value).key,
        )
        for index, value in enumerate(values)
    )
    union = _UnionFind(len(records))
    edges: list[EquivalenceGraphEdge] = []
    unresolved: list[tuple[int, int]] = []
    edge_keys: set[tuple[object, ...]] = set()

    def add_edge(edge: EquivalenceGraphEdge) -> None:
        key = (
            edge.source,
            edge.target,
            edge.kind,
            edge.provenance,
        )
        if key not in edge_keys:
            edge_keys.add(key)
            edges.append(edge)

    for i, left_record in enumerate(records):
        for j in range(i + 1, len(records)):
            right_record = records[j]

            if (
                left_record.signature.family
                == right_record.signature.family
            ):
                comparison = signature_engine.compare(
                    left_record.value,
                    right_record.value,
                )
                if comparison.kind in {
                    SignatureComparisonKind.EXACT_SIGNATURE,
                    SignatureComparisonKind
                    .SAME_SEMANTIC_STATE_DIFFERENT_REPRESENTATION,
                }:
                    union.union(i, j)
                    add_edge(
                        EquivalenceGraphEdge(
                            source=i,
                            target=j,
                            kind=GraphEdgeKind.SIGNATURE_EQUIVALENCE,
                            provenance=(
                                "same-family-semantic-signature",
                            ),
                            claim_ids=(
                                "DEF_SIGNATURE_COMPARISON",
                            ),
                        )
                    )
                continue

            pair_has_bridge = False
            pair_has_strong_bridge = False

            for source, target in ((i, j), (j, i)):
                source_record = records[source]
                target_record = records[target]
                try:
                    result = bridge_registry.compare(
                        source_record.value,
                        target_record.value,
                        allow_lossy=True,
                        max_hops=max_hops,
                    )
                except UnsupportedBridgeError:
                    continue
                except AmbiguousBridgeError:
                    raise

                if not result.equivalent_after_bridge:
                    continue

                pair_has_bridge = True
                route = result.route
                claim_ids = _claim_ids_from_route(route)

                if route.fully_reversible:
                    pair_has_strong_bridge = True
                    union.union(source, target)
                    add_edge(
                        EquivalenceGraphEdge(
                            source=min(source, target),
                            target=max(source, target),
                            kind=GraphEdgeKind.LOSSLESS_BRIDGE,
                            provenance=route.provenance,
                            claim_ids=claim_ids,
                        )
                    )
                    break

                if route.lossy:
                    add_edge(
                        EquivalenceGraphEdge(
                            source=source,
                            target=target,
                            kind=GraphEdgeKind.LOSSY_PROJECTION,
                            provenance=route.provenance,
                            claim_ids=claim_ids,
                        )
                    )
                else:
                    add_edge(
                        EquivalenceGraphEdge(
                            source=source,
                            target=target,
                            kind=GraphEdgeKind.UNKNOWN_BRIDGE,
                            provenance=route.provenance,
                            claim_ids=claim_ids,
                        )
                    )

            if not pair_has_bridge and not pair_has_strong_bridge:
                unresolved.append((i, j))

    groups: dict[int, list[int]] = {}
    for record in records:
        root = union.find(record.ordinal)
        groups.setdefault(root, []).append(record.ordinal)

    components = tuple(
        tuple(group)
        for _, group in sorted(
            groups.items(),
            key=lambda item: min(item[1]),
        )
    )

    return BridgeEquivalenceGraph(
        records=records,
        edges=tuple(edges),
        components=components,
        unresolved_cross_family_pairs=tuple(unresolved),
    )
