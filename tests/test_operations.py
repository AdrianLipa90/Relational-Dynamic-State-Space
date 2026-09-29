import pytest

from rdss import RelationalPoint, SemanticScale, SemanticScaleGraph, TensorScalarElement, TypedRelation
from rdss.operations import (
    BranchRefinementMap,
    ContractionRule,
    OrbitalAction,
    RelationPath,
    RelationTransport,
    RelationalProductRule,
    SemanticScaleMap,
    TensorBraidingRule,
    TensorProductRule,
    TransportPath,
    orbital_composition_residual,
    orbital_identity_residual,
    orbital_inverse_residual,
    orbital_product_residual,
    product_bilinearity_residuals,
    reference_tensor_product,
    relative_moire_action,
    semantic_orbital_commutator_residual,
    semantic_product_residual,
    tensor_map_residual,
    contraction_map_residual,
    transport_composition_residual,
    transport_product_residual,
    typed_refinement_residual,
    refinement_transport_residual,
    semantic_transport_residual,
    orbital_transport_residual,
    refinement_semantic_residual,
    refinement_orbital_residual,
    reference_tensor_flip,
    tensor_associator_residual,
    tensor_unit_residual,
    tensor_braiding_residual,
)


def elem(value, *, rank=(0, 0), carrier=None, scale=None):
    return TensorScalarElement(
        components=(complex(value),),
        rank=rank,
        carrier=carrier or RelationalPoint(),
        scale=scale or SemanticScale("object"),
    )


def test_reference_tensor_product_adds_ranks_and_multiplies_components():
    p = RelationalPoint()
    s = SemanticScale("object")
    a = TensorScalarElement((2.0, 3.0), (1, 0), p, s)
    b = TensorScalarElement((5.0,), (0, 1), p, s)

    out = reference_tensor_product(a, b)

    assert out.rank == (1, 1)
    assert out.components == (10.0 + 0j, 15.0 + 0j)


def test_reference_tensor_product_fails_closed_across_semantic_scales():
    p = RelationalPoint()
    a = elem(2.0, carrier=p, scale=SemanticScale("fruit"))
    b = elem(3.0, carrier=p, scale=SemanticScale("vegetable"))

    with pytest.raises(ValueError):
        reference_tensor_product(a, b)


def test_typed_relation_transport_checks_source_and_target():
    source = RelationalPoint((-1,))
    target = RelationalPoint((1,))
    relation = TypedRelation(source, target, "r")

    def move(x):
        return TensorScalarElement(x.components, x.rank, target, x.scale)

    transport = RelationTransport(relation, move)
    x = elem(1.0, carrier=source)

    assert transport(x).carrier == target

    with pytest.raises(ValueError):
        transport(elem(1.0, carrier=target))


def test_contraction_rule_checks_rank_reduction_without_inventing_formula():
    p = RelationalPoint()
    s = SemanticScale("object")
    x = TensorScalarElement((7.0,), (1, 1), p, s)

    rule = ContractionRule(
        "trace-like",
        lambda z: TensorScalarElement(z.components, (0, 0), z.carrier, z.scale),
    )

    assert rule(x).rank == (0, 0)


def test_orbital_relative_action_requires_explicit_inverse():
    p = RelationalPoint()
    s = SemanticScale("object")
    x = elem(1.0, carrier=p, scale=s)

    def scale_by(k):
        def op(z):
            return TensorScalarElement(
                tuple(k * c for c in z.components),
                z.rank,
                z.carrier,
                z.scale,
            )
        return op

    ui = OrbitalAction("Ui", scale_by(3.0), scale_by(1 / 3))
    uj = OrbitalAction("Uj", scale_by(2.0), scale_by(1 / 2))

    out = relative_moire_action(ui, uj, x)

    assert out.components == pytest.approx((1.5 + 0j,))


def test_relational_product_rule_has_no_hidden_associativity_requirement():
    product = RelationalProductRule(
        "left-biased",
        lambda a, b: TensorScalarElement(
            (a.components[0] + 2 * b.components[0],),
            a.rank,
            a.carrier,
            a.scale,
        ),
    )

    a, b, c = elem(1), elem(2), elem(3)
    left = product(product(a, b), c)
    right = product(a, product(b, c))

    assert left.components != right.components



