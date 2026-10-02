# Bipolar tetrahedral exchange binding

Status: exact selector-free structural closure inside the already-derived
bipolar tetrahedral carrier; physical flavour-sector identity remains a
separate bridge.

## Geometry first

A tetrahedron has four triangular faces, four vertices and six edges.

Let the positive Stella tetrahedron be

[
T_+={v_0,v_1,v_2,v_3},
]

with exact sign realization

[
(1,1,1),quad
(1,-1,-1),quad
(-1,1,-1),quad
(-1,-1,1).
]

The opposite-polarity tetrahedron is

[
T_-=-T_+.
]

Index face (F_i^pm) by the vertex opposite that face. For the positive
vertex (v_i),

[
v_icdot x=-1
quad	ext{on }F_i^+,
]

while

[
v_icdot x=+1
quad	ext{on }F_i^-.
]

Therefore central inversion

[
iota:xmapsto-x
]

forces the face pairing

[
oxed{
F_i^+longleftrightarrow F_i^-,
qquad i=0,1,2,3.
}
]

There are exactly four paired faces. No face can disappear from the bipolar
exchange carrier without adding a boundary or another external carrier.

## Three flavours

TIR already contains an exact three-label (C_3) family/flavour
representation crosswalk. RDSS imports only that abstract three-label carrier,
not the stronger physical temporal-to-flavour identification.

Let

[
mathcal F_3={f_0,f_1,f_2}.
]

Then the directed exchange-incidence set is

[
mathcal C
=
{+,-}
	imes
{F_0,F_1,F_2,F_3}
	imes
mathcal F_3.
]

Hence

[
oxed{
|mathcal C|
=
2cdot4cdot3
=
24.
}
]

Polarity reversal acts freely on (mathcal C), so the undirected exchange
quotient has

[
oxed{
|mathcal C/Z_2|
=
12.
}
]

This distinguishes 24 oriented incidences from 12 paired exchanges.

## No hidden channel selector

The polarity flip (Z_2), tetrahedral face action (A_4), and flavour cycle
(C_3) act transitively on the 24 directed incidences.

Therefore any normalized scalar channel weighting invariant under the full
structural exchange symmetry is unique:

[
oxed{
w_c=rac1{24}.
}
]

A non-uniform channel assignment requires additional structure that breaks the
declared symmetry.

## Why the active multiplier is three

The operator tetrahedron carries the exact split

[
{I,S,P,J}
=
{I}
sqcup
{S,P,J}.
]

Under tetrahedral self-duality, the identity label fixes one dual face and the
remaining three dual faces form one (C_3) orbit. The only subsets of this
active three-face set invariant under the (C_3) stabilizer are

[
arnothing
quad	ext{and}quad
{S,P,J}.
]

Thus a non-trivial selector-free exchange cannot choose one or two active
faces. It must use all three:

[
oxed{
Xlongmapsto X	imes{S,P,J},
qquad
|X|longmapsto3|X|.
}
]

This is the selection theorem that was missing from the earlier purely
cardinality-level Collatz closure.

## Why the repair is one

The identity-dual face is the single fixed face outside the active (C_3)
orbit. Minimal closure restores this unique identity channel once:

[
oxed{
X	imes{S,P,J}
longmapsto
(X	imes{S,P,J})sqcup{I}.
}
]

Therefore

[
oxed{
nlongmapsto3n+1.
}
]

Choosing more than one closure token or choosing only a proper subset of the
three active channels requires additional non-canonical structure.

## Why association is two

The bipolar pair is related by the free polarity involution. Complete
association identifies the two members of each free (Z_2) orbit, therefore

[
oxed{
nlongmapstorac n2
}
]

whenever the carrier admits complete pairing, i.e. for even cardinality.

The selector-free operation roles are consequently

[
oxed{
2;:;	ext{bipolar }Z_2	ext{ association},
qquad
3;:;	ext{complete active }C_3	ext{ face orbit},
qquad
1;:;	ext{unique identity closure}.
}
]

Within the already-derived bipolar tetrahedral carrier this removes the affine
operation-role ansatz.

## The 24 / 12 phase crosscheck

The non-trivial (Z_2) polarity class is already embedded in (U(1)) as a
half-turn. Therefore one half-turn per directed incidence gives

[
24	imesrac12=12
]

normalized turns, equivalently

[
oxed{
Phi_{m total}=24pi.
}
]

This exactly reproduces the incidence count (24) and normalized turn measure
(12) already used by the canonical (kappa) reference chart.

It does not by itself prove that the entire structural (ln2) is represented
as a constant information density over that measure. The count/phase measure
is now geometrically closed; the information-density binding remains a
separate statement.

## What is actually closed

PASS:

- (T_-=-T_+) opposite polarity;
- all four faces paired by central inversion;
- three-label structural flavour carrier imported from the existing TIR
  (C_3) representation;
- 12 undirected face-flavour exchanges;
- 24 directed polarity-face-flavour incidences;
- transitivity of the structural channel symmetry;
- unique invariant channel weighting;
- selector-free active orbit has cardinality three;
- unique identity closure has cardinality one;
- free polarity quotient has cardinality two;
- resulting operation-role signature is (2,3,1);
- (3n+1) follows from complete active exchange plus minimal identity closure;
- (24) incidences and (12) half-turns reproduce the existing kappa
  denominator geometry.

Still separate:

- identifying the abstract three-label (C_3) carrier with a particular
  measured physical flavour sector;
- proving that a concrete physical system realizes the complete RDSS/TIR
  bipolar exchange carrier;
- promoting the constant information-density condition for (kappa) from
  reference normalization to theorem without an additional information
  conservation/equivariance argument.

## Executable surfaces

- `src/rdss/bipolar_tetrahedral_exchange.py`
- `tests/test_bipolar_tetrahedral_exchange.py`
- `src/rdss/axioms.py`
