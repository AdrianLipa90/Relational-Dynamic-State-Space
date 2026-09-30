from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from math import isfinite
from typing import Any, Callable


class EquivalenceKind(str, Enum):
    IDENTITY = "identity"
    EXACT_EQUIVALENCE = "exact_equivalence"
    ISOMORPHISM = "isomorphism"
    REFERENCE_REPRESENTATION = "reference_representation"
    FORGETFUL_PROJECTION = "forgetful_projection"
    APPROXIMATION = "approximation"


class InformationEffect(str, Enum):
    LOSSLESS = "lossless"
    LOSSY = "lossy"
    UNKNOWN = "unknown"


class ReductionError(RuntimeError):
    pass


class AmbiguousReductionError(ReductionError):
    pass


class ReductionCycleError(ReductionError):
    pass


class LossyReductionError(ReductionError):
    pass


def _type_tag(value: object) -> str:
    cls = type(value)
    return f"{cls.__module__}.{cls.__qualname__}"


def _freeze(value: Any) -> object:
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if not isfinite(value):
            raise ValueError("canonical form rejects non-finite float values")
        return ("float", value.hex())
    if isinstance(value, complex):
        if not (isfinite(value.real) and isfinite(value.imag)):
            raise ValueError("canonical form rejects non-finite complex values")
        return ("complex", value.real.hex(), value.imag.hex())
    if isinstance(value, Enum):
        return ("enum", _type_tag(value), _freeze(value.value))
    if isinstance(value, Mapping):
        items = tuple(
            sorted(
                ((_freeze(k), _freeze(v)) for k, v in value.items()),
                key=repr,
            )
        )
        return ("mapping", _type_tag(value), items)
    if is_dataclass(value) and not isinstance(value, type):
        payload = tuple(
            (field.name, _freeze(getattr(value, field.name)))
            for field in fields(value)
        )
        return ("dataclass", _type_tag(value), payload)
    if isinstance(value, tuple):
        return (
            "tuple",
            _type_tag(value),
            tuple(_freeze(item) for item in value),
        )
    if isinstance(value, list):
        return ("list", tuple(_freeze(item) for item in value))
    if isinstance(value, frozenset):
        return (
            "frozenset",
            tuple(sorted((_freeze(item) for item in value), key=repr)),
        )
    raise TypeError(f"unsupported canonical value type: {_type_tag(value)}")


@dataclass(frozen=True)
class CanonicalNormalForm:
    """Exact tagged normal form plus non-authoritative reduction provenance.

    The key determines strict canonical equality. Provenance records how a
    reducer reached the represented value and is deliberately excluded from
    semantic key comparison.
    """

    key: object
    provenance: tuple[str, ...] = ()

    def same_key(self, other: "CanonicalNormalForm") -> bool:
        if not isinstance(other, CanonicalNormalForm):
            return False
        return self.key == other.key


def strict_normal_form(value: object) -> CanonicalNormalForm:
    if isinstance(value, CanonicalNormalForm):
        return value
    return CanonicalNormalForm(_freeze(value))


Predicate = Callable[[object], bool]
Transform = Callable[[object], object]


@dataclass(frozen=True)
class ReductionRule:
    name: str
    applies: Predicate
    transform: Transform
    kind: EquivalenceKind
    information_effect: InformationEffect
    inverse: Transform | None = None
    preserves: tuple[str, ...] = ()
    claim_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("reduction rule name must be non-empty")
        if any(not item.strip() for item in self.preserves):
            raise ValueError("preserved invariant names must be non-empty")
        if any(not item.strip() for item in self.claim_ids):
            raise ValueError("claim ids must be non-empty")
        if self.kind is EquivalenceKind.ISOMORPHISM:
            if (
                self.information_effect is not InformationEffect.LOSSLESS
                or self.inverse is None
            ):
                raise ValueError(
                    "isomorphism rules require LOSSLESS effect and an inverse"
                )
        if self.kind in {
            EquivalenceKind.FORGETFUL_PROJECTION,
            EquivalenceKind.APPROXIMATION,
        } and self.information_effect is InformationEffect.LOSSLESS:
            raise ValueError(
                "projection/approximation cannot be declared LOSSLESS"
            )
        if (
            self.information_effect is InformationEffect.LOSSLESS
            and self.inverse is None
        ):
            raise ValueError(
                "LOSSLESS reduction requires an explicit inverse"
            )


