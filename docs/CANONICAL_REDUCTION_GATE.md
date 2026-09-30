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


## Explicit bridge registry

Semantic families remain incomparable until an explicit bridge is registered.

A bridge record contains

\[
B=
(
F_s,F_t,f,f^{-1},\rho,\eta,
\mathcal I,\mathcal C
),
\]

where \(F_s,F_t\) are source/target signature families, \(f\) is the forward
map, \(f^{-1}\) is optional, \(\rho\) is the semantic relation kind,
\(\eta\) is the information effect, \(\mathcal I\) is the preserved-invariant
set and \(\mathcal C\) is claim provenance.

Reverse routing exists only when \(f^{-1}\) is explicitly supplied.

A bridge declared LOSSLESS must pass an executable round-trip validator on
every value actually routed through it. Strict canonical equality is the
default:

\[
\mathcal N_0\!\left(f^{-1}(f(X))\right)
=
\mathcal N_0(X).
\]

A numerical bridge may instead supply an explicit validator when the
mathematical map is reversible but floating evaluation is not bitwise exact.
The validator is part of the bridge contract and is audited at route execution
time.

The current registry contains seven explicit bridges:

1. occurrence-address to reference-point coordinates:
   REFERENCE_REPRESENTATION + LOSSLESS;
2. finite U1Phase to finite ZeroAxisPoint:
   REFERENCE_REPRESENTATION + LOSSLESS on the domain u != -1;
3. TypedZero to the all-zero TensorScalarElement in the same sector:
   REFERENCE_REPRESENTATION + LOSSLESS;
4. RelationOccurrence to TypedRelation:
   FORGETFUL_PROJECTION + LOSSY;
5. OccurrenceRelationPath to RelationPath:
   FORGETFUL_PROJECTION + LOSSY;
6. RelationalBinaryDistinction to BinaryDistinction:
   FORGETFUL_PROJECTION + LOSSY;
7. RelationalGenerativeModel to GenerativeRelationModel:
   FORGETFUL_PROJECTION + LOSSY.

The occurrence/reference-point bridge is reversible as a reference coordinate
realization while preserving the semantic sort distinction

\[
\operatorname{OccurrenceAddress}
\not\equiv
\operatorname{RelationalPoint}.
\]

The four forgetful bridges have no reverse edge. The finite U1/Zero-Axis
bridge excludes u=-1 because that phase corresponds to the compactified point
at infinity rather than a finite ZeroAxisPoint.

Routing uses shortest explicit bridge paths. If multiple distinct shortest
routes reach the requested semantic family, routing fails closed as ambiguity.

Bridge comparison first transports one value into the semantic family of the
other and only then invokes signature comparison. LOSSY/UNKNOWN routes require
explicit opt-in.

## Bridge-aware equivalence graph

For a finite value set, the bridge registry and signature engine induce a
graph with two fundamentally different edge classes.

Strong edges are:

\[
\text{same-family semantic signature}
\quad\text{or}\quad
\text{fully reversible LOSSLESS bridge match}.
\]

Only strong edges generate union-find equivalence components.

Directed weak edges are:

\[
\text{LOSSY projection}
\quad\text{or}\quad
\text{UNKNOWN bridge}.
\]

They are recorded but never collapse components.

Therefore

\[
\boxed{
\text{LOSSY edge}
\not\Rightarrow
\text{equivalence-component union}.
}
\]

A component means equivalence under the currently selected lossless
signature/bridge policy. It is not promoted to ontological identity.

The graph reports unresolved cross-family pairs when no explicit bridge route
matches. These unresolved pairs are useful targets for later mathematics:
they show where a bridge theorem is still missing rather than silently
manufacturing one.


## Bridge gap report

Unresolved cross-family pairs are not discarded. They are grouped by unordered
semantic-family pair:

\[
G(F_i,F_j)
=
\{
(a,b):
\operatorname{family}(a)=F_i,\;
\operatorname{family}(b)=F_j,\;
\text{no registered matching bridge route}
\}.
\]

The report exposes

\[
\left(
N_{\rm family\ pairs},
N_{\rm unresolved\ record\ pairs}
\right)
\]

