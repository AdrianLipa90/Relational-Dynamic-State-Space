from math import log

import pytest

from rdss.ofhm_prefix_completion import (
    common_prefix_length,
    countable_boundary_dimension_is_infinite,
    countable_prefix_completion_is_totally_bounded,
    finite_alphabet_boundary_dimension,
    prefix_chain_cauchy_bound,
    prefix_ultrametric,
    symbolic_completion_certificate,
    uniform_countable_branch_probability_exists,
)


def test_common_prefix_length() -> None:
    assert common_prefix_length((), ()) == 0
    assert common_prefix_length((1, 2), (1, 2)) == 2
    assert common_prefix_length((1, 2), (1, 3)) == 1
    assert common_prefix_length((1,), (1, 2, 3)) == 1
    assert common_prefix_length((-4, 7), (-4, 7, 9)) == 2


def test_prefix_ultrametric_basic_values() -> None:
    assert prefix_ultrametric((1, 2), (1, 2)) == 0.0
    assert prefix_ultrametric((1,), (2,)) == pytest.approx(1.0)
    assert prefix_ultrametric((1, 2), (1, 3)) == pytest.approx(0.5)
    assert prefix_ultrametric((1, 2), (1, 2, 9)) == pytest.approx(0.25)


def test_prefix_ultrametric_strong_triangle_inequality() -> None:
    words = (
        (),
        (0,),
        (1,),
        (0, 0),
        (0, 1),
        (0, 0, 4),
        (0, 0, 5),
        (-3, 2, 8),
    )
    for x in words:
        for y in words:
            for z in words:
                assert prefix_ultrametric(x, z) <= max(
                    prefix_ultrametric(x, y),
                    prefix_ultrametric(y, z),
                )


def test_infinite_branch_prefixes_have_cauchy_tail_bound() -> None:
    assert prefix_chain_cauchy_bound(0) == pytest.approx(1.0)
    assert prefix_chain_cauchy_bound(1) == pytest.approx(0.5)
    assert prefix_chain_cauchy_bound(10) == pytest.approx(2.0 ** -10)

    branch = tuple(range(20))
    for depth in range(1, 10):
        left = branch[:depth]
        right = branch[:18]
        assert prefix_ultrametric(left, right) <= prefix_chain_cauchy_bound(depth)


def test_countable_prefix_completion_is_not_totally_bounded() -> None:
    assert countable_prefix_completion_is_totally_bounded() is False
    # Distinct first-level branch labels are pairwise distance one.
    for left in range(-5, 6):
        for right in range(-5, 6):
            if left != right:
                assert prefix_ultrametric((left,), (right,)) == pytest.approx(1.0)


def test_finite_subshift_dimensions_are_unbounded() -> None:
    assert finite_alphabet_boundary_dimension(2) == pytest.approx(1.0)
    assert finite_alphabet_boundary_dimension(4) == pytest.approx(2.0)
    assert finite_alphabet_boundary_dimension(8) == pytest.approx(3.0)

    values = [finite_alphabet_boundary_dimension(m) for m in (2, 4, 16, 256)]
    assert values == sorted(values)
    assert values[-1] == pytest.approx(log(256.0) / log(2.0))
    assert countable_boundary_dimension_is_infinite() is True


def test_no_uniform_probability_on_countably_infinite_branch_alphabet() -> None:
    assert uniform_countable_branch_probability_exists() is False


def test_symbolic_completion_certificate() -> None:
    receipt = symbolic_completion_certificate()
    assert receipt["address_carrier"] == "Z^{<omega}"
    assert receipt["boundary"] == "Z^omega"
    assert receipt["prefix_metric_base"] == pytest.approx(2.0)
    assert receipt["totally_bounded"] is False
    assert receipt["compact"] is False
    assert receipt["hausdorff_dimension_infinite"] is True
    assert receipt["uniform_countable_branch_probability"] is False
    assert receipt["unique_continuum_probability_measure_forced"] is False
    assert receipt["euclidean_embedding_forced"] is False
