# Relational Distinction Binding Gate

## Status

**CANDIDATE REDUCTION — executable, not promoted.**

This gate separates two statements that must not be conflated.

The existing candidate

\[
\mathrm{RA0}^{*}
\]

asserts recursive hosted binary distinction structure. In the current language, a binary distinction is not automatically a primitive relation. Therefore RA0* supports the RR1 closure theorem but does not, by itself, prove RA0.

A stronger candidate is introduced:

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}.
}
\]

In the code ledger this is RA0_REL_STAR.

## Relationally bound binary distinction

A relationally bound distinction at occurrence \(p_\omega\) contains two branch-relation occurrences

\[
r_-:
p_\omega\to p_{\omega-},
\qquad
r_+:
p_\omega\to p_{\omega+}.
\]

The branch positions are distinct by occurrence address.

The underlying endpoint carrier labels may coincide:

\[
\operatorname{carrier}(p_{\omega-})
=
\operatorname{carrier}(p_{\omega+}).
\]

The branch relation occurrences may also share the same relation type or label in a more general realization; their occurrence identity is supplied by the branch slot. The reference executable witness uses explicit relation labels for clarity.

Thus the singleton case is legitimate:

\[
a
\xrightarrow{r_-}
a,
\qquad
a
\xrightarrow{r_+}
a.
\]

## Candidate axiom

The candidate is:

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}:
\text{every admitted carrier hosts at least one admitted relationally bound binary distinction.}
}
\]

The endpoint occurrences are required to carry admitted carrier labels.

This is stronger than the current RA0* because it adds an explicit binding from distinction structure to primitive relational incidence.

## RA0 theorem

Let \(p_\omega\) be admitted.

By \(\mathrm{RA0}^{\mathrm{rel}*}\), there exists at least one hosted relational distinction, hence at least one branch relation occurrence

\[
r_-:
p_\omega\to p_{\omega-}
\]

(and also \(r_+\)).

Therefore \(p_\omega\) is incident to a primitive relation.

Hence

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}
\Rightarrow
\mathrm{RA0}.
}
\]

This implication is stronger than required because the candidate supplies outgoing incidence, while RA0 itself is orientation-neutral.

## RR1 theorem

The same candidate supplies two branch occurrence slots whose endpoint carriers are admitted.

The rule therefore re-applies at every admitted child occurrence.

By induction on path length,

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}
\Rightarrow
\mathrm{RR1}
}
\]

at every finite refinement depth.

## Combined reduction

Consequently,

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}
\Rightarrow
\mathrm{RA0}+\mathrm{RR1}.
}
\]

With META0 retained as the model-formation rule, the candidate reduced foundation is

\[
\boxed{
\mathrm{META0}
\triangleright
\mathrm{RA0}^{\mathrm{rel}*}.
}
\]

This is a genuine one-object-level-axiom candidate.

## What has not been proved

The repository has **not** proved

\[
\mathrm{META0}
\Rightarrow
\mathrm{RA0}^{\mathrm{rel}*},
\]

nor

\[
\mathrm{RA0}
\Rightarrow
\mathrm{RA0}^{\mathrm{rel}*}.
\]

The candidate therefore remains a strengthening of the current object-level foundation, not a theorem forced by META0 or old RA0.

Likewise, no claim is made that every mathematical notion of distinction must be relation-bound in this exact manner.

## Executable reference witness

The reference kernel includes:

- RelationalBinaryDistinction;
- RelationalGenerativeModel;
- singleton_ra0_rel_star_model.

The singleton witness has one admitted carrier \(a\) and two branch-relation occurrences:

\[
(-,r_-,a,a),
\qquad
(+,r_+,a,a).
\]

It satisfies the executable candidate, RA0, and recursive RR1 to every tested finite depth.

## Promotion condition

RA0_REL_STAR may replace the current pair RA0+RR1 only if the project explicitly accepts the following semantic identification:

\[
\boxed{
\text{hosted primitive distinction}
\Longrightarrow
\text{explicit primitive relational incidence}.
}
\]

Until that identification is promoted, the canonical foundation remains

\[
\boxed{
\mathrm{META0}
\triangleright
(\mathrm{RA0}+\mathrm{RR1}).
}
\]
