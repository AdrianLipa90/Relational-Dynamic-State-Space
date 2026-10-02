from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .algebraic_geometry_cell import (
    TETRAHEDRON_NEGATIVE_VERTICES,
    TETRAHEDRON_POSITIVE_VERTICES,
)


FaceLabel = int
FlavorLabel = int
PolarityLabel = int
Vertex3 = tuple[int, int, int]
ExchangeChannel = tuple[PolarityLabel, FaceLabel, FlavorLabel]

FACE_COUNT = 4
EDGE_COUNT = 6
FLAVOR_COUNT = 3
POLARITY_COUNT = 2

POSITIVE_VERTICES: tuple[Vertex3, ...] = TETRAHEDRON_POSITIVE_VERTICES
NEGATIVE_VERTICES: tuple[Vertex3, ...] = TETRAHEDRON_NEGATIVE_VERTICES


def _dot(left: Vertex3, right: Vertex3) -> int:
    return sum(a * b for a, b in zip(left, right))


def _neg(vertex: Vertex3) -> Vertex3:
    return tuple(-value for value in vertex)  # type: ignore[return-value]


def tetrahedron_faces(vertices: tuple[Vertex3, ...]) -> tuple[tuple[Vertex3, ...], ...]:
    """Return the four triangular faces, indexed by opposite vertex."""

    if len(vertices) != 4:
        raise ValueError("a tetrahedron requires exactly four vertices")
    return tuple(
        tuple(vertex for j, vertex in enumerate(vertices) if j != i)
        for i in range(4)
    )


POSITIVE_FACES = tetrahedron_faces(POSITIVE_VERTICES)
NEGATIVE_FACES = tetrahedron_faces(NEGATIVE_VERTICES)


def polarity_face_pairing() -> tuple[tuple[FaceLabel, FaceLabel], ...]:
    """Canonical face pairing induced by central inversion x -> -x.

    Face i of T+ is sent exactly to face i of T-. The indexing is by the
    opposite positive tetrahedron vertex.
    """

    pairs: list[tuple[int, int]] = []
    for i, positive_face in enumerate(POSITIVE_FACES):
        inverted = {_neg(vertex) for vertex in positive_face}
        if inverted != set(NEGATIVE_FACES[i]):
            raise ArithmeticError("central inversion does not preserve face label")
        pairs.append((i, i))
    return tuple(pairs)


def face_plane_constants() -> tuple[tuple[int, int], ...]:
    """Exact opposite face-plane constants for the bipolar tetrahedra.

    For positive vertex v_i, the positive face opposite v_i obeys
    v_i dot x = -1, while its polarity partner in T- obeys v_i dot x = +1.
    """

    result: list[tuple[int, int]] = []
    for i, normal in enumerate(POSITIVE_VERTICES):
        plus_constants = {_dot(normal, vertex) for vertex in POSITIVE_FACES[i]}
        minus_constants = {_dot(normal, vertex) for vertex in NEGATIVE_FACES[i]}
        if plus_constants != {-1} or minus_constants != {1}:
            raise ArithmeticError("unexpected bipolar tetrahedral face plane")
        result.append((-1, 1))
    return tuple(result)


def directed_face_flavor_channels() -> tuple[ExchangeChannel, ...]:
    """All directed polarity x face x flavour incidences."""

    return tuple(
        (polarity, face, flavor)
        for polarity in range(POLARITY_COUNT)
        for face in range(FACE_COUNT)
        for flavor in range(FLAVOR_COUNT)
    )


def polarity_exchange(channel: ExchangeChannel) -> ExchangeChannel:
    """Free involution exchanging the two polarity orientations."""

    polarity, face, flavor = channel
    if polarity not in (0, 1):
        raise ValueError("polarity must be 0 or 1")
    if not 0 <= face < FACE_COUNT:
        raise ValueError("face outside tetrahedral range")
    if not 0 <= flavor < FLAVOR_COUNT:
        raise ValueError("flavor outside three-label range")
    return (1 - polarity, face, flavor)


def undirected_face_flavor_pairs() -> tuple[frozenset[ExchangeChannel], ...]:
    """Quotient the 24 directed incidences by the free polarity involution."""

    seen: set[ExchangeChannel] = set()
    pairs: list[frozenset[ExchangeChannel]] = []
    for channel in directed_face_flavor_channels():
        if channel in seen:
            continue
        partner = polarity_exchange(channel)
        orbit = frozenset((channel, partner))
        if len(orbit) != 2:
            raise ArithmeticError("polarity exchange must act freely")
        seen.update(orbit)
        pairs.append(orbit)
    return tuple(pairs)


def _face_cycle_012(channel: ExchangeChannel) -> ExchangeChannel:
    p, f, a = channel
    return (p, {0: 1, 1: 2, 2: 0}.get(f, f), a)


def _face_cycle_013(channel: ExchangeChannel) -> ExchangeChannel:
    p, f, a = channel
    return (p, {0: 1, 1: 3, 3: 0}.get(f, f), a)


def _flavor_cycle(channel: ExchangeChannel) -> ExchangeChannel:
    p, f, a = channel
    return (p, f, (a + 1) % FLAVOR_COUNT)


def exchange_symmetry_orbit(seed: ExchangeChannel = (0, 0, 0)) -> frozenset[ExchangeChannel]:
    """Orbit under polarity Z2, tetrahedral A4 generators, and flavor C3.

    The two face 3-cycles generate A4 on the four faces. Together with the
    polarity flip and the flavor 3-cycle they act transitively on the
    2 x 4 x 3 directed incidence set.
    """

    generators = (polarity_exchange, _face_cycle_012, _face_cycle_013, _flavor_cycle)
    orbit = {seed}
    frontier = [seed]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            nxt = generator(current)
            if nxt not in orbit:
                orbit.add(nxt)
                frontier.append(nxt)
    return frozenset(orbit)


def unique_invariant_channel_weight() -> tuple[int, int]:
    """Return the unique normalized invariant rational weight numerator/denominator.

    Transitivity forces every channel weight equal. Normalization over 24
    channels then fixes each weight to 1/24.
    """

    orbit = exchange_symmetry_orbit()
    total = len(directed_face_flavor_channels())
    if len(orbit) != total:
        raise ArithmeticError("exchange symmetry is not transitive")
    return (1, total)


def bipolar_exchange_counts() -> dict[str, int | bool | tuple[int, int]]:
    """Exact combinatorial receipt for the bipolar tetrahedral exchange layer."""

    directed = directed_face_flavor_channels()
    undirected = undirected_face_flavor_pairs()
    orbit = exchange_symmetry_orbit()
    return {
        "tetrahedron_faces": FACE_COUNT,
        "tetrahedron_edges": EDGE_COUNT,
        "flavors": FLAVOR_COUNT,
        "polarities": POLARITY_COUNT,
        "face_pairs": len(polarity_face_pairing()),
        "undirected_face_flavor_pairs": len(undirected),
        "directed_face_flavor_incidences": len(directed),
        "symmetry_orbit_size": len(orbit),
        "symmetry_transitive": len(orbit) == len(directed),
        "invariant_channel_weight": unique_invariant_channel_weight(),
    }


def half_turn_normalized_measure() -> int:
    """Total normalized-turn measure for one half-turn per directed incidence.

    24 directed incidences x 1/2 turn = 12 normalized turns.
    """

    directed_count = len(directed_face_flavor_channels())
    if directed_count % 2:
        raise ArithmeticError("directed incidence count must be even")
    return directed_count // 2
