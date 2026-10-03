from __future__ import annotations

from math import log
from typing import Sequence


# REF: RDSS OFHM parent main @ 3fe6ed391d374a09c0b077b8bdedb3aabe16a28e
#       src/rdss/orbital_fractal_hilbert_moire.py
#       finite symbolic address carrier Z^{<omega}; rank is enumeration only.
# REF: Infinities @ 339d6c58f3e7d86c67a4f758cd7416692f8f8280
#       research/EULERS_INFINITY_V0_1.md
#       research/TIR_E6_FOURIER_HILBERT_HOTEL_CORE_V0_1.md
# REF: standard ultrametric completion of a countably branching rooted tree.
#       No Euclidean embedding or probability measure is imported.


def common_prefix_length(left: Sequence[int], right: Sequence[int]) -> int:
    """Length of the maximal common prefix of two finite integer words."""

    a = tuple(int(x) for x in left)
    b = tuple(int(x) for x in right)
    length = 0
    for x, y in zip(a, b):
        if x != y:
            break
        length += 1
    return length


def prefix_ultrametric(
    left: Sequence[int],
    right: Sequence[int],
    *,
    base: float = 2.0,
) -> float:
    """Canonical prefix ultrametric on finite words Z^{<omega}.

    d(a,b)=0 for a=b and base^{-LCP(a,b)} otherwise.

    If one word is a strict prefix of the other, LCP is the shorter length.
    The metric depends only on the prefix tree, not on the Hilbert-Hotel rank.
    """

    b = float(base)
    if b <= 1.0:
        raise ValueError("base must be greater than one")
    a_word = tuple(int(x) for x in left)
    b_word = tuple(int(x) for x in right)
    if a_word == b_word:
        return 0.0
    return b ** (-common_prefix_length(a_word, b_word))


def prefix_chain_cauchy_bound(depth: int, *, base: float = 2.0) -> float:
    """Uniform tail bound for prefixes of one infinite branch.

    Any two prefixes whose lengths are at least depth and that belong to the
    same infinite branch share at least depth symbols, hence their distance
    is at most base^{-depth}.
    """

    n = int(depth)
    b = float(base)
    if n < 0:
        raise ValueError("depth must be non-negative")
    if b <= 1.0:
        raise ValueError("base must be greater than one")
    return b ** (-n)


def finite_alphabet_boundary_dimension(
    alphabet_size: int,
    *,
    base: float = 2.0,
) -> float:
    """Hausdorff dimension of an m-symbol full-shift boundary.

    Under the prefix metric d=base^{-LCP}, the m-ary boundary is the
    self-similar full shift with m cylinders of ratio 1/base, so
    dim_H=log(m)/log(base).
    """

    m = int(alphabet_size)
    b = float(base)
    if m < 2:
        raise ValueError("alphabet_size must be at least two")
    if b <= 1.0:
        raise ValueError("base must be greater than one")
    return log(float(m)) / log(b)


def countable_boundary_dimension_is_infinite(*, base: float = 2.0) -> bool:
    """Exact conclusion for the countably branching prefix boundary.

    For every finite m>=2, the full countable boundary contains an isometric
    m-symbol full-shift sub-boundary with dimension log(m)/log(base).
    These lower bounds are unbounded as m grows, so the whole boundary has
    infinite Hausdorff dimension.
    """

    b = float(base)
    if b <= 1.0:
        raise ValueError("base must be greater than one")
    return True


def countable_prefix_completion_is_totally_bounded() -> bool:
    """False: first-level children form an infinite pairwise-distance-1 set."""

    return False


def uniform_countable_branch_probability_exists() -> bool:
    """False for a countably infinite alphabet.

    Full permutation invariance would assign one singleton mass p to every
    branch label. p=0 gives total mass zero; p>0 gives divergent total mass.
    Thus no uniform probability distribution exists on the branch alphabet.
    """

    return False


def symbolic_completion_certificate(*, base: float = 2.0) -> dict[str, object]:
    """Machine receipt for the canonical OFHM symbolic completion/no-go."""

    b = float(base)
    if b <= 1.0:
        raise ValueError("base must be greater than one")

    finite_lower_bounds = tuple(
        finite_alphabet_boundary_dimension(m, base=b)
        for m in (2, 3, 4, 8, 16, 32)
    )
    return {
        "address_carrier": "Z^{<omega}",
        "boundary": "Z^omega",
        "prefix_metric_base": b,
        "prefix_chain_tail_bound_depth_10": prefix_chain_cauchy_bound(10, base=b),
        "first_level_pair_distance": prefix_ultrametric((0,), (1,), base=b),
        "totally_bounded": countable_prefix_completion_is_totally_bounded(),
        "compact": False,
        "finite_alphabet_dimension_lower_bounds": finite_lower_bounds,
        "hausdorff_dimension_infinite": countable_boundary_dimension_is_infinite(base=b),
        "uniform_countable_branch_probability": uniform_countable_branch_probability_exists(),
        "unique_continuum_probability_measure_forced": False,
        "euclidean_embedding_forced": False,
    }
