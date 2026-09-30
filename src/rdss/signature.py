from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Callable

from .canonical import strict_normal_form


class SignatureAxis(str, Enum):
    CARRIER = "carrier"
    OCCURRENCE = "occurrence"
    RELATIONS = "relations"
    RANK = "rank"
    SCALE = "scale"
    ORBIT = "orbit"
    DIMENSION = "dimension"
    PHASE = "phase"
    STATE = "state"


_STATE_AXES = frozenset(
    {
        SignatureAxis.PHASE,
        SignatureAxis.STATE,
    }
)


class SignatureComparisonKind(str, Enum):
    EXACT_SIGNATURE = "exact_signature"
    SAME_SEMANTIC_STATE_DIFFERENT_REPRESENTATION = (
        "same_semantic_state_different_representation"
    )
    SAME_STRUCTURE_DIFFERENT_STATE = "same_structure_different_state"
    STRUCTURAL_DIFFERENCE = "structural_difference"
    INCOMPARABLE = "incomparable"


class NoveltyKind(str, Enum):
    EXACT_REPEAT = "exact_repeat"
    SIGNATURE_EQUIVALENT = "signature_equivalent"
    REPRESENTATION_ONLY = "representation_only"
    NEW_STATE = "new_state"
    NEW_STRUCTURE = "new_structure"
    NEW_FAMILY = "new_family"


class SignatureError(RuntimeError):
    pass


class UnsupportedSignatureError(SignatureError):
    pass


class AmbiguousSignatureError(SignatureError):
    pass


def _representation_tag(value: object) -> str:
    cls = type(value)
    return f"{cls.__module__}.{cls.__qualname__}"


def _canonical_key(value: object) -> object:
    return strict_normal_form(value).key


@dataclass(frozen=True)
class RDSSSignature:
    """Finite semantic signature separated from concrete representation.

    Axes are exact canonical keys. Carrier/occurrence/relation/rank/scale/orbit
    and dimension are structural axes. Phase and state are state axes.
    Representation and provenance are recorded separately.
    """

    family: str
    axes: tuple[tuple[SignatureAxis, object], ...]
    representation: str
    provenance: tuple[str, ...] = ()
    claim_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.family.strip():
            raise ValueError("signature family must be non-empty")
        if not self.representation.strip():
            raise ValueError("signature representation must be non-empty")
        if any(not item.strip() for item in self.provenance):
            raise ValueError("signature provenance entries must be non-empty")
        if any(not item.strip() for item in self.claim_ids):
            raise ValueError("signature claim ids must be non-empty")

        normalized: list[tuple[SignatureAxis, object]] = []
        seen: set[SignatureAxis] = set()
        for raw_axis, raw_value in self.axes:
            axis = SignatureAxis(raw_axis)
            if axis in seen:
                raise ValueError(f"duplicate signature axis: {axis.value}")
            seen.add(axis)
            _canonical_key(raw_value)
            normalized.append((axis, raw_value))
        normalized.sort(key=lambda item: item[0].value)
        object.__setattr__(self, "axes", tuple(normalized))

    @property
    def axis_map(self) -> dict[SignatureAxis, object]:
        return dict(self.axes)

    @property
    def structural_axes(self) -> tuple[tuple[SignatureAxis, object], ...]:
        return tuple(
            item for item in self.axes
            if item[0] not in _STATE_AXES
        )

    @property
    def state_axes(self) -> tuple[tuple[SignatureAxis, object], ...]:
        return tuple(
            item for item in self.axes
            if item[0] in _STATE_AXES
        )

    @property
    def structural_key(self) -> object:
        return (
            self.family,
            tuple(
                (axis, _canonical_key(value))
                for axis, value in self.structural_axes
            ),
        )

    @property
    def state_key(self) -> object:
        return tuple(
            (axis, _canonical_key(value))
            for axis, value in self.state_axes
        )

    @property
    def semantic_key(self) -> object:
        return (
            self.structural_key,
            self.state_key,
        )


ExtractorFunction = Callable[[object], RDSSSignature]
Predicate = Callable[[object], bool]


@dataclass(frozen=True)
class SignatureExtractor:
    name: str
    applies: Predicate
    extract: ExtractorFunction
    claim_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("signature extractor name must be non-empty")
        if any(not item.strip() for item in self.claim_ids):
            raise ValueError("signature extractor claim ids must be non-empty")


