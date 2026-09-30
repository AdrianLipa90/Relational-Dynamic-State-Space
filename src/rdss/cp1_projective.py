from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .realizations import CP1State


CP1_PROJECTIVE_TOLERANCE = 1e-12


class CP1ProjectiveError(RuntimeError):
    pass


@dataclass(frozen=True)
class CP1ProjectivePoint:
    """Chart coordinate for one projective point [alpha:beta] in CP1.

    The chart is selected by the larger amplitude magnitude. Multiplying the
    underlying normalized state by a common non-zero phase leaves both chart
    selection and the coordinate invariant.
    """

    chart: str
    coordinate: complex

    def __post_init__(self) -> None:
        if self.chart not in {"alpha", "beta"}:
            raise ValueError(
                "CP1 projective chart must be 'alpha' or 'beta'"
            )
        z = complex(self.coordinate)
        if not (
            isfinite(z.real)
            and isfinite(z.imag)
        ):
            raise ValueError(
                "CP1 projective coordinate must be finite"
            )
        object.__setattr__(
            self,
            "coordinate",
            z,
        )

    def residual_to(
        self,
        other: "CP1ProjectivePoint",
    ) -> float:
        if not isinstance(other, CP1ProjectivePoint):
            raise TypeError(
                "other must be CP1ProjectivePoint"
            )
        if self.chart != other.chart:
            return float("inf")
        return abs(
            self.coordinate - other.coordinate
        )

    def equivalent_to(
        self,
        other: "CP1ProjectivePoint",
        *,
        tolerance: float = CP1_PROJECTIVE_TOLERANCE,
    ) -> bool:
        if tolerance <= 0 or not isfinite(tolerance):
            raise ValueError(
                "projective tolerance must be positive and finite"
            )
        return (
            self.chart == other.chart
            and self.residual_to(other) <= tolerance
        )


@dataclass(frozen=True)
class CP1ProjectiveComparison:
    left: CP1ProjectivePoint
    right: CP1ProjectivePoint
    determinant_residual: float
    fubini_study_distance: float
    coordinate_residual: float
    equivalent: bool
    tolerance: float


@dataclass(frozen=True)
class CP1ProjectiveClass:
    """Finite reference quotient class represented by one CP1ProjectivePoint."""

    representative: CP1ProjectivePoint
    member_count: int
    member_indices: tuple[int, ...]

    def __post_init__(self) -> None:
        if self.member_count <= 0:
            raise ValueError(
                "projective class must contain at least one member"
            )
        if self.member_count != len(self.member_indices):
            raise ValueError(
                "projective member count must match member indices"
            )


@dataclass(frozen=True)
class CP1ProjectiveQuotientSummary:
    records: int
    strict_representatives: int
    projective_classes: int
    collapsed_representatives: int


@dataclass(frozen=True)
class CP1ProjectiveQuotient:
    points: tuple[CP1ProjectivePoint, ...]
    classes: tuple[CP1ProjectiveClass, ...]
    summary: CP1ProjectiveQuotientSummary


def cp1_projective_point(
    state: CP1State,
) -> CP1ProjectivePoint:
    if not isinstance(state, CP1State):
        raise TypeError(
            "state must be CP1State"
        )

    alpha = state.alpha
    beta = state.beta

    if abs(alpha) >= abs(beta):
        if alpha == 0:
            raise CP1ProjectiveError(
                "normalized CP1 state has no non-zero pivot"
            )
        return CP1ProjectivePoint(
            "alpha",
            beta / alpha,
        )

    if beta == 0:
        raise CP1ProjectiveError(
            "normalized CP1 state has no non-zero pivot"
        )
    return CP1ProjectivePoint(
        "beta",
        alpha / beta,
    )


def cp1_projective_determinant_residual(
    left: CP1State,
    right: CP1State,
) -> float:
    if not isinstance(left, CP1State):
        raise TypeError("left must be CP1State")
    if not isinstance(right, CP1State):
        raise TypeError("right must be CP1State")

    return abs(
        left.alpha * right.beta
        - left.beta * right.alpha
    )


def compare_cp1_projective(
    left: CP1State,
    right: CP1State,
    *,
    tolerance: float = CP1_PROJECTIVE_TOLERANCE,
) -> CP1ProjectiveComparison:
    if tolerance <= 0 or not isfinite(tolerance):
        raise ValueError(
            "projective tolerance must be positive and finite"
        )

    left_point = cp1_projective_point(left)
    right_point = cp1_projective_point(right)
    determinant_residual = (
        cp1_projective_determinant_residual(
            left,
            right,
        )
    )
    distance = left.fubini_study_distance(right)
    coordinate_residual = left_point.residual_to(
        right_point
    )

    equivalent = (
        determinant_residual <= tolerance
        and distance <= tolerance
        and left_point.equivalent_to(
            right_point,
            tolerance=tolerance,
        )
    )

    return CP1ProjectiveComparison(
        left=left_point,
        right=right_point,
        determinant_residual=determinant_residual,
        fubini_study_distance=distance,
        coordinate_residual=coordinate_residual,
        equivalent=equivalent,
        tolerance=tolerance,
    )


def cp1_projectively_equivalent(
    left: CP1State,
    right: CP1State,
    *,
    tolerance: float = CP1_PROJECTIVE_TOLERANCE,
) -> bool:
    return compare_cp1_projective(
        left,
        right,
        tolerance=tolerance,
    ).equivalent


def quotient_cp1_states(
    states: tuple[CP1State, ...],
    *,
    tolerance: float = CP1_PROJECTIVE_TOLERANCE,
) -> CP1ProjectiveQuotient:
    if not states:
        return CP1ProjectiveQuotient(
            points=(),
            classes=(),
            summary=CP1ProjectiveQuotientSummary(
                records=0,
                strict_representatives=0,
                projective_classes=0,
                collapsed_representatives=0,
            ),
        )

    points = tuple(
        cp1_projective_point(state)
        for state in states
    )
    classes: list[list[int]] = []

    for index, state in enumerate(states):
        placed = False
        for members in classes:
            representative = states[members[0]]
            if cp1_projectively_equivalent(
                representative,
                state,
                tolerance=tolerance,
            ):
                members.append(index)
                placed = True
                break
        if not placed:
            classes.append([index])

    quotient_classes = tuple(
        CP1ProjectiveClass(
            representative=points[members[0]],
            member_count=len(members),
            member_indices=tuple(members),
        )
        for members in classes
    )

    return CP1ProjectiveQuotient(
        points=points,
        classes=quotient_classes,
        summary=CP1ProjectiveQuotientSummary(
            records=len(states),
            strict_representatives=len(states),
            projective_classes=len(quotient_classes),
            collapsed_representatives=(
                len(states)
                - len(quotient_classes)
            ),
        ),
    )
