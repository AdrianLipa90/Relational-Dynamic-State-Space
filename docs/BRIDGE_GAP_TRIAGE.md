# RDSS Bridge-Gap Triage

## Purpose

This document classifies bridge gaps without inferring equivalence from visual
or conceptual similarity.

The machine-readable source is src/rdss/triage.py and the deterministic CLI is
scripts/reference_bridge_triage.py.

## Status vocabulary

The current statuses are:

- IMPLEMENTED_LOSSLESS — explicit bridge, explicit inverse, runtime round-trip
  obligation;
- IMPLEMENTED_LOSSY — explicit one-way projection with information loss;
- IMPLEMENTED_CONTEXTUAL_LOSSY — explicit one-way projection that is executable
  only with caller-supplied typed context and is intentionally excluded from
  the global bridge graph;
- CONTEXT_REQUIRED — a context-dependent transformation has been identified but
  no typed contextual bridge implementation exists yet;
- MISSING_INTERMEDIATE_FAMILY — a known bridge formula requires a semantic
  family that is not yet represented explicitly in the signature layer;
- COMPOSITE_NOT_EQUIVALENT — the source is a compound object containing target
  objects but is not another representation of one target object;
- NO_BRIDGE_CLAIM — no current theorem/definition justifies a bridge.

## Current triage

| Source family | Target family | Status | Reason |
|---|---|---|---|
| occurrence_address | relational_carrier | IMPLEMENTED_LOSSLESS | Binary reference-coordinate map has explicit inverse and strict round trip. |
| typed_zero | tensor_scalar_element | IMPLEMENTED_LOSSLESS | TypedZero is the all-zero element in the exact same typed additive sector. |
| relation_occurrence | typed_relation | IMPLEMENTED_LOSSY | Occurrence addresses are forgotten. |
| occurrence_relation_path | relation_path | IMPLEMENTED_LOSSY | Path occurrence addresses are forgotten. |
| relational_binary_distinction | binary_distinction | IMPLEMENTED_LOSSY | Explicit relation labels are forgotten. |
| relational_generative_model | generative_relation_model | IMPLEMENTED_LOSSY | Explicit branch-relation binding is forgotten under RA0_REL_STAR to RA0_STAR projection. |
| branch_relation_occurrence | typed_relation | IMPLEMENTED_CONTEXTUAL_LOSSY | CarrierMapContext supplies the symbolic-label to RelationalPoint map; materialization remains LOSSY because the branch slot is forgotten and the bridge is not inserted into the global graph. |
| zero_axis_point | u1_phase | IMPLEMENTED_LOSSLESS | Explicit U1Phase now bridges reversibly to finite ZeroAxisPoint through Omega/Omega^{-1}; u=-1 remains outside the finite domain. |
| cp1_distinction | cp1_state | COMPOSITE_NOT_EQUIVALENT | MinimalDistinction contains two CP1 states over a carrier; it is not one CP1 state. |
| semantic_scale_graph | semantic_scale | COMPOSITE_NOT_EQUIVALENT | A scale graph is a relation among scale labels, not one scale node. |
| center_half_turn_bridge | moire_relative_rotation | NO_BRIDGE_CLAIM | No current claim identifies the bridge object with a relative Moire rotation. |

Current summary:

\[
(
N_{\rm entries},
N_{\rm lossless},
N_{\rm lossy},
N_{\rm context},
N_{\rm missing\ intermediate},
N_{\rm composite},
N_{\rm no\ claim}
)
=
(11,3,4,1,0,0,2,1).
\]

## Consequence for next work

The next mathematically justified bridge work is not to add arbitrary edges.

The priority order is:

1. preserve contextual bridges outside the global equivalence graph unless a
   future theorem eliminates their external-context dependency;
2. preserve composite objects as composites unless a quotient/decomposition
   theorem explicitly changes their status;
3. keep CenterHalfTurnBridge and MoireRotation distinct until a bridge theorem
   exists.

This triage is diagnostic. It neither asserts that every gap should be closed
nor that every pair of families admits a meaningful bridge.
