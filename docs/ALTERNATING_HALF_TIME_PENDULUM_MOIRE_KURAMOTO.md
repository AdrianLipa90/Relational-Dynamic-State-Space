# Alternating Half-Time, Pendulum and Moire-Kuramoto Closure

Status: STRUCTURAL_DYNAMICS_CLOSED / PHYSICAL_CLOCK_AND_SUBSTRATE_BINDING_SEPARATE

## Frozen parents

- RDSS parent main:
  `e1d2dda2ffbcbb38392869f94012cea03fffd751`
- TIR main:
  `9783782570a2ccfa1fc42c99b605dad48e02aa78`

TIR source surfaces:

- `TIR/foundations/TIR_PRESPACETIME_STELLA_HALF_SUCCESSOR_V0_1.md`
- `TIR/foundations/TIR_STELLA_ALTERNATING_ROTATION_INFERENCE_V0_1.md`
- `TIR/foundations/TIR_RELATIONAL_PHASE_LAGRANGIAN_CORE_V0_1.md`
- `TIR/foundations/TIR_WHITE_THREAD_SPIN_LIFT_LYAPUNOV_V0_1.md`
- `TIR/foundations/TIR_KAPPA_FLAVOUR_MIXING_NORMALIZATION_V0_1.md`

## 1. Half-time is structural order, not half of an assumed clock

The TIR pretime carrier is

\[
\mathcal X=\mathbb N_0\times{+,-}
\]

with

\[
H(n,+)=(n,-),
\qquad
H(n,-)=(n+1,+).
\]

Therefore

\[
\boxed{H^2=S}.
\]

The normalized occurrence grade is

\[

u(n,+)=n,
\qquad

u(n,-)=n+\frac12.
\]

Hence one application of (H) advances the structural order by (1/2),
while two complementary applications give one full successor.

The internal phase state is not discretized by this statement:

\[
\thetainmathbb R/2pimathbb Z.
\]

Thus the exact structural split is

\[
\boxed{
\text{occurrence order: discrete half-frames}
\qquad
\text{phase state: continuous }U(1).
}
\]

This is the precise meaning of frame-like but fuzzy phase time at the present
layer.

The pretime half-index and the (U(1)) half-turn are separately typed. Their
common numerical value (1/2) is not used as an unstated semantic
identification.

## 2. Information budget per directed channel and per paired exchange

The closed bipolar channel orbit contains

\[
N_{\to}=24
\]

directed incidences and

\[
N_{\leftrightarrow}=12
\]

undirected exchange pairs.

The total binary source information is

\[
I_*=\ln2.
\]

Therefore one directed incidence carries the invariant information share

\[
\boxed{
I_{\to}=\frac{\ln2}{24}.
}
\]

Because

\[
\kappa=\frac{\ln2}{24\pi},
\]

this is equivalently

\[
\boxed{
I_{\to}=\pi\kappa.
}
\]

One undirected pair contains the two opposite directed incidences, hence

\[
\boxed{
I_{\leftrightarrow}
=
2I_{\to}
=
\frac{\ln2}{12}
=
2\pi\kappa.
}
\]

## 3. Canonical chordal mismatch fixes the pair potential

For a projected (U(1)) mismatch

\[
\Delta=\theta_i-\theta_j-\Gamma_{ij},
\]

the squared chordal distance on the unit circle is

\[
|e^{iDelta}-1|^2
=
2-2\cos\Delta.
\]

Normalize it to the interval ([0,1]):

\[
\boxed{
c(\Delta)
=
\frac{|e^{iDelta}-1|^2}{4}
=
\frac{1-\cos\Delta}{2}.
}
\]

Then

\[
c(0)=0,
\qquad
c(\pi)=1.
\]

Thus the half-turn exactly saturates the paired exchange mismatch scale.

Multiplying by the already fixed information budget of one undirected pair
gives

\[
V_{\leftrightarrow}(\Delta)
=
I_{\leftrightarrow}c(\Delta).
\]

Therefore

\[
\boxed{
V_{\leftrightarrow}(\Delta)
=
\frac{\ln2}{24}(1-\cos\Delta)
=
\pi\kappa(1-\cos\Delta).
}
\]

No free coupling amplitude remains in this canonical information-normalized
pair potential.

At the half-turn,

\[
\boxed{
V_{\leftrightarrow}(\pi)
=
\frac{\ln2}{12}.
}
\]

