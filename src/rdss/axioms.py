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
    CANDIDATE_AXIOM = "candidate_axiom"
    THEOREM = "theorem"


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
        "RA0_STAR",
        ClaimKind.CANDIDATE_AXIOM,
        "Every admitted carrier hosts an admitted non-degenerate binary distinction whose endpoint occurrences are admitted carriers.",
        ("DEF_POINT", "DEF_BINARY_REL"),
    ),
    Claim(
        "THM_RR1_FROM_RA0_STAR",
        ClaimKind.THEOREM,
        "RA0* generates recursive binary refinement to arbitrary finite depth by induction on path-labelled occurrences.",
        ("RA0_STAR",),
    ),
    Claim(
        "PRIM_MODULE",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Each typed tensor-scalar sector carries an additive K-module structure; the reference kernel uses complex components.",
    ),
    Claim(
        "DEF_TS",
        ClaimKind.DEFINITION,
        "Tensor-scalar grading uses A^(p,q) with scalars in rank (0,0).",
        ("PRIM_MODULE",),
    ),
    Claim(
        "PRIM_PRODUCT",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "A typed relational product star_R may be supplied without assuming associativity or commutativity.",
    ),
    Claim(
        "PRIM_TENSOR_PRODUCT",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "A typed tensor product may combine compatible tensor-scalar sectors; concrete component formulas belong to realizations.",
        ("PRIM_MODULE",),
    ),
    Claim(
        "PRIM_CONTRACTION",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Typed contraction lowers one covariant and one contravariant rank when a contraction rule is supplied.",
        ("PRIM_MODULE",),
    ),
    Claim(
        "DEF_BILINEARITY_RESIDUAL",
        ClaimKind.DEFINITION,
        "Bilinearity residuals measure failure of additivity and scalar-linearity of the relational product.",
        ("PRIM_PRODUCT", "PRIM_MODULE"),
    ),
    Claim(
        "PRIM_SCALE",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Semantic scale is a typed partial-order/category-like structure, not necessarily a real scalar.",
    ),
    Claim(
        "PRIM_TRANSPORT",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Typed relation transports T_r may act between carrier sectors along composable relations.",
        ("DEF_BINARY_REL", "PRIM_MODULE"),
    ),
    Claim(
        "DER_HOLONOMY",
        ClaimKind.DERIVED,
        "Relational holonomy is transport around a closed composable relation path, measured against the starting state.",
        ("PRIM_TRANSPORT",),
    ),
    Claim(
        "DEF_TRANSPORT_RESIDUAL",
        ClaimKind.DEFINITION,
        "Transport composition residual measures failure of direct transport to equal sequential transport.",
        ("PRIM_TRANSPORT",),
    ),
    Claim(
        "DEF_TRANSPORT_PRODUCT_COHERENCE",
        ClaimKind.DEFINITION,
        "Transport-product residual measures failure of T_r(X star Y) = T_r(X) star' T_r(Y).",
        ("PRIM_TRANSPORT", "PRIM_PRODUCT", "PRIM_MODULE"),
    ),
    Claim(
        "PRIM_ORBIT",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Admissible orbital actions U_g may act on algebra elements.",
    ),
    Claim(
        "DEF_SCALE_ORBIT_RESIDUAL",
        ClaimKind.DEFINITION,
        "The semantic-scale/orbital commutator residual measures order dependence of coarse-graining and orbital action.",
        ("PRIM_SCALE", "PRIM_ORBIT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_SCALE_PRODUCT_COHERENCE",
        ClaimKind.DEFINITION,
        "Semantic-product residual measures failure of S(X star Y) = S(X) star' S(Y).",
        ("PRIM_SCALE", "PRIM_PRODUCT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_ORBITAL_COHERENCE",
        ClaimKind.DEFINITION,
        "Orbital identity, inverse and composition residuals diagnose exact action-law coherence.",
        ("PRIM_ORBIT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_ORBIT_PRODUCT_COHERENCE",
        ClaimKind.DEFINITION,
        "Orbital-product residual measures failure of U(X star Y) = U(X) star' U(Y).",
        ("PRIM_ORBIT", "PRIM_PRODUCT", "PRIM_MODULE"),
    ),
    Claim(
        "DER_MOIRE",
        ClaimKind.DERIVED,
        "Moiré is the relative orbital action M_ij = U_i U_j^{-1} when the inverse exists.",
        ("PRIM_ORBIT",),
    ),
    Claim(
        "PRIM_REFINEMENT_MAP",
        ClaimKind.STRUCTURAL_PRIMITIVE,
        "Typed branch refinement maps F_-/F_+ send level n sectors to selected child sectors at level n+1.",
        ("RR1", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_REFINEMENT_RESIDUAL",
        ClaimKind.DEFINITION,
        "Delta_F measures failure of exact product preservation under refinement.",
        ("PRIM_REFINEMENT_MAP", "PRIM_PRODUCT", "PRIM_MODULE"),
    ),
    Claim(
        "DEF_REFINEMENT_TRANSPORT_COHERENCE",
        ClaimKind.DEFINITION,
        "Refinement-transport residual measures failure of the naturality square between parent transport and child transport.",
        ("PRIM_REFINEMENT_MAP", "PRIM_TRANSPORT", "PRIM_MODULE"),
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
        ("ZA_BRIDGE", "DER_HOLONOMY"),
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
