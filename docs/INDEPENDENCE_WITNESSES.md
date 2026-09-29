# Finite independence witnesses

The dependency ledger is supplemented by explicit finite models.

## W1: RA0 without RR1

Carrier:
[
{a,b}.
]

Admitted points:
[
{a,b}.
]

Primitive relations:
[
a	o b,qquad b	o a.
]

No refinement map is supplied.

Therefore every admitted point participates as the source of a relation, so RA0 holds, while recursive relational closure RR1 fails.

Hence, in the current formal language,

[
oxed{mathrm{RA0}
otRightarrowmathrm{RR1}}.
]

## W2: RR1 without RA0

Carrier:
[
{a,b,q,a_-,a_+,b_-,b_+}.
]

Relations:
[
a	o b,qquad b	o a.
]

Refinements:
[
amapsto(a_-,a_+),qquad
bmapsto(b_-,b_+).
]

The additional admitted point (q) has no outgoing relation. Therefore RR1 holds on every primitive relation endpoint, while RA0 fails at (q).

Thus

[
oxed{mathrm{RR1}
otRightarrowmathrm{RA0}}.
]

## W3: RA0 + RR1 without CP1

Take the same finite binary relation/refinement structure but provide no complex amplitudes, no projective quotient, and no Fubini-Study metric.

Both RA0 and RR1 hold. The CP1 layer is absent.

Therefore

[
oxed{mathrm{RA0}+mathrm{RR1}
otRightarrow CP^1}.
]

This establishes why CP1 is classified as a **reference realization**, not as a foundational axiom or a theorem of RA0+RR1.

## Scope of these witnesses

These are finite model witnesses for the current formal statements only. They do not prove independence from every possible stronger reformulation of the relational axiom. If RA0 is strengthened later, the witness set must be rerun against the new statement.
