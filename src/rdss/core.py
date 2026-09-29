from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, sqrt
from typing import Callable, Mapping, Sequence

Vector = tuple[float, ...]
Matrix = tuple[tuple[float, ...], ...]
SemanticFeatures = Mapping[str, float]


def _finite_vector(values: Sequence[float]) -> Vector:
    out = tuple(float(x) for x in values)
    if not out:
        raise ValueError("state vector must be non-empty")
    if not all(isfinite(x) for x in out):
        raise ValueError("state vector must contain only finite values")
    return out


def _square_matrix(values: Sequence[Sequence[float]]) -> Matrix:
    out = tuple(tuple(float(x) for x in row) for row in values)
    if not out or any(len(row) != len(out) for row in out):
        raise ValueError("metric/operator matrix must be non-empty and square")
    if not all(isfinite(x) for row in out for x in row):
        raise ValueError("matrix must contain only finite values")
    return out


def _matvec(matrix: Matrix, vector: Vector) -> Vector:
    if len(matrix) != len(vector):
        raise ValueError("matrix and vector dimensions do not match")
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix)


def _l2_distance(a: Vector, b: Vector) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must have equal dimensions")
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _matrix_distance(a: Matrix, b: Matrix) -> float:
    if len(a) != len(b) or any(len(x) != len(y) for x, y in zip(a, b)):
        raise ValueError("matrices must have equal dimensions")
    return sqrt(sum((x - y) ** 2 for ra, rb in zip(a, b) for x, y in zip(ra, rb)))


@dataclass(frozen=True)
class ArithmeticRelation:
    """An arithmetic truth separated from its semantic/geometric representation."""

    left: float
    operator: str
    right: float

    def evaluate(self) -> float:
        if self.operator == "+":
            return self.left + self.right
        if self.operator == "-":
            return self.left - self.right
        if self.operator == "*":
            return self.left * self.right
        if self.operator == "/":
            if self.right == 0:
                raise ZeroDivisionError("division by zero")
            return self.left / self.right
        raise ValueError(f"unsupported operator: {self.operator!r}")


@dataclass(frozen=True)
class HyperoctagonalLattice:
    """Topology contract for the spatial carrier.

    RDSS v0.1 does not canonize one unique hyperoctagonal construction.
    The lattice is represented by explicit sites plus an adjacency rule so
    competing realizations can be tested without changing the upper layers.
    """

    sites: tuple[tuple[int, ...], ...]
    neighbors: Callable[[tuple[int, ...]], tuple[tuple[int, ...], ...]]

    def __post_init__(self) -> None:
        if not self.sites:
            raise ValueError("lattice requires at least one site")
        dim = len(self.sites[0])
        if dim == 0 or any(len(site) != dim for site in self.sites):
            raise ValueError("all lattice sites must share a non-zero dimension")

    @property
    def dimension(self) -> int:
        return len(self.sites[0])


@dataclass(frozen=True)
class HilbertMoireSpace:
    """Geometric carrier independent of the time algebra."""

    lattice: HyperoctagonalLattice
    local_dimension: int

    def __post_init__(self) -> None:
        if self.local_dimension <= 0:
            raise ValueError("local Hilbert dimension must be positive")

    @property
    def nominal_dimension(self) -> int:
        return len(self.lattice.sites) * self.local_dimension


@dataclass(frozen=True)
class LinearRelationalAttachment:
    """Reference implementation of the relational attachment N_rel.

    The functional form is intentionally explicit and replaceable:
        chi = bias + sum_k weights[k] * features[k]

    Feature extraction is outside this class. This prevents RDSS from silently
    treating an arbitrary semantic encoding as canonical physics.
    """

    weights: Mapping[str, float]
    bias: float = 0.0

    def __call__(self, features: SemanticFeatures) -> float:
        chi = float(self.bias)
        for name, weight in self.weights.items():
            value = float(features.get(name, 0.0))
            if not isfinite(value) or not isfinite(float(weight)):
                raise ValueError("semantic features and weights must be finite")
            chi += float(weight) * value
        if not isfinite(chi):
            raise ValueError("relational attachment produced non-finite chi")
        return chi


@dataclass(frozen=True)
class SemanticMetric:
    """Metric whose explicit scalar deformation is driven by relational semantics."""

    base_metric: Matrix

    def __post_init__(self) -> None:
        matrix = _square_matrix(self.base_metric)
        object.__setattr__(self, "base_metric", matrix)

    def deform(self, chi: float) -> Matrix:
        if not isfinite(chi):
            raise ValueError("chi must be finite")
        scale = exp(2.0 * chi)
        return tuple(tuple(scale * value for value in row) for row in self.base_metric)


@dataclass(frozen=True)
class TimeAlgebraOperator:
    """One explicit element/action of the time algebra on the state vector."""

    name: str
    matrix: Matrix

    def __post_init__(self) -> None:
        matrix = _square_matrix(self.matrix)
        object.__setattr__(self, "matrix", matrix)
        if not self.name.strip():
            raise ValueError("operator name must be non-empty")

    def act(self, state: Vector) -> Vector:
        return _matvec(self.matrix, _finite_vector(state))


@dataclass(frozen=True)
class DynamicState:
    """One coupled RDSS state.

    The arithmetic/semantic relation is not stored as a truth-value override.
    State evolution and metric deformation are separate outputs of one step.
    """

    vector: Vector
    metric: Matrix
    step_index: int = 0

    def __post_init__(self) -> None:
        vector = _finite_vector(self.vector)
        metric = _square_matrix(self.metric)
        if len(metric) != len(vector):
            raise ValueError("state and metric dimensions must match")
        if self.step_index < 0:
            raise ValueError("step index cannot be negative")
        object.__setattr__(self, "vector", vector)
        object.__setattr__(self, "metric", metric)

    def step(
        self,
        *,
        operator: TimeAlgebraOperator,
        attachment: LinearRelationalAttachment,
        semantic_features: SemanticFeatures,
        semantic_metric: SemanticMetric,
    ) -> "DynamicState":
        next_vector = operator.act(self.vector)
        chi = attachment(semantic_features)
        next_metric = semantic_metric.deform(chi)
        return DynamicState(next_vector, next_metric, self.step_index + 1)


@dataclass(frozen=True)
class PageAttractorResult:
    converged: bool
    iterations: int
    state: DynamicState
    state_delta: float
    metric_delta: float


def evolve_until_page_attractor(
    initial: DynamicState,
    update: Callable[[DynamicState], DynamicState],
    *,
    tolerance: float = 1e-10,
    max_steps: int = 256,
) -> PageAttractorResult:
    """Iterate a coupled update and test fixed-point convergence.

    In RDSS v0.1 a page attractor means a fixed-point attractor. Periodic and
    higher-order attractors are deliberately left for the next layer.
    """

    if tolerance <= 0 or not isfinite(tolerance):
        raise ValueError("tolerance must be positive and finite")
    if max_steps <= 0:
        raise ValueError("max_steps must be positive")

    current = initial
    state_delta = float("inf")
    metric_delta = float("inf")

    for iteration in range(1, max_steps + 1):
        nxt = update(current)
        state_delta = _l2_distance(current.vector, nxt.vector)
        metric_delta = _matrix_distance(current.metric, nxt.metric)
        if state_delta <= tolerance and metric_delta <= tolerance:
            return PageAttractorResult(True, iteration, nxt, state_delta, metric_delta)
        current = nxt

    return PageAttractorResult(False, max_steps, current, state_delta, metric_delta)
