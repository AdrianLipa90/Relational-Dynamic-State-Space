from __future__ import annotations

from math import exp, isfinite


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
