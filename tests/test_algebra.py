import pytest

from rdss.algebra import (
    RelationalPoint,
    SemanticScale,
    SemanticScaleGraph,
    TensorScalarElement,
    TypedZero,
    associator,
    commutator,
    refinement_residual,
)


def test_minimal_point_refines_recursively_without_physical_scale():
    root = RelationalPoint()
    minus, plus = root.refine()
    mm, mp = minus.refine()

    assert root.level == 0
    assert minus.address == (-1,)
    assert plus.address == (1,)
    assert mm.address == (-1, -1)
    assert mp.address == (-1, 1)


def test_scalar_sector_is_tensor_rank_zero():
    scalar = TensorScalarElement(
        components=(3.0,),
        rank=(0, 0),
        carrier=RelationalPoint(),
        scale=SemanticScale("object"),
    )
    assert scalar.is_scalar


def test_typed_zero_is_exact_additive_sector_not_empty_relation():
    carrier = RelationalPoint((-1, 1))
    scale = SemanticScale("object")
    zero = TypedZero(
        rank=(1, 1),
        carrier=carrier,
        scale=scale,
        dimension=3,
    )

    assert zero.rank == (1, 1)
    assert zero.carrier == carrier
    assert zero.scale == scale
    assert zero.dimension == 3
    assert zero.level == 2
    assert zero.as_element().components == (0j, 0j, 0j)


def test_typed_zero_distinguishes_carriers_at_same_refinement_level():
    scale = SemanticScale("object")
    left = TypedZero(
        rank=(0, 0),
        carrier=RelationalPoint((-1,)),
        scale=scale,
        dimension=1,
    )
    right = TypedZero(
        rank=(0, 0),
        carrier=RelationalPoint((1,)),
        scale=scale,
        dimension=1,
    )

    assert left.level == right.level == 1
    assert left != right


def test_typed_zero_from_element_materializes_additive_identity():
    p = RelationalPoint((1, -1))
    scale = SemanticScale("object")
    x = TensorScalarElement((2.0, -3.0), (1, 0), p, scale)

    zero = TypedZero.from_element(x)
    z = zero.as_element()

    assert zero.carrier == p
    assert zero.dimension == len(x.components)
    assert x + z == x
    assert x - x == z


def test_semantic_scale_is_partial_order_like_coarse_graining():
    graph = SemanticScaleGraph(
        edges=(
            ("granny-smith", "apple"),
            ("apple", "fruit"),
            ("fruit", "food"),
            ("vegetable", "food"),
            ("food", "object"),
        )
    )

    assert graph.can_coarsen("granny-smith", "fruit")
    assert graph.common_scale(("fruit", "vegetable")) == "food"


def test_commutator_and_associator_are_diagnostics_not_axioms():
    product = lambda x, y: x * y

    assert commutator(product, 2.0, 3.0) == pytest.approx(0.0)
    assert associator(product, 2.0, 3.0, 4.0) == pytest.approx(0.0)


def test_refinement_residual_detects_exact_and_broken_self_similarity():
    product = lambda x, y: x + y
    exact_refine = lambda x: 2.0 * x
    broken_refine = lambda x: x * x

    assert refinement_residual(exact_refine, product, 2.0, 3.0) == pytest.approx(0.0)
    assert refinement_residual(broken_refine, product, 2.0, 3.0) > 0.0


def test_tensor_scalar_reference_sector_has_additive_module_operations():
    p = RelationalPoint()
    scale = SemanticScale("object")
    a = TensorScalarElement((1.0, 2.0), (1, 0), p, scale)
    b = TensorScalarElement((3.0, -1.0), (1, 0), p, scale)

    assert (a + b).components == (4.0 + 0j, 1.0 + 0j)
    assert (a - b).components == (-2.0 + 0j, 3.0 + 0j)
    assert a.scale_by(2.0).components == (2.0 + 0j, 4.0 + 0j)


def test_addition_fails_closed_across_typed_sectors():
    p = RelationalPoint()
    a = TensorScalarElement((1.0,), (0, 0), p, SemanticScale("fruit"))
    b = TensorScalarElement((1.0,), (0, 0), p, SemanticScale("vegetable"))

    with pytest.raises(ValueError):
        _ = a + b


def test_zero_like_is_additive_identity_in_typed_sector():
    p = RelationalPoint()
    scale = SemanticScale("object")
    x = TensorScalarElement((2.0, -3.0), (1, 0), p, scale)
    zero = x.zero_like()

    assert zero.components == (0j, 0j)
    assert (x + zero) == x
    assert (x - x) == zero


def test_refinement_residual_operates_on_tensor_scalar_elements():
    p = RelationalPoint()
    scale = SemanticScale("object")
    x = TensorScalarElement((2.0,), (0, 0), p, scale)
    y = TensorScalarElement((3.0,), (0, 0), p, scale)

    def product(a, b):
        return a + b

    def exact_refine(a):
        return a.scale_by(2.0)

    assert refinement_residual(exact_refine, product, x, y) == pytest.approx(0.0)



def test_relational_point_finite_word_action_is_monoid_action():
    p = RelationalPoint((-1,))
    u = (1, -1)
    v = (-1, 1, 1)

    assert p.advance(()) == p
    assert p.advance(u).advance(v) == p.advance(u + v)


def test_relational_point_generators_match_binary_refinement():
    p = RelationalPoint((1,))
    left, right = p.refine()

    assert left == p.advance((-1,))
    assert right == p.advance((1,))


def test_relational_point_advance_fails_closed_on_invalid_word():
    with pytest.raises(ValueError):
        RelationalPoint().advance((0,))
