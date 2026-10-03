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

The weighting profile is structural input. It is not inferred automatically from a semantic scale label. `THM_SEMANTIC_WEIGHTING_UNDERDETERMINED_BY_SCALE_LABEL` proves by explicit counterexample that the current structural signature does not select a unique profile. `docs/SEMANTIC_WEIGHTING_GATE.md` is therefore a historical filename for a closed realization boundary, not an open derivation gate.

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

Separates the unique foundational law, definitions, structural primitives,
formation rules, derived constructions, reference realizations, bridges,
theorems, historical gate identifiers, and external evidence gates.

The current canonical foundational stratification is

\[
A_0
\; + \;
\text{sourced TIR relational-existence typing}
\Longrightarrow
\text{relational witness / durable relation roles}
\Longrightarrow
\text{derived structure}.
\]

\(\mathrm{RA0}\) is theorem-level closed under the sourced relational-existence
typing. Historical \(\mathrm{RR1}\), \(\mathrm{RA0}^{*}\) and
\(\mathrm{RA0}^{\mathrm{rel}*}\) are retained as formation schemas rather
than universal proof obligations. The structural ledger has
\(N_{\mathrm{DERIVATION\_GATE}}=0\); concrete OFHM physical binding is
separately typed as one \(\mathrm{EVIDENCE\_GATE}\).

Three older realization-specific documents are likewise closed by exact
underdetermination rather than by hidden defaults:

- semantic weights are not unique from a scale label/signature;
- indexed contraction is not unique from total rank plus a flat payload;
- non-strict associator/braiding data cannot be reconstructed after
  parenthesization has been flattened.

These are realization-input boundaries, not structural derivation gates. See
`THM_REALIZATION_BOUNDARIES_CLOSED_BY_UNDERDETERMINATION`.

## Layer 4 — Generic phase representation

