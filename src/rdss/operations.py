from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .algebra import TensorScalarElement, TypedRelation


ElementMap = Callable[[TensorScalarElement], TensorScalarElement]
BinaryElementMap = Callable[[TensorScalarElement, TensorScalarElement], TensorScalarElement]


def reference_tensor_product(
    left: TensorScalarElement,
    right: TensorScalarElement,
) -> TensorScalarElement:
    """Reference tensor product for elements in the same carrier and semantic scale.

    The component storage is flattened, so this is intentionally a minimal
    Kronecker-style reference realization rather than a universal tensor engine.
    """
    if left.carrier != right.carrier:
        raise ValueError("reference tensor product requires the same carrier")
    if left.scale != right.scale:
        raise ValueError("reference tensor product requires the same semantic scale")

    p, q = left.rank
    r, s = right.rank
    components = tuple(a * b for a in left.components for b in right.components)
    return TensorScalarElement(
        components=components,
        rank=(p + r, q + s),
        carrier=left.carrier,
        scale=left.scale,
    )


@dataclass(frozen=True)
class RelationalProductRule:
    """Explicit relational product rule; no algebraic laws are assumed."""

    name: str
    rule: BinaryElementMap

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("product rule name must be non-empty")

    def __call__(
        self,
        left: TensorScalarElement,
        right: TensorScalarElement,
    ) -> TensorScalarElement:
        result = self.rule(left, right)
        if not isinstance(result, TensorScalarElement):
            raise TypeError("relational product must return TensorScalarElement")
        return result


@dataclass(frozen=True)
class RelationTransport:
    """Typed transport T_r along an explicit binary relation."""

    relation: TypedRelation
    mapping: ElementMap

    def __call__(self, element: TensorScalarElement) -> TensorScalarElement:
        if element.carrier != self.relation.source:
            raise ValueError("transport input is not on the relation source")
        result = self.mapping(element)
        if not isinstance(result, TensorScalarElement):
            raise TypeError("transport must return TensorScalarElement")
        if result.carrier != self.relation.target:
            raise ValueError("transport result is not on the relation target")
        return result


@dataclass(frozen=True)
class ContractionRule:
    """Explicit one-pair contraction rule.

    The kernel checks typing but does not invent an index metric or contraction
    formula. Those belong to a concrete realization.
    """

    name: str
    mapping: ElementMap

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("contraction rule name must be non-empty")

    def __call__(self, element: TensorScalarElement) -> TensorScalarElement:
        p, q = element.rank
        if p < 1 or q < 1:
            raise ValueError("one-pair contraction requires rank p>=1 and q>=1")
        result = self.mapping(element)
        if not isinstance(result, TensorScalarElement):
            raise TypeError("contraction must return TensorScalarElement")
        if result.rank != (p - 1, q - 1):
            raise ValueError("contraction must lower rank by exactly (1,1)")
        if result.carrier != element.carrier or result.scale != element.scale:
            raise ValueError("reference contraction must preserve carrier and scale")
        return result


@dataclass(frozen=True)
class OrbitalAction:
    """Typed orbital action with an optional explicit inverse."""

    name: str
    forward: ElementMap
    inverse: ElementMap | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("orbital action name must be non-empty")

    def act(self, element: TensorScalarElement) -> TensorScalarElement:
        result = self.forward(element)
        if not isinstance(result, TensorScalarElement):
            raise TypeError("orbital action must return TensorScalarElement")
        return result

    def invert(self, element: TensorScalarElement) -> TensorScalarElement:
        if self.inverse is None:
            raise ValueError("orbital action has no supplied inverse")
        result = self.inverse(element)
        if not isinstance(result, TensorScalarElement):
            raise TypeError("inverse orbital action must return TensorScalarElement")
        return result


def relative_moire_action(
    left: OrbitalAction,
    right: OrbitalAction,
    element: TensorScalarElement,
) -> TensorScalarElement:
    """Apply M_ij = U_i U_j^{-1} when U_j^{-1} is explicitly available."""
    return left.act(right.invert(element))
