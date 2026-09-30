# Canonical Normal Form and Reduction Gate

## Purpose

This layer exists to reduce representational chaos without silently identifying
mathematically different objects.

The governing rule is:

\[
\boxed{
\text{normalize structure}
\neq
\text{erase distinctions}.
}
\]

RDSS therefore separates strict canonical identity from explicit semantic
reductions.

## Strict canonical normal form

For an executable value \(X\), define the strict normal form

\[
\mathcal N_0(X)
=
(\operatorname{type}(X),\operatorname{payload}(X)).
\]

The reference implementation recursively freezes finite executable data while
retaining type tags. Dataclasses retain field names and values; tuple
subclasses retain their concrete type tag; finite floats and complex values are
encoded exactly rather than rounded.

Consequently, representation type remains part of strict identity.

In particular,

\[
\boxed{
\mathcal N_0(
\operatorname{OccurrenceAddress}(\omega)
)
\neq
\mathcal N_0(
\operatorname{RelationalPoint}(\omega)
)
}
\]

even when the displayed binary coordinates coincide.

This preserves the existing carrier/occurrence separation.

By construction,

\[
\boxed{
\mathcal N_0(\mathcal N_0(X))
=
\mathcal N_0(X).
}
\]

This is registered as THM_STRICT_NORMAL_FORM_IDEMPOTENCE.

## Explicit reduction rule

A reduction rule is typed by

\[
R
=
(P,f,\rho,\eta,f^{-1},\mathcal I,\mathcal C),
\]

where \(P\) is the applicability predicate, \(f\) the forward transformation,
\(\rho\) the semantic relation kind, \(\eta\) the information effect,
\(f^{-1}\) an optional explicit inverse, \(\mathcal I\) the preserved
invariants and \(\mathcal C\) the claim-provenance set.

The allowed relation kinds are

\[
\rho\in
\{
\mathrm{IDENTITY},
\mathrm{EXACT\_EQUIVALENCE},
\mathrm{ISOMORPHISM},
\mathrm{REFERENCE\_REPRESENTATION},
\mathrm{FORGETFUL\_PROJECTION},
\mathrm{APPROXIMATION}
\}.
\]

The information effect is independently declared as

\[
\eta\in
\{
\mathrm{LOSSLESS},
\mathrm{LOSSY},
\mathrm{UNKNOWN}
\}.
\]

The two classifications are intentionally independent.

## Reversibility rule

A reduction may be declared LOSSLESS only when an explicit inverse is supplied.

For an isomorphism rule this is mandatory:

\[
\boxed{
\rho=\mathrm{ISOMORPHISM}
\Longrightarrow
\eta=\mathrm{LOSSLESS}
\land
f^{-1}\text{ supplied}.
}
\]

The executable roundtrip check verifies

\[
\mathcal N_0\!\left(f^{-1}(f(X))\right)
=
\mathcal N_0(X).
\]

A passing round trip is evidence for the supplied executable realization; it is
not by itself a universal theorem about every object in a broader mathematical
class.

## Fail-closed reduction dynamics

For current state \(X_k\), let

\[
A(X_k)
=
\{R_j:P_j(X_k)=\mathrm{True}\}
\]

be the set of applicable reduction rules.

The engine uses

\[
|A(X_k)|=0
\Rightarrow
\text{normal form reached},
\]

\[
|A(X_k)|=1
\Rightarrow
X_{k+1}=f_j(X_k),
\]

\[
|A(X_k)|>1
\Rightarrow
\boxed{\mathrm{AMBIGUOUS\_REDUCTION}}.
\]

Registration order is not used as hidden mathematical authority.

The exact canonical key of every visited state is retained. Re-visiting a key,
or applying a no-progress rule, raises a cycle error:

\[
\mathcal N_0(X_{k+1})
\in
\{
\mathcal N_0(X_0),\ldots,\mathcal N_0(X_k)
\}
\Rightarrow
\boxed{\mathrm{REDUCTION\_CYCLE}}.
\]

A finite max_steps guard is an additional executable termination boundary.
A general global termination or confluence theorem has not yet been claimed.

## Provenance trace

Every accepted reduction step records

\[
(
\text{rule},
\rho,
\eta,
\mathcal N_0(X_k),
\mathcal N_0(X_{k+1}),
\text{inverse?},
\mathcal I,
\mathcal C
).
\]

Thus the final canonical key and the route used to obtain it remain separate:

\[
\boxed{
\text{canonical key}
\neq
\text{provenance}.
}
\]

