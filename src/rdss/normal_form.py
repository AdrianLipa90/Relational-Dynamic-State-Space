from __future__ import annotations

from dataclasses import dataclass

from .canonical import strict_normal_form
from .confluence import (
    certified_irreducible_result,
    rdss_forgetful_confluence_certificate,
)
from .rewrite import (
    rdss_forgetful_rewrite_system,
    rdss_forgetful_termination_certificate,
)


@dataclass(frozen=True)
class ScopedRewriteNormalForm:
    """Unique irreducible result under one explicitly named rewrite system."""

    scope: str
    source_key: object
    target_key: object
    value: object
    rule_names: tuple[str, ...]
    lossy: bool
    termination_certificate: str
    confluence_certificate: str
    claim_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.scope.strip():
            raise ValueError(
                "normal-form scope must be non-empty"
            )
        if any(not claim.strip() for claim in self.claim_ids):
            raise ValueError(
                "normal-form claim ids must be non-empty"
            )

    @property
    def rewritten(self) -> bool:
        return bool(self.rule_names)

    @property
    def global_canonical(self) -> bool:
        return False


def rdss_forgetful_normal_form(
    value: object,
) -> ScopedRewriteNormalForm:
    """Return the certified normal form under the reference forgetful system.

    This function is intentionally scoped. It does not claim a global RDSS
    canonical representative.
    """
    system = rdss_forgetful_rewrite_system()
    termination = rdss_forgetful_termination_certificate()
    confluence = rdss_forgetful_confluence_certificate()

    result = certified_irreducible_result(
        system,
        value,
        termination=termination,
        confluence=confluence,
    )

    return ScopedRewriteNormalForm(
        scope="rdss-reference-forgetful-v1",
        source_key=strict_normal_form(value).key,
        target_key=strict_normal_form(result.value).key,
        value=result.value,
        rule_names=result.rule_names,
        lossy=result.lossy,
        termination_certificate=(
            result.termination_certificate
        ),
        confluence_certificate=(
            result.confluence_certificate
        ),
        claim_ids=(
            "REF_FORGETFUL_SCOPED_NORMAL_FORM",
            "THM_REFERENCE_FORGETFUL_UNIQUE_IRREDUCIBLE",
        ),
    )
