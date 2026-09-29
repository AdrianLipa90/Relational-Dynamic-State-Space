# RTOFA Axiom Audit

This document separates axioms, definitions, structural primitives, reference realizations, derived constructions, and imported bridges.

## Classification

| ID | Class | Statement | Direct dependencies |
|---|---|---|---|
| RA0 | AXIOM | An admitted observable is not independent of relation. | — |
| DEF_POINT | DEFINITION | The minimal algebraic carrier is an unscaled point. | RA0 |
| RR1 | AXIOM | A selected relational point may itself carry a further distinction. | RA0, DEF_POINT |
| REF_CP1 | REFERENCE REALIZATION | A minimal complex binary distinction may be represented by CP1 with Fubini–Study metric. | DEF_POINT |
| DEF_TS | DEFINITION | Tensor-scalar grading uses rank (p,q); scalars are rank (0,0). | RA0 |
| PRIM_SCALE | STRUCTURAL PRIMITIVE | Semantic scale is a typed partial-order/category-like structure. | RA0 |
| PRIM_ORBIT | STRUCTURAL PRIMITIVE | Admissible orbital actions U_g may act on algebra elements. | RA0 |
| DER_MOIRE | DERIVED | Relative Moiré action is M_ij = U_i U_j^{-1} where the inverse exists. | PRIM_ORBIT |
| DEF_REFINEMENT_RESIDUAL | DEFINITION | Delta_F measures failure of exact product preservation under refinement. | RR1 |
| ZA_BRIDGE | BRIDGE | The companion Zero Axis model supplies Omega(s)=s/(1-s) and the critical-axis/unit-circle equivalence. | — |
| DER_WINDING | DERIVED | Winding and phase residual come from closed phase paths. | ZA_BRIDGE |

## Independence conclusions

1. **RA0 does not imply CP1.** CP1 requires the additional choice of a complex two-channel projective realization. The general relational axiom can have non-CP1 models.
2. **RR1 is independent of RA0.** RA0 only requires relation; it does not force recursive refinement. Fractality therefore requires its own closure axiom.
3. **Tensor-scalar grading is a structural definition, not a consequence of RA0.**
4. **Semantic scale is independent of orbital structure.** A model may carry one without the other.
5. **Moiré is not primitive once orbital actions are admitted.** It is a relative action and should be derived.
6. **Winding is not primitive once a phase path is given.** It is a path invariant.
7. **Zero Axis is not an axiom of the general algebra.** It is an imported bridge from the companion Zero Axis model.
8. **Associativity, commutativity and exact refinement self-similarity remain open properties.** Their residuals are diagnostics.

## Minimal foundational set

The current minimal axiom set is therefore

[
oxed{mathrm{RA0}+mathrm{RR1}}
]

with all other objects either definitions, optional structural primitives, reference realizations, derived constructions, or bridges.

This is intentionally conservative: a later proof may reduce RR1 to a theorem of a stronger form of RA0, but the current kernel does not assume that result.