Two values may have the same final key while retaining different provenance
histories.

## Equality versus projection comparison

The default comparison path rejects any reduction trace containing LOSSY or
UNKNOWN.

Therefore

\[
\boxed{
\text{strict/lossless comparison}
\neq
\text{comparison after information loss}.
}
\]

A lossy comparison requires explicit allow_lossy=True. That opt-in means only
that the caller intentionally compares the projected values. It does not
promote the original inputs to strict equality, isomorphism, or identity.

## Initial RDSS projection rules

The first domain-specific rule set contains only structures whose status was
already explicit in RDSS.

For a relation occurrence,

\[
(r,\omega_s,\omega_t)
\longmapsto
r,
\]

and for an occurrence-aware path,

\[
((r_1,\omega_0,\omega_1),\ldots,
 (r_n,\omega_{n-1},\omega_n))
\longmapsto
(r_1,\ldots,r_n).
\]

Both are declared

\[
\boxed{
\rho=\mathrm{FORGETFUL\_PROJECTION},
\qquad
\eta=\mathrm{LOSSY}.
}
\]

They are grounded in DEF_OCCURRENCE_FORGETFUL_PROJECTION; the path rule also
records THM_OCCURRENCE_COMPOSABILITY_PROJECTS.

The projection preserves ordered relation values and carrier composability, but
it discards occurrence addresses. Therefore it cannot be used silently to
claim occurrence-level equivalence.

## Non-assumptions

The canonical reduction layer does not assume:

- OccurrenceAddress equals RelationalPoint;
- projection equality implies identity;
- every reference representation is invertible;
- every reduction system is confluent;
- every reduction system terminates globally;
- approximation is exact equivalence;
- CP1, Hilbert--Moire, Zero Axis, or a physical geometry is the unique normal
  form of RDSS.

## Next gates

The current implementation establishes the reduction substrate. The next
mathematical gates are:

1. an explicit RDSS signature extractor for carrier, occurrence, relation,
   rank, semantic scale, phase, and representation fields;
2. a typed registry of proven isomorphisms and reference representations;
3. confluence analysis for compatible rule subsets;
4. a well-founded reduction ordering for termination proofs;
5. explicit quotient policies, including any future \(U(1)\) phase
   normalization modulo one turn;
6. machine-readable invariant preservation checks rather than string labels
   alone.

No item in this list is silently assumed by v0.1.


## Canonical semantic signature

Strict normalization answers whether two executable values have the same exact
tagged payload. It does not by itself answer whether a difference belongs to
structure, state, or representation.

The signature layer therefore records

\[
\boxed{
\Sigma(X)=
(
\text{family};
\text{carrier},
\text{occurrence},
\text{relations},
\text{rank},
\text{scale},
\text{orbit},
\text{dimension};
\text{phase},
\text{state};
\text{representation},
\text{provenance}
).
}
\]

The semicolons indicate the current stratification.

Structural axes are

\[
\{
\text{carrier},
\text{occurrence},
\text{relations},
\text{rank},
\text{scale},
\text{orbit},
\text{dimension}
\},
\]

while state axes are

\[
\{
\text{phase},
\text{state}
\}.
\]

Representation and provenance are recorded separately.

This prevents a changed amplitude, phase or vector from being promoted to a
change of algebraic structure. Conversely, a changed carrier, occurrence path,
relation topology, tensor rank, semantic scale, orbital sector or dimension is
not hidden as a mere state update.

### Signature comparison

For two supported objects \(X,Y\), comparison is classified as one of

\[
\begin{aligned}
&\mathrm{EXACT\_SIGNATURE},\\
&\mathrm{SAME\_SEMANTIC\_STATE\_DIFFERENT\_REPRESENTATION},\\
&\mathrm{SAME\_STRUCTURE\_DIFFERENT\_STATE},\\
&\mathrm{STRUCTURAL\_DIFFERENCE},\\
&\mathrm{INCOMPARABLE}.
\end{aligned}
\]

INCOMPARABLE is fail-closed. It means the current signature registry has no
declared common semantic family. It does not mean that no bridge can exist.
Such a bridge must be added explicitly before a stronger identification is
allowed.

Relative novelty is then classified as

\[
\{
\text{exact repeat},
\text{signature-equivalent},
\text{representation-only},
\text{new state},
\text{new structure},
\text{new family}
\}.
\]

Thus the executable question

\[
\boxed{
\text{new information?}
\quad\text{or}\quad
\text{new representation?}
}
\]

