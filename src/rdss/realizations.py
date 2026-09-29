from __future__ import annotations

from dataclasses import dataclass
from math import acos, isfinite, pi
from typing import Callable

from .algebra import RelationalPoint, TensorScalarElement
from .closure import GenerativeRelationModel, RelationalGenerativeModel
from .phase import wrap_phase
from .operations import OccurrenceTransportPath, TransportPath


@dataclass(frozen=True)
class CP1State:
    """Normalized representative of one point in the CP1 reference realization."""

    alpha: complex
    beta: complex

    def __post_init__(self) -> None:
        a = complex(self.alpha)
        b = complex(self.beta)
        if not (
            isfinite(a.real)
            and isfinite(a.imag)
            and isfinite(b.real)
            and isfinite(b.imag)
        ):
            raise ValueError("CP1 amplitudes must be finite")
        norm2 = abs(a) ** 2 + abs(b) ** 2
        if norm2 <= 0.0:
            raise ValueError("the zero vector does not define a CP1 point")
        norm = norm2 ** 0.5
        object.__setattr__(self, "alpha", a / norm)
        object.__setattr__(self, "beta", b / norm)

    def overlap_abs(self, other: "CP1State") -> float:
        inner = self.alpha.conjugate() * other.alpha + self.beta.conjugate() * other.beta
        return min(1.0, max(0.0, abs(inner)))

    def fubini_study_distance(self, other: "CP1State") -> float:
        return acos(self.overlap_abs(other))

    def orthogonal_partner(self) -> "CP1State":
        return CP1State(-self.beta.conjugate(), self.alpha.conjugate())


@dataclass(frozen=True)
class MinimalDistinction:
    """Reference relation selecting two projective states over one carrier."""

    carrier: RelationalPoint
    left: CP1State
    right: CP1State
    label: str = "distinction"

    def __post_init__(self) -> None:
        if self.separation <= 1e-12:
            raise ValueError(
                "CP1 distinction requires two projectively distinct states"
            )

    @property
    def separation(self) -> float:
        return self.left.fubini_study_distance(self.right)

    def is_maximal(self, tolerance: float = 1e-12) -> bool:
        if tolerance <= 0 or not isfinite(tolerance):
            raise ValueError("tolerance must be positive and finite")
        return abs(self.separation - (pi / 2.0)) <= tolerance


@dataclass(frozen=True)
class MoireRotation:
    """Scalar-angle reference realization of a relative orbital rotation."""

    theta_i: float
    theta_j: float

    def __post_init__(self) -> None:
        if not (isfinite(self.theta_i) and isfinite(self.theta_j)):
            raise ValueError("rotation angles must be finite")

    @property
    def delta(self) -> float:
        return wrap_phase(self.theta_i - self.theta_j)


