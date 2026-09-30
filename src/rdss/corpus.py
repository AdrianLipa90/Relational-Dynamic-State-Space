from __future__ import annotations

from dataclasses import dataclass

from .algebra import (
    OccurrenceAddress,
    RelationalPoint,
    SemanticScale,
    SemanticScaleGraph,
    TensorScalarElement,
    TypedRelation,
    TypedZero,
)
from .closure import (
    BinaryDistinction,
    BranchRelationOccurrence,
    GenerativeRelationModel,
    RelationalBinaryDistinction,
    RelationalGenerativeModel,
)
from .equivalence_graph import (
    BridgeEquivalenceGraph,
    BridgeGapReport,
    build_bridge_equivalence_graph,
)
from .operations import (
    OccurrenceRelationPath,
    RelationOccurrence,
    RelationPath,
)
from .orbital_information import (
    CenterHalfTurnBridge,
    HilbertMoireFibreState,
)
from .phase import U1Phase
from .realizations import (
    CP1State,
    MinimalDistinction,
    MoireRotation,
)
from .signature import (
    NoveltyKind,
    SignatureCatalogSummary,
    UnsupportedSignatureError,
    rdss_signature_catalog,
    rdss_signature_engine,
)
from .zero_axis import ZeroAxisPoint


@dataclass(frozen=True)
class CorpusItem:
    name: str
    value: object
    source_claim_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("corpus item name must be non-empty")
        if any(not item.strip() for item in self.source_claim_ids):
            raise ValueError("corpus claim ids must be non-empty")


@dataclass(frozen=True)
class CorpusCoverageGap:
    name: str
    representation: str
    reason: str


@dataclass(frozen=True)
class CorpusNovelty:
    name: str
    novelty: NoveltyKind
    family: str


@dataclass(frozen=True)
class CorpusScanResult:
    items: tuple[CorpusItem, ...]
    supported_items: tuple[CorpusItem, ...]
    coverage_gaps: tuple[CorpusCoverageGap, ...]
    novelty: tuple[CorpusNovelty, ...]
    catalog_summary: SignatureCatalogSummary
    equivalence_graph: BridgeEquivalenceGraph

    @property
    def coverage_complete(self) -> bool:
        return not self.coverage_gaps

    @property
    def bridge_gap_report(self) -> BridgeGapReport:
        return self.equivalence_graph.bridge_gap_report()

    @property
    def novelty_counts(self) -> dict[NoveltyKind, int]:
        counts = {kind: 0 for kind in NoveltyKind}
        for item in self.novelty:
            counts[item.novelty] += 1
        return counts


def _type_tag(value: object) -> str:
    cls = type(value)
    return f"{cls.__module__}.{cls.__qualname__}"


