# RTOFA Axiom Audit

This audit separates **model-formation rules**, **axioms**, **definitions**, **structural primitives**, **reference realizations**, **derived constructions**, and **imported bridges**. A dependency edge means "this construction explicitly uses that item"; it is not a claim that every item is logically derivable from the foundational axiom.

## Classification

| ID | Class | Statement | Direct dependencies |
|---|---|---|---|
| META0 | FORMATION RULE | Absolute nothingness has no object-language denotation; admissible RTOFA models have a non-empty admitted carrier domain. | — |
| EX0 | THEOREM | Every admissible RTOFA model contains at least one admitted relational carrier. | META0 |
| RA0 | AXIOM | Every admitted observable is incident to at least one primitive relation, as source or target. | — |
| DEF_POINT | DEFINITION | The minimal algebraic carrier is an unscaled point. | — |
| DEF_OCCURRENCE_ADDRESS_SPACE | DEFINITION | Occurrence addresses are finite words over {-1,+1}, with concatenation and the empty word. | — |
| DEF_CARRIER_OCCURRENCE_SEPARATION | DEFINITION | Carrier values and occurrence addresses are distinct semantic sorts; relation values are typed on carriers while branch-aware identity is carried by OccurrenceAddress. | DEF_POINT, DEF_OCCURRENCE_ADDRESS_SPACE |
| REF_RELATIONAL_POINT_BINARY_COORDINATE | REFERENCE REALIZATION | RelationalPoint retains a binary reference coordinate for compatibility with existing realizations; this coordinate is not canonical occurrence identity. | DEF_POINT, DEF_OCCURRENCE_ADDRESS_SPACE |
| THM_OCCURRENCE_ADDRESS_FREE_MONOID | THEOREM | The finite binary address space is the free monoid on generators -1 and +1 under concatenation. | DEF_OCCURRENCE_ADDRESS_SPACE |
| THM_REFINEMENT_RIGHT_ACTION | THEOREM | Appending finite words to OccurrenceAddress values defines the regular right action of the address monoid. | DEF_OCCURRENCE_ADDRESS_SPACE |
| THM_REFINEMENT_LEVEL_GRADING | THEOREM | Word length grades the occurrence-address monoid: level(omega·u)=level(omega)+|u|. | THM_REFINEMENT_RIGHT_ACTION |
| DEF_OCCURRENCE_PREFIX_ORDER | DEFINITION | Prefix order is u<=v iff v=uw for some finite binary word w. | DEF_OCCURRENCE_ADDRESS_SPACE |
| THM_OCCURRENCE_MEET_SEMILATTICE | THEOREM | Finite binary addresses form a rooted meet-semilattice under prefix order; meet is longest common prefix. | DEF_OCCURRENCE_PREFIX_ORDER |
| DEF_OCCURRENCE_TREE_DISTANCE | DEFINITION | d_T(u,v)=|u|+|v|-2|u meet v|. | THM_OCCURRENCE_MEET_SEMILATTICE, THM_REFINEMENT_LEVEL_GRADING |
| THM_OCCURRENCE_TREE_METRIC | THEOREM | The canonical occurrence-tree distance is a metric on finite path-labelled occurrence addresses. | DEF_OCCURRENCE_TREE_DISTANCE |
| DEF_BINARY_REL | DEFINITION | A primitive typed relation is binary: r:a->b. Higher arity is constructed separately. | — |
| DEF_RELATION_OCCURRENCE | DEFINITION | A relation occurrence is a typed relation value together with source/target OccurrenceAddress values; distinct occurrences may project to the same relation value. | DEF_BINARY_REL, DEF_CARRIER_OCCURRENCE_SEPARATION |
| DEF_OCCURRENCE_PATH | DEFINITION | An occurrence-aware path is composable in both carrier value and occurrence address, with one carrier consistently assigned to each occurrence address. | DEF_RELATION_OCCURRENCE |
| DEF_OCCURRENCE_FORGETFUL_PROJECTION | DEFINITION | The projection pi_occ_to_val forgets occurrence addresses while preserving ordered typed relation values. | DEF_OCCURRENCE_PATH |
| THM_OCCURRENCE_COMPOSABILITY_PROJECTS | THEOREM | Every occurrence-composable path projects to a composable relation-value path. | DEF_OCCURRENCE_FORGETFUL_PROJECTION |
| THM_OCCURRENCE_CLOSED_IMPLIES_VALUE_CLOSED | THEOREM | With consistent occurrence-to-carrier assignment, occurrence closure implies carrier/value closure. | DEF_OCCURRENCE_FORGETFUL_PROJECTION |
| REF_VALUE_CLOSED_OCCURRENCE_OPEN_COUNTERMODEL | REFERENCE REALIZATION | A singleton self-relation step can be value-closed while moving from the root occurrence to a child occurrence. | DEF_OCCURRENCE_FORGETFUL_PROJECTION |
| THM_VALUE_CLOSED_NOT_OCCURRENCE_CLOSED | THEOREM | The singleton countermodel proves the converse closure implication fails. | REF_VALUE_CLOSED_OCCURRENCE_OPEN_COUNTERMODEL |
| DEF_BINARY_DISTINCTION | DEFINITION | A hosted binary distinction has two distinct branch-occurrence slots (-,+); non-degeneracy is occurrence/address-level and does not require different carrier labels. | DEF_POINT, DEF_OCCURRENCE_ADDRESS_SPACE |
| DEF_RELATIONAL_DISTINCTION | DEFINITION | A relationally bound distinction equips the two branch-occurrence slots with explicit primitive branch-relation occurrences; occurrence identity includes the branch slot, so the underlying relation values may coincide. | DEF_BINARY_DISTINCTION, DEF_RELATION_OCCURRENCE |
| RR1 | AXIOM | At every admitted path-labelled occurrence, a selected endpoint may itself carry a further non-degenerate binary distinction; the rule re-applies at every finite refinement depth. | DEF_POINT, DEF_BINARY_DISTINCTION |
| THM_RR1_REALIZES_FINITE_WORDS | THEOREM | Under RR1 every finite binary address word from an admitted root is realized by a path-labelled occurrence. | RR1, DEF_OCCURRENCE_ADDRESS_SPACE |
| RA0_STAR | CANDIDATE AXIOM | Every admitted carrier hosts an admitted non-degenerate binary distinction whose endpoint occurrences are admitted. | DEF_POINT, DEF_BINARY_DISTINCTION |
| RA0_REL_STAR | CANDIDATE AXIOM | Every admitted carrier hosts at least one admitted relationally bound binary distinction whose endpoint occurrences are admitted. | DEF_POINT, DEF_RELATIONAL_DISTINCTION |
| THM_RA0_STAR_FROM_RA0_REL_STAR | THEOREM | Forgetting explicit branch-relation binding from an RA0_REL_STAR model yields an RA0_STAR model with the same admitted carriers and branch-occurrence structure. | RA0_REL_STAR |
| THM_RA0_FROM_RA0_REL_STAR | THEOREM | RA0_REL_STAR implies relational admissibility because each admitted host has branch-relation incidence. | RA0_REL_STAR |
| THM_RR1_FROM_RA0_REL_STAR | THEOREM | RA0_REL_STAR generates recursive binary refinement to arbitrary finite depth. | RA0_REL_STAR |
| THM_META0_CARDINALITY_LOWER_BOUND | THEOREM | META0 forces every admissible RTOFA model to satisfy |Adm| >= 1. | META0 |
| REF_SINGLETON_RA0_REL_STAR_MODEL | REFERENCE REALIZATION | Explicit recursive singleton model satisfying META0 + RA0_REL_STAR with |Adm| = 1. | META0, RA0_REL_STAR |
| THM_SINGLETON_FOUNDATION_MINIMALITY | THEOREM | Lower bound |Adm| >= 1 plus the singleton witness shows the exact minimum is 1. | THM_META0_CARDINALITY_LOWER_BOUND, REF_SINGLETON_RA0_REL_STAR_MODEL |
| THM_RELATION_VALUE_CARDINALITY_LOWER_BOUND | THEOREM | META0 plus RA0_REL_STAR force at least one underlying primitive relation value after forgetting branch occurrence identity. | META0, RA0_REL_STAR |
| REF_MINIMAL_SINGLE_RELATION_VALUE_MODEL | REFERENCE REALIZATION | Explicit singleton model with one admitted carrier, one underlying self-relation value, and two distinct branch occurrences. | META0, RA0_REL_STAR |
| THM_SINGLE_RELATION_VALUE_MINIMALITY | THEOREM | The exact minimum underlying relation-value cardinality under META0 plus RA0_REL_STAR is 1. | THM_RELATION_VALUE_CARDINALITY_LOWER_BOUND, REF_MINIMAL_SINGLE_RELATION_VALUE_MODEL |
| THM_RELATION_OCCURRENCE_CARDINALITY_LOWER_BOUND | THEOREM | META0 plus RA0_REL_STAR force at least two branch-relation occurrences. | META0, RA0_REL_STAR |
| THM_TWO_RELATION_OCCURRENCE_MINIMALITY | THEOREM | The minimal singleton witness attains the branch-occurrence lower bound, so the exact minimum is 2. | THM_RELATION_OCCURRENCE_CARDINALITY_LOWER_BOUND, REF_MINIMAL_SINGLE_RELATION_VALUE_MODEL |
| THM_MINIMAL_RELATIONAL_ATOM_SIGNATURE | THEOREM | The exact minimal cardinality triple is one admitted carrier, one underlying relation value, and two branch-relation occurrences. | THM_SINGLETON_FOUNDATION_MINIMALITY, THM_SINGLE_RELATION_VALUE_MINIMALITY, THM_TWO_RELATION_OCCURRENCE_MINIMALITY |
| THM_BINARY_OCCURRENCE_COUNT | THEOREM | A complete binary occurrence unfolding through finite depth N contains exactly 2^(N+1)-1 path-labelled occurrences. | RR1, DEF_BINARY_DISTINCTION |
| THM_FINITE_WORD_OCCURRENCE_COUNTABILITY | THEOREM | The full finite-word occurrence address space {-1,+1}^{<omega} is countably infinite. | THM_BINARY_OCCURRENCE_COUNT |
| DEF_OCCURRENCE_BOUNDARY | DEFINITION | The ideal occurrence boundary is {-1,+1}^N; its elements are infinite branch sequences, not additional finite carriers. | DEF_OCCURRENCE_ADDRESS_SPACE |
| THM_BOUNDARY_CYLINDER_COUNT | THEOREM | At prefix depth n, the ideal boundary decomposes into exactly 2^n prefix cylinders. | DEF_OCCURRENCE_BOUNDARY |
| THM_OCCURRENCE_BOUNDARY_CONTINUUM | THEOREM | The ideal occurrence boundary has cardinality 2^aleph_0 via its bijection with P(N). | DEF_OCCURRENCE_BOUNDARY |
| THM_RR1_REALIZES_BOUNDARY_PREFIX_CHAINS | THEOREM | RR1 realizes every finite prefix of every ideal boundary path but does not assert an infinite-address limit carrier. | RR1, DEF_OCCURRENCE_BOUNDARY |
| THM_RR1_FROM_RA0_STAR | THEOREM | RA0* generates recursive binary refinement to arbitrary finite depth by induction on path-labelled occurrences. | RA0_STAR |
| REF_CP1 | REFERENCE REALIZATION | A minimal complex binary distinction may be represented by two projectively distinct CP1 states with Fubini-Study metric. | DEF_POINT, DEF_BINARY_DISTINCTION |
| REF_CP1_REFINEMENT | REFERENCE REALIZATION | Recursive refinement is realized as a tree of local CP1/FS fibres indexed by relational carriers. | REF_CP1, RR1 |
| PRIM_MODULE | STRUCTURAL PRIMITIVE | Each typed tensor-scalar sector carries an additive K-module structure; the reference kernel uses complex components. | — |
| DEF_TS | DEFINITION | Tensor-scalar grading uses rank (p,q); scalars are rank (0,0). | PRIM_MODULE |
| DEF_TYPED_ZERO | DEFINITION | Additive zero is typed by rank, exact carrier, semantic scale, and component dimension; level is derived from carrier. | PRIM_MODULE, DEF_POINT, PRIM_SCALE |
| PRIM_PRODUCT | STRUCTURAL PRIMITIVE | A typed relational product star_R may be supplied without assuming associativity or commutativity. | — |
| PRIM_TENSOR_PRODUCT | STRUCTURAL PRIMITIVE | A typed tensor product combines compatible tensor-scalar sectors; component formulas belong to realizations. | PRIM_MODULE |
| PRIM_CONTRACTION | STRUCTURAL PRIMITIVE | A typed contraction lowers one covariant and one contravariant rank when a contraction rule is supplied. | PRIM_MODULE |
| DEF_BILINEARITY_RESIDUAL | DEFINITION | Bilinearity residuals measure failure of product additivity and scalar-linearity. | PRIM_PRODUCT, PRIM_MODULE |
| DEF_TENSOR_MAP_COHERENCE | DEFINITION | Measures monoidality of a supplied typed map with respect to tensor product. | PRIM_TENSOR_PRODUCT, PRIM_MODULE |
| DEF_TENSOR_MONOIDAL_COHERENCE | DEFINITION | Tests strict associativity, explicit unit, and supplied braiding by residuals. | PRIM_TENSOR_PRODUCT, PRIM_MODULE |
| DEF_CONTRACTION_MAP_COHERENCE | DEFINITION | Measures contraction naturality under a supplied typed map. | PRIM_CONTRACTION, PRIM_MODULE |
| PRIM_SCALE | STRUCTURAL PRIMITIVE | Semantic scale is a typed partial-order/category-like structure. | — |
| PRIM_SEMANTIC_WEIGHTING | STRUCTURAL PRIMITIVE | A supplied semantic profile assigns non-negative weights to a fixed named residual signature. | PRIM_SCALE |
| DEF_RELATIONAL_POTENTIAL | DEFINITION | The relational deformation potential is the weighted p-functional induced by that profile. | PRIM_SEMANTIC_WEIGHTING |
| DER_SEMANTIC_POTENTIAL_SHIFT | DERIVED | Difference of two semantic potential profiles evaluated on the same residual signature. | DEF_RELATIONAL_POTENTIAL |
| DER_RELATIONAL_ATTRACTOR | DERIVED | Set of admissible candidates attaining minimum relational potential. | DEF_RELATIONAL_POTENTIAL |
| PRIM_TRANSPORT | STRUCTURAL PRIMITIVE | Typed transports T_r act along composable binary relations between carrier sectors. | DEF_BINARY_REL, PRIM_MODULE |
| DER_HOLONOMY | DERIVED | Value-level relational holonomy is transport around a carrier-closed composable relation-value path, measured against the initial state. | PRIM_TRANSPORT |
| DER_OCCURRENCE_HOLONOMY | DERIVED | Occurrence-aware holonomy requires a path closed in both carrier value and occurrence address; carrier closure alone is insufficient. | PRIM_TRANSPORT, DEF_OCCURRENCE_PATH |
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
| REF_HOLONOMY_U1 | REFERENCE REALIZATION | A concrete realization supplies a U(1) representation of closed value-level relational holonomy. | DER_HOLONOMY |
| REF_OCCURRENCE_HOLONOMY_U1 | REFERENCE REALIZATION | A concrete realization separately supplies a U(1) representation of occurrence-closed relational holonomy. | DER_OCCURRENCE_HOLONOMY |
| DER_OCCURRENCE_WINDING | DERIVED | Occurrence-level topological winding is derived only after occurrence-closed holonomy has an explicit U(1) phase representation. | REF_OCCURRENCE_HOLONOMY_U1 |
| DER_WINDING | DERIVED | Topological winding is derived only after a closed value-level relational holonomy has an explicit U(1) phase representation. | REF_HOLONOMY_U1 |
| REF_HOLONOMY_ZERO_AXIS | REFERENCE REALIZATION | A verified finite U(1) holonomy phase may be lifted through Omega^{-1} to the companion Zero Axis. | REF_HOLONOMY_U1, ZA_BRIDGE |

