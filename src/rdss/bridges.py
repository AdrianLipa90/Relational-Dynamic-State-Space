from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from .canonical import EquivalenceKind, InformationEffect, strict_normal_form
from .signature import (
    RDSSSignature,
    SignatureComparison,
    SignatureEngine,
    rdss_signature_engine,
)


Predicate = Callable[[object], bool]
Transform = Callable[[object], object]
RoundtripValidator = Callable[[object, object], bool]


class BridgeError(RuntimeError):
    pass


class UnsupportedBridgeError(BridgeError):
    pass


class AmbiguousBridgeError(BridgeError):
    pass


class BridgeTypeError(BridgeError):
    pass


class BridgeRoundtripError(BridgeError):
    pass


class LossyBridgeError(BridgeError):
    pass


class BridgeDirection(str, Enum):
    FORWARD = "forward"
    INVERSE = "inverse"


@dataclass(frozen=True)
class BridgeSpec:
    """Explicit typed bridge between two semantic signature families."""

    name: str
    source_family: str
    target_family: str
    forward: Transform
    source_check: Predicate
    target_check: Predicate
    kind: EquivalenceKind
    information_effect: InformationEffect
    inverse: Transform | None = None
    roundtrip_validator: RoundtripValidator | None = None
    preserves: tuple[str, ...] = ()
    claim_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("bridge name must be non-empty")
        if not self.source_family.strip() or not self.target_family.strip():
            raise ValueError("bridge families must be non-empty")
        if any(not item.strip() for item in self.preserves):
            raise ValueError("bridge preserved invariants must be non-empty")
        if any(not item.strip() for item in self.claim_ids):
            raise ValueError("bridge claim ids must be non-empty")
        if self.kind is EquivalenceKind.IDENTITY:
            raise ValueError(
                "cross-representation identity must not be registered as a bridge"
            )
        if self.kind is EquivalenceKind.ISOMORPHISM:
            if (
                self.information_effect is not InformationEffect.LOSSLESS
                or self.inverse is None
            ):
                raise ValueError(
                    "isomorphism bridge requires LOSSLESS effect and inverse"
                )
        if (
            self.information_effect is InformationEffect.LOSSLESS
            and self.inverse is None
        ):
            raise ValueError(
                "LOSSLESS bridge requires an explicit inverse"
            )
        if (
            self.kind
            in {
                EquivalenceKind.FORGETFUL_PROJECTION,
                EquivalenceKind.APPROXIMATION,
            }
            and self.information_effect is InformationEffect.LOSSLESS
        ):
            raise ValueError(
                "projection/approximation bridge cannot be LOSSLESS"
            )


@dataclass(frozen=True)
class BridgeStep:
    bridge_name: str
    direction: BridgeDirection
    kind: EquivalenceKind
    information_effect: InformationEffect
    source_family: str
    target_family: str
    source_key: object
    target_key: object
    roundtrip_verified: bool
    preserves: tuple[str, ...]
    claim_ids: tuple[str, ...]


@dataclass(frozen=True)
class BridgeRoute:
    value: object
    steps: tuple[BridgeStep, ...]

    @property
    def lossy(self) -> bool:
        return any(
            step.information_effect is InformationEffect.LOSSY
            for step in self.steps
        )

    @property
    def unknown_information_effect(self) -> bool:
        return any(
            step.information_effect is InformationEffect.UNKNOWN
            for step in self.steps
        )

    @property
    def fully_reversible(self) -> bool:
        return bool(self.steps) and all(
            step.information_effect is InformationEffect.LOSSLESS
            and step.roundtrip_verified
            for step in self.steps
        )

    @property
    def provenance(self) -> tuple[str, ...]:
        return tuple(
            f"{step.bridge_name}:{step.direction.value}"
            for step in self.steps
        )


