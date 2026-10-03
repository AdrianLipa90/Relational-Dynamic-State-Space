# Non-Strict Monoidal Coherence Realization Boundary

Historical filename: `MONOIDAL_COHERENCE_GATE.md`.

## Status

**CLOSED BY INFORMATION-LOSS NO-GO / COHERENCE DATA REQUIRED FOR NON-STRICT REALIZATIONS.**

The current flat `TensorScalarElement` supports a strict reference subclass
and residual diagnostics. It does not retain the syntax tree needed to recover
a non-strict associator.

This is not an open derivation gate.

## Exact no-go witness

The parenthesized tensor expressions

\[
(((Wotimes X)otimes Y)otimes Z)
\]

and

\[
Wotimes(Xotimes(Yotimes Z))
\]

are distinct syntax trees, but flattening retains only the same ordered leaf
payload

\[
(W,X,Y,Z).
\]

Hence the flattening map is non-injective:

\[
\boxed{
\text{parenthesized tensor tree}
longrightarrow
\text{flat payload}
}
\]

loses exactly the information required to reconstruct an associator path.

Therefore the flat payload alone cannot force explicit maps

\[
alpha_{X,Y,Z}:
(Xotimes Y)otimes Z
\to
Xotimes(Yotimes Z)
\]

or the associated pentagon/hexagon data.

The theorem-level ledger node is

`THM_NONSTRICT_MONOIDAL_COHERENCE_UNDERDETERMINED_BY_FLATTENING`.

The executable witness is
`monoidal_coherence_underdetermination_certificate()`.

## Canonical interpretation

A non-strict braided monoidal realization may supply parenthesized objects,
associator and braiding isomorphisms, typed composition, and pentagon/hexagon
tests. The strict reference subclass remains valid without them.

Thus non-strict coherence is a realization extension, not a missing theorem
of the general RDSS algebra.