## Audit conclusions

1. **META0 is logically prior to the object-level axioms.** It is a model-formation meta-axiom: absolute nothingness is not reified, and intended RTOFA models have non-empty admitted carrier domains.
2. **EX0 is a theorem of META0, not an extra ontological axiom.** A raw empty mathematical presentation may satisfy universal formulas vacuously, but it is excluded from the intended model class.
3. **RA0 and RR1 remain independent object-level foundational assumptions in the current kernel.** RA0 requires orientation-neutral relational incidence; it does not force recursive refinement.
4. **Binary relation typing is explicit.** It is part of the signature rather than a hidden consequence of RA0.
5. **Carrier values and occurrence addresses are separate sorts.** `OccurrenceAddress` carries branch identity; `RelationalPoint` carries a carrier/reference-coordinate value. The binary coordinate retained by `RelationalPoint` is a reference realization, not the canonical occurrence identity.
6. **Binary distinction non-degeneracy is occurrence-level.** The two branch slots \((-),(+)\) are distinct occurrences even when both carry the same carrier label. Carrier-label inequality is not required.
7. **CP1 is not an axiom.** It is the chosen minimal complex binary projective realization. A non-CP1 model can still satisfy RA0 and RR1.
8. **The additive K-module structure, tensor-scalar grading, semantic scale, supplied semantic weighting, typed transport, orbital action and relational product are signature choices/structural primitives.** They are not derived from RA0. The additive module is required before differences such as commutators, associators and refinement residuals are meaningful.
9. **Moiré is derived once invertible orbital actions are present.**
10. **Refinement residual requires both recursive refinement and a relational product.**
11. **Occurrence-to-value forgetting is explicit.** The projection \(\pi_{\rm occ\to val}\) drops occurrence addresses but preserves ordered relation values. Occurrence composability projects to value composability.
12. **Carrier closure and occurrence closure are distinct.** Occurrence closure implies carrier/value closure under a consistent assignment, while the singleton self-relation countermodel shows the converse fails.
13. **Value-level and occurrence-level U(1) representations are separate reference realizations.** Neither is a universal theorem of the core algebra.
14. **Topological winding depends on that U(1) representation and an explicit closure check, not on Zero Axis.**
15. **Zero Axis is an independent imported bridge.** Its finite inverse projective lift is optional and occurs only after a U(1) phase has already been supplied.
16. **Associativity, commutativity and exact refinement self-similarity remain testable properties.**
17. **RA0_REL_STAR is a stronger one-object-level-axiom candidate.** It differs from RA0* by explicitly binding binary distinction slots to primitive relation occurrences; only this stronger candidate currently carries explicit theorems to both RA0 and RR1.
18. **Carrier cardinality and occurrence cardinality are independent scales.** A singleton carrier presentation can generate \(2^{N+1}-1\) distinct path-labelled occurrences through depth \(N\), and the full finite-word address space is countably infinite.
19. **Underlying relation-value cardinality can also be minimal.** Two distinct branch occurrences may project to one self-relation value, so the minimal singleton RA0_REL_STAR model simultaneously attains \(|\operatorname{Adm}|=1\) and \(|\operatorname{RelVal}|=1\).
20. **Occurrence addresses form a free monoid.** The finite words \(\{-1,+1\}^{*}\) compose by concatenation with the empty word as identity; `OccurrenceAddress.advance` is the canonical right action, and RR1 realizes every finite word from an admitted root.
21. **Refinement level is a monoid grading.** The occurrence-address level is word length: \(\ell(uv)=\ell(u)+\ell(v)\) and \(\ell(\omega u)=\ell(\omega)+|u|\).
22. **Occurrence addresses carry a canonical tree metric.** Prefix order gives longest-common-prefix meet, and \(d_T(u,v)=|u|+|v|-2|u\wedge v|\) is the induced combinatorial tree metric. This is address geometry, not a physical metric.

