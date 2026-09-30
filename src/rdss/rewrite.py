from __future__ import annotations

from dataclasses import dataclass

from .bridges import (
    BridgeDirection,
    BridgeInvariant,
    BridgeSpec,
    rdss_bridge_specs,
)
from .canonical import (
    EquivalenceKind,
    InformationEffect,
    strict_normal_form,
)
from .signature import (
    SignatureEngine,
    rdss_signature_engine,
)


class RewriteError(RuntimeError):
    pass


class RewriteRuleError(RewriteError):
    pass


class NoRewriteRuleError(RewriteError):
    pass


class AmbiguousRewriteError(RewriteError):
    pass


class RewriteTypeError(RewriteError):
    pass


class RewriteInvariantError(RewriteError):
    pass


class RewriteCycleError(RewriteError):
    pass


class RewriteStepLimitError(RewriteError):
    pass


class RewriteTerminationCertificateError(RewriteError):
    pass


@dataclass(frozen=True)
class RewriteRule:
    """One explicit oriented rewrite rule.

    Orientation is part of the rule. No canonical representative or global
    priority is implied by registration.
    """

    name: str
    source_family: str
    target_family: str
    transform: object
    source_check: object
    target_check: object
    kind: EquivalenceKind
    information_effect: InformationEffect
    invariants: tuple[BridgeInvariant, ...] = ()
    claim_ids: tuple[str, ...] = ()
    source_bridge_name: str | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("rewrite rule name must be non-empty")
        if not self.source_family.strip():
            raise ValueError(
                "rewrite source family must be non-empty"
            )
        if not self.target_family.strip():
            raise ValueError(
                "rewrite target family must be non-empty"
            )
        if self.source_bridge_name is not None:
            if not self.source_bridge_name.strip():
                raise ValueError(
                    "source bridge name must be non-empty"
                )
        invariant_names = [
            invariant.name for invariant in self.invariants
        ]
        if len(invariant_names) != len(set(invariant_names)):
            raise ValueError(
                "rewrite invariant names must be unique"
            )
        if any(not claim.strip() for claim in self.claim_ids):
            raise ValueError(
                "rewrite claim ids must be non-empty"
            )

    @classmethod
    def from_bridge_spec(
        cls,
        spec: BridgeSpec,
    ) -> "RewriteRule":
        return cls(
            name=f"rewrite:{spec.name}",
            source_family=spec.source_family,
            target_family=spec.target_family,
            transform=spec.forward,
            source_check=spec.source_check,
            target_check=spec.target_check,
            kind=spec.kind,
            information_effect=spec.information_effect,
            invariants=spec.invariants,
            claim_ids=spec.claim_ids,
            source_bridge_name=spec.name,
        )


@dataclass(frozen=True)
class FamilyRankViolation:
    rule_name: str
    source_family: str
    target_family: str
    source_rank: int
    target_rank: int


@dataclass(frozen=True)
class RewriteTerminationAudit:
    certificate_name: str
    checked_rules: tuple[str, ...]
    violations: tuple[FamilyRankViolation, ...]

    @property
    def verified(self) -> bool:
        return not self.violations


@dataclass(frozen=True)
class FamilyRankTerminationCertificate:
    """Natural-number ranking certificate over semantic families."""

    name: str
    ranks: tuple[tuple[str, int], ...]
    default_rank: int = 0
    claim_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError(
                "termination certificate name must be non-empty"
            )
        families = [family for family, _ in self.ranks]
        if any(not family.strip() for family in families):
            raise ValueError(
                "termination certificate families must be non-empty"
            )
        if len(families) != len(set(families)):
            raise ValueError(
                "termination certificate families must be unique"
            )
        if self.default_rank < 0:
            raise ValueError(
                "termination default rank must be non-negative"
            )
        if any(rank < 0 for _, rank in self.ranks):
            raise ValueError(
                "termination ranks must be non-negative"
            )
        if any(not claim.strip() for claim in self.claim_ids):
            raise ValueError(
                "termination certificate claim ids must be non-empty"
            )

    @property
    def rank_map(self) -> dict[str, int]:
        return dict(self.ranks)

    def rank(self, family: str) -> int:
        return self.rank_map.get(
            family,
            self.default_rank,
        )

    def audit(
        self,
        system: "RewriteSystem",
    ) -> RewriteTerminationAudit:
        violations: list[FamilyRankViolation] = []
        checked: list[str] = []

        for rule in system.rules:
            checked.append(rule.name)
            source_rank = self.rank(rule.source_family)
            target_rank = self.rank(rule.target_family)
            if source_rank <= target_rank:
                violations.append(
                    FamilyRankViolation(
                        rule_name=rule.name,
                        source_family=rule.source_family,
                        target_family=rule.target_family,
                        source_rank=source_rank,
                        target_rank=target_rank,
                    )
                )

        return RewriteTerminationAudit(
            certificate_name=self.name,
            checked_rules=tuple(checked),
            violations=tuple(violations),
        )

    def require_valid(
        self,
        system: "RewriteSystem",
    ) -> RewriteTerminationAudit:
        audit = self.audit(system)
        if not audit.verified:
            details = ", ".join(
                (
                    f"{item.rule_name}:"
                    f"{item.source_rank}<={item.target_rank}"
                )
                for item in audit.violations
            )
            raise RewriteTerminationCertificateError(
                "termination certificate failed: "
                + details
            )
        return audit


