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

[
mathcal X=mathbb N_0	imes{+,-}
]

with

[
H(n,+)=(n,-),
qquad
H(n,-)=(n+1,+).
]

Therefore

[
oxed{H^2=S}.
]

The normalized occurrence grade is

[

u(n,+)=n,
qquad

u(n,-)=n+rac12.
]

Hence one application of (H) advances the structural order by (1/2),
while two complementary applications give one full successor.

The internal phase state is not discretized by this statement:

[
	hetainmathbb R/2pimathbb Z.
]

Thus the exact structural split is

[
oxed{
	ext{occurrence order: discrete half-frames}
qquad
	ext{phase state: continuous }U(1).
}
]

This is the precise meaning of frame-like but fuzzy phase time at the present
layer.

The pretime half-index and the (U(1)) half-turn are separately typed. Their
common numerical value (1/2) is not used as an unstated semantic
identification.

## 2. Information budget per directed channel and per paired exchange

The closed bipolar channel orbit contains

[
N_{	o}=24
]

directed incidences and

[
N_{leftrightarrow}=12
]

undirected exchange pairs.

The total binary source information is

[
I_*=ln2.
]

Therefore one directed incidence carries the invariant information share

[
oxed{
I_{	o}=rac{ln2}{24}.
}
]

Because

[
kappa=rac{ln2}{24pi},
]

this is equivalently

[
oxed{
I_{	o}=pikappa.
}
]

One undirected pair contains the two opposite directed incidences, hence

[
oxed{
I_{leftrightarrow}
=
2I_{	o}
=
rac{ln2}{12}
=
2pikappa.
}
]

## 3. Canonical chordal mismatch fixes the pair potential

For a projected (U(1)) mismatch

[
Delta=	heta_i-	heta_j-Gamma_{ij},
]

the squared chordal distance on the unit circle is

[
|e^{iDelta}-1|^2
=
2-2cosDelta.
]

Normalize it to the interval ([0,1]):

[
oxed{
c(Delta)
=
rac{|e^{iDelta}-1|^2}{4}
=
rac{1-cosDelta}{2}.
}
]

Then

[
c(0)=0,
qquad
c(pi)=1.
]

Thus the half-turn exactly saturates the paired exchange mismatch scale.

Multiplying by the already fixed information budget of one undirected pair
gives

[
V_{leftrightarrow}(Delta)
=
I_{leftrightarrow}c(Delta).
]

Therefore

[
oxed{
V_{leftrightarrow}(Delta)
=
rac{ln2}{24}(1-cosDelta)
=
pikappa(1-cosDelta).
}
]

No free coupling amplitude remains in this canonical information-normalized
pair potential.

At the half-turn,

[
oxed{
V_{leftrightarrow}(pi)
=
rac{ln2}{12}.
}
]

Consequently twelve maximally mismatched exchange pairs give

[
12V_{leftrightarrow}(pi)
=
oxed{ln2}.
]

This is an independent normalization closure check.

## 4. Opposite gradients and the relational zero

Write

[
Delta=	heta_+-	heta_- - Gamma.
]

Let

[
A_*=rac{ln2}{24}=pikappa.
]

Then

[
V=A_*(1-cosDelta).
]

The gradients are

[
rac{partial V}{partial	heta_+}
=
A_*sinDelta,
]

[
rac{partial V}{partial	heta_-}
=
-A_*sinDelta.
]

The relational forces are therefore

[
oxed{
F_+
=
-A_*sinDelta,
qquad
F_-
=
+A_*sinDelta.
}
]

Hence

[
oxed{
F_++F_-=0.
}
]

The interaction can change the relative coordinate but cannot accelerate the
center mode.

This is the exact algebraic meaning of inertia with respect to the relational
zero at this layer.

## 5. Pendulum closure

Use the already promoted TIR phase inertia (I_phi>0), and optionally an
equal Rayleigh coefficient (etage0) on each of the two sectors.

Define center and relative coordinates

[
c=rac{	heta_++	heta_-}{2},
qquad
Delta=	heta_+-	heta_-.
]

Adding the two sector equations gives

[
oxed{
I_phiddot c+etadot c=0.
}
]