def test_closed_relational_path_has_abstract_holonomy_residual():
    a = RelationalPoint((-1,))
    b = RelationalPoint((1,))
    scale = SemanticScale("object")
    x = elem(1.0, carrier=a, scale=scale)

    rab = TypedRelation(a, b, "ab")
    rba = TypedRelation(b, a, "ba")

    def move_to(target, factor):
        def mapping(z):
            return TensorScalarElement(
                tuple(factor * c for c in z.components),
                z.rank,
                target,
                z.scale,
            )
        return mapping

    path = TransportPath(
        (
            RelationTransport(rab, move_to(b, 1j)),
            RelationTransport(rba, move_to(a, 1j)),
        )
    )

    assert path.relation_path.closed
    assert path.apply(x).components == (-1.0 + 0j,)
    assert path.holonomy_residual(x) == pytest.approx(2.0)


def test_trivial_closed_transport_has_zero_holonomy_residual():
    a = RelationalPoint((-1,))
    b = RelationalPoint((1,))
    x = elem(2.0, carrier=a)

    rab = TypedRelation(a, b, "ab")
    rba = TypedRelation(b, a, "ba")

    def relocate(target):
        return lambda z: TensorScalarElement(z.components, z.rank, target, z.scale)

    path = TransportPath(
        (
            RelationTransport(rab, relocate(b)),
            RelationTransport(rba, relocate(a)),
        )
    )

    assert path.holonomy_residual(x) == pytest.approx(0.0)


def test_open_relation_path_rejects_holonomy_claim():
    a = RelationalPoint((-1,))
    b = RelationalPoint((1,))
    rab = TypedRelation(a, b, "ab")
    path = TransportPath(
        (
            RelationTransport(
                rab,
                lambda z: TensorScalarElement(z.components, z.rank, b, z.scale),
            ),
        )
    )

    assert not path.relation_path.closed
    with pytest.raises(ValueError):
        path.holonomy_residual(elem(1.0, carrier=a))


def test_transport_composition_residual_measures_functoriality_defect():
    a = RelationalPoint((-1,))
    b = RelationalPoint((1,))
    c = RelationalPoint((-1, -1))
    scale = SemanticScale("object")
    x = elem(1.0, carrier=a, scale=scale)

    rab = TypedRelation(a, b, "ab")
    rbc = TypedRelation(b, c, "bc")
    rac = TypedRelation(a, c, "ac")

    def move(target, factor):
        return lambda z: TensorScalarElement(
            tuple(factor * v for v in z.components),
            z.rank,
            target,
            z.scale,
        )

    first = RelationTransport(rab, move(b, 2.0))
    second = RelationTransport(rbc, move(c, 3.0))
    direct_exact = RelationTransport(rac, move(c, 6.0))
    direct_defect = RelationTransport(rac, move(c, 5.0))

    assert transport_composition_residual(
        direct_exact, first, second, x
    ) == pytest.approx(0.0)
    assert transport_composition_residual(
        direct_defect, first, second, x
    ) == pytest.approx(1.0)



def test_exact_bilinear_product_has_zero_residuals():
    p = RelationalPoint()
    scale = SemanticScale("object")

    def scalar_product(a, b):
        return TensorScalarElement(
            (a.components[0] * b.components[0],),
            a.rank,
            a.carrier,
            a.scale,
        )

    product = RelationalProductRule("bilinear", scalar_product)
    x = elem(2.0, carrier=p, scale=scale)
    y = elem(3.0, carrier=p, scale=scale)
    z = elem(5.0, carrier=p, scale=scale)

    residuals = product_bilinearity_residuals(product, x, y, z, 7.0)
    assert all(value == pytest.approx(0.0) for value in residuals.values())


def test_nonlinear_product_exposes_bilinearity_defect():
    p = RelationalPoint()
    scale = SemanticScale("object")

    product = RelationalProductRule(
        "nonlinear",
        lambda a, b: TensorScalarElement(
            (a.components[0] ** 2 + b.components[0],),
            a.rank,
            a.carrier,
            a.scale,
        ),
    )
    x = elem(2.0, carrier=p, scale=scale)
    y = elem(3.0, carrier=p, scale=scale)
    z = elem(5.0, carrier=p, scale=scale)

    residuals = product_bilinearity_residuals(product, x, y, z, 2.0)
    assert any(value > 0.0 for value in residuals.values())


