# Semantic Weighting Derivation Gate

## Status

**OPEN by design.**

The current RTOFA potential layer can evaluate an explicit semantic weighting profile

\[
W_\sigma
=
\{w_{\sigma i}\}_{i\in I},
\]

but it does not derive those weights from the semantic scale label or scale graph.

## Current invariant

The implemented direction is

\[
\boxed{
(D,W_\sigma,p)
\longmapsto
V_R^{(p)}.
}
\]

The non-implemented direction is

\[
\boxed{
(\Sigma,\text{relations},\text{context})
\;\not\Rightarrow_{\rm current\ kernel}\;
W_\sigma.
}
\]

A scale label such as \(\sigma=\text{fruit}\) is therefore not numerically interpreted by itself.

## Why this gate exists

Inferring weights from semantic labels without an explicit rule would hide a large amount of model-specific structure inside what appears to be an algebraic definition.

A genuine derivation needs an explicit semantic weighting law, for example a typed map of the schematic form

\[
\mathcal W:
(\sigma,I,\Gamma_{\rm sem},C)
\longrightarrow
\mathbb R_{\ge0}^{I},
\]

where

- \(\sigma\) is the semantic scale/context;
- \(I\) is the named residual signature;
- \(\Gamma_{\rm sem}\) is whatever relational semantic structure the realization admits;
- \(C\) is any additional declared context.

The exact domain is deliberately not fixed by the general algebra.

## Promotion conditions

The gate may be promoted only after a concrete realization supplies:

1. an explicit domain for semantic information;
2. a deterministic or probabilistically specified weighting map \(\mathcal W\);
3. invariance/equivariance rules under semantic relabelling where appropriate;
4. normalization or scale conventions;
5. fail-closed behavior for unknown/incompatible semantic inputs;
6. exact and broken witnesses;
7. tests showing that changing representation labels alone does not silently change weights;
8. synchronized LaTeX and claim-ledger entries.

## Non-conclusion

This gate does not weaken the relational potential construction. It separates two problems:

\[
\text{derive semantic weights}
\qquad\text{from}\qquad
\text{evaluate a potential using supplied weights}.
\]

Only the second is part of the current reference kernel.
