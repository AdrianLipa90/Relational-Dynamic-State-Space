from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FiniteRelationModel:
    """Finite witness model for RA0/RR1 dependency checks.

    relations are directed primitive relations (source, target).
    refinements map a relational endpoint to two distinct descendant points.
    """

    points: frozenset[str]
    admitted: frozenset[str]
    relations: frozenset[tuple[str, str]]
    refinements: tuple[tuple[str, str, str], ...] = ()

    def __post_init__(self) -> None:
        if not self.admitted <= self.points:
            raise ValueError("admitted points must belong to the carrier")
        for source, target in self.relations:
            if source not in self.points or target not in self.points:
                raise ValueError("relation endpoints must belong to the carrier")
        seen: set[str] = set()
        for parent, left, right in self.refinements:
            if parent in seen:
                raise ValueError("each parent has at most one reference refinement")
            seen.add(parent)
            if parent not in self.points or left not in self.points or right not in self.points:
                raise ValueError("refinement points must belong to the carrier")
            if left == right:
                raise ValueError("a distinction requires two distinct descendants")

    def satisfies_ra0(self) -> bool:
        """RA0 witness semantics: every admitted point has an outgoing relation."""
        sources = {source for source, _ in self.relations}
        return self.admitted <= sources

    def satisfies_rr1(self) -> bool:
        """RR1 witness semantics: refinement closes recursively on reachable descendants.

        Starting from every primitive relation endpoint, each reachable
        refinement occurrence must itself have a non-degenerate refinement.
        Finite cyclic presentations are allowed; recursion is about closure of
        occurrences, not ontic novelty of carrier labels.
        """
        refinement_map = {
            parent: (left, right)
            for parent, left, right in self.refinements
        }
        frontier = list({x for edge in self.relations for x in edge})
        seen: set[str] = set()

        while frontier:
            current = frontier.pop()
            if current in seen:
                continue
            if current not in refinement_map:
                return False
            left, right = refinement_map[current]
            seen.add(current)
            frontier.extend((left, right))
        return True


def witness_ra0_not_rr1() -> FiniteRelationModel:
    """RA0 holds but recursive closure is deliberately absent."""
    return FiniteRelationModel(
        points=frozenset({"a", "b"}),
        admitted=frozenset({"a", "b"}),
        relations=frozenset({("a", "b"), ("b", "a")}),
        refinements=(),
    )


def witness_rr1_not_ra0() -> FiniteRelationModel:
    """Recursive RR1 holds while an admitted isolated point breaks RA0."""
    return FiniteRelationModel(
        points=frozenset({"a", "b", "q"}),
        admitted=frozenset({"a", "b", "q"}),
        relations=frozenset({("a", "b"), ("b", "a")}),
        refinements=(
            ("a", "a", "b"),
            ("b", "a", "b"),
        ),
    )


def witness_ra0_rr1_without_cp1() -> FiniteRelationModel:
    """A recursive cyclic relational/refinement model with no CP1 layer."""
    return FiniteRelationModel(
        points=frozenset({"a", "b"}),
        admitted=frozenset({"a", "b"}),
        relations=frozenset({("a", "b"), ("b", "a")}),
        refinements=(
            ("a", "a", "b"),
            ("b", "a", "b"),
        ),
    )