def test_orbital_inverse_residual_checks_supplied_inverse():
    x = elem(1.0)

    def scale_by(k):
        return lambda z: TensorScalarElement(
            tuple(k * c for c in z.components),
            z.rank,
            z.carrier,
            z.scale,
        )

    exact = OrbitalAction("U2", scale_by(2.0), scale_by(0.5))
    broken = OrbitalAction("U2-bad", scale_by(2.0), scale_by(1.0 / 3.0))

    assert orbital_inverse_residual(exact, x) == pytest.approx(0.0)
    assert orbital_inverse_residual(broken, x) > 0.0


def test_orbital_composition_residual_checks_action_law_on_sample():
    x = elem(1.0)

    def scale_action(name, factor):
        return OrbitalAction(
            name,
            lambda z: TensorScalarElement(
                tuple(factor * c for c in z.components),
                z.rank,
                z.carrier,
                z.scale,
            ),
        )

    u2 = scale_action("U2", 2.0)
    u3 = scale_action("U3", 3.0)
    u6 = scale_action("U6", 6.0)
    u5 = scale_action("U5", 5.0)

    assert orbital_composition_residual(u6, u2, u3, x) == pytest.approx(0.0)
    assert orbital_composition_residual(u5, u2, u3, x) == pytest.approx(1.0)



def test_orbital_identity_residual_checks_identity_representative():
    x = elem(1.0)

    identity = OrbitalAction("Ue", lambda z: z)
    not_identity = OrbitalAction(
        "bad-Ue",
        lambda z: TensorScalarElement(
            tuple(2.0 * c for c in z.components),
            z.rank,
            z.carrier,
            z.scale,
        ),
    )

    assert orbital_identity_residual(identity, x) == pytest.approx(0.0)
    assert orbital_identity_residual(not_identity, x) == pytest.approx(1.0)



def test_semantic_scale_map_is_executable_coarse_graining():
    graph = SemanticScaleGraph((("apple", "fruit"), ("fruit", "food")))
    source = SemanticScale("apple")
    target = SemanticScale("food")
    x = elem(2.0, scale=source)

    scale_map = SemanticScaleMap(
        graph,
        source,
        target,
        lambda z: TensorScalarElement(
            z.components,
            z.rank,
            z.carrier,
            target,
        ),
    )

    out = scale_map(x)
    assert out.scale == target
    assert out.components == x.components


def test_semantic_scale_map_rejects_unavailable_coarse_graining():
    graph = SemanticScaleGraph((("apple", "fruit"),))
    with pytest.raises(ValueError):
        SemanticScaleMap(
            graph,
            SemanticScale("fruit"),
            SemanticScale("apple"),
            lambda z: z,
        )


def test_semantic_orbital_commutator_detects_order_dependence():
    graph = SemanticScaleGraph((("apple", "fruit"),))
    source = SemanticScale("apple")
    target = SemanticScale("fruit")
    x = elem(2.0, scale=source)

    orbital = OrbitalAction(
        "double",
        lambda z: TensorScalarElement(
            tuple(2.0 * c for c in z.components),
            z.rank,
            z.carrier,
            z.scale,
        ),
    )

    pure_relabel = SemanticScaleMap(
        graph,
        source,
        target,
        lambda z: TensorScalarElement(z.components, z.rank, z.carrier, target),
    )
    shifted = SemanticScaleMap(
        graph,
        source,
        target,
        lambda z: TensorScalarElement(
            tuple(c + 1.0 for c in z.components),
            z.rank,
            z.carrier,
            target,
        ),
    )

    assert semantic_orbital_commutator_residual(
        pure_relabel, orbital, x
    ) == pytest.approx(0.0)
    assert semantic_orbital_commutator_residual(
        shifted, orbital, x
    ) == pytest.approx(1.0)



