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
- package-root public exports: 67.

Static checks found:

- no CP1, Moiré-angle, U(1) winding, or Zero-Axis symbols leaking into \`algebra.py\`;
- no missing public re-exports among the audited layer symbols;
- no stale references to the superseded combined holonomy/phase claim;
- no stale calls to the superseded combined holonomy-to-Zero-Axis helper.

### Claim graph

The current claim ledger contains:

\[
44
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

The current repository contains 124 Python test functions:

| File | Test functions |
|---|---:|
| \`tests/test_algebra.py\` | 12 |
| \`tests/test_axioms.py\` | 26 |
| \`tests/test_closure.py\` | 8 |
| \`tests/test_independence_witnesses.py\` | 5 |
| \`tests/test_layering.py\` | 3 |
| \`tests/test_operations.py\` | 37 |
| \`tests/test_phase.py\` | 3 |
| \`tests/test_potential.py\` | 13 |
| \`tests/test_realizations.py\` | 13 |
| \`tests/test_zero_axis.py\` | 4 |
| **Total** | **124** |

This is an inventory count, not a runtime result.

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

Static markdown audit found no remaining control-character corruption or bare math delimiters in the audited architecture, coherence, indexed-tensor, relational-potential, semantic-weighting-gate, independence-witness, axiom-audit, and README documents after the raw-string repair.

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
4. **Holonomy-to-\(U(1)\) existence theorem** — the executable interface exists, but no universal theorem says every RTOFA holonomy admits such a representation.
5. **RA0* promotion** — \(\mathrm{RA0}^{*}\Rightarrow\mathrm{RR1}\) is tracked under the strengthened candidate statement; the canonical foundational set remains \(\mathrm{RA0}+\mathrm{RR1}\).

## Branch safety

All writes in this development sequence were directed to

\`feat/rdss-foundation-v0.1\`.

No merge to \`main\` is asserted by this status file.
