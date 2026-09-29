# Finite independence witnesses

The dependency ledger is supplemented by explicit finite models. These witnesses use finite cyclic presentations when necessary so recursive closure does not get confused with ontically new carrier labels.

## W1: RA0 without RR1

Carrier:

\[
\{a,b\}.
\]

Admitted points:

\[
\{a,b\}.
\]

Primitive relations:

\[
a\to b,
\qquad
b\to a.
\]

No refinement rule is supplied.

Therefore every admitted point is the source of a relation, so RA0 holds, while recursive relational closure RR1 fails immediately.

Hence, in the current formal language,

\[
\boxed{
\mathrm{RA0}\not\Rightarrow\mathrm{RR1}.
}
\]

## W2: RR1 without RA0

Use the finite carrier

\[
\{a,b,q\},
\]

with all three points admitted.

Primitive relations are

\[
a\to b,
\qquad
b\to a.
\]

Recursive refinements are given cyclically by

\[
a\mapsto(a,b),
\qquad
b\mapsto(a,b).
\]

Starting from either primitive relation endpoint, every reachable refinement descendant is again \(a\) or \(b\), and both have a supplied non-degenerate refinement. Thus RR1 is recursively closed.

The admitted point \(q\), however, has no outgoing primitive relation. Therefore RA0 fails at \(q\).

Hence

\[
\boxed{
\mathrm{RR1}\not\Rightarrow\mathrm{RA0}.
}
\]

The cyclic presentation is deliberate: RR1 concerns recursive relational closure, not novelty of carrier labels.

## W3: RA0 + RR1 without CP1

Use the finite carrier

\[
\{a,b\},
\]

with primitive relations

\[
a\to b,
\qquad
b\to a,
\]

and cyclic refinements

\[
a\mapsto(a,b),
\qquad
b\mapsto(a,b).
\]

Both RA0 and recursively closed RR1 hold.

Now provide no complex amplitudes, no projective quotient, no CP1 state, and no Fubini--Study metric. The projective realization is absent while the relational axioms still hold.

Therefore

\[
\boxed{
\mathrm{RA0}+\mathrm{RR1}
\not\Rightarrow
CP^1.
}
\]

This establishes why CP1 is classified as a **reference realization**, not as a foundational axiom or a theorem of RA0+RR1.

## One-level refinement is not RR1

A model in which

\[
a\mapsto(a_-,a_+),
\qquad
b\mapsto(b_-,b_+)
\]

but none of \(a_-,a_+,b_-,b_+\) can refine does **not** satisfy recursive RR1 under the current witness semantics.

This regression case is tested explicitly.

## Scope of these witnesses

These are finite model witnesses for the current formal statements only. They do not prove independence from every possible stronger reformulation of the relational axiom.

If RA0 or RR1 is strengthened later, the witness set must be rerun against the new statement.