Consequently twelve maximally mismatched exchange pairs give

\[
12V_{\leftrightarrow}(\pi)
=
\boxed{\ln2}.
\]

This is an independent normalization closure check.

## 4. Opposite gradients and the relational zero

Write

\[
\Delta=\theta_+-\theta_- - \Gamma.
\]

Let

\[
A_*=\frac{\ln2}{24}=\pi\kappa.
\]

Then

\[
V=A_*(1-\cos\Delta).
\]

The gradients are

\[
\frac{\partial V}{\partial\theta_+}
=
A_*\sin\Delta,
\]

\[
\frac{\partial V}{\partial\theta_-}
=
-A_*\sin\Delta.
\]

The relational forces are therefore

\[
\boxed{
F_+
=
-A_*\sin\Delta,
\qquad
F_-
=
+A_*\sin\Delta.
}
\]

Hence

\[
\boxed{
F_++F_-=0.
}
\]

The interaction can change the relative coordinate but cannot accelerate the
center mode.

This is the exact algebraic meaning of inertia with respect to the relational
zero at this layer.

## 5. Pendulum closure

Use the already promoted TIR phase inertia (I_phi>0), and optionally an
equal Rayleigh coefficient (etage0) on each of the two sectors.

Define center and relative coordinates

\[
c=\frac{\theta_++\theta_-}{2},
\qquad
\Delta=\theta_+-\theta_-.
\]

Adding the two sector equations gives

\[
\boxed{
I_phiddot c+etadot c=0.
}
\]

Subtracting gives

\[
\boxed{
I_phi\ddot\Delta
+
\eta\dot\Delta
+
2A_*\sin\Delta
=
0.
}
\]

Since \(A_*=\pi\kappa\),

\[
\boxed{
I_phi\ddot\Delta
+
\eta\dot\Delta
+
2\pi\kappa\sin\Delta
=
0.
}
\]

Equivalently, with reduced inertia and damping

\[
\mu=\frac{I_phi}{2},
\qquad
\gamma=\frac{\eta}{2},
\]

the same equation is

\[
\boxed{
\mu\ddot\Delta
+
\gamma\dot\Delta
+
\pi\kappa\sin\Delta
=
0.
}
\]

This is the standard pendulum equation on the relative phase coordinate.

The conservative core (eta=0) has

\[
\ddot c=0,
\]

so the center is inertial while the relative phase oscillates in the forced
periodic potential.

## 6. Frame-native inertia

The full successor is

\[
S=H^2.
\]

Consider a local linear three-frame inertial operator

\[
D_2x_n
=
a x_{n-1}+b x_n+c x_{n+1}.
\]

Requiring it to annihilate constants gives

\[
a+b+c=0.
\]

Requiring it also to annihilate uniform drift (x_n=alpha n+\beta) gives

\[
c=a.
\]

Therefore

\[
b=-2a.
\]

Up to one overall scale, the unique local operator is

\[
\boxed{
D_2x_n
=
x_{n+1}-2x_n+x_{n-1}.
}
\]

Thus on a normalized full-successor spacing (h),

\[
\boxed{
I_phi
\frac{
\Delta_{n+1}-2\Delta_n+\Delta_{n-1}
}{h^2}
+
2\pi\kappa\sin\Delta_n
=
0.
}
\]

The occurrence index is discrete; (Delta_n) is still a continuous phase
representative. Physical seconds are not assumed. A dimensional clock
calibration of (h) remains downstream.

## 7. Moire potential

For an undirected Moire graph with gauge-reduced edge mismatch

\[
\Delta_{ij}
=
\theta_i-\theta_j-\Gamma_{ij},
\]

define the canonical information potential

\[
\boxed{
V_{\rm M}
=
\pi\kappa
\sum_{{i,j}in E}
\left(
1-\cos\Delta_{ij}
\right).
}
\]

For each edge,

\[
\partial_{\theta_i}V_{ij}
=
\pi\kappa\sin\Delta_{ij},
\qquad
\partial_{\theta_j}V_{ij}
=
-\pi\kappa\sin\Delta_{ij}.
\]

Thus the network force is automatically a sine-coupling force. No independent
Kuramoto sine ansatz is required.

A common phase shift

\[
\theta_imapsto\theta_i+\alpha
\]

leaves every (Delta_{ij}) and therefore (V_{\rm M}) unchanged.

## 8. Inertial and overdamped regimes are one dynamics

