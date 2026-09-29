from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .algebra import SemanticScale, SemanticScaleGraph, TensorScalarElement, TypedRelation


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



def orbital_identity_residual(
    identity: OrbitalAction,
    element: TensorScalarElement,
) -> float:
    """Measure U_e X - X for a supplied identity representative."""
    return abs(identity.act(element) - element)



@dataclass(frozen=True)
class SemanticScaleMap:
    """Executable coarse-graining morphism S_(sigma->tau)."""

    graph: SemanticScaleGraph
    source: SemanticScale
    target: SemanticScale
    mapping: ElementMap

    def __post_init__(self) -> None:
        if not self.graph.can_coarsen(self.source.label, self.target.label):
            raise ValueError("semantic scale graph does not admit this coarse-graining")

    def __call__(self, element: TensorScalarElement) -> TensorScalarElement:
        if element.scale != self.source:
            raise ValueError("semantic scale map input has the wrong source scale")
        result = self.mapping(element)
        if not isinstance(result, TensorScalarElement):
            raise TypeError("semantic scale map must return TensorScalarElement")
        if result.scale != self.target:
            raise ValueError("semantic scale map result has the wrong target scale")
        if result.carrier != element.carrier or result.rank != element.rank:
            raise ValueError("reference semantic scale map preserves carrier and tensor rank")
        return result


def semantic_orbital_commutator_residual(
    scale_map: SemanticScaleMap,
    orbital: OrbitalAction,
    element: TensorScalarElement,
) -> float:
    """Measure U S X - S U X for a semantic-scale/orbital pair."""
    orbital_after_scale = orbital.act(scale_map(element))
    scale_after_orbital = scale_map(orbital.act(element))
    return abs(orbital_after_scale - scale_after_orbital)



@dataclass(frozen=True)
class BranchRefinementMap:
    """Typed branch refinement F_-/F_+ from level n to level n+1."""

    branch: int
    target_scale: SemanticScale
    mapping: ElementMap

    def __post_init__(self) -> None:
        if self.branch not in (-1, 1):
            raise ValueError("refinement branch must be -1 or +1")

    def __call__(self, element: TensorScalarElement) -> TensorScalarElement:
        result = self.mapping(element)
        if not isinstance(result, TensorScalarElement):
            raise TypeError("refinement map must return TensorScalarElement")
        expected_carrier = type(element.carrier)(
            element.carrier.address + (self.branch,)
        )
        if result.carrier != expected_carrier:
            raise ValueError("refinement result is not on the selected child carrier")
        if result.rank != element.rank:
            raise ValueError("reference refinement preserves tensor rank")
        if result.scale != self.target_scale:
            raise ValueError("refinement result has the wrong target semantic scale")
        return result


def typed_refinement_residual(
    refinement: BranchRefinementMap,
    product: RelationalProductRule,
    x: TensorScalarElement,
    y: TensorScalarElement,
) -> float:
    """Measure F(X star Y) - F(X) star F(Y) in one refinement branch."""
    refined_product = refinement(product(x, y))
    product_refined = product(refinement(x), refinement(y))
    return abs(refined_product - product_refined)



def transport_product_residual(
    transport: RelationTransport,
    source_product: RelationalProductRule,
    target_product: RelationalProductRule,
    x: TensorScalarElement,
    y: TensorScalarElement,
) -> float:
    """Measure T_r(X star Y) - (T_r X) star' (T_r Y)."""
    direct = transport(source_product(x, y))
    transported_product = target_product(transport(x), transport(y))
    return abs(direct - transported_product)


def semantic_product_residual(
    scale_map: SemanticScaleMap,
    source_product: RelationalProductRule,
    target_product: RelationalProductRule,
    x: TensorScalarElement,
    y: TensorScalarElement,
) -> float:
    """Measure S(X star Y) - S(X) star' S(Y)."""
    direct = scale_map(source_product(x, y))
    scaled_product = target_product(scale_map(x), scale_map(y))
    return abs(direct - scaled_product)


def orbital_product_residual(
    orbital: OrbitalAction,
    source_product: RelationalProductRule,
    target_product: RelationalProductRule,
    x: TensorScalarElement,
    y: TensorScalarElement,
) -> float:
    """Measure U(X star Y) - U(X) star' U(Y)."""
    direct = orbital.act(source_product(x, y))
    orbital_product = target_product(orbital.act(x), orbital.act(y))
    return abs(direct - orbital_product)


def refinement_transport_residual(
    parent_transport: RelationTransport,
    child_transport: RelationTransport,
    source_refinement: BranchRefinementMap,
    target_refinement: BranchRefinementMap,
    element: TensorScalarElement,
) -> float:
    """Measure failure of the refinement/transport naturality square.

    Compares F_target(T_parent X) with T_child(F_source X).
    """
    via_parent_then_refine = target_refinement(parent_transport(element))
    via_refine_then_child = child_transport(source_refinement(element))
    return abs(via_parent_then_refine - via_refine_then_child)



def tensor_map_residual(
    mapping: ElementMap,
    source_tensor_product: BinaryElementMap,
    target_tensor_product: BinaryElementMap,
    x: TensorScalarElement,
    y: TensorScalarElement,
) -> float:
    """Measure Phi(X tensor Y) - Phi(X) tensor' Phi(Y).

    The supplied mapping may be a transport, semantic scale map, refinement
    map, orbital map adapter, or another typed unary morphism.
    """
    direct = mapping(source_tensor_product(x, y))
    mapped_tensor = target_tensor_product(mapping(x), mapping(y))
    return abs(direct - mapped_tensor)


def contraction_map_residual(
    high_rank_map: ElementMap,
    low_rank_map: ElementMap,
    source_contraction: ContractionRule,
    target_contraction: ContractionRule,
    element: TensorScalarElement,
) -> float:
    """Measure naturality of contraction under a supplied typed map.

    Compares C_target(Phi_high X) with Phi_low(C_source X).
    """
    map_then_contract = target_contraction(high_rank_map(element))
    contract_then_map = low_rank_map(source_contraction(element))
    return abs(map_then_contract - contract_then_map)
