import pytest

from rdss import RelationalPoint, SemanticScale, TensorScalarElement, TypedRelation
from rdss.operations import (
    ContractionRule,
    OrbitalAction,
    RelationPath,
    RelationTransport,
    RelationalProductRule,
    TransportPath,
    orbital_composition_residual,
    orbital_identity_residual,
    orbital_inverse_residual,
    product_bilinearity_residuals,
    reference_tensor_product,
    relative_moire_action,
    transport_composition_residual,
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
