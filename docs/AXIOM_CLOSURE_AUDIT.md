# RTOFA Axiom Closure Audit

## Question

Can the current two-axiom foundation

\[
\mathrm{RA0}+\mathrm{RR1}
\]

be reduced to one axiom without hiding RR1 inside a change of wording?

## Baseline result

No. The current RA0 is too weak.

RA0 says that an admitted observable is incident to at least one primitive relation, irrespective of arrow orientation. The finite witness W1 already shows

\[
\boxed{\mathrm{RA0}\not\Rightarrow\mathrm{RR1}}.
\]

A two-cycle may satisfy relational admissibility while carrying no explicit recursive distinction structure.

Therefore RR1 cannot be demoted under the current wording of RA0.

## Strengthened candidate RA0*

A stronger one-axiom candidate is:

\[
\boxed{
\mathrm{RA0}^{*}:
\text{every admitted carrier hosts at least one admitted non-degenerate binary distinction,}
}
\]

with the closure clause

\[
\boxed{
\text{the two selected endpoint occurrences are themselves admitted carriers.}
}
\]

The words "binary", "non-degenerate", "host", and "endpoint occurrence" are part of the formal content and must not be silently omitted.

## Occurrence-level non-degeneracy

The word **non-degenerate** refers to the two branch occurrences, not to inequality of carrier labels.

For a hosted occurrence \(p_\omega\), the binary distinction supplies two child slots

\[
p_{\omega-},
\qquad
p_{\omega+},
\]

with distinct path addresses

\[
\omega-\neq\omega+.
\]

It is therefore possible that

\[
\operatorname{carrier}(p_{\omega-})
=
\operatorname{carrier}(p_{\omega+})
\]

while the distinction remains binary at the occurrence level.

The minimal singleton presentation

\[
D(a)=(a,a)
\]

is consequently admissible as a binary occurrence distinction: the underlying carrier label repeats, but the left and right branch occurrences are different.

This is stronger than merely allowing cyclic presentations. It shows directly that recursive relational structure does not require two ontically distinct carrier labels at the first branching step.

RA0* does not require uniqueness of the distinction hosted by a carrier. A carrier may admit several valid binary distinctions. For a finite unfolding one may select one admissible witness at each occurrence; the executable reference kernel uses a deterministic lexicographic selector only so that repeated runs produce the same tree. That selector is an implementation convention, not additional axiomatic content.

## Closure theorem

Let \(p_{\omega}\) be a path-labelled relational occurrence with address

\[
\omega\in\{-1,+1\}^{n}.
\]

Assume RA0*. Since \(p_{\omega}\) is admitted, RA0* supplies a non-degenerate binary distinction

\[
D(p_{\omega})=
\left(
p_{\omega-},
p_{\omega+}
\right),
\]

and both endpoint occurrences are admitted.

By induction on \(n\), for every finite depth \(N\),

\[
\boxed{
V_n=\{-1,+1\}^{n},
\qquad 0\le n\le N,
}
\]

is generated as a complete binary refinement tree.

Hence, in the path-labelled occurrence semantics,

\[
\boxed{
\mathrm{RA0}^{*}\Rightarrow\mathrm{RR1}.
}
\]

RR1 can therefore be demoted to a theorem **only if RA0*** is promoted as the intended foundational axiom.

## Relationally bound one-axiom candidate

The current RA0* does not, by itself, prove RA0 because a hosted binary
distinction is represented separately from primitive relational incidence.

Introduce the stronger candidate

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}
}
\]

(code identifier RA0_REL_STAR) by requiring every admitted carrier to host
at least one **relationally bound** binary distinction. Such a distinction
contains branch-relation occurrences

\[
r_-:p_\omega\to p_{\omega-},
\qquad
r_+:p_\omega\to p_{\omega+},
\]

with admitted endpoint occurrences.

Then every admitted host has primitive relational incidence, so

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}
\Rightarrow
\mathrm{RA0}.
}
\]

The endpoint-admissibility and recursive hosted-distinction clauses also give,
by the same finite-depth induction,

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}
\Rightarrow
\mathrm{RR1}.
}
\]

Therefore

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}
\Rightarrow
\mathrm{RA0}+\mathrm{RR1}.
}
\]

This implication is strict in the expanded language. Take the singleton

\[
P=\{a\},
\qquad
R=\{(a,a)\},
\qquad
D(a)=(a,a),
\]

but supply no branch-slot-to-relation binding. Then META0, RA0, RA0*, and
recursive RR1 hold, while RA0_REL_STAR fails. Hence

\[
\boxed{
\mathrm{RA0}+\mathrm{RR1}
\not\Rightarrow
\mathrm{RA0}^{\mathrm{rel}*}.
}
\]

The one-object-level-axiom candidate therefore compresses the old pair by
adding genuine semantic structure; it is not equivalent to the old pair
without that added binding.

The singleton executable witness is

\[
a\xrightarrow{r_-}a,
\qquad
a\xrightarrow{r_+}a,
\]

where the two branch-relation occurrences are distinct by branch slot even
though source and target carrier labels coincide.