@dataclass(frozen=True)
class ReductionStep:
    rule_name: str
    kind: EquivalenceKind
    information_effect: InformationEffect
    before_key: object
    after_key: object
    inverse_available: bool
    preserves: tuple[str, ...]
    claim_ids: tuple[str, ...]


@dataclass(frozen=True)
class ReductionTrace:
    steps: tuple[ReductionStep, ...]

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
        return all(
            step.information_effect is InformationEffect.LOSSLESS
            and step.inverse_available
            for step in self.steps
        )

    @property
    def provenance(self) -> tuple[str, ...]:
        return tuple(step.rule_name for step in self.steps)


@dataclass(frozen=True)
class ReductionResult:
    value: object
    trace: ReductionTrace

    @property
    def normal_form(self) -> CanonicalNormalForm:
        return CanonicalNormalForm(
            key=strict_normal_form(self.value).key,
            provenance=self.trace.provenance,
        )


@dataclass(frozen=True)
class EquivalenceResult:
    equivalent: bool
    left: ReductionResult
    right: ReductionResult

    @property
    def comparison_is_lossless(self) -> bool:
        return not (
            self.left.trace.lossy
            or self.right.trace.lossy
            or self.left.trace.unknown_information_effect
            or self.right.trace.unknown_information_effect
        )


class ReductionEngine:
    """Deterministic fail-closed reducer.

    Exactly one rule may apply at each step. Competing rules are reported as
    ambiguity instead of being resolved by registration order.
    """

    def __init__(
        self,
        rules: tuple[ReductionRule, ...] = (),
    ) -> None:
        names = [rule.name for rule in rules]
        if len(names) != len(set(names)):
            raise ValueError("reduction rule names must be unique")
        self._rules = tuple(rules)

    @property
    def rules(self) -> tuple[ReductionRule, ...]:
        return self._rules

    def reduce(
        self,
        value: object,
        *,
        max_steps: int = 64,
    ) -> ReductionResult:
        if max_steps <= 0:
            raise ValueError("max_steps must be positive")

        current = value
        current_key = strict_normal_form(current).key
        seen = {current_key}
        steps: list[ReductionStep] = []

        for _ in range(max_steps):
            applicable = tuple(
                rule
                for rule in self._rules
                if bool(rule.applies(current))
            )
            if not applicable:
                return ReductionResult(
                    current,
                    ReductionTrace(tuple(steps)),
                )
            if len(applicable) > 1:
                names = ", ".join(
                    rule.name for rule in applicable
                )
                raise AmbiguousReductionError(
                    f"multiple reduction rules apply: {names}"
                )

            rule = applicable[0]
            next_value = rule.transform(current)
            next_key = strict_normal_form(next_value).key

            if next_key == current_key or next_key in seen:
                raise ReductionCycleError(
                    f"reduction rule {rule.name!r} "
                    "does not make acyclic progress"
                )

            steps.append(
                ReductionStep(
                    rule_name=rule.name,
                    kind=rule.kind,
                    information_effect=rule.information_effect,
                    before_key=current_key,
                    after_key=next_key,
                    inverse_available=rule.inverse is not None,
                    preserves=rule.preserves,
                    claim_ids=rule.claim_ids,
                )
            )
            current = next_value
            current_key = next_key
            seen.add(current_key)

        raise ReductionError(
            f"reduction exceeded max_steps={max_steps}"
        )

    def compare(
        self,
        left: object,
        right: object,
        *,
        allow_lossy: bool = False,
        max_steps: int = 64,
    ) -> EquivalenceResult:
        left_result = self.reduce(left, max_steps=max_steps)
        right_result = self.reduce(right, max_steps=max_steps)

        if not allow_lossy:
            traces = (left_result.trace, right_result.trace)
            if any(
                trace.lossy
                or trace.unknown_information_effect
                for trace in traces
            ):
                raise LossyReductionError(
                    "comparison crossed LOSSY/UNKNOWN reduction; "
                    "pass allow_lossy=True explicitly"
                )

        return EquivalenceResult(
            equivalent=left_result.normal_form.same_key(
                right_result.normal_form
            ),
            left=left_result,
            right=right_result,
        )


def roundtrip_check(
    rule: ReductionRule,
    value: object,
) -> bool:
    if rule.inverse is None:
        raise ValueError(
            "roundtrip check requires an explicit inverse"
        )
    if not rule.applies(value):
        raise ValueError(
            "reduction rule does not apply to supplied value"
        )

    reduced = rule.transform(value)
    recovered = rule.inverse(reduced)
    return strict_normal_form(recovered).same_key(
        strict_normal_form(value)
    )
