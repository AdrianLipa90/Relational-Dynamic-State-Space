from rdss import (
    OccurrenceAddress,
    RelationalPoint,
    TypedRelation,
)
from rdss.bridges import rdss_bridge_registry
from rdss.corpus import rdss_reference_corpus
from rdss.normal_form import rdss_forgetful_normal_form
from rdss.operations import RelationOccurrence
from rdss.provenance import (
    build_claim_dependency_graph,
    provenance_for_bridge_route,
    provenance_for_normal_form,
    provenance_for_rewrite_trace,
    provenance_for_value,
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


def test_value_provenance_links_factorization_signature_and_claim_graph():
    value = OccurrenceAddress((-1,))
    provenance = provenance_for_value(value)

    assert provenance.factorization.family == "occurrence_address"
    assert provenance.signature_provenance == (
        "occurrence_address_signature",
    )
    assert "DEF_OCCURRENCE_ADDRESS_SPACE" in provenance.root_claim_ids
    assert "DEF_RDSS_CANONICAL_SIGNATURE" in provenance.root_claim_ids
    assert_topological(provenance.graph)


def test_every_reference_corpus_value_has_resolvable_claim_provenance():
    for item in rdss_reference_corpus():
        provenance = provenance_for_value(
            item.value
        )

        assert provenance.root_claim_ids
        assert provenance.graph.roots == provenance.root_claim_ids
        assert provenance.graph.claim_count >= len(
            provenance.root_claim_ids
        )
        assert sum(
            provenance.graph.kind_counts.values()
        ) == provenance.graph.claim_count
        assert_topological(provenance.graph)


def test_bridge_route_provenance_expands_bridge_claim_dependencies():
    route = rdss_bridge_registry().direct(
        OccurrenceAddress((-1,)),
        "relational_carrier",
    )

    provenance = provenance_for_bridge_route(route)
    claim_ids = set(
        provenance.graph.ordered_claim_ids
    )

    assert provenance.source == "bridge_route"
    assert "DEF_CARRIER_OCCURRENCE_SEPARATION" in claim_ids
    assert "REF_RELATIONAL_POINT_BINARY_COORDINATE" in claim_ids
    assert "DEF_POINT" in claim_ids
    assert "DEF_OCCURRENCE_ADDRESS_SPACE" in claim_ids
    assert_topological(provenance.graph)


def test_rewrite_trace_provenance_tracks_forgetful_projection_claims():
    point = RelationalPoint()
    relation = TypedRelation(point, point, "r")
    occurrence = RelationOccurrence(
        relation,
        (),
        (-1,),
    )
    trace = (
        rdss_forgetful_rewrite_system()
        .trace_until_irreducible(occurrence)
    )

    provenance = provenance_for_rewrite_trace(
        trace
    )
    claim_ids = set(
        provenance.graph.ordered_claim_ids
    )

    assert provenance.source == "rewrite_trace"
    assert "DEF_OCCURRENCE_FORGETFUL_PROJECTION" in claim_ids
    assert_topological(provenance.graph)


def test_scoped_normal_form_provenance_reaches_termination_and_confluence():
    point = RelationalPoint()
    relation = TypedRelation(point, point, "r")
    occurrence = RelationOccurrence(
        relation,
        (),
        (-1,),
    )
    result = rdss_forgetful_normal_form(
        occurrence
    )

    provenance = provenance_for_normal_form(
        result
    )
    claim_ids = set(
        provenance.graph.ordered_claim_ids
    )

    assert provenance.source == "scoped_normal_form"
    assert "REF_FORGETFUL_SCOPED_NORMAL_FORM" in claim_ids
    assert "THM_REFERENCE_FORGETFUL_REWRITE_TERMINATES" in claim_ids
    assert "THM_REFERENCE_FORGETFUL_REWRITE_CONFLUENT" in claim_ids
    assert "THM_STRICT_FAMILY_RANK_TERMINATION" in claim_ids
    assert "THM_DETERMINISTIC_REWRITE_CONFLUENCE" in claim_ids
    assert_topological(provenance.graph)


def test_claim_dependency_graph_deduplicates_roots():
    graph = build_claim_dependency_graph(
        (
            "DEF_POINT",
            "DEF_POINT",
        )
    )

    assert graph.roots == ("DEF_POINT",)
    assert graph.ordered_claim_ids == (
        "DEF_POINT",
    )
