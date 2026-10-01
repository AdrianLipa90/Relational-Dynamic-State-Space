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

## Occurrence-to-relation-value projection

A branch-relation occurrence carries the slot as part of its identity:

\[
o=(\epsilon,r,s,t),
\qquad
\epsilon\in\{-1,+1\}.
\]

Forgetting only the occurrence slot gives the core typed relation value

\[
\boxed{
\pi_{\mathrm{rel}}:
(\epsilon,r,s,t)
\longmapsto
(s,t,r).
}
\]

The executable reference kernel materializes this through
\`BranchRelationOccurrence.as_typed_relation(...)\`.

The projection need not be injective. It is possible that

\[
o_-\neq o_+,
\]

while

\[
\pi_{\mathrm{rel}}(o_-)
=
\pi_{\mathrm{rel}}(o_+).
\]

For example,

\[
o_-=(-,r,a,a),
\qquad
o_+=(+,r,a,a)
\]

are distinct branch occurrences but represent the same underlying typed
relation value after forgetting the branch slot.

Thus RTOFA distinguishes:

\[
\boxed{
\text{relation occurrence}
\neq
\text{relation value}.
}
\]

This distinction is required for recursive branch structure and later
transport/holonomy bookkeeping.

## Explicit countermodel for old RA0*

The distinction-to-relation binding is not cosmetic.

Take

\[
P=\{a\},
\qquad
\operatorname{Adm}=\{a\},
\qquad
R=\varnothing,
\]

with hosted refinement

\[
a\mapsto(a,a).
\]

The current RA0* occurrence condition holds: the admitted carrier hosts a
binary occurrence distinction and both branch carrier labels are admitted.

But there is no primitive relation incident to \(a\). Therefore

\[
\boxed{
\mathrm{RA0}^{*}
\not\Rightarrow
\mathrm{RA0}.
}
\]

Because the admitted domain is non-empty, this is not a vacuity effect.

The historical RA0_REL_STAR strengthening exists precisely to add the missing
relation binding. In the current ledger it is a derivation gate, not an axiom.

## Historical strengthened derivation gate

The strengthened gate is:

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}:
\text{every admitted carrier hosts at least one admitted relationally bound binary distinction.}
}
\]

The endpoint occurrences are required to carry admitted carrier labels.

This is stronger than the current RA0* because it adds an explicit binding from distinction structure to primitive relational incidence.

## Forgetful projection to RA0*

A relationally bound distinction contains strictly more data than a plain
binary occurrence distinction. Forgetting only the explicit branch-relation
binding gives

\[
U:
\mathrm{RA0}^{\mathrm{rel}*}\text{-models}
\longrightarrow
\mathrm{RA0}^{*}\text{-models}.
\]

Concretely,

\[
U(r_-,r_+,p_\omega,p_{\omega-},p_{\omega+})
=
(p_\omega,p_{\omega-},p_{\omega+}),
\]

while preserving the admitted carrier set and the \((-),(+)\) occurrence
addresses.

The executable model implements this as \`as_ra0_star_model()\`.

Therefore

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}
\Rightarrow
\mathrm{RA0}^{*}.
}
\]

Combined with the existing closure theorem,

\[
\mathrm{RA0}^{*}\Rightarrow\mathrm{RR1},
\]

this gives an independent factorization of the RR1 implication.

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

This implication is stronger than required because the strengthened gate supplies outgoing incidence, while RA0 itself is orientation-neutral.

## RR1 theorem

The same strengthened gate supplies two branch occurrence slots whose endpoint carriers are admitted.

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

This provides a conditional compression of the historical RA0+RR1 pair.
It does not replace the current foundation. The current foundation remains

\[
\boxed{
A_0
\Longrightarrow
\mathrm{META0}
\Longrightarrow
\text{derived structure / explicit derivation gates}.
}
\]

RA0_REL_STAR is therefore a strengthened derivation gate, not a second axiom.

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

The strengthened gate therefore remains a conditional structure not forced by META0 or old RA0; it has no independent axiom status.

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

## Singleton cardinality theorem

The singleton conclusion has two separate ingredients.

First, META0 gives the lower bound

\[
\boxed{
|\operatorname{Adm}^{\mathfrak M}|\ge 1
}
\]

for every admissible RTOFA model.

Second, the executable singleton model

\[
a\xrightarrow{r_-}a,
\qquad
a\xrightarrow{r_+}a
\]

satisfies META0 and RA0_REL_STAR with

\[
|\operatorname{Adm}|=1.
\]

Therefore the lower bound is attained, and hence

\[
\boxed{
\min_{\mathfrak M\models\mathrm{META0}+\mathrm{RA0}^{\mathrm{rel}*}}
|\operatorname{Adm}^{\mathfrak M}|
=
1.
}
\]

The claim ledger separates these steps as:

- \`THM_META0_CARDINALITY_LOWER_BOUND\`;
- \`REF_SINGLETON_RA0_REL_STAR_MODEL\`;
- \`THM_SINGLETON_FOUNDATION_MINIMALITY\`.

This is a metatheoretic cardinality statement about the model class, not a claim that one physical object is sufficient for a physical universe.

## Minimal relation-occurrence cardinality

META0 plus RA0_REL_STAR imply that at least one admitted host exists. Every hosted relationally bound binary distinction contains the two branch slots

\[
(-),(+),
\]

so every such model has at least two branch-relation occurrences:

\[
\boxed{
|\operatorname{RelOcc}|\ge 2.
}
\]

The minimal singleton model attains that bound with

\[
o_-=(-,r,a,a),
\qquad
o_+=(+,r,a,a).
\]

Hence

\[
\boxed{
\min |\operatorname{RelOcc}|=2.
}
\]

Combining the exact carrier, relation-value, and relation-occurrence minima gives

\[
\boxed{
\left(
|\operatorname{Adm}|,
|\operatorname{RelVal}|,
|\operatorname{RelOcc}|
\right)
=
(1,1,2).
}
\]

This is a metatheoretic minimality statement for the candidate model class, not a physical particle claim.

## Strictness countermodel for RA0 + RR1

The converse implication also fails.

Take one admitted carrier label

\[
P=\{a\},
\qquad
\operatorname{Adm}=\{a\},
\]

with primitive self-relation

\[
R=\{(a,a)\}
\]

and recursive binary occurrence refinement

\[
D(a)=(a,a).
\]

This model satisfies META0 non-vacuity, orientation-neutral RA0, RA0*, and recursive RR1.

Now leave the branch slots unbound: there is no declared assignment

\[
(-)\mapsto o_-,
\qquad
(+)\mapsto o_+
\]

from the distinction slots to primitive relation occurrences.

Then RA0_REL_STAR fails even though RA0 and RR1 hold. Therefore

\[
\boxed{
\mathrm{RA0}+\mathrm{RR1}
\not\Rightarrow
\mathrm{RA0}^{\mathrm{rel}*}.
}
\]

Together with the forward implication,

\[
\mathrm{RA0}^{\mathrm{rel}*}
\Rightarrow
\mathrm{RA0}+\mathrm{RR1},
\]

this proves that the historical compression gate is a genuine strengthening in the expanded language. Under the current one-axiom ledger this affects conditional structure, not the axiom count.

## Derivation-closing condition

RA0_REL_STAR may discharge the historical RA0/RR1 closure package only if the project explicitly derives or accepts the following semantic identification:

\[
\boxed{
\text{hosted primitive distinction}
\Longrightarrow
\text{explicit primitive relational incidence}.
}
\]

Until that identification is closed, RA0_REL_STAR remains a derivation gate.
The canonical foundation remains

\[
\boxed{
A_0
\Longrightarrow
\mathrm{META0}
\Longrightarrow
\text{derived structure / explicit derivation gates}.
}
\]