@dataclass(frozen=True)
class BridgeComparison:
    route: BridgeRoute
    comparison: SignatureComparison

    @property
    def equivalent_after_bridge(self) -> bool:
        return self.comparison.kind.value in {
            "exact_signature",
            "same_semantic_state_different_representation",
        }


@dataclass(frozen=True)
class _BridgeEdge:
    spec: BridgeSpec
    direction: BridgeDirection

    @property
    def source_family(self) -> str:
        if self.direction is BridgeDirection.FORWARD:
            return self.spec.source_family
        return self.spec.target_family

    @property
    def target_family(self) -> str:
        if self.direction is BridgeDirection.FORWARD:
            return self.spec.target_family
        return self.spec.source_family

    @property
    def transform(self) -> Transform:
        if self.direction is BridgeDirection.FORWARD:
            return self.spec.forward
        if self.spec.inverse is None:
            raise UnsupportedBridgeError(
                f"bridge {self.spec.name!r} has no inverse"
            )
        return self.spec.inverse

    @property
    def inverse_transform(self) -> Transform | None:
        if self.direction is BridgeDirection.FORWARD:
            return self.spec.inverse
        return self.spec.forward

    @property
    def source_check(self) -> Predicate:
        if self.direction is BridgeDirection.FORWARD:
            return self.spec.source_check
        return self.spec.target_check

    @property
    def target_check(self) -> Predicate:
        if self.direction is BridgeDirection.FORWARD:
            return self.spec.target_check
        return self.spec.source_check


