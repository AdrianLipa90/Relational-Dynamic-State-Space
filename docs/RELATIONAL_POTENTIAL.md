# Relational Deformation Potential

## Status

The relational deformation potential is a **derived scalar diagnostic** over an explicit residual signature.

It is not assumed to be physical energy, mass, gravitational potential, or metric curvature.

## Residual signature

Choose a finite named residual signature

\[
D(X)
=
\{d_i(X)\}_{i\in I},
\qquad
d_i(X)\ge 0.
\]

The names in \(I\) are part of the type contract. Changing the signature changes the diagnostic itself.

## Semantic weighting

A semantic profile at scale/context \(\sigma\) supplies explicit non-negative weights

\[
W_\sigma
=
\{w_{\sigma i}\}_{i\in I},
\qquad
w_{\sigma i}\ge 0,
\]

with at least one positive weight.

The weights are **not inferred from the label \(\sigma\)** by the current kernel. They are supplied structural data.

This distinction is essential:

\[
\boxed{
\text{semantic label}
\neq
\text{semantic weighting law}.
}
\]

## Potential

For \(p\ge 1\),

\[
\boxed{
V_R^{(p)}(X\mid\sigma)
=
\left(
\sum_{i\in I}
w_{\sigma i}\,d_i(X)^p
\right)^{1/p}.
}
\]

The reference implementation fails closed if:

- the residual signature does not match the profile;
- a residual is negative or non-finite;
- a weight is negative or non-finite;
- all weights vanish;
- \(p<1\) or is non-finite.

## Pure semantic deformation

If the numerical residual signature \(D(X)\) is held fixed while the semantic profile changes from \(\sigma\) to \(\tau\), define

\[
\boxed{
\Delta_{\sigma\to\tau}V_R(X)
=
V_R^{(p)}(X\mid\tau)
-
V_R^{(p)}(X\mid\sigma).
}
\]

Thus the same represented algebraic state and the same measured residuals can acquire a different scalar diagnostic solely because the supplied semantic weighting changed.

This is the formal version of a semantic scalar deformation.

## Relational attractor set

For a finite admissible candidate set \(\mathcal C\), let each candidate \(c\) have potential \(V_R(c)\). Define

\[
\boxed{
\operatorname{Attr}_R(\mathcal C)
=
\operatorname*{arg\,min}_{c\in\mathcal C}
V_R(c).
}
\]

The reference implementation preserves ties. It does not invent an arbitrary winner.

## Geometry boundary

The general algebra does **not** identify \(V_R\) with geometric curvature.

A geometric realization may later supply a separate map such as

\[
\mathcal G:
V_R
\longmapsto
\delta g
\]

or another deformation observable, but such a map would be an additional realization/bridge and requires its own definition, implementation, tests, and LaTeX statement.

Therefore the current implication is only

\[
\boxed{
\text{residual signature}
+
\text{semantic weighting}
\longrightarrow
\text{relational deformation scalar}.
}
\]

No physical interpretation is forced by this construction.
