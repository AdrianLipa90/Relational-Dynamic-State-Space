# Bipolar tetrahedral exchange binding

Status: exact selector-free structural closure inside the already-derived
bipolar tetrahedral carrier; physical flavour-sector identity remains a
separate bridge.

## Geometry first

A tetrahedron has four triangular faces, four vertices and six edges.

Let the positive Stella tetrahedron be

\[
T_+={v_0,v_1,v_2,v_3},
\]

with exact sign realization

\[
(1,1,1),quad
(1,-1,-1),quad
(-1,1,-1),quad
(-1,-1,1).
\]

The opposite-polarity tetrahedron is

\[
T_-=-T_+.
\]

Index face (F_i^pm) by the vertex opposite that face. For the positive
vertex (v_i),

\[
v_icdot x=-1
quad\text{on }F_i^+,
\]

while

\[
v_icdot x=+1
quad\text{on }F_i^-.
\]

Therefore central inversion

\[
iota:xmapsto-x
\]

forces the face pairing

\[
\boxed{
F_i^+\longleftrightarrow F_i^-,
\qquad i=0,1,2,3.
}
\]

There are exactly four paired faces. No face can disappear from the bipolar
exchange carrier without adding a boundary or another external carrier.

## Three flavours

TIR already closes the three-flavour carrier itself:
\[
\boxed{N_F=3}.
\]
Its dependency surfaces explicitly record `THREE_FLAVOUR_CARRIER = CLOSED -> N_F=3`
and `TIR.FLAVOUR.STAGE66_SU3F_GENERATION = CLOSED`. RDSS therefore imports
three as a sourced TIR result, not as an abstract cardinality placeholder.
The distinct downstream `TIR.FLAVOUR.PHYSICAL_BINDING` gate concerns the
stronger physical sector/readout identification and is not required for the
face--flavour incidence count below.

Let

\[
\mathcal F_3={f_0,f_1,f_2}.
\]

Then the directed exchange-incidence set is

\[
\mathcal C
=
{+,-}
\times
{F_0,F_1,F_2,F_3}
\times
\mathcal F_3.
\]

Hence

\[
\boxed{
|\mathcal C|
=
2\cdot4\cdot3
=
24.
}
\]

Polarity reversal acts freely on \(\mathcal C\), so the undirected exchange
quotient has

\[
\boxed{
|\mathcal C/Z_2|
=
12.
}
\]

This distinguishes 24 oriented incidences from 12 paired exchanges.

## No hidden channel selector

The polarity flip (Z_2), tetrahedral face action (A_4), and flavour cycle
(C_3) act transitively on the 24 directed incidences.

Therefore any normalized scalar channel weighting invariant under the full
structural exchange symmetry is unique:

\[
\boxed{
w_c=\frac1{24}.
}
\]

A non-uniform channel assignment requires additional structure that breaks the
declared symmetry.

## Why the active multiplier is three

The operator tetrahedron carries the exact split

\[
{I,S,P,J}
=
{I}
\sqcup
{S,P,J}.
\]

Under tetrahedral self-duality, the identity label fixes one dual face and the
remaining three dual faces form one (C_3) orbit. The only subsets of this
active three-face set invariant under the (C_3) stabilizer are

\[
\varnothing
quad\text{and}quad
{S,P,J}.
\]

Thus a non-trivial selector-free exchange cannot choose one or two active
faces. It must use all three:

\[
\boxed{
Xlongmapsto X\times{S,P,J},
\qquad
|X|\longmapsto3|X|.
}
\]

This is the selection theorem that was missing from the earlier purely
cardinality-level Collatz closure.

## Why the repair is one

The identity-dual face is the single fixed face outside the active (C_3)
orbit. Minimal closure restores this unique identity channel once:

\[
\boxed{
X\times{S,P,J}
\longmapsto
(X\times{S,P,J})\sqcup{I}.
}
\]

Therefore

\[
\boxed{
nlongmapsto3n+1.
}
\]

Choosing more than one closure token or choosing only a proper subset of the
three active channels requires additional non-canonical structure.

## Why association is two

The bipolar pair is related by the free polarity involution. Complete
association identifies the two members of each free (Z_2) orbit, therefore

\[
\boxed{
nlongmapsto\frac n2
}
\]

whenever the carrier admits complete pairing, i.e. for even cardinality.

The selector-free operation roles are consequently

\[
\boxed{
2;:;\text{bipolar }Z_2\text{ association},
\qquad
3;:;\text{complete active }C_3\text{ face orbit},
\qquad
1;:;\text{unique identity closure}.
}
\]

Within the already-derived bipolar tetrahedral carrier this removes the affine
operation-role ansatz.

## The 24 / 12 phase crosscheck

The non-trivial (Z_2) polarity class is already embedded in (U(1)) as a
half-turn. Therefore one half-turn per directed incidence gives

\[
24\times\frac12=12
\]

normalized turns, equivalently

\[
\boxed{
\Phi_{\rm total}=24\pi.
}
\]

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
- three-flavour carrier (N_F=3) imported as a CLOSED TIR result;
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


## Provenance

Code comments use inline `# REF:` anchors.

- TIR three-flavour parent:
  commit `9783782570a2ccfa1fc42c99b605dad48e02aa78`,
  `TIR/foundations/TIR_COEFFICIENT_MAGNITUDE_PARENT_EVALUATION_V0_1.md`
  and `DEPENDENCY_EXPORT.json`.
- RDSS selector-free bipolar binding:
  commit `d6f80e4539db368f828a064c2ab0fff730ec3490`.
- RDSS corrected closed-flavour import:
  commit `7e947fee4b85192b35605a91bc35530891d88289`.
- RDSS theorem-level kappa claim ledger:
  commit `2fb4645a16074280494423f4b27bc7d3ff5bc092`.
- Shannon entropy source: C. E. Shannon, 1948.
