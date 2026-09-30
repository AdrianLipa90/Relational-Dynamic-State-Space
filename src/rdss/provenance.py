from __future__ import annotations

from dataclasses import dataclass

from .axioms import (
    Claim,
    ClaimKind,
    claim_map,
)
from .bridges import BridgeRoute
from .factorization import (
    SemanticFactorization,
    factorize_value,
)
from .normal_form import ScopedRewriteNormalForm
from .rewrite import RewriteTrace
from .signature import (
    SignatureEngine,
    rdss_signature_engine,
)


@dataclass(frozen=True)
class ClaimDependencyEdge:
    claim_id: str
    depends_on: str


@dataclass(frozen=True)
class ClaimDependencyGraph:
    roots: tuple[str, ...]
    ordered_claim_ids: tuple[str, ...]
    claims: tuple[Claim, ...]
    edges: tuple[ClaimDependencyEdge, ...]

    @property
    def claim_count(self) -> int:
        return len(self.claims)

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    @property
    def kind_counts(self) -> dict[ClaimKind, int]:
        counts = {kind: 0 for kind in ClaimKind}
        for claim in self.claims:
            counts[claim.kind] += 1
        return counts

    @property
    def foundational_claim_ids(self) -> tuple[str, ...]:
        return tuple(
            claim.id
            for claim in self.claims
            if claim.kind
            in {
                ClaimKind.AXIOM,
                ClaimKind.FORMATION_RULE,
                ClaimKind.STRUCTURAL_PRIMITIVE,
            }
        )


@dataclass(frozen=True)
class ValueClaimProvenance:
    factorization: SemanticFactorization
    signature_provenance: tuple[str, ...]
    root_claim_ids: tuple[str, ...]
    graph: ClaimDependencyGraph


@dataclass(frozen=True)
class TransformationClaimProvenance:
    source: str
    root_claim_ids: tuple[str, ...]
    graph: ClaimDependencyGraph


def _unique(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(items))


def build_claim_dependency_graph(
    root_claim_ids: tuple[str, ...],
) -> ClaimDependencyGraph:
    roots = _unique(root_claim_ids)
    claims = claim_map()

    for root in roots:
        if root not in claims:
            raise KeyError(f"unknown root claim: {root}")

    ordered: list[str] = []
    permanent: set[str] = set()
    temporary: set[str] = set()

    def visit(claim_id: str) -> None:
        if claim_id in permanent:
            return
        if claim_id in temporary:
            raise ValueError(
                f"dependency cycle at {claim_id}"
            )
        if claim_id not in claims:
            raise KeyError(
                f"unknown dependency claim: {claim_id}"
            )

        temporary.add(claim_id)
        for dependency in claims[claim_id].depends_on:
            visit(dependency)
        temporary.remove(claim_id)
        permanent.add(claim_id)
        ordered.append(claim_id)

    for root in roots:
        visit(root)

    selected = set(ordered)
    edges = tuple(
        ClaimDependencyEdge(
            claim_id=claim_id,
            depends_on=dependency,
        )
        for claim_id in ordered
        for dependency in claims[claim_id].depends_on
        if dependency in selected
    )

    return ClaimDependencyGraph(
        roots=roots,
        ordered_claim_ids=tuple(ordered),
        claims=tuple(claims[item] for item in ordered),
        edges=edges,
    )


def provenance_for_value(
    value: object,
    *,
    signature_engine: SignatureEngine | None = None,
) -> ValueClaimProvenance:
    engine = signature_engine or rdss_signature_engine()
    signature = engine.signature(value)
    factorization = factorize_value(
        value,
        signature_engine=engine,
    )
    roots = _unique(signature.claim_ids)

    return ValueClaimProvenance(
        factorization=factorization,
        signature_provenance=signature.provenance,
        root_claim_ids=roots,
        graph=build_claim_dependency_graph(roots),
    )


def provenance_for_bridge_route(
    route: BridgeRoute,
) -> TransformationClaimProvenance:
    roots = _unique(
        tuple(
            claim_id
            for step in route.steps
            for claim_id in step.claim_ids
        )
    )
    return TransformationClaimProvenance(
        source="bridge_route",
        root_claim_ids=roots,
        graph=build_claim_dependency_graph(roots),
    )


def provenance_for_rewrite_trace(
    trace: RewriteTrace,
) -> TransformationClaimProvenance:
    roots = _unique(
        tuple(
            claim_id
            for step in trace.steps
            for claim_id in step.claim_ids
        )
    )
    return TransformationClaimProvenance(
        source="rewrite_trace",
        root_claim_ids=roots,
        graph=build_claim_dependency_graph(roots),
    )


def provenance_for_normal_form(
    result: ScopedRewriteNormalForm,
) -> TransformationClaimProvenance:
    roots = _unique(result.claim_ids)
    return TransformationClaimProvenance(
        source="scoped_normal_form",
        root_claim_ids=roots,
        graph=build_claim_dependency_graph(roots),
    )
