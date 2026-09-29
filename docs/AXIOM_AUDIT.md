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
| REF_CP1_REFINEMENT | REFERENCE REALIZATION | Recursive refinement is realized as a tree of local CP1/FS fibres indexed by relational carriers. | REF_CP1, RR1 |
| PRIM_MODULE | STRUCTURAL PRIMITIVE | Each typed tensor-scalar sector carries an additive K-module structure; the reference kernel uses complex components. | — |
| DEF_TS | DEFINITION | Tensor-scalar grading uses rank (p,q); scalars are rank (0,0). | PRIM_MODULE |
| PRIM_PRODUCT | STRUCTURAL PRIMITIVE | A typed relational product star_R may be supplied without assuming associativity or commutativity. | — |
| PRIM_TENSOR_PRODUCT | STRUCTURAL PRIMITIVE | A typed tensor product combines compatible tensor-scalar sectors; component formulas belong to realizations. | PRIM_MODULE |
| PRIM_CONTRACTION | STRUCTURAL PRIMITIVE | A typed contraction lowers one covariant and one contravariant rank when a contraction rule is supplied. | PRIM_MODULE |
| DEF_BILINEARITY_RESIDUAL | DEFINITION | Bilinearity residuals measure failure of product additivity and scalar-linearity. | PRIM_PRODUCT, PRIM_MODULE |
| DEF_TENSOR_MAP_COHERENCE | DEFINITION | Measures monoidality of a supplied typed map with respect to tensor product. | PRIM_TENSOR_PRODUCT, PRIM_MODULE |
| DEF_TENSOR_MONOIDAL_COHERENCE | DEFINITION | Tests strict associativity, explicit unit, and supplied braiding by residuals. | PRIM_TENSOR_PRODUCT, PRIM_MODULE |
| DEF_CONTRACTION_MAP_COHERENCE | DEFINITION | Measures contraction naturality under a supplied typed map. | PRIM_CONTRACTION, PRIM_MODULE |
| PRIM_SCALE | STRUCTURAL PRIMITIVE | Semantic scale is a typed partial-order/category-like structure. | — |
| PRIM_TRANSPORT | STRUCTURAL PRIMITIVE | Typed transports T_r act along composable binary relations between carrier sectors. | DEF_BINARY_REL, PRIM_MODULE |
| DER_HOLONOMY | DERIVED | Relational holonomy is transport around a closed composable relation path, measured against the initial state. | PRIM_TRANSPORT |
| DEF_TRANSPORT_RESIDUAL | DEFINITION | Delta_T measures failure of direct transport to equal sequential transport. | PRIM_TRANSPORT |
| DEF_TRANSPORT_PRODUCT_COHERENCE | DEFINITION | Measures failure of T_r(X star Y)=T_r(X) star' T_r(Y). | PRIM_TRANSPORT, PRIM_PRODUCT, PRIM_MODULE |
| DEF_SCALE_TRANSPORT_COHERENCE | DEFINITION | Measures failure of semantic-scale/transport naturality. | PRIM_SCALE, PRIM_TRANSPORT, PRIM_MODULE |
| PRIM_ORBIT | STRUCTURAL PRIMITIVE | Admissible orbital actions U_g may act on algebra elements. | — |
| DEF_SCALE_ORBIT_RESIDUAL | DEFINITION | Delta_(S,U) measures order dependence of semantic coarse-graining and orbital action. | PRIM_SCALE, PRIM_ORBIT, PRIM_MODULE |
| DEF_SCALE_PRODUCT_COHERENCE | DEFINITION | Measures failure of S(X star Y)=S(X) star' S(Y). | PRIM_SCALE, PRIM_PRODUCT, PRIM_MODULE |
| DEF_ORBITAL_COHERENCE | DEFINITION | Identity, inverse and composition residuals diagnose exact group-action coherence. | PRIM_ORBIT, PRIM_MODULE |
| DEF_ORBIT_PRODUCT_COHERENCE | DEFINITION | Measures failure of U(X star Y)=U(X) star' U(Y). | PRIM_ORBIT, PRIM_PRODUCT, PRIM_MODULE |
| DEF_ORBIT_TRANSPORT_COHERENCE | DEFINITION | Measures orbital equivariance of typed transport. | PRIM_ORBIT, PRIM_TRANSPORT, PRIM_MODULE |
| DER_MOIRE | DERIVED | Relative Moiré action is M_ij = U_i U_j^{-1} where a supplied inverse is coherent. | PRIM_ORBIT |
| PRIM_REFINEMENT_MAP | STRUCTURAL PRIMITIVE | Typed branch maps F_-/F_+ advance a selected relational carrier by one refinement level. | RR1, PRIM_MODULE |
| DEF_REFINEMENT_RESIDUAL | DEFINITION | Delta_F measures failure of exact product preservation under refinement. | PRIM_REFINEMENT_MAP, PRIM_PRODUCT, PRIM_MODULE |
| DEF_REFINEMENT_TRANSPORT_COHERENCE | DEFINITION | Measures failure of the refinement/transport naturality square. | PRIM_REFINEMENT_MAP, PRIM_TRANSPORT, PRIM_MODULE |
| DEF_REFINEMENT_SCALE_COHERENCE | DEFINITION | Measures refinement/coarse-graining naturality. | PRIM_REFINEMENT_MAP, PRIM_SCALE, PRIM_MODULE |
| DEF_REFINEMENT_ORBIT_COHERENCE | DEFINITION | Measures refinement/orbital equivariance. | PRIM_REFINEMENT_MAP, PRIM_ORBIT, PRIM_MODULE |
| ZA_BRIDGE | BRIDGE | The companion Zero Axis model supplies Omega(s)=s/(1-s) and the critical-axis/unit-circle equivalence. | — |
| DER_WINDING | DERIVED | Topological winding is derived only from a closed phase path with a continuous lift. | ZA_BRIDGE |

