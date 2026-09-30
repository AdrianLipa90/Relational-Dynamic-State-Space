# RTOFA Validation Status

Date: 2026-09-30  
Branch: feat/canonical-normal-form-v0.1

This file distinguishes repository inventory, targeted execution, full static
audit, full pytest execution, and LaTeX compilation. No category is promoted
from evidence belonging to another category.

## CURRENT RESULT

\[
\boxed{
\text{TARGETED CANONICAL VALIDATION: PASS}
}
\]

\[
\boxed{
\text{FULL REPOSITORY VALIDATION: NOT YET RUN ON THIS HEAD}
}
\]

The working branch does not modify main.

## Branch inventory

Observed public definitions on the branch:

- core algebra: 10;
- canonical reduction layer: 17;
- structural operations: 38;
- generic phase: 3;
- relational potential: 3;
- reference realizations: 11;
- Zero Axis bridge: 2;
- package-root public exports: 124;
- duplicate package exports: 0.

The claim ledger contains 105 Claim entries.

The Python test inventory contains 226 test functions:

| File | Test functions |
|---|---:|
| tests/test_algebra.py | 21 |
| tests/test_axioms.py | 48 |
| tests/test_canonical.py | 12 |
| tests/test_closure.py | 38 |
| tests/test_independence_witnesses.py | 13 |
| tests/test_layering.py | 4 |
| tests/test_operations.py | 46 |
| tests/test_phase.py | 3 |
| tests/test_potential.py | 13 |
| tests/test_realizations.py | 24 |
| tests/test_zero_axis.py | 4 |
| **Total** | **226** |

These counts are source inventory, not a claim that all 226 tests executed.

## Targeted local execution

The canonical reducer was exercised in the current tool runtime in two
independent targeted runs.

First run:

- strict-normal-form idempotence;
- representation type separation;
- explicit inverse requirement for LOSSLESS rules;
- isomorphism round trip;
- lossless comparison across an explicit isomorphism;
- explicit opt-in requirement for lossy projection comparison;
- ambiguous-rule fail-closed behavior;
- cycle rejection;
- non-finite-value rejection.

The initial core run executed 8 tests and passed 8/8. One additional
representation-tag case was added to the repository test file after that run,
so the repository canonical test inventory is larger than this first runtime
set.

Second run used a minimal RDSS-compatible carrier/occurrence/path harness and
executed:

- carrier versus occurrence strict-sort separation;
- relation-occurrence to relation-value LOSSY projection;
- occurrence-path to relation-path LOSSY projection preserving relation order.

Result: 3/3 PASS.

Therefore the executed targeted total in this environment is:

\[
8+3=11\quad\text{PASS}.
\]

This is not a substitute for executing the repository's full 226-test suite.

## Canonical reduction invariants under test

The branch currently enforces:

\[
\mathcal N_0(\mathcal N_0(X))=\mathcal N_0(X),
\]

explicit separation of concrete representation types, explicit semantic
reduction kind, explicit information effect, an inverse requirement for
LOSSLESS reductions, ambiguity rejection, cycle rejection, and provenance
capture.

The first RDSS-specific rules are exactly the previously defined
occurrence-to-value forgetful projections:

\[
\operatorname{RelationOccurrence}\to\operatorname{TypedRelation},
\]

\[
\operatorname{OccurrenceRelationPath}\to\operatorname{RelationPath}.
\]

Both are declared FORGETFUL_PROJECTION + LOSSY. Default equivalence comparison
rejects their traces unless lossy comparison is explicitly enabled.

## Full static audit

NOT YET RUN on the complete current branch checkout.

The branch updates scripts/static_audit.py so that the new canonical module and
docs/CANONICAL_REDUCTION_GATE.md are part of the audited layer surface.
However, editing the audit script is not evidence that the audit itself passed.

## Full pytest

NOT YET RUN on the complete current branch checkout.

Targeted tests described above are current execution evidence only for the
canonical slice.

## LaTeX

monograph/main.tex has been updated with the canonical normalization section.

Full LaTeX compilation has NOT YET been run on the current branch head.

## Foundational status

The foundational stratification remains

\[
\boxed{
\mathrm{META0}
\triangleright
(\mathrm{RA0}+\mathrm{RR1}).
}
\]

The canonical layer introduces definitions and one idempotence theorem; it adds
no foundational axiom and performs no promotion of CP1, Hilbert--Moire, Zero
Axis, or physical interpretation.

