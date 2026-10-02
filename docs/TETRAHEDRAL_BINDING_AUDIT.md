# Tetrahedral binding audit

Status: exact downstream geometric closure; upstream/physical binding not closed.

## Object

The already-derived durable-role operator algebra has Frobenius-orthonormal
basis

[
mathcal B_H={I,S,P,J},
qquad J=SP,
]

with semantic split

[
mathcal B_H={I}sqcup{S,P,J}.
]

No new operator, integer coefficient or length scale is introduced.

## Exact regular tetrahedron

Treat the four orthonormal basis elements as four points in the real operator
space. For distinct basis points (E_a,E_b),

[
|E_a-E_b|_F^2
=
|E_a|_F^2+|E_b|_F^2
-2(E_a,E_b)_F
=
1+1
=
2.
]

This is the exact Pythagorean step proposed in the audit. All six edges have
the same length (sqrt2), and the three edge vectors from any vertex are
linearly independent. Therefore the four points form a regular tetrahedron.

For centroid

[
C=rac{I+S+P+J}{4},
]

the centered Gram matrix is

[
G_C=
egin{pmatrix}
3/4&-1/4&-1/4&-1/4\
-1/4&3/4&-1/4&-1/4\
-1/4&-1/4&3/4&-1/4\
-1/4&-1/4&-1/4&3/4
end{pmatrix}.
]

Hence normalized distinct vertices satisfy

[
widehat v_icdotwidehat v_j=-rac13.
]

The edge Gram matrix from the identity vertex is

[
G_E=
egin{pmatrix}
2&1&1\
1&2&1\
1&1&2
end{pmatrix},
qquad
det G_E=4.
]

Thus the exact induced tetrahedral volume is

[
V=rac{sqrt{det G_E}}{3!}=rac13.
]

## Exact Stella isometry

The existing positive-parity Stella tetrahedron uses

[
(1,1,1),quad
(1,-1,-1),quad
(-1,1,-1),quad
(-1,-1,1).
]

After scaling by (1/2), its Gram matrix is exactly (G_C). Therefore the
centered operator tetrahedron and the existing Stella tetrahedron are
isometric up to vertex permutation.

This is a non-numerical exact equality of Gram matrices.

## Exact Klein-four 1-2-3 signature

The positive-parity Stella vertices are closed under componentwise sign
multiplication. The vertex ((1,1,1)) is the unique identity and the other
three vertices square to it. Therefore the sign-coordinate tetrahedron is

[
T_+cong V_4congmathbb Z_2	imesmathbb Z_2.
]

It carries the exact signature

[
1 	ext{identity},
qquad
3 	ext{non-identity elements},
qquad
operatorname{ord}(g)=2 	ext{for every }g
e e.
]

This is a genuine (1,2,3) geometric/sign binding. It must not be confused
with an algebra isomorphism to the Hamlet operator product: in the operator
algebra (J^2=-I), whereas every non-identity element of the sign-coordinate
(V_4) has square (+1).

## The 1+3 split and 3n+1

The tetrahedron carries the already-derived semantic partition

[
{I}sqcup{S,P,J}.
]

Therefore for a finite carrier set (X),

[
left|
(X	imes{S,P,J})sqcup{I}
ight|
=
3|X|+1.
]

Under the existing canonical dissociation-plus-repair semantics, this is
exactly the odd affine Collatz cardinality.

The tetrahedral calculation therefore gives an exact geometric realization of

[
1oplus3
]

and of the already-derived (3n+1) count.

## Verdict

### PASS

- Pythagorean edge identity: exact.
- Regular tetrahedron from ({I,S,P,J}): exact.
- One identity plus three active vertices: exact.
- Isometry to the existing positive Stella tetrahedron: exact.
- Tetrahedral completion cardinality (3n+1): exact under the existing
  active-sector plus identity-restoration semantics.

### DOES NOT CLOSE THE UPSTREAM GATES

The tetrahedron is downstream of the durable relation-role algebra and the
Frobenius normalization. Therefore using it to derive the earlier
Hamlet-to-relation binding would be circular.

Likewise, the equality

[
|(X	imes{S,P,J})sqcup{I}|=3|X|+1
]

does not by itself prove that primitive natural dynamics must instantiate this
completion. It geometrizes the already-derived operation semantics but does
not supply the missing independent physical/foundational selection principle.

So this route is **correct and useful**, but it is a closure/crosscheck of the
coefficient geometry rather than a complete solution of the primitive-dynamics
binding gate.

## Machine surfaces

- `src/rdss/tetrahedral_binding.py`
- `tests/test_tetrahedral_binding.py`
- claim ledger nodes:
  - `DEF_HAMLET_OPERATOR_BASIS_SIMPLEX`
  - `THM_HAMLET_OPERATOR_BASIS_REGULAR_TETRAHEDRON`
  - `THM_HAMLET_OPERATOR_TETRAHEDRON_VOLUME`
  - `THM_HAMLET_OPERATOR_TETRAHEDRON_STELLA_ISOMETRY`
  - `THM_TETRAHEDRAL_ONE_PLUS_THREE_SPLIT`
  - `THM_TETRAHEDRAL_COMPLETION_CARDINALITY_3N_PLUS_1`
  - `THM_TETRAHEDRAL_GEOMETRY_MATCHES_COLLATZ_ODD_CARDINALITY`
  - `THM_TETRAHEDRAL_BINDING_IS_DOWNSTREAM_NOT_UPSTREAM_CLOSURE`