def rdss_reference_corpus() -> tuple[CorpusItem, ...]:
    """Build a finite corpus from actual executable RDSS reference types.

    The corpus historically exposed signature-coverage gaps. The current
    registry covers every value in this reference corpus, while the scanner
    still preserves explicit coverage-gap reporting for future corpus growth.
    """
    occ_root = OccurrenceAddress()
    occ_left = OccurrenceAddress((-1,))
    point_root = RelationalPoint()
    point_left = RelationalPoint((-1,))
    scale_object = SemanticScale("object")

    scalar_one = TensorScalarElement(
        (1 + 0j,),
        (0, 0),
        point_root,
        scale_object,
    )
    scalar_zero = TensorScalarElement(
        (0 + 0j,),
        (0, 0),
        point_root,
        scale_object,
    )
    scalar_two = TensorScalarElement(
        (2 + 0j,),
        (0, 0),
        point_root,
        scale_object,
    )
    rank_one = TensorScalarElement(
        (1 + 0j,),
        (1, 0),
        point_root,
        scale_object,
    )

    down = TypedRelation(point_root, point_left, "down")
    up = TypedRelation(point_left, point_root, "up")
    occ_down = RelationOccurrence(
        down,
        occ_root,
        occ_left,
    )
    occ_up = RelationOccurrence(
        up,
        occ_left,
        occ_root,
    )
    relation_cycle = RelationPath((down, up))
    occurrence_cycle = OccurrenceRelationPath(
        (occ_down, occ_up)
    )

    cp1_north = CP1State(1 + 0j, 0 + 0j)
    cp1_south = CP1State(0 + 0j, 1 + 0j)
    cp1_north_phase = CP1State(0 + 1j, 0 + 0j)

    hilbert_q1 = HilbertMoireFibreState(
        occ_left,
        "orbital-A",
        0.25,
        (1 + 0j, 0 + 1j),
    )
    hilbert_q2 = HilbertMoireFibreState(
        occ_left,
        "orbital-A",
        0.5,
        (1 + 0j, 0 + 1j),
    )
    hilbert_orbit_b = HilbertMoireFibreState(
        occ_left,
        "orbital-B",
        0.25,
        (1 + 0j, 0 + 1j),
    )

    distinction = BinaryDistinction("a", "b", "c")
    zero_axis_reference = ZeroAxisPoint(1.0)
    zero_axis_phase = U1Phase(zero_axis_reference.omega)

    return (
        CorpusItem(
            "occ-root",
            occ_root,
            ("DEF_OCCURRENCE_ADDRESS_SPACE",),
        ),
        CorpusItem(
            "occ-left",
            occ_left,
            ("DEF_OCCURRENCE_ADDRESS_SPACE",),
        ),
        CorpusItem(
            "occ-left-repeat",
            OccurrenceAddress((-1,)),
            ("DEF_OCCURRENCE_ADDRESS_SPACE",),
        ),
        CorpusItem(
            "point-root",
            point_root,
            ("DEF_POINT",),
        ),
        CorpusItem(
            "point-left",
            point_left,
            ("DEF_POINT",),
        ),
        CorpusItem(
            "scale-object",
            scale_object,
            ("PRIM_SCALE",),
        ),
        CorpusItem(
            "tensor-scalar-one",
            scalar_one,
            ("DEF_TS", "PRIM_MODULE"),
        ),
        CorpusItem(
            "tensor-scalar-zero",
            scalar_zero,
            ("DEF_TS", "PRIM_MODULE", "DEF_TYPED_ZERO"),
        ),
        CorpusItem(
            "tensor-scalar-two",
            scalar_two,
            ("DEF_TS", "PRIM_MODULE"),
        ),
        CorpusItem(
            "tensor-rank-one",
            rank_one,
            ("DEF_TS", "PRIM_MODULE"),
        ),
        CorpusItem(
            "relation-down",
            down,
            ("DEF_BINARY_REL",),
        ),
        CorpusItem(
            "relation-up",
            up,
            ("DEF_BINARY_REL",),
        ),
        CorpusItem(
            "relation-occurrence-down",
            occ_down,
            ("DEF_RELATION_OCCURRENCE",),
        ),
        CorpusItem(
            "relation-occurrence-up",
            occ_up,
            ("DEF_RELATION_OCCURRENCE",),
        ),
        CorpusItem(
            "relation-cycle",
            relation_cycle,
            ("DEF_BINARY_REL",),
        ),
        CorpusItem(
            "occurrence-cycle",
            occurrence_cycle,
            ("DEF_OCCURRENCE_PATH",),
        ),
        CorpusItem(
            "hilbert-moire-q-quarter",
            hilbert_q1,
            ("REF_HILBERT_MOIRE_FIBRE",),
        ),
        CorpusItem(
            "hilbert-moire-q-half",
            hilbert_q2,
            ("REF_HILBERT_MOIRE_FIBRE",),
        ),
        CorpusItem(
            "hilbert-moire-orbit-b",
            hilbert_orbit_b,
            ("REF_HILBERT_MOIRE_FIBRE",),
        ),
        CorpusItem(
            "cp1-north",
            cp1_north,
            ("REF_CP1",),
        ),
        CorpusItem(
            "cp1-south",
            cp1_south,
            ("REF_CP1",),
        ),
        CorpusItem(
            "cp1-north-global-phase",
            cp1_north_phase,
            ("REF_CP1",),
        ),
        CorpusItem(
            "moire-base",
            MoireRotation(1.0, 0.25),
            ("DER_MOIRE",),
        ),
        CorpusItem(
            "moire-common-shift",
            MoireRotation(2.0, 1.25),
            ("DER_MOIRE",),
        ),
        CorpusItem(
            "moire-new-delta",
            MoireRotation(1.0, 0.0),
            ("DER_MOIRE",),
        ),
        CorpusItem(
            "typed-zero",
            TypedZero.from_element(scalar_one),
            ("DEF_TYPED_ZERO",),
        ),
        CorpusItem(
            "semantic-scale-graph",
            SemanticScaleGraph(
                (("object", "system"),)
            ),
            ("PRIM_SCALE",),
        ),
        CorpusItem(
            "minimal-distinction",
            MinimalDistinction(
                point_root,
                cp1_north,
                cp1_south,
            ),
            ("REF_CP1",),
        ),
        CorpusItem(
            "center-half-turn-bridge",
            CenterHalfTurnBridge(),
            ("BRIDGE_CENTER_HALF_TURN",),
        ),
        CorpusItem(
            "zero-axis-point",
            zero_axis_reference,
            ("ZA_BRIDGE",),
        ),
        CorpusItem(
            "u1-zero-axis-companion",
            zero_axis_phase,
            ("REF_U1_PHASE_VALUE",),
        ),
        CorpusItem(
            "binary-distinction",
            distinction,
            ("DEF_BINARY_DISTINCTION",),
        ),
        CorpusItem(
            "branch-relation-occurrence",
            BranchRelationOccurrence(
                -1,
                "r-left",
                "a",
                "b",
            ),
            ("DEF_RELATIONAL_DISTINCTION",),
        ),
        CorpusItem(
            "relational-binary-distinction",
            RelationalBinaryDistinction(
                "a",
                "b",
                "c",
                "r-left",
                "r-right",
            ),
            ("DEF_RELATIONAL_DISTINCTION",),
        ),
        CorpusItem(
            "relational-generative-relation-model",
            RelationalGenerativeModel(
                frozenset({"a", "b", "c"}),
                (
                    RelationalBinaryDistinction(
                        "a",
                        "b",
                        "c",
                        "r-left",
                        "r-right",
                    ),
                ),
            ),
            ("RA0_REL_STAR",),
        ),
        CorpusItem(
            "generative-relation-model",
            GenerativeRelationModel(
                frozenset({"a", "b", "c"}),
                (distinction,),
            ),
            ("RA0_STAR",),
        ),
    )


def scan_rdss_reference_corpus(
    items: tuple[CorpusItem, ...] | None = None,
) -> CorpusScanResult:
    corpus = items or rdss_reference_corpus()
    signature_engine = rdss_signature_engine()

    supported: list[CorpusItem] = []
    gaps: list[CorpusCoverageGap] = []

    for item in corpus:
        try:
            signature_engine.signature(item.value)
        except UnsupportedSignatureError as exc:
            gaps.append(
                CorpusCoverageGap(
                    name=item.name,
                    representation=_type_tag(item.value),
                    reason=str(exc),
                )
            )
        else:
            supported.append(item)

    catalog = rdss_signature_catalog()
    novelty: list[CorpusNovelty] = []
    for item in supported:
        assessment = catalog.add(item.value)
        novelty.append(
            CorpusNovelty(
                name=item.name,
                novelty=assessment.novelty,
                family=assessment.signature.family,
            )
        )

    graph = build_bridge_equivalence_graph(
        tuple(item.value for item in supported)
    )

    return CorpusScanResult(
        items=corpus,
        supported_items=tuple(supported),
        coverage_gaps=tuple(gaps),
        novelty=tuple(novelty),
        catalog_summary=catalog.summary(),
        equivalence_graph=graph,
    )
