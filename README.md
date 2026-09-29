# Relational Tensor-Scalar Orbital-Fractal Algebra (RTOFA)

This repository develops a **general relational algebra**. The current core is intentionally independent of a particular spacetime, physical model, or application.

The canonical algebraic object is a typed family

\[
\mathfrak A_{\rm rel}
=
\left\{\mathcal A_{\sigma,n}^{p,q}\right\},
\]

where \((p,q)\) is tensor rank, \(n\) is refinement level, and \(\sigma\in\Sigma\) is a semantic scale/context. The scalar sector is the rank-zero sector

\[
\mathbb K_{\sigma,n}=\mathcal A_{\sigma,n}^{0,0}.
\]

## Foundational split

The axiom audit distinguishes claims by role instead of labeling every useful construction an axiom.

The current minimal axiom set is

\[
\boxed{\mathrm{RA0}+\mathrm{RR1}}.
\]

**RA0 — relational admissibility**

\[
\operatorname{Adm}(x)
\Longrightarrow
\exists\,y,r:\operatorname{Rel}_r(x,y).
\]

An admitted observable is not defined independently of relation.

**RR1 — recursive relational closure**

A selected relational point may itself carry a further distinction. This is the explicit extra assumption that generates the fractal/refinement tower; it is not silently claimed to follow from RA0.

The minimal algebraic carrier is an unscaled point \(p\). Algebraic zero is not identified with absence of relation.

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
\mathcal A_{\sigma,n}^{p,q}(p_\omega)
\to
\mathcal A_{\tau,n+1}^{p,q}(p_{\omega\epsilon}).
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
(\mathcal A_{\sigma,n}^{p,q},+,0,-,\mathbb K\curvearrowright\mathcal A_{\sigma,n}^{p,q}).
\]

The abstract algebra does not fix \(\mathbb K=\mathbb C\). The reference kernel uses complex components. This structure is required before commutators, associators, and refinement residuals can be interpreted as differences. The executable zero of a reference element preserves its typed sector and satisfies \(X+0_X=X\) and \(X-X=0_X\).

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

Holding the residual signature fixed isolates a purely semantic shift:

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

## Relational transport and abstract holonomy

For a composable relation path

\[
\gamma=(r_1,\ldots,r_m),
\qquad
r_k:a_{k-1}\to a_k,
\]

the core transport is

\[
T_\gamma=T_{r_m}\circ\cdots\circ T_{r_1}.
\]

If the path is closed, \(a_m=a_0\), its abstract relational holonomy is the return transport

\[
\mathcal H_\gamma:=T_\gamma,
\]

with state residual

\[
\varepsilon_\gamma(X)=\|\mathcal H_\gamma X-X\|.
\]

This definition requires neither spacetime nor \(U(1)\). A separate transport-composition residual measures failure of direct and sequential transport to agree.

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

This is an imported **bridge**, not an axiom of the general algebra. A concrete realization may independently supply a map from closed relational holonomy into \(U(1)\). Phase turn-count and topological winding depend on that phase representation plus closure; they do not depend on Zero Axis. If an application additionally uses the companion Zero Axis bridge, a verified finite phase may be lifted through \(\Omega^{-1}(u)=u/(1+u)\), while \(u=-1\) is the compactified point at infinity.

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

See `docs/ARCHITECTURE.md` for module layering, `docs/RELATIONAL_POTENTIAL.md` for the semantic deformation scalar, `docs/AXIOM_AUDIT.md` for the typed dependency ledger, `docs/INDEPENDENCE_WITNESSES.md` for finite countermodels, `docs/COHERENCE_MATRIX.md` for compatibility laws, `docs/INDEXED_TENSOR_GATE.md` for the contraction/tensor realization boundary, `docs/MONOIDAL_COHERENCE_GATE.md` for the non-strict pentagon/hexagon boundary, and `docs/VALIDATION_STATUS.md` for current verification status.

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

The holonomy phase map

\[
\chi:\mathcal H_\gamma\to U(1)
\]

is a reference-realization question. The optional Zero Axis lift

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

Useful modes:

```text
python scripts/validate.py --tests-only
python scripts/validate.py --latex-only
python scripts/validate.py --require-latex
```

The default run executes pytest and then compiles the monograph when `latexmk` or `pdflatex` is installed. `--require-latex` converts a missing LaTeX toolchain from SKIP to FAIL.

See `docs/VALIDATION_STATUS.md` for the latest distinction between static checks and runtime execution.

## Development invariant

Every promoted primitive should have synchronized forms:

\[
\boxed{\text{definition}+\text{reference code}+\text{test}+\text{LaTeX}}.
\]


## One-axiom closure candidate

The current canonical foundation remains

\[
\mathrm{RA0}+\mathrm{RR1}.
\]

A stronger candidate has now been isolated:

\[
\boxed{
\mathrm{RA0}^{*}:
\text{every admitted carrier hosts an admitted non-degenerate binary distinction,}
}
\]

with the selected endpoint occurrences themselves admitted.

Under this stronger statement, recursive refinement follows by induction on path-labelled occurrences:

\[
\boxed{
\mathrm{RA0}^{*}\Rightarrow\mathrm{RR1}.
}
\]

This does **not** mean old RA0 implied RR1. RA0* explicitly adds binary non-degeneracy and endpoint admissibility. It also does not force ontically new carrier identities at each depth:

\[
\mathrm{RA0}^{*}\not\Rightarrow\mathrm{NOVELTY}.
\]

See `docs/AXIOM_CLOSURE_AUDIT.md`.
