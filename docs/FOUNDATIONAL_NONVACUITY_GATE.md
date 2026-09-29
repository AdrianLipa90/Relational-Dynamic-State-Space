# Foundational Non-Vacuity Gate

## Status

**OPEN by design.**

The current canonical foundation is

\[
\mathrm{RA0}+\mathrm{RR1}.
\]

Under the executable witness semantics, both statements are satisfied by the empty model because they constrain admitted relational carriers only if such carriers exist.

Therefore

\[
\boxed{
\mathrm{RA0}+\mathrm{RR1}
\not\Rightarrow
\mathrm{EX0},
}
\]

where the candidate non-vacuity statement is

\[
\boxed{
\mathrm{EX0}:
\exists p\;\operatorname{Adm}(p).
}
\]

## Why this matters

The motivating relational intuition contains two logically different claims:

1. an admitted observable is not independent of relation;
2. the intended theory is not the empty structure.

RA0 formalizes the first. It does not formalize the second.

RR1 also does not supply existence on its own: if there is no admitted relational occurrence, there is nothing to refine.

The strengthened closure candidate RA0* is likewise universally quantified over admitted carriers and is therefore vacuously true on the empty presentation.

## Empty witness

The finite model

\[
P=\varnothing,
\qquad
\operatorname{Adm}=\varnothing,
\qquad
R=\varnothing,
\qquad
F=\varnothing
\]

satisfies RA0 and RR1 vacuously while failing EX0.

This witness is executable in \`src/rdss/witnesses.py\`.

## Promotion choices

There are at least three clean options:

### Option A — separate non-vacuity axiom

Promote

\[
\mathrm{EX0}
\]

as a separate foundational axiom. The foundation becomes

\[
\mathrm{EX0}+\mathrm{RA0}+\mathrm{RR1}.
\]

### Option B — strengthen RA0

Redefine RA0 to include both non-vacuity and relational admissibility, for example schematically

\[
\exists p\,\operatorname{Adm}(p)
\quad\land\quad
\forall x\,
\bigl(
\operatorname{Adm}(x)
\Rightarrow
\exists y,r\,\operatorname{Rel}_r(x,y)
\bigr).
\]

This is a genuine strengthening and invalidates the old independence ledger unless all witnesses are rerun.

### Option C — treat non-vacuity as an external model-selection condition

Keep the algebraic axioms unchanged but explicitly restrict intended models to non-empty admitted carriers.

This is weaker as foundational bookkeeping because the non-vacuity condition then lives outside the formal axiom set.

## RA0* consequence

Even if RA0* is later promoted, non-vacuity remains separate unless RA0* itself is strengthened:

\[
\mathrm{RA0}^{*}
\not\Rightarrow
\mathrm{EX0}.
\]

RA0* says every admitted carrier has at least one admitted non-degenerate binary distinction. It does not assert that an admitted carrier exists.

## Current repository rule

EX0 is tracked as a **candidate axiom**, not silently promoted.

The canonical foundation remains

\[
\boxed{
\mathrm{RA0}+\mathrm{RR1}
}
\]

until the non-vacuity choice is made explicitly.