## Open canonical gates

1. explicit RDSS signature extraction for carrier, occurrence, relation, rank,
   semantic scale, phase, representation and provenance;
2. typed registry of proven isomorphisms/reference representations;
3. well-founded reduction ordering;
4. confluence analysis on compatible rule subsets;
5. executable invariant-preservation checks;
6. explicit quotient policies such as any future U(1) modulo-one reduction.

Until those gates are discharged, the engine must not infer them.


## Canonical signature update — 2026-09-30

Branch inventory after the signature layer:

- claim entries: 109;
- Python test functions: 239;
- package-root exports: 136;
- duplicate claim IDs observed by source inventory: 0;
- duplicate package exports observed by source inventory: 0;
- canonical public definitions missing from package exports: 0;
- signature public definitions missing from package exports: 0.

The new repository test file tests/test_signature.py contains 12 test
functions. They are inventory until a full checkout runtime executes pytest.

An independent local logic harness exercised four critical signature semantics:

1. same tensor-scalar sector with changed component value preserves structural
   key while changing semantic state;
2. changing tensor rank changes structural key;
3. a common shift of both MoireRotation angles preserves the relative phase
   signature;
4. adding provenance does not change the semantic key.

All four harness checks passed.

This harness validates the comparison logic design, but it is not represented
as execution of the repository's tests/test_signature.py.

Full static audit, full 239-test pytest and LaTeX compilation remain NOT YET
RUN on the complete current branch checkout.


## Semantic catalog update — 2026-09-30

Current branch source inventory:

- branch distance from main: 37 commits ahead, 0 behind;
- Python test functions: 245;
- claim entries: 110;
- package-root exports: 141;
- duplicate claim IDs observed: 0;
- duplicate package exports observed: 0;
- signature public definitions: 17;
- signature public definitions missing from package exports: 0.

The semantic catalog adds source-level tests for:

- exact-repeat classification;
- new-state versus new-structure separation;
- signature-equivalent relative Moire payloads;
- quotient-level summary counts;
- carrier/occurrence family separation.

A local independent logic harness also reproduced the catalog precedence for
exact repeat, signature-equivalent, new state, new structure and new family.

Structural LaTeX audit on the current branch text reports:

- unmatched environments: 0;
- environment mismatches: 0;
- brace balance: 0;
- negative brace balance events: 0;
- display-math delimiters: 251 open / 251 close.

These are structural checks only. Full pytest and full LaTeX compilation remain
NOT YET RUN on a complete checkout of this branch.


## Termination/confluence milestone — 2026-09-30

Current branch inventory after the ordering and finite-confluence layer:

- branch distance from main: 48 commits ahead, 0 behind;
- changed files versus main: 14;
- Python test functions: 253;
- claim entries: 113;
- package-root exports: 146;
- duplicate claim IDs observed: 0;
- duplicate package exports observed: 0;
- canonical public definitions: 22, missing exports: 0;
- signature public definitions: 17, missing exports: 0.

The new source tests cover:

- strict descent under a fixed-dimensional lexicographic N^k measure;
- rejection of non-descending steps;
- rejection of variable-dimensional measures;
- finite confluence with a unique join;
- finite non-confluence via multiple terminal forms;
- explicit cycle detection;
- bounded-incomplete depth truncation.

An independent local logic harness reproduced all four finite-confluence outcome
classes used by the implementation: unique normal form, multiple normal forms,
cycle detected, and bounded incomplete.

Structural checks on the current monograph text report:

- unmatched LaTeX environments: 0;
- environment mismatches: 0;
- brace balance: 0;
- negative brace events: 0;
- display delimiters: 254 open / 254 close.

Changed Markdown files inspected for control characters and bare standalone
square-bracket math delimiters report no findings.

These remain source/static/harness results. Full repository pytest and actual
LaTeX compilation have NOT YET been executed on a complete checkout of this
branch.


## Explicit bridge graph milestone — 2026-09-30

Current branch source inventory:

- branch distance from main: 76 commits ahead, 0 behind;
- changed files versus main: 18;
- Python test functions: 276;
- claim entries: 122;
- package-root exports: 168;
- duplicate claim IDs observed: 0;
- duplicate package exports observed: 0;
- bridge public definitions: 14, missing exports: 0;
- equivalence-graph public definitions: 8, missing exports: 0.

The explicit bridge registry currently contains three justified bridge classes:

