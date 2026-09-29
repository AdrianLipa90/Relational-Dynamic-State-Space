from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Sequence

ComplexVector = tuple[complex, ...]
ComplexMatrix = tuple[tuple[complex, ...], ...]


def _finite_complex(z: complex) -> bool:
    return isfinite(z.real) and isfinite(z.imag)


def _complex_vector(values: Sequence[complex]) -> ComplexVector:
    out = tuple(complex(v) for v in values)
    if not out:
        raise ValueError("Hilbert vector must be non-empty")
    if not all(_finite_complex(v) for v in out):
        raise ValueError("Hilbert vector must contain only finite values")
    return out


def _rect_matrix(values: Sequence[Sequence[complex]]) -> ComplexMatrix:
    out = tuple(tuple(complex(v) for v in row) for row in values)
    if not out or not out[0]:
        raise ValueError("representation matrix must be non-empty")
    width = len(out[0])
    if any(len(row) != width for row in out):
        raise ValueError("representation matrix rows must have equal length")
    if not all(_finite_complex(v) for row in out for v in row):
        raise ValueError("representation matrix must contain finite values")
    return out


def _square_matrix(values: Sequence[Sequence[complex]]) -> ComplexMatrix:
    out = _rect_matrix(values)
    if len(out) != len(out[0]):
        raise ValueError("metric matrix must be square")
    return out


def _matvec(matrix: ComplexMatrix, vector: ComplexVector) -> ComplexVector:
    if len(matrix[0]) != len(vector):
        raise ValueError("representation and Hilbert dimensions do not match")
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix)


@dataclass(frozen=True)
class InfoHolonomicCoordinate:
    """Internal complex RDSS coordinate zeta = I + i*Theta.

    It belongs to the Hilbert-state description. It is not an external
    spacetime axis and does not select any particular derived geometry.
    """

    information: float
    holonomic: float

    def __post_init__(self) -> None:
        if not (isfinite(self.information) and isfinite(self.holonomic)):
            raise ValueError("informational-holonomic coordinates must be finite")

    @property
    def zeta(self) -> complex:
        return complex(self.information, self.holonomic)


@dataclass(frozen=True)
class HilbertMoireKet:
    """Canonical RDSS carrier state before choosing a representation."""

    amplitudes: ComplexVector
    info_holonomic: InfoHolonomicCoordinate = InfoHolonomicCoordinate(0.0, 0.0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "amplitudes", _complex_vector(self.amplitudes))

    @property
    def norm(self) -> float:
        return sqrt(sum(abs(v) ** 2 for v in self.amplitudes))


@dataclass(frozen=True)
class DerivedRepresentation:
    """A derived coordinate representation of the canonical Hilbert carrier."""

    name: str
    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("representation name must be non-empty")
        object.__setattr__(self, "matrix", _rect_matrix(self.matrix))

    def project(self, state: HilbertMoireKet) -> ComplexVector:
        return _matvec(self.matrix, state.amplitudes)


@dataclass(frozen=True)
class RepresentationMetric:
    """Metric/quadratic form attached to one derived representation."""

    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        object.__setattr__(self, "matrix", _square_matrix(self.matrix))

    def quadratic_form(self, displacement: Sequence[complex]) -> complex:
        v = _complex_vector(displacement)
        if len(v) != len(self.matrix):
            raise ValueError("metric and representation dimensions do not match")
        gv = _matvec(self.matrix, v)
        return sum(v[i].conjugate() * gv[i] for i in range(len(v)))


def representation_displacement(
    representation: DerivedRepresentation,
    start: HilbertMoireKet,
    end: HilbertMoireKet,
) -> ComplexVector:
    a = representation.project(start)
    b = representation.project(end)
    return tuple(y - x for x, y in zip(a, b))
