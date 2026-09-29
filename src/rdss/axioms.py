from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ClaimKind(str, Enum):
    AXIOM = "axiom"
    DEFINITION = "definition"
    STRUCTURAL_PRIMITIVE = "structural_primitive"
    REFERENCE_REALIZATION = "reference_realization"
    DERIVED = "derived"
    BRIDGE = "bridge"


@dataclass(frozen=True)
class Claim:
    id: str
    kind: ClaimKind
    statement: str
    depends_on: tuple[str, ...] = ()


CLAIMS: tuple[Claim, ...] = (
    Claim(
        "RA0",
        ClaimKind.AXIOM,
        "Relational admissibility: an admitted observable is not independent of relation.",
    ),
    Claim(
        "DEF_POINT",
        ClaimKind.DEFINITION,
        "The minimal algebraic carrier is an unscaled point.",
    ),
    Claim(
        "DEF_BINARY_REL",
        ClaimKind.DEFINITION,
        "A primitive typed relation is binary: r:a->b. Higher arity is constructed separately.",
    ),
    Claim(
        "RR1",
        ClaimKind.AXIOM,
        "Recursive relational closure: a selected relational endpoint may itself carry a further distinction.",
        ("DEF_POINT", "DEF_BINARY_REL"),
    ),
    Claim(
        "REF_CP1",
        ClaimKind.REFERENCE_REALIZATION,
        "A minimal complex binary distinction may be represented by CP^1 with Fubini-Study metric.",
        ("DEF_POINT", "DEF_BINARY_REL"),
    ),
    Claim(
        "DEF_TS",
        ClaimKind.DEFINITION,
        "Tensor-scalar grading uses A^(p,q) with scalars in rank (0,0).",
    ),
    Claim(
        "PRIM_PRODUCT",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "A typed relational product star_R may be supplied without assuming associativity or commutativity.",
    ),
    Claim(
        "PRIM_SCALE",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Semantic scale is a typed partial-order/category-like structure, not necessarily a real scalar.",
    ),
    Claim(
        "PRIM_ORBIT",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Admissible orbital actions U_g may act on algebra elements.",
    ),
    Claim(
        "DER_MOIRE",
        ClaimKind.DERIVED,
        "Moiré is the relative orbital action M_ij = U_i U_j^{-1} when the inverse exists.",
        ("PRIM_ORBIT",),
    ),
    Claim(
        "DEF_REFINEMENT_RESIDUAL",
        ClaimKind.DEFINITION,
        "Delta_F measures failure of exact product preservation under refinement.",
        ("RR1", "PRIM_PRODUCT"),
    ),
    Claim(
        "ZA_BRIDGE",
        ClaimKind.BRIDGE,
        "The companion Zero Axis model supplies Omega(s)=s/(1-s) and the critical-axis unit-circle equivalence.",
    ),
    Claim(
        "DER_WINDING",
        ClaimKind.DERIVED,
        "Topological winding is derived only for a closed phase path with a continuous phase lift.",
        ("ZA_BRIDGE",),
    ),
)


def claim_map() -> dict[str, Claim]:
    return {claim.id: claim for claim in CLAIMS}


def dependency_closure(claim_id: str) -> frozenset[str]:
    claims = claim_map()
    if claim_id not in claims:
        raise KeyError(claim_id)

    seen: set[str] = set()
    stack = list(claims[claim_id].depends_on)
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        if current not in claims:
            raise KeyError(f"unknown dependency: {current}")
        seen.add(current)
        stack.extend(claims[current].depends_on)
    return frozenset(seen)


def validate_dependency_dag() -> None:
    claims = claim_map()
    if len(claims) != len(CLAIMS):
        raise ValueError("claim ids must be unique")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise ValueError(f"dependency cycle at {node}")
        if node in visited:
            return
        visiting.add(node)
        for dep in claims[node].depends_on:
            if dep not in claims:
                raise ValueError(f"unknown dependency {dep!r} in {node}")
            visit(dep)
        visiting.remove(node)
        visited.add(node)

    for node in claims:
        visit(node)


def foundational_axioms() -> tuple[Claim, ...]:
    return tuple(claim for claim in CLAIMS if claim.kind is ClaimKind.AXIOM)