def test_typed_branch_refinement_advances_exactly_one_level():
    root = RelationalPoint()
    scale = SemanticScale("object")
    x = elem(2.0, carrier=root, scale=scale)

    refine_plus = BranchRefinementMap(
        1,
        scale,
        lambda z: TensorScalarElement(
            z.components,
            z.rank,
            RelationalPoint(z.carrier.address + (1,)),
            scale,
        ),
    )

    out = refine_plus(x)
    assert out.carrier.address == (1,)
    assert out.carrier.level == x.carrier.level + 1
    assert out.rank == x.rank


def test_typed_refinement_residual_detects_exact_and_broken_branch_maps():
    root = RelationalPoint()
    scale = SemanticScale("object")
    x = elem(2.0, carrier=root, scale=scale)
    y = elem(3.0, carrier=root, scale=scale)

    product = RelationalProductRule(
        "add",
        lambda a, b: a + b,
    )

    exact = BranchRefinementMap(
        -1,
        scale,
        lambda z: TensorScalarElement(
            tuple(2.0 * c for c in z.components),
            z.rank,
            RelationalPoint(z.carrier.address + (-1,)),
            scale,
        ),
    )
    broken = BranchRefinementMap(
        -1,
        scale,
        lambda z: TensorScalarElement(
            tuple(c * c for c in z.components),
            z.rank,
            RelationalPoint(z.carrier.address + (-1,)),
            scale,
        ),
    )

    assert typed_refinement_residual(exact, product, x, y) == pytest.approx(0.0)
    assert typed_refinement_residual(broken, product, x, y) > 0.0


def test_refinement_map_rejects_wrong_child_carrier():
    root = RelationalPoint()
    scale = SemanticScale("object")
    x = elem(1.0, carrier=root, scale=scale)

    bad = BranchRefinementMap(
        1,
        scale,
        lambda z: TensorScalarElement(
            z.components,
            z.rank,
            RelationalPoint(z.carrier.address + (-1,)),
            scale,
        ),
    )

    with pytest.raises(ValueError):
        bad(x)



def test_transport_product_residual_detects_multiplicativity_defect():
    a = RelationalPoint((-1,))
    b = RelationalPoint((1,))
    scale = SemanticScale("object")
    x = elem(2.0, carrier=a, scale=scale)
    y = elem(3.0, carrier=a, scale=scale)
    relation = TypedRelation(a, b, "ab")

    product = RelationalProductRule(
        "mul",
        lambda u, v: TensorScalarElement(
            (u.components[0] * v.components[0],),
            u.rank,
            u.carrier,
            u.scale,
        ),
    )

    exact_transport = RelationTransport(
        relation,
        lambda z: TensorScalarElement(
            z.components,
            z.rank,
            b,
            z.scale,
        ),
    )
    scaled_transport = RelationTransport(
        relation,
        lambda z: TensorScalarElement(
            tuple(2.0 * c for c in z.components),
            z.rank,
            b,
            z.scale,
        ),
    )

    assert transport_product_residual(
        exact_transport, product, product, x, y
    ) == pytest.approx(0.0)
    assert transport_product_residual(
        scaled_transport, product, product, x, y
    ) > 0.0


def test_semantic_product_residual_detects_context_product_defect():
    graph = SemanticScaleGraph((("apple", "fruit"),))
    source = SemanticScale("apple")
    target = SemanticScale("fruit")
    x = elem(2.0, scale=source)
    y = elem(3.0, scale=source)

    product = RelationalProductRule(
        "add",
        lambda u, v: u + v,
    )

    exact_scale = SemanticScaleMap(
        graph,
        source,
        target,
        lambda z: TensorScalarElement(
            z.components, z.rank, z.carrier, target
        ),
    )
    shifted_scale = SemanticScaleMap(
        graph,
        source,
        target,
        lambda z: TensorScalarElement(
            tuple(c + 1.0 for c in z.components),
            z.rank,
            z.carrier,
            target,
        ),
    )

    assert semantic_product_residual(
        exact_scale, product, product, x, y
    ) == pytest.approx(0.0)
    assert semantic_product_residual(
        shifted_scale, product, product, x, y
    ) > 0.0


