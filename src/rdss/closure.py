from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .algebra import RelationalPoint, TypedRelation


@dataclass(frozen=True)
class BinaryDistinction:
    """One hosted binary distinction with distinct left/right occurrence slots.

    Non-degeneracy is occurrence-level: the - and + branch positions are
    distinct even when both positions carry the same underlying carrier label.
    """

    host: str
    left: str
    right: str

    def __post_init__(self) -> None:
        if not self.host or not self.left or not self.right:
            raise ValueError("distinction labels must be non-empty")


@dataclass(frozen=True, order=True)
class BranchRelationOccurrence:
    """One primitive relation occurrence bound to a binary branch slot."""

    branch: int
    relation_label: str
    source: str
    target: str

    def __post_init__(self) -> None:
        if self.branch not in (-1, 1):
            raise ValueError("branch must be -1 or +1")
        if not self.relation_label.strip():
            raise ValueError("relation label must be non-empty")
        if not self.source or not self.target:
            raise ValueError("relation occurrence endpoints must be non-empty")

    def as_typed_relation(
        self,
        carriers: Mapping[str, RelationalPoint],
    ) -> TypedRelation:
        """Forget occurrence slot while materializing the core relation value."""
        try:
            source = carriers[self.source]
            target = carriers[self.target]
        except KeyError as exc:
            raise KeyError(
                f"missing carrier mapping for relation occurrence endpoint {exc.args[0]!r}"
            ) from exc
        return TypedRelation(source, target, self.relation_label)


@dataclass(frozen=True)
class RelationalBinaryDistinction:
    """Binary occurrence distinction with explicit branch-relation labels."""

    host: str
    left: str
    right: str
    left_relation: str
    right_relation: str

    def __post_init__(self) -> None:
        if not self.host or not self.left or not self.right:
            raise ValueError("distinction labels must be non-empty")
        if not self.left_relation.strip() or not self.right_relation.strip():
            raise ValueError("branch relation labels must be non-empty")

    @property
    def branch_relation_occurrences(
        self,
    ) -> tuple[BranchRelationOccurrence, BranchRelationOccurrence]:
        """Return the two typed branch-relation occurrence records."""
        return (
            BranchRelationOccurrence(
                -1,
                self.left_relation,
                self.host,
                self.left,
            ),
            BranchRelationOccurrence(
                1,
                self.right_relation,
                self.host,
                self.right,
            ),
        )

    @property
    def binary(self) -> BinaryDistinction:
        return BinaryDistinction(self.host, self.left, self.right)


