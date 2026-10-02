from fractions import Fraction

from rdss.tetrahedral_binding import (
    ACTIVE_OPERATOR_LABELS,
    ACTIVE_SIGN_TETRAHEDRON,
    OPERATOR_SIMPLEX_LABELS,
    active_sign_centered_gram,
    operator_simplex_centered_gram,
    operator_simplex_edge_gram,
    operator_simplex_is_regular_tetrahedron,
    operator_simplex_squared_distance,
    operator_simplex_volume,
    operator_stella_gram_isometry_holds,
    sign_vertex_product,
    stella_klein_four_certificate,
    tetrahedral_binding_certificate,
    tetrahedral_completion_cardinality,
)


def test_operator_basis_is_exact_regular_tetrahedron() -> None:
    assert OPERATOR_SIMPLEX_LABELS == ("I", "S", "P", "J")
    assert ACTIVE_OPERATOR_LABELS == ("S", "P", "J")
    assert operator_simplex_is_regular_tetrahedron()

    for i, left in enumerate(OPERATOR_SIMPLEX_LABELS):
        for right in OPERATOR_SIMPLEX_LABELS[i + 1 :]:
            # Pythagorean edge: orthonormal unit basis points give 1^2+1^2.
            assert operator_simplex_squared_distance(left, right) == Fraction(2)


def test_centered_tetrahedron_gram_is_exact() -> None:
    expected = (
        (Fraction(3, 4), Fraction(-1, 4), Fraction(-1, 4), Fraction(-1, 4)),
        (Fraction(-1, 4), Fraction(3, 4), Fraction(-1, 4), Fraction(-1, 4)),
        (Fraction(-1, 4), Fraction(-1, 4), Fraction(3, 4), Fraction(-1, 4)),
        (Fraction(-1, 4), Fraction(-1, 4), Fraction(-1, 4), Fraction(3, 4)),
    )
    assert operator_simplex_centered_gram() == expected

    for i, row in enumerate(expected):
        for j, value in enumerate(row):
            if i == j:
                assert value == Fraction(3, 4)
            else:
                assert value / expected[i][i] == Fraction(-1, 3)


def test_edge_gram_and_volume_are_exact() -> None:
    assert operator_simplex_edge_gram() == (
        (Fraction(2), Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(2), Fraction(1)),
        (Fraction(1), Fraction(1), Fraction(2)),
    )
    assert operator_simplex_volume() == Fraction(1, 3)


def test_operator_simplex_matches_existing_stella_tetrahedron() -> None:
    assert set(ACTIVE_SIGN_TETRAHEDRON.values())
    assert operator_stella_gram_isometry_holds()
    assert active_sign_centered_gram() == operator_simplex_centered_gram()


def test_tetrahedral_completion_is_three_n_plus_one_but_not_physical_binding() -> None:
    for n in range(0, 33):
        assert tetrahedral_completion_cardinality(n) == 3 * n + 1

    receipt = tetrahedral_binding_certificate()
    assert receipt["identity_vertices"] == 1
    assert receipt["active_vertices"] == 3
    assert receipt["vertex_count"] == 4
    assert receipt["edge_squared"] == Fraction(2)
    assert receipt["centered_norm_squared"] == Fraction(3, 4)
    assert receipt["normalized_cross_inner_product"] == Fraction(-1, 3)
    assert receipt["edge_gram_determinant"] == 4
    assert receipt["volume"] == Fraction(1, 3)
    assert receipt["regular_tetrahedron"] is True
    assert receipt["stella_isometry"] is True
    assert receipt["physical_dynamics_binding"] is False


def test_positive_parity_tetrahedron_is_klein_four_sign_group() -> None:
    receipt = stella_klein_four_certificate()
    assert receipt["group_order"] == 4
    assert receipt["identity_count"] == 1
    assert receipt["nonidentity_count"] == 3
    assert receipt["nonidentity_order"] == 2
    assert receipt["closed"] is True
    assert receipt["commutative"] is True
    assert receipt["klein_four"] is True
    assert receipt["operator_multiplication_identified"] is False

    identity = (1, 1, 1)
    for vertex in ACTIVE_SIGN_TETRAHEDRON.values():
        assert sign_vertex_product(identity, vertex) == vertex
        assert sign_vertex_product(vertex, identity) == vertex
