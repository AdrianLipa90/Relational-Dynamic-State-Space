# RTOFA Axiom Closure Audit

## Question

Can the current two-axiom foundation

\[
\mathrm{RA0}+\mathrm{RR1}
\]

be reduced to one axiom without hiding RR1 inside a change of wording?

## Baseline result

No. The current RA0 is too weak.

RA0 says that an admitted observable is not independent of relation. The finite witness W1 already shows

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

## Why this is not a free proof from old RA0

RA0* is genuinely stronger than RA0. It adds three pieces of content:

1. the relation hosted by an admitted carrier is a non-degenerate distinction;
2. the primitive distinction is binary;
3. selected endpoint occurrences remain admitted carriers.

The closure theorem is valid because these clauses are explicit. Calling them "implicit" would hide assumptions.

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

Current canonical status:

\[
\boxed{
\mathrm{RA0}+\mathrm{RR1}
}
\]

Candidate reduced status:

\[
\boxed{
\mathrm{RA0}^{*}
}
\]

with

\[
\mathrm{RR1}
\quad\text{demoted to}\quad
\mathrm{THM\_RR1\_FROM\_RA0\_STAR}.
\]

Do not promote RA0* merely because it is shorter. Promotion is justified only if its stronger wording is accepted as the intended meaning of the foundational relational principle.
