# Relational Admissibility Reduction Gate

## Status

**OPEN by design.**

Historically this gate treated

\[
\operatorname{Adm}
\]

as a primitive predicate and kept RA0 as a separate object-level assumption.
The current claim ledger instead has exactly one axiom, \(A_0\), and
classifies RA0 as a derivation gate. META0 is the downstream model-formation
rule. The countermodel below is retained because it still proves that META0
alone does not force relational incidence.

## Countermodel: META0 non-vacuity without RA0

Take a finite raw presentation with one carrier

\[
P=\{a\},
\qquad
\operatorname{Adm}=\{a\},
\qquad
R=\varnothing.
\]

The admitted carrier domain is non-empty, so the executable non-vacuity component of META0 is satisfied.

But

\[
a
\]

is incident to no primitive relation. Hence RA0 fails.

Therefore, when \(\operatorname{Adm}\) is primitive,

\[
\boxed{
\mathrm{META0}
\not\Rightarrow
\mathrm{RA0}.
}
\]

This is an important independence result: non-vacuity is not relationality.

## Historical route A — primitive admissibility

Keep

\[
\operatorname{Adm}(x)
\]

primitive and retain

\[
\boxed{
\mathrm{RA0}:
\operatorname{Adm}(x)
\Rightarrow
\exists y,r\,
\left(
\operatorname{Rel}_r(x,y)
\lor
\operatorname{Rel}_r(y,x)
\right)
}
\]

as a primitive relational-admissibility derivation gate.

In the current ledger this route does not alter the unique foundation:

\[
\boxed{
A_0
\Longrightarrow
\mathrm{META0}
\Longrightarrow
\text{explicit derivation gates}.
}
\]

This route preserves the ability to talk about admitted carriers before imposing relational incidence.

## Alternative route B — define admissibility relationally

Instead define a relational admissibility predicate by

\[
\boxed{
\operatorname{Adm}_{R}(x)
:\Longleftrightarrow
\exists y,r\,
\left(
\operatorname{Rel}_r(x,y)
\lor
\operatorname{Rel}_r(y,x)
\right).
}
\]

Under this definition,

\[
\operatorname{Adm}_{R}(x)
\Rightarrow
\exists y,r\,
\left(
\operatorname{Rel}_r(x,y)
\lor
\operatorname{Rel}_r(y,x)
\right)
\]

is true by definitional expansion. RA0 would no longer be an independent axiom.

This can discharge the RA0 derivation gate by definition. It does not change
the axiom count: \(A_0\) remains the unique axiom, while RR1/RA0* remain
downstream derivation targets.

## Cost of route B

Route B is not a free theorem. It changes the meaning of the language.

It makes the following statement constitutive:

\[
\boxed{
\text{to be admitted}
=
\text{to be relationally incident}.
}
\]

Consequently:

- an isolated carrier cannot be admitted by definition;
- admissibility can no longer vary independently of the relation graph;
- the orientation of primitive arrows remains irrelevant to objecthood because incidence uses source **or** target;
- any later semantics requiring admitted but temporarily relation-free carriers would need a different predicate.

Thus route B is a genuine definitional reduction, not a proof of old RA0 from META0.

## Promotion condition

RA0 may be demoted from AXIOM to THEOREM/DEFINITION only if the project explicitly accepts relationally defined admissibility as the intended semantics of \(\operatorname{Adm}\).

Until then:

\[
\boxed{
\mathrm{META0}
\triangleright
(\mathrm{RA0}+\mathrm{RR1})
}
\]

remains canonical.

## Why this matters

The reduction programme now separates three logically distinct claims:

\[
\text{non-vacuity},
\qquad
\text{relational admissibility},
\qquad
\text{recursive closure}.
\]

They must not be merged by rhetoric.

The current executable witnesses establish:

\[
\mathrm{META0}\not\Rightarrow\mathrm{RA0},
\]

\[
\mathrm{RA0}\not\Rightarrow\mathrm{RR1},
\]

and

\[
\mathrm{RR1}\not\Rightarrow\mathrm{RA0}.
\]

Only an explicit definitional or strengthened-axiom change may collapse those layers.
