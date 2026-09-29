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

Exact self-similarity is not assumed. Its failure is measured by

\[
\Delta_F(X,Y)
=
F(X\star Y)-F(X)\star F(Y).
\]

## Additive tensor-scalar sectors

Each typed sector carries an additive module structure over a scalar domain \(\mathbb K\):

\[
(\mathcal A_{\sigma,n}^{p,q},+,0,-,\mathbb K\curvearrowright\mathcal A_{\sigma,n}^{p,q}).
\]

The abstract algebra does not fix \(\mathbb K=\mathbb C\). The reference kernel uses complex components. This structure is required before commutators, associators, and refinement residuals can be interpreted as differences. The executable zero of a reference element preserves its typed sector and satisfies \(X+0_X=X\) and \(X-X=0_X\).

## Product and orbital coherence

The relational product is not assumed bilinear. Additivity and scalar-linearity residuals are measured explicitly; exact \(\mathbb K\)-bilinearity is the zero-defect subclass.

Likewise, \(U_g\) is first an indexed family of orbital operators. Exact group action requires vanishing identity, inverse, and composition residuals. Relative Moiré

\[
M_{ij}=U_iU_j^{-1}
\]

is only claimed where the supplied inverse passes its coherence check.

## Semantic scales

Semantic scale is not assumed to be one real number. It lives in a typed scale structure \(\Sigma\), represented in the reference kernel by an acyclic coarse-graining graph.

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

This is an imported **bridge**, not an axiom of the general algebra. It supplies a phase realization of the more general relational holonomy. Phase turn-count and residual are derived from phase paths. A topological winding number is asserted only after the path is explicitly verified closed.

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

See `docs/AXIOM_AUDIT.md` for the typed dependency ledger and `docs/INDEPENDENCE_WITNESSES.md` for finite countermodels establishing the current non-implications.

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
