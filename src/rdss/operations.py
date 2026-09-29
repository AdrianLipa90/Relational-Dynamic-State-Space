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



@dataclass(frozen=True)
class RelationPath:
    """Composable ordered path of typed binary relations."""

    relations: tuple[TypedRelation, ...]

    def __post_init__(self) -> None:
        if not self.relations:
            raise ValueError("relation path must contain at least one relation")
        for left, right in zip(self.relations, self.relations[1:]):
            if left.target != right.source:
                raise ValueError("relation path is not composable")

    @property
    def source(self):
        return self.relations[0].source

    @property
    def target(self):
        return self.relations[-1].target

    @property
    def closed(self) -> bool:
        return self.source == self.target


@dataclass(frozen=True)
class TransportPath:
    """A relation path together with one transport for each edge."""

    transports: tuple[RelationTransport, ...]

    def __post_init__(self) -> None:
        if not self.transports:
            raise ValueError("transport path must contain at least one transport")
        relations = tuple(t.relation for t in self.transports)
        RelationPath(relations)

    @property
    def relation_path(self) -> RelationPath:
        return RelationPath(tuple(t.relation for t in self.transports))

    def apply(self, element: TensorScalarElement) -> TensorScalarElement:
        if element.carrier != self.relation_path.source:
            raise ValueError("element is not on the path source")
        current = element
        for transport in self.transports:
            current = transport(current)
        return current

    def holonomy_residual(self, element: TensorScalarElement) -> float:
        """Norm of T_gamma(X)-X for a closed relational path."""
        path = self.relation_path
        if not path.closed:
            raise ValueError("holonomy residual requires a closed relation path")
        final = self.apply(element)
        return abs(final - element)


def transport_composition_residual(
    direct: RelationTransport,
    first: RelationTransport,
    second: RelationTransport,
    element: TensorScalarElement,
) -> float:
    """Measure failure of direct transport to equal sequential transport."""
    if first.relation.target != second.relation.source:
        raise ValueError("sequential transports are not composable")
    if direct.relation.source != first.relation.source:
        raise ValueError("direct and sequential transports have different sources")
    if direct.relation.target != second.relation.target:
        raise ValueError("direct and sequential transports have different targets")

    direct_value = direct(element)
    sequential_value = second(first(element))
    return abs(direct_value - sequential_value)



def product_bilinearity_residuals(
    product: RelationalProductRule,
    x: TensorScalarElement,
    y: TensorScalarElement,
    z: TensorScalarElement,
    scalar: complex,
) -> dict[str, float]:
    """Measure additivity and scalar-linearity defects of the relational product.

    Exact K-bilinearity is the special case where all four residuals vanish.
    """
    left_add = product(x + y, z) - (product(x, z) + product(y, z))
    right_add = product(x, y + z) - (product(x, y) + product(x, z))
    left_scalar = product(x.scale_by(scalar), y) - product(x, y).scale_by(scalar)
    right_scalar = product(x, y.scale_by(scalar)) - product(x, y).scale_by(scalar)
    return {
        "left_additivity": abs(left_add),
        "right_additivity": abs(right_add),
        "left_scalar": abs(left_scalar),
        "right_scalar": abs(right_scalar),
    }


def orbital_inverse_residual(
    action: OrbitalAction,
    element: TensorScalarElement,
) -> float:
    """Check supplied inverse in both orders on one reference element."""
    forward_back = action.invert(action.act(element)) - element
    back_forward = action.act(action.invert(element)) - element
    return max(abs(forward_back), abs(back_forward))


def orbital_composition_residual(
    composed: OrbitalAction,
    left: OrbitalAction,
    right: OrbitalAction,
    element: TensorScalarElement,
) -> float:
    """Measure U_(gh) X - U_g(U_h X) for a supplied composition representative."""
    direct = composed.act(element)
    sequential = left.act(right.act(element))
    return abs(direct - sequential)