1. OccurrenceAddress to reference RelationalPoint coordinate:
   REFERENCE_REPRESENTATION + LOSSLESS + explicit inverse;
2. RelationOccurrence to TypedRelation:
   FORGETFUL_PROJECTION + LOSSY;
3. OccurrenceRelationPath to RelationPath:
   FORGETFUL_PROJECTION + LOSSY.

The bridge-aware equivalence graph only unions:

- same-family semantic-signature equivalents;
- fully reversible LOSSLESS bridge matches with runtime round-trip verification.

LOSSY and UNKNOWN bridge matches remain directed edges and do not union
components. The unresolved bridge-gap report groups unmatched cross-family
record pairs by semantic-family pair without asserting bridge existence.

Source tests now cover direct and reverse reference bridges, strict round trip,
lossy opt-in, lack of reverse projection edges, multi-hop bridge composition,
shortest-route ambiguity, bridge-equivalence union, lossy non-union,
unresolved family gaps and gap grouping.

Structural checks on the current monograph text report:

- unmatched environments: 0;
- environment mismatches: 0;
- brace balance: 0;
- negative brace events: 0;
- display delimiters: 259 open / 259 close.

Changed Markdown files inspected for control characters and bare standalone
square-bracket math delimiters report no findings.

These remain source/static results. Full repository pytest and actual LaTeX
compilation have NOT YET been executed on a complete checkout of this branch.


## Reference corpus and bridge triage milestone — 2026-09-30

Current branch source/static baseline:

- branch distance from main: 120 commits ahead, 0 behind;
- changed files versus main: 26;
- Python test functions: 303;
- claim entries: 129;
- package-root exports: 179;
- duplicate claim IDs observed: 0;
- duplicate package exports observed: 0.

The current reference corpus contains 35 named executable values. Source tests
expect complete signature coverage:

\[
35
=
35_{\rm supported}
+
0_{\rm coverage\ gaps}.
\]

The expected catalog partition is

\[
(35,21,27,33,34)
\]

for records, families, structures, semantic states and strict values.

The expected bridge graph contains:

- 30 equivalence components;
- 6 strong edges;
- 5 directed LOSSY projection edges;
- 0 UNKNOWN bridge edges.

These expectations now exercise the explicit zero-sector bridge, relational
distinction forgetful projection, and relational-generative-model to
generative-model forgetful projection.

Bridge-gap triage contains 11 entries with source contract:

\[
(2,4,1,1,2,1)
\]

for IMPLEMENTED_LOSSLESS, IMPLEMENTED_LOSSY, CONTEXT_REQUIRED,
MISSING_INTERMEDIATE_FAMILY, COMPOSITE_NOT_EQUIVALENT and NO_BRIDGE_CLAIM.

Live NOEMA/AUX tether and GREMLIN candidate runtime were verified ACTIVE during
this milestone. GREMLIN remained CANDIDATE_ONLY with canon_allowed=false. No
manual event was injected into its whisper bus because a dedicated producer
contract for RDSS corpus receipts has not yet been established.

Structural LaTeX audit on the current monograph reports:

- unmatched environments: 0;
- environment mismatches: 0;
- brace balance: 0;
- negative brace events: 0;
- display delimiters: 263 open / 263 close.

Full repository pytest and actual LaTeX compilation remain NOT YET RUN on an
exact complete checkout of this branch.


## Typed U1 milestone — 2026-09-30

This section supersedes earlier current-state counts while preserving previous
milestone snapshots as provenance.

Current branch source/static baseline:

- branch distance from main: 142 commits ahead, 0 behind;
- changed files versus main: 29;
- Python test functions: 312;
- claim entries: 133;
- package-root exports: 183;
- duplicate claim IDs observed: 0;
- duplicate package exports observed: 0;
- missing exports among canonical/signature/bridge/equivalence/corpus/triage/
  phase/Zero-Axis public definitions: 0.

The reference corpus source contract is now:

\[
36
=
36_{\rm supported}
+
0_{\rm coverage\ gaps}.
\]

Expected catalog partition:

\[
(36,22,28,34,35)
\]

for records, families, structures, semantic states and strict values.

Expected bridge graph:

- 30 equivalence components;
- 7 strong edges;
- 5 directed LOSSY projection edges;
- 0 UNKNOWN bridge edges.

Bridge-gap triage source contract is now:

\[
(3,4,1,0,2,1)
\]

