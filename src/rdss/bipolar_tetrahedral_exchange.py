from __future__ import annotations

from math import log, pi

from .algebraic_geometry_cell import (
    TETRAHEDRON_NEGATIVE_VERTICES,
    TETRAHEDRON_POSITIVE_VERTICES,
)


FaceLabel = int
FlavorLabel = int
PolarityLabel = int
Vertex3 = tuple[int, int, int]
ExchangeChannel = tuple[PolarityLabel, FaceLabel, FlavorLabel]

# REF: TIR main @ 9783782570a2ccfa1fc42c99b605dad48e02aa78
#       TIR/foundations/TIR_COEFFICIENT_MAGNITUDE_PARENT_EVALUATION_V0_1.md
#       THREE_FLAVOUR_CARRIER = CLOSED -> N_F=3
# REF: RDSS @ 7e947fee4b85192b35605a91bc35530891d88289
#       BRIDGE_TIR_THREE_FLAVOUR_C3_LABEL_CARRIER imports that closed result.
FACE_COUNT = 4
EDGE_COUNT = 6
FLAVOR_COUNT = 3
POLARITY_COUNT = 2

OPERATOR_DUAL_FACE_LABELS: tuple[str, ...] = ("I", "S", "P", "J")
IDENTITY_DUAL_FACE = "I"
ACTIVE_DUAL_FACES: tuple[str, ...] = ("S", "P", "J")

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


def active_dual_face_cycle(face: str) -> str:
    """C3 stabilizer action on the three faces dual to S,P,J."""

    if face == "S":
        return "P"
    if face == "P":
        return "J"
    if face == "J":
        return "S"
    if face == "I":
        return "I"
    raise ValueError(f"unknown dual-face label: {face!r}")


def invariant_active_face_subsets() -> tuple[frozenset[str], ...]:
    """All subsets of {S,P,J} invariant under the C3 face stabilizer."""

    faces = ACTIVE_DUAL_FACES
    subsets: list[frozenset[str]] = []
    for mask in range(1 << len(faces)):
        subset = frozenset(faces[i] for i in range(len(faces)) if mask & (1 << i))
        image = frozenset(active_dual_face_cycle(face) for face in subset)
        if image == subset:
            subsets.append(subset)
    return tuple(subsets)


def selector_free_active_exchange_faces() -> frozenset[str]:
    """Unique non-empty C3-invariant active-face selection.

    With no extra selector, non-trivial exchange cannot choose one or two of
    the three symmetry-related active faces. The unique non-empty invariant
    subset is the complete active orbit {S,P,J}.
    """

    nonempty = tuple(subset for subset in invariant_active_face_subsets() if subset)
    if nonempty != (frozenset(ACTIVE_DUAL_FACES),):
        raise ArithmeticError("active-face C3 orbit is not uniquely selected")
    return nonempty[0]


def selector_free_active_exchange_cardinality(cardinality: int) -> int:
    """Complete active exchange duplicates each carrier element across 3 faces."""

    n = int(cardinality)
    if n < 0 or n != cardinality:
        raise ValueError("cardinality must be a non-negative integer")
    return n * len(selector_free_active_exchange_faces())


def minimal_identity_face_closure_cardinality(cardinality: int) -> int:
    """Add the single fixed identity-dual closure face exactly once."""

    n = int(cardinality)
    if n < 0 or n != cardinality:
        raise ValueError("cardinality must be a non-negative integer")
    return n + 1


def selector_free_tetrahedral_odd_completion(cardinality: int) -> int:
    """Forced minimal non-trivial active exchange plus unique identity closure."""

    return minimal_identity_face_closure_cardinality(
        selector_free_active_exchange_cardinality(cardinality)
    )


def polarity_association_quotient_cardinality(cardinality: int) -> int:
    """Free bipolar Z2 association quotient, defined only for even cardinality."""

    n = int(cardinality)
    if n < 0 or n != cardinality:
        raise ValueError("cardinality must be a non-negative integer")
    if n % 2:
        raise ValueError("free polarity pairing requires even cardinality")
    return n // 2


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


# REF: Shannon (1948), plus RDSS THM_Z2_UNIQUE_SWAP_INVARIANT_PROBABILITY.
# REF: RDSS @ d6f80e4539db368f828a064c2ab0fff730ec3490
#       gives the transitive 24-channel bipolar exchange orbit and half-turn structure.
def binary_maximum_entropy_nats() -> float:
    """Maximum Shannon entropy of a binary Z2-invariant source.

    Z2 invariance forces p_-=p_+=1/2. Therefore the binary Shannon entropy is
    uniquely maximal at ln(2). This is source entropy, not entropy of a
    24-outcome channel-label distribution.
    """

    p = 0.5
    return -(p * log(p) + p * log(p))


def invariant_channel_information_nats() -> float:
    """Forced information share of one directed exchange channel.

    The source information ln(2) is distributed over the single transitive
    24-channel orbit. Invariant normalized weighting is uniquely 1/24.
    """

    numerator, denominator = unique_invariant_channel_weight()
    if numerator != 1:
        raise ArithmeticError("unexpected invariant channel-weight numerator")
    return binary_maximum_entropy_nats() / denominator


def polarity_half_turn_radians() -> float:
    """Non-trivial Z2 phase embedded in U(1) is the half-turn pi."""

    return pi


def forced_kappa_from_bipolar_exchange() -> float:
    """Derive kappa = ln(2)/(24*pi) from source entropy and exchange symmetry.

    Chain:
      Z2 binary maximum entropy -> ln(2)
      transitive bipolar tetrahedral face-flavour orbit -> 24 equal channels
      non-trivial polarity exchange in U(1) -> pi radians per channel

    Hence kappa = (ln(2)/24)/pi.
    """

    return invariant_channel_information_nats() / polarity_half_turn_radians()


def forced_kappa_closed_form() -> float:
    """Closed-form numerical reference for the forced kappa theorem."""

    return log(2.0) / (24.0 * pi)


def forced_kappa_certificate() -> dict[str, int | float | bool | tuple[int, int]]:
    """Machine receipt for the theorem-level kappa derivation."""

    channel_count = len(directed_face_flavor_channels())
    entropy = binary_maximum_entropy_nats()
    channel_info = invariant_channel_information_nats()
    half_turn = polarity_half_turn_radians()
    kappa = forced_kappa_from_bipolar_exchange()
    closed = forced_kappa_closed_form()
    return {
        "binary_source_states": 2,
        "binary_max_entropy_nats": entropy,
        "directed_channels": channel_count,
        "invariant_channel_weight": unique_invariant_channel_weight(),
        "information_per_channel_nats": channel_info,
        "half_turn_radians": half_turn,
        "total_phase_measure_radians": channel_count * half_turn,
        "kappa": kappa,
        "closed_form_kappa": closed,
        "matches_closed_form": abs(kappa - closed) <= 1e-15,
    }


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
        "invariant_active_face_subsets": invariant_active_face_subsets(),
        "selector_free_active_faces": selector_free_active_exchange_faces(),
        "forced_kappa": forced_kappa_from_bipolar_exchange(),
    }


def half_turn_normalized_measure() -> int:
    """Total normalized-turn measure for one half-turn per directed incidence.

    24 directed incidences x 1/2 turn = 12 normalized turns.
    """

    directed_count = len(directed_face_flavor_channels())
    if directed_count % 2:
        raise ArithmeticError("directed incidence count must be even")
    return directed_count // 2
