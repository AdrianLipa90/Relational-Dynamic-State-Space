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

Therefore every admitted point is incident to a primitive relation, so RA0 holds, while recursive relational closure RR1 fails immediately.

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

The admitted point \(q\), however, is incident to no primitive relation. Therefore RA0 fails at \(q\).

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

but none of the descendant occurrences can refine does **not** satisfy recursive RR1 under the current witness semantics. The carrier labels attached to the two branch occurrences need not be different; failure here is failure of recursive continuation, not label equality.

This regression case is tested explicitly.

## Scope of these witnesses

These are finite model witnesses for the current formal statements only. They do not prove independence from every possible stronger reformulation of the relational axiom.

If RA0 or RR1 is strengthened later, the witness set must be rerun against the new statement.


## W4: formula-level RA0 + RR1 without EX0

Take the empty finite presentation

\[
P=\varnothing,
\qquad
\operatorname{Adm}=\varnothing,
\qquad
R=\varnothing,
\qquad
F=\varnothing.
\]

RA0 is satisfied vacuously because there is no admitted carrier that violates relational admissibility. RR1 is likewise satisfied vacuously because there is no relational occurrence that fails to refine.

EX0 fails:

\[
\neg\exists p\,\operatorname{Adm}(p).
\]

Therefore

\[
\boxed{
\mathrm{RA0}+\mathrm{RR1}
\not\Rightarrow
\mathrm{EX0}.
}
\]

This witness isolates formula-level non-vacuity from relational admissibility and recursive closure. Under META0, this empty presentation is **not** an admissible RTOFA model; it is retained only as a metamathematical vacuity witness.


## W5: META0 non-vacuity without RA0

Take

\[
P=\{a\},
\qquad
\operatorname{Adm}=\{a\},
\qquad
R=\varnothing.
\]

The admitted carrier domain is non-empty. Hence the executable non-vacuity component of META0 is satisfied.

However \(a\) is incident to no primitive relation, so RA0 fails.

Therefore, while \(\operatorname{Adm}\) remains a primitive predicate,

\[
\boxed{
\mathrm{META0}
\not\Rightarrow
\mathrm{RA0}.
}
\]

This is why non-vacuity and relational admissibility remain separate layers in the canonical foundation.

If admissibility is later **defined** relationally rather than treated as primitive, this witness no longer applies because the language itself has changed. That possible reduction is documented in \`docs/RELATIONAL_ADMISSIBILITY_REDUCTION_GATE.md\`.


## W6: singleton occurrence recursion

Take one carrier label

\[
P=\{a\},
\qquad
\operatorname{Adm}=\{a\},
\]

with the self-relation

\[
a\to a
\]

and recursive refinement

\[
a\mapsto(a,a).
\]

The two entries on the right are the left and right **occurrence slots**. Their path addresses are distinct even though both carry the same label \(a\).

Hence the unfolding is

\[
a_{\varnothing},
\qquad
a_-,a_+,
\qquad
a_{--},a_{-+},a_{+-},a_{++},
\quad\ldots
\]

The model satisfies META0 non-vacuity, RA0 relational incidence, and recursive RR1.

Therefore

\[
\boxed{
\text{recursive binary occurrence structure}
\not\Rightarrow
\text{two distinct carrier labels}.
}
\]

This witness is the finite discrete analogue of the distinction between one underlying carrier and two relational/polar slots.
