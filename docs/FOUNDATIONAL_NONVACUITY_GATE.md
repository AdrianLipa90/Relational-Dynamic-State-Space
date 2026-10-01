# Foundational Non-Vacuity Boundary

## Status

**RESOLVED at the model-formation level by the unique axiom A0 through META0.**

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

## A0 and the META0 formation rule

RTOFA has one axiom, A0. Its model-theoretic non-reification consequence is recorded by the formation rule

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

META0 is not another axiom. It records a model-class consequence of A0; RA0 and RR1 are now explicit derivation gates rather than object-level axioms.

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

## Canonical one-axiom foundation

The foundational stratification is now

\[
\boxed{
A_0
\Longrightarrow
\mathrm{META0}
\Longrightarrow
\{\mathrm{EX0},\text{ explicit derivation gates}\}.
}
\]

Here:

- A0 is the unique axiom;
- META0 is a model-formation rule induced by A0;
- EX0 is a theorem of META0;
- RA0, RR1, RA0_STAR and RA0_REL_STAR are named derivation gates, not axioms.

The historical countermodels remain useful because they show that particular
old formalizations of admissibility or recursive closure do not follow merely
from weaker intermediate statements. They no longer justify adding another
axiom; instead they identify exactly where the derivation from A0 must be
strengthened.

## Meaning of “forced”

The word **forced** here has a precise scope.

A0 is the unique foundational commitment of RTOFA; META0 is its chosen model-formation realization. This is not claimed to be forced in every possible logical formalism. Logics with empty domains can be defined.

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
