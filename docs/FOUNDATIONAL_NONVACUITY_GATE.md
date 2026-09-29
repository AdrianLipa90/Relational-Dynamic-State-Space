# Foundational Non-Vacuity Boundary

## Status

**RESOLVED at the model-formation level by META0.**

The previous version treated

\[
\mathrm{EX0}:\exists p\,\operatorname{Adm}(p)
\]

as a candidate object-level axiom. That bookkeeping is no longer used.

## The category distinction

Absolute nothingness cannot be represented by an object inside the theory. Giving it a symbol, carrier, state, value, or set would already reify it as something in the mathematical language.

In particular,

\[
\varnothing
\]

is **not** absolute nothingness. It is a mathematical object: the empty set.

Likewise, an empty first-order/finite presentation is still a mathematical structure. It may be used as a metamathematical witness, but it is not identified with absolute nothingness.

## META0 — formation meta-axiom

RTOFA therefore uses the model-formation rule

\[
\boxed{
\mathrm{META0}:
\begin{cases}
\text{absolute nothingness has no denotation in the RTOFA object language},\\[2mm]
\mathfrak M\in\operatorname{Mod}(\mathrm{RTOFA})
\Rightarrow
\operatorname{Adm}^{\mathfrak M}\neq\varnothing.
\end{cases}
}
\]

META0 is logically prior to the object-level relational axioms. It says what counts as an admissible model; it does not introduce a new object called “nothing.”

## EX0 becomes a theorem of the model class

For every admissible RTOFA model,

\[
\operatorname{Adm}^{\mathfrak M}\neq\varnothing,
\]

hence immediately

\[
\boxed{
\mathrm{EX0}:
\exists p\,\operatorname{Adm}(p).
}
\]

Thus, in the claim ledger,

\[
\boxed{
\mathrm{META0}\models\mathrm{EX0}.
}
\]

EX0 is therefore classified as a theorem of model-formation semantics, not as an additional ontological axiom.

## Why the empty raw presentation is still retained

Consider the raw mathematical presentation

\[
P=\varnothing,\qquad
\operatorname{Adm}=\varnothing,\qquad
R=\varnothing,\qquad
F=\varnothing.
\]

Universal object-level statements such as RA0, RR1, or RA0* may hold there vacuously.

Therefore, at the level of unrestricted formula semantics,

\[
\mathrm{RA0}+\mathrm{RR1}\not\vdash\mathrm{EX0},
\]

and similarly

\[
\mathrm{RA0}^{*}\not\vdash\mathrm{EX0}.
\]

This remains useful as an independence observation.

But the empty raw presentation fails META0 and therefore is excluded from

\[
\operatorname{Mod}(\mathrm{RTOFA}).
\]

There is no contradiction:

\[
\boxed{
\text{formula-level vacuity}
\neq
\text{admissible-model semantics}.
}
\]

## Canonical foundation after META0

The foundational stratification is now

\[
\boxed{
\mathrm{META0}
\;\triangleright\;
(\mathrm{RA0}+\mathrm{RR1}).
}
\]

Here:

- META0 is the model-formation meta-axiom;
- RA0 is relational admissibility inside an admitted model;
- RR1 is recursive relational closure;
- EX0 is a theorem of META0.

The stronger closure candidate RA0* remains separate:

\[
\mathrm{RA0}^{*}\Rightarrow\mathrm{RR1}
\]

under its explicit binary-distinction and endpoint-admissibility clauses.

META0 is still required at the model-class level; RA0* alone is universally quantified and can be vacuously true on an empty raw presentation.

## Meaning of “forced”

The word **forced** here has a precise scope.

META0 is not claimed to be a theorem of every possible logical formalism. Logics with empty domains can be defined.

Rather, META0 is constitutive of RTOFA semantics:

1. absolute nothingness is not an object-language denotation;
2. a mathematical structure purporting to instantiate RTOFA must contain at least one admitted carrier.

Once those semantic rules define the model class, EX0 is forced within that class.

This avoids both errors:

- reifying “nothing” as an object;
- silently obtaining existence from a universally quantified formula by rhetoric rather than formal semantics.

## Executable witness semantics

The reference kernel intentionally allows construction of an empty **raw presentation** so vacuous truth can be tested explicitly.

It exposes a separate model-admissibility check:

\[
\texttt{is\_admissible\_rtofa\_model()}
\]

which fails on the empty raw presentation and passes on non-empty presentations.

That separation is deliberate and should remain invariant.
