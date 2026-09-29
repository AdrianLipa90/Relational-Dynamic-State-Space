# RTOFA Layer Architecture

The repository is intentionally split so that the general relational algebra is not contaminated by a particular geometric, phase, or physical realization.

## Layer 0 — Core algebra

`src/rdss/algebra.py`

Contains only representation-independent algebraic objects and diagnostics:

- `RelationalPoint`;
- `SemanticScale` and `SemanticScaleGraph`;
- `TensorScalarElement`;
- `TypedZero`;
- `TypedRelation`;
- commutator, associator, and generic refinement residual.

The core contains no CP1 state, Bloch/Fubini-Study object, scalar-angle Moiré coordinate, U(1) winding, Zero Axis coordinate, spacetime, or physical law.

## Layer 1 — Structural operators and coherence

`src/rdss/operations.py`

Contains typed executable operators:

[
star_R,quad
otimes,quad
operatorname{Contr},quad
T_r,quad
U_g,quad
S_{sigma	o	au},quad
F_pm,
]

together with residual diagnostics for their algebraic laws and naturality squares.

The rule is:

[
oxed{	ext{structure preservation is measured, not presumed}.}
]

## Layer 2 — Foundational logic

`src/rdss/axioms.py`, `src/rdss/closure.py`, `src/rdss/witnesses.py`

Separates axioms, definitions, structural primitives, derived constructions, reference realizations, bridges, candidate axioms, and theorems.

The current canonical foundational set is

[
mathrm{RA0}+mathrm{RR1}.
]

(mathrm{RA0}^{*}) remains a stronger candidate closure statement.

## Layer 3 — Generic phase representation

`src/rdss/phase.py`

Contains representation-level U(1) utilities:

- principal phase wrapping;
- turn count plus residual;
- closed-path winding.

These are not coordinates of the core algebra.

## Layer 4 — Reference realizations

`src/rdss/realizations.py`

Contains concrete realizations that may represent parts of the core:

- `CP1State`;
- Fubini-Study `MinimalDistinction`;
- fibre-local recursive CP1 realization;
- scalar-angle `MoireRotation`;
- explicit closed-holonomy-to-U(1) representation interface.

A reference realization is executable and tested but is not thereby a theorem forced by the core axioms.

## Layer 5 — Zero Axis bridge

`src/rdss/zero_axis.py`

Contains the finite Zero Axis point

[
s=rac12+it
]

and its projective coordinate

[
Omega(s)=rac{s}{1-s}.
]

The critical-axis/unit-circle identity belongs to the companion Zero Axis bridge, not to the primitive RTOFA signature.

## Public API

`src/rdss/__init__.py` re-exports stable user-facing names from all layers for convenience. Re-export does not change epistemic ownership: a symbol exported by `rdss` may still belong to a realization or bridge layer rather than the core.

## Promotion invariant

Any promoted structure must be synchronized across:

[
oxed{
	ext{definition}
+
	ext{implementation}
+
	ext{test}
+
	ext{LaTeX}
}
]

and its epistemic role must remain explicit.
