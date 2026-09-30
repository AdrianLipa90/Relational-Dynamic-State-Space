from __future__ import annotations

from dataclasses import dataclass

from .canonical import strict_normal_form
from .confluence import (
    rdss_forgetful_confluence_certificate,
)
from .normal_form import (
    ScopedRewriteNormalForm,
    rdss_forgetful_normal_form,
)
from .provenance import (
    ClaimDependencyGraph,
    TransformationClaimProvenance,
    ValueClaimProvenance,
    build_claim_dependency_graph,
    provenance_for_normal_form,
    provenance_for_rewrite_trace,
    provenance_for_value,
)
from .rewrite import (
    RewriteTrace,
    rdss_forgetful_rewrite_system,
    rdss_forgetful_termination_certificate,
)


class ReductionCertificateError(RuntimeError):
    pass


@dataclass(frozen=True)
class ReductionCertificate:
    """Auditable object-level certificate for one scoped rewrite reduction."""

    scope: str
    source: ValueClaimProvenance
    target: ValueClaimProvenance
    rewrite_trace: RewriteTrace
    rewrite_provenance: TransformationClaimProvenance
    normal_form: ScopedRewriteNormalForm
    normal_form_provenance: TransformationClaimProvenance
    verified_invariants: tuple[str, ...]
    root_claim_ids: tuple[str, ...]
    claim_graph: ClaimDependencyGraph
    claim_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.scope.strip():
            raise ValueError(
                "reduction certificate scope must be non-empty"
            )
        if any(not item.strip() for item in self.root_claim_ids):
            raise ValueError(
                "reduction certificate root claim IDs must be non-empty"
            )
        if any(not item.strip() for item in self.claim_ids):
            raise ValueError(
                "reduction certificate claim IDs must be non-empty"
            )

    @property
    def rewritten(self) -> bool:
        return bool(self.rewrite_trace.steps)

    @property
    def lossy(self) -> bool:
        return self.rewrite_trace.lossy

    @property
    def source_family(self) -> str:
        return self.source.factorization.family

    @property
    def target_family(self) -> str:
        return self.target.factorization.family

    @property
    def global_canonical(self) -> bool:
        return False

    @property
    def verified(self) -> bool:
        try:
            validate_reduction_certificate(self)
        except ReductionCertificateError:
            return False
        return True


def _unique(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(items))


def validate_reduction_certificate(
    certificate: ReductionCertificate,
) -> None:
    system = rdss_forgetful_rewrite_system()

    if certificate.scope != certificate.normal_form.scope:
        raise ReductionCertificateError(
            "certificate scope disagrees with normal-form scope"
        )

    if certificate.global_canonical:
        raise ReductionCertificateError(
            "scoped reduction certificate cannot be global canonical"
        )

    source_key = strict_normal_form(
        certificate.rewrite_trace.initial
    ).key
    target_key = strict_normal_form(
        certificate.rewrite_trace.value
    ).key

    if certificate.normal_form.source_key != source_key:
        raise ReductionCertificateError(
            "normal-form source key disagrees with rewrite trace"
        )
    if certificate.normal_form.target_key != target_key:
        raise ReductionCertificateError(
            "normal-form target key disagrees with rewrite trace"
        )
    if strict_normal_form(
        certificate.normal_form.value
    ).key != target_key:
        raise ReductionCertificateError(
            "normal-form value disagrees with rewrite trace target"
        )

    expected_source = provenance_for_value(
        certificate.rewrite_trace.initial
    )
    expected_target = provenance_for_value(
        certificate.rewrite_trace.value
    )
    if certificate.source.factorization != expected_source.factorization:
        raise ReductionCertificateError(
            "source factorization disagrees with rewrite input"
        )
    if certificate.target.factorization != expected_target.factorization:
        raise ReductionCertificateError(
            "target factorization disagrees with rewrite target"
        )

    if (
        certificate.normal_form.rule_names
        != certificate.rewrite_trace.rule_names
    ):
        raise ReductionCertificateError(
            "normal-form rule provenance disagrees with rewrite trace"
        )

    if certificate.normal_form.lossy != certificate.rewrite_trace.lossy:
        raise ReductionCertificateError(
            "normal-form lossiness disagrees with rewrite trace"
        )

    if not system.irreducible(certificate.rewrite_trace.value):
        raise ReductionCertificateError(
            "certificate target is not irreducible"
        )

    repeat = rdss_forgetful_normal_form(
        certificate.rewrite_trace.value
    )
    if repeat.rule_names:
        raise ReductionCertificateError(
            "certificate target is not idempotent under scoped normal form"
        )
    if repeat.target_key != certificate.normal_form.target_key:
        raise ReductionCertificateError(
            "idempotent target key disagrees with certificate target key"
        )

    expected_invariants = _unique(
        tuple(
            name
            for step in certificate.rewrite_trace.steps
            for name in step.verified_invariants
        )
    )
    if certificate.verified_invariants != expected_invariants:
        raise ReductionCertificateError(
            "verified invariant inventory disagrees with rewrite trace"
        )

    if certificate.claim_graph.roots != certificate.root_claim_ids:
        raise ReductionCertificateError(
            "claim graph roots disagree with certificate roots"
        )


def certify_forgetful_reduction(
    value: object,
) -> ReductionCertificate:
    system = rdss_forgetful_rewrite_system()
    termination = rdss_forgetful_termination_certificate()
    confluence = rdss_forgetful_confluence_certificate()

    termination.require_valid(system)
    confluence.require_valid(system)

    source = provenance_for_value(value)
    trace = system.trace_certified(
        value,
        termination,
    )
    normal_form = rdss_forgetful_normal_form(value)

    if trace.rule_names != normal_form.rule_names:
        raise ReductionCertificateError(
            "trace and scoped normal form disagree"
        )
    if trace.lossy != normal_form.lossy:
        raise ReductionCertificateError(
            "trace and scoped normal form lossiness disagree"
        )

    target = provenance_for_value(trace.value)
    rewrite_provenance = provenance_for_rewrite_trace(
        trace
    )
    normal_form_provenance = provenance_for_normal_form(
        normal_form
    )

    verified_invariants = _unique(
        tuple(
            name
            for step in trace.steps
            for name in step.verified_invariants
        )
    )

    roots = _unique(
        source.root_claim_ids
        + target.root_claim_ids
        + rewrite_provenance.root_claim_ids
        + normal_form_provenance.root_claim_ids
        + termination.claim_ids
        + confluence.claim_ids
        + (
            "REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE",
        )
    )

    certificate = ReductionCertificate(
        scope=normal_form.scope,
        source=source,
        target=target,
        rewrite_trace=trace,
        rewrite_provenance=rewrite_provenance,
        normal_form=normal_form,
        normal_form_provenance=normal_form_provenance,
        verified_invariants=verified_invariants,
        root_claim_ids=roots,
        claim_graph=build_claim_dependency_graph(roots),
        claim_ids=(
            "REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE",
            "THM_REFERENCE_OBJECT_REDUCTION_CERTIFICATE_CONSISTENT",
        ),
    )

    validate_reduction_certificate(certificate)
    return certificate
