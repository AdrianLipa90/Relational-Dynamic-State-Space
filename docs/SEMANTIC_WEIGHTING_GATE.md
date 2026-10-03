# Semantic Weighting Realization Boundary

Historical filename: `SEMANTIC_WEIGHTING_GATE.md`.

## Status

**CLOSED BY UNDERDETERMINATION / REALIZATION DATA REQUIRED.**

The general RDSS potential layer evaluates an explicitly supplied semantic
weighting profile

\[
W_sigma={w_{sigma i}}_{iin I},
\]

but the current structural signature does not select a unique such profile.

This is no longer counted as an open derivation gate.

## Exact no-go witness

Fix the same semantic scale label, the same residual signature ((a,b)), the
same order (p=1), and the same residual vector

\[
D=(1,1).
\]

Both positive profiles

\[
W^{(1)}=(1,1),
qquad
W^{(2)}=(2,1)
\]

satisfy the existing structural requirements, but

\[
V_{W^{(1)}}(D)=2,
qquad
V_{W^{(2)}}(D)=3.
\]

Therefore

\[
\boxed{
(sigma,I,D,p)

otRightarrow
\text{a unique }W_sigma.
}
\]

The theorem-level ledger node is

`THM_SEMANTIC_WEIGHTING_UNDERDETERMINED_BY_SCALE_LABEL`.

The executable witness is
`semantic_weighting_underdetermination_certificate()` in
`src/rdss/realization_boundaries.py`.

## Canonical interpretation

The implemented direction remains

\[
\boxed{
(D,W_sigma,p)longmapsto V_R^{(p)}.
}
\]

A concrete realization may additionally supply a typed law

\[
mathcal W:
(sigma,I,Gamma_{\rm sem},C)
longrightarrow
mathbb R_{ge0}^{I},
\]

together with its own equivariance, normalization and fail-closed rules.
Those are realization data, not missing consequences of the general algebra.

Hence semantic weighting is an explicit input boundary, not an unresolved
foundational or structural theorem.