This candidate is strictly stronger in formal content than the current RA0*:
it adds the distinction-to-relation binding. It is executable but not
promoted.

See docs/RELATIONAL_DISTINCTION_BINDING_GATE.md.

## Why this is not a free proof from old RA0

RA0* is genuinely stronger than RA0. It adds three pieces of content:

1. the admitted carrier hosts a non-degenerate binary distinction at the occurrence/slot level;
2. the primitive distinction is binary;
3. selected endpoint occurrences remain admitted carriers.

The closure theorem is valid because these clauses are explicit. Calling them "implicit" would hide assumptions.

## Singleton occurrence witness

An even smaller witness uses one carrier label:

\[
D(a)=(a,a).
\]

The unfolding begins

\[
a_{\varnothing},
\qquad
a_{-},a_{+},
\qquad
a_{--},a_{-+},a_{+-},a_{++},
\quad\ldots
\]

Every node carries the same underlying label \(a\), but every path-labelled occurrence is distinct.

Thus

\[
\boxed{
\text{binary occurrence structure}
\not\Rightarrow
\text{binary carrier-label multiplicity}.
}
\]

## Cycles do not break recursive refinement

The underlying carrier presentation may be finite or cyclic. Example:

\[
D(a)=(a,b),
\qquad
D(b)=(a,b).
\]

The carrier labels repeat, but path-labelled occurrences do not:

\[
a_{\varnothing},
\quad
a_{-},b_{+},
\quad
a_{--},b_{-+},a_{+-},b_{++},
\quad \ldots
\]

Thus recursive relational structure does not require infinitely many distinct carrier labels.

## Ideal boundary of the occurrence tree

The actual occurrence addresses generated at finite depth form the countable set

\[
B^{<\omega}=\{-1,+1\}^{<\omega}.
\]

Its ideal boundary is defined separately as

\[
\boxed{
\partial V=B^\omega=\{-1,+1\}^{\mathbb N}.
}
\]

At depth \(n\), there are exactly \(2^n\) prefix cylinders. The boundary is in bijection with \(\mathcal P(\mathbb N)\), hence

\[
\boxed{
|\partial V|=2^{\aleph_0}.
}
\]

RR1 realizes every finite prefix of every \(\xi\in\partial V\), producing a coherent prefix chain. It does not assert convergence of that chain to an admitted infinite-address carrier.

Therefore the uncountability of \(\partial V\) is a property of the ideal path boundary, not a theorem that the carrier domain is uncountable.

## Novelty is a separate property

If the intended theory requires every refinement occurrence to introduce an ontically new carrier, then RA0* is still insufficient.

Define novelty schematically by

\[
p_{\omega}\neq p_{\nu}
\qquad
(\omega\neq\nu)
\]

at the carrier-identity level, not merely at the occurrence-address level.

The cyclic RA0* witness falsifies this condition while satisfying recursive closure. Therefore

\[
\boxed{
\mathrm{RA0}^{*}\not\Rightarrow\mathrm{NOVELTY}.
}
\]

A novelty requirement would need a separate axiom or a later theorem from additional structure.

## Status recommendation

Current canonical stratification:

\[
\boxed{
\mathrm{META0}
\;\triangleright\;
(\mathrm{RA0}+\mathrm{RR1})
}
\]

Candidate reduced object-level statuses:

\[
\boxed{
\mathrm{META0}
\;\triangleright\;
\mathrm{RA0}^{*}
}
\]

for recursive closure alone, and

\[
\boxed{
\mathrm{META0}
\;\triangleright\;
\mathrm{RA0}^{\mathrm{rel}*}
}
\]

for the stronger executable candidate that implies both RA0 and RR1.

with

\[
\mathrm{RR1}
\quad\text{demoted to}\quad
\mathrm{THM\_RR1\_FROM\_RA0\_STAR}.
\]

Do not promote RA0* merely because it is shorter. Promotion is justified only if its stronger wording is accepted as the intended meaning of the foundational relational principle.


## Non-vacuity semantics after META0

The closure formulas remain compatible with an empty **raw presentation**:

\[
\mathrm{RA0}+\mathrm{RR1}\not\vdash\mathrm{EX0},
\qquad
\mathrm{RA0}^{*}\not\vdash\mathrm{EX0}.
\]

This is a formula-level vacuity fact and remains useful for independence auditing.

It no longer means that the empty presentation belongs to the intended RTOFA model class. META0 imposes

\[
\mathfrak M\in\operatorname{Mod}(\mathrm{RTOFA})
\Longrightarrow
\operatorname{Adm}^{\mathfrak M}\neq\varnothing,
\]

so within the admissible model semantics

\[
\boxed{
\mathrm{META0}\models\mathrm{EX0}.
}
\]

Thus RA0* may collapse the object-level recursive closure assumption into one stronger relational rule, while META0 remains prior as a model-formation condition.

The empty raw presentation is retained only as a mathematical vacuity witness; it is not identified with absolute nothingness and is not an admissible RTOFA model.