@dataclass(frozen=True)
class SignatureComparison:
    kind: SignatureComparisonKind
    left: RDSSSignature
    right: RDSSSignature
    strict_equal: bool

    @property
    def novelty(self) -> NoveltyKind:
        if self.kind is SignatureComparisonKind.INCOMPARABLE:
            return NoveltyKind.NEW_FAMILY
        if self.kind is SignatureComparisonKind.STRUCTURAL_DIFFERENCE:
            return NoveltyKind.NEW_STRUCTURE
        if self.kind is SignatureComparisonKind.SAME_STRUCTURE_DIFFERENT_STATE:
            return NoveltyKind.NEW_STATE
        if (
            self.kind
            is SignatureComparisonKind.SAME_SEMANTIC_STATE_DIFFERENT_REPRESENTATION
        ):
            return NoveltyKind.REPRESENTATION_ONLY
        if self.strict_equal:
            return NoveltyKind.EXACT_REPEAT
        return NoveltyKind.SIGNATURE_EQUIVALENT


class SignatureEngine:
    """Deterministic fail-closed semantic signature extractor/comparator."""

    def __init__(
        self,
        extractors: tuple[SignatureExtractor, ...],
    ) -> None:
        if not extractors:
            raise ValueError("at least one signature extractor is required")
        names = [extractor.name for extractor in extractors]
        if len(names) != len(set(names)):
            raise ValueError("signature extractor names must be unique")
        self._extractors = tuple(extractors)

    @property
    def extractors(self) -> tuple[SignatureExtractor, ...]:
        return self._extractors

    def signature(self, value: object) -> RDSSSignature:
        applicable = tuple(
            extractor
            for extractor in self._extractors
            if bool(extractor.applies(value))
        )
        if not applicable:
            raise UnsupportedSignatureError(
                f"no signature extractor for {_representation_tag(value)}"
            )
        if len(applicable) > 1:
            names = ", ".join(
                extractor.name for extractor in applicable
            )
            raise AmbiguousSignatureError(
                f"multiple signature extractors apply: {names}"
            )

        extractor = applicable[0]
        signature = extractor.extract(value)
        if not isinstance(signature, RDSSSignature):
            raise TypeError(
                "signature extractor must return RDSSSignature"
            )
        return replace(
            signature,
            provenance=signature.provenance + (extractor.name,),
            claim_ids=tuple(
                dict.fromkeys(
                    signature.claim_ids + extractor.claim_ids
                )
            ),
        )

    def compare(
        self,
        left: object,
        right: object,
    ) -> SignatureComparison:
        left_signature = self.signature(left)
        right_signature = self.signature(right)
        strict_equal = strict_normal_form(left).same_key(
            strict_normal_form(right)
        )

        if left_signature.family != right_signature.family:
            kind = SignatureComparisonKind.INCOMPARABLE
        elif left_signature.semantic_key == right_signature.semantic_key:
            if left_signature.representation == right_signature.representation:
                kind = SignatureComparisonKind.EXACT_SIGNATURE
            else:
                kind = (
                    SignatureComparisonKind
                    .SAME_SEMANTIC_STATE_DIFFERENT_REPRESENTATION
                )
        elif (
            left_signature.structural_key
            == right_signature.structural_key
        ):
            kind = SignatureComparisonKind.SAME_STRUCTURE_DIFFERENT_STATE
        else:
            kind = SignatureComparisonKind.STRUCTURAL_DIFFERENCE

        return SignatureComparison(
            kind=kind,
            left=left_signature,
            right=right_signature,
            strict_equal=strict_equal,
        )


def _signature(
    value: object,
    *,
    family: str,
    axes: tuple[tuple[SignatureAxis, object], ...],
    claim_ids: tuple[str, ...] = (),
) -> RDSSSignature:
    return RDSSSignature(
        family=family,
        axes=axes,
        representation=_representation_tag(value),
        claim_ids=claim_ids,
    )


