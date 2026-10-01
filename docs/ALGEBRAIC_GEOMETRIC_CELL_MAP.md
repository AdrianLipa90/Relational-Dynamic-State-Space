# Algebraic-geometric cell map

Status: **formal reference construction on the RDSS branch**.

This document supersedes the earlier local picture in which the octahedron was
used as the external static cage. The corrected geometry uses a static cube,
the Stella Octangula as the two tetrahedral sectors on the cube vertices, and
the octahedron as the internal relational core.

No additional axioms are introduced.

## Foundation contract

RDSS enforces a one-axiom foundation. The unique foundational axiom is
\(A_0\). Every other item is a definition, theorem/derived result, reference
realization, bridge, structural primitive, or explicit derivation gate.

The public TIR repository is used as a **read-only reference source**. RDSS may
import verified formal consequences from TIR; this document does not authorize
writes to TIR.

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
\text{Stella Octangula}
\Rightarrow
\text{closed local cell}.
\]

The Euler--Berry spin/polarization step is imported through the read-only TIR
reference bridge
\`BRIDGE_TIR_EULER_BERRY_SPIN_HALF_POLARIZATION\`.

## Static cubic cage

The local static cage is the canonical cube

\[
Q_n=\mathrm{const}
\]

with vertex set

\[
V(Q_n)=\{(\pm1,\pm1,\pm1)\}.
\]

Thus

\[
|V(Q_n)|=8.
\]

These eight vertices are the static support geometry of the local cell.

## Stella Octangula as the vertex partition

The cube vertices split canonically into two parity classes:

\[
V_+
=
\{(x,y,z)\in V(Q_n):xyz=+1\},
\]

\[
V_-
=
\{(x,y,z)\in V(Q_n):xyz=-1\}.
\]

Each class contains four vertices:

\[
|V_+|=|V_-|=4,
\qquad
V_+\cap V_-=\varnothing,
\qquad
V_+\cup V_-=V(Q_n).
\]

Each support is a regular tetrahedron. In the canonical coordinates every
pair of distinct vertices within one support has squared distance

\[
d^2=8.
\]

Therefore the two complementary supports define the standard oppositely
oriented tetrahedral compound

\[
\boxed{
T_+\cup T_-=\text{Stella Octangula}.
}
\]

The key geometric correction is now explicit:

\[
\boxed{
V(T_+)\cup V(T_-)=V(Q_n).
}
\]

The Stella vertices are the cage vertices; there is no longer an open
coordinate-placement gate for these vertices.

## What is dynamic

The support geometry does not move.

The local dynamic variables belong to the two tetrahedral sectors:

\[
T_{+,n}(t),\qquad T_{-,n}(t),
\]

where time dependence refers to state variables such as local \(U(1)\) phase,
polarization/spin sector and angular state, not to motion of the cube
vertices.

Thus

\[
\boxed{
\text{static support}
=
Q_n
}
\]

while

\[
\boxed{
\text{dynamic state}
=
\{\phi_{\pm,n}(t),P_{\pm,n},\theta_{\pm,n}(t)\}.
}
\]

Through the TIR reference bridge,

\[
s=\frac12,
\qquad
2\pi\mapsto-1,
\qquad
4\pi\mapsto+1.
\]

## Internal octahedral relational core

For the standard cubic Stella embedding, the common central intersection of
the two tetrahedral solids is the regular octahedron

\[
O_n=T_{+,n}\cap T_{-,n}
\]

with canonical core vertices

\[
V(O_n)
=
\{
(\pm1,0,0),
(0,\pm1,0),
(0,0,\pm1)
\}.
\]

Therefore the octahedron is no longer the external cage. It is the internal
relational core:

\[
\boxed{
Q_n
\supset
(T_{+,n}\cup T_{-,n})
\supset
O_n.
}
\]

The structural roles are now:

\[
\boxed{
\text{cube}=\text{static cage / gluing support},
}
\]

\[
\boxed{
\text{Stella Octangula}=\text{two tetrahedral state sectors},
}
\]

\[
\boxed{
\text{octahedron}=\text{internal relational core}.
}
\]

## Local information cell

The corrected local cell is

\[
\boxed{
\mathcal C_n(t)
=
\bigl(
Q_n;
T_{+,n}(t),
T_{-,n}(t);
O_n
\bigr).
}
\]

The local canonical information action remains the existing RDSS value

\[
\boxed{
\kappa
=
\frac{\ln2}{24\pi}.
}
\]

The executable construction uses the existing \`KAPPA_PHI\`; no second
constant is introduced.

## Static gluing

Neighbouring cells are glued through static cube faces:

\[
F_{n,a}\sim F_{m,b}.
\]

The executable object is a cubic face-adjacency complex. Unlike the previous
octahedral-cage draft, the canonical cubic support also has the standard
Euclidean face-to-face lattice realization.

Local tetrahedral phase/spin/angular state does not move a shared cube face.

## Open derivation gates

The corrected geometry closes the previous vertex-embedding gate. The open
formal work is now downstream:

1. derive the neighbour-coupling law across a shared static cube face;
2. determine how relative tetrahedral phase/polarization/angular state is
   transported across that face;
3. derive the resulting moiré field from those relative states;
4. determine whether a higher-order dodecahedral/icosahedral organization
   emerges from the cubic-cell dynamics rather than being imposed locally.

These are derivation targets, not new axioms.

## Claim-ledger binding

The corrected map is registered as:

- \`DEF_STATIC_CUBIC_FRAME\` — definition;
- \`BRIDGE_TIR_EULER_BERRY_SPIN_HALF_POLARIZATION\` — read-only TIR bridge;
- \`DEF_STELLA_CUBIC_VERTEX_PARTITION\` — definition;
- \`DEF_DYNAMIC_TETRAHEDRAL_PAIR\` — definition;
- \`REF_STELLA_OCTANGULA_CUBIC_EMBEDDING\` — reference realization;
- \`REF_OCTAHEDRAL_RELATIONAL_CORE\` — reference realization;
- \`DEF_CUBIC_FACE_ADJACENCY_COMPLEX\` — definition;
- \`REF_ALGEBRAIC_GEOMETRIC_INFORMATION_CELL\` — reference realization;
- \`GATE_CELL_RELATIVE_STATE_TO_MOIRE\` — derivation gate.

The foundational axiom inventory remains exactly

\[
\boxed{\{A_0\}}.
\]
