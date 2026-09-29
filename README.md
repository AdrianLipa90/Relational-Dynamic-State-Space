# Relational Tensor-Scalar Orbital-Fractal Algebra (RTOFA)

This repository develops a **general relational algebra**. The current core is intentionally independent of a particular spacetime, physical model, or application.

The canonical algebraic object is a typed family

\[
\mathfrak A_{\rm rel}
=
\left\{\mathcal A_{\sigma,\omega}^{p,q}\right\},
\]

where \((p,q)\) is tensor rank, \(\omega\in\{-1,+1\}^{*}\) is the exact path-labelled relational carrier address, and \(\sigma\in\Sigma\) is a semantic scale/context. The refinement level is derived as \(n=|\omega|\); it does not identify the sector by itself. The scalar sector is the rank-zero sector

\[
\mathbb K_{\sigma,\omega}=\mathcal A_{\sigma,\omega}^{0,0}.
\]

## Foundational split

The axiom audit distinguishes claims by role instead of labeling every useful construction an axiom.

The current minimal axiom set is

\[
\boxed{
\mathrm{META0}
\;\triangleright\;
(\mathrm{RA0}+\mathrm{RR1})
}.
\]

Here \(\mathrm{META0}\) is a **model-formation meta-axiom**, not an object-level proposition.

**META0 — non-reification and model non-vacuity**

Absolute nothingness has no denotation in the RTOFA object language. In particular, it is not represented by a carrier, state, relation, zero, or by the empty set. The empty set is already a mathematical object.

The intended model class is therefore restricted by definition to non-empty admitted carrier domains:

\[
\boxed{
\mathfrak M\in\operatorname{Mod}(\mathrm{RTOFA})
\Longrightarrow
\operatorname{Adm}^{\mathfrak M}\neq\varnothing.
}
\]

Consequently

\[
\boxed{
\mathrm{EX0}:
\exists p\,\operatorname{Adm}(p)
}
\]

is a theorem of the model-formation semantics, not an additional ontological axiom.

A raw empty mathematical presentation is still useful metamathematically: RA0, RR1, and RA0* can be vacuously true on it. But that presentation is not an admissible RTOFA model and is not identified with “absolute nothing.”

**RA0 — relational admissibility**

Once a carrier is admitted, it is not defined as an observable independently of relation:

\[
\operatorname{Adm}(x)
\Longrightarrow
\exists\,y,r:
\bigl(
\operatorname{Rel}_r(x,y)
\lor
\operatorname{Rel}_r(y,x)
\bigr).
\]

**RR1 — recursive relational closure**

At every admitted path-labelled occurrence, a selected relational point may itself carry a further non-degenerate binary distinction, and the same rule re-applies at every finite refinement depth. Non-degeneracy is occurrence-level: the branch slots \((-),(+)\) are distinct even when both carry the same underlying carrier label. Thus a singleton witness \(D(a)=(a,a)\) is allowed. This is the explicit extra assumption that generates the fractal/refinement tower; it is not silently claimed to follow from RA0.

The minimal algebraic carrier is an unscaled point \(p\). Algebraic zero is not identified with absence of relation.