def rdss_signature_extractors() -> tuple[SignatureExtractor, ...]:
    """Return explicit signature extractors for admitted executable RDSS types."""
    from .algebra import (
        OccurrenceAddress,
        RelationalPoint,
        SemanticScale,
        SemanticScaleGraph,
        TensorScalarElement,
        TypedRelation,
        TypedZero,
    )
    from .closure import (
        BinaryDistinction,
        BranchRelationOccurrence,
        GenerativeRelationModel,
        RelationalBinaryDistinction,
        RelationalGenerativeModel,
    )
    from .operations import (
        OccurrenceRelationPath,
        RelationOccurrence,
        RelationPath,
    )
    from .orbital_information import (
        CenterHalfTurnBridge,
        HilbertMoireFibreState,
    )
    from .phase import U1Phase
    from .realizations import (
        CP1State,
        MinimalDistinction,
        MoireRotation,
    )
    from .zero_axis import ZeroAxisPoint

    return (
        SignatureExtractor(
            "occurrence_address_signature",
            lambda value: isinstance(value, OccurrenceAddress),
            lambda value: _signature(
                value,
                family="occurrence_address",
                axes=(
                    (SignatureAxis.OCCURRENCE, tuple(value)),
                ),
                claim_ids=("DEF_OCCURRENCE_ADDRESS_SPACE",),
            ),
            ("DEF_RDSS_CANONICAL_SIGNATURE",),
        ),
        SignatureExtractor(
            "relational_point_signature",
            lambda value: isinstance(value, RelationalPoint),
            lambda value: _signature(
                value,
                family="relational_carrier",
                axes=(
                    (SignatureAxis.CARRIER, value),
                ),
                claim_ids=("DEF_POINT",),
            ),
            ("DEF_RDSS_CANONICAL_SIGNATURE",),
        ),
        SignatureExtractor(
            "semantic_scale_signature",
            lambda value: isinstance(value, SemanticScale),
            lambda value: _signature(
                value,
                family="semantic_scale",
                axes=(
                    (SignatureAxis.SCALE, value.label),
                ),
                claim_ids=("PRIM_SCALE",),
            ),
            ("DEF_RDSS_CANONICAL_SIGNATURE",),
        ),
        SignatureExtractor(
            "tensor_scalar_signature",
            lambda value: isinstance(value, TensorScalarElement),
            lambda value: _signature(
                value,
                family="tensor_scalar_element",
                axes=(
                    (SignatureAxis.CARRIER, value.carrier),
                    (SignatureAxis.RANK, value.rank),
                    (SignatureAxis.SCALE, value.scale),
                    (SignatureAxis.DIMENSION, len(value.components)),
                    (SignatureAxis.STATE, value.components),
                ),
                claim_ids=("DEF_TS", "PRIM_MODULE"),
            ),
            (
                "DEF_RDSS_CANONICAL_SIGNATURE",
                "DEF_SIGNATURE_AXIS_STRATIFICATION",
            ),
        ),
        SignatureExtractor(
            "typed_relation_signature",
            lambda value: isinstance(value, TypedRelation),
            lambda value: _signature(
                value,
                family="typed_relation",
                axes=(
                    (
                        SignatureAxis.RELATIONS,
                        (
                            value.source,
                            value.target,
                            value.label,
                        ),
                    ),
                ),
                claim_ids=("DEF_BINARY_REL",),
            ),
            ("DEF_RDSS_CANONICAL_SIGNATURE",),
        ),
        SignatureExtractor(
            "relation_occurrence_signature",
            lambda value: isinstance(value, RelationOccurrence),
            lambda value: _signature(
                value,
                family="relation_occurrence",
                axes=(
                    (SignatureAxis.RELATIONS, value.relation),
                    (
                        SignatureAxis.OCCURRENCE,
                        (
                            value.source_occurrence,
                            value.target_occurrence,
                        ),
                    ),
                ),
                claim_ids=("DEF_RELATION_OCCURRENCE",),
            ),
            (
                "DEF_RDSS_CANONICAL_SIGNATURE",
                "DEF_SIGNATURE_AXIS_STRATIFICATION",
            ),
        ),
        SignatureExtractor(
            "relation_path_signature",
            lambda value: isinstance(value, RelationPath),
            lambda value: _signature(
                value,
                family="relation_path",
                axes=(
                    (SignatureAxis.RELATIONS, value.relations),
                ),
                claim_ids=("DEF_BINARY_REL",),
            ),
            ("DEF_RDSS_CANONICAL_SIGNATURE",),
        ),
        SignatureExtractor(
            "occurrence_relation_path_signature",
            lambda value: isinstance(value, OccurrenceRelationPath),
            lambda value: _signature(
                value,
                family="occurrence_relation_path",
                axes=(
                    (
                        SignatureAxis.RELATIONS,
                        tuple(
                            item.relation
                            for item in value.occurrences
                        ),
                    ),
                    (
                        SignatureAxis.OCCURRENCE,
                        tuple(
                            (
                                item.source_occurrence,
                                item.target_occurrence,
                            )
                            for item in value.occurrences
                        ),
                    ),
                ),
                claim_ids=("DEF_OCCURRENCE_PATH",),
            ),
            (
                "DEF_RDSS_CANONICAL_SIGNATURE",
                "DEF_SIGNATURE_AXIS_STRATIFICATION",
            ),
        ),
        SignatureExtractor(
            "hilbert_moire_fibre_signature",
            lambda value: isinstance(value, HilbertMoireFibreState),
            lambda value: _signature(
                value,
                family="hilbert_moire_fibre",
                axes=(
                    (SignatureAxis.OCCURRENCE, value.occurrence),
                    (SignatureAxis.ORBIT, value.orbit_label),
                    (SignatureAxis.DIMENSION, len(value.vector)),
                    (SignatureAxis.PHASE, value.phase_turn),
                    (SignatureAxis.STATE, value.vector),
                ),
                claim_ids=("REF_HILBERT_MOIRE_FIBRE",),
            ),
            (
                "DEF_RDSS_CANONICAL_SIGNATURE",
                "DEF_SIGNATURE_AXIS_STRATIFICATION",
            ),
        ),
        SignatureExtractor(
            "cp1_state_signature",
            lambda value: isinstance(value, CP1State),
            lambda value: _signature(
                value,
                family="cp1_state",
                axes=(
                    (SignatureAxis.DIMENSION, 2),
                    (
                        SignatureAxis.STATE,
                        (value.alpha, value.beta),
                    ),
                ),
                claim_ids=("REF_CP1",),
            ),
            (
                "DEF_RDSS_CANONICAL_SIGNATURE",
                "DEF_SIGNATURE_AXIS_STRATIFICATION",
            ),
        ),
        SignatureExtractor(
            "moire_rotation_signature",
            lambda value: isinstance(value, MoireRotation),
            lambda value: _signature(
                value,
                family="moire_relative_rotation",
                axes=(
                    (SignatureAxis.ORBIT, "relative_rotation"),
                    (SignatureAxis.PHASE, value.delta),
                ),
                claim_ids=("DER_MOIRE",),
            ),
            (
                "DEF_RDSS_CANONICAL_SIGNATURE",
                "DEF_SIGNATURE_AXIS_STRATIFICATION",
            ),
        ),

        SignatureExtractor(
            "typed_zero_signature",
            lambda value: isinstance(value, TypedZero),
            lambda value: _signature(
                value,
                family="typed_zero",
                axes=(
                    (SignatureAxis.CARRIER, value.carrier),
                    (SignatureAxis.RANK, value.rank),
                    (SignatureAxis.SCALE, value.scale),
                    (SignatureAxis.DIMENSION, value.dimension),
                ),
                claim_ids=("DEF_TYPED_ZERO",),
            ),
            (
                "DEF_RDSS_CANONICAL_SIGNATURE",
                "DEF_SIGNATURE_AXIS_STRATIFICATION",
            ),
        ),
        SignatureExtractor(
            "semantic_scale_graph_signature",
            lambda value: isinstance(value, SemanticScaleGraph),
            lambda value: _signature(
                value,
                family="semantic_scale_graph",
                axes=(
                    (SignatureAxis.RELATIONS, value.edges),
                ),
                claim_ids=("PRIM_SCALE",),
            ),
            ("DEF_RDSS_CANONICAL_SIGNATURE",),
        ),
        SignatureExtractor(
            "minimal_distinction_signature",
            lambda value: isinstance(value, MinimalDistinction),
            lambda value: _signature(
                value,
                family="cp1_distinction",
                axes=(
                    (SignatureAxis.CARRIER, value.carrier),
                    (SignatureAxis.RELATIONS, value.label),
                    (
                        SignatureAxis.STATE,
                        (value.left, value.right),
                    ),
                ),
                claim_ids=("REF_CP1",),
            ),
            (
                "DEF_RDSS_CANONICAL_SIGNATURE",
                "DEF_SIGNATURE_AXIS_STRATIFICATION",
            ),
        ),
        SignatureExtractor(
            "center_half_turn_bridge_signature",
            lambda value: isinstance(value, CenterHalfTurnBridge),
            lambda value: _signature(
                value,
                family="center_half_turn_bridge",
                axes=(
                    (
                        SignatureAxis.RELATIONS,
                        (
                            value.balance_coordinate,
                            value.half_turn,
                        ),
                    ),
                ),
                claim_ids=("BRIDGE_CENTER_HALF_TURN",),
            ),
            ("DEF_RDSS_CANONICAL_SIGNATURE",),
        ),
        SignatureExtractor(
            "u1_phase_signature",
            lambda value: isinstance(value, U1Phase),
            lambda value: _signature(
                value,
                family="u1_phase",
                axes=(
                    (SignatureAxis.PHASE, value.value),
                ),
                claim_ids=("REF_U1_PHASE_VALUE",),
            ),
            (
                "DEF_RDSS_CANONICAL_SIGNATURE",
                "DEF_SIGNATURE_AXIS_STRATIFICATION",
            ),
        ),
        SignatureExtractor(
            "zero_axis_point_signature",
            lambda value: isinstance(value, ZeroAxisPoint),
            lambda value: _signature(
                value,
                family="zero_axis_point",
                axes=(
                    (SignatureAxis.DIMENSION, 1),
                    (SignatureAxis.STATE, value.t),
                ),
                claim_ids=("ZA_BRIDGE",),
            ),
            (
                "DEF_RDSS_CANONICAL_SIGNATURE",
                "DEF_SIGNATURE_AXIS_STRATIFICATION",
            ),
        ),
        SignatureExtractor(
            "binary_distinction_signature",
            lambda value: isinstance(value, BinaryDistinction),
            lambda value: _signature(
                value,
                family="binary_distinction",
                axes=(
                    (
                        SignatureAxis.RELATIONS,
                        (
                            value.host,
                            value.left,
                            value.right,
                        ),
                    ),
                ),
                claim_ids=("DEF_BINARY_DISTINCTION",),
            ),
            ("DEF_RDSS_CANONICAL_SIGNATURE",),
        ),
        SignatureExtractor(
            "branch_relation_occurrence_signature",
            lambda value: isinstance(value, BranchRelationOccurrence),
            lambda value: _signature(
                value,
                family="branch_relation_occurrence",
                axes=(
                    (SignatureAxis.OCCURRENCE, value.branch),
                    (
                        SignatureAxis.RELATIONS,
                        (
                            value.relation_label,
                            value.source,
                            value.target,
                        ),
                    ),
                ),
                claim_ids=("DEF_RELATIONAL_DISTINCTION",),
            ),
            (
                "DEF_RDSS_CANONICAL_SIGNATURE",
                "DEF_SIGNATURE_AXIS_STRATIFICATION",
            ),
        ),
        SignatureExtractor(
            "relational_binary_distinction_signature",
            lambda value: isinstance(value, RelationalBinaryDistinction),
            lambda value: _signature(
                value,
                family="relational_binary_distinction",
                axes=(
                    (
                        SignatureAxis.RELATIONS,
                        (
                            value.host,
                            value.left,
                            value.right,
                            value.left_relation,
                            value.right_relation,
                        ),
                    ),
                ),
                claim_ids=("DEF_RELATIONAL_DISTINCTION",),
            ),
            ("DEF_RDSS_CANONICAL_SIGNATURE",),
        ),
        SignatureExtractor(
            "relational_generative_model_signature",
            lambda value: isinstance(value, RelationalGenerativeModel),
            lambda value: _signature(
                value,
                family="relational_generative_model",
                axes=(
                    (
                        SignatureAxis.RELATIONS,
                        (
                            tuple(sorted(value.admitted)),
                            tuple(
                                sorted(
                                    value.distinctions,
                                    key=lambda item: (
                                        item.host,
                                        item.left,
                                        item.right,
                                        item.left_relation,
                                        item.right_relation,
                                    ),
                                )
                            ),
                        ),
                    ),
                ),
                claim_ids=("RA0_REL_STAR",),
            ),
            ("DEF_RDSS_CANONICAL_SIGNATURE",),
        ),
        SignatureExtractor(
            "generative_relation_model_signature",
            lambda value: isinstance(value, GenerativeRelationModel),
            lambda value: _signature(
                value,
                family="generative_relation_model",
                axes=(
                    (
                        SignatureAxis.RELATIONS,
                        (
                            tuple(sorted(value.admitted)),
                            tuple(
                                sorted(
                                    value.distinctions,
                                    key=lambda item: (
                                        item.host,
                                        item.left,
                                        item.right,
                                    ),
                                )
                            ),
                        ),
                    ),
                ),
                claim_ids=("RA0_STAR",),
            ),
            ("DEF_RDSS_CANONICAL_SIGNATURE",),
        ),
    )


