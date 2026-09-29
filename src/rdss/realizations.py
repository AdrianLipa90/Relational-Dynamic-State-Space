from __future__ import annotations

from dataclasses import dataclass
from math import pi

from .algebra import CP1State, MinimalDistinction, RelationalPoint


@dataclass(frozen=True)
class CP1RefinementRealization:
    """Tree of local CP1/Fubini-Study fibres over relational carriers.

    Each carrier p_omega owns a local CP1 distinction. The selected left/right
    projective states index the child carriers p_(omega,-) and p_(omega,+).
    Child carriers may in turn own their own local CP1 fibres.

    The local CP1 state at a parent is not identified with the projective
    coordinate system of a child fibre; the link is incidence/refinement.
    """

    distinctions: tuple[MinimalDistinction, ...]

    def __post_init__(self) -> None:
        carriers = [d.carrier for d in self.distinctions]
        if len(carriers) != len(set(carriers)):
            raise ValueError("each relational carrier may have at most one CP1 fibre")

    @property
    def by_carrier(self) -> dict[RelationalPoint, MinimalDistinction]:
        return {d.carrier: d for d in self.distinctions}

    def distinction_at(self, carrier: RelationalPoint) -> MinimalDistinction:
        try:
            return self.by_carrier[carrier]
        except KeyError as exc:
            raise KeyError(f"no CP1 distinction at carrier {carrier.address}") from exc

    def branch_state(self, carrier: RelationalPoint, branch: int) -> CP1State:
        if branch not in (-1, 1):
            raise ValueError("branch must be -1 or +1")
        d = self.distinction_at(carrier)
        return d.left if branch == -1 else d.right

    def child_carrier(self, carrier: RelationalPoint, branch: int) -> RelationalPoint:
        if branch not in (-1, 1):
            raise ValueError("branch must be -1 or +1")
        return RelationalPoint(carrier.address + (branch,))

    def complete_through_depth(self, root: RelationalPoint, depth: int) -> bool:
        """Require one local CP1 distinction at every node through depth."""
        if depth < 0:
            raise ValueError("depth must be non-negative")
        fibres = self.by_carrier
        level = (root,)
        for current_depth in range(depth + 1):
            if any(carrier not in fibres for carrier in level):
                return False
            if current_depth == depth:
                break
            level = tuple(
                RelationalPoint(carrier.address + (branch,))
                for carrier in level
                for branch in (-1, 1)
            )
        return True

    def fs_profile(
        self,
        root: RelationalPoint,
        depth: int,
    ) -> dict[tuple[int, ...], float]:
        if not self.complete_through_depth(root, depth):
            raise ValueError("CP1 refinement realization is incomplete")
        fibres = self.by_carrier
        out: dict[tuple[int, ...], float] = {}
        level = (root,)
        for current_depth in range(depth + 1):
            for carrier in level:
                out[carrier.address] = fibres[carrier].separation
            if current_depth == depth:
                break
            level = tuple(
                RelationalPoint(carrier.address + (branch,))
                for carrier in level
                for branch in (-1, 1)
            )
        return out


def reference_maximal_cp1_tree(
    depth: int,
    *,
    root: RelationalPoint = RelationalPoint(),
) -> CP1RefinementRealization:
    """Build a finite reference tree with maximal FS distinction in each fibre."""
    if depth < 0:
        raise ValueError("depth must be non-negative")

    north = CP1State(1.0, 0.0)
    south = north.orthogonal_partner()

    distinctions: list[MinimalDistinction] = []
    level = (root,)
    for current_depth in range(depth + 1):
        for carrier in level:
            distinctions.append(
                MinimalDistinction(
                    carrier=carrier,
                    left=north,
                    right=south,
                    label="maximal-reference-distinction",
                )
            )
        if current_depth == depth:
            break
        level = tuple(
            RelationalPoint(carrier.address + (branch,))
            for carrier in level
            for branch in (-1, 1)
        )

    realization = CP1RefinementRealization(tuple(distinctions))
    if any(abs(value - pi / 2.0) > 1e-12 for value in realization.fs_profile(root, depth).values()):
        raise AssertionError("reference CP1 tree must be maximally distinguished")
    return realization