def test_orbital_product_residual_detects_nonautomorphic_action():
    x = elem(2.0)
    y = elem(3.0)
    product = RelationalProductRule(
        "mul",
        lambda u, v: TensorScalarElement(
            (u.components[0] * v.components[0],),
            u.rank,
            u.carrier,
            u.scale,
        ),
    )

    identity = OrbitalAction("id", lambda z: z)
    doubling = OrbitalAction(
        "double",
        lambda z: TensorScalarElement(
            tuple(2.0 * c for c in z.components),
            z.rank,
            z.carrier,
            z.scale,
        ),
    )

    assert orbital_product_residual(
        identity, product, product, x, y
    ) == pytest.approx(0.0)
    assert orbital_product_residual(
        doubling, product, product, x, y
    ) > 0.0


def test_refinement_transport_residual_checks_naturality_square():
    a = RelationalPoint((-1,))
    b = RelationalPoint((1,))
    scale = SemanticScale("object")
    x = elem(2.0, carrier=a, scale=scale)

    parent = TypedRelation(a, b, "ab")
    a_child = RelationalPoint(a.address + (1,))
    b_child = RelationalPoint(b.address + (1,))
    child = TypedRelation(a_child, b_child, "ab+")

    parent_transport = RelationTransport(
        parent,
        lambda z: TensorScalarElement(
            z.components, z.rank, b, z.scale
        ),
    )
    child_transport = RelationTransport(
        child,
        lambda z: TensorScalarElement(
            z.components, z.rank, b_child, z.scale
        ),
    )

    source_refine = BranchRefinementMap(
        1,
        scale,
        lambda z: TensorScalarElement(
            z.components,
            z.rank,
            RelationalPoint(z.carrier.address + (1,)),
            scale,
        ),
    )
    target_refine = BranchRefinementMap(
        1,
        scale,
        lambda z: TensorScalarElement(
            z.components,
            z.rank,
            RelationalPoint(z.carrier.address + (1,)),
            scale,
        ),
    )

    assert refinement_transport_residual(
        parent_transport,
        child_transport,
        source_refine,
        target_refine,
        x,
    ) == pytest.approx(0.0)

    broken_child_transport = RelationTransport(
        child,
        lambda z: TensorScalarElement(
            tuple(2.0 * c for c in z.components),
            z.rank,
            b_child,
            z.scale,
        ),
    )
    assert refinement_transport_residual(
        parent_transport,
        broken_child_transport,
        source_refine,
        target_refine,
        x,
    ) > 0.0



def test_tensor_map_residual_checks_monoidality():
    p = RelationalPoint()
    scale = SemanticScale("object")
    x = elem(2.0, carrier=p, scale=scale)
    y = elem(3.0, carrier=p, scale=scale)

    identity = lambda z: z
    doubling = lambda z: TensorScalarElement(
        tuple(2.0 * c for c in z.components),
        z.rank,
        z.carrier,
        z.scale,
    )

    assert tensor_map_residual(
        identity,
        reference_tensor_product,
        reference_tensor_product,
        x,
        y,
    ) == pytest.approx(0.0)

    assert tensor_map_residual(
        doubling,
        reference_tensor_product,
        reference_tensor_product,
        x,
        y,
    ) > 0.0


def test_contraction_map_residual_checks_naturality():
    p = RelationalPoint()
    scale = SemanticScale("object")
    x = TensorScalarElement((5.0,), (1, 1), p, scale)

    contraction = ContractionRule(
        "drop-one-pair",
        lambda z: TensorScalarElement(
            z.components,
            (z.rank[0] - 1, z.rank[1] - 1),
            z.carrier,
            z.scale,
        ),
    )

    identity = lambda z: z
    scale2 = lambda z: TensorScalarElement(
        tuple(2.0 * c for c in z.components),
        z.rank,
        z.carrier,
        z.scale,
    )
    scale3 = lambda z: TensorScalarElement(
        tuple(3.0 * c for c in z.components),
        z.rank,
        z.carrier,
        z.scale,
    )

    assert contraction_map_residual(
        identity,
        identity,
        contraction,
        contraction,
        x,
    ) == pytest.approx(0.0)

    assert contraction_map_residual(
        scale2,
        scale3,
        contraction,
        contraction,
        x,
    ) > 0.0