\`src/rdss/phase.py\`

Contains representation-level U(1) utilities:

- explicit normalized U1Phase values;
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

## Layer 5a — General orbital-fractal Hilbert-Moiré algebra

`src/rdss/orbital_fractal_hilbert_moire.py`

This source-grounded synthesis imports general rules from read-only Infinities,
GREMLIN and Informational-Dynamics-of-Metatime references while keeping RDSS
as the owning algebraic layer.

It contains:

- finite countable symbolic branch addresses \\(\\mathbb Z^{<\\omega}\\);
- an explicit countable ranking and Hilbert-Hotel successor distinct from local refinement;
- Euler inverse-branch realization on a declared complex-Log branch;
- dimension-independent BEES relative-phase coherence;
- the exact U(1) Moiré cocycle \\(M_{ij}M_{jk}=M_{ik}\\);
- norm-preserving Hilbert-fibre transport \\(T_{ij}v=M_{ij}v\\);
- first-order BEES/Kuramoto and second-order IDT relational phase updates.

The layer is finite and executable. It does not promote arbitrary infinite
symbolic addresses to convergent geometric fractal points and does not attach
the algebra to a physical substrate without a separate binding derivation.

See `docs/GENERAL_ORBITAL_FRACTAL_HILBERT_MOIRE_ALGEBRA.md`.

### Alternating half-time phase dynamics

\`src/rdss/alternating_phase_dynamics.py\`

The OFHM dynamical layer is refined by the exact TIR Stella half-successor

\[
H(n,+)=(n,-),\qquad
H(n,-)=(n+1,+),\qquad
H^2=S.
\]

Occurrence order is discrete in half-frames while the internal state remains a
continuous \(U(1)\) phase.

The closed bipolar channel normalization gives 24 directed incidences and 12
undirected exchange pairs. One undirected pair carries information budget
\(\ln2/12\). Normalized \(U(1)\) chordal mismatch fixes

\[
V_{ij}
=
\pi\kappa
\left(1-\cos\Delta_{ij}\right),
\qquad
\kappa=\frac{\ln2}{24\pi}.
\]

Its endpoint gradients are equal and opposite. For a bipolar pair this splits
into an inertial center mode and a relative pendulum equation. On a network,
the same potential gives the Moiré sine coupling; the overdamped
Euler--Lagrange--Rayleigh reduction is gauge-twisted Kuramoto flow.

The frame-native inertial operator on the full successor is the unique local
three-frame stencil, up to scale,

\[
x_{n+1}-2x_n+x_{n-1}.
\]

This closes the historical structural \`GATE_MOIRE_DYNAMICAL_LAW\`.
Physical clock calibration, continuum-field realization and substrate
identification remain downstream bridges.

See \`docs/ALTERNATING_HALF_TIME_PENDULUM_MOIRE_KURAMOTO.md\`.

### Foundational closure frontier

The canonical TIR relational-existence typing is imported explicitly rather
than attributed to \(A_0\) alone. Historical First-Hamlet dynamical gates are
discharged as non-foundational/superseded; \`RA0\` is theorem-level closed;
\`RR1\`, \`RA0_STAR\` and \`RA0_REL_STAR\` are retained as formation schemas,
not open axiomatic obligations.

Arbitrary selected finite refinement is supplied by the free finite-word
occurrence monoid and its right action.

The historical structural Collatz gates are also discharged.

The former geometric-fractal limit gate is closed by a theorem-level no-go:
the canonical infinite symbolic boundary is Baire space
\(\mathbb Z^{\mathbb N}\), while measure, metric scale, Hausdorff dimension
and external geometric embedding are not uniquely selected by the structural
carrier.

Therefore the current ledger has

\[
\boxed{
N_{\rm DERIVATION\_GATE}=0.
}
\]

Physical binding is retained separately as the sole external
\`EVIDENCE_GATE\`:

- \`GATE_OFHM_PHYSICAL_BINDING\`.

See \`docs/FOUNDATIONAL_CLOSURE_FRONTIER.md\`.

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

The critical-axis/unit-circle identity belongs to the companion Zero Axis bridge, not to the primitive RTOFA signature. The finite typed U1/Zero-Axis bridge is explicit on \(U(1)\setminus\{-1\}\); the exceptional phase remains the compactified point at infinity. The existence of a holonomy-to-\(U(1)\) representation is a separate realization question.

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


## Cross-cutting reference corpus layer

\`src/rdss/corpus.py\` and \`scripts/reference_corpus_scan.py\`

The reference corpus is the first finite executable dataset used to exercise
the canonical/signature/bridge stack as one system.

The corpus originally exposed executable types without admitted signature
extractors. Those gaps are now covered by explicit semantic families. The
scanner retains fail-closed coverage-gap reporting for any future corpus value
that lacks an admitted extractor.

The scanner composes:

\[
\mathcal N_0
\to
\Sigma
\to
\text{catalog}
\to
\text{bridge graph}
\to
\text{gap report}.
\]

It therefore acts as a regression target for mathematical compression, not as a
new foundational layer.


## Cross-cutting contextual bridge layer

\`src/rdss/contextual_bridges.py\`

Context-dependent transformations are separated from the global bridge graph.
A contextual bridge is executable only after the caller supplies a typed
context object.

The current example materializes BranchRelationOccurrence into TypedRelation
using CarrierMapContext. This operation is LOSSY because branch-slot identity
is forgotten.

No contextual bridge is automatically promoted to a global equivalence edge.


### Executable bridge invariants

Both global and contextual bridge layers enforce executable preservation tests.
The global form compares source and target projections; the contextual form may
also project through explicit caller-supplied context.

A failed invariant aborts bridge execution. Verified invariant names are stored
on the returned bridge step for downstream audit and GREMLIN ingestion.


## Cross-cutting rewrite layer

src/rdss/rewrite.py

The rewrite system is an oriented transformation layer above explicit bridge
semantics. It does not assign hidden priorities and does not declare canonical
representatives.

The current reference subsystem adapts only FORGETFUL_PROJECTION bridges.
Automatic execution is permitted only when one rule applies. Multiple
applicable rules fail closed as ambiguity; repeated states fail closed as
cycles.

Executable bridge invariants are reused by rewrite steps and verified invariant
names remain attached to the rewrite provenance.


## Cross-cutting confluence layer

src/rdss/confluence.py

The confluence layer separates static rule-overlap candidates from concrete
critical pairs.

The current reference certificate is deliberately sufficient rather than
maximally general: all forgetful rules have distinct source semantic families.
This makes the rewrite relation deterministic and therefore confluent.

The layer combines this confluence certificate with the explicit termination
certificate to produce a certified unique irreducible result under the selected
forgetful rewrite system. It does not promote that result to a global RDSS
canonical normal form.


## Cross-cutting semantic factorization layer

src/rdss/factorization.py

This layer is a view over RDSSSignature, not a second signature system. It
exposes family, structure, state and representation as separate auditable
coordinates and preserves the original signature keys exactly.

The factorization layer is intended for graph compression, diagnostics and
cross-repository comparison where "same structure", "same state" and "same
representation" must not be conflated.


## Cross-cutting claim provenance layer

src/rdss/provenance.py

The provenance layer projects explicit signature/transformation claim IDs onto the existing authoritative claim DAG. Dependencies are returned in topological order.

Value provenance binds semantic factorization and signature extractor provenance to the induced claim subgraph. Bridge routes, rewrite traces and scoped normal forms expose the same dependency expansion from their own recorded root claims.

This is a read-only provenance view. It is not a claim-authoring or claim-promotion mechanism.


## Cross-cutting reduction certificate layer

src/rdss/reduction_certificate.py and src/rdss/certificate_scan.py

The object certificate composes value provenance, certified rewrite trace,
scoped normal form, target provenance, executable invariant evidence and the
combined authoritative claim dependency projection.

The batch scanner applies the same fail-closed factory to the finite reference
corpus and emits aggregate diagnostics. The JSON CLI is intended as a stable
machine-readable handoff surface for later GREMLIN ingestion.

Neither layer changes the claim ledger or promotes scoped results to global
canonical forms.


## Cross-cutting loss witness layer

src/rdss/loss_witness.py

The loss-witness layer adversarially validates the current forgetful projections by constructing distinct source pairs that collapse to one target under the same rule. This provides executable noninjectivity evidence for the LOSSY classification instead of relying on labels alone.

The witness layer reuses the priority-free rewrite system and executable invariant engine; it does not introduce new rewrite rules.