@dataclass(frozen=True)
class CP1RefinementRealization:
    """Tree of local CP1/Fubini-Study fibres over relational carriers.

    Each carrier p_omega owns a local CP1 distinction. The selected left/right
    projective states index the child carriers p_(omega,-) and p_(omega,+).
    Child carriers may in turn own their own local CP1 fibres.

    The local CP1 state at a parent is not identified with the projective
    coordinate system of a child fibre; the link is incidence/refinement.
    """

    distinctions: tuple[MinimalDistinction, ...]

    def __post_init__(self) -> None:
        carriers = [d.carrier for d in self.distinctions]
        if len(carriers) != len(set(carriers)):
            raise ValueError("each relational carrier may have at most one CP1 fibre")

    @property
    def by_carrier(self) -> dict[RelationalPoint, MinimalDistinction]:
        return {d.carrier: d for d in self.distinctions}

    def distinction_at(self, carrier: RelationalPoint) -> MinimalDistinction:
        try:
            return self.by_carrier[carrier]
        except KeyError as exc:
            raise KeyError(f"no CP1 distinction at carrier {carrier.address}") from exc

    def branch_state(self, carrier: RelationalPoint, branch: int) -> CP1State:
        if branch not in (-1, 1):
            raise ValueError("branch must be -1 or +1")
        d = self.distinction_at(carrier)
        return d.left if branch == -1 else d.right

    def child_carrier(self, carrier: RelationalPoint, branch: int) -> RelationalPoint:
        if branch not in (-1, 1):
            raise ValueError("branch must be -1 or +1")
        return RelationalPoint(carrier.address + (branch,))

    def complete_through_depth(self, root: RelationalPoint, depth: int) -> bool:
        """Require one local CP1 distinction at every node through depth."""
        if depth < 0:
            raise ValueError("depth must be non-negative")
        fibres = self.by_carrier
        level = (root,)
        for current_depth in range(depth + 1):
            if any(carrier not in fibres for carrier in level):
                return False
            if current_depth == depth:
                break
            level = tuple(
                RelationalPoint(carrier.address + (branch,))
                for carrier in level
                for branch in (-1, 1)
            )
        return True

    def fs_profile(
        self,
        root: RelationalPoint,
        depth: int,
    ) -> dict[tuple[int, ...], float]:
        if not self.complete_through_depth(root, depth):
            raise ValueError("CP1 refinement realization is incomplete")
        fibres = self.by_carrier
        out: dict[tuple[int, ...], float] = {}
        level = (root,)
        for current_depth in range(depth + 1):
            for carrier in level:
                out[carrier.address] = fibres[carrier].separation
            if current_depth == depth:
                break
            level = tuple(
                RelationalPoint(carrier.address + (branch,))
                for carrier in level
                for branch in (-1, 1)
            )
        return out


def reference_maximal_cp1_tree(
    depth: int,
    *,
    root: RelationalPoint = RelationalPoint(),
) -> CP1RefinementRealization:
    """Build a finite reference tree with maximal FS distinction in each fibre."""
    if depth < 0:
        raise ValueError("depth must be non-negative")

    north = CP1State(1.0, 0.0)
    south = north.orthogonal_partner()

    distinctions: list[MinimalDistinction] = []
    level = (root,)
    for current_depth in range(depth + 1):
        for carrier in level:
            distinctions.append(
                MinimalDistinction(
                    carrier=carrier,
                    left=north,
                    right=south,
                    label="maximal-reference-distinction",
                )
            )
        if current_depth == depth:
            break
        level = tuple(
            RelationalPoint(carrier.address + (branch,))
            for carrier in level
            for branch in (-1, 1)
        )

    realization = CP1RefinementRealization(tuple(distinctions))
    if any(abs(value - pi / 2.0) > 1e-12 for value in realization.fs_profile(root, depth).values()):
        raise AssertionError("reference CP1 tree must be maximally distinguished")
    return realization




@dataclass(frozen=True)
class CP1RelationalUnfolding:
    """Finite occurrence unfolding paired with local CP1 reference fibres.

    The same underlying carrier label may occur at many distinct path-labelled
    RelationalPoint addresses. CP1 fibres are indexed by those occurrence
    addresses, not by the carrier label quotient.
    """

    occurrence_labels: tuple[tuple[RelationalPoint, str], ...]
    fibres: CP1RefinementRealization

    def __post_init__(self) -> None:
        points = [point for point, _ in self.occurrence_labels]
        if len(points) != len(set(points)):
            raise ValueError("occurrence addresses must be unique")
        if set(points) != set(self.fibres.by_carrier):
            raise ValueError(
                "occurrence labels and CP1 fibres must use the same address set"
            )
        if any(not label for _, label in self.occurrence_labels):
            raise ValueError("underlying carrier labels must be non-empty")

    @property
    def label_by_address(self) -> dict[tuple[int, ...], str]:
        return {
            point.address: label
            for point, label in self.occurrence_labels
        }

    @property
    def addresses(self) -> frozenset[tuple[int, ...]]:
        return frozenset(self.label_by_address)


