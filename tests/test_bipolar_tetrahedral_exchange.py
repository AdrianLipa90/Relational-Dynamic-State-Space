from rdss.bipolar_tetrahedral_exchange import (
    EDGE_COUNT,
    FACE_COUNT,
    FLAVOR_COUNT,
    POLARITY_COUNT,
    ACTIVE_DUAL_FACES,
    binary_maximum_entropy_nats,
    bipolar_exchange_counts,
    directed_face_flavor_channels,
    exchange_symmetry_orbit,
    face_plane_constants,
    forced_kappa_certificate,
    forced_kappa_closed_form,
    forced_kappa_from_bipolar_exchange,
    invariant_active_face_subsets,
    invariant_channel_information_nats,
    minimal_identity_face_closure_cardinality,
    polarity_association_quotient_cardinality,
    half_turn_normalized_measure,
    polarity_exchange,
    polarity_face_pairing,
    polarity_half_turn_radians,
    selector_free_active_exchange_cardinality,
    selector_free_active_exchange_faces,
    selector_free_tetrahedral_odd_completion,
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


def test_selector_free_active_exchange_forces_three_and_identity_closure_forces_plus_one() -> None:
    assert invariant_active_face_subsets() == (
        frozenset(),
        frozenset(ACTIVE_DUAL_FACES),
    )
    assert selector_free_active_exchange_faces() == frozenset(("S", "P", "J"))

    for n in range(0, 33):
        assert selector_free_active_exchange_cardinality(n) == 3 * n
        assert minimal_identity_face_closure_cardinality(3 * n) == 3 * n + 1
        assert selector_free_tetrahedral_odd_completion(n) == 3 * n + 1

    for n in range(0, 34, 2):
        assert polarity_association_quotient_cardinality(n) == n // 2


def test_bipolar_exchange_receipt() -> None:
    receipt = bipolar_exchange_counts()
    assert receipt["tetrahedron_faces"] == 4
    assert receipt["tetrahedron_edges"] == 6
    assert receipt["flavors"] == 3
    assert receipt["polarities"] == 2
    assert receipt["face_pairs"] == 4
    assert receipt["undirected_face_flavor_pairs"] == 12
    assert receipt["directed_face_flavor_incidences"] == 24
    assert receipt["symmetry_orbit_size"] == 24
    assert receipt["symmetry_transitive"] is True
    assert receipt["invariant_channel_weight"] == (1, 24)
    assert receipt["invariant_active_face_subsets"] == (
        frozenset(),
        frozenset(ACTIVE_DUAL_FACES),
    )
    assert receipt["selector_free_active_faces"] == frozenset(ACTIVE_DUAL_FACES)


def test_binary_max_entropy_forces_ln2() -> None:
    from math import log

    assert abs(binary_maximum_entropy_nats() - log(2.0)) <= 1e-15


def test_transitive_24_channel_orbit_forces_equal_information_share() -> None:
    from math import log

    assert unique_invariant_channel_weight() == (1, 24)
    assert abs(invariant_channel_information_nats() - log(2.0) / 24.0) <= 1e-15


def test_half_turn_and_uniform_channel_share_force_kappa() -> None:
    from math import log, pi

    assert abs(polarity_half_turn_radians() - pi) <= 1e-15
    assert abs(forced_kappa_from_bipolar_exchange() - log(2.0) / (24.0 * pi)) <= 1e-15
    assert abs(forced_kappa_from_bipolar_exchange() - forced_kappa_closed_form()) <= 1e-15

    receipt = forced_kappa_certificate()
    assert receipt["binary_source_states"] == 2
    assert abs(receipt["binary_max_entropy_nats"] - log(2.0)) <= 1e-15
    assert receipt["directed_channels"] == 24
    assert receipt["invariant_channel_weight"] == (1, 24)
    assert abs(receipt["information_per_channel_nats"] - log(2.0) / 24.0) <= 1e-15
    assert abs(receipt["half_turn_radians"] - pi) <= 1e-15
    assert abs(receipt["total_phase_measure_radians"] - 24.0 * pi) <= 1e-15
    assert receipt["matches_closed_form"] is True