def test_semantic_transport_residual_checks_naturality():
    a = RelationalPoint((-1,))
    b = RelationalPoint((1,))
    apple = SemanticScale("apple")
    fruit = SemanticScale("fruit")
    graph = SemanticScaleGraph((("apple", "fruit"),))
    x = elem(2.0, carrier=a, scale=apple)
    relation = TypedRelation(a, b, "ab")

    source_transport = RelationTransport(
        relation,
        lambda z: TensorScalarElement(z.components, z.rank, b, apple),
    )
    target_transport = RelationTransport(
        relation,
        lambda z: TensorScalarElement(z.components, z.rank, b, fruit),
    )
    broken_target_transport = RelationTransport(
        relation,
        lambda z: TensorScalarElement(
            tuple(2.0 * c for c in z.components), z.rank, b, fruit
        ),
    )

    source_scale = SemanticScaleMap(
        graph,
        apple,
        fruit,
        lambda z: TensorScalarElement(z.components, z.rank, z.carrier, fruit),
    )
    target_scale = SemanticScaleMap(
        graph,
        apple,
        fruit,
        lambda z: TensorScalarElement(z.components, z.rank, z.carrier, fruit),
    )

    assert semantic_transport_residual(
        source_transport,
        target_transport,
        source_scale,
        target_scale,
        x,
    ) == pytest.approx(0.0)

    assert semantic_transport_residual(
        source_transport,
        broken_target_transport,
        source_scale,
        target_scale,
        x,
    ) > 0.0


def test_orbital_transport_residual_checks_equivariance():
    a = RelationalPoint((-1,))
    b = RelationalPoint((1,))
    x = elem(2.0, carrier=a)
    relation = TypedRelation(a, b, "ab")
    transport = RelationTransport(
        relation,
        lambda z: TensorScalarElement(z.components, z.rank, b, z.scale),
    )

    def scale_action(name, factor):
        return OrbitalAction(
            name,
            lambda z: TensorScalarElement(
                tuple(factor * c for c in z.components),
                z.rank,
                z.carrier,
                z.scale,
            ),
        )

    source_orbit = scale_action("Ua", 2.0)
    target_orbit = scale_action("Ub", 2.0)
    broken_target = scale_action("Ub-broken", 3.0)

    assert orbital_transport_residual(
        transport, source_orbit, target_orbit, x
    ) == pytest.approx(0.0)
    assert orbital_transport_residual(
        transport, source_orbit, broken_target, x
    ) > 0.0


def test_refinement_semantic_residual_checks_commuting_square():
    root = RelationalPoint()
    apple = SemanticScale("apple")
    fruit = SemanticScale("fruit")
    graph = SemanticScaleGraph((("apple", "fruit"),))
    x = elem(2.0, carrier=root, scale=apple)

    source_refine = BranchRefinementMap(
        1,
        apple,
        lambda z: TensorScalarElement(
            z.components,
            z.rank,
            RelationalPoint(z.carrier.address + (1,)),
            apple,
        ),
    )
    target_refine = BranchRefinementMap(
        1,
        fruit,
        lambda z: TensorScalarElement(
            z.components,
            z.rank,
            RelationalPoint(z.carrier.address + (1,)),
            fruit,
        ),
    )

    parent_scale = SemanticScaleMap(
        graph,
        apple,
        fruit,
        lambda z: TensorScalarElement(z.components, z.rank, z.carrier, fruit),
    )
    child_scale = SemanticScaleMap(
        graph,
        apple,
        fruit,
        lambda z: TensorScalarElement(z.components, z.rank, z.carrier, fruit),
    )
    broken_child_scale = SemanticScaleMap(
        graph,
        apple,
        fruit,
        lambda z: TensorScalarElement(
            tuple(c + 1.0 for c in z.components),
            z.rank,
            z.carrier,
            fruit,
        ),
    )

    assert refinement_semantic_residual(
        source_refine,
        target_refine,
        parent_scale,
        child_scale,
        x,
    ) == pytest.approx(0.0)
    assert refinement_semantic_residual(
        source_refine,
        target_refine,
        parent_scale,
        broken_child_scale,
        x,
    ) > 0.0