together with the concrete record ordinals in each family-pair gap.

This is a diagnostic of missing formal coverage. It does not assert

\[
\boxed{
\text{unresolved pair}
\not\Rightarrow
\text{bridge exists}.
}
\]

A gap can be resolved only by adding an explicit justified bridge, proving that
the families should remain distinct, or refining the signatures so that the
apparent gap is classified more accurately.


## Contextual bridge registry

Some transformations require information that is not carried by the source
value itself. These are not placed in the global bridge registry.

The contextual registry accepts an explicit context object at execution time:

\[
(X,C)\longmapsto Y.
\]

The first contextual bridge is

\[
\operatorname{BranchRelationOccurrence}
+
\operatorname{CarrierMapContext}
\longrightarrow
\operatorname{TypedRelation}.
\]

CarrierMapContext explicitly maps symbolic endpoint labels to RelationalPoint
values. The mapping is caller-supplied data and is not inferred from relation
labels or branch identity.

The transformation remains

\[
\boxed{
\mathrm{FORGETFUL\_PROJECTION}
+
\mathrm{LOSSY}
}
\]

because the branch occurrence slot is absent from TypedRelation. Indeed, two
branch occurrences with the same relation label and symbolic endpoints but
opposite branch slots materialize to the same TypedRelation under the same
context.

Contextual bridges are kept separate from the global BridgeRegistry so that
the absence of context cannot silently create a global equivalence edge.


## Executable bridge invariants

Bridge preservation claims are no longer only descriptive strings.

A global bridge may attach executable invariant records

\[
I_k=(p_k^{(s)},p_k^{(t)},\approx_k),
\]

where \(p_k^{(s)}\) and \(p_k^{(t)}\) project source and target values into the
quantity that should be preserved and \(\approx_k\) is an explicit comparator.

For every traversed edge the registry requires

\[
p_k^{(s)}(X)
\approx_k
p_k^{(t)}(B(X)).
\]

If any declared invariant fails, execution raises BridgeInvariantError and no
BridgeStep is returned.

The current seven global bridges have executable invariants covering:

- occurrence/reference binary coordinate word;
- finite U1/Zero-Axis projective correspondence;
- typed-zero rank, carrier, scale, dimension and additive-zero state;
- relation value under occurrence forgetting;
- admitted carriers and binary-distinction skeleton under relational-model
  forgetting;
- binary-distinction skeleton under relational-distinction forgetting;
- ordered relation values under occurrence-path forgetting.

Returned BridgeStep records contain the exact names of verified invariants.

Contextual bridges use the analogous typed form

\[
I_k=(p_k^{(s,c)},p_k^{(t)},\approx_k),
\]

where the source projection may depend on the explicit context \(C\).
BranchRelationOccurrence materialization currently verifies relation label,
resolved source carrier and resolved target carrier before returning a
ContextualBridgeStep.

The invariant engine is fail-closed. A descriptive preserves declaration never
overrides a failed executable invariant.


## Priority-free rewrite system

The rewrite layer represents explicit oriented transformations. Registering a
rule does not declare its target canonical.

A rule records

\[
R=
(
F_s,F_t,T,\rho,\eta,
\mathcal I,\mathcal C
),
\]

where \(F_s,F_t\) are semantic families, \(T\) is the oriented transform,
\(\rho\) is relation kind, \(\eta\) is information effect,
\(\mathcal I\) are executable invariants and \(\mathcal C\) is claim
provenance.

Automatic rewriting is priority-free:

\[
\#\operatorname{Applicable}(X)=
\begin{cases}
0 & \text{irreducible under the selected system},\\
1 & \text{automatic step admitted},\\
>1 & \text{AMBIGUOUS; fail closed}.
\end{cases}
\]

Registration order never selects between multiple applicable rules.

The current reference forgetful rewrite system is generated from the four
global FORGETFUL_PROJECTION bridges:

1. RelationOccurrence \(\to\) TypedRelation;
2. RelationalGenerativeModel \(\to\) GenerativeRelationModel;
3. RelationalBinaryDistinction \(\to\) BinaryDistinction;
4. OccurrenceRelationPath \(\to\) RelationPath.

