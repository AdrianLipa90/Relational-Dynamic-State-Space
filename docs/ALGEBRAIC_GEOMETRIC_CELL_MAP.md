# Algebraic-geometric cell map

Status: **formal reference construction on the RDSS branch**.

This document records only the structure agreed for the current dry
formalization. It does not introduce additional axioms.

## Foundation contract

RDSS now enforces a one-axiom foundation. The unique foundational axiom is
\(A_0\), the relational non-realizability of absolute nothingness. Every other
item is a definition, theorem/derived result, reference realization, bridge,
structural primitive, or an explicitly open derivation gate.

The public TIR repository is used as a **read-only reference source**. RDSS may
import verified formal consequences from TIR; this document does not authorize
writes to TIR.

Reference provenance for the spin/polarization bridge:
`The-Fundamental-Theory-of-Informational-Relations/TIR/foundations/TIR_CANONICAL_DERIVATION_SPINE_V0_1.md`,
Euler--Berry spin closure and polarization sections. The imported scope is
formal/symbolic; it is not promoted into a universal claim about physical spin.

## Dependency map

The current target map is

\[
A_0
\Rightarrow
\text{distinction}
\Rightarrow
(p_+,p_-)
\Rightarrow
R(p_+,p_-)
\Rightarrow
\mathbb C,\pi
\Rightarrow
U(1)
\Rightarrow
\mathbb{CP}^1
\Rightarrow
s=\frac12
\Rightarrow
\text{polarization}
\Rightarrow
(T_+,T_-)
\Rightarrow
\text{closed local cell}.
\]

Where a dependency is not proved directly inside RDSS but has public TIR
provenance, it is represented by a read-only bridge. Where neither a local
proof nor an imported reference closes the step, it remains an explicit
derivation gate rather than being promoted to another axiom.

## Local geometry

The minimal regular 3D simplex is the tetrahedron. The two relational poles
are represented by an oppositely polarized tetrahedral pair

\[
T_+(t),\qquad T_-(t).
\]

The tetrahedra are the **dynamic** degrees of freedom.

The standard regular two-tetrahedron compound is the Stella Octangula. In its
standard embedding, the common central intersection of the two tetrahedra is a
regular octahedron. RDSS records this as a reference realization; it does not
silently equate that standard coordinate embedding with the still abstract
dynamic cell implementation.

Their local cage is a **static octahedral frame**

\[
O_n=\mathrm{const}.
\]

The implementation deliberately stores the octahedron only as a six-vertex,
eight-face combinatorial frame. No coordinate binding of the dynamic
tetrahedral vertices to that frame is imposed until it is derived.

A local cell is therefore represented as

\[
\boxed{
\mathcal C_n(t)
=
\bigl(
O_n;
T_{+,n}(t),
T_{-,n}(t)
\bigr).
}
\]

The dynamic tetrahedra carry opposite polarization, local \(U(1)\) phase and
angular state. Through the read-only TIR Euler--Berry bridge, the reference
spin sector is

\[
s=\frac12,
\]

with the symbolic spinorial closure

\[
2\pi\mapsto -1,
\qquad
4\pi\mapsto +1.
\]

## Static gluing

Neighbouring static frames are related face-to-face:

\[
F_{n,a}\sim F_{m,b}.
\]

The executable object is a **face-adjacency complex**. It intentionally does
not claim that congruent regular octahedra alone form a Euclidean
space-filling honeycomb. A concrete Euclidean realization is a separate gate.

This separation is essential:

\[
\boxed{
\text{static topology}
=
\{O_n,\text{ face adjacencies}\},
}
\]

while

\[
\boxed{
\text{local dynamics}
=
\{T_{+,n}(t),T_{-,n}(t)\}.
}
\]

Changing phase, angular offset or polarization state of the dynamic sector
does not move the static octahedral frame.

## Information action

The local canonical information action is the existing RDSS constant

\[
\boxed{
\kappa
=
\frac{\ln 2}{24\pi}.
}
\]

The executable construction binds each local cell to the existing
`KAPPA_PHI` value rather than defining a second constant.

## Open derivation gates

The following are deliberately **not** silently assumed:

1. the exact coordinate binding of the dynamic tetrahedra to the chosen static
   octahedral frame;
2. the proof that the chosen octahedral face-adjacency complex has the intended
   global geometric realization;
3. the exact neighbour-coupling law for tetrahedral phase/orientation;
4. the derivation of the moiré field from those relative local states.

These gates are the next formal work. They are not new axioms.

## Claim-ledger binding

The executable map is registered without adding an axiom:

- `DEF_STATIC_OCTAHEDRAL_FRAME` — definition;
- `BRIDGE_TIR_EULER_BERRY_SPIN_HALF_POLARIZATION` — read-only TIR bridge;
- `DEF_DYNAMIC_TETRAHEDRAL_PAIR` — definition;
- `REF_STELLA_OCTANGULA_STANDARD_COMPOUND` — reference realization;
- `GATE_DYNAMIC_TETRAHEDRA_STATIC_FRAME_EMBEDDING` — derivation gate;
- `DEF_OCTAHEDRAL_FACE_ADJACENCY_COMPLEX` — definition;
- `REF_ALGEBRAIC_GEOMETRIC_INFORMATION_CELL` — reference realization;
- `GATE_CELL_RELATIVE_STATE_TO_MOIRE` — derivation gate.

The foundational axiom inventory remains exactly \(\{A_0\}\).