class BridgeRegistry:
    """Explicit graph of legal inter-family transformations.

    The registry never infers a bridge from similar signatures. Reverse edges
    exist only when an explicit inverse was supplied.
    """

    def __init__(
        self,
        bridges: tuple[BridgeSpec, ...],
        *,
        signature_engine: SignatureEngine | None = None,
    ) -> None:
        names = [bridge.name for bridge in bridges]
        if len(names) != len(set(names)):
            raise ValueError("bridge names must be unique")
        self._bridges = tuple(bridges)
        self._signature_engine = signature_engine or rdss_signature_engine()

    @property
    def bridges(self) -> tuple[BridgeSpec, ...]:
        return self._bridges

    @property
    def signature_engine(self) -> SignatureEngine:
        return self._signature_engine

    def _edges_from(
        self,
        family: str,
        value: object,
    ) -> tuple[_BridgeEdge, ...]:
        edges: list[_BridgeEdge] = []
        for spec in self._bridges:
            forward = _BridgeEdge(spec, BridgeDirection.FORWARD)
            if (
                forward.source_family == family
                and bool(forward.source_check(value))
            ):
                edges.append(forward)

            if spec.inverse is not None:
                inverse = _BridgeEdge(spec, BridgeDirection.INVERSE)
                if (
                    inverse.source_family == family
                    and bool(inverse.source_check(value))
                ):
                    edges.append(inverse)
        return tuple(edges)

    def _apply_edge(
        self,
        value: object,
        edge: _BridgeEdge,
    ) -> tuple[object, BridgeStep]:
        source_signature = self._signature_engine.signature(value)
        if source_signature.family != edge.source_family:
            raise BridgeTypeError(
                f"bridge {edge.spec.name!r} expects family "
                f"{edge.source_family!r}, got {source_signature.family!r}"
            )
        if not edge.source_check(value):
            raise BridgeTypeError(
                f"bridge {edge.spec.name!r} rejected source value"
            )

        target = edge.transform(value)
        if not edge.target_check(target):
            raise BridgeTypeError(
                f"bridge {edge.spec.name!r} produced invalid target type"
            )
        target_signature = self._signature_engine.signature(target)
        if target_signature.family != edge.target_family:
            raise BridgeTypeError(
                f"bridge {edge.spec.name!r} promised target family "
                f"{edge.target_family!r}, got {target_signature.family!r}"
            )

        roundtrip_verified = False
        inverse_transform = edge.inverse_transform
        if edge.spec.information_effect is InformationEffect.LOSSLESS:
            if inverse_transform is None:
                raise BridgeRoundtripError(
                    f"LOSSLESS bridge {edge.spec.name!r} has no inverse"
                )
            recovered = inverse_transform(target)
            if edge.spec.roundtrip_validator is None:
                roundtrip_verified = strict_normal_form(recovered).same_key(
                    strict_normal_form(value)
                )
            else:
                roundtrip_verified = bool(
                    edge.spec.roundtrip_validator(
                        value,
                        recovered,
                    )
                )
            if not roundtrip_verified:
                raise BridgeRoundtripError(
                    f"bridge {edge.spec.name!r} failed strict round trip"
                )

        step = BridgeStep(
            bridge_name=edge.spec.name,
            direction=edge.direction,
            kind=edge.spec.kind,
            information_effect=edge.spec.information_effect,
            source_family=edge.source_family,
            target_family=edge.target_family,
            source_key=source_signature.semantic_key,
            target_key=target_signature.semantic_key,
            roundtrip_verified=roundtrip_verified,
            preserves=edge.spec.preserves,
            claim_ids=edge.spec.claim_ids,
        )
        return target, step

    def direct(
        self,
        value: object,
        target_family: str,
    ) -> BridgeRoute:
        source_signature = self._signature_engine.signature(value)
        candidates = tuple(
            edge
            for edge in self._edges_from(
                source_signature.family,
                value,
            )
            if edge.target_family == target_family
        )
        if not candidates:
            raise UnsupportedBridgeError(
                f"no direct bridge from {source_signature.family!r} "
                f"to {target_family!r}"
            )
        if len(candidates) > 1:
            names = ", ".join(
                edge.spec.name for edge in candidates
            )
            raise AmbiguousBridgeError(
                f"multiple direct bridges apply: {names}"
            )

        target, step = self._apply_edge(value, candidates[0])
        return BridgeRoute(target, (step,))

    def route(
        self,
        value: object,
        target_family: str,
        *,
        max_hops: int = 4,
    ) -> BridgeRoute:
        if max_hops <= 0:
            raise ValueError("max_hops must be positive")

        start_signature = self._signature_engine.signature(value)
        if start_signature.family == target_family:
            return BridgeRoute(value, ())

        frontier: list[tuple[object, tuple[BridgeStep, ...]]] = [
            (value, ())
        ]
        seen: set[tuple[str, object]] = {
            (
                start_signature.family,
                strict_normal_form(value).key,
            )
        }

        for depth in range(1, max_hops + 1):
            next_frontier: list[
                tuple[object, tuple[BridgeStep, ...]]
            ] = []
            solutions: list[BridgeRoute] = []

            for current, steps in frontier:
                signature = self._signature_engine.signature(current)
                for edge in self._edges_from(
                    signature.family,
                    current,
                ):
                    target, step = self._apply_edge(current, edge)
                    route_steps = steps + (step,)
                    target_signature = self._signature_engine.signature(target)

                    if target_signature.family == target_family:
                        solutions.append(
                            BridgeRoute(target, route_steps)
                        )
                        continue

                    key = (
                        target_signature.family,
                        strict_normal_form(target).key,
                    )
                    if key in seen:
                        continue
                    seen.add(key)
                    next_frontier.append(
                        (target, route_steps)
                    )

            if solutions:
                route_keys = {
                    (
                        strict_normal_form(route.value).key,
                        tuple(
                            (
                                step.bridge_name,
                                step.direction.value,
                            )
                            for step in route.steps
                        ),
                    )
                    for route in solutions
                }
                if len(route_keys) > 1:
                    raise AmbiguousBridgeError(
                        "multiple shortest bridge routes reach "
                        f"family {target_family!r}"
                    )
                return solutions[0]

            frontier = next_frontier
            if not frontier:
                break

        raise UnsupportedBridgeError(
            f"no bridge route to family {target_family!r} "
            f"within max_hops={max_hops}"
        )

    def compare(
        self,
        left: object,
        right: object,
        *,
        allow_lossy: bool = False,
        max_hops: int = 4,
    ) -> BridgeComparison:
        right_signature = self._signature_engine.signature(right)
        route = self.route(
            left,
            right_signature.family,
            max_hops=max_hops,
        )
        if (
            not allow_lossy
            and (
                route.lossy
                or route.unknown_information_effect
            )
        ):
            raise LossyBridgeError(
                "bridge route crosses LOSSY/UNKNOWN information effect; "
                "pass allow_lossy=True explicitly"
            )
        comparison = self._signature_engine.compare(
            route.value,
            right,
        )
        return BridgeComparison(route, comparison)


