# Relational center, Hilbert--Moire carrier and information operator gate

Status: **STRUCTURAL BRIDGE / REFERENCE REALIZATION / NOT A NEW CORE AXIOM**

This document extends the existing RTOFA/RDSS algebra without replacing its
current foundation, occurrence semantics, Moire operator, holonomy machinery,
Zero-Axis bridge or CP1 reference realization.

## Foundational motivation

The motivating relational statement is retained verbatim:

> nic z definicji nie może istnieć gdyż nie ma do czego się odnieść

Within RDSS this sentence is not silently promoted above the existing META0,
RA0 and RR1 classification. The executable consequences added here begin only
after a normalized dual coordinate is explicitly supplied.

## Relational center

Let

\[
p\in[0,1],
\qquad
\mathcal J:p\mapsto1-p.
\]

Define the centered coordinate

\[
\boxed{Z=2p-1}.
\]

Then

\[
Z(\mathcal Jp)=-Z(p)
\]

and the unique self-dual point is

\[
\boxed{p=\frac12\iff Z=0}.
\]

The notation

\[
\boxed{\frac12=0_R}
\]

means only this coordinate identity: the external midpoint \(p=1/2\) is the
zero of the centered relational chart. It is not the arithmetic equality
\(1/2=0\).

## Center-to-half-turn bridge

RDSS already distinguishes abstract relational structure from optional U(1)
realizations. Therefore the numerical occurrence of \(1/2\) in the balance
coordinate is not by itself identified with a displacement \(q=1/2\) on the
phase circle.

The bridge is made explicit:

\[
B_{0\to\pi}:
p=\frac12
\longmapsto
q=\frac12
\in\mathbb R/\mathbb Z.
\]

Under the normalized phase chart

\[
U(q)=e^{2\pi iq},
\]

the bridge image is

\[
\boxed{U(1/2)=-1}.
\]

This is a **BRIDGE datum/reference realization**. A future derivation of this
bridge from more primitive orbital structure must prove the required
orientation, positive quadratic form and continuous norm-preserving action.

In particular the stronger claim

\[
K^2=-I
\]

is not silently promoted here. When an oriented two-dimensional real
inner-product carrier with compatible complex structure \(K\) is supplied,

\[
e^{\phi K}
=
\cos\phi\,I+\sin\phi\,K
\]

realizes

\[
SO(2)\cong U(1).
\]

The upstream forcing of that structure remains a separate gate.

## Hilbert--Moire carrier

The existing RDSS occurrence/refinement structure supplies the discrete
layer/address variable. A compatible abstract layered Hilbert carrier may be
written

\[
\boxed{
\mathcal H_{\rm HM}
=
\int_F^\oplus \mathcal H_x\,d\mu_F(x)
}
\]

when a refinement space \(F\), measure \(\mu_F\), and measurable Hilbert
fibres \(\mathcal H_x\) are supplied.

A finite executable chart is represented by

\[
\Psi_{\omega,\ell,q}
=
(\omega,\ell,q,v),
\]

where

- \(\omega\) is an existing RDSS occurrence address;
- \(\ell\) is an orbital label;
- \(q\in\mathbb R\) is a normalized U(1) turn coordinate modulo integer turns;
- \(v\neq0\) is a finite Hilbert vector.

This is implemented as HilbertMoireFibreState. It is a finite fibre chart,
not a claim that the direct-integral measure theory follows from the RDSS core.

For two fibre states \(i,j\), the U(1) relative Moire phase is

\[
\boxed{
M_{ij}^{U(1)}
=
U(q_i)U(q_j)^{-1}
=
e^{2\pi i(q_i-q_j)}.
}
\]

This is the phase-fibre realization of the already existing RDSS derived
relative orbital action \(M_{ij}=U_iU_j^{-1}\).

For equal amplitudes,

\[
A e^{2\pi iq_i}+A e^{2\pi iq_j}
=
2A
e^{2\pi i(q_i+q_j)/2}
\cos\bigl(\pi(q_i-q_j)\bigr).
\]

Thus mean phase and half-difference are exact two-layer coordinates.

## Information operator

Balanced binary information is

\[
\boxed{
I_\star
=
H_2(1/2)
=
\ln2.
}
\]

The canonical project normalization uses the reference incidence count

\[
N_F=3,
\qquad
\dim\mathfrak{su}(3)=3^2-1=8,
\]

hence

\[
\boxed{
N_{\rm mix}=3(3^2-1)=24.
}
\]

RDSS records this as a **reference normalization**, not as a theorem derived
from META0/RA0/RR1.

With one normalized half-turn per channel,

\[
\Delta q_\star=\frac12,
\]

the total normalized turn measure is

\[
\boxed{
Q_{\rm mix}
=
24\cdot\frac12
=
12.
}
\]

Therefore

\[
\boxed{
\kappa_q
=
\frac{I_\star}{Q_{\rm mix}}
=
\frac{\ln2}{12}.
}
\]

The information one-form in normalized-turn coordinates is

\[
\boxed{
d\mathcal I
=
\kappa_q\,dq.
}
\]

For the radian chart

\[
\phi=2\pi q,
\qquad
dq=\frac{d\phi}{2\pi},
\]

so

\[
\boxed{
d\mathcal I
=
\kappa_\phi\,d\phi,
\qquad
\kappa_\phi
=
\frac{\ln2}{24\pi}.
}
\]

The repository-wide canonical radian constant is therefore

\[
\boxed{
\kappa
\equiv
\kappa_\phi
=
\frac{\ln2}{24\pi}.
}
\]

## Dependency classification

**EXACT / DERIVED INSIDE THE DECLARED CHART**
- \(Z=2p-1\);
- \(p=1/2\iff Z=0\);
- \(U(q)=e^{2\pi iq}\);
- \(q=1/2\Rightarrow U=-1\);
- \(3(3^2-1)=24\);
- \(24(1/2)=12\);
- \(\kappa_q=\ln2/12\);
- \(\phi=2\pi q\Rightarrow\kappa_\phi=\ln2/(24\pi)\);
- equal-amplitude two-layer Moire factorization.

**REFERENCE REALIZATION / BRIDGE**
- the map from relational-center coordinate \(p=1/2\) to orbital displacement
  class \(q=1/2\);
- the Hilbert--Moire direct-integral carrier;
- the canonical 3-by-8 incidence normalization.

**OPEN**
- deriving the center-to-half-turn bridge without supplying it;
- deriving \(K^2=-I\), orientation and compatible positive metric solely from
  the current minimal RDSS foundation;
- any sector-specific physical interpretation of \(\kappa\) or
  \(\mathcal H_{\rm HM}\).

No existing RDSS core axiom is replaced by this gate.