## Canonical foundational stratification

\[
\boxed{
\mathrm{META0}
\;\triangleright\;
(\mathrm{RA0}+\mathrm{RR1})
}
\]

META0 belongs to model formation rather than the object language. RA0 and RR1 are the current object-level axioms. EX0 is a theorem of META0.

This deliberately small foundation does **not** mean that the rest of the signature follows from these statements; the remaining ingredients are typed definitions, independent structural primitives, realizations, derivations, or bridges.

## Open reduction targets

There are now two distinct reduction questions.

First, with primitive \(\operatorname{Adm}\),

\[
\mathrm{META0}\not\Rightarrow\mathrm{RA0}.
\]

A one-carrier non-empty presentation with no relations is the executable countermodel. RA0 can be demoted only if admissibility itself is explicitly defined by orientation-neutral relational incidence. That definitional option is tracked in `docs/RELATIONAL_ADMISSIBILITY_REDUCTION_GATE.md`.

Second, recursive closure may be reduced through the stronger candidate RA0*:

\[
\mathrm{RA0}^{*}\Rightarrow\mathrm{RR1}.
\]

Third, if hosted distinction is explicitly bound to primitive branch-relation occurrences, the stronger candidate RA0_REL_STAR satisfies

\[
\boxed{
\mathrm{RA0\_REL\_STAR}
\Rightarrow
\mathrm{RA0}+\mathrm{RR1}.
}
\]