def rdss_bridge_specs() -> tuple[BridgeSpec, ...]:
    """Return only bridges already justified by the current RDSS ledger."""
    from .algebra import (
        OccurrenceAddress,
        RelationalPoint,
        TensorScalarElement,
        TypedRelation,
        TypedZero,
    )
    from .closure import (
        BinaryDistinction,
        GenerativeRelationModel,
        RelationalBinaryDistinction,
        RelationalGenerativeModel,
    )
    from .operations import (
        OccurrenceRelationPath,
        RelationOccurrence,
        RelationPath,
        forget_occurrence_path,
        forget_relation_occurrence,
    )
    from .phase import U1Phase, U1_TOLERANCE
    from .realizations import reference_point_from_occurrence
    from .zero_axis import (
        ZeroAxisPoint,
        finite_zero_axis_lift_u1,
        finite_zero_axis_phase,
    )

    return (
        BridgeSpec(
            name="occurrence_to_reference_point",
            source_family="occurrence_address",
            target_family="relational_carrier",
            forward=reference_point_from_occurrence,
            inverse=lambda value: OccurrenceAddress(value.address),
            source_check=lambda value: isinstance(
                value,
                OccurrenceAddress,
            ),
            target_check=lambda value: isinstance(
                value,
                RelationalPoint,
            ),
            kind=EquivalenceKind.REFERENCE_REPRESENTATION,
            information_effect=InformationEffect.LOSSLESS,
            preserves=("binary coordinate word",),
            claim_ids=(
                "DEF_CARRIER_OCCURRENCE_SEPARATION",
                "REF_RELATIONAL_POINT_BINARY_COORDINATE",
            ),
        ),
        BridgeSpec(
            name="u1_to_finite_zero_axis",
            source_family="u1_phase",
            target_family="zero_axis_point",
            forward=finite_zero_axis_lift_u1,
            inverse=finite_zero_axis_phase,
            roundtrip_validator=lambda original, recovered: (
                (
                    isinstance(original, U1Phase)
                    and isinstance(recovered, U1Phase)
                    and abs(original.value - recovered.value)
                    <= 10.0 * U1_TOLERANCE
                )
                or
                (
                    isinstance(original, ZeroAxisPoint)
                    and isinstance(recovered, ZeroAxisPoint)
                    and abs(original.t - recovered.t)
                    <= 10.0 * U1_TOLERANCE
                )
            ),
            source_check=lambda value: (
                isinstance(value, U1Phase)
                and abs(1.0 + value.value) > U1_TOLERANCE
            ),
            target_check=lambda value: isinstance(
                value,
                ZeroAxisPoint,
            ),
            kind=EquivalenceKind.REFERENCE_REPRESENTATION,
            information_effect=InformationEffect.LOSSLESS,
            preserves=(
                "finite U(1) phase",
                "finite Zero-Axis coordinate",
                "projective Omega correspondence",
            ),
            claim_ids=(
                "REF_U1_ZERO_AXIS_FINITE_BRIDGE",
                "ZA_BRIDGE",
            ),
        ),
        BridgeSpec(
            name="typed_zero_to_zero_element",
            source_family="typed_zero",
            target_family="tensor_scalar_element",
            forward=lambda value: value.as_element(),
            inverse=TypedZero.from_element,
            source_check=lambda value: isinstance(value, TypedZero),
            target_check=lambda value: (
                isinstance(value, TensorScalarElement)
                and all(component == 0j for component in value.components)
            ),
            kind=EquivalenceKind.REFERENCE_REPRESENTATION,
            information_effect=InformationEffect.LOSSLESS,
            preserves=(
                "tensor rank",
                "carrier",
                "semantic scale",
                "component dimension",
                "additive zero",
            ),
            claim_ids=(
                "DEF_TYPED_ZERO",
                "DEF_TS",
                "PRIM_MODULE",
            ),
        ),
        BridgeSpec(
            name="forget_relation_occurrence",
            source_family="relation_occurrence",
            target_family="typed_relation",
            forward=forget_relation_occurrence,
            source_check=lambda value: isinstance(
                value,
                RelationOccurrence,
            ),
            target_check=lambda value: isinstance(
                value,
                TypedRelation,
            ),
            kind=EquivalenceKind.FORGETFUL_PROJECTION,
            information_effect=InformationEffect.LOSSY,
            preserves=(
                "typed relation value",
                "source carrier",
                "target carrier",
            ),
            claim_ids=(
                "DEF_OCCURRENCE_FORGETFUL_PROJECTION",
            ),
        ),
        BridgeSpec(
            name="forget_relational_generative_binding",
            source_family="relational_generative_model",
            target_family="generative_relation_model",
            forward=lambda value: value.as_ra0_star_model(),
            source_check=lambda value: isinstance(
                value,
                RelationalGenerativeModel,
            ),
            target_check=lambda value: isinstance(
                value,
                GenerativeRelationModel,
            ),
            kind=EquivalenceKind.FORGETFUL_PROJECTION,
            information_effect=InformationEffect.LOSSY,
            preserves=(
                "admitted carrier labels",
                "binary distinction hosts",
                "left endpoint labels",
                "right endpoint labels",
            ),
            claim_ids=(
                "THM_RA0_STAR_FROM_RA0_REL_STAR",
                "RA0_REL_STAR",
                "RA0_STAR",
            ),
        ),
        BridgeSpec(
            name="forget_relational_distinction_binding",
            source_family="relational_binary_distinction",
            target_family="binary_distinction",
            forward=lambda value: value.binary,
            source_check=lambda value: isinstance(
                value,
                RelationalBinaryDistinction,
            ),
            target_check=lambda value: isinstance(
                value,
                BinaryDistinction,
            ),
            kind=EquivalenceKind.FORGETFUL_PROJECTION,
            information_effect=InformationEffect.LOSSY,
            preserves=(
                "host label",
                "left endpoint label",
                "right endpoint label",
                "binary branch slots",
            ),
            claim_ids=(
                "DEF_RELATIONAL_DISTINCTION",
                "DEF_BINARY_DISTINCTION",
            ),
        ),
        BridgeSpec(
            name="forget_occurrence_path",
            source_family="occurrence_relation_path",
            target_family="relation_path",
            forward=forget_occurrence_path,
            source_check=lambda value: isinstance(
                value,
                OccurrenceRelationPath,
            ),
            target_check=lambda value: isinstance(
                value,
                RelationPath,
            ),
            kind=EquivalenceKind.FORGETFUL_PROJECTION,
            information_effect=InformationEffect.LOSSY,
            preserves=(
                "ordered relation values",
                "carrier composability",
            ),
            claim_ids=(
                "DEF_OCCURRENCE_FORGETFUL_PROJECTION",
                "THM_OCCURRENCE_COMPOSABILITY_PROJECTS",
            ),
        ),
    )


def rdss_bridge_registry() -> BridgeRegistry:
    return BridgeRegistry(rdss_bridge_specs())
