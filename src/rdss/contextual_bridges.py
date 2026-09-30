from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Callable

from .algebra import RelationalPoint
from .canonical import EquivalenceKind, InformationEffect
from .closure import BranchRelationOccurrence
from .operations import TypedRelation
from .signature import SignatureEngine, rdss_signature_engine


class ContextualBridgeError(RuntimeError):
    pass


class UnsupportedContextualBridgeError(ContextualBridgeError):
    pass


class AmbiguousContextualBridgeError(ContextualBridgeError):
    pass


class ContextualBridgeTypeError(ContextualBridgeError):
    pass


class ContextualBridgeDirection(str, Enum):
    FORWARD = "forward"


@dataclass(frozen=True)
class CarrierMapContext:
    """Finite symbolic-label to RelationalPoint context.

    The map is contextual data. It is not part of BranchRelationOccurrence
    identity and is not inferred from relation labels.
    """

    entries: tuple[tuple[str, RelationalPoint], ...]

    def __post_init__(self) -> None:
        labels = [label for label, _ in self.entries]
        if any(not label.strip() for label in labels):
            raise ValueError("carrier context labels must be non-empty")
        if len(labels) != len(set(labels)):
            raise ValueError("carrier context labels must be unique")
        if any(
            not isinstance(point, RelationalPoint)
            for _, point in self.entries
        ):
            raise TypeError(
                "carrier context values must be RelationalPoint"
            )

    @classmethod
    def from_mapping(
        cls,
        mapping: Mapping[str, RelationalPoint],
    ) -> "CarrierMapContext":
        return cls(
            tuple(
                sorted(
                    mapping.items(),
                    key=lambda item: item[0],
                )
            )
        )

    @property
    def mapping(self) -> dict[str, RelationalPoint]:
        return dict(self.entries)

    def resolve(self, label: str) -> RelationalPoint:
        try:
            return self.mapping[label]
        except KeyError as exc:
            raise KeyError(
                f"carrier context has no label {label!r}"
            ) from exc


ContextPredicate = Callable[[object], bool]
ContextualTransform = Callable[[object, object], object]


@dataclass(frozen=True)
class ContextualBridgeSpec:
    name: str
    source_family: str
    target_family: str
    context_name: str
    source_check: ContextPredicate
    context_check: ContextPredicate
    target_check: ContextPredicate
    transform: ContextualTransform
    kind: EquivalenceKind
    information_effect: InformationEffect
    preserves: tuple[str, ...] = ()
    claim_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError(
                "contextual bridge name must be non-empty"
            )
        if not self.source_family.strip():
            raise ValueError(
                "contextual bridge source family must be non-empty"
            )
        if not self.target_family.strip():
            raise ValueError(
                "contextual bridge target family must be non-empty"
            )
        if not self.context_name.strip():
            raise ValueError(
                "contextual bridge context name must be non-empty"
            )
        if self.kind is EquivalenceKind.IDENTITY:
            raise ValueError(
                "contextual bridge cannot declare cross-family identity"
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
                "projection/approximation contextual bridge "
                "cannot be LOSSLESS"
            )
        if any(not item.strip() for item in self.preserves):
            raise ValueError(
                "contextual bridge preserved invariants "
                "must be non-empty"
            )
        if any(not item.strip() for item in self.claim_ids):
            raise ValueError(
                "contextual bridge claim ids must be non-empty"
            )


@dataclass(frozen=True)
class ContextualBridgeStep:
    bridge_name: str
    context_name: str
    kind: EquivalenceKind
    information_effect: InformationEffect
    source_family: str
    target_family: str
    preserves: tuple[str, ...]
    claim_ids: tuple[str, ...]


@dataclass(frozen=True)
class ContextualBridgeResult:
    value: object
    step: ContextualBridgeStep

    @property
    def lossy(self) -> bool:
        return (
            self.step.information_effect
            is InformationEffect.LOSSY
        )