See \`docs/FOUNDATIONAL_NONVACUITY_GATE.md\` for the distinction between raw formula semantics and the intended non-empty model class.

A singleton carrier can therefore unfold through distinct path-labelled occurrences:
\[
a_{\varnothing}
\to
\{a_-,a_+\}
\to
\{a_{--},a_{-+},a_{+-},a_{++}\}
\to\cdots.
\]
### Occurrence growth versus carrier cardinality

For complete binary refinement through depth \(N\),

\[
\boxed{
|V_{\le N}|=2^{N+1}-1.
}
\]

Thus a singleton carrier presentation can keep

\[
|\operatorname{Adm}|=1
\]

while the number of path-labelled relational occurrences grows without bound.

The full finite-word address space

\[
V_{<\omega}=\{-1,+1\}^{<\omega}
\]

is countably infinite. The reference kernel implements the explicit bijection

\[
\rho(\omega)
=
2^{|\omega|}-1+\operatorname{bin}(\omega),
\]

with \(-1\mapsto0\), \(+1\mapsto1\), through
`finite_word_rank` / `finite_word_unrank`.

### Ideal occurrence boundary

The countable finite-word tree has a separate ideal boundary

\[
\boxed{
\partial V
=
\{-1,+1\}^{\mathbb N}.
}
\]

Boundary points are infinite branch sequences, not additional finite occurrence carriers. At prefix depth \(n\), the boundary is partitioned into exactly

\[
2^n
\]

prefix cylinders; the reference helpers `binary_words_at_depth` and `binary_boundary_cylinder_count` audit this finite basis.

Via the bijection

\[
\xi
\longmapsto
\{n\in\mathbb N:\xi_n=+1\},
\]

the ideal boundary has cardinality

\[
\boxed{
|\partial V|=2^{\aleph_0}.
}
\]

RR1 realizes every finite prefix of every ideal boundary sequence. It does **not** by itself assert a limit carrier for an infinite address. Thus

\[
\boxed{
\text{uncountable ideal boundary}
\neq
\text{uncountably many admitted carriers}.
}
\]

### Carrier values and occurrence addresses

RTOFA now keeps two sorts explicit:

\[
\boxed{
\text{carrier value }a
\neq
\text{occurrence address }\omega.
}
\]

A primitive relation value is typed on carriers,

\[
r:a\to b,
\]

while branch-aware identity is carried independently by

\[
\omega\in B^*
=
\{-1,+1\}^{*}.
\]

The same carrier value may therefore occur at many addresses:

\[
\operatorname{carrier}(\omega_1)
=
\operatorname{carrier}(\omega_2)
=
a,
\qquad
\omega_1\neq\omega_2.
\]

This is why a self-relation may be closed as a relation value while remaining
open as a branch occurrence.

See `docs/CARRIER_OCCURRENCE_SEPARATION.md`.

### Occurrence address monoid

The finite occurrence-address words form

\[
B^*=\{-1,+1\}^{*},
\]

the free monoid on the two branch generators under concatenation, with the
empty word \(\varnothing\) as identity.

For \(\omega,u\in B^*\), define

\[
\boxed{
\omega\cdot u=\omega u.
}
\]

Therefore

\[
\omega\cdot\varnothing=\omega,
\qquad
(\omega\cdot u)\cdot v
=
\omega\cdot(uv).
\]

`OccurrenceAddress.advance` implements this right action and
`OccurrenceAddress.refine` is the one-generator binary refinement.

The word-length map is the natural grading:

\[
\ell(\omega)=|\omega|,
\qquad
\ell(\omega u)=\ell(\omega)+|u|.
\]

RR1 is separate: it asserts that every finite address word is actually
realized by a relational occurrence from an admitted root.

### Canonical occurrence-tree geometry

The address monoid carries the prefix order

\[
u\preceq v
\Longleftrightarrow
\exists w:\ v=uw.
\]

The meet is the longest common prefix,

\[
u\wedge v=\operatorname{LCP}(u,v),
\]

and the canonical tree distance is

\[
\boxed{
d_T(u,v)
=
|u|+|v|-2|u\wedge v|.
}
\]

`OccurrenceAddress.is_prefix_of`, `.meet`, and `.tree_distance`
implement these objects. Thus the finite occurrence-address space is a rooted
meet-semilattice with its canonical combinatorial tree metric.

This metric belongs to the occurrence-address layer. It is not a physical
distance and is not identified with Fubini--Study, Hilbert-space, Minkowski,
or any later geometric realization.

### Reference embedding into binary point coordinates

Existing projective/refinement realizations retain a binary coordinate on
`RelationalPoint`. The relation to canonical occurrence addresses is made
explicit by the reference injection

\[
\boxed{
\iota:
B^*
\hookrightarrow
P_{\rm ref},
\qquad
\iota(\omega)=p_\omega.
}
\]

In code this is `reference_point_from_occurrence`.

This is a realization map, not an identity of types:

\[
\boxed{
\operatorname{OccurrenceAddress}
\not\equiv
\operatorname{RelationalPoint}.
}
\]

`RelationalPoint.advance` and its binary-coordinate helpers are retained for
reference-realization compatibility, but they are not the canonical source of
branch-occurrence identity.

### Minimal underlying relation value

The two branch occurrences do not need two distinct underlying relation
values. The minimal relational witness may use one self-relation

\[
r:a\to a
\]

for both branch slots. After forgetting occurrence identity,

\[
\pi_{\rm rel}(o_-)
=
\pi_{\rm rel}(o_+)
=
(a,a,r),
\]

while \(o_-\neq o_+\) because their branch slots differ.

Thus the same minimal model can satisfy

\[
\boxed{
|\operatorname{Adm}|=1,
\qquad
|\operatorname{RelVal}|=1,
\qquad
|\operatorname{RelOcc}|=2.
}
\]

The distinction multiplicity therefore resides in the occurrence layer rather
than requiring multiple base carriers or multiple underlying relation values.
This triple is exact for the candidate model class: META0 gives the non-empty
carrier lower bound, RA0_REL_STAR gives the two-occurrence lower bound, and
the singleton one-relation witness attains all three simultaneously.

## Reference minimal distinction

A minimal complex binary distinction may be represented by

\[
\mathbb P(\mathbb C^2)=CP^1\simeq S^2,
\]

with Fubini-Study distance

\[
d_{\rm FS}([\psi],[\phi])=\arccos |\langle\psi|\phi\rangle|.
\]

This is a **reference realization**, not a theorem forced by RA0.

## Recursive relational refinement

\[
p_\omega\longmapsto\{p_{\omega-},p_{\omega+}\},
\qquad
\omega\in\{-1,+1\}^n.
\]

For each branch \(\epsilon\in\{-1,+1\}\), the executable algebra refinement is typed as

\[
F_{\epsilon}:
\mathcal A_{\sigma,\omega}^{p,q}
\to
\mathcal A_{\tau,\omega\epsilon}^{p,q}.
\]

Exact self-similarity is not assumed. Branch refinement is primitive, while its compatibility with the product is measured by

\[
\Delta_F(X,Y)
=
F(X\star Y)-F(X)\star F(Y).
\]

### Recursive CP1 fibre reference

The CP1/Fubini-Study layer is implemented as a tested **reference realization** of recursive refinement:

\[
\mathcal F_\omega\simeq CP^1.
\]

A local distinction in \(\mathcal F_\omega\) indexes child carriers \(p_{\omega-},p_{\omega+}\), each of which may support its own local CP1 fibre. Parent projective states are not identified with child-fibre coordinates. The link is incidence/refinement, not one global sphere.

## Additive tensor-scalar sectors

Each typed sector carries an additive module structure over a scalar domain \(\mathbb K\):

\[
(\mathcal A_{\sigma,\omega}^{p,q},+,0,-,\mathbb K\curvearrowright\mathcal A_{\sigma,\omega}^{p,q}).
\]

The abstract algebra does not fix \(\mathbb K=\mathbb C\). The reference kernel uses complex components. This structure is required before commutators, associators, and refinement residuals can be interpreted as differences. The executable zero of a reference element preserves its exact typed sector — tensor rank, relational carrier, semantic scale, and component dimension — and satisfies \(X+0_X=X\) and \(X-X=0_X\). Refinement level alone does not identify the zero sector.

Strict tensor coherence is also tested rather than presumed: the kernel measures tensor associativity, explicit left/right unit, and supplied braiding residuals. Full non-strict pentagon/hexagon coherence remains open.

## Product and orbital coherence

The relational product is not assumed bilinear. Additivity and scalar-linearity residuals are measured explicitly; exact \(\mathbb K\)-bilinearity is the zero-defect subclass.

Likewise, \(U_g\) is first an indexed family of orbital operators. Exact group action requires vanishing identity, inverse, and composition residuals. Relative Moiré

\[
M_{ij}=U_iU_j^{-1}
\]

is only claimed where the supplied inverse passes its coherence check.

## Semantic scales

Semantic scale is not assumed to be one real number. It lives in a typed scale structure \(\Sigma\), represented in the reference kernel by an acyclic coarse-graining graph. The reference kernel implements semantic coarse-graining as an executable typed map \(S_{\sigma\to\tau}\).

The order dependence of semantic scaling and orbital action is measured by

\[
\Delta_{S,U}(X)=\|U(SX)-S(UX)\|.
\]

## Orbital and Moiré sector

Orbital action is a structural primitive:

\[
U_g:\mathcal A\to\mathcal A.
\]

The orbit is derived:

\[
\operatorname{Orb}(X)=\{U_gX:g\in G\}.
\]

Moiré is also derived once orbital actions are available:

\[
M_{ij}=U_iU_j^{-1},
\]

where the inverse exists.

## Cross-operation coherence

The main structural maps are not assumed to preserve one another. The kernel measures

\[
\Delta_{T,\star},
\qquad
\Delta_{S,\star},
\qquad
\Delta_{U,\star},
\qquad
\Delta_{F,T}.
\]

These test, respectively, transport/product compatibility, semantic-scale/product compatibility, orbital/product compatibility, and the refinement/transport naturality square. Vanishing residuals define structure-preserving subclasses; non-zero values remain deformation data.

## Relational deformation potential

A selected set of non-negative residual diagnostics may be collected into a fixed signature

\[
d(X)=\{d_i(X)\}_{i\in I}.
\]

A supplied semantic profile assigns non-negative weights \(w_{\sigma i}\) to that same signature. The current kernel does not infer these weights from the scale label \(\sigma\). The reference scalar potential is

\[
\boxed{
V_R^{(p)}(X\mid\sigma)
=
\left(
\sum_{i\in I}
w_{\sigma i}\,d_i(X)^p
\right)^{1/p},
\qquad
p\ge 1.
}
\]

This is a derived relational deformation scalar, not physical energy.

Holding the residual signature and the potential order \(p\) fixed isolates a purely semantic shift:

\[
\boxed{
\Delta_{\sigma\to\tau}V_R(X)
=
V_R(X\mid\tau)-V_R(X\mid\sigma).
}
\]

Therefore the represented algebraic residuals may remain numerically unchanged while semantic weighting changes the scalar relational potential.

For a finite admissible candidate set, the relational attractor set is

\[
\operatorname{Attr}_R(X)
=
\arg\min_T V_R(TX),
\]

with ties retained rather than broken arbitrarily.

## Relational transport and two closure notions

For a composable relation-value path

\[
\gamma=(r_1,\ldots,r_m),
\qquad
r_k:a_{k-1}\to a_k,
\]

the core transport is

\[
T_\gamma=T_{r_m}\circ\cdots\circ T_{r_1}.
\]

At the value level, carrier closure is

\[
a_m=a_0.
\]

This gives the value-level holonomy residual

\[
\varepsilon_\gamma^{\mathrm{val}}(X)
=
\left\|
\mathcal H_\gamma^{\mathrm{val}}X-X
\right\|.
\]

Occurrence-aware paths retain source and target occurrence addresses in addition to the typed relation value. Their closure condition is

\[
\omega_m=\omega_0.
\]

With a consistent occurrence-to-carrier assignment, occurrence closure implies carrier closure, but the converse is false. The singleton step

\[
a_{\varnothing}\to a_-,
\]

projects to the carrier self-relation \(a\to a\), so it is carrier-closed after forgetting occurrence identity while remaining occurrence-open.

Therefore

\[
\boxed{
\text{carrier-closed}
\not\Rightarrow
\text{occurrence-closed}.
}
\]

The implementation keeps these levels separate:

- `RelationPath` / `TransportPath` for relation-value paths;
- `RelationOccurrence` / `OccurrenceRelationPath`;
- `OccurrenceTransportPath` for occurrence-aware holonomy.

## Phase representations

The value-level reference interface is

\[
\chi:
\mathcal H_\gamma^{\mathrm{val}}
\to
U(1),
\]

implemented by `HolonomyPhaseRepresentation`.

The occurrence-aware reference interface is separate:

\[
\widetilde\chi:
\mathcal H_{\widetilde\gamma}^{\mathrm{occ}}
\to
U(1),
\]

implemented by `OccurrenceHolonomyPhaseRepresentation`.

Both interfaces validate unit modulus and path closure at their own level. Neither is a universal existence theorem.
## Zero Axis / phase bridge

The companion Zero Axis model supplies

\[
\Omega(s)=\frac{s}{1-s},
\]

with

\[
\Re s=\frac12
\Longleftrightarrow
|\Omega(s)|=1.
\]

This is an imported **bridge**, not an axiom of the general algebra. Value-level and occurrence-level holonomy have separate optional \(U(1)\) reference interfaces. Phase turn-count and winding depend on the chosen interface plus the corresponding closure condition; they do not depend on Zero Axis. If an application additionally uses the companion Zero Axis bridge, a verified finite phase may be lifted through \(\Omega^{-1}(u)=u/(1+u)\), while \(u=-1\) is the compactified point at infinity.

## Non-assumptions

The kernel does **not** assume:

- a Planck-scale minimal point;
- a particular spacetime or metric;
- associativity or commutativity of the relational product;
- exact self-similarity under refinement;
- one-dimensional semantic scale;
- CP1 as the only possible relational realization;
- winding, orbit, or residual as primitive state variables;
- Zero Axis as an axiom of the general algebra;
- any physical identification without a separate bridge theorem.

See `docs/ARCHITECTURE.md` for module layering, `docs/FOUNDATIONAL_NONVACUITY_GATE.md` for META0/non-vacuity semantics, `docs/RELATIONAL_ADMISSIBILITY_REDUCTION_GATE.md` for the RA0 definitional-reduction question, `docs/RELATIONAL_DISTINCTION_BINDING_GATE.md` for the one-object-level-axiom candidate, `docs/RELATIONAL_POTENTIAL.md` for the semantic deformation scalar, `docs/SEMANTIC_WEIGHTING_GATE.md` for the open weight-derivation problem, `docs/AXIOM_AUDIT.md` for the typed dependency ledger, `docs/INDEPENDENCE_WITNESSES.md` for finite countermodels, `docs/COHERENCE_MATRIX.md` for compatibility laws, `docs/INDEXED_TENSOR_GATE.md` for the contraction/tensor realization boundary, `docs/MONOIDAL_COHERENCE_GATE.md` for the non-strict pentagon/hexagon boundary, and `docs/VALIDATION_STATUS.md` for current verification status.

## Layer architecture

The implementation is deliberately stratified:

\[
\boxed{
\text{core algebra}
\to
\text{structural operators}
\to
\text{relational potential diagnostics}
\to
\text{phase/reference realizations}
\to
\text{optional bridges}
}
\]

\`src/rdss/algebra.py\` is representation-free. CP1/Fubini--Study and scalar-angle Moiré live in \`realizations.py\`; generic U(1) utilities live in \`phase.py\`; Zero Axis lives in \`zero_axis.py\`. The package root re-exports these names for convenience without changing their epistemic layer.

The value-level holonomy phase map

\[
\chi:\mathcal H_\gamma^{\mathrm{val}}\to U(1)
\]

and the occurrence-level map

\[
\widetilde\chi:\mathcal H_{\widetilde\gamma}^{\mathrm{occ}}\to U(1)
\]

are separate reference-realization interfaces. The optional Zero Axis lift

\[
\Omega^{-1}(u)=\frac{u}{1+u}
\]

is a separate bridge applied only after a unit phase has already been established.

See \`docs/ARCHITECTURE.md\` for the exact module ownership and promotion rules.

## Local validation

The repository includes a local validator that does not use GitHub Actions:

```text
python scripts/validate.py
```

Static audit alone:

```text
python scripts/static_audit.py
```

Useful modes:

```text
python scripts/validate.py --tests-only
python scripts/validate.py --latex-only
python scripts/validate.py --require-latex
```

The default run executes `scripts/static_audit.py` first, then pytest, and then compiles the monograph when `latexmk` or `pdflatex` is installed. The static stage audits Python syntax/import surfaces, layer ownership, the claim DAG, test inventory, Markdown integrity, and structural LaTeX balance. `--require-latex` converts a missing LaTeX toolchain from SKIP to FAIL.

See `docs/VALIDATION_STATUS.md` for the latest distinction between static checks and runtime execution.

## Development invariant

Every promoted primitive should have synchronized forms:

\[
\boxed{\text{definition}+\text{reference code}+\text{test}+\text{LaTeX}}.
\]


## One-axiom closure candidate

The current canonical foundational stratification remains

\[
\boxed{
\mathrm{META0}
\;\triangleright\;
(\mathrm{RA0}+\mathrm{RR1})
}.
\]

A stronger candidate has now been isolated:

\[
\boxed{
\mathrm{RA0}^{*}:
\text{every admitted carrier hosts an admitted non-degenerate binary distinction,}
}
\]

with the selected endpoint occurrences themselves admitted. The left/right occurrence slots are distinct by address; their carrier labels need not differ.

Under this stronger statement, recursive refinement follows by induction on path-labelled occurrences:

\[
\boxed{
\mathrm{RA0}^{*}\Rightarrow\mathrm{RR1}.
}
\]

This does **not** mean old RA0 implied RR1. RA0* explicitly adds occurrence-level binary non-degeneracy and endpoint admissibility. It does not require two different carrier labels at a branch and therefore does not force ontically new carrier identities at each depth:

\[
\mathrm{RA0}^{*}\not\Rightarrow\mathrm{NOVELTY}.
\]

A still stronger executable candidate binds the two distinction slots to explicit primitive branch-relation occurrences:

\[
r_-:p_\omega\to p_{\omega-},
\qquad
r_+:p_\omega\to p_{\omega+}.
\]

In the ledger this candidate is `RA0_REL_STAR`, written schematically as

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}.
}
\]

It satisfies two explicit theorem claims:

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}\Rightarrow\mathrm{RA0},
\qquad
\mathrm{RA0}^{\mathrm{rel}*}\Rightarrow\mathrm{RR1}.
}
\]

Hence

\[
\boxed{
\mathrm{RA0}^{\mathrm{rel}*}
\Rightarrow
\mathrm{RA0}+\mathrm{RR1}.
}
\]

The converse fails in the expanded language: a singleton can satisfy RA0 and
recursive RR1 while carrying no explicit branch-slot to primitive-relation
binding. Therefore

\[
\boxed{
\mathrm{RA0}+\mathrm{RR1}
\not\Rightarrow
\mathrm{RA0}^{\mathrm{rel}*}.
}
\]

So this is a genuine strengthening/compression, not a notational
re-expression of the old pair.

Under META0 this is the current executable **one-object-level-axiom candidate**,

\[
\mathrm{META0}
\triangleright
\mathrm{RA0}^{\mathrm{rel}*},
\]

but it is not promoted: distinction-to-relation binding is additional formal content.

See `docs/AXIOM_CLOSURE_AUDIT.md`. The distinction-to-relation reduction is isolated in `docs/RELATIONAL_DISTINCTION_BINDING_GATE.md`; the separate question of defining admissibility relationally is in `docs/RELATIONAL_ADMISSIBILITY_REDUCTION_GATE.md`.