The adapter reuses each bridge's LOSSY information effect, executable
invariants and claim provenance.

The current 36-record reference corpus contains five values to which exactly
one of these rules applies, 31 values irreducible under this selected subset,
and no multi-rule ambiguity in the source contract.

A rewrite trace records visited semantic-family/strict-value states. Repeating
a state raises RewriteCycleError rather than being mistaken for termination.

No confluence or global canonical-normal-form claim follows from this layer.


## Family-rank termination certificate

Termination is proved only for rewrite subsets carrying an explicit decreasing
measure.

A family-rank certificate supplies

\[
\mu:F\to\mathbb N.
\]

It is valid for a rewrite system exactly when every registered rule

\[
F_s\to F_t
\]

satisfies

\[
\mu(F_s)>\mu(F_t).
\]

Because \(\mathbb N\) has no infinite strictly descending chain, a verified
certificate excludes infinite rewrite traces for that selected system.

The current reference forgetful subsystem uses

\[
\mu=
\begin{cases}
1,&F\in\{
\text{relation_occurrence},
\text{relational_generative_model},
\text{relational_binary_distinction},
\text{occurrence_relation_path}
\},\\
0,&\text{otherwise}.
\end{cases}
\]

Every one of the four reference forgetful rules maps rank \(1\) to rank \(0\).
No reference forgetful rule originates at rank \(0\). Therefore

\[
\boxed{
L_{\rm trace}\le 1
}
\]

for every automatic trace in this subsystem.

This proves termination only for the selected reference forgetful rewrite
system. It does not prove termination for arbitrary future rewrite rules.


## Critical pairs and confluence certificate

A source-family overlap audit inspects unordered pairs of rewrite rules.
Rules with different declared source families cannot both apply to one admitted
value because every value has one semantic signature family.

Candidate overlap:

\[
R_i:F\to F_i,
\qquad
R_j:F\to F_j.
\]

For a concrete value \(X\) with two applicable rules the analyzer records the
critical pair

\[
R_i(X),
\qquad
R_j(X).
\]

The reference forgetful rewrite system has four rules with pairwise distinct
source families, therefore its source-family overlap audit is empty.

Hence every admitted value has at most one immediate rewrite successor:

\[
\boxed{
\#\operatorname{Succ}(X)\le 1.
}
\]

A deterministic rewrite relation is confluent. If

\[
X\to^*Y,
\qquad
X\to^*Z,
\]

both endpoints lie on the same unique successor orbit. Without loss of
generality the shorter path endpoint rewrites to the longer one, so the pair is
joinable.

Therefore the current reference forgetful system is confluent.

Combining this certificate with the family-rank termination certificate yields
a unique irreducible result for every admitted value under this selected
rewrite system.

This result is scoped:

\[
\boxed{
\text{unique irreducible under reference forgetful rewrite}
\neq
\text{global RDSS canonical normal form}.
}
\]


## Scoped rewrite normal form

Once one selected rewrite system has both a verified termination certificate
and a verified confluence certificate, it admits a unique irreducible result.

RDSS records that result together with its scope and certificate provenance:

\[
N_{\mathcal R}(X)
=
(
\text{scope},
\text{source key},
\text{target key},
\text{rewrite provenance},
\text{lossiness},
\text{termination certificate},
\text{confluence certificate}
).
\]

For the current reference subsystem the scope is

\[
\texttt{rdss-reference-forgetful-v1}.
\]

On the 36-record reference corpus:

- 5 values are rewritten through one LOSSY forgetful rule;
- 31 values are already irreducible;
- every result is irreducible under the selected system;
- reapplying the scoped normal form performs no further rewrite.

Thus

\[
N_{\mathcal R}(N_{\mathcal R}(X))
=
N_{\mathcal R}(X)
\]

at the strict target-key level.

The API explicitly reports

\[
\boxed{\texttt{global\_canonical}=\mathrm{False}}.
\]

This prevents the selected forgetful quotient from being silently promoted to a
global RDSS canonical normal form.


## Structure-state-representation factorization

RDSS now exposes the existing signature semantics as an explicit factorization

\[
\mathfrak F(X)
=
(F,S,\sigma,\rho),
\]

