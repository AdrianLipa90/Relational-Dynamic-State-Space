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

This is an imported **bridge**, not an axiom of the general algebra. Phase turn-count and residual are derived from phase paths. A topological winding number is asserted only after the path is explicitly verified closed.

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