Subtracting gives

[
oxed{
I_phiddotDelta
+
etadotDelta
+
2A_*sinDelta
=
0.
}
]

Since (A_*=pikappa),

[
oxed{
I_phiddotDelta
+
etadotDelta
+
2pikappasinDelta
=
0.
}
]

Equivalently, with reduced inertia and damping

[
mu=rac{I_phi}{2},
qquad
gamma=rac{eta}{2},
]

the same equation is

[
oxed{
muddotDelta
+
gammadotDelta
+
pikappasinDelta
=
0.
}
]

This is the standard pendulum equation on the relative phase coordinate.

The conservative core (eta=0) has

[
ddot c=0,
]

so the center is inertial while the relative phase oscillates in the forced
periodic potential.

## 6. Frame-native inertia

The full successor is

[
S=H^2.
]

Consider a local linear three-frame inertial operator

[
D_2x_n
=
a x_{n-1}+b x_n+c x_{n+1}.
]

Requiring it to annihilate constants gives

[
a+b+c=0.
]

Requiring it also to annihilate uniform drift (x_n=alpha n+eta) gives

[
c=a.
]

Therefore

[
b=-2a.
]

Up to one overall scale, the unique local operator is

[
oxed{
D_2x_n
=
x_{n+1}-2x_n+x_{n-1}.
}
]

Thus on a normalized full-successor spacing (h),

[
oxed{
I_phi
rac{
Delta_{n+1}-2Delta_n+Delta_{n-1}
}{h^2}
+
2pikappasinDelta_n
=
0.
}
]

The occurrence index is discrete; (Delta_n) is still a continuous phase
representative. Physical seconds are not assumed. A dimensional clock
calibration of (h) remains downstream.

## 7. Moire potential

For an undirected Moire graph with gauge-reduced edge mismatch

[
Delta_{ij}
=
	heta_i-	heta_j-Gamma_{ij},
]

define the canonical information potential

[
oxed{
V_{m M}
=
pikappa
sum_{{i,j}in E}
left(
1-cosDelta_{ij}
ight).
}
]

For each edge,

[
partial_{	heta_i}V_{ij}
=
pikappasinDelta_{ij},
qquad
partial_{	heta_j}V_{ij}
=
-pikappasinDelta_{ij}.
]

Thus the network force is automatically a sine-coupling force. No independent
Kuramoto sine ansatz is required.

A common phase shift

[
	heta_imapsto	heta_i+alpha
]

leaves every (Delta_{ij}) and therefore (V_{m M}) unchanged.

## 8. Inertial and overdamped regimes are one dynamics

The TIR phase-action parent supplies the Euler--Lagrange--Rayleigh form

[
I_iddot	heta_i
+
eta_idot	heta_i
+
rac{partial V_{m M}}{partial	heta_i}
=
0.
]

This is the inertial network phase dynamics.

In the overdamped limit,

[
I_iddot	heta_i	o0,
]

so

[
oxed{
eta_idot	heta_i
=
-
rac{partial V_{m M}}{partial	heta_i}.
}
]

Therefore

[
oxed{
eta_idot	heta_i
=
-pikappa
sum_j
sinDelta_{ij}
}
]

with the edge orientation fixing the displayed sign convention.

This is gauge-twisted Kuramoto flow.

Hence

[
oxed{
	ext{pendulum}
=
	ext{two-sector inertial reduction},
}
]

while

[
oxed{
	ext{Kuramoto}
=
	ext{overdamped network reduction}.
}
]

They are not competing laws.

Both descend from the same relational phase potential.

## 9. Lyapunov closure

For the overdamped system,

[
dot	heta_i
=
-rac1{eta_i}
rac{partial V_{m M}}{partial	heta_i}.
]

Therefore

[
dot V_{m M}
=
sum_i
rac{partial V_{m M}}{partial	heta_i}
dot	heta_i
=
-sum_i
rac1{eta_i}
left(
rac{partial V_{m M}}{partial	heta_i}
ight)^2.
]

Hence

[
oxed{
dot V_{m M}le0.
}
]

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
  [
  V_{leftrightarrow}=pikappa(1-cosDelta);
  ]
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
