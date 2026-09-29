from math import sqrt

import pytest

from rdss.algebra import SemanticScale
from rdss.potential import (
    RelationalPotentialProfile,
    relational_attractor_set,
    semantic_potential_shift,
)


def test_relational_potential_is_weighted_p_functional():
    profile = RelationalPotentialProfile(
        SemanticScale("object"),
        (("semantic_orbit", 1.0), ("transport_product", 1.0)),
        p=2.0,
    )

    value = profile.evaluate(
        {"semantic_orbit": 3.0, "transport_product": 4.0}
    )

    assert value == pytest.approx(5.0)


def test_semantic_profile_changes_scalar_with_fixed_residual_signature():
    residuals = {"fruit_relation": 3.0, "shape_relation": 4.0}
    source = RelationalPotentialProfile(
        SemanticScale("object"),
        (("fruit_relation", 1.0), ("shape_relation", 1.0)),
        p=1.0,
    )
    target = RelationalPotentialProfile(
        SemanticScale("food-context"),
        (("fruit_relation", 2.0), ("shape_relation", 1.0)),
        p=1.0,
    )

    assert source.evaluate(residuals) == pytest.approx(7.0)
    assert target.evaluate(residuals) == pytest.approx(10.0)
    assert semantic_potential_shift(residuals, source, target) == pytest.approx(3.0)


def test_zero_residual_signature_has_zero_potential():
    profile = RelationalPotentialProfile(
        SemanticScale("object"),
        (("a", 2.0), ("b", 5.0)),
    )

    assert profile.evaluate({"a": 0.0, "b": 0.0}) == pytest.approx(0.0)


def test_potential_fails_closed_on_signature_mismatch():
    profile = RelationalPotentialProfile(
        SemanticScale("object"),
        (("a", 1.0), ("b", 1.0)),
    )

    with pytest.raises(ValueError):
        profile.evaluate({"a": 1.0})


def test_potential_rejects_negative_residuals_and_weights():
    with pytest.raises(ValueError):
        RelationalPotentialProfile(
            SemanticScale("object"),
            (("a", -1.0),),
        )

    profile = RelationalPotentialProfile(
        SemanticScale("object"),
        (("a", 1.0),),
    )
    with pytest.raises(ValueError):
        profile.evaluate({"a": -0.1})


def test_potential_requires_valid_order_and_positive_weight():
    with pytest.raises(ValueError):
        RelationalPotentialProfile(
            SemanticScale("object"),
            (("a", 1.0),),
            p=0.5,
        )

    with pytest.raises(ValueError):
        RelationalPotentialProfile(
            SemanticScale("object"),
            (("a", 0.0),),
        )


def test_relational_attractor_set_selects_minimum_without_arbitrary_tie_break():
    assert relational_attractor_set(
        {"minus": 2.0, "plus": 1.0}
    ) == ("plus",)

    assert relational_attractor_set(
        {"minus": 1.0, "plus": 1.0}
    ) == ("minus", "plus")


def test_semantic_shift_requires_same_residual_signature():
    residuals = {"a": 1.0, "b": 2.0}
    source = RelationalPotentialProfile(
        SemanticScale("source"),
        (("a", 1.0), ("b", 1.0)),
    )
    target = RelationalPotentialProfile(
        SemanticScale("target"),
        (("a", 1.0), ("c", 1.0)),
    )

    with pytest.raises(ValueError):
        semantic_potential_shift(residuals, source, target)
