from math import exp

import pytest

from rdss import (
    ArithmeticRelation,
    DynamicState,
    LinearRelationalAttachment,
    SemanticMetric,
    TimeAlgebraOperator,
    evolve_until_page_attractor,
)


def test_arithmetic_truth_is_not_changed_by_semantic_geometry():
    relation = ArithmeticRelation(2, "+", 2)
    attachment = LinearRelationalAttachment({"relation_strength": 0.25})
    metric = SemanticMetric(((1.0, 0.0), (0.0, 1.0)))

    chi = attachment({"relation_strength": 1.0})
    deformed = metric.deform(chi)

    assert relation.evaluate() == 4
    assert deformed[0][0] == pytest.approx(exp(0.5))
    assert deformed != metric.base_metric


def test_zero_semantic_attachment_leaves_metric_unchanged():
    metric = SemanticMetric(((2.0, 0.0), (0.0, 3.0)))
    attachment = LinearRelationalAttachment({"relation_strength": 0.0})

    chi = attachment({"relation_strength": 99.0})

    assert chi == 0.0
    assert metric.deform(chi) == metric.base_metric


def test_time_operator_and_semantic_deformation_are_separate_channels():
    state = DynamicState((1.0, 0.0), ((1.0, 0.0), (0.0, 1.0)))
    op = TimeAlgebraOperator("swap", ((0.0, 1.0), (1.0, 0.0)))
    attachment = LinearRelationalAttachment({"semantic_load": 0.1})
    metric = SemanticMetric(((1.0, 0.0), (0.0, 1.0)))

    nxt = state.step(
        operator=op,
        attachment=attachment,
        semantic_features={"semantic_load": 2.0},
        semantic_metric=metric,
    )

    assert nxt.vector == (0.0, 1.0)
    assert nxt.metric[0][0] == pytest.approx(exp(0.4))
    assert nxt.step_index == 1


def test_fixed_point_page_attractor():
    initial = DynamicState((1.0, 0.0), ((1.0, 0.0), (0.0, 1.0)))

    def update(state: DynamicState) -> DynamicState:
        return DynamicState(state.vector, state.metric, state.step_index + 1)

    result = evolve_until_page_attractor(initial, update)

    assert result.converged
    assert result.iterations == 1
    assert result.state_delta == 0.0
    assert result.metric_delta == 0.0


def test_fail_closed_on_non_finite_semantics():
    attachment = LinearRelationalAttachment({"x": 1.0})
    with pytest.raises(ValueError):
        attachment({"x": float("nan")})
