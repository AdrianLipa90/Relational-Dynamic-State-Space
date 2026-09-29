# Non-Strict Monoidal Coherence Gate

## Status

**OPEN by design.**

The current RTOFA tensor layer can test a strict reference subclass:

\[
(X\otimes Y)\otimes Z
=
X\otimes(Y\otimes Z),
\]

explicit left/right units, and a supplied two-factor braiding candidate.

That is not yet a general non-strict monoidal structure.

## Missing structure

To state the pentagon and hexagon laws without ambiguity, a concrete realization must retain parenthesization and expose explicit isomorphisms

\[
\alpha_{X,Y,Z}:
(X\otimes Y)\otimes Z
\longrightarrow
X\otimes(Y\otimes Z),
\]

together with a braiding

\[
\beta_{X,Y}:
X\otimes Y
\longrightarrow
Y\otimes X.
\]

The current flattened \`TensorScalarElement\` does not remember the expression tree

\[
((X\otimes Y)\otimes Z)
\quad\text{versus}\quad
(X\otimes(Y\otimes Z)),
\]

because both are represented only by the resulting typed element.

## Pentagon gate

A non-strict associator must make the two canonical maps from

\[
(((W\otimes X)\otimes Y)\otimes Z)
\]

to

\[
W\otimes(X\otimes(Y\otimes Z))
\]

agree. The corresponding pentagon residual cannot be defined faithfully until the five parenthesized tensor objects and the relevant \(\alpha\)-maps are explicit.

## Hexagon gate

For a braided realization, the associator and braiding must satisfy the two hexagon coherence diagrams. Again, this requires explicit parenthesized source and target objects; a flat component tuple is insufficient.

## Promotion condition

This gate may be promoted only after the repository contains:

1. a parenthesized tensor-expression object;
2. explicit associator isomorphisms;
3. explicit braiding isomorphisms;
4. typed composition of those isomorphisms;
5. pentagon and hexagon residuals;
6. exact and broken finite witnesses;
7. synchronized LaTeX statements.

Until then, the implemented tensor sector is correctly described as a strict reference subclass with residual diagnostics, not a completed braided monoidal category.
