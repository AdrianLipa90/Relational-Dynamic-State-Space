from dataclasses import dataclass

import pytest

from rdss.canonical import (
    AmbiguousReductionError,
    EquivalenceKind,
    InformationEffect,
    LossyReductionError,
    ReductionCycleError,
    ReductionEngine,
    ReductionRule,
    roundtrip_check,
    strict_normal_form,
)


@dataclass(frozen=True)
class A:
    value: int


@dataclass(frozen=True)
class B:
    value: int


class Address(tuple):
    pass


def test_strict_normal_form_is_idempotent():
    normal = strict_normal_form(A(3))
    assert strict_normal_form(normal) is normal


def test_type_tag_keeps_distinct_representations_distinct():
    assert not strict_normal_form(A(3)).same_key(
        strict_normal_form(B(3))
    )


def test_tuple_subclass_keeps_its_representation_tag():
    assert not strict_normal_form(Address((-1, 1))).same_key(
        strict_normal_form((-1, 1))
    )


def test_lossless_rule_requires_inverse():
    with pytest.raises(ValueError):
        ReductionRule(
            "bad",
            lambda x: isinstance(x, A),
            lambda x: B(x.value),
            EquivalenceKind.REFERENCE_REPRESENTATION,
            InformationEffect.LOSSLESS,
        )


def test_isomorphism_roundtrip_and_compare():
    rule = ReductionRule(
        "a_to_b",
        lambda x: isinstance(x, A),
        lambda x: B(x.value),
        EquivalenceKind.ISOMORPHISM,
        InformationEffect.LOSSLESS,
        inverse=lambda x: A(x.value),
        preserves=("value",),
        claim_ids=("DEF_TEST",),
    )

    assert roundtrip_check(rule, A(7))

    result = ReductionEngine((rule,)).compare(
        A(7),
        B(7),
    )

    assert result.equivalent
    assert result.comparison_is_lossless
    assert result.left.trace.provenance == ("a_to_b",)


def test_lossy_projection_requires_explicit_opt_in_for_equivalence():
    rule = ReductionRule(
        "drop_sign",
        lambda x: isinstance(x, A),
        lambda x: abs(x.value),
        EquivalenceKind.FORGETFUL_PROJECTION,
        InformationEffect.LOSSY,
    )
    engine = ReductionEngine((rule,))

    with pytest.raises(LossyReductionError):
        engine.compare(A(-3), 3)

    assert engine.compare(
        A(-3),
        3,
        allow_lossy=True,
    ).equivalent


def test_competing_rules_fail_closed():
    first = ReductionRule(
        "first",
        lambda x: isinstance(x, A),
        lambda x: B(x.value),
        EquivalenceKind.APPROXIMATION,
        InformationEffect.UNKNOWN,
    )
    second = ReductionRule(
        "second",
        lambda x: isinstance(x, A),
        lambda x: x.value,
        EquivalenceKind.FORGETFUL_PROJECTION,
        InformationEffect.LOSSY,
    )

    with pytest.raises(AmbiguousReductionError):
        ReductionEngine((first, second)).reduce(A(2))


def test_cycle_is_rejected():
    forward = ReductionRule(
        "a_to_b",
        lambda x: isinstance(x, A),
        lambda x: B(x.value),
        EquivalenceKind.APPROXIMATION,
        InformationEffect.UNKNOWN,
    )
    backward = ReductionRule(
        "b_to_a",
        lambda x: isinstance(x, B),
        lambda x: A(x.value),
        EquivalenceKind.APPROXIMATION,
        InformationEffect.UNKNOWN,
    )

    with pytest.raises(ReductionCycleError):
        ReductionEngine((forward, backward)).reduce(A(2))


def test_nonfinite_values_fail_closed():
    with pytest.raises(ValueError):
        strict_normal_form(float("nan"))
