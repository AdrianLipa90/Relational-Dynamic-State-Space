"""Relational Dynamic State Space (RDSS) reference kernel."""

from .core import (
    ArithmeticRelation,
    DynamicState,
    HilbertMoireSpace,
    HyperoctagonalLattice,
    LinearRelationalAttachment,
    PageAttractorResult,
    SemanticMetric,
    TimeAlgebraOperator,
    evolve_until_page_attractor,
)

__all__ = [
    "ArithmeticRelation",
    "DynamicState",
    "HilbertMoireSpace",
    "HyperoctagonalLattice",
    "LinearRelationalAttachment",
    "PageAttractorResult",
    "SemanticMetric",
    "TimeAlgebraOperator",
    "evolve_until_page_attractor",
]
