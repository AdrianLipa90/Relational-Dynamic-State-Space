from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BridgeTriageStatus(str, Enum):
    IMPLEMENTED_LOSSLESS = "implemented_lossless"
    IMPLEMENTED_LOSSY = "implemented_lossy"
    CONTEXT_REQUIRED = "context_required"
    MISSING_INTERMEDIATE_FAMILY = "missing_intermediate_family"
    COMPOSITE_NOT_EQUIVALENT = "composite_not_equivalent"
    NO_BRIDGE_CLAIM = "no_bridge_claim"


@dataclass(frozen=True)
class BridgeTriageEntry:
    source_family: str
    target_family: str
    status: BridgeTriageStatus
    reason: str
    claim_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.source_family.strip() or not self.target_family.strip():
            raise ValueError("triage families must be non-empty")
        if not self.reason.strip():
            raise ValueError("triage reason must be non-empty")
        if any(not item.strip() for item in self.claim_ids):
            raise ValueError("triage claim ids must be non-empty")


@dataclass(frozen=True)
class BridgeTriageSummary:
    entries: int
    implemented_lossless: int
    implemented_lossy: int
    context_required: int
    missing_intermediate_family: int
    composite_not_equivalent: int
    no_bridge_claim: int


@dataclass(frozen=True)
class BridgeTriageReport:
    entries: tuple[BridgeTriageEntry, ...]

    def by_status(
        self,
        status: BridgeTriageStatus,
    ) -> tuple[BridgeTriageEntry, ...]:
        return tuple(
            entry
            for entry in self.entries
            if entry.status is status
        )

    def summary(self) -> BridgeTriageSummary:
        counts = {
            status: len(self.by_status(status))
            for status in BridgeTriageStatus
        }
        return BridgeTriageSummary(
            entries=len(self.entries),
            implemented_lossless=counts[
                BridgeTriageStatus.IMPLEMENTED_LOSSLESS
            ],
            implemented_lossy=counts[
                BridgeTriageStatus.IMPLEMENTED_LOSSY
            ],
            context_required=counts[
                BridgeTriageStatus.CONTEXT_REQUIRED
            ],
            missing_intermediate_family=counts[
                BridgeTriageStatus.MISSING_INTERMEDIATE_FAMILY
            ],
            composite_not_equivalent=counts[
                BridgeTriageStatus.COMPOSITE_NOT_EQUIVALENT
            ],
            no_bridge_claim=counts[
                BridgeTriageStatus.NO_BRIDGE_CLAIM
            ],
        )


def rdss_reference_bridge_triage() -> BridgeTriageReport:
    """Return the current explicit bridge-gap classification.

    The report is conservative. It records only bridges already implemented or
    obstacles visible from current RDSS typing. It does not infer new bridges
    from similarity.
    """
    return BridgeTriageReport(
        (
            BridgeTriageEntry(
                "occurrence_address",
                "relational_carrier",
                BridgeTriageStatus.IMPLEMENTED_LOSSLESS,
                "Binary reference-coordinate representation has an explicit inverse and strict round trip.",
                (
                    "REF_OCCURRENCE_POINT_BRIDGE",
                    "THM_REFERENCE_COORDINATE_ROUNDTRIP",
                ),
            ),
            BridgeTriageEntry(
                "typed_zero",
                "tensor_scalar_element",
                BridgeTriageStatus.IMPLEMENTED_LOSSLESS,
                "TypedZero is reversibly represented by the all-zero TensorScalarElement in the same typed additive sector.",
                (
                    "REF_TYPED_ZERO_ELEMENT_BRIDGE",
                    "THM_TYPED_ZERO_ELEMENT_ROUNDTRIP",
                ),
            ),
            BridgeTriageEntry(
                "relation_occurrence",
                "typed_relation",
                BridgeTriageStatus.IMPLEMENTED_LOSSY,
                "Occurrence addresses are forgotten while the typed relation value is retained.",
                ("DEF_OCCURRENCE_FORGETFUL_PROJECTION",),
            ),
            BridgeTriageEntry(
                "occurrence_relation_path",
                "relation_path",
                BridgeTriageStatus.IMPLEMENTED_LOSSY,
                "Occurrence path addresses are forgotten while ordered relation values are retained.",
                (
                    "DEF_OCCURRENCE_FORGETFUL_PROJECTION",
                    "THM_OCCURRENCE_COMPOSABILITY_PROJECTS",
                ),
            ),
            BridgeTriageEntry(
                "relational_binary_distinction",
                "binary_distinction",
                BridgeTriageStatus.IMPLEMENTED_LOSSY,
                "Explicit left/right relation labels are forgotten while host and endpoint slots are retained.",
                (
                    "DEF_RELATIONAL_DISTINCTION_FORGETFUL_PROJECTION",
                ),
            ),
            BridgeTriageEntry(
                "relational_generative_model",
                "generative_relation_model",
                BridgeTriageStatus.IMPLEMENTED_LOSSY,
                "RA0_REL_STAR presentation projects to RA0_STAR by forgetting explicit branch-relation binding.",
                (
                    "DEF_RELATIONAL_GENERATIVE_FORGETFUL_PROJECTION",
                    "THM_RA0_STAR_FROM_RA0_REL_STAR",
                ),
            ),
            BridgeTriageEntry(
                "branch_relation_occurrence",
                "typed_relation",
                BridgeTriageStatus.CONTEXT_REQUIRED,
                "Materializing a TypedRelation requires an external mapping from symbolic endpoint labels to RelationalPoint carriers.",
                ("DEF_RELATIONAL_DISTINCTION",),
            ),
            BridgeTriageEntry(
                "zero_axis_point",
                "u1_phase",
                BridgeTriageStatus.IMPLEMENTED_LOSSLESS,
                "The finite projective Omega/Omega^{-1} bridge now uses the explicit U1Phase family and an explicit numerical round-trip validator; u=-1 remains outside the finite bridge domain.",
                (
                    "REF_U1_ZERO_AXIS_FINITE_BRIDGE",
                    "THM_U1_ZERO_AXIS_FINITE_ROUNDTRIP",
                ),
            ),
            BridgeTriageEntry(
                "cp1_distinction",
                "cp1_state",
                BridgeTriageStatus.COMPOSITE_NOT_EQUIVALENT,
                "MinimalDistinction contains an ordered pair of projectively distinct CP1 states over a carrier; it is not another representation of one CP1State.",
                ("REF_CP1",),
            ),
            BridgeTriageEntry(
                "semantic_scale_graph",
                "semantic_scale",
                BridgeTriageStatus.COMPOSITE_NOT_EQUIVALENT,
                "A semantic-scale graph is a relation among scale labels, not another representation of one SemanticScale node.",
                ("PRIM_SCALE",),
            ),
            BridgeTriageEntry(
                "center_half_turn_bridge",
                "moire_relative_rotation",
                BridgeTriageStatus.NO_BRIDGE_CLAIM,
                "CenterHalfTurnBridge records a specific center-to-half-turn bridge; no current theorem identifies that bridge object with a relative Moire rotation.",
                ("BRIDGE_CENTER_HALF_TURN",),
            ),
        )
    )