def test_refinement_orbital_residual_checks_equivariance():
    root = RelationalPoint()
    scale = SemanticScale("object")
    x = elem(2.0, carrier=root, scale=scale)

    refinement = BranchRefinementMap(
        -1,
        scale,
        lambda z: TensorScalarElement(
            z.components,
            z.rank,
            RelationalPoint(z.carrier.address + (-1,)),
            scale,
        ),
    )

    def scale_action(name, factor):
        return OrbitalAction(
            name,
            lambda z: TensorScalarElement(
                tuple(factor * c for c in z.components),
                z.rank,
                z.carrier,
                z.scale,
            ),
        )

    parent_orbit = scale_action("Up", 2.0)
    child_orbit = scale_action("Uc", 2.0)
    broken_child = scale_action("Uc-broken", 3.0)

    assert refinement_orbital_residual(
        refinement, parent_orbit, child_orbit, x
    ) == pytest.approx(0.0)
    assert refinement_orbital_residual(
        refinement, parent_orbit, broken_child, x
    ) > 0.0



def test_tensor_product_rule_is_general_but_rank_typed():
    p = RelationalPoint()
    scale = SemanticScale("object")
    left = TensorScalarElement((2.0,), (1, 0), p, scale)
    right = TensorScalarElement((3.0,), (0, 1), p, scale)

    rule = TensorProductRule(
        "reference-like",
        lambda a, b: TensorScalarElement(
            (a.components[0] * b.components[0],),
            (a.rank[0] + b.rank[0], a.rank[1] + b.rank[1]),
            a.carrier,
            a.scale,
        ),
    )

    out = rule(left, right)
    assert out.rank == (1, 1)
    assert out.components == (6.0 + 0j,)


def test_tensor_product_rule_rejects_wrong_rank():
    p = RelationalPoint()
    scale = SemanticScale("object")
    left = TensorScalarElement((2.0,), (1, 0), p, scale)
    right = TensorScalarElement((3.0,), (0, 1), p, scale)

    bad = TensorProductRule(
        "bad-rank",
        lambda a, b: TensorScalarElement(
            (a.components[0] * b.components[0],),
            (0, 0),
            a.carrier,
            a.scale,
        ),
    )

    with pytest.raises(ValueError):
        bad(left, right)



def test_reference_tensor_product_is_strictly_associative():
    p = RelationalPoint()
    scale = SemanticScale("object")
    x = TensorScalarElement((1.0, 2.0), (1, 0), p, scale)
    y = TensorScalarElement((3.0, 5.0), (0, 1), p, scale)
    z = TensorScalarElement((7.0,), (1, 1), p, scale)

    assert tensor_associator_residual(
        reference_tensor_product, x, y, z
    ) == pytest.approx(0.0)


def test_explicit_tensor_unit_is_checked_not_assumed():
    p = RelationalPoint()
    scale = SemanticScale("object")
    unit = TensorScalarElement((1.0,), (0, 0), p, scale)
    bad_unit = TensorScalarElement((2.0,), (0, 0), p, scale)
    x = TensorScalarElement((3.0, 5.0), (1, 0), p, scale)

    assert tensor_unit_residual(
        reference_tensor_product, unit, unit, x
    ) == pytest.approx(0.0)
    assert tensor_unit_residual(
        reference_tensor_product, bad_unit, unit, x
    ) > 0.0


def test_reference_tensor_flip_realizes_braiding():
    p = RelationalPoint()
    scale = SemanticScale("object")
    x = TensorScalarElement((1.0, 2.0), (1, 0), p, scale)
    y = TensorScalarElement((3.0, 5.0), (0, 1), p, scale)

    flip = TensorBraidingRule("flip", reference_tensor_flip)
    assert tensor_braiding_residual(
        reference_tensor_product, flip, x, y
    ) == pytest.approx(0.0)


def test_bad_braiding_has_nonzero_residual():
    p = RelationalPoint()
    scale = SemanticScale("object")
    x = TensorScalarElement((1.0, 2.0), (1, 0), p, scale)
    y = TensorScalarElement((3.0, 5.0), (0, 1), p, scale)

    bad = TensorBraidingRule(
        "identity-order",
        lambda a, b: reference_tensor_product(a, b),
    )

    assert tensor_braiding_residual(
        reference_tensor_product, bad, x, y
    ) > 0.0
