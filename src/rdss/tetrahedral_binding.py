from __future__ import annotations

from fractions import Fraction
from math import isqrt

from .algebraic_geometry_cell import TETRAHEDRON_POSITIVE_VERTICES


OperatorLabel = str
Vector3 = tuple[int, int, int]
Vector4 = tuple[Fraction, Fraction, Fraction, Fraction]

OPERATOR_SIMPLEX_LABELS: tuple[OperatorLabel, ...] = ("I", "S", "P", "J")
ACTIVE_OPERATOR_LABELS: tuple[OperatorLabel, ...] = ("S", "P", "J")

OPERATOR_SIMPLEX_VERTICES: dict[OperatorLabel, Vector4] = {
    "I": (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
    "S": (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
    "P": (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
    "J": (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
}

# Exact sign realization of the regular tetrahedron in the active 3-space.
# It is the positive xyz-parity tetrahedron already used by the Stella cell.
ACTIVE_SIGN_TETRAHEDRON: dict[OperatorLabel, Vector3] = {
    "I": (1, 1, 1),
    "S": (1, -1, -1),
    "P": (-1, 1, -1),
    "J": (-1, -1, 1),
}


def _dot(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), start=Fraction(0))


def _sub(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(a - b for a, b in zip(left, right))


def operator_simplex_centroid() -> Vector4:
    """Centroid of the four Frobenius-orthonormal operator-basis points."""

    return (Fraction(1, 4),) * 4


def centered_operator_vertex(label: OperatorLabel) -> Vector4:
    """Centered simplex vertex E_label - C in exact rational coordinates."""

    try:
        vertex = OPERATOR_SIMPLEX_VERTICES[label]
    except KeyError as exc:
        raise ValueError(f"unknown operator label: {label!r}") from exc
    return _sub(vertex, operator_simplex_centroid())  # type: ignore[return-value]


def operator_simplex_squared_distance(
    left_label: OperatorLabel,
    right_label: OperatorLabel,
) -> Fraction:
    """Squared Frobenius distance between two operator-basis points."""

    try:
        left = OPERATOR_SIMPLEX_VERTICES[left_label]
        right = OPERATOR_SIMPLEX_VERTICES[right_label]
    except KeyError as exc:
        raise ValueError(f"unknown operator label: {exc.args[0]!r}") from exc
    delta = _sub(left, right)
    return _dot(delta, delta)


def operator_simplex_centered_gram() -> tuple[tuple[Fraction, ...], ...]:
    """Exact Gram matrix of centered {I,S,P,J} simplex vertices."""

    centered = tuple(centered_operator_vertex(label) for label in OPERATOR_SIMPLEX_LABELS)
    return tuple(tuple(_dot(left, right) for right in centered) for left in centered)


def operator_simplex_edge_gram() -> tuple[tuple[Fraction, ...], ...]:
    """Gram matrix for edges S-I, P-I, J-I."""

    root = OPERATOR_SIMPLEX_VERTICES["I"]
    edges = tuple(_sub(OPERATOR_SIMPLEX_VERTICES[label], root) for label in ACTIVE_OPERATOR_LABELS)
    return tuple(tuple(_dot(left, right) for right in edges) for left in edges)


def _det3(matrix: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise ValueError("determinant helper requires a 3x3 matrix")
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def operator_simplex_volume() -> Fraction:
    """Exact tetrahedral 3-volume in the induced Frobenius metric."""

    det = _det3(operator_simplex_edge_gram())
    if det < 0:
        raise ArithmeticError("negative Gram determinant")
    num_root = isqrt(det.numerator)
    den_root = isqrt(det.denominator)
    if num_root * num_root != det.numerator or den_root * den_root != det.denominator:
        raise ArithmeticError("operator simplex Gram determinant is not a rational square")
    return Fraction(num_root, den_root * 6)


def sign_vertex_product(left: Vector3, right: Vector3) -> Vector3:
    """Componentwise product on the positive-parity tetrahedral sign vertices."""

    if left not in ACTIVE_SIGN_TETRAHEDRON.values():
        raise ValueError("left vertex is not in the positive-parity tetrahedron")
    if right not in ACTIVE_SIGN_TETRAHEDRON.values():
        raise ValueError("right vertex is not in the positive-parity tetrahedron")
    return tuple(a * b for a, b in zip(left, right))  # type: ignore[return-value]


def stella_klein_four_certificate() -> dict[str, object]:
    """Exact V4 certificate for the positive-parity sign tetrahedron.

    This is a group structure on sign coordinates. It is a geometric/sign
    crosscheck and is not identified with the noncommutative operator product,
    for which J^2=-I.
    """

    vertices = tuple(ACTIVE_SIGN_TETRAHEDRON.values())
    identity = (1, 1, 1)
    closure = all(sign_vertex_product(a, b) in vertices for a in vertices for b in vertices)
    commutative = all(
        sign_vertex_product(a, b) == sign_vertex_product(b, a)
        for a in vertices
        for b in vertices
    )
    nonidentity = tuple(vertex for vertex in vertices if vertex != identity)
    order_two = all(sign_vertex_product(vertex, vertex) == identity for vertex in nonidentity)
    return {
        "group_order": len(vertices),
        "identity_count": sum(vertex == identity for vertex in vertices),
        "nonidentity_count": len(nonidentity),
        "nonidentity_order": 2 if order_two else None,
        "closed": closure,
        "commutative": commutative,
        "klein_four": closure and commutative and len(vertices) == 4 and len(nonidentity) == 3 and order_two,
        "operator_multiplication_identified": False,
    }


def scaled_active_sign_vertex(label: OperatorLabel) -> tuple[Fraction, Fraction, Fraction]:
    """Stella tetrahedron vertex scaled by 1/2 to match the centered operator simplex."""

    try:
        vertex = ACTIVE_SIGN_TETRAHEDRON[label]
    except KeyError as exc:
        raise ValueError(f"unknown operator label: {label!r}") from exc
    return tuple(Fraction(value, 2) for value in vertex)  # type: ignore[return-value]


def active_sign_centered_gram() -> tuple[tuple[Fraction, ...], ...]:
    """Gram matrix of the 1/2-scaled positive-parity Stella tetrahedron."""

    vertices = tuple(scaled_active_sign_vertex(label) for label in OPERATOR_SIMPLEX_LABELS)
    return tuple(tuple(_dot(left, right) for right in vertices) for left in vertices)


def operator_simplex_is_regular_tetrahedron() -> bool:
    """Exact regular-tetrahedron certificate for {I,S,P,J}."""

    distances = {
        operator_simplex_squared_distance(left, right)
        for i, left in enumerate(OPERATOR_SIMPLEX_LABELS)
        for right in OPERATOR_SIMPLEX_LABELS[i + 1 :]
    }
    return distances == {Fraction(2)} and _det3(operator_simplex_edge_gram()) > 0


def operator_stella_gram_isometry_holds() -> bool:
    """The centered operator simplex and scaled Stella tetrahedron are isometric."""

    return (
        set(ACTIVE_SIGN_TETRAHEDRON.values()) == set(TETRAHEDRON_POSITIVE_VERTICES)
        and operator_simplex_centered_gram() == active_sign_centered_gram()
    )


def tetrahedral_completion_cardinality(cardinality: int) -> int:
    """Cardinality of active three-sector product plus one global identity anchor.

    This is the exact structural count |X x {S,P,J}| + |{I}| = 3|X| + 1.
    It is not, by itself, a physical law selecting this completion as dynamics.
    """

    n = int(cardinality)
    if n < 0 or n != cardinality:
        raise ValueError("cardinality must be a non-negative integer")
    return 3 * n + 1


def tetrahedral_binding_certificate() -> dict[str, object]:
    """Return the exact downstream geometric binding receipt."""

    gram = operator_simplex_centered_gram()
    return {
        "operator_labels": OPERATOR_SIMPLEX_LABELS,
        "identity_vertices": 1,
        "active_vertices": len(ACTIVE_OPERATOR_LABELS),
        "vertex_count": len(OPERATOR_SIMPLEX_LABELS),
        "edge_squared": operator_simplex_squared_distance("I", "S"),
        "centered_norm_squared": gram[0][0],
        "centered_cross_inner_product": gram[0][1],
        "normalized_cross_inner_product": gram[0][1] / gram[0][0],
        "edge_gram_determinant": _det3(operator_simplex_edge_gram()),
        "volume": operator_simplex_volume(),
        "regular_tetrahedron": operator_simplex_is_regular_tetrahedron(),
        "stella_isometry": operator_stella_gram_isometry_holds(),
        "stella_v4": stella_klein_four_certificate(),
        "physical_dynamics_binding": False,
    }