is no longer answered by visual similarity.

### Current admitted extractors

Version 0.1 supplies explicit extractors for:

- OccurrenceAddress;
- RelationalPoint;
- SemanticScale;
- TensorScalarElement;
- TypedRelation;
- RelationOccurrence;
- RelationPath;
- OccurrenceRelationPath;
- HilbertMoireFibreState;
- CP1State;
- MoireRotation.

No generic reflection fallback is used. Unsupported object types fail closed.

The MoireRotation extractor uses the already-defined relative phase delta as
its semantic phase axis. Consequently a common shift of both supplied angles
may change the raw executable payload while leaving the same relative
signature. This is classified as signature-equivalent rather than strict
object identity.

The CP1 extractor currently retains the normalized representative amplitudes as
state. A global-phase quotient is not silently imposed by this version; an
explicit projective canonicalization policy remains a later gate.


## Semantic signature catalog

Pairwise comparison is lifted to a finite catalog without deleting source
objects.

For indexed records \(X_i\), the catalog simultaneously groups by

\[
\text{family},
\qquad
K_{\rm struct},
\qquad
K_{\rm semantic},
\qquad
K_{\rm strict}.
\]

These correspond to progressively finer quotients:

\[
\boxed{
\text{family}
\supseteq
\text{structure}
\supseteq
\text{semantic state}
\supseteq
\text{strict payload}.
}
\]

A new candidate is classified against previously indexed records in the
following fail-closed precedence:

\[
\text{EXACT\_REPEAT}
\prec
\text{SIGNATURE\_EQUIVALENT}
\prec
\text{REPRESENTATION\_ONLY}
\prec
\text{NEW\_STATE}
\prec
\text{NEW\_STRUCTURE}
\prec
\text{NEW\_FAMILY}.
\]

The order is a classification precedence, not a numeric metric or value
judgment.

The catalog retains every source value and its ordinal. It does not physically
merge, delete, or rewrite records. Its role is to expose where apparent
multiplicity collapses at a chosen semantic quotient level.

The summary reports:

\[
(
N_{\rm records},
N_{\rm families},
N_{\rm structures},
N_{\rm semantic\ states},
N_{\rm strict\ values}
).
\]

This provides the first executable compression view over a heterogeneous RDSS
object set.


## Termination ordering

Cycle detection protects one observed run but does not prove that every
possible reduction path terminates. A stronger certificate is an explicit
well-founded measure.

Version 0.1 admits a fixed-dimensional map

\[
\mu:X\to\mathbb N^k,
\qquad
1\le k<\infty,
\]

with lexicographic order. The dimension \(k\) is fixed by the order object; a
variable-length tuple is rejected.

Every ordered reduction step must satisfy

\[
\boxed{
\mu(X_{n+1})<_{\rm lex}\mu(X_n).
}
\]

Because lexicographic order on fixed finite-dimensional \(\mathbb N^k\) is
well-founded, an infinite strictly descending chain cannot exist. Therefore

\[
\boxed{
\forall n\;
\mu(X_{n+1})<_{\rm lex}\mu(X_n)
\Longrightarrow
\text{the reduction sequence terminates}.
}
\]

The executable engine checks strict descent at every applied step. A
non-descending rule fails closed.

This theorem is conditional on the supplied measure being defined on every
state reached by the admitted reduction system. RDSS does not invent a measure
for a rule set.

## Finite confluence audit

Operational reduction rejects multiple simultaneously applicable rules as
AMBIGUOUS_REDUCTION. A separate audit mode intentionally explores those
branches to test whether they rejoin.

For a supplied start state and finite depth \(d\), the auditor constructs the
reachable reduction graph and reports one of

\[
\{
\mathrm{UNIQUE\_NORMAL\_FORM},
\mathrm{MULTIPLE\_NORMAL\_FORMS},
\mathrm{CYCLE\_DETECTED},
\mathrm{BOUNDED\_INCOMPLETE}
\}.
\]

UNIQUE_NORMAL_FORM means that the fully explored bounded graph reaches exactly
one terminal strict canonical key and contains no detected cycle or depth
truncation.

MULTIPLE_NORMAL_FORMS is a concrete non-confluence witness for the explored
start state.

CYCLE_DETECTED is a concrete termination failure witness unless an additional
quotient or ordering changes the admitted state graph.

BOUNDED_INCOMPLETE means the selected depth was insufficient to decide.

The finite audit is evidence on one explored graph. It is deliberately not
promoted to a global Church--Rosser theorem for the whole reduction system.
