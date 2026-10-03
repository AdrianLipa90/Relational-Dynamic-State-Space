# Relational Admissibility — Historical Reduction Gate

## Status

**RESOLVED / SUPERSEDED AS A CANONICAL DERIVATION GATE.**

The historical countermodel in this document remains valid:

\[
mathrm{META0}
otRightarrowmathrm{RA0}.
\]

That fact is still important. Non-vacuity alone does not imply relational
incidence.

The current canonical RDSS foundation, however, no longer attempts to derive
RA0 from META0 alone. It explicitly imports the canonical TIR
relational-existence typing

\[
\boxed{
operatorname{Exist}(x)Longrightarrowexists R_x
}
\]

through `BRIDGE_TIR_RELATIONAL_EXISTENCE_TYPING`.

Consequently `RA0` is theorem-level closed under the sourced TIR/RDSS
foundation chain and is not an open derivation gate.

## Historical countermodel: META0 without relational incidence

Take

\[
P={a},
qquad
operatorname{Adm}={a},
qquad
R=\varnothing.
\]

The admitted carrier domain is non-empty, so the non-vacuity component of
META0 is satisfied, but (a) is incident to no primitive relation. Hence

\[
\boxed{
mathrm{META0}
otRightarrowmathrm{RA0}.
}
\]

The current theory retains this as an independence result. It prevents the
sourced relational-existence rule from being misreported as a theorem of
META0 or (A_0) alone.

## Canonical resolution

The active dependency is

\[
\boxed{
A_0
+
\text{sourced TIR relational-existence typing}
Longrightarrow
\text{relational witness}
Longrightarrow
mathrm{RA0}.
}
\]

The ledger nodes are:

- `BRIDGE_TIR_RELATIONAL_EXISTENCE_TYPING`;
- `THM_CANONICAL_EXISTENCE_FORCES_RELATIONAL_WITNESS`;
- historical id `RA0`, now theorem-level closed.

This route preserves proof hygiene:

- (A_0) remains the unique foundational law;
- META0 remains a model-formation rule;
- the relational-existence implication is explicitly sourced rather than
  silently attributed to non-vacuity;
- a bare singleton mathematical presentation remains a useful countermodel to
  the stronger unsourced implication.

## Historical alternative: relationally defined admissibility

One may alternatively define

\[
operatorname{Adm}_{R}(x)
:Longleftrightarrow
exists y,r,
\bigl(
operatorname{Rel}_r(x,y)
lor
operatorname{Rel}_r(y,x)
\bigr).
\]

Under that different language RA0 follows by definitional expansion. RDSS does
not need this reduction for its current canonical closure; it is retained as a
historical semantic option.

## Recursive refinement remains separate

The old independence statements

\[
mathrm{RA0}
otRightarrowmathrm{RR1},
qquad
mathrm{RR1}
otRightarrowmathrm{RA0}
\]

remain valid for the historical schemas. The current canonical theory does not
need a universal RR1 law: arbitrary selected finite refinement depth is
constructively available through

`THM_FINITE_RELATIONAL_REFINEMENT_AVAILABLE`,

while `RR1` is retained as a formation-rule identifier for stronger complete
recursive hosting.

Thus this historical gate is closed without conflating non-vacuity,
relationality and recursive refinement.
