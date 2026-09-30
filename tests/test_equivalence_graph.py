from rdss import (
    OccurrenceAddress,
    RelationalPoint,
    SemanticScale,
    TensorScalarElement,
    TypedRelation,
)
from rdss.equivalence_graph import (
    GraphEdgeKind,
    build_bridge_equivalence_graph,
)
from rdss.operations import RelationOccurrence
from rdss.realizations import MoireRotation


def element(value, *, rank=(0, 0)):
    return TensorScalarElement(
        (complex(value),),
        rank,
        RelationalPoint(),
        SemanticScale("object"),
    )


def test_lossless_reference_bridge_unions_occurrence_and_reference_point():
    graph = build_bridge_equivalence_graph(
        (
            OccurrenceAddress((-1, 1)),
            RelationalPoint((-1, 1)),
        )
    )

    assert graph.components == ((0, 1),)
    assert len(graph.strong_edges) == 1
    assert graph.strong_edges[0].kind is GraphEdgeKind.LOSSLESS_BRIDGE
    assert graph.strong_edges[0].claim_ids == (
        "DEF_CARRIER_OCCURRENCE_SEPARATION",
        "REF_RELATIONAL_POINT_BINARY_COORDINATE",
    )


def test_lossy_forgetful_projection_does_not_union_components():
    carrier = RelationalPoint()
    relation = TypedRelation(carrier, carrier, "r")
    occurrence = RelationOccurrence(
        relation,
        (),
        (-1,),
    )

    graph = build_bridge_equivalence_graph(
        (occurrence, relation)
    )

    assert graph.components == ((0,), (1,))
    assert len(graph.lossy_projection_edges) == 1
    edge = graph.lossy_projection_edges[0]
    assert edge.source == 0
    assert edge.target == 1
    assert edge.kind is GraphEdgeKind.LOSSY_PROJECTION


def test_same_family_signature_equivalence_unions_shifted_moire_payloads():
    graph = build_bridge_equivalence_graph(
        (
            MoireRotation(1.0, 0.25),
            MoireRotation(2.0, 1.25),
        )
    )

    assert graph.components == ((0, 1),)
    assert graph.strong_edges[0].kind is GraphEdgeKind.SIGNATURE_EQUIVALENCE


def test_same_structure_different_state_does_not_union():
    graph = build_bridge_equivalence_graph(
        (
            element(1),
            element(2),
        )
    )

    assert graph.components == ((0,), (1,))
    assert not graph.edges


def test_structural_difference_does_not_union():
    graph = build_bridge_equivalence_graph(
        (
            element(1, rank=(0, 0)),
            element(1, rank=(1, 0)),
        )
    )

    assert graph.components == ((0,), (1,))
    assert not graph.edges


def test_unbridged_cross_family_pair_is_reported_unresolved():
    graph = build_bridge_equivalence_graph(
        (
            OccurrenceAddress(),
            MoireRotation(1.0, 0.0),
        )
    )

    assert graph.components == ((0,), (1,))
    assert graph.unresolved_cross_family_pairs == ((0, 1),)


def test_graph_summary_exposes_compression_without_erasing_projections():
    carrier = RelationalPoint()
    relation = TypedRelation(carrier, carrier, "r")
    occurrence = RelationOccurrence(relation, (), (-1,))

    graph = build_bridge_equivalence_graph(
        (
            OccurrenceAddress((-1,)),
            RelationalPoint((-1,)),
            occurrence,
            relation,
            MoireRotation(1.0, 0.25),
            MoireRotation(2.0, 1.25),
        )
    )

    summary = graph.summary()

    assert summary.records == 6
    assert summary.equivalence_components == 4
    assert summary.strong_edges == 2
    assert summary.lossy_projection_edges == 1
    assert summary.unknown_bridge_edges == 0


def test_component_lookup_is_total_on_records():
    graph = build_bridge_equivalence_graph(
        (
            OccurrenceAddress((1,)),
            RelationalPoint((1,)),
            element(3),
        )
    )

    assert graph.component_of(0) == (0, 1)
    assert graph.component_of(1) == (0, 1)
    assert graph.component_of(2) == (2,)



def test_bridge_gap_report_groups_missing_family_links():
    graph = build_bridge_equivalence_graph(
        (
            OccurrenceAddress(),
            MoireRotation(1.0, 0.0),
            MoireRotation(2.0, 0.5),
        )
    )

    report = graph.bridge_gap_report()

    assert report.family_pairs == 1
    assert report.unresolved_pairs == 2
    gap = report.gaps[0]
    assert {
        gap.left_family,
        gap.right_family,
    } == {
        "occurrence_address",
        "moire_relative_rotation",
    }
    assert gap.count == 2


def test_bridge_gap_report_is_empty_when_every_cross_family_pair_is_bridged():
    graph = build_bridge_equivalence_graph(
        (
            OccurrenceAddress((-1,)),
            RelationalPoint((-1,)),
        )
    )

    report = graph.bridge_gap_report()

    assert report.family_pairs == 0
    assert report.unresolved_pairs == 0
    assert report.gaps == ()
