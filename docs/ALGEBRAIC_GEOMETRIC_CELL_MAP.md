# Algebraic-geometric cell map

Status: **formal reference construction on the RDSS branch**.

This document records only the structure agreed for the current dry
formalization. It does not introduce additional axioms.

## Foundation contract

RDSS is being migrated to a one-axiom foundation. The intended unique
foundational axiom is the non-realizability of absolute nothingness without
relation. Every other item is either a definition, an already sourced
derivation, a reference realization, or an explicitly open derivation gate.

The public TIR repository may be used as a read-only reference source. RDSS may
import verified consequences from it. This document does not authorize writes
to TIR.

## Dependency map

The current target map is

[
A_0
Rightarrow
	ext{distinction}
Rightarrow
(p_+,p_-)
Rightarrow
R(p_+,p_-)
Rightarrow
mathbb C,pi
Rightarrow
U(1)
Rightarrow
mathbb{CP}^1
Rightarrow
s=rac12
Rightarrow
	ext{polarization}
Rightarrow
(T_+,T_-)
Rightarrow
	ext{closed local cell}.
]

Where a dependency is not yet proved inside RDSS, it must remain an explicit
derivation gate rather than being promoted to another axiom.

## Local geometry

The minimal regular 3D simplex is the tetrahedron. The two relational poles
are represented by an oppositely polarized tetrahedral pair

[
T_+(t),qquad T_-(t).
]

The tetrahedra are the **dynamic** degrees of freedom.

Their local cage is a **static octahedral frame**

[
O_n=mathrm{const}.
]

The implementation deliberately stores the octahedron only as a six-vertex,
eight-face combinatorial frame. No coordinate embedding of the tetrahedral
vertices into that frame is imposed until it is derived.

A local cell is therefore represented as

[
oxed{
mathcal C_n(t)
=
igl(
O_n;
T_{+,n}(t),
T_{-,n}(t)
igr).
}
]

The dynamic tetrahedra carry opposite polarization, local (U(1)) phase and
angular state. Their reference spin sector is (s=1/2), with the symbolic
spinorial closure

[
2pimapsto -1,
qquad
4pimapsto +1.
]

## Static gluing

Neighbouring static frames are related face-to-face:

[
F_{n,a}sim F_{m,b}.
]

The executable object is a **face-adjacency complex**. It intentionally does
not claim that congruent regular octahedra alone form a Euclidean
space-filling honeycomb. A concrete Euclidean realization is a separate gate.

This separation is essential:

[
oxed{
	ext{static topology}={O_n,	ext{ face adjacencies}},
}
]

while

[
oxed{
	ext{local dynamics}={T_{+,n}(t),T_{-,n}(t)}.
}
]

Changing phase, angular offset or polarization state of the dynamic sector
does not move the static octahedral frame.

## Information action

The local canonical information action is the existing RDSS constant

[
oxed{
kappa
=
rac{ln 2}{24pi}.
}
]

The executable construction binds each local cell to the existing
`KAPPA_PHI` value rather than defining a second constant.

## Open derivation gates

The following are deliberately **not** silently assumed:

1. the exact coordinate embedding of the dynamic tetrahedra in the octahedral
   cage;
2. the proof that the chosen octahedral adjacency complex has the intended
   geometric realization;
3. the exact neighbour-coupling law for tetrahedral phase/orientation;
4. the derivation of the moire field from those relative local states.

These gates are the next formal work. They are not new axioms.