class ContextualBridgeRegistry:
    """Fail-closed registry for bridges requiring caller-supplied context.

    These bridges are intentionally separate from BridgeRegistry so that
    missing context cannot become an implicit global equivalence edge.
    """

    def __init__(
        self,
        specs: tuple[ContextualBridgeSpec, ...],
        *,
        signature_engine: SignatureEngine | None = None,
    ) -> None:
        names = [spec.name for spec in specs]
        if len(names) != len(set(names)):
            raise ValueError(
                "contextual bridge names must be unique"
            )
        self._specs = tuple(specs)
        self._signature_engine = (
            signature_engine or rdss_signature_engine()
        )

    @property
    def specs(self) -> tuple[ContextualBridgeSpec, ...]:
        return self._specs

    def direct(
        self,
        value: object,
        target_family: str,
        *,
        context: object,
    ) -> ContextualBridgeResult:
        source_signature = self._signature_engine.signature(
            value
        )
        candidates = tuple(
            spec
            for spec in self._specs
            if spec.source_family == source_signature.family
            and spec.target_family == target_family
            and bool(spec.source_check(value))
            and bool(spec.context_check(context))
        )

        if not candidates:
            raise UnsupportedContextualBridgeError(
                f"no contextual bridge from "
                f"{source_signature.family!r} "
                f"to {target_family!r} for supplied context"
            )
        if len(candidates) > 1:
            names = ", ".join(
                spec.name for spec in candidates
            )
            raise AmbiguousContextualBridgeError(
                f"multiple contextual bridges apply: {names}"
            )

        spec = candidates[0]
        target = spec.transform(value, context)
        if not spec.target_check(target):
            raise ContextualBridgeTypeError(
                f"contextual bridge {spec.name!r} "
                "produced invalid target"
            )
        target_signature = self._signature_engine.signature(
            target
        )
        if target_signature.family != spec.target_family:
            raise ContextualBridgeTypeError(
                f"contextual bridge {spec.name!r} promised "
                f"{spec.target_family!r}, got "
                f"{target_signature.family!r}"
            )

        return ContextualBridgeResult(
            value=target,
            step=ContextualBridgeStep(
                bridge_name=spec.name,
                context_name=spec.context_name,
                kind=spec.kind,
                information_effect=spec.information_effect,
                source_family=spec.source_family,
                target_family=spec.target_family,
                preserves=spec.preserves,
                claim_ids=spec.claim_ids,
            ),
        )


def materialize_branch_relation_occurrence(
    value: BranchRelationOccurrence,
    context: CarrierMapContext,
) -> TypedRelation:
    """Materialize a symbolic branch occurrence into a typed relation.

    The branch slot itself is intentionally forgotten by this projection.
    """
    if not isinstance(value, BranchRelationOccurrence):
        raise TypeError(
            "value must be BranchRelationOccurrence"
        )
    if not isinstance(context, CarrierMapContext):
        raise TypeError("context must be CarrierMapContext")
    return value.as_typed_relation(context.mapping)


def rdss_contextual_bridge_specs(
) -> tuple[ContextualBridgeSpec, ...]:
    return (
        ContextualBridgeSpec(
            name="materialize_branch_relation_occurrence",
            source_family="branch_relation_occurrence",
            target_family="typed_relation",
            context_name="carrier_label_map",
            source_check=lambda value: isinstance(
                value,
                BranchRelationOccurrence,
            ),
            context_check=lambda context: isinstance(
                context,
                CarrierMapContext,
            ),
            target_check=lambda value: isinstance(
                value,
                TypedRelation,
            ),
            transform=materialize_branch_relation_occurrence,
            kind=EquivalenceKind.FORGETFUL_PROJECTION,
            information_effect=InformationEffect.LOSSY,
            preserves=(
                "relation label",
                "source endpoint through supplied carrier map",
                "target endpoint through supplied carrier map",
            ),
            claim_ids=(
                "DEF_CONTEXTUAL_BRANCH_RELATION_MATERIALIZATION",
                "DEF_RELATIONAL_DISTINCTION",
            ),
        ),
    )


def rdss_contextual_bridge_registry(
) -> ContextualBridgeRegistry:
    return ContextualBridgeRegistry(
        rdss_contextual_bridge_specs()
    )
