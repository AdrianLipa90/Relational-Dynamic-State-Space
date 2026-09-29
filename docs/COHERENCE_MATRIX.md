# RTOFA Coherence Matrix

This matrix records which compatibility laws are implemented as exact checks, residual diagnostics, or still-open structure.

| Structure pair | Diagnostic / condition | Status |
|---|---|---|
| additive module ↔ relational product | left/right additivity and scalar-linearity residuals | IMPLEMENTED |
| product ↔ associativity | associator | IMPLEMENTED |
| product ↔ commutativity | commutator | IMPLEMENTED |
| transport ↔ composition | transport composition residual | IMPLEMENTED |
| transport ↔ carrier-closed relation-value loop | value-level holonomy residual | IMPLEMENTED |
| transport ↔ occurrence-closed loop | occurrence-aware holonomy residual | IMPLEMENTED |
| carrier closure ↔ occurrence closure | carrier closure does not imply occurrence closure | IMPLEMENTED COUNTEREXAMPLE |
| transport ↔ product | \(\Delta_{T,\star}\) | IMPLEMENTED |
| semantic scale/graph ↔ semantic weighting profile | derivation law \(\mathcal W\) | OPEN — SEMANTIC WEIGHTING GATE |
| residual signature ↔ semantic weighting | \(V_R^{(p)}\) scalar potential | IMPLEMENTED |
| relational potential ↔ geometric deformation | realization/bridge map \(V_R\mapsto\delta g\) or analogue | OPEN |
| semantic scale ↔ orbital action | \(\Delta_{S,U}\) | IMPLEMENTED |
| semantic scale ↔ product | \(\Delta_{S,\star}\) | IMPLEMENTED |
| orbital family ↔ identity/inverse/composition | orbital coherence residuals | IMPLEMENTED |
| orbital action ↔ product | \(\Delta_{U,\star}\) | IMPLEMENTED |
| refinement ↔ product | \(\Delta_F\) | IMPLEMENTED |
| refinement ↔ transport | \(\Delta_{F,T}\) naturality square | IMPLEMENTED |
| arbitrary typed map ↔ tensor product | tensor-map monoidality residual | IMPLEMENTED |
| arbitrary typed map ↔ contraction | contraction naturality residual | IMPLEMENTED |
| semantic scale ↔ transport | naturality square | IMPLEMENTED |
| orbital action ↔ transport | equivariance square | IMPLEMENTED |
| refinement ↔ semantic scale | branch/coarse-graining coherence | IMPLEMENTED |
| refinement ↔ orbital action | branch/orbit equivariance | IMPLEMENTED |
| tensor product ↔ strict associativity/unit/supplied braiding | residual diagnostics | IMPLEMENTED |
| tensor product ↔ non-strict associator/braiding | pentagon/hexagon coherence | OPEN — MONOIDAL COHERENCE GATE |
| contraction ↔ tensor product | requires indexed slot/pairing realization | OPEN — INDEXED TENSOR GATE |
| value-level holonomy ↔ \(U(1)\) phase | explicit representation interface \(\chi\) | REFERENCE IMPLEMENTED |
| occurrence-aware holonomy ↔ \(U(1)\) phase | explicit occurrence-preserving representation interface | REFERENCE IMPLEMENTED |
| occurrence-aware holonomy ↔ \(U(1)\) phase | existence/universality theorem | OPEN |
| value-level holonomy ↔ \(U(1)\) phase | existence/universality theorem for \(\chi\) | OPEN |
| \(U(1)\) phase ↔ Zero Axis | finite \(\Omega^{-1}(u)=u/(1+u)\) lift; \(u=-1\) at infinity | REFERENCE IMPLEMENTED |
| CP1/FS realization ↔ recursive refinement | local-fibre tree realization | REFERENCE IMPLEMENTED |

## Interpretation

An IMPLEMENTED row does not mean the corresponding law is imposed universally. It means the kernel can measure its defect and recognize the zero-defect subclass. REFERENCE IMPLEMENTED means a concrete realization exists and is tested, but it is not promoted to a theorem of the general algebra.

The general principle is

\[
\boxed{
\text{structure preservation is tested, not presumed}.
}
\]

For any compatibility defect \(D\), the exact subclass is

\[
D=0,
\]

while

\[
D\neq 0
\]

is retained as relational deformation data.

The OPEN rows are the next closure targets. They should not be promoted to laws until a definition, executable reference implementation, tests, and LaTeX statement exist.