This is the current executable one-object-level-axiom candidate under META0. It remains unpromoted because the distinction-to-relation binding is additional formal content.

Neither reduction is performed by rhetoric; each requires an explicit change of formal status.


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

Relational holonomy is more general than any phase representation. A concrete realization may separately provide

\[
\chi:\mathcal H_\gamma\to U(1).
\]

Only after such a representation exists do phase residual and topological winding become available. Zero Axis is not required for this step. Its projective map is a later optional bridge from an already verified \(U(1)\) phase.

## Algebra and orbit coherence

The word "algebra" does not silently impose bilinearity on the context-dependent relational product. The kernel measures left/right additivity and scalar-linearity residuals. Likewise, an indexed orbital operator family is not called an exact group action merely by notation; identity, inverse, and composition residuals are checked explicitly.

Exact K-bilinearity and exact group action are therefore promoted only as zero-defect subclasses of the more general relational operator structure.


## Cross-operation coherence

The principal maps are not assumed to preserve one another automatically. The kernel records first-order compatibility defects:

\[
\Delta_{T,\star}(X,Y)
=
\left\|
T_r(X\star Y)
-
T_r(X)\star' T_r(Y)
\right\|,
\]

\[
\Delta_{S,\star}(X,Y)
=
\left\|
S(X\star Y)
-
S(X)\star' S(Y)
\right\|,
\]

