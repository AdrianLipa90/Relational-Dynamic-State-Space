# RDSS Reference Corpus Scan

## Purpose

This milestone applies the canonical/signature/bridge machinery to a finite
corpus built from actual executable RDSS reference types.

It is deliberately not a hand-labelled conceptual table. The corpus is
constructed from current Python objects and the scan is produced by:

\[
\mathcal N_0
\rightarrow
\Sigma
\rightarrow
\text{SignatureCatalog}
\rightarrow
\text{BridgeEquivalenceGraph}
\rightarrow
\text{BridgeGapReport}.
\]

## Corpus contract

The current source corpus contains 36 named values spanning:

- occurrence addresses and reference relational points;
- semantic scale;
- tensor-scalar states and a rank change;
- relation values and relation occurrences;
- value-level and occurrence-aware relation paths;
- Hilbert--Moire fibre states;
- CP1 reference states;
- relative Moire rotations;
- typed zero;
- semantic-scale graph;
- minimal CP1 distinction;
- center-to-half-turn bridge;
- Zero Axis point;
- binary distinction;
- branch-relation occurrence;
- relational binary distinction;
- finite generative relation model.

The corpus intentionally contains duplicate, same-state-family,
same-structure/different-state, structural-difference and cross-family cases.

## Signature-coverage frontier

The first corpus draft exposed nine executable types without admitted
signatures. They were used as explicit coverage targets rather than dropped or
coerced into existing families.

The current source registry now gives each of those types its own semantic
family, so the source contract is:

\[
36
=
36_{\rm supported}
+
0_{\rm coverage\ gaps}.
\]

The newly covered families correspond to:

1. TypedZero;
2. SemanticScaleGraph;
3. MinimalDistinction;
4. CenterHalfTurnBridge;
5. ZeroAxisPoint;
6. BinaryDistinction;
7. BranchRelationOccurrence;
8. RelationalBinaryDistinction;
9. GenerativeRelationModel.

Closing signature coverage does not introduce cross-family equivalence. Each
type remains distinct until a separately justified bridge is registered.

## Expected novelty partition on the supported slice

The source contract currently expects:

\[
\begin{array}{l|r}
\text{class} & \text{count}\\
\hline
\text{EXACT\_REPEAT} & 1\\
\text{SIGNATURE\_EQUIVALENT} & 1\\
\text{REPRESENTATION\_ONLY} & 0\\
\text{NEW\_STATE} & 5\\
\text{NEW\_STRUCTURE} & 6\\
\text{NEW\_FAMILY} & 11
\end{array}
\]

for the original 24-record supported slice. After closing the former coverage
gaps, adding the explicit zero-element bridge witness and adding the relational
generative model, the current 36-record source contract expects
NEW_STATE=6 and NEW_FAMILY=22.

The corresponding catalog expectations are

\[
(
N_{\rm records},
N_{\rm families},
N_{\rm structures},
N_{\rm semantic\ states},
N_{\rm strict\ values}
)
=
(36,22,28,34,35).
\]

These numbers are executable test expectations. They must not be reported as a
runtime PASS until the full branch checkout runs the test suite or the corpus
CLI.

## Bridge-graph expectations

The current source tests expect the full corpus to produce:

\[
N_{\rm equivalence\ components}=30,
\]

with:

\[
N_{\rm strong\ edges}=7,
\qquad
N_{\rm lossy\ projection\ edges}=5,
\qquad
N_{\rm unknown\ bridge\ edges}=0.
\]

The intended compression examples are:

- occurrence root and its reference RelationalPoint coordinate share one
  lossless bridge-equivalence component;
- occurrence left, its repeated occurrence record and its reference point
  coordinate share one component;
- common-shift Moire rotations share one semantic-signature component;
- RelationOccurrence and TypedRelation remain in separate components even
  when a directed LOSSY forgetful projection exists;
- occurrence-aware and value-level relation cycles remain separate components
  across their LOSSY projection;
- a typed U1Phase companion and its finite ZeroAxisPoint share one LOSSLESS
  bridge-equivalence component, so adding the explicit intermediate family
  does not increase the number of independent equivalence components.

## Deterministic CLI receipt

scripts/reference_corpus_scan.py emits JSON schema

rdss.reference-corpus-scan/v1

with:

- corpus size;
- supported size;
- coverage gaps;
- novelty counts and per-record novelty;
- catalog summary;
- equivalence-graph summary;
- bridge-gap summary;
- family-pair gap details.

Default execution is diagnostic. --require-complete returns non-zero if future
corpus growth introduces any signature coverage gap. The current source
contract expects complete coverage, but that expectation still requires runtime
execution on an exact checkout.

## Validation boundary

At the time this document was added, the current environment had verified
live NOEMA/AUX tether and active GREMLIN candidate runtime, but no complete
local RDSS checkout was available. Therefore:

\[
\boxed{
\text{SOURCE CONTRACT PRESENT}
\neq
\text{CORPUS RUNTIME PASS}.
}
\]

The next runtime gate is to execute the corpus CLI and full pytest on an exact
checkout of the branch and preserve the resulting JSON/test receipts.