def rdss_signature_engine() -> SignatureEngine:
    return SignatureEngine(rdss_signature_extractors())



@dataclass(frozen=True)
class SignatureRecord:
    ordinal: int
    signature: RDSSSignature
    strict_key: object
    value: object


@dataclass(frozen=True)
class CatalogAssessment:
    novelty: NoveltyKind
    signature: RDSSSignature
    representative: SignatureRecord | None = None

    @property
    def is_redundant(self) -> bool:
        return self.novelty in {
            NoveltyKind.EXACT_REPEAT,
            NoveltyKind.SIGNATURE_EQUIVALENT,
            NoveltyKind.REPRESENTATION_ONLY,
        }


@dataclass(frozen=True)
class SignatureCatalogSummary:
    records: int
    families: int
    structures: int
    semantic_states: int
    strict_values: int


class SignatureCatalog:
    """Deterministic in-memory index over RDSS semantic signatures.

    The catalog does not delete or merge user values. It classifies each value
    against already indexed records and exposes quotient-like groupings at
    family, structure, semantic-state and strict-payload levels.
    """

    def __init__(self, engine: SignatureEngine) -> None:
        self._engine = engine
        self._records: list[SignatureRecord] = []

    @property
    def records(self) -> tuple[SignatureRecord, ...]:
        return tuple(self._records)

    def assess(self, value: object) -> CatalogAssessment:
        signature = self._engine.signature(value)
        strict_key = strict_normal_form(value).key

        exact = tuple(
            record
            for record in self._records
            if record.strict_key == strict_key
        )
        if exact:
            return CatalogAssessment(
                NoveltyKind.EXACT_REPEAT,
                signature,
                exact[0],
            )

        semantic = tuple(
            record
            for record in self._records
            if record.signature.family == signature.family
            and record.signature.semantic_key == signature.semantic_key
        )
        if semantic:
            representation_variant = next(
                (
                    record
                    for record in semantic
                    if record.signature.representation
                    != signature.representation
                ),
                None,
            )
            if representation_variant is not None:
                return CatalogAssessment(
                    NoveltyKind.REPRESENTATION_ONLY,
                    signature,
                    representation_variant,
                )
            return CatalogAssessment(
                NoveltyKind.SIGNATURE_EQUIVALENT,
                signature,
                semantic[0],
            )

        structural = tuple(
            record
            for record in self._records
            if record.signature.family == signature.family
            and record.signature.structural_key == signature.structural_key
        )
        if structural:
            return CatalogAssessment(
                NoveltyKind.NEW_STATE,
                signature,
                structural[0],
            )

        same_family = tuple(
            record
            for record in self._records
            if record.signature.family == signature.family
        )
        if same_family:
            return CatalogAssessment(
                NoveltyKind.NEW_STRUCTURE,
                signature,
                same_family[0],
            )

        return CatalogAssessment(
            NoveltyKind.NEW_FAMILY,
            signature,
            None,
        )

    def add(self, value: object) -> CatalogAssessment:
        assessment = self.assess(value)
        self._records.append(
            SignatureRecord(
                ordinal=len(self._records),
                signature=assessment.signature,
                strict_key=strict_normal_form(value).key,
                value=value,
            )
        )
        return assessment

    def _group_by(
        self,
        key_fn: Callable[[SignatureRecord], object],
    ) -> tuple[tuple[SignatureRecord, ...], ...]:
        groups: dict[object, list[SignatureRecord]] = {}
        for record in self._records:
            key = key_fn(record)
            groups.setdefault(key, []).append(record)
        return tuple(
            tuple(groups[key])
            for key in sorted(groups, key=repr)
        )

    def family_groups(self) -> tuple[tuple[SignatureRecord, ...], ...]:
        return self._group_by(
            lambda record: record.signature.family
        )

    def structure_groups(self) -> tuple[tuple[SignatureRecord, ...], ...]:
        return self._group_by(
            lambda record: record.signature.structural_key
        )

    def semantic_groups(self) -> tuple[tuple[SignatureRecord, ...], ...]:
        return self._group_by(
            lambda record: record.signature.semantic_key
        )

    def strict_groups(self) -> tuple[tuple[SignatureRecord, ...], ...]:
        return self._group_by(
            lambda record: record.strict_key
        )

    def summary(self) -> SignatureCatalogSummary:
        return SignatureCatalogSummary(
            records=len(self._records),
            families=len(self.family_groups()),
            structures=len(self.structure_groups()),
            semantic_states=len(self.semantic_groups()),
            strict_values=len(self.strict_groups()),
        )


def rdss_signature_catalog() -> SignatureCatalog:
    return SignatureCatalog(rdss_signature_engine())
