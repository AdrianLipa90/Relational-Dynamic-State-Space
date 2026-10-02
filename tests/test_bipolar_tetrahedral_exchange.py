from rdss.bipolar_tetrahedral_exchange import (
    EDGE_COUNT,
    FACE_COUNT,
    FLAVOR_COUNT,
    POLARITY_COUNT,
    bipolar_exchange_counts,
    directed_face_flavor_channels,
    exchange_symmetry_orbit,
    face_plane_constants,
    half_turn_normalized_measure,
    polarity_exchange,
    polarity_face_pairing,
    undirected_face_flavor_pairs,
    unique_invariant_channel_weight,
)


def test_tetrahedral_face_and_edge_counts_are_exact() -> None:
    assert FACE_COUNT == 4
    assert EDGE_COUNT == 6


def test_central_inversion_pairs_all_four_faces() -> None:
    assert polarity_face_pairing() == ((0, 0), (1, 1), (2, 2), (3, 3))
    assert face_plane_constants() == ((-1, 1),) * 4


def test_three_flavours_on_four_faces_and_two_polarities_force_24_directed_incidences() -> None:
    assert FLAVOR_COUNT == 3
    assert POLARITY_COUNT == 2
    channels = directed_face_flavor_channels()
    assert len(channels) == 2 * 4 * 3 == 24
    assert len(set(channels)) == 24


def test_polarity_exchange_is_free_and_quotient_has_12_pairs() -> None:
    channels = directed_face_flavor_channels()
    for channel in channels:
        partner = polarity_exchange(channel)
        assert partner != channel
        assert polarity_exchange(partner) == channel
    pairs = undirected_face_flavor_pairs()
    assert len(pairs) == 4 * 3 == 12
    assert all(len(pair) == 2 for pair in pairs)


def test_bipolar_face_flavour_symmetry_is_transitive() -> None:
    orbit = exchange_symmetry_orbit()
    assert len(orbit) == 24
    assert orbit == frozenset(directed_face_flavor_channels())
    assert unique_invariant_channel_weight() == (1, 24)


def test_half_turn_measure_matches_existing_kappa_reference_count() -> None:
    # 24 oriented incidences, one half-turn each -> 12 normalized turns.
    assert half_turn_normalized_measure() == 12


def test_bipolar_exchange_receipt() -> None:
    receipt = bipolar_exchange_counts()
    assert receipt == {
        "tetrahedron_faces": 4,
        "tetrahedron_edges": 6,
        "flavors": 3,
        "polarities": 2,
        "face_pairs": 4,
        "undirected_face_flavor_pairs": 12,
        "directed_face_flavor_incidences": 24,
        "symmetry_orbit_size": 24,
        "symmetry_transitive": True,
        "invariant_channel_weight": (1, 24),
    }