for IMPLEMENTED_LOSSLESS, IMPLEMENTED_LOSSY, CONTEXT_REQUIRED,
MISSING_INTERMEDIATE_FAMILY, COMPOSITE_NOT_EQUIVALENT and NO_BRIDGE_CLAIM.

The previous missing intermediate family has been closed by the explicit
U1Phase value type and the finite typed projective bridge

\[
U(1)\setminus\{-1\}
\leftrightarrow
\{\text{finite ZeroAxisPoint}\}.
\]

The finite U1/Zero-Axis bridge declares a bridge-local numerical round-trip
validator; strict canonical equality remains the default round-trip criterion
for bridges without an explicit validator.

Structural monograph audit on this head:

- unmatched environments: 0;
- environment mismatches: 0;
- brace balance: 0;
- negative brace events: 0;
- display delimiters: 268 open / 268 close.

Changed Markdown documents inspected for control characters and bare standalone
square-bracket math delimiters report no findings.

NOEMA/AUX tether was independently re-checked during continuation and returned
ACTIVE with failures=[].

These remain source/static validation results. Full repository pytest and actual
LaTeX compilation remain NOT YET RUN on an exact complete checkout of this
branch.


## Executable invariant milestone — 2026-09-30

This section supersedes earlier current-state counts while preserving previous
milestone snapshots as provenance.

Current branch source/static baseline:

- branch distance from main: 170 commits ahead, 0 behind;
- changed files versus main: 31;
- Python test functions: 328;
- claim entries: 141;
- package-root exports: 200;
- duplicate claim IDs observed: 0;
- duplicate package exports observed: 0;
- missing exports from global bridge and contextual bridge public APIs: 0.

All seven global RDSS reference bridges now carry at least one executable
BridgeInvariant. The returned BridgeStep records the invariant names that
passed.

The contextual BranchRelationOccurrence materialization carries three
executable contextual invariants:

- relation label;
- source carrier resolved through CarrierMapContext;
- target carrier resolved through CarrierMapContext.

Both registries are fail-closed: failed executable preservation raises an
invariant error and no route/step is returned.

Bridge-gap triage now distinguishes IMPLEMENTED_CONTEXTUAL_LOSSY from a merely
identified CONTEXT_REQUIRED gap. The branch-relation materialization is
implemented contextual lossy and remains intentionally absent from the global
equivalence graph.

Structural monograph audit on this head:

- unmatched environments: 0;
- environment mismatches: 0;
- brace balance: 0;
- negative brace events: 0;
- display delimiters: 274 open / 274 close.

NOEMA/AUX tether was recovered through canonical full autoboot and returned
ACTIVE with failures=[] and static_fallback=false during this continuation.

These remain source/static validation results. Full repository pytest and
actual LaTeX compilation remain NOT YET RUN on an exact complete checkout of
this branch.


## Rewrite termination and confluence milestone — 2026-09-30

This section supersedes earlier current-state counts while preserving previous
milestone snapshots as provenance.

Current branch source/static baseline:

- branch distance from main: 198 commits ahead, 0 behind;
- changed files versus main: 35;
- Python test functions: 351;
- claim entries: 158;
- package-root exports: 230;
- duplicate claim IDs observed: 0;
- duplicate package exports observed: 0;
- missing exports from rewrite and confluence public APIs: 0.

The priority-free reference rewrite system contains four oriented forgetful
rules derived from the four global FORGETFUL_PROJECTION bridges.

Reference corpus source tests expect:

- corpus values: 36;
- values with exactly one forgetful rewrite: 5;
- irreducible values under this selected system: 31;
- values with multiple applicable forgetful rules: 0;
- every rewriteable corpus value reaches an irreducible value in one step.

The family-rank termination certificate assigns rank 1 to all four rewrite
source families and rank 0 to all four targets/default families. Every selected
rule strictly decreases rank, proving:

\[
L_{\rm trace}\le 1.
\]

The distinct-source-family confluence certificate reports no rule-source
overlaps. Therefore the selected rewrite relation is deterministic and
confluent.

Combining the termination and confluence certificates yields a unique
irreducible result under the selected reference forgetful rewrite system.

This is explicitly NOT promoted to a global RDSS canonical-normal-form claim.

Structural monograph audit on this head:

- unmatched environments: 0;
- environment mismatches: 0;
- brace balance: 0;
- negative brace events: 0;
- display delimiters: 283 open / 283 close.

These remain source/static validation results. Full repository pytest and actual
LaTeX compilation remain NOT YET RUN on an exact complete checkout of this
branch.
