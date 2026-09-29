# Relational Admissibility Reduction Gate

## Status

**OPEN by design.**

The current object-level foundation treats

\[
\operatorname{Adm}
\]

as a primitive predicate and keeps RA0 as an axiom.

META0 settles non-reification and model non-vacuity, but it does not by itself force relational incidence.

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

## Current route A — primitive admissibility

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

as an object-level axiom.

Then the canonical stratification remains

\[
\boxed{
\mathrm{META0}
\triangleright
(\mathrm{RA0}+\mathrm{RR1}).
}
\]

This route preserves the ability to talk about admitted carriers before imposing relational incidence.

## Candidate route B — define admissibility relationally

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

The object-level foundation could then reduce schematically to

\[
\mathrm{RR1}
\]

under META0, or to the stronger candidate RA0* if RA0* is chosen as the recursive closure principle.

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