def reference_cp1_unfolding(
    model: GenerativeRelationModel | RelationalGenerativeModel,
    root: str,
    depth: int,
) -> CP1RelationalUnfolding:
    """Pair one finite recursive unfolding with a local maximal CP1 fibre tree."""
    if depth < 0:
        raise ValueError("depth must be non-negative")

    labels = model.unfold(root, depth)
    root_point = RelationalPoint()
    fibres = reference_maximal_cp1_tree(depth, root=root_point)
    occurrence_labels = tuple(
        sorted(
            (
                (RelationalPoint(address), label)
                for address, label in labels.items()
            ),
            key=lambda item: item[0].address,
        )
    )
    return CP1RelationalUnfolding(occurrence_labels, fibres)


PhaseMap = Callable[[TransportPath, TensorScalarElement], complex]


@dataclass(frozen=True)
class HolonomyPhaseRepresentation:
    """Explicit representation of closed relational holonomy in U(1).

    The phase map is supplied by a concrete realization. RTOFA does not assume
    that every abstract relational holonomy admits such a representation.
    """

    name: str
    phase_map: PhaseMap
    tolerance: float = 1e-10

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("phase representation name must be non-empty")
        if self.tolerance <= 0 or not isfinite(self.tolerance):
            raise ValueError("tolerance must be positive and finite")

    def phase(
        self,
        path: TransportPath,
        element: TensorScalarElement,
    ) -> complex:
        if not path.relation_path.closed:
            raise ValueError("phase representation requires closed relational holonomy")
        if element.carrier != path.relation_path.source:
            raise ValueError("phase representation element is not on the path source")
        value = complex(self.phase_map(path, element))
        if not (isfinite(value.real) and isfinite(value.imag)):
            raise ValueError("phase representation must be finite")
        modulus = abs(value)
        if abs(modulus - 1.0) > self.tolerance:
            raise ValueError("phase representation does not lie on U(1)")
        if modulus == 0.0:
            raise ValueError("zero cannot represent a U(1) phase")
        return value / modulus



OccurrencePhaseMap = Callable[[OccurrenceTransportPath, TensorScalarElement], complex]


@dataclass(frozen=True)
class OccurrenceHolonomyPhaseRepresentation:
    """Explicit U(1) representation of occurrence-closed relational holonomy.

    This is separate from value-level HolonomyPhaseRepresentation. Carrier
    closure alone is insufficient: the occurrence path must return to the same
    path-labelled occurrence address.
    """

    name: str
    phase_map: OccurrencePhaseMap
    tolerance: float = 1e-10

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("occurrence phase representation name must be non-empty")
        if self.tolerance <= 0 or not isfinite(self.tolerance):
            raise ValueError("tolerance must be positive and finite")

    def phase(
        self,
        path: OccurrenceTransportPath,
        element: TensorScalarElement,
    ) -> complex:
        if not path.occurrence_path.closed:
            raise ValueError(
                "occurrence phase representation requires occurrence-closed holonomy"
            )
        if element.carrier != path.occurrence_path.source:
            raise ValueError(
                "occurrence phase representation element is not on the path source"
            )
        value = complex(self.phase_map(path, element))
        if not (isfinite(value.real) and isfinite(value.imag)):
            raise ValueError("occurrence phase representation must be finite")
        modulus = abs(value)
        if abs(modulus - 1.0) > self.tolerance:
            raise ValueError("occurrence phase representation does not lie on U(1)")
        if modulus == 0.0:
            raise ValueError("zero cannot represent a U(1) occurrence phase")
        return value / modulus



def lift_value_phase_to_occurrence(
    representation: HolonomyPhaseRepresentation,
    *,
    name: str | None = None,
) -> OccurrenceHolonomyPhaseRepresentation:
    """Compose a value-level U(1) representation with occurrence forgetting.

    The induced occurrence representation is branch-blind: it depends only on
    the projected value-level transport path.
    """

    def phase_map(
        path: OccurrenceTransportPath,
        element: TensorScalarElement,
    ) -> complex:
        return representation.phase(path.value_transport_path, element)

    return OccurrenceHolonomyPhaseRepresentation(
        name or f"occurrence-lift:{representation.name}",
        phase_map,
        representation.tolerance,
    )