@dataclass(frozen=True)
class GenerativeRelationModel:
    """Finite presentation of the strengthened one-axiom candidate RA0*.

    RA0*:
        Every admitted carrier hosts at least one admitted non-degenerate
        binary distinction, and the selected endpoint occurrences are
        themselves admitted carriers.

    The underlying presentation may be finite and cyclic. Recursive
    refinement is defined on path-labelled occurrences, so cycles in the
    presentation do not collapse distinct refinement occurrences.
    """

    admitted: frozenset[str]
    distinctions: tuple[BinaryDistinction, ...]

    def __post_init__(self) -> None:
        by_host: dict[str, list[BinaryDistinction]] = {}
        for d in self.distinctions:
            by_host.setdefault(d.host, []).append(d)
        if any(host not in self.admitted for host in by_host):
            raise ValueError("every distinction host must be admitted")
        endpoints = {x for d in self.distinctions for x in (d.left, d.right)}
        if not endpoints <= self.admitted:
            raise ValueError("distinction endpoints must themselves be admitted")

    @property
    def distinctions_by_host(self) -> Mapping[str, tuple[BinaryDistinction, ...]]:
        out: dict[str, list[BinaryDistinction]] = {}
        for d in self.distinctions:
            out.setdefault(d.host, []).append(d)
        return {
            host: tuple(sorted(items, key=lambda x: (x.left, x.right)))
            for host, items in out.items()
        }

    @property
    def selected_distinction_by_host(self) -> Mapping[str, BinaryDistinction]:
        """Canonical reference selector used only to build one unfolding.

        RA0* requires existence of at least one distinction per admitted host,
        not uniqueness. When several are available, the reference kernel
        selects the lexicographically first endpoint pair so unfolding is
        deterministic without strengthening the axiom.
        """
        return {
            host: items[0]
            for host, items in self.distinctions_by_host.items()
            if items
        }

    def satisfies_ra0_star(self) -> bool:
        """Every admitted carrier has at least one non-degenerate admitted distinction."""
        by_host = self.distinctions_by_host
        return self.admitted <= set(by_host)

    def is_admissible_rtofa_model(self) -> bool:
        """Apply META0 model formation semantics.

        The raw finite presentation class allows the empty presentation so
        vacuous truth can be audited explicitly. The empty presentation is a
        mathematical object, but it is not an admissible RTOFA model because
        the admitted carrier domain is empty.
        """
        return bool(self.admitted)

    def unfold(self, root: str, depth: int) -> dict[tuple[int, ...], str]:
        """Unfold the recursive relation into path-labelled binary occurrences.

        Addresses use -1 for left and +1 for right. The same carrier label may
        reappear at different addresses; those are distinct relational
        occurrences in the unfolding.
        """
        if root not in self.admitted:
            raise ValueError("root must be admitted")
        if depth < 0:
            raise ValueError("depth must be non-negative")
        if not self.satisfies_ra0_star():
            raise ValueError("model does not satisfy RA0*")

        by_host = self.selected_distinction_by_host
        level: dict[tuple[int, ...], str] = {(): root}
        all_nodes = dict(level)

        for _ in range(depth):
            next_level: dict[tuple[int, ...], str] = {}
            for address, carrier in level.items():
                distinction = by_host[carrier]
                next_level[address + (-1,)] = distinction.left
                next_level[address + (1,)] = distinction.right
            all_nodes.update(next_level)
            level = next_level
        return all_nodes

    def rr1_holds_through_depth(self, root: str, depth: int) -> bool:
        """Check recursive binary refinement on all occurrences up to depth."""
        if depth < 0:
            raise ValueError("depth must be non-negative")
        if not self.satisfies_ra0_star():
            return False
        tree = self.unfold(root, depth + 1)
        for address in tuple(tree):
            if len(address) > depth:
                continue
            if address + (-1,) not in tree or address + (1,) not in tree:
                return False
        return True


@dataclass(frozen=True)
class RelationalGenerativeModel:
    """Finite presentation of the relationally bound candidate RA0_REL_STAR.

    Every hosted distinction carries two explicit branch-relation occurrences.
    This is stronger than GenerativeRelationModel/RA0*: it binds recursive
    distinction structure to primitive relational incidence.
    """

    admitted: frozenset[str]
    distinctions: tuple[RelationalBinaryDistinction, ...]

    def __post_init__(self) -> None:
        hosts = {d.host for d in self.distinctions}
        if not hosts <= self.admitted:
            raise ValueError("every relational distinction host must be admitted")
        endpoints = {x for d in self.distinctions for x in (d.left, d.right)}
        if not endpoints <= self.admitted:
            raise ValueError("relational distinction endpoints must be admitted")

    @property
    def distinctions_by_host(
        self,
    ) -> Mapping[str, tuple[RelationalBinaryDistinction, ...]]:
        out: dict[str, list[RelationalBinaryDistinction]] = {}
        for d in self.distinctions:
            out.setdefault(d.host, []).append(d)
        return {
            host: tuple(
                sorted(
                    items,
                    key=lambda x: (
                        x.left,
                        x.right,
                        x.left_relation,
                        x.right_relation,
                    ),
                )
            )
            for host, items in out.items()
        }

    @property
    def selected_distinction_by_host(
        self,
    ) -> Mapping[str, RelationalBinaryDistinction]:
        return {
            host: items[0]
            for host, items in self.distinctions_by_host.items()
            if items
        }

    def satisfies_ra0_rel_star(self) -> bool:
        """Every admitted carrier hosts at least one relational distinction."""
        return self.admitted <= set(self.distinctions_by_host)

    def satisfies_ra0(self) -> bool:
        """RA0 follows because every admitted host has branch-relation incidence."""
        return self.satisfies_ra0_rel_star()

    def is_admissible_rtofa_model(self) -> bool:
        return bool(self.admitted)

    def as_ra0_star_model(self) -> GenerativeRelationModel:
        """Forget explicit branch-relation binding and retain binary distinction.

        This is the executable projection witnessing
        RA0_REL_STAR => RA0_STAR.
        """
        return GenerativeRelationModel(
            admitted=self.admitted,
            distinctions=tuple(d.binary for d in self.distinctions),
        )

    def unfold(self, root: str, depth: int) -> dict[tuple[int, ...], str]:
        if root not in self.admitted:
            raise ValueError("root must be admitted")
        if depth < 0:
            raise ValueError("depth must be non-negative")
        if not self.satisfies_ra0_rel_star():
            raise ValueError("model does not satisfy RA0_REL_STAR")

        by_host = self.selected_distinction_by_host
        level: dict[tuple[int, ...], str] = {(): root}
        all_nodes = dict(level)
        for _ in range(depth):
            next_level: dict[tuple[int, ...], str] = {}
            for address, carrier in level.items():
                distinction = by_host[carrier]
                next_level[address + (-1,)] = distinction.left
                next_level[address + (1,)] = distinction.right
            all_nodes.update(next_level)
            level = next_level
        return all_nodes

    def rr1_holds_through_depth(self, root: str, depth: int) -> bool:
        if depth < 0:
            raise ValueError("depth must be non-negative")
        if not self.satisfies_ra0_rel_star():
            return False
        tree = self.unfold(root, depth + 1)
        for address in tuple(tree):
            if len(address) > depth:
                continue
            if address + (-1,) not in tree or address + (1,) not in tree:
                return False
        return True

    def branch_relations_at(
        self,
        host: str,
    ) -> tuple[BranchRelationOccurrence, BranchRelationOccurrence]:
        try:
            distinction = self.selected_distinction_by_host[host]
        except KeyError as exc:
            raise KeyError(f"no relational distinction at host {host!r}") from exc
        return distinction.branch_relation_occurrences