@dataclass(frozen=True)
class RewriteStep:
    rule_name: str
    source_family: str
    target_family: str
    source_key: object
    target_key: object
    kind: EquivalenceKind
    information_effect: InformationEffect
    verified_invariants: tuple[str, ...]
    claim_ids: tuple[str, ...]
    source_bridge_name: str | None = None

    @property
    def lossy(self) -> bool:
        return self.information_effect is InformationEffect.LOSSY


@dataclass(frozen=True)
class RewriteTrace:
    initial: object
    value: object
    steps: tuple[RewriteStep, ...]

    @property
    def lossy(self) -> bool:
        return any(step.lossy for step in self.steps)

    @property
    def rule_names(self) -> tuple[str, ...]:
        return tuple(step.rule_name for step in self.steps)


class RewriteSystem:
    """Priority-free finite rewrite system.

    Automatic stepping is allowed only when exactly one rule applies.
    Multiple applicable rules fail closed as ambiguity.
    """

    def __init__(
        self,
        rules: tuple[RewriteRule, ...],
        *,
        signature_engine: SignatureEngine | None = None,
    ) -> None:
        names = [rule.name for rule in rules]
        if len(names) != len(set(names)):
            raise ValueError("rewrite rule names must be unique")
        self._rules = tuple(rules)
        self._signature_engine = (
            signature_engine or rdss_signature_engine()
        )

    @property
    def rules(self) -> tuple[RewriteRule, ...]:
        return self._rules

    @property
    def signature_engine(self) -> SignatureEngine:
        return self._signature_engine

    def applicable_rules(
        self,
        value: object,
    ) -> tuple[RewriteRule, ...]:
        signature = self._signature_engine.signature(value)
        return tuple(
            rule
            for rule in self._rules
            if rule.source_family == signature.family
            and bool(rule.source_check(value))
        )

    def irreducible(self, value: object) -> bool:
        return not self.applicable_rules(value)

    def apply(
        self,
        value: object,
        rule_name: str,
    ) -> tuple[object, RewriteStep]:
        candidates = tuple(
            rule
            for rule in self.applicable_rules(value)
            if rule.name == rule_name
        )
        if not candidates:
            raise NoRewriteRuleError(
                f"rewrite rule {rule_name!r} does not apply"
            )
        if len(candidates) > 1:
            raise AmbiguousRewriteError(
                f"multiple rules named {rule_name!r} apply"
            )

        rule = candidates[0]
        source_signature = self._signature_engine.signature(value)
        target = rule.transform(value)

        if not bool(rule.target_check(target)):
            raise RewriteTypeError(
                f"rewrite rule {rule.name!r} produced invalid target"
            )
        target_signature = self._signature_engine.signature(target)
        if target_signature.family != rule.target_family:
            raise RewriteTypeError(
                f"rewrite rule {rule.name!r} promised "
                f"{rule.target_family!r}, got "
                f"{target_signature.family!r}"
            )

        verified: list[str] = []
        for invariant in rule.invariants:
            if not invariant.verify(
                value,
                target,
                direction=BridgeDirection.FORWARD,
            ):
                raise RewriteInvariantError(
                    f"rewrite rule {rule.name!r} failed invariant "
                    f"{invariant.name!r}"
                )
            verified.append(invariant.name)

        step = RewriteStep(
            rule_name=rule.name,
            source_family=source_signature.family,
            target_family=target_signature.family,
            source_key=strict_normal_form(value).key,
            target_key=strict_normal_form(target).key,
            kind=rule.kind,
            information_effect=rule.information_effect,
            verified_invariants=tuple(verified),
            claim_ids=rule.claim_ids,
            source_bridge_name=rule.source_bridge_name,
        )
        return target, step

    def step(
        self,
        value: object,
    ) -> tuple[object, RewriteStep]:
        candidates = self.applicable_rules(value)
        if not candidates:
            raise NoRewriteRuleError(
                "no rewrite rule applies"
            )
        if len(candidates) > 1:
            names = ", ".join(
                rule.name for rule in candidates
            )
            raise AmbiguousRewriteError(
                f"multiple rewrite rules apply: {names}"
            )
        return self.apply(value, candidates[0].name)

    def trace_certified(
        self,
        value: object,
        certificate: FamilyRankTerminationCertificate,
    ) -> RewriteTrace:
        certificate.require_valid(self)
        if self.irreducible(value):
            return RewriteTrace(
                initial=value,
                value=value,
                steps=(),
            )

        family = self._signature_engine.signature(
            value
        ).family
        bound = certificate.rank(family)
        if bound <= 0:
            raise RewriteTerminationCertificateError(
                "rewriteable value has non-positive certified rank"
            )
        return self.trace_until_irreducible(
            value,
            max_steps=bound,
        )

    def trace_explicit(
        self,
        value: object,
        rule_names: tuple[str, ...],
    ) -> RewriteTrace:
        current = value
        steps: list[RewriteStep] = []
        for rule_name in rule_names:
            current, step = self.apply(
                current,
                rule_name,
            )
            steps.append(step)
        return RewriteTrace(
            initial=value,
            value=current,
            steps=tuple(steps),
        )

    def trace_until_irreducible(
        self,
        value: object,
        *,
        max_steps: int = 32,
    ) -> RewriteTrace:
        if max_steps <= 0:
            raise ValueError("max_steps must be positive")

        current = value
        steps: list[RewriteStep] = []
        signature = self._signature_engine.signature(current)
        seen = {
            (
                signature.family,
                strict_normal_form(current).key,
            )
        }

        for _ in range(max_steps):
            candidates = self.applicable_rules(current)
            if not candidates:
                return RewriteTrace(
                    initial=value,
                    value=current,
                    steps=tuple(steps),
                )
            if len(candidates) > 1:
                names = ", ".join(
                    rule.name for rule in candidates
                )
                raise AmbiguousRewriteError(
                    "automatic rewrite trace encountered "
                    f"multiple rules: {names}"
                )

            current, step = self.apply(
                current,
                candidates[0].name,
            )
            steps.append(step)
            signature = self._signature_engine.signature(current)
            key = (
                signature.family,
                strict_normal_form(current).key,
            )
            if key in seen:
                raise RewriteCycleError(
                    "rewrite trace revisited a semantic family/"
                    "strict-value state"
                )
            seen.add(key)

        if self.irreducible(current):
            return RewriteTrace(
                initial=value,
                value=current,
                steps=tuple(steps),
            )
        raise RewriteStepLimitError(
            f"rewrite trace exceeded max_steps={max_steps}"
        )


def rdss_forgetful_rewrite_rules(
) -> tuple[RewriteRule, ...]:
    """Orient currently registered forgetful bridges as rewrite rules."""
    return tuple(
        RewriteRule.from_bridge_spec(spec)
        for spec in rdss_bridge_specs()
        if spec.kind is EquivalenceKind.FORGETFUL_PROJECTION
    )


def rdss_forgetful_rewrite_system() -> RewriteSystem:
    return RewriteSystem(
        rdss_forgetful_rewrite_rules()
    )



def rdss_forgetful_termination_certificate(
) -> FamilyRankTerminationCertificate:
    return FamilyRankTerminationCertificate(
        name="rdss-forgetful-family-rank-v1",
        ranks=(
            ("relation_occurrence", 1),
            ("relational_generative_model", 1),
            ("relational_binary_distinction", 1),
            ("occurrence_relation_path", 1),
            ("typed_relation", 0),
            ("generative_relation_model", 0),
            ("binary_distinction", 0),
            ("relation_path", 0),
        ),
        default_rank=0,
        claim_ids=(
            "REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE",
        ),
    )
