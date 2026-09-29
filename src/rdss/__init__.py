"""General relational tensor-scalar orbital-fractal algebra reference kernel."""

from .algebra import (
    CP1State,
    MinimalDistinction,
    MoireRotation,
    RelationalPoint,
    SemanticScale,
    SemanticScaleGraph,
    TensorScalarElement,
    TypedRelation,
    TypedZero,
    ZeroAxisPoint,
    associator,
    closed_path_winding,
    commutator,
    refinement_residual,
    winding_and_residual,
    wrap_phase,
)

__all__ = [
    "CP1State",
    "MinimalDistinction",
    "MoireRotation",
    "RelationalPoint",
    "SemanticScale",
    "SemanticScaleGraph",
    "TensorScalarElement",
    "TypedRelation",
    "TypedZero",
    "ZeroAxisPoint",
    "associator",
    "closed_path_winding",
    "commutator",
    "refinement_residual",
    "winding_and_residual",
    "wrap_phase",
    "CLAIMS",
    "Claim",
    "ClaimKind",
    "claim_map",
    "dependency_closure",
    "foundational_axioms",
    "validate_dependency_dag",
    "ContractionRule",
]


from .axioms import (
    CLAIMS,
    Claim,
    ClaimKind,
    claim_map,
    dependency_closure,
    foundational_axioms,
    validate_dependency_dag,
)


from .operations import (
    ContractionRule,
    OrbitalAction,
    RelationTransport,
    RelationalProductRule,
    reference_tensor_product,
    relative_moire_action,
)
