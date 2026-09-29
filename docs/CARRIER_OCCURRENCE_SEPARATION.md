# Carrier Value / Occurrence Address Separation

## Status

**FOUNDATIONAL TYPE INVARIANT.**

RTOFA distinguishes two logically different objects:

\[
\boxed{
\text{carrier value } a
\quad\neq\quad
\text{occurrence address } \omega.
}
\]

The distinction is required for recursive models in which the same underlying carrier value may appear at many path-labelled occurrences.

## Carrier value

A carrier value answers:

> Which underlying relational carrier is represented?

In the executable algebraic kernel, typed tensor-scalar elements and typed relation values are attached to carrier/reference-coordinate values represented by RelationalPoint.

A primitive relation value has the form

\[
r:a\to b.
\]

Carrier-value equality is therefore about the endpoints of the relation value.

## Occurrence address

An occurrence address answers:

> At which branch-labelled occurrence of the recursive unfolding does this carrier value appear?

The canonical finite address space is

\[
B^{<\omega}
=
\{-1,+1\}^{<\omega}.
\]

The executable type is OccurrenceAddress.

For example,

\[
\omega=(-,+,-)
\]

is an occurrence address independently of which carrier value is attached to it.

## Repeated carriers

The same carrier value may occur at distinct addresses:

\[
\operatorname{carrier}(\omega_1)
=
\operatorname{carrier}(\omega_2)
=
a,
\qquad
\omega_1\neq\omega_2.
\]

The singleton recursive witness is the minimal example:

\[
a_{\varnothing},
\quad
a_-,
a_+,
\quad
a_{--},a_{-+},a_{+-},a_{++},
\ldots
\]

All occurrences carry the same value \(a\), but their occurrence addresses are different.

## Relation value versus relation occurrence

A relation value is

\[
r:a\to b.
\]

A relation occurrence is the triple

\[
\widetilde r
=
(r,\omega_{\rm src},\omega_{\rm dst}).
\]

Two distinct occurrences may therefore project to the same relation value:

\[
\widetilde r_1\neq\widetilde r_2,
\qquad
\pi(\widetilde r_1)
=
\pi(\widetilde r_2)
=
r.
\]

This projection is the reason carrier-value closure and occurrence closure are different notions.

## Closure

Value-level closure requires only

\[
a_m=a_0.
\]

Occurrence-level closure additionally requires

\[
\omega_m=\omega_0.
\]

Thus

\[
\boxed{
\text{occurrence-closed}
\Rightarrow
\text{carrier-closed}
}
\]

for a consistent occurrence-to-carrier assignment, while the converse is false.

The singleton refinement step

\[
a_{\varnothing}
\xrightarrow{r}
a_-
\]

is the minimal counterexample:

\[
a=a
\]

at the value level, but

\[
\varnothing\neq(-)
\]

at the occurrence level.

## Reference binary-coordinate embedding

Existing CP1/refinement realizations use a binary coordinate on RelationalPoint. To preserve compatibility while keeping the semantic sorts separate, the reference layer provides the explicit injection

\[
\boxed{
\iota:
B^{<\omega}
\hookrightarrow
P_{\rm ref},
\qquad
\iota(\omega)=p_\omega.
}
\]

In code this is reference_point_from_occurrence.

This is a **reference embedding**, not a type identity:

\[
\boxed{
\operatorname{OccurrenceAddress}
\not\equiv
\operatorname{RelationalPoint}.
}
\]

The binary coordinate stored by a reference RelationalPoint may numerically equal the tuple representing \(\omega\), but the two values belong to different semantic roles.

## Why this matters

Without this separation, a repeated carrier value can be mistaken for a repeated occurrence, producing false conclusions such as:

- a self-relation automatically forms an occurrence loop;
- carrier closure automatically implies branch-aware holonomy closure;
- recursive singleton refinement collapses after one step;
- relation-value cardinality equals relation-occurrence cardinality.

All four are false in the current formalism.

## Promotion invariant

Any new branch-aware construction must state explicitly whether it acts on:

1. carrier values;
2. occurrence addresses;
3. relation values;
4. relation occurrences.

A function that forgets one of these layers must expose that projection explicitly.

Silent identification of carrier values with occurrence addresses is forbidden.
