from __future__ import annotations

from math import exp, isfinite, log


def _finite(value: float, name: str) -> float:
    x = float(value)
    if not isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def distinction_flow(amplitude: float, control: float) -> float:
    """Reference persistence flow d_dot=d(mu-d) on the domain d>=0."""

    d = _finite(amplitude, "amplitude")
    mu = _finite(control, "control")
    if d < 0.0:
        raise ValueError("distinction amplitude must be non-negative")
    return d * (mu - d)


def distinction_potential(amplitude: float, control: float) -> float:
    """Lyapunov potential W=-mu*d^2/2+d^3/3 for the reference flow."""

    d = _finite(amplitude, "amplitude")
    mu = _finite(control, "control")
    if d < 0.0:
        raise ValueError("distinction amplitude must be non-negative")
    return -0.5 * mu * d * d + (d * d * d) / 3.0


def distinction_potential_gradient(amplitude: float, control: float) -> float:
    """dW/dd; the reference flow is exactly minus this gradient."""

    d = _finite(amplitude, "amplitude")
    mu = _finite(control, "control")
    if d < 0.0:
        raise ValueError("distinction amplitude must be non-negative")
    return -mu * d + d * d


def distinction_potential_dissipation(amplitude: float, control: float) -> float:
    """dW/dt along the flow; always non-positive."""

    velocity = distinction_flow(amplitude, control)
    return -(velocity * velocity)


def persistence_equilibria(control: float) -> tuple[float, ...]:
    """Non-negative equilibria of d_dot=d(mu-d)."""

    mu = _finite(control, "control")
    if mu > 0.0:
        return (0.0, mu)
    return (0.0,)


def equilibrium_linear_rate(equilibrium: float, control: float) -> float:
    """Derivative of d(mu-d) with respect to d at one equilibrium."""

    d = _finite(equilibrium, "equilibrium")
    mu = _finite(control, "control")
    if d < 0.0:
        raise ValueError("equilibrium must be non-negative")
    return mu - 2.0 * d


def persistence_regime(control: float) -> str:
    """Classify the reference flow as dispersion, critical, or structure."""

    mu = _finite(control, "control")
    if mu < 0.0:
        return "dispersion"
    if mu > 0.0:
        return "structure"
    return "critical"


def distinction_solution(amplitude0: float, control: float, time: float) -> float:
    """Exact forward solution of d_dot=d(mu-d) for d0>=0 and t>=0."""

    d0 = _finite(amplitude0, "amplitude0")
    mu = _finite(control, "control")
    t = _finite(time, "time")
    if d0 < 0.0:
        raise ValueError("initial distinction amplitude must be non-negative")
    if t < 0.0:
        raise ValueError("time must be non-negative")
    if d0 == 0.0:
        return 0.0
    if mu == 0.0:
        return d0 / (1.0 + d0 * t)

    e = exp(-mu * t)
    denominator = 1.0 + (mu / d0 - 1.0) * e
    return mu / denominator


def asymptotic_distinction(control: float) -> float:
    """Forward attractor amplitude for every strictly positive initial d."""

    mu = _finite(control, "control")
    return max(mu, 0.0)


def _positive_odd_integer(value: int, name: str = "state") -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value <= 0 or value % 2 == 0:
        raise ValueError(f"{name} must be a positive odd integer")
    return value


def two_adic_valuation(value: int) -> int:
    """Return nu_2(value) for a positive integer."""

    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an integer")
    if value <= 0:
        raise ValueError("value must be positive")
    exponent = 0
    x = value
    while x % 2 == 0:
        exponent += 1
        x //= 2
    return exponent


def collatz_dissociate(state: int) -> int:
    """Dissociation operator D(n)=3n on a positive odd state."""

    n = _positive_odd_integer(state)
    return 3 * n


def collatz_complete(dissociated: int) -> int:
    """Completion/repair operator R(m)=m+1 after dissociation."""

    if isinstance(dissociated, bool) or not isinstance(dissociated, int):
        raise TypeError("dissociated must be an integer")
    if dissociated <= 0 or dissociated % 2 == 0:
        raise ValueError("dissociated state must be positive odd")
    return dissociated + 1


def collatz_associate(completed: int) -> tuple[int, int]:
    """Associate by removing every available factor two."""

    if isinstance(completed, bool) or not isinstance(completed, int):
        raise TypeError("completed must be an integer")
    if completed <= 0 or completed % 2 != 0:
        raise ValueError("completed state must be positive even")
    steps = two_adic_valuation(completed)
    return (completed >> steps, steps)


def collatz_association_cycle(state: int) -> tuple[int, int]:
    """Accelerated odd Collatz cycle D -> R -> A*.

    Returns the next odd state and the number of association (/2) steps.
    No global convergence claim is made.
    """

    n = _positive_odd_integer(state)
    completed = collatz_complete(collatz_dissociate(n))
    return collatz_associate(completed)


def collatz_log_gain(state: int) -> float:
    """Local log expansion ln(T_C(n)/n) of one accelerated odd cycle."""

    n = _positive_odd_integer(state)
    next_state, _ = collatz_association_cycle(n)
    return log(next_state / n)


def collatz_association_balance(state: int) -> float:
    """Association-minus-dissociation balance for one accelerated odd cycle.

    Positive means association dominates the net scale change; negative means
    dissociation dominates; zero is locally critical.
    """

    n = _positive_odd_integer(state)
    completed = collatz_complete(collatz_dissociate(n))
    association_steps = two_adic_valuation(completed)
    return association_steps * log(2.0) - log(completed / n)


def collatz_persistence_regime(state: int, *, atol: float = 1e-15) -> str:
    """Classify local Collatz balance as structure/dispersion/critical."""

    balance = collatz_association_balance(state)
    if abs(balance) <= atol:
        return "critical"
    if balance > 0.0:
        return "structure"
    return "dispersion"


def distinction_flow_from_collatz(amplitude: float, state: int) -> float:
    """Reference persistence flow with control derived from Collatz balance."""

    return distinction_flow(amplitude, collatz_association_balance(state))
