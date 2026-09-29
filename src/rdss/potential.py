from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping

from .algebra import SemanticScale


@dataclass(frozen=True)
class RelationalPotentialProfile:
    """Semantic weighting of a fixed residual signature.

    The profile is a derived scalar diagnostic, not a physical energy.
    Residual names are explicit so a semantic change cannot silently add or
    remove measured structure.
    """

    scale: SemanticScale
    weights: tuple[tuple[str, float], ...]
    p: float = 2.0

    def __post_init__(self) -> None:
        p = float(self.p)
        if not isfinite(p) or p < 1.0:
            raise ValueError("potential order p must be finite and >= 1")
        if not self.weights:
            raise ValueError("potential profile needs at least one residual weight")

        normalized: list[tuple[str, float]] = []
        seen: set[str] = set()
        positive = False
        for name, weight in self.weights:
            name = str(name).strip()
            weight = float(weight)
            if not name:
                raise ValueError("residual weight name must be non-empty")
            if name in seen:
                raise ValueError(f"duplicate residual weight: {name}")
            if not isfinite(weight) or weight < 0.0:
                raise ValueError("residual weights must be finite and non-negative")
            positive = positive or weight > 0.0
            seen.add(name)
            normalized.append((name, weight))

        if not positive:
            raise ValueError("potential profile needs at least one positive weight")

        object.__setattr__(self, "p", p)
        object.__setattr__(self, "weights", tuple(normalized))

    @property
    def labels(self) -> frozenset[str]:
        return frozenset(name for name, _ in self.weights)

    @property
    def weight_map(self) -> dict[str, float]:
        return dict(self.weights)

    def evaluate(self, residuals: Mapping[str, float]) -> float:
        """Evaluate a weighted p-potential on one exact residual signature."""
        provided = frozenset(residuals)
        if provided != self.labels:
            missing = sorted(self.labels - provided)
            extra = sorted(provided - self.labels)
            raise ValueError(
                f"residual signature mismatch: missing={missing}, extra={extra}"
            )

        total = 0.0
        weights = self.weight_map
        for name in sorted(self.labels):
            value = float(residuals[name])
            if not isfinite(value) or value < 0.0:
                raise ValueError("residual values must be finite and non-negative")
            total += weights[name] * value ** self.p

        result = total ** (1.0 / self.p)
        if not isfinite(result) or result < 0.0:
            raise ValueError("relational potential must be finite and non-negative")
        return result


def semantic_potential_shift(
    residuals: Mapping[str, float],
    source: RelationalPotentialProfile,
    target: RelationalPotentialProfile,
) -> float:
    """Change in scalar potential caused by changing semantic profile.

    The residual signature is held fixed. This isolates semantic deformation
    from a change in the represented algebraic residuals themselves.
    """
    if source.labels != target.labels:
        raise ValueError("semantic potential shift requires the same residual signature")
    return target.evaluate(residuals) - source.evaluate(residuals)


def relational_attractor_set(
    candidate_potentials: Mapping[str, float],
    *,
    tolerance: float = 1e-12,
) -> tuple[str, ...]:
    """Return every admissible candidate at the minimum relational potential.

    Ties are preserved instead of being resolved arbitrarily.
    """
    if not candidate_potentials:
        raise ValueError("attractor set needs at least one candidate")
    tolerance = float(tolerance)
    if not isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be positive and finite")

    normalized: dict[str, float] = {}
    for label, value in candidate_potentials.items():
        label = str(label).strip()
        value = float(value)
        if not label:
            raise ValueError("candidate label must be non-empty")
        if label in normalized:
            raise ValueError(f"duplicate candidate label: {label}")
        if not isfinite(value) or value < 0.0:
            raise ValueError("candidate potentials must be finite and non-negative")
        normalized[label] = value

    minimum = min(normalized.values())
    return tuple(
        sorted(
            label
            for label, value in normalized.items()
            if abs(value - minimum) <= tolerance
        )
    )
