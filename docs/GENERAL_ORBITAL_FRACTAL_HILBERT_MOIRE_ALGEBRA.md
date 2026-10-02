# General Orbital-Fractal Hilbert-Moiré Algebra

Status: STRUCTURAL ALGEBRA CLOSED / PHYSICAL REALIZATION EXTERNAL

This document specifies the finite symbolic and relational phase layer of RDSS.
It adds no foundational law.

## 1. Frozen source provenance

The executable layer keeps the following source parents pinned:

- Infinities:
  \`339d6c58f3e7d86c67a4f758cd7416692f8f8280\`;
- GREMLIN:
  \`b0000828238e0cd244f5eb1fb679155315df372f\`;
- Informational Dynamics of Metatime:
  \`31f1a74d65aeb5e107840fa9971b335c7f339504\`;
- TIR foundation/dynamics parent used by the later closure:
  \`9783782570a2ccfa1fc42c99b605dad48e02aa78\`.

The executable source is
\`src/rdss/orbital_fractal_hilbert_moire.py\`.

## 2. Finite countable branch carrier

The OFHM symbolic refinement carrier is

\[
\boxed{
\mathcal A_{\rm F}
=
\mathbb Z^{<\omega}.
}
\]

An element is a finite integer word

\[
a=(k_1,\ldots,k_n).
\]

The binary RDSS occurrence carrier embeds by preserving branch labels:

\[
\{-1,+1\}^{<\omega}
\hookrightarrow
\mathbb Z^{<\omega}.
\]

This is a symbolic address. It is not automatically a geometric point.

## 3. Euler branch realization

On the declared complex logarithm branch,

\[
\mathcal E(z)=e^{i\pi z}
\]

has inverse branches

\[
\boxed{
\mathcal E_k^{-1}(w)
=
2k-\frac{i}{\pi}\operatorname{Log}(w),
\qquad
k\in\mathbb Z.
}
\]

Finite inverse compositions therefore carry finite integer branch addresses.

This supplies symbolic branching. It does not by itself supply an external
metric fractal.

## 4. Hilbert-Hotel enumeration

An explicit bijection

\[
\rho:\mathbb Z^{<\omega}\leftrightarrow\mathbb N
\]

provides a Hilbert-Hotel successor

\[
\boxed{
S_{\rm HH}(a)
=
\rho^{-1}(\rho(a)+1).
}
\]

The executable zigzag/Cantor ranking is one declared enumeration coordinate.
It is not claimed to be the unique canonical enumeration.

Local refinement

\[
R_k(a)=a\frown k
\]

and Hilbert-Hotel shift are distinct operations:

\[
\boxed{
R_k\neq S_{\rm HH}.
}
\]

No commutation law between them is silently assumed.

## 5. Relative phase and Moiré cocycle

For scalar phase coordinates,

\[
U_i=e^{i\theta_i},
\]

define

\[
\boxed{
M_{ij}
=
U_iU_j^{-1}
=
e^{i(\theta_i-\theta_j)}.
}
\]

Then

\[
\boxed{
M_{ij}M_{jk}=M_{ik},
\qquad
M_{ii}=1,
\qquad
M_{ji}=M_{ij}^{-1}.
}
\]

This is the exact finite Moiré phase cocycle.

The BEES coherence magnitude

\[
C(X,Y)
=
\left|
\frac1d
\sum_{r=1}^{d}
e^{i(\theta_r^X-\theta_r^Y)}
\right|
\]

is a lossy diagnostic because of the final absolute value. It is never used
to reconstruct the signed/complex relative phase.

## 6. Hilbert-fibre transport

For a finite Hilbert vector \(v\), define

\[
\boxed{
T_{ij}v=M_{ij}v.
}
\]

Since \(M_{ij}\in U(1)\),

\[
\|T_{ij}v\|=\|v\|,
\]

and cocycle composition gives

\[
\boxed{
T_{ij}T_{jk}=T_{ik}.
}
\]

Thus Hilbert transport is downstream of the Moiré cocycle and adds no
independent phase law.

## 7. Finite OFHM state

The finite executable state is

\[
\boxed{
\Psi=(a,\ell,\theta,v,\omega),
}
\]

where

- \(a\in\mathbb Z^{<\omega}\) is the finite symbolic address;
- \(\ell\) is an orbital label;
- \(\theta\in\mathbb R/2\pi\mathbb Z\) is phase;
- \(v\neq0\) is a finite Hilbert vector;
- \(\omega\) is the angular-velocity coordinate used by the second-order chart.

## 8. Alternating half-time dynamics

The exact Stella half-successor is

\[
H(n,+)=(n,-),
\qquad
H(n,-)=(n+1,+),
\]

so

\[
\boxed{H^2=S.}
\]

Occurrence order is discrete in half-frames while the internal phase remains
continuous on \(U(1)\).

The bipolar exchange orbit contains 24 directed incidences and 12 undirected
exchange pairs. With

\[
\kappa=\frac{\ln2}{24\pi},
\]

one directed channel carries

\[
\frac{\ln2}{24}
=
\pi\kappa,
\]

and one undirected pair carries

\[
\frac{\ln2}{12}.
\]

## 9. Canonical pair potential

For projected mismatch

\[
\Delta_{ij}
=
\theta_i-\theta_j-\Gamma_{ij},
\]

the normalized squared chordal mismatch is

\[
c(\Delta)
=
\frac{|e^{i\Delta}-1|^2}{4}
=
\frac{1-\cos\Delta}{2}.
\]

It obeys

\[
c(0)=0,
\qquad
c(\pi)=1.
\]

Hence the pair information budget fixes

\[
\boxed{
V_{ij}
=
\pi\kappa
\left(1-\cos\Delta_{ij}\right)
=
\frac{\ln2}{24}
\left(1-\cos\Delta_{ij}\right).
}
\]

At the half-turn,

\[
V_{ij}(\pi)=\frac{\ln2}{12}.
\]

Twelve maximally mismatched pairs therefore saturate the binary budget:

\[
\boxed{
12V_{ij}(\pi)=\ln2.
}
\]

## 10. Pendulum and relational zero

For a bipolar pair,

\[
F_+
=
-\pi\kappa\sin\Delta,
\qquad
F_-
=
+\pi\kappa\sin\Delta,
\]

so

\[
\boxed{
F_++F_-=0.
}
\]

With equal phase inertia \(I_\phi>0\) and damping \(\eta\ge0\),

\[
\boxed{
I_\phi\ddot c+\eta\dot c=0
}
\]

for the center coordinate and

\[
\boxed{
I_\phi\ddot\Delta
+
\eta\dot\Delta
+
2\pi\kappa\sin\Delta
=
0
}
\]

for the relative coordinate.

The local force is a potential gradient; inertia belongs to the composed
two-sector/full-successor dynamics.

## 11. Frame-native second difference

The unique local linear three-frame stencil, up to overall scale, that
annihilates constants and uniform drift is

\[
\boxed{
D_2x_n
=
x_{n+1}-2x_n+x_{n-1}.
}
\]

Therefore the conservative full-frame relative equation is

\[
\boxed{
I_\phi
\frac{
\Delta_{n+1}-2\Delta_n+\Delta_{n-1}
}{h^2}
+
2\pi\kappa\sin\Delta_n
=
0.
}
\]

The structural successor scale \(h\) is dimensionless until a physical clock
calibration is supplied.

## 12. Moiré-Kuramoto closure

For an undirected phase graph,

\[
\boxed{
V_{\rm M}
=
\pi\kappa
\sum_{\{i,j\}\in E}
\left(1-\cos\Delta_{ij}\right).
}
\]

Differentiation produces the sine interaction kernel.

The inertial equation is

\[
I_i\ddot\theta_i
+
\eta_i\dot\theta_i
+
\frac{\partial V_{\rm M}}{\partial\theta_i}
=
0.
\]

In the overdamped limit,

\[
\boxed{
\eta_i\dot\theta_i
=
-
\frac{\partial V_{\rm M}}{\partial\theta_i},
}
\]

which is the gauge-twisted Kuramoto flow generated by the same potential.

Thus

\[
\boxed{
\text{pendulum}
=
\text{two-sector inertial reduction},
}
\]

and

\[
\boxed{
\text{Kuramoto}
=
\text{overdamped network reduction}.
}
\]

## 13. Canonical symbolic infinite boundary

The finite prefix carrier determines the ideal symbolic boundary

\[
\boxed{
\partial_{\rm sym}\mathcal A_{\rm F}
=
\mathbb Z^{\mathbb N}
}
\]

with the finite-prefix cylinder topology.

Because \(\mathbb Z\) is countably infinite and discrete,
\(\mathbb Z^{\mathbb N}\) is Baire space up to a fixed bijection
\(\mathbb Z\leftrightarrow\mathbb N\).

The first-symbol cylinders

\[
C_k=\{x:x_0=k\},
\qquad k\in\mathbb Z,
\]

form a countable clopen cover with no finite subcover. Hence

\[
\boxed{
\mathbb Z^{\mathbb N}
\text{ is not compact}.
}
\]

The canonical boundary is therefore symbolic/topological, not a forced compact
geometric fractal.

## 14. Geometric-limit no-go theorem

### 14.1 Measure non-uniqueness

For every \(b>1\),

\[
p_b(k)
=
\frac{b-1}{b+1}
b^{-|k|}
\]

is a normalized full-support probability distribution on \(\mathbb Z\).

Its product measure \(\mu_b\) lives on the same cylinder topology.

But

\[
\mu_2([0])=\frac13,
\qquad
\mu_3([0])=\frac12.
\]

Therefore

\[
\boxed{
\text{OFHM prefix structure does not select a unique continuum measure}.
}
\]

### 14.2 Metric scale non-uniqueness

For \(0<\lambda<1\), define the compatible prefix ultrametric

\[
d_\lambda(x,y)
=
\lambda^{N(x,y)}
\]

for \(x\neq y\), where \(N(x,y)\) is common-prefix length.

The finite symbolic algebra does not select \(\lambda\).

On the embedded binary boundary \(\{-1,+1\}^{\mathbb N}\),

\[
\dim_H
=
\frac{\ln2}{-\ln\lambda}.
\]

Thus

\[
\lambda=\frac12
\Rightarrow
\dim_H=1,
\]

while

\[
\lambda=\frac14
\Rightarrow
\dim_H=\frac12.
\]

Hence

\[
\boxed{
\text{prefix topology alone does not select a canonical Hausdorff dimension}.
}
\]

### 14.3 External geometric convergence

The OFHM structural signature contains no canonical map

\[
\Phi:\mathbb Z^{\mathbb N}\to X
\]

into a metric geometric space \(X\), and no contraction system selecting such
a map.

Therefore convergence of an infinite symbolic address to an external
geometric point is not a well-typed intrinsic statement until a geometric
realization is supplied.

The historical
\`GATE_OFHM_GEOMETRIC_FRACTAL_LIMIT\`
is therefore closed by no-go:

\[
\boxed{
\text{canonical symbolic boundary exists}
\quad\land\quad
\text{unique geometric fractal realization is underdetermined}.
}
\]

## 15. Physical realization is an evidence frontier

The structural algebra contains no unique map to a named material, quantum,
spacetime or measurement substrate and contains no dimensional calibration
data.

Therefore physical substrate selection is not another mathematical theorem to
derive from OFHM alone.

The historical identifier

\`GATE_OFHM_PHYSICAL_BINDING\`

has status

\[
\boxed{
\texttt{EVIDENCE\_GATE},
}
\]

not \`DERIVATION_GATE\`.

A physical claim requires:

1. an explicit realization map;
2. dimensional calibration;
3. empirical or independently sourced evidence;
4. falsifiable comparison with observation.

## 16. Closure status

Internal structural derivation gates:

\[
\boxed{
N_{\rm DERIVATION\_GATE}=0.
}
\]

External empirical frontier:

\[
\boxed{
N_{\rm EVIDENCE\_GATE}=1.
}
\]

The remaining evidence gate is exactly

\[
\boxed{
\texttt{GATE\_OFHM\_PHYSICAL\_BINDING}.
}
\]

This is not counted as an unresolved mathematical proof obligation.

## 17. Executable surfaces

- \`src/rdss/orbital_fractal_hilbert_moire.py\`
- \`src/rdss/alternating_phase_dynamics.py\`
- \`tests/test_orbital_fractal_hilbert_moire.py\`
- \`tests/test_alternating_phase_dynamics.py\`
- \`src/rdss/axioms.py\`

The geometric-limit no-go receipt is

\`ofhm_geometric_limit_no_go_certificate()\`.

The pendulum/Moiré-Kuramoto receipt is

\`alternating_phase_closure_certificate()\`.

## 18. Proof discipline

No specific compact fractal, measure, dimension or physical substrate is
silently inserted.

A chosen geometric realization may be added later as a separately typed
reference/bridge structure.

A chosen physical realization requires evidence and remains external to
structural proof closure.
