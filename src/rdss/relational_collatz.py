from __future__ import annotations


def _positive_integer(value: int, name: str = "cardinality") -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def association_quotient_cardinality(cardinality: int) -> int:
    """Cardinality of a free two-role orbit quotient.

    A fixed-point-free involutive pairing partitions a finite carrier into
    two-element orbits, so the quotient cardinality is n/2. Odd cardinality
    fails closed because a complete free pairing is impossible.
    """

    n = _positive_integer(cardinality)
    if n % 2:
        raise ValueError("association requires even cardinality")
    return n // 2


def dissociation_fibre_cardinality(cardinality: int, multiplicity: int = 3) -> int:
    """Cardinality of X x F_d for a finite dissociation fibre F_d."""

    n = _positive_integer(cardinality)
    d = _positive_integer(multiplicity, "multiplicity")
    if d <= 1:
        raise ValueError("dissociation multiplicity must exceed one")
    return n * d


def singleton_repair_cardinality(cardinality: int) -> int:
    """Cardinality after adjoining one missing singleton by disjoint union."""

    n = _positive_integer(cardinality)
    return n + 1


def relational_collatz_step(cardinality: int) -> int:
    """Deterministic cardinality normalization from association/dissociation.

    Even n: quotient by the free durable-role Z2 pairing -> n/2.
    Odd n: three-fibre dissociation followed by singleton repair -> 3n+1.
    """

    n = _positive_integer(cardinality)
    if n % 2 == 0:
        return association_quotient_cardinality(n)
    return singleton_repair_cardinality(dissociation_fibre_cardinality(n, 3))


def standard_collatz_step(cardinality: int) -> int:
    """Reference formula used only for exact equivalence testing."""

    n = _positive_integer(cardinality)
    return n // 2 if n % 2 == 0 else 3 * n + 1


def relational_collatz_equivalence(limit: int) -> bool:
    """Check exact equality with the standard formula on 1..limit."""

    m = _positive_integer(limit, "limit")
    return all(relational_collatz_step(n) == standard_collatz_step(n) for n in range(1, m + 1))


def odd_branch_reopens_association(cardinality: int) -> bool:
    """Odd branch 3n+1 is always even, so the next association quotient exists."""

    n = _positive_integer(cardinality)
    if n % 2 == 0:
        raise ValueError("odd-branch check requires odd cardinality")
    repaired = relational_collatz_step(n)
    return repaired % 2 == 0 and association_quotient_cardinality(repaired) >= 1
