# Relational Dynamic State Space (RDSS)

RDSS is a mathematical and computational framework that keeps three layers explicit and separate:

1. **Time algebra / dynamics** — operators define ordered state transitions.
2. **Hilbert–Moiré space** — a geometric carrier for admissible states, with a hyperoctagonal-lattice interface.
3. **Relational semantics** — semantic features produce an explicit scalar attachment \(\chi\) that deforms the state-space metric.

The central structural object is

\[
\mathfrak A_T \curvearrowright
\left(\mathcal H_{\mathrm{HM}}, g[\chi(\mathrm{Sem}(\mathcal R,\Psi))]\right).
\]

Arithmetic truth and geometric embedding are deliberately separated. For example, the algebraic statement

\[
2+2=4
\]

remains invariant, while the representation of that relation may generate a non-zero semantic scalar \(\chi\), and therefore a deformed metric

\[
g' = e^{2\chi} g.
\]

This repository does **not** assume that the resulting attractors are physical mass or that relational deformation is physical gravity. Those are possible later interpretations only after independent mathematical and empirical gates.

## Core vocabulary

- **Relational attachment** \(\mathcal N_{\rm rel}\): map from explicit relational/semantic features to a scalar deformation parameter \(\chi\).
- **Page attractor** \(\mathcal A_{\rm page}\): a stable state/metric configuration under the coupled update rule.
- **Time algebra** \(\mathfrak A_T\): ordered dynamics acting on admissible states.
- **Hilbert–Moiré space** \(\mathcal H_{\rm HM}\): geometric state carrier with a replaceable lattice/topology backend.
- **Dynamic state space**: the coupled triple \((\mathcal H_{\rm HM},\mathfrak A_T,\rho)\) with semantic metric feedback.

## Status

`v0.1-foundation` is intentionally minimal. It establishes interfaces, invariants, tests, and a matching LaTeX monograph before any stronger physical interpretation is admitted.
