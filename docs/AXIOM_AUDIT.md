# RTOFA Axiom Audit

This audit separates **axioms**, **definitions**, **structural primitives**, **reference realizations**, **derived constructions**, and **imported bridges**. A dependency edge means "this construction explicitly uses that item"; it is not a claim that every item is logically derivable from the foundational axiom.

## Classification

| ID | Class | Statement | Direct dependencies |
|---|---|---|---|
| RA0 | AXIOM | An admitted observable is not independent of relation. | — |
| DEF_POINT | DEFINITION | The minimal algebraic carrier is an unscaled point. | — |
| DEF_BINARY_REL | DEFINITION | A primitive typed relation is binary: r:a->b. Higher arity is constructed separately. | — |
| RR1 | AXIOM | A selected relational endpoint may itself carry a further distinction. | DEF_POINT, DEF_BINARY_REL |
| RA0_STAR | CANDIDATE AXIOM | Every admitted carrier hosts an admitted non-degenerate binary distinction whose endpoint occurrences are admitted. | DEF_POINT, DEF_BINARY_REL |
| THM_RR1_FROM_RA0_STAR | THEOREM | RA0* generates recursive binary refinement to arbitrary finite depth by induction on path-labelled occurrences. | RA0_STAR |
| REF_CP1 | REFERENCE REALIZATION | A minimal complex binary distinction may be represented by CP1 with Fubini-Study metric. | DEF_POINT, DEF_BINARY_REL |
| PRIM_MODULE | STRUCTURAL PRIMITIVE | Each typed tensor-scalar sector carries an additive K-module structure; the reference kernel uses complex components. | — |
| DEF_TS | DEFINITION | Tensor-scalar grading uses rank (p,q); scalars are rank (0,0). | PRIM_MODULE |
| PRIM_PRODUCT | STRUCTURAL PRIMITIVE | A typed relational product star_R may be supplied without assuming associativity or commutativity. | — |
| PRIM_SCALE | STRUCTURAL PRIMITIVE | Semantic scale is a typed partial-order/category-like structure. | — |
| PRIM_ORBIT | STRUCTURAL PRIMITIVE | Admissible orbital actions U_g may act on algebra elements. | — |
| DER_MOIRE | DERIVED | Relative Moiré action is M_ij = U_i U_j^{-1} where the inverse exists. | PRIM_ORBIT |
| DEF_REFINEMENT_RESIDUAL | DEFINITION | Delta_F measures failure of exact product preservation under refinement. | RR1, PRIM_PRODUCT, PRIM_MODULE |
| ZA_BRIDGE | BRIDGE | The companion Zero Axis model supplies Omega(s)=s/(1-s) and the critical-axis/unit-circle equivalence. | — |
| DER_WINDING | DERIVED | Topological winding is derived only from a closed phase path with a continuous lift. | ZA_BRIDGE |

## Audit conclusions

1. **RA0 and RR1 are independent foundational assumptions in the current kernel.** RA0 requires relational admissibility; it does not force recursive refinement.
2. **Binary relation typing is explicit.** It is part of the signature rather than a hidden consequence of RA0.
3. **CP1 is not an axiom.** It is the chosen minimal complex binary projective realization. A non-CP1 model can still satisfy RA0 and RR1.
4. **The additive K-module structure, tensor-scalar grading, semantic scale, orbital action and relational product are signature choices/structural primitives.** They are not derived from RA0. The additive module is required before differences such as commutators, associators and refinement residuals are meaningful.
5. **Moiré is derived once invertible orbital actions are present.**
6. **Refinement residual requires both recursive refinement and a relational product.**
7. **Zero Axis is imported from the companion model.** It is not an axiom of the general algebra.
8. **A nonzero phase residual means the path is not closed.** A topological winding integer is asserted only after an explicit closure check.
9. **Associativity, commutativity and exact refinement self-similarity remain testable properties.**

## Minimal foundational axiom set

[
oxed{mathrm{RA0}+mathrm{RR1}}
]

This is a deliberately small axiom set. It does **not** mean that the rest of the signature follows from these two axioms; it means those other ingredients are typed definitions, independent structural primitives, realizations, derivations, or bridges.

## Open reduction target

A future theorem may show that a stronger formulation of relational admissibility forces recursive closure, in which case RR1 could be demoted from axiom to theorem. The current repository does not assume such a result.


## Closure-audit update

The one-axiom reduction has now been isolated precisely.

The old statement RA0 remains too weak:

\[
\mathrm{RA0}\not\Rightarrow\mathrm{RR1}.
\]

The strengthened candidate RA0* adds non-degenerate binary distinction and endpoint admissibility. Under those explicit clauses, recursive refinement is a theorem:

\[
\boxed{\mathrm{RA0}^{*}\Rightarrow\mathrm{RR1}}.
\]

This is not a free derivation from old RA0; it is a stronger foundational statement. The cyclic finite witness also shows

\[
\mathrm{RA0}^{*}\not\Rightarrow\mathrm{NOVELTY},
\]

so ontically fresh carrier identities at every refinement depth would require additional structure.

See `docs/AXIOM_CLOSURE_AUDIT.md`.