\[
\Delta_{U,\star}(X,Y)
=
\left\|
U(X\star Y)
-
U(X)\star' U(Y)
\right\|,
\]

and the refinement/transport naturality defect

\[
\Delta_{F,T}(X)
=
\left\|
F_{\mathrm{target}}(T_{\mathrm{parent}}X)
-
T_{\mathrm{child}}(F_{\mathrm{source}}X)
\right\|.
\]

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

The reference tensor sector checks

\[
\Delta_{\alpha}^{\otimes},
\qquad
\Delta_{\mathbf 1}^{\otimes},
\qquad
\Delta_{\beta}^{\otimes},
\]

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


## Holonomy phase and Zero-Axis boundaries

The first reference interface is independent of Zero Axis:

\[
\chi:\mathcal H_\gamma\to U(1).
\]

It exists only for realizations that can represent a closed relational holonomy by a unit-modulus phase. This interface is the dependency needed by winding.

The companion Zero Axis is a separate optional bridge. Given an already verified finite phase \(u\in U(1)\),

\[
\Omega^{-1}(u)=\frac{u}{1+u}
\]

returns a finite point on the Zero Axis for \(u\neq-1\); \(u=-1\) is the compactified point at infinity.

Thus two different open questions remain distinguishable:

1. when a general RTOFA holonomy admits a \(U(1)\) representation \(\chi\);
2. whether and why a chosen application should additionally bind that phase to the companion Zero Axis.

Neither statement is promoted to a universal theorem of the core algebra.


## Relational deformation potential boundary

Let

\[
D(X)=\{d_i(X)\}_{i\in I},
\qquad
d_i(X)\ge 0
\]

be an explicit named residual signature. A semantic weighting profile supplies

\[
W_\sigma=\{w_{\sigma i}\}_{i\in I},
\qquad
w_{\sigma i}\ge 0.
\]

The current kernel does **not** infer \(W_\sigma\) from the label \(\sigma\). The weighting law is explicit structural input.

For \(p\ge1\),

\[
V_R^{(p)}(X\mid\sigma)
=
\left(
\sum_{i\in I}
w_{\sigma i}d_i(X)^p
\right)^{1/p}.
\]

Holding \(D(X)\) and \(p\) fixed while changing only the supplied weighting defines the semantic potential shift

\[
\Delta_{\sigma\to\tau}V_R(X)
=
V_R(X\mid\tau)-V_R(X\mid\sigma).
\]

For a finite admissible candidate set \(\mathcal C\),

\[
\operatorname{Attr}_R(\mathcal C)
=
\operatorname*{arg\,min}_{c\in\mathcal C}V_R(c).
\]

This construction is a relational scalar diagnostic. It is not identified with energy, mass, gravity, or metric curvature by the general algebra. A potential-to-geometry map would be a separate realization/bridge.


## Non-vacuity and non-reification boundary

At the level of unrestricted raw presentations, the universal object-level formulas remain compatible with an empty carrier domain:

\[
\mathrm{RA0}+\mathrm{RR1}
\not\vdash
\mathrm{EX0},
\qquad
\mathrm{RA0}^{*}
\not\vdash
\mathrm{EX0}.
\]

That empty presentation is a mathematical object and is useful as a vacuity witness. It is **not** identified with absolute nothingness.

META0 fixes the intended model semantics:

\[
\boxed{
\mathfrak M\in\operatorname{Mod}(\mathrm{RTOFA})
\Longrightarrow
\operatorname{Adm}^{\mathfrak M}\neq\varnothing.
}
\]

Hence

\[
\boxed{
\mathrm{META0}\models\mathrm{EX0},
\qquad
\mathrm{EX0}:\exists p\,\operatorname{Adm}(p).
}
\]

The executable reference kernel preserves this distinction by allowing an empty raw presentation while marking it as not admissible through the model-formation check.

