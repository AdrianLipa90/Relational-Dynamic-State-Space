# OFHM Prefix Completion and Geometric No-Go

Status: SYMBOLIC_COMPLETION_CLOSED / EUCLIDEAN_EMBEDDING_SEPARATE

## Scope

The finite OFHM address carrier is

\[
\mathcal A_F=\mathbb Z^{<\omega}.
\]

The Hilbert-Hotel rank is an explicit enumeration coordinate and is not used
to define geometry. The intrinsic combinatorial relation is prefix extension.

## Prefix ultrametric

For finite words \(a,b\), let \(L(a,b)\) be maximal common-prefix length.
For any fixed \(\beta>1\), define

\[
d_\beta(a,b)=
\begin{cases}
0,&a=b,\\
\beta^{-L(a,b)},&a\ne b.
\end{cases}
\]

This is an ultrametric because

\[
L(x,z)\ge\min\{L(x,y),L(y,z)\},
\]

hence

\[
d_\beta(x,z)
\le
\max\{d_\beta(x,y),d_\beta(y,z)\}.
\]

The topology is independent of the particular finite \(\beta>1\): it is the
standard prefix/cylinder topology.

## Completion

For an infinite integer branch

\[
a=(a_1,a_2,\ldots)\in\mathbb Z^\omega,
\]

let \(a|_n\) be its length-\(n\) prefix. For \(m,n\ge N\),

\[
d_\beta(a|_m,a|_n)\le\beta^{-N},
\]

so prefixes form a Cauchy sequence.

Conversely, a non-eventually-stationary Cauchy sequence of finite words fixes,
for each depth \(N\), one eventual common prefix of length \(N\). These
compatible prefixes determine one unique element of \(\mathbb Z^\omega\).

Therefore the metric completion adds exactly the infinite branches:

\[
\boxed{
\widehat{\mathbb Z^{<\omega}}
=
\mathbb Z^{<\omega}
\sqcup
\mathbb Z^\omega.
}
\]

The added boundary is the countable-alphabet Baire space

\[
\boxed{\partial\mathcal A_F=\mathbb Z^\omega.}
\]

This is a symbolic/topological completion. It is not a Euclidean embedding.

## Noncompactness

Distinct first-level children

\[
(k),\qquad k\in\mathbb Z,
\]

have pairwise distance one. Thus for any radius below one, infinitely many
balls are required to cover them. The completion is not totally bounded and
therefore is not compact.

## Hausdorff dimension

For every finite \(m\ge2\), restrict the alphabet to an \(m\)-element subset.
The resulting full-shift boundary is an isometric subspace with

\[
\dim_H
=
\frac{\ln m}{\ln\beta}.
\]

Because these lower bounds are unbounded as \(m\to\infty\),

\[
\boxed{
\dim_H(\mathbb Z^\omega,d_\beta)=\infty.
}
\]

Thus OFHM does have an exact Hausdorff-dimension statement for its intrinsic
prefix metric: the dimension is infinite, not an unspecified fitted finite
number.

## Measure no-go

A probability distribution on the countably infinite first-level alphabet
that is invariant under every branch-label permutation would assign one mass
\(p\) to every integer label.

If \(p=0\), total mass is zero. If \(p>0\), the sum diverges. Hence

\[
\boxed{
\text{no uniform permutation-invariant branch probability exists}.
}
\]

Non-uniform product, Markov or Gibbs measures can be introduced only after
supplying extra weights/dynamics. Therefore the symbolic algebra does not
force a unique continuum probability measure.

## Geometric embedding firewall

Any map

\[
E:\mathbb Z^\omega\to X
\]

into a Euclidean, complex, manifold, Hilbert or other geometric target is an
additional realization. Convergence, compactness and image dimension depend
on \(E\).

Accordingly, the historical
\`GATE_OFHM_GEOMETRIC_FRACTAL_LIMIT\` is closed by two exact results:

1. the intrinsic symbolic completion is known;
2. a universal Euclidean geometric fractal and unique continuum measure do
   not follow from the symbolic carrier alone.

A chosen geometric embedding is tracked by
\`BRIDGE_OFHM_GEOMETRIC_EMBEDDING\`, not by a hidden theorem.

## Executable receipt

- \`src/rdss/ofhm_prefix_completion.py\`
- \`tests/test_ofhm_prefix_completion.py\`
- \`THM_OFHM_SYMBOLIC_COMPLETION_BAIRE_BOUNDARY\`
- \`THM_OFHM_PREFIX_COMPLETION_NONCOMPACT\`
- \`THM_OFHM_PREFIX_BOUNDARY_INFINITE_HAUSDORFF_DIMENSION\`
- \`THM_OFHM_NO_UNIQUE_CONTINUUM_MEASURE\`
- historical \`GATE_OFHM_GEOMETRIC_FRACTAL_LIMIT\` promoted to theorem-level
  closure.
