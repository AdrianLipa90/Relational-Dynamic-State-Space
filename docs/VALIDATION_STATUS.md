# RTOFA Validation Status

Date: 2026-09-29  
Branch: \`feat/rdss-foundation-v0.1\`

This file distinguishes static verification from runtime execution. A static PASS must not be read as a pytest or LaTeX runtime PASS.

## STATIC PASS

### Layer ownership

Observed public definitions:

- core algebra: 9;
- structural operations: 33;
- generic phase: 3;
- relational potential: 3;
- reference realizations: 6;
- Zero Axis bridge: 2;
- package-root public exports: 77.

Static checks found:

- no CP1, Moiré-angle, U(1) winding, or Zero-Axis symbols leaking into \`algebra.py\`;
- no missing public re-exports among the audited layer symbols;
- no stale references to the superseded combined holonomy/phase claim;
- no stale calls to the superseded combined holonomy-to-Zero-Axis helper.

### Claim graph

The current claim ledger contains:

\[
60
\]

unique claim IDs.

Static dependency audit:

- duplicate claim IDs: 0;
- unknown dependency IDs: 0;
- dependency cycles: 0;
- unknown claim IDs referenced by \`tests/test_axioms.py\`: 0.

The relevant separation is now explicit:

\[
\mathcal H_\gamma
\xrightarrow{\chi}
U(1)
\]

is represented by \`REF_HOLONOMY_U1\`, while the optional companion lift

\[
U(1)
\xrightarrow{\Omega^{-1}}
\widehat{\mathcal Z}_0
\]

is represented separately by \`REF_HOLONOMY_ZERO_AXIS\`.

### Test inventory

The current repository contains 166 Python test functions:

| File | Test functions |
|---|---:|
| \`tests/test_algebra.py\` | 12 |
| \`tests/test_axioms.py\` | 35 |
| \`tests/test_closure.py\` | 25 |
| \`tests/test_independence_witnesses.py\` | 10 |
| \`tests/test_layering.py\` | 3 |
| \`tests/test_operations.py\` | 43 |
| \`tests/test_phase.py\` | 3 |
| \`tests/test_potential.py\` | 13 |
| \`tests/test_realizations.py\` | 18 |
| \`tests/test_zero_axis.py\` | 4 |
| **Total** | **166** |

This is an inventory count, not a runtime result.

### Foundational semantics audit

The current foundation is stratified as

\[
\mathrm{META0}
\triangleright
(\mathrm{RA0}+\mathrm{RR1}).
\]

META0 is a model-formation rule: absolute nothingness is not reified in the object language and admissible RTOFA models have non-empty admitted carrier domains. EX0 is a theorem of META0.

RA0 is now orientation-neutral: an admitted observable must be incident to a primitive relation as source or target.

Executable finite witnesses also establish that model non-vacuity does not imply RA0 while \(\operatorname{Adm}\) remains primitive:

\[
\mathrm{META0}\not\Rightarrow\mathrm{RA0}.
\]

The possible definitional reduction of RA0 is intentionally left OPEN.

### Occurrence-level distinction audit

Binary distinction non-degeneracy is now defined at the occurrence/address level.

The two slots

\[
\omega-,
\qquad
\omega+
\]

are distinct even when both carry the same carrier label. The executable singleton witness

\[
D(a)=(a,a)
\]

therefore satisfies recursive occurrence closure without assuming ontic label multiplicity.

The CP1 reference layer keeps a separate geometric non-degeneracy rule: the two projective states representing a distinction must have positive Fubini--Study separation.

### Relationally bound reduction audit

The stronger candidate RA0_REL_STAR explicitly binds the two distinction slots to primitive branch-relation occurrences. The ledger records the strengthening theorem

\[
\mathrm{RA0\_REL\_STAR}
\Rightarrow
\mathrm{RA0}^{*},
\]

together with

\[
\mathrm{RA0\_REL\_STAR}\Rightarrow\mathrm{RA0},
\qquad
\mathrm{RA0\_REL\_STAR}\Rightarrow\mathrm{RR1}.
\]

Hence

\[
\mathrm{RA0\_REL\_STAR}
\Rightarrow
\mathrm{RA0}^{*}
\Rightarrow
\mathrm{RR1},
\]

while independently

\[
\mathrm{RA0\_REL\_STAR}
\Rightarrow
\mathrm{RA0}.
\]

This candidate is executable but remains unpromoted.

The finite non-empty countermodel with one carrier, no primitive relations, and refinement \(a\mapsto(a,a)\) establishes

\[
\mathrm{RA0}^{*}\not\Rightarrow\mathrm{RA0}.
\]

Thus RA0* without primitive relation incidence is strictly weaker than RA0_REL_STAR.

### Occurrence-path holonomy audit

Relation values and relation occurrences are now separate objects.

A carrier/value path may be closed while the corresponding path-labelled occurrence remains open. The singleton refinement step

\[
a_{\varnothing}\to a_{-}
\]

projects to the carrier self-relation \(a\to a\), providing the executable counterexample

\[
\text{carrier-closed}
\not\Rightarrow
\text{occurrence-closed}.
\]

Occurrence-aware holonomy therefore requires closure in both carrier value and occurrence address. The public API now exposes \`RelationOccurrence\`, \`OccurrenceRelationPath\`, and \`OccurrenceTransportPath\`.

### Occurrence-phase representation audit

Value-level and occurrence-level phase representations are now separate executable interfaces.

\[
\mathcal H^{\mathrm{val}}_\gamma
\longrightarrow
U(1)
\]

is represented by \`HolonomyPhaseRepresentation\`, while

\[
\mathcal H^{\mathrm{occ}}_{\widetilde\gamma}
\longrightarrow
U(1)
\]

is represented by \`OccurrenceHolonomyPhaseRepresentation\`.

The occurrence interface rejects carrier-closed but occurrence-open pseudo-loops before phase evaluation. Neither interface is promoted to a universal existence theorem.

### Singleton-cardinality audit

The exact minimum-cardinality statement is split into two steps:

\[
\mathrm{META0}
\Rightarrow
|\operatorname{Adm}|\ge1,
\]

and the explicit singleton reference model attains

\[
|\operatorname{Adm}|=1
\]

while satisfying META0 plus RA0_REL_STAR.

Only their combination yields the exact minimum theorem.

### Typed-zero audit

The additive zero is now typed by the exact additive sector:

\[
(\text{rank},\text{carrier},\text{semantic scale},\text{component dimension}).
\]

Refinement level is derived from the carrier and is not sufficient to identify the zero sector. Two carriers at the same level therefore have distinct typed zeros.

### Relational potential audit

The current potential layer explicitly separates:

\[
\text{semantic scale label}
\neq
\text{supplied semantic weighting profile}.
\]

A pure semantic shift requires the same residual signature and the same potential order \(p\); otherwise the reference implementation fails closed.

The potential remains a scalar relational diagnostic. No potential-to-geometry or physical interpretation is promoted by the current kernel.

### Documentation integrity

Static markdown audit covers the architecture, foundational non-vacuity, relational-admissibility reduction, coherence, indexed-tensor, relational-potential, semantic-weighting, independence-witness, axiom-audit, and README documents.

## RUNTIME NOT RUN ON CURRENT HEAD

### Python tests

The latest branch snapshot has **not** been executed through full local \`pytest\`.

Reason: the available local runtime could not resolve \`github.com\`, so it could not clone/materialize the current branch. GitHub Actions were intentionally not used.

Earlier runtime test runs on older snapshots do not certify the current head.

### LaTeX

The latest \`monograph/main.tex\` has **not** been recompiled after the final layer split and holonomy/Zero-Axis separation.

An earlier pre-refactor snapshot compiled successfully, but that result does not certify the current head.

## OPEN GATES

The following are intentionally open rather than silently assumed:

1. **Indexed tensor contraction gate** — requires explicit slot signatures, pairing, component shape, and contraction evaluator.
2. **Non-strict monoidal coherence gate** — requires parenthesized tensor objects plus explicit associator/braiding isomorphisms before pentagon/hexagon can be tested.
3. **Semantic weighting derivation gate** — the kernel evaluates supplied semantic weights but does not derive \(W_\sigma\) from a semantic graph/context.
4. **Value-holonomy-to-\(U(1)\) existence theorem** — the executable value-level interface exists, but no universal theorem says every RTOFA value holonomy admits such a representation.
5. **Occurrence-holonomy-to-\(U(1)\) existence theorem** — an explicit occurrence-preserving reference interface is now implemented, but no universal theorem says every occurrence-aware holonomy admits such a representation.
6. **Relational-admissibility reduction gate** — RA0 may be demoted only if \(\operatorname{Adm}\) is explicitly redefined by relational incidence; META0 alone does not imply RA0.
7. **Relational distinction binding promotion** — RA0_REL_STAR implies RA0_STAR, RA0, and RR1 only because it explicitly binds distinction slots to primitive branch-relation occurrences; this extra content remains unpromoted.
8. **RA0* promotion** — \(\mathrm{RA0}^{*}\Rightarrow\mathrm{RR1}\) is tracked under the strengthened candidate statement; the canonical object-level pair remains \(\mathrm{RA0}+\mathrm{RR1}\) under META0.

## Branch safety

All writes in this development sequence were directed to

\`feat/rdss-foundation-v0.1\`.

No merge to \`main\` is asserted by this status file.