## Audit conclusions

1. **RA0 and RR1 are independent foundational assumptions in the current kernel.** RA0 requires relational admissibility; it does not force recursive refinement.
2. **Binary relation typing is explicit.** It is part of the signature rather than a hidden consequence of RA0.
3. **CP1 is not an axiom.** It is the chosen minimal complex binary projective realization. A non-CP1 model can still satisfy RA0 and RR1.
4. **The additive K-module structure, tensor-scalar grading, semantic scale, typed transport, orbital action and relational product are signature choices/structural primitives.** They are not derived from RA0. The additive module is required before differences such as commutators, associators and refinement residuals are meaningful.
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


## Holonomy stratification

Typed relation transport belongs to the core signature. For a closed composable path \(\gamma\),

\[
\mathcal H_\gamma=T_\gamma
\]

is the abstract relational holonomy, with residual

\[
\varepsilon_\gamma(X)=\|T_\gamma X-X\|.
\]

The transport-composition defect

\[
\Delta_T
=
\|T_{r_2\circ r_1}X-T_{r_2}(T_{r_1}X)\|
\]

measures local failure of functorial transport.

Relational holonomy is therefore more general than its phase realization. The Zero Axis bridge supplies the projective \(U(1)\) sector in which selected closed holonomies admit a phase and topological winding.


## Algebra and orbit coherence

The word "algebra" does not silently impose bilinearity on the context-dependent relational product. The kernel measures left/right additivity and scalar-linearity residuals. Likewise, an indexed orbital operator family is not called an exact group action merely by notation; identity, inverse, and composition residuals are checked explicitly.

Exact K-bilinearity and exact group action are therefore promoted only as zero-defect subclasses of the more general relational operator structure.


## Cross-operation coherence

The principal maps are not assumed to preserve one another automatically. The kernel records four first-order compatibility defects:

[
Delta_{T,star}(X,Y)
=
left|
T_r(Xstar Y)
-
T_r(X)star' T_r(Y)
ight|,
]

[
Delta_{S,star}(X,Y)
=
left|
S(Xstar Y)
-
S(X)star' S(Y)
ight|,
]

[
Delta_{U,star}(X,Y)
=
left|
U(Xstar Y)
-
U(X)star' U(Y)
ight|,
]

and the refinement/transport naturality defect

[
Delta_{F,T}(X)
=
left|
F_{mathrm{target}}(T_{mathrm{parent}}X)
-
T_{mathrm{child}}(F_{mathrm{source}}X)
ight|.
]

Vanishing defects define structure-preserving subclasses. Non-zero defects are retained as relational deformation data.


## First-order naturality closure

The first-order map-to-map naturality layer is now closed for the currently admitted core operators. Executable residuals exist for:

- semantic scale versus transport;
- orbital action versus transport;
- refinement versus semantic scale;
- refinement versus orbital action;
- arbitrary typed maps versus tensor product;
- arbitrary typed maps versus contraction.

These are still diagnostics, not universal equations. A realization belongs to the corresponding exact subclass only when its residual vanishes on the stated domain.


## Tensor coherence boundary

The reference tensor sector now checks:

[
Delta_{alpha}^{otimes},
qquad
Delta_{mathbf 1}^{otimes},
qquad
Delta_{eta}^{otimes},
]

for strict associativity, explicitly supplied left/right units, and a supplied braiding rule. These are diagnostics; they do not force every tensor realization to be strict or symmetric.

Full non-strict monoidal coherence, including explicit associator and braiding isomorphisms with pentagon/hexagon laws, remains OPEN.


## CP1 refinement realization boundary

The CP1 refinement realization is fibre-local:

\[
\mathcal F_\omega\simeq CP^1.
\]

A selected projective state in the parent fibre indexes a child relational carrier, which may then own a new local CP1 fibre. The parent state is not identified with the coordinate system of the child fibre.

This closes the implementation gate for a recursive CP1/Fubini-Study **reference realization**, while preserving the earlier independence result

\[
\mathrm{RA0}+\mathrm{RR1}\not\Rightarrow CP^1.
\]
