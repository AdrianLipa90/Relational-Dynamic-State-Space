import pytest

from rdss import RelationalPoint, SemanticScale, TensorScalarElement, TypedRelation
from rdss.operations import (
    ContractionRule,
    OrbitalAction,
    RelationTransport,
    RelationalProductRule,
    reference_tensor_product,
    relative_moire_action,
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