def singleton_ra0_rel_star_model() -> RelationalGenerativeModel:
    """One carrier, two branch-relation occurrence slots, recursive closure."""
    return RelationalGenerativeModel(
        admitted=frozenset({"a"}),
        distinctions=(
            RelationalBinaryDistinction(
                host="a",
                left="a",
                right="a",
                left_relation="r-",
                right_relation="r+",
            ),
        ),
    )


def singleton_ra0_star_model() -> GenerativeRelationModel:
    """Single carrier with two distinct branch-occurrence slots.

    Both left and right slots carry the same carrier label a. The
    distinction is nevertheless binary because the path addresses - and +
    are distinct occurrences.
    """
    return GenerativeRelationModel(
        admitted=frozenset({"a"}),
        distinctions=(
            BinaryDistinction("a", "a", "a"),
        ),
    )


def two_cycle_ra0_star_model() -> GenerativeRelationModel:
    """Small cyclic presentation whose unfolding is still a binary tree.

    Underlying labels repeat, but path-labelled occurrences remain distinct.
    This separates recursive relational structure from ontic novelty.
    """
    return GenerativeRelationModel(
        admitted=frozenset({"a", "b"}),
        distinctions=(
            BinaryDistinction("a", "a", "b"),
            BinaryDistinction("b", "a", "b"),
        ),
    )


def requires_novelty(
    model: GenerativeRelationModel,
    root: str,
    depth: int,
) -> bool:
    """Check the stronger, optional property that every occurrence has a new carrier label.

    This is deliberately *not* part of RA0*. It is provided to show that
    ontic novelty would require an additional assumption beyond relational
    recursion.
    """
    tree = model.unfold(root, depth)
    labels = list(tree.values())
    return len(labels) == len(set(labels))



def binary_occurrence_count_through_depth(depth: int) -> int:
    """Number of binary path-labelled occurrences from level 0 through depth."""
    if depth < 0:
        raise ValueError("depth must be non-negative")
    return (1 << (depth + 1)) - 1


def finite_word_rank(address: tuple[int, ...]) -> int:
    """Bijection from finite {-1,+1} words to non-negative integers.

    Words are ordered first by length and then lexicographically after
    encoding -1 as bit 0 and +1 as bit 1.
    """
    rank = (1 << len(address)) - 1
    index = 0
    for branch in address:
        if branch not in (-1, 1):
            raise ValueError("address branches must be -1 or +1")
        index = (index << 1) | (1 if branch == 1 else 0)
    return rank + index


def finite_word_unrank(rank: int) -> tuple[int, ...]:
    """Inverse of finite_word_rank on the non-negative integers."""
    if rank < 0:
        raise ValueError("rank must be non-negative")

    length = (rank + 1).bit_length() - 1
    start = (1 << length) - 1
    index = rank - start

    address: list[int] = []
    for shift in range(length - 1, -1, -1):
        bit = (index >> shift) & 1
        address.append(1 if bit else -1)
    return tuple(address)