See \`docs/FOUNDATIONAL_NONVACUITY_GATE.md\`.



## Canonical reduction claim layer

The canonical reduction machinery is not a new foundational axiom. Its current
claim classification is:

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_CANONICAL_NORMAL_FORM | DEFINITION | Exact type-tagged canonical key plus separate non-authoritative provenance. | — |
| DEF_REDUCTION_RELATION_KIND | DEFINITION | Every reduction declares identity/equivalence/isomorphism/reference/projection/approximation status. | DEF_CANONICAL_NORMAL_FORM |
| DEF_REDUCTION_INFORMATION_EFFECT | DEFINITION | Every reduction declares LOSSLESS/LOSSY/UNKNOWN; LOSSLESS requires an explicit inverse. | DEF_REDUCTION_RELATION_KIND |
| DEF_REDUCTION_TRACE | DEFINITION | Every accepted step records before/after keys, relation kind, information effect, preserved invariants and claim provenance; ambiguity/cycles fail closed. | DEF_REDUCTION_INFORMATION_EFFECT |
| THM_STRICT_NORMAL_FORM_IDEMPOTENCE | THEOREM | Strict normalization satisfies \(\mathcal N_0(\mathcal N_0(X))=\mathcal N_0(X)\) by construction. | DEF_CANONICAL_NORMAL_FORM |

None of these claims changes

\[
\boxed{
\mathrm{META0}
\triangleright
(\mathrm{RA0}+\mathrm{RR1}).
}
\]

The first RDSS-specific canonical reductions reuse the existing
DEF_OCCURRENCE_FORGETFUL_PROJECTION and
THM_OCCURRENCE_COMPOSABILITY_PROJECTS claims. They are marked LOSSY and are not
reclassified as identity or isomorphism.

See docs/CANONICAL_REDUCTION_GATE.md.


## Canonical signature claim layer

The semantic signature engine is a classification layer, not a foundational
extension.

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_RDSS_CANONICAL_SIGNATURE | DEFINITION | Supported executable objects expose a finite semantic signature separated from concrete representation, provenance, and strict object identity. | DEF_CANONICAL_NORMAL_FORM |
| DEF_SIGNATURE_AXIS_STRATIFICATION | DEFINITION | Carrier, occurrence, relations, rank, scale, orbit and dimension are structural axes; phase and state payload are state axes. | DEF_RDSS_CANONICAL_SIGNATURE |
| DEF_SIGNATURE_COMPARISON | DEFINITION | Comparison distinguishes same semantic signature, representation-only difference, same structure/different state, structural difference, and incomparable families. | DEF_SIGNATURE_AXIS_STRATIFICATION |
| DEF_SIGNATURE_NOVELTY_CLASSIFICATION | DEFINITION | Relative novelty is classified as exact repeat, signature-equivalent, representation-only, new state, new structure, or new family. | DEF_SIGNATURE_COMPARISON |

No signature comparison may convert INCOMPARABLE into equivalence without an
explicit bridge. No signature claim modifies META0, RA0 or RR1.


## Reduction termination and confluence layer

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_LEXICOGRAPHIC_REDUCTION_ORDER | DEFINITION | A fixed finite-dimensional \(\mathbb N^k\) measure may certify strict lexicographic descent of each reduction step. | DEF_REDUCTION_TRACE |
| THM_STRICT_LEX_DESCENT_TERMINATES | THEOREM | Strict descent in fixed finite-dimensional lexicographic \(\mathbb N^k\) excludes infinite reduction chains. | DEF_LEXICOGRAPHIC_REDUCTION_ORDER |
| DEF_FINITE_CONFLUENCE_AUDIT | DEFINITION | A bounded branch exploration reports unique normal form, multiple normal forms, cycle, or bounded incompleteness. | DEF_REDUCTION_TRACE |

The termination theorem is conditional on the supplied measure and its strict
descent on every admitted step. The finite confluence audit is not a universal
confluence theorem.


## Explicit bridge graph claim layer

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_BRIDGE_REGISTRY | DEFINITION | Explicit typed graph of legal inter-family transformations with direction, information effect, inverse availability, invariants and claim provenance. | DEF_SIGNATURE_COMPARISON, DEF_REDUCTION_RELATION_KIND, DEF_REDUCTION_INFORMATION_EFFECT |
| DEF_BRIDGE_ROUTE | DEFINITION | Finite composition of registered bridge edges; reverse traversal requires an explicit inverse; multiple distinct shortest routes fail closed. | DEF_BRIDGE_REGISTRY |
| DEF_BRIDGE_COMPARISON | DEFINITION | Route one value into the other's semantic family, then compare signatures; LOSSY/UNKNOWN routes require opt-in. | DEF_BRIDGE_ROUTE, DEF_SIGNATURE_COMPARISON |
| REF_OCCURRENCE_POINT_BRIDGE | REFERENCE_REALIZATION | Reversible binary coordinate bridge between OccurrenceAddress and the reference RelationalPoint coordinate. | REF_RELATIONAL_POINT_BINARY_COORDINATE, DEF_CARRIER_OCCURRENCE_SEPARATION, DEF_BRIDGE_REGISTRY |
| THM_REFERENCE_COORDINATE_ROUNDTRIP | THEOREM | The explicit reference-coordinate conversion round-trips exactly on the executable binary coordinate types. | REF_OCCURRENCE_POINT_BRIDGE |
| DEF_BRIDGE_EQUIVALENCE_GRAPH | DEFINITION | Finite graph with strong lossless/signature edges and separate directed LOSSY/UNKNOWN edges. | DEF_BRIDGE_COMPARISON, DEF_SIGNATURE_COMPARISON |
| DEF_BRIDGE_EQUIVALENCE_COMPONENT | DEFINITION | Components are generated only by strong same-signature or fully reversible LOSSLESS bridge edges. | DEF_BRIDGE_EQUIVALENCE_GRAPH |
| THM_LOSSY_BRIDGE_NONUNION | THEOREM | LOSSY edges are never passed to component union in the reference graph construction. | DEF_BRIDGE_EQUIVALENCE_COMPONENT |

The bridge component relation is relative to the selected explicit bridge
policy. It is not promoted to object identity. In particular, the reversible
OccurrenceAddress/RelationalPoint reference-coordinate bridge preserves
semantic sort separation.


### Bridge-gap diagnostic

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_BRIDGE_GAP_REPORT | DEFINITION | Groups unresolved cross-family record pairs by semantic-family pair without asserting that a bridge exists. | DEF_BRIDGE_EQUIVALENCE_GRAPH |

The gap report is a research-navigation diagnostic, not a foundational claim or
an automatic bridge-discovery theorem.


## Typed U1 phase and finite Zero-Axis bridge

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| REF_U1_PHASE_VALUE | REFERENCE REALIZATION | Explicit finite normalized complex representative of a point on \(U(1)\). | — |
| DEF_BRIDGE_ROUNDTRIP_VALIDATOR | DEFINITION | LOSSLESS bridges use strict canonical round-trip equality by default and may explicitly declare a numerical validator when floating evaluation is not bitwise exact. | DEF_BRIDGE_REGISTRY |
| REF_U1_ZERO_AXIS_FINITE_BRIDGE | REFERENCE REALIZATION | Finite projective bridge \(U(1)\setminus\{-1\}\leftrightarrow\{1/2+it\}\). | REF_U1_PHASE_VALUE, ZA_BRIDGE, DEF_BRIDGE_ROUNDTRIP_VALIDATOR |
| THM_U1_ZERO_AXIS_FINITE_ROUNDTRIP | THEOREM | The finite projective bridge returns the starting semantic value within its declared numerical validator; \(u=-1\) is outside the finite domain. | REF_U1_ZERO_AXIS_FINITE_BRIDGE |

The numerical validator does not globally replace exact canonical equality.
It is bridge-local, explicit, and part of the executable proof obligation.

The typed U1 family closes the previous MISSING_INTERMEDIATE_FAMILY triage item
for the finite Zero-Axis interface. It does not by itself prove that every RDSS
holonomy admits a U(1) representation.


## Executable bridge invariant layer

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_EXECUTABLE_BRIDGE_INVARIANT | DEFINITION | Named source/target projections plus comparator; global bridge execution fails closed if the invariant is false. | DEF_BRIDGE_REGISTRY |
| THM_REFERENCE_BRIDGE_INVARIANT_ENFORCEMENT | THEOREM | Reference BridgeRegistry executes every attached invariant before returning a BridgeStep. | DEF_EXECUTABLE_BRIDGE_INVARIANT |
| DEF_EXECUTABLE_CONTEXTUAL_BRIDGE_INVARIANT | DEFINITION | Contextual invariant may project through source plus explicit context before comparison with target. | DEF_CONTEXTUAL_BRIDGE_REGISTRY, DEF_EXECUTABLE_BRIDGE_INVARIANT |
| THM_REFERENCE_CONTEXTUAL_INVARIANT_ENFORCEMENT | THEOREM | Reference ContextualBridgeRegistry executes every attached contextual invariant before returning a ContextualBridgeStep. | DEF_EXECUTABLE_CONTEXTUAL_BRIDGE_INVARIANT |

Executable invariant failure is a route failure. Descriptive preservation text
does not override an executable FAIL.


## Rewrite termination certificate layer

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_FAMILY_RANK_TERMINATION_CERTIFICATE | DEFINITION | Natural-number rank on semantic families that must strictly decrease across every selected rewrite rule. | DEF_PRIORITY_FREE_REWRITE_SYSTEM |
| THM_STRICT_FAMILY_RANK_TERMINATION | THEOREM | Strict descent in \(\mathbb N\) excludes infinite rewrite traces. | DEF_FAMILY_RANK_TERMINATION_CERTIFICATE |
| REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE | REFERENCE REALIZATION | Rank 1 on the four current forgetful source families and rank 0 on their targets/default families. | DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER, DEF_FAMILY_RANK_TERMINATION_CERTIFICATE |
| THM_REFERENCE_FORGETFUL_REWRITE_TERMINATES | THEOREM | Every reference forgetful trace has length at most one. | REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE, THM_STRICT_FAMILY_RANK_TERMINATION |

No claim of termination is made for rewrite systems that do not pass an
explicit certificate audit.


## Confluence certificate layer

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_RULE_SOURCE_FAMILY_OVERLAP_AUDIT | DEFINITION | Enumerates rewrite-rule pairs sharing a declared source semantic family. | DEF_PRIORITY_FREE_REWRITE_SYSTEM, DEF_RDSS_CANONICAL_SIGNATURE |
| DEF_DISTINCT_SOURCE_FAMILY_CONFLUENCE_CERTIFICATE | DEFINITION | Valid when no two selected rewrite rules share a source semantic family. | DEF_RULE_SOURCE_FAMILY_OVERLAP_AUDIT |
| THM_DISTINCT_SOURCE_FAMILY_DETERMINISM | THEOREM | Distinct rule source families imply at most one immediate successor per admitted value. | DEF_DISTINCT_SOURCE_FAMILY_CONFLUENCE_CERTIFICATE |
| THM_DETERMINISTIC_REWRITE_CONFLUENCE | THEOREM | Deterministic rewrite relations are confluent because all finite derivations lie on one successor orbit. | THM_DISTINCT_SOURCE_FAMILY_DETERMINISM |
| REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE | REFERENCE REALIZATION | The four reference forgetful rules have pairwise distinct source families. | DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER, DEF_DISTINCT_SOURCE_FAMILY_CONFLUENCE_CERTIFICATE |
| THM_REFERENCE_FORGETFUL_REWRITE_CONFLUENT | THEOREM | The reference forgetful rewrite relation is confluent. | REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE, THM_DETERMINISTIC_REWRITE_CONFLUENCE |
| THM_TERMINATING_CONFLUENT_UNIQUE_IRREDUCIBLE | THEOREM | Termination plus confluence gives a unique irreducible result under the selected system. | THM_STRICT_FAMILY_RANK_TERMINATION, THM_DETERMINISTIC_REWRITE_CONFLUENCE |
| THM_REFERENCE_FORGETFUL_UNIQUE_IRREDUCIBLE | THEOREM | The selected reference forgetful system gives a unique irreducible result for each admitted value. | THM_REFERENCE_FORGETFUL_REWRITE_TERMINATES, THM_REFERENCE_FORGETFUL_REWRITE_CONFLUENT, THM_TERMINATING_CONFLUENT_UNIQUE_IRREDUCIBLE |

The last result is explicitly scoped to the selected forgetful rewrite system
and is not a global RDSS canonical-normal-form claim.


## Scoped normal form layer

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_SCOPED_REWRITE_NORMAL_FORM | DEFINITION | Unique irreducible result under one explicitly named rewrite system with explicit termination/confluence certificate provenance. | THM_TERMINATING_CONFLUENT_UNIQUE_IRREDUCIBLE |
| REF_FORGETFUL_SCOPED_NORMAL_FORM | REFERENCE REALIZATION | The rdss-reference-forgetful-v1 scoped normal form, which may perform LOSSY forgetful rewrites. | DEF_SCOPED_REWRITE_NORMAL_FORM, REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE, REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE |
| THM_REFERENCE_FORGETFUL_NORMAL_FORM_IDEMPOTENT | THEOREM | Reapplying the selected forgetful normal form yields the same strict target key and no further rewrite. | REF_FORGETFUL_SCOPED_NORMAL_FORM, THM_REFERENCE_FORGETFUL_UNIQUE_IRREDUCIBLE |

The reference scoped normal form is explicitly not a global RDSS canonical
normal-form claim.


## Semantic factorization layer

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_SEMANTIC_FACTORIZATION | DEFINITION | Explicit \((F,S,\sigma,\rho)\) view over RDSSSignature: family, structural key, state key and representation tag. | DEF_RDSS_CANONICAL_SIGNATURE, DEF_SIGNATURE_AXIS_STRATIFICATION |
| THM_FACTORIZATION_RECONSTRUCTS_SEMANTIC_KEY | THEOREM | The factorization preserves the original structural, state and semantic keys exactly. | DEF_SEMANTIC_FACTORIZATION |
| DEF_FACTORIZATION_COMPARISON | DEFINITION | Ordered comparison by family, structure, state and representation. | DEF_SEMANTIC_FACTORIZATION |
| REF_REFERENCE_CORPUS_FACTORIZATION_SUMMARY | REFERENCE REALIZATION | Current 36-record source corpus contracts to 22 families, 28 structures, 34 semantic states and 22 representation classes. | DEF_REFERENCE_CORPUS, DEF_SEMANTIC_FACTORIZATION |

This layer does not add a new quotient or override bridge semantics.


## Claim provenance graph layer

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_CLAIM_DEPENDENCY_PROJECTION | DEFINITION | Expands explicit root claim IDs into the induced subgraph of the authoritative RDSS claim ledger without creating or promoting claims. | DEF_RDSS_CANONICAL_SIGNATURE |
| THM_PROVENANCE_TOPOLOGICAL_ORDER | THEOREM | Every included dependency is emitted before every included claim that depends on it. | DEF_CLAIM_DEPENDENCY_PROJECTION |
| DEF_VALUE_CLAIM_PROVENANCE | DEFINITION | Combines semantic factorization, signature extractor provenance, signature claim roots and their dependency graph. | DEF_CLAIM_DEPENDENCY_PROJECTION, DEF_SEMANTIC_FACTORIZATION, DEF_RDSS_CANONICAL_SIGNATURE |
| DEF_TRANSFORMATION_CLAIM_PROVENANCE | DEFINITION | Expands BridgeRoute, RewriteTrace or ScopedRewriteNormalForm claim roots through the same authoritative dependency graph. | DEF_CLAIM_DEPENDENCY_PROJECTION, DEF_BRIDGE_ROUTE, DEF_PRIORITY_FREE_REWRITE_SYSTEM, DEF_SCOPED_REWRITE_NORMAL_FORM |

The provenance layer is read-only with respect to the claim ledger.


## Object reduction certificate layer

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_OBJECT_REDUCTION_CERTIFICATE | DEFINITION | One auditable object-level bundle joining source/target provenance, certified rewrite trace, scoped normal form, invariant evidence and the combined claim graph. | DEF_VALUE_CLAIM_PROVENANCE, DEF_TRANSFORMATION_CLAIM_PROVENANCE, DEF_SCOPED_REWRITE_NORMAL_FORM, DEF_EXECUTABLE_BRIDGE_INVARIANT |
| REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE | REFERENCE REALIZATION | Reference certificate for rdss-reference-forgetful-v1 with explicit termination/confluence identities and global canonicality false. | DEF_OBJECT_REDUCTION_CERTIFICATE, REF_FORGETFUL_SCOPED_NORMAL_FORM, REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE, REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE |
| THM_REFERENCE_OBJECT_REDUCTION_CERTIFICATE_CONSISTENT | THEOREM | Reference factory checks strict keys, complete value/transformation provenance, certificate identities, irreducibility, idempotence, invariant inventory and authoritative claim projection before returning. | REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE, THM_REFERENCE_FORGETFUL_NORMAL_FORM_IDEMPOTENT, THM_PROVENANCE_TOPOLOGICAL_ORDER |
| DEF_REFERENCE_REDUCTION_CERTIFICATE_SCAN | DEFINITION | Applies the object certificate factory independently to every named value in the reference corpus and aggregates diagnostics. | DEF_REFERENCE_CORPUS, DEF_OBJECT_REDUCTION_CERTIFICATE |
| REF_REFERENCE_REDUCTION_CERTIFICATE_SCAN | REFERENCE REALIZATION | Current source contract: 36 verified, 5 rewritten, 31 fixed, 5 LOSSY, zero global-canonical, 22 source families, 18 target families. | DEF_REFERENCE_REDUCTION_CERTIFICATE_SCAN, REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE |

The batch layer aggregates certificates; it does not weaken per-object validation.


## Loss witness layer

| ID | Kind | Meaning | Dependencies |
|---|---|---|---|
| DEF_LOSS_WITNESS | DEFINITION | Two strict-unequal source values collapse through one declared LOSSY rule to one strict-equal irreducible target, with executable invariant evidence. | DEF_REWRITE_RULE, DEF_EXECUTABLE_BRIDGE_INVARIANT |
| REF_FORGETFUL_LOSS_WITNESSES | REFERENCE REALIZATION | One executable noninjectivity witness exists for each of the four current forgetful rewrite rules. | DEF_LOSS_WITNESS, DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER |
| THM_REFERENCE_FORGETFUL_REWRITES_NONINJECTIVE | THEOREM | Each current forgetful rule is noninjective on its full source family, so no two-sided inverse exists there and the LOSSY classification is witnessed independently. | REF_FORGETFUL_LOSS_WITNESSES |

The witnesses validate information loss; they do not add new equivalences.