The TIR phase-action parent supplies the Euler--Lagrange--Rayleigh form

\[
I_iddot\theta_i
+
\eta_idot\theta_i
+
\frac{\partial V_{\rm M}}{\partial\theta_i}
=
0.
\]

This is the inertial network phase dynamics.

In the overdamped limit,

\[
I_iddot\theta_i\to0,
\]

so

\[
\boxed{
\eta_idot\theta_i
=
-
\frac{\partial V_{\rm M}}{\partial\theta_i}.
}
\]

Therefore

\[
\boxed{
\eta_idot\theta_i
=
-\pi\kappa
\sum_j
\sin\Delta_{ij}
}
\]

with the edge orientation fixing the displayed sign convention.

This is gauge-twisted Kuramoto flow.

Hence

\[
\boxed{
\text{pendulum}
=
\text{two-sector inertial reduction},
}
\]

while

\[
\boxed{
\text{Kuramoto}
=
\text{overdamped network reduction}.
}
\]

They are not competing laws.

Both descend from the same relational phase potential.

## 9. Lyapunov closure

For the overdamped system,

\[
\dot\theta_i
=
-\frac1{\eta_i}
\frac{\partial V_{\rm M}}{\partial\theta_i}.
\]

Therefore

\[
\dot V_{\rm M}
=
\sum_i
\frac{\partial V_{\rm M}}{\partial\theta_i}
\dot\theta_i
=
-\sum_i
\frac1{\eta_i}
\left(
\frac{\partial V_{\rm M}}{\partial\theta_i}
\right)^2.
\]

Hence

\[
\boxed{
\dot V_{\rm M}\le0.
}
\]

This reproduces the exact conditional TIR White-Thread Lyapunov result on the
canonical RDSS information normalization.

## 10. What is closed

PASS:

- exact pretime half-successor (H^2=S);
- discrete half-frame occurrence order;
- continuous (U(1)) phase state on each occurrence;
- 24 directed incidences and 12 undirected exchange pairs;
- directed information share (ln2/24);
- paired information budget (ln2/12);
- canonical pair potential
  \[
  V_{\leftrightarrow}=\pi\kappa(1-\cos\Delta);
  \]
- exact opposite pair gradients and zero net center force;
- relative pendulum equation;
- unique local symmetric second-frame difference;
- frame-native pendulum recurrence;
- canonical Moire information potential;
- sine coupling as the gradient of that potential;
- Kuramoto as the overdamped limit;
- Lyapunov monotonicity in the static-holonomy overdamped sector;
- historical `GATE_MOIRE_DYNAMICAL_LAW` closed at the structural relational
  phase level.

## 11. What remains separate

This closure does not claim:

- that the normalized successor unit (h) is already calibrated in physical
  seconds;
- that the pretime half-index is semantically identical to every other
  occurrence of numerical (1/2) in TIR;
- that the abstract phase inertia (I_phi) is a measured mechanical moment
  of inertia;
- that the Moire phase graph is already a specific material, gravitational,
  electromagnetic or particle-physics substrate;
- that a continuum field equation follows without a separate continuum
  realization.

Those are physical/sector bindings downstream of the structural dynamical law.

## 12. Executable surfaces

- `src/rdss/alternating_phase_dynamics.py`
- `tests/test_alternating_phase_dynamics.py`
- `src/rdss/axioms.py`
- `src/rdss/foundational_provenance.py`

Canonical theorem nodes:

- `BRIDGE_TIR_PRETIME_STELLA_HALF_SUCCESSOR`
- `BRIDGE_TIR_WHITE_THREAD_PHASE_ACTION`
- `THM_FRAME_FUZZY_HALF_SUCCESSOR`
- `THM_CANONICAL_PAIR_INFORMATION_POTENTIAL`
- `THM_BIPOLAR_PAIR_FORCE_ANTISYMMETRY`
- `THM_BIPOLAR_RELATIVE_PENDULUM`
- `THM_FRAME_SECOND_DIFFERENCE_UNIQUE`
- `THM_FRAME_PENDULUM_SUCCESSOR`
- `THM_MOIRE_INFORMATION_POTENTIAL`
- `THM_MOIRE_KURAMOTO_CLOSURE`
- `THM_PENDULUM_KURAMOTO_COMMON_PARENT`
- historical id `GATE_MOIRE_DYNAMICAL_LAW` promoted to theorem-level closed
  status.
