# RTOFA Layer Architecture

The repository is intentionally split so that the general relational algebra is not contaminated by a particular geometric, phase, or physical realization.

## Layer 0 — Core algebra

\`src/rdss/algebra.py\`

Contains only representation-independent algebraic objects and diagnostics:

- \`RelationalPoint\` for carrier/reference-coordinate values;
- \`OccurrenceAddress\` for canonical path-labelled occurrence identity;
- \`SemanticScale\` and \`SemanticScaleGraph\`;
- \`TensorScalarElement\`;
- \`TypedZero\`;
- \`TypedRelation\`;
- commutator, associator, and generic refinement residual.

The core contains no CP1 state, Bloch/Fubini-Study object, scalar-angle Moiré coordinate, U(1) winding, Zero Axis coordinate, spacetime, or physical law.

Carrier values and occurrence addresses are separate semantic sorts. `RelationalPoint` may retain a binary reference coordinate for compatibility, but branch-aware occurrence identity is carried by `OccurrenceAddress`. See `docs/CARRIER_OCCURRENCE_SEPARATION.md`.

## Layer 1 — Structural operators and coherence

\`src/rdss/operations.py\`

Contains typed executable operators:

\[
\star_R,\quad
\otimes,\quad
\operatorname{Contr},\quad
T_r,\quad
U_g,\quad
S_{\sigma\to\tau},\quad
F_\pm,
\]

together with residual diagnostics for their algebraic laws and naturality squares.

The rule is:

\[
\boxed{\text{structure preservation is measured, not presumed}.}
\]

Occurrence identity is preserved separately from relation values. The structural-operator layer therefore contains both value-level and occurrence-aware path types:

- \`RelationPath\` / \`TransportPath\` for carrier/value paths;
- \`RelationOccurrence\` / \`OccurrenceRelationPath\`;
- \`OccurrenceTransportPath\` for holonomy that requires return to the same occurrence address.

A carrier self-loop can be closed at the value level while remaining open at the occurrence level. Occurrence-aware holonomy is therefore strictly guarded against this information loss.

## Cross-cutting canonical reduction layer

\`src/rdss/canonical.py\`

This layer gives RDSS a fail-closed mechanism for deciding when two
representations may be reduced to a common executable form without silently
erasing semantic distinctions.

The strict form preserves concrete type tags:

\[
\mathcal N_0(X)
=
(\operatorname{type}(X),\operatorname{payload}(X)).
\]

Therefore equal-looking binary coordinates on \`OccurrenceAddress\` and
\`RelationalPoint\` remain different strict forms.

Every non-trivial reduction rule declares:

- semantic relation kind;
- information effect: LOSSLESS, LOSSY, or UNKNOWN;
- optional inverse;
- preserved invariants;
- claim provenance.

Multiple simultaneously applicable rules fail as ambiguity. Re-visiting an
already observed strict key fails as a reduction cycle. LOSSY/UNKNOWN traces
are rejected by default when testing equivalence.

The first RDSS-specific rules are only the already-established
occurrence-to-value forgetful projections. They are explicitly marked LOSSY.
No projection is promoted to identity, isomorphism, or strict equality.

See \`docs/CANONICAL_REDUCTION_GATE.md\`.

## Layer 2 — Relational potential diagnostics

\`src/rdss/potential.py\`

Contains the scalar diagnostic layer built from explicit residual signatures and supplied semantic weighting profiles:

- \`RelationalPotentialProfile\`;
- \`semantic_potential_shift\`;
- \`relational_attractor_set\`.

The weighting profile is structural input. It is not inferred automatically from a semantic scale label. Automatic derivation of weights from a semantic graph/context remains the explicit gate documented in `docs/SEMANTIC_WEIGHTING_GATE.md`.

The core statement is

\[
\text{residual signature}
+
\text{supplied semantic weighting}
\longrightarrow
V_R.
\]

\(V_R\) is not identified with energy or curvature. A map from \(V_R\) into a geometric deformation belongs to a later realization/bridge.

## Layer 3 — Foundational logic

\`src/rdss/axioms.py\`, \`src/rdss/closure.py\`, \`src/rdss/witnesses.py\`

Separates axioms, definitions, structural primitives, derived constructions, reference realizations, bridges, candidate axioms, and theorems.

The current canonical foundational stratification is

\[
\mathrm{META0}
\;\triangleright\;
(\mathrm{RA0}+\mathrm{RR1}).
\]

\(\mathrm{RA0}^{*}\) remains a stronger candidate closure statement.

## Layer 4 — Generic phase representation

\`src/rdss/phase.py\`

Contains representation-level U(1) utilities:

- principal phase wrapping;
- turn count plus residual;
- closed-path winding.

These are not coordinates of the core algebra.

## Layer 5 — Reference realizations

\`src/rdss/realizations.py\`

Contains concrete realizations that may represent parts of the core:

- \`CP1State\`;
- Fubini-Study \`MinimalDistinction\`;
- fibre-local recursive CP1 realization;
- scalar-angle \`MoireRotation\`;
- explicit value-level closed-holonomy-to-U(1) representation interface;
- explicit occurrence-closed-holonomy-to-U(1) representation interface (`OccurrenceHolonomyPhaseRepresentation`).

A reference realization is executable and tested but is not thereby a theorem forced by the core axioms.

## Layer 6 — Zero Axis bridge

\`src/rdss/zero_axis.py\`

Contains the finite Zero Axis point

\[
s=\frac12+it
\]

and its projective coordinate

\[
\Omega(s)=\frac{s}{1-s}.
\]

For a separately verified phase \(u\in U(1)\), \(u\neq-1\), the optional bridge is

\[
\Omega^{-1}(u)=\frac{u}{1+u}.
\]

The critical-axis/unit-circle identity belongs to the companion Zero Axis bridge, not to the primitive RTOFA signature. The existence of a holonomy-to-\(U(1)\) representation is a separate realization question.

## Public API

\`src/rdss/__init__.py\` re-exports stable user-facing names from all layers for convenience. Re-export does not change epistemic ownership: a symbol exported by \`rdss\` may still belong to a realization or bridge layer rather than the core.

## Promotion invariant

Any promoted structure must be synchronized across:

\[
\boxed{
\text{definition}
+
\text{implementation}
+
\text{test}
+
\text{LaTeX}
}
\]

and its epistemic role must remain explicit.


## Cross-cutting canonical signature layer

\`src/rdss/signature.py\`

This layer classifies supported executable values without changing their
epistemic ownership.

It records structural axes

\[
(\text{carrier},\text{occurrence},\text{relations},\text{rank},
\text{scale},\text{orbit},\text{dimension})
\]

separately from state axes

\[
(\text{phase},\text{state}),
\]

and records concrete representation and provenance independently.

The comparison layer distinguishes exact semantic signature,
representation-only variants, same structure with different state, structural
difference, and incomparable semantic families.

Incomparability is fail-closed. Cross-family identification requires an
explicit bridge rather than a heuristic similarity rule.

The current registry has no generic reflection fallback: only explicitly
admitted RDSS types receive signatures.

See \`docs/CANONICAL_REDUCTION_GATE.md\`.


## Cross-cutting bridge graph layer

\`src/rdss/bridges.py\` and \`src/rdss/equivalence_graph.py\`

The bridge registry is the only cross-family routing authority for canonical
comparison. Similar-looking signatures do not create edges automatically.

Reversible LOSSLESS bridges may generate strong equivalence edges after
runtime round-trip verification. Forgetful/LOSSY bridges remain directed
projection edges.

The equivalence graph therefore separates

\[
\boxed{
\text{lossless equivalence connectivity}
\neq
\text{directed information-losing projection}.
}
\]

This layer does not alter the epistemic ownership of the underlying
realizations or bridges.