where:

- \(F\) is semantic family;
- \(S\) is the structural key built from every non-state signature axis;
- \(\sigma\) is the state key built from PHASE and STATE axes;
- \(\rho\) is the concrete representation tag.

No new quotient is introduced. The factorization is reconstructed directly from
RDSSSignature and therefore preserves

\[
S=\operatorname{structural\_key}(\Sigma(X)),
\]

\[
\sigma=\operatorname{state\_key}(\Sigma(X)),
\]

and

\[
(S,\sigma)=\operatorname{semantic\_key}(\Sigma(X)).
\]

Comparison proceeds in the order

\[
F
\rightarrow
S
\rightarrow
\sigma
\rightarrow
\rho.
\]

This yields the explicit classes:

\[
\{
\text{DIFFERENT\_FAMILY},
\text{DIFFERENT\_STRUCTURE},
\text{DIFFERENT\_STATE},
\text{REPRESENTATION\_ONLY},
\text{SAME\_FACTORIZATION}
\}.
\]

Important examples from the current reference model:

- changing TensorScalarElement components while rank/carrier/scale/dimension
  stay fixed is a state change;
- changing tensor rank is structural;
- a common angular shift of both MoireRotation angles leaves the same
  factorization because the relative phase is unchanged;
- CP1 global phase is currently represented as a state difference because no
  CP1 projective-phase quotient has yet been installed in the signature layer;
- OccurrenceAddress and RelationalPoint remain different families even when an
  explicit lossless reference bridge relates them.

The 36-record reference corpus source contract factors into

\[
(36,22,28,34,22)
\]

for records, families, structures, semantic states and representation classes.


## Claim provenance dependency graph

RDSS can now answer the provenance question

\[
\text{from which claims does this value or transformation follow?}
\]

without creating a second ledger.

Given explicit root claim IDs \(R\), the provenance layer returns the induced subgraph of the authoritative claim DAG:

\[
G_R=\operatorname{InducedDependencyGraph}(R).
\]

The graph is emitted in topological order: every dependency appears before the claim that depends on it.

For one admitted value the provenance bundle combines semantic factorization, signature extractor provenance, signature root claim IDs and the induced dependency graph.

Transformation provenance is also available for BridgeRoute, RewriteTrace and ScopedRewriteNormalForm. In each case the root claims are those already carried by the transformation; the provenance layer only expands their existing dependency closure.

It does not manufacture, promote, reclassify or rewrite claims. It is a read-only projection of the authoritative RDSS ledger.


## Object-level reduction certificate

A scoped normal form is now wrapped in an object-level reduction certificate
that binds the complete evidence chain for one input value.

For input \(X\), the certificate contains:

\[
\mathcal C(X)=
(\mathfrak F(X),G_X,T_X,N_{\mathcal R}(X),\mathfrak F(Y),G_Y,\mathcal I,G_{\mathcal C}),
\]

where \(Y\) is the selected-system irreducible result, \(G_X\) and \(G_Y\)
are value claim-provenance graphs, \(T_X\) is the certified rewrite trace,
\(\mathcal I\) is the inventory of executable invariants that passed, and
\(G_{\mathcal C}\) is the induced claim graph for the combined certificate.

The factory fails closed unless all of the following agree:

- strict source and target keys;
- complete source and target value provenance;
- rewrite rule provenance;
- scoped-normal-form provenance;
- termination and confluence certificate identities;
- lossiness;
- target irreducibility;
- scoped-normal-form idempotence;
- executable invariant inventory;
- authoritative claim dependency projection.

The certificate explicitly reports

\[
\boxed{\texttt{global\_canonical}=\mathrm{False}}.
\]

## Reference reduction-certificate scan

The reference batch scan applies the same certificate factory independently to
every named corpus value. The current source contract is:

\[
(36,36,5,31,5,0,22,18),
\]

for records, verified certificates, rewritten values, fixed points, LOSSY
reductions, global-canonical-true results, distinct source families and distinct
target families.

The deterministic CLI emits schema

rdss.reduction-certificate-scan/v1.

It exits non-zero if not every record verifies or if any result claims global
canonicality.
