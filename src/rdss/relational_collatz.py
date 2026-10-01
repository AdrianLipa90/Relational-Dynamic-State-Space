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

def durable_role_count() -> int:
    """Cardinality of the persistent relation-role orbit."""

    return 2


def full_operator_basis() -> tuple[str, str, str, str]:
    """Canonical real basis of the durable two-role operator algebra."""

    return ("I", "S", "P", "J")


def active_operator_basis() -> tuple[str, str, str]:
    """Non-identity sector of the canonical operator basis."""

    return tuple(label for label in full_operator_basis() if label != "I")


def operator_algebra_real_dimension(role_count: int = 2) -> int:
    """Real dimension of End(R^q)=M_q(R)."""

    q = _positive_integer(role_count, "role_count")
    return q * q


def nonidentity_operator_dimension(role_count: int = 2) -> int:
    """Operator-algebra dimension after removing the identity line."""

    q = _positive_integer(role_count, "role_count")
    return operator_algebra_real_dimension(q) - 1


def universal_constant_repair(role_count: int = 2) -> int:
    """Minimal residue-independent repair after multiplier q^2-1.

    A single constant repair mapping every nonzero residue class mod q into
    the divisible class exists only for q=2. In that binary case the minimal
    positive repair is 1.
    """

    q = _positive_integer(role_count, "role_count")
    if q < 2:
        raise ValueError("role_count must be at least two")
    multiplier = q * q - 1
    repairs = [
        repair
        for repair in range(1, q + 1)
        if all(
            (multiplier * residue + repair) % q == 0
            for residue in range(1, q)
        )
    ]
    if not repairs:
        raise ValueError("no residue-independent universal repair exists")
    return min(repairs)


def active_seed_from_relation_algebra() -> int:
    """Canonical active seed: cardinality of the non-identity operator sector."""

    return len(active_operator_basis())


def relational_collatz_depth_to_one(seed: int, *, max_steps: int = 10_000) -> int:
    """Exact finite depth for seeds that reach one within max_steps.

    No global Collatz-convergence claim is made.
    """

    n = _positive_integer(seed, "seed")
    if max_steps < 0:
        raise ValueError("max_steps must be non-negative")
    for depth in range(max_steps + 1):
        if n == 1:
            return depth
        if depth == max_steps:
            break
        n = relational_collatz_step(n)
    raise RuntimeError("seed did not reach one within max_steps")


def relational_l_constant_certificate() -> dict[str, int | bool]:
    """Exact relational Collatz derivation with Gaussian crosscheck.

    Primary values:
      L4 = durable role count,
      L5 = first completed D/R/A cycle from the active seed,
      L3 = exact finite depth of the same seed to one.

    The Gaussian/root-extension result is used only as an independent
    crosscheck of the same triple.
    """

    from .gaussian_bombelli import l_constants_from_gaussian_and_root_extension

    seed = active_seed_from_relation_algebra()
    first = relational_collatz_step(seed)
    second = relational_collatz_step(first)

    l4 = durable_role_count()
    l5 = second
    l3 = relational_collatz_depth_to_one(seed)
    gaussian_l3, gaussian_l4, gaussian_l5 = l_constants_from_gaussian_and_root_extension()

    return {
        "role_count": l4,
        "operator_dimension": operator_algebra_real_dimension(),
        "nonidentity_dimension": nonidentity_operator_dimension(),
        "active_basis_size": len(active_operator_basis()),
        "universal_repair": universal_constant_repair(),
        "association_divisor": l4,
        "dissociation_multiplier": nonidentity_operator_dimension(),
        "active_seed": seed,
        "seed_step_1": first,
        "seed_step_2": second,
        "depth_to_one": l3,
        "L3": l3,
        "L4": l4,
        "L5": l5,
        "seed_matches_multiplier": seed == nonidentity_operator_dimension(),
        "first_full_cycle_reaches_L5": second == l5,
        "depth_matches_L3": relational_collatz_depth_to_one(seed) == l3,
        "root_extension_matches": l3 == l4 + l5,
        "gaussian_triple_matches": (l3, l4, l5) == (gaussian_l3, gaussian_l4, gaussian_l5),
    }

