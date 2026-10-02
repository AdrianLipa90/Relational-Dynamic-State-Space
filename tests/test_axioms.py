from pathlib import Path

from rdss.axioms import (
    CANONICAL_PROVENANCE,
    ClaimKind,
    claim_map,
    dependency_closure,
    foundational_axioms,
    foundational_laws,
    formation_rules,
    validate_dependency_dag,
)


def test_dependency_graph_is_acyclic_and_resolved():
    validate_dependency_dag()


def test_canonical_names_and_provenance_are_locked():
    claims = claim_map()

    assert "First Law of Existence" in claims["A0"].statement
    assert "Canonical name: First Law of Existence" in CANONICAL_PROVENANCE["A0"]
    assert "law of reality" in CANONICAL_PROVENANCE["A0"].lower()
    assert "not aliases" in CANONICAL_PROVENANCE["A0"]

    first_hamlet = CANONICAL_PROVENANCE["THM_FIRST_HAMLET_DISPERSION_STRUCTURE"]
    assert "DISPERSION/STRUCTURE" in first_hamlet
    assert "not the downstream durable role carrier N/S" in first_hamlet

    roles = CANONICAL_PROVENANCE["THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT"]
    assert "orientation-role orbit N/S" in roles
    assert "one carrier" in roles

    collatz = CANONICAL_PROVENANCE["THM_RELATION_ALGEBRA_DETERMINISTICALLY_GENERATES_COLLATZ_MAP"]
    assert "/2" in collatz
    assert "x3" in collatz
    assert "+1" in collatz
    assert "basis-direction set" in collatz
    assert "not the set of all non-identity operators" in collatz

    gaussian = CANONICAL_PROVENANCE["THM_L_CONSTANTS_SINGLE_GENERATOR_CLOSURE"]
    assert "g=q+J=2+J" in gaussian
    assert "L4=2" in gaussian
    assert "L5=N(g)=5" in gaussian
    assert "L3=7" in gaussian




def test_kappa_constant_density_is_explicit_reference_condition():
    claims = claim_map()

    assert claims["REF_KAPPA_UNIFORM_INFORMATION_DENSITY"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["REF_KAPPA_UNIFORM_INFORMATION_DENSITY"].depends_on == (
        "REF_KAPPA_MIXING_NORMALIZATION",
    )
    assert claims["DER_KAPPA_NORMALIZED_TURN"].depends_on == (
        "REF_KAPPA_UNIFORM_INFORMATION_DENSITY",
    )
    assert "not forced" in claims["REF_KAPPA_UNIFORM_INFORMATION_DENSITY"].statement


def test_ofhm_moire_uses_phase_data_not_lossy_coherence_inverse():
    claims = claim_map()

    assert claims["BRIDGE_OFHM_BEES_PHASE_DATA"].kind is ClaimKind.BRIDGE
    assert claims["BRIDGE_OFHM_BEES_RELATIVE_PHASE_COHERENCE"].depends_on == (
        "BRIDGE_OFHM_BEES_PHASE_DATA",
    )
    assert claims["DER_OFHM_MOIRE_COCYCLE"].depends_on == (
        "BRIDGE_OFHM_BEES_PHASE_DATA",
    )
    assert "lossy" in claims["BRIDGE_OFHM_BEES_RELATIVE_PHASE_COHERENCE"].statement.lower()


def test_ofhm_hilbert_hotel_enumeration_is_not_claimed_unique():
    claims = claim_map()
    text = claims["BRIDGE_OFHM_HILBERT_HOTEL_SHIFT"].statement.lower()

    assert "not a unique canonical enumeration" in text
    assert "no commutation law" in text

def test_monograph_locks_canonical_name_and_basis_wording():
    monograph = Path("monograph/main.tex").read_text(encoding="utf-8")

    assert "First Law of Existence" in monograph
    assert "Law of Reality" not in monograph
    assert "complete non-identity operator sector" not in monograph
    assert "three distinguished non-identity" in monograph
    assert "V_B=\\mathbb R e_-\\oplus\\mathbb R e_+" not in monograph
    assert "V_R=\\mathbb R e_N\\oplus\\mathbb R e_S" in monograph

def test_binary_relation_is_explicit_signature_definition():
    claims = claim_map()
    assert claims["DEF_BINARY_REL"].kind is ClaimKind.DEFINITION
    assert claims["DEF_BINARY_REL"].depends_on == ()



def test_occurrence_forgetful_projection_and_closure_theorems():
    claims = claim_map()

    assert claims["DEF_OCCURRENCE_FORGETFUL_PROJECTION"].kind is ClaimKind.DEFINITION
    projection_closure = dependency_closure("DEF_OCCURRENCE_FORGETFUL_PROJECTION")
    assert projection_closure == frozenset(
        {
            "DEF_OCCURRENCE_PATH",
            "DEF_RELATION_OCCURRENCE",
            "DEF_BINARY_REL",
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_POINT",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

    assert claims["THM_OCCURRENCE_COMPOSABILITY_PROJECTS"].kind is ClaimKind.THEOREM
    assert {
        "DEF_OCCURRENCE_FORGETFUL_PROJECTION",
        *projection_closure,
    } == dependency_closure("THM_OCCURRENCE_COMPOSABILITY_PROJECTS")

    assert claims["THM_OCCURRENCE_CLOSED_IMPLIES_VALUE_CLOSED"].kind is ClaimKind.THEOREM
    assert {
        "DEF_OCCURRENCE_FORGETFUL_PROJECTION",
        *projection_closure,
    } == dependency_closure("THM_OCCURRENCE_CLOSED_IMPLIES_VALUE_CLOSED")

    assert claims["REF_VALUE_CLOSED_OCCURRENCE_OPEN_COUNTERMODEL"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["THM_VALUE_CLOSED_NOT_OCCURRENCE_CLOSED"].kind is ClaimKind.THEOREM
    assert "REF_VALUE_CLOSED_OCCURRENCE_OPEN_COUNTERMODEL" in dependency_closure(
        "THM_VALUE_CLOSED_NOT_OCCURRENCE_CLOSED"
    )


def test_binary_distinction_is_occurrence_level_not_label_inequality():
    claims = claim_map()
    assert claims["DEF_BINARY_DISTINCTION"].kind is ClaimKind.DEFINITION
    assert set(claims["DEF_BINARY_DISTINCTION"].depends_on) == {
        "DEF_POINT",
        "DEF_OCCURRENCE_ADDRESS_SPACE",
    }


def test_occurrence_address_space_is_separate_from_carrier_values():
    claims = claim_map()

    assert claims["DEF_OCCURRENCE_ADDRESS_SPACE"].kind is ClaimKind.DEFINITION
    assert claims["DEF_OCCURRENCE_ADDRESS_SPACE"].depends_on == ()

    assert claims["DEF_CARRIER_OCCURRENCE_SEPARATION"].kind is ClaimKind.DEFINITION
    assert set(claims["DEF_CARRIER_OCCURRENCE_SEPARATION"].depends_on) == {
        "DEF_POINT",
        "DEF_OCCURRENCE_ADDRESS_SPACE",
    }

    assert claims["REF_RELATIONAL_POINT_BINARY_COORDINATE"].kind is ClaimKind.REFERENCE_REALIZATION
    assert dependency_closure("REF_RELATIONAL_POINT_BINARY_COORDINATE") == frozenset(
        {"DEF_POINT", "DEF_OCCURRENCE_ADDRESS_SPACE"}
    )


def test_relation_occurrence_and_occurrence_path_are_explicit_definitions():
    claims = claim_map()

    assert claims["DEF_RELATION_OCCURRENCE"].kind is ClaimKind.DEFINITION
    assert set(claims["DEF_RELATION_OCCURRENCE"].depends_on) == {
        "DEF_BINARY_REL",
        "DEF_CARRIER_OCCURRENCE_SEPARATION",
    }
    assert dependency_closure("DEF_RELATION_OCCURRENCE") == frozenset(
        {
            "DEF_BINARY_REL",
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_POINT",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

    assert claims["DEF_OCCURRENCE_PATH"].kind is ClaimKind.DEFINITION
    assert claims["DEF_OCCURRENCE_PATH"].depends_on == (
        "DEF_RELATION_OCCURRENCE",
    )
    assert dependency_closure("DEF_OCCURRENCE_PATH") == frozenset(
        {
            "DEF_RELATION_OCCURRENCE",
            "DEF_BINARY_REL",
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_POINT",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

def test_cp1_is_not_mislabeled_as_foundational_axiom():
    claims = claim_map()
    assert claims["REF_CP1"].kind is ClaimKind.REFERENCE_REALIZATION
    assert set(claims["REF_CP1"].depends_on) == {
        "DEF_POINT",
        "DEF_BINARY_DISTINCTION",
        "DEF_CP1_PROJECTIVE_EQUIVALENCE",
    }



def test_relationally_bound_distinction_is_explicit_definition():
    claims = claim_map()
    assert claims["DEF_RELATIONAL_DISTINCTION"].kind is ClaimKind.DEFINITION
    assert set(claims["DEF_RELATIONAL_DISTINCTION"].depends_on) == {
        "DEF_BINARY_DISTINCTION",
        "DEF_RELATION_OCCURRENCE",
    }
    assert dependency_closure("DEF_RELATIONAL_DISTINCTION") == frozenset(
        {
            "DEF_BINARY_DISTINCTION",
            "DEF_RELATION_OCCURRENCE",
            "DEF_BINARY_REL",
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
            "DEF_POINT",
        }
    )

def test_recursive_refinement_is_explicit_derivation_gate():
    claims = claim_map()
    assert claims["RR1"].kind is ClaimKind.DERIVATION_GATE
    assert "RA0" not in dependency_closure("RR1")
    assert set(claims["RR1"].depends_on) == {"A0", "DEF_POINT", "DEF_BINARY_DISTINCTION"}


def test_structural_primitives_do_not_silently_depend_on_ra0():
    claims = claim_map()
    for claim_id in ("PRIM_MODULE", "PRIM_PRODUCT", "PRIM_TENSOR_PRODUCT", "PRIM_CONTRACTION", "PRIM_SCALE", "PRIM_SEMANTIC_WEIGHTING", "PRIM_TRANSPORT", "PRIM_REFINEMENT_MAP", "PRIM_ORBIT"):
        assert claims[claim_id].kind is ClaimKind.STRUCTURAL_PRIMITIVE
        assert "RA0" not in dependency_closure(claim_id)


def test_moire_is_derived_from_orbital_primitive():
    claims = claim_map()
    assert claims["DER_MOIRE"].kind is ClaimKind.DERIVED
    assert dependency_closure("DER_MOIRE") == frozenset({"PRIM_ORBIT"})



def test_refinement_residual_depends_on_refinement_and_product():
    assert dependency_closure("DEF_REFINEMENT_RESIDUAL") == frozenset(
        {
            "A0",
            "PRIM_REFINEMENT_MAP",
            "RR1",
            "DEF_POINT",
            "DEF_BINARY_DISTINCTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
            "PRIM_PRODUCT",
            "PRIM_MODULE",
        }
    )

def test_zero_axis_is_a_bridge_not_an_axiom_of_general_algebra():
    claims = claim_map()
    assert claims["ZA_BRIDGE"].kind is ClaimKind.BRIDGE
    assert claims["ZA_BRIDGE"].depends_on == ()


def test_relational_holonomy_is_derived_from_typed_transport():
    claims = claim_map()
    assert claims["DER_HOLONOMY"].kind is ClaimKind.DERIVED
    assert dependency_closure("DER_HOLONOMY") == frozenset(
        {"PRIM_TRANSPORT", "DEF_BINARY_REL", "PRIM_MODULE"}
    )



def test_occurrence_holonomy_requires_occurrence_path_semantics():
    claims = claim_map()
    assert claims["DER_OCCURRENCE_HOLONOMY"].kind is ClaimKind.DERIVED
    assert dependency_closure("DER_OCCURRENCE_HOLONOMY") == frozenset(
        {
            "PRIM_TRANSPORT",
            "PRIM_MODULE",
            "DEF_BINARY_REL",
            "DEF_OCCURRENCE_PATH",
            "DEF_RELATION_OCCURRENCE",
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
            "DEF_POINT",
        }
    )


def test_occurrence_u1_representation_and_winding_dependencies():
    claims = claim_map()

    assert claims["REF_OCCURRENCE_HOLONOMY_U1"].kind is ClaimKind.REFERENCE_REALIZATION
    occurrence_base = frozenset(
        {
            "REF_OCCURRENCE_HOLONOMY_U1",
            "DER_OCCURRENCE_HOLONOMY",
            "PRIM_TRANSPORT",
            "PRIM_MODULE",
            "DEF_BINARY_REL",
            "DEF_OCCURRENCE_PATH",
            "DEF_RELATION_OCCURRENCE",
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
            "DEF_POINT",
        }
    )
    assert dependency_closure("REF_OCCURRENCE_HOLONOMY_U1") == (
        occurrence_base - {"REF_OCCURRENCE_HOLONOMY_U1"}
    )

    assert claims["DER_OCCURRENCE_WINDING"].kind is ClaimKind.DERIVED
    assert dependency_closure("DER_OCCURRENCE_WINDING") == occurrence_base


def test_branch_blind_occurrence_phase_lift_dependencies():
    claims = claim_map()

    assert claims["DER_BRANCH_BLIND_OCCURRENCE_PHASE"].kind is ClaimKind.DERIVED
    assert dependency_closure("DER_BRANCH_BLIND_OCCURRENCE_PHASE") == frozenset(
        {
            "REF_HOLONOMY_U1",
            "DER_HOLONOMY",
            "REF_OCCURRENCE_HOLONOMY_U1",
            "DER_OCCURRENCE_HOLONOMY",
            "PRIM_TRANSPORT",
            "PRIM_MODULE",
            "DEF_BINARY_REL",
            "DEF_OCCURRENCE_PATH",
            "DEF_RELATION_OCCURRENCE",
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
            "DEF_POINT",
        }
    )

def test_winding_depends_on_explicit_holonomy_u1_representation():
    claims = claim_map()
    assert claims["DER_WINDING"].kind is ClaimKind.DERIVED
    assert dependency_closure("DER_WINDING") == frozenset(
        {
            "REF_HOLONOMY_U1",
            "DER_HOLONOMY",
            "PRIM_TRANSPORT",
            "DEF_BINARY_REL",
            "PRIM_MODULE",
        }
    )


def test_foundational_law_set_is_small_and_explicit():
    ids = {claim.id for claim in foundational_laws()}
    assert ids == {"A0"}
    assert foundational_axioms() == foundational_laws()



def test_ra0_star_is_candidate_not_silent_replacement():
    claims = claim_map()

    assert claims["RA0_STAR"].kind is ClaimKind.DERIVATION_GATE
    assert set(claims["RA0_STAR"].depends_on) == {"DEF_POINT", "DEF_BINARY_DISTINCTION"}
    assert claims["THM_RR1_FROM_RA0_STAR"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_RR1_FROM_RA0_STAR") == frozenset(
        {
            "RA0_STAR",
            "DEF_POINT",
            "DEF_BINARY_DISTINCTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )


def test_ra0_rel_star_is_candidate_with_two_explicit_theorems():
    claims = claim_map()

    assert claims["RA0_REL_STAR"].kind is ClaimKind.DERIVATION_GATE
    assert set(claims["RA0_REL_STAR"].depends_on) == {
        "DEF_POINT",
        "DEF_RELATIONAL_DISTINCTION",
    }

    base = frozenset(
        {
            "RA0_REL_STAR",
            "DEF_RELATIONAL_DISTINCTION",
            "DEF_BINARY_DISTINCTION",
            "DEF_RELATION_OCCURRENCE",
            "DEF_BINARY_REL",
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
            "DEF_POINT",
        }
    )

    assert claims["THM_RA0_STAR_FROM_RA0_REL_STAR"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_RA0_STAR_FROM_RA0_REL_STAR") == base

    assert claims["THM_RA0_FROM_RA0_REL_STAR"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_RA0_FROM_RA0_REL_STAR") == base

    assert claims["THM_RR1_FROM_RA0_REL_STAR"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_RR1_FROM_RA0_REL_STAR") == base


def test_bare_meta0_minimal_point_cardinality_is_exact():
    claims = claim_map()

    assert claims["THM_META0_CARDINALITY_LOWER_BOUND"].kind is ClaimKind.THEOREM
    assert claims["REF_META0_SINGLETON_POINT_PRESENTATION"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["THM_META0_MINIMAL_CARRIER_CARDINALITY"].kind is ClaimKind.THEOREM

    closure = dependency_closure("THM_META0_MINIMAL_CARRIER_CARDINALITY")
    assert closure == frozenset(
        {
            "A0",
            "META0",
            "DEF_POINT",
            "THM_META0_CARDINALITY_LOWER_BOUND",
            "REF_META0_SINGLETON_POINT_PRESENTATION",
        }
    )


def test_singleton_foundation_minimality_splits_lower_bound_and_attainability():
    claims = claim_map()

    assert claims["THM_META0_CARDINALITY_LOWER_BOUND"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_META0_CARDINALITY_LOWER_BOUND") == frozenset(
        {
            "A0","META0"}
    )

    assert claims["REF_SINGLETON_RA0_REL_STAR_MODEL"].kind is ClaimKind.REFERENCE_REALIZATION
    witness_closure = dependency_closure("REF_SINGLETON_RA0_REL_STAR_MODEL")
    assert witness_closure == frozenset(
        {
            "A0",
            "META0",
            "RA0_REL_STAR",
            "DEF_POINT",
            "DEF_RELATIONAL_DISTINCTION",
            "DEF_BINARY_DISTINCTION",
            "DEF_RELATION_OCCURRENCE",
            "DEF_BINARY_REL",
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

    assert claims["THM_SINGLETON_FOUNDATION_MINIMALITY"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_SINGLETON_FOUNDATION_MINIMALITY") == frozenset(
        {
            "A0",
            "THM_META0_CARDINALITY_LOWER_BOUND",
            "REF_SINGLETON_RA0_REL_STAR_MODEL",
            "META0",
            "RA0_REL_STAR",
            "DEF_POINT",
            "DEF_RELATIONAL_DISTINCTION",
            "DEF_BINARY_DISTINCTION",
            "DEF_RELATION_OCCURRENCE",
            "DEF_BINARY_REL",
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

def test_current_canonical_foundation_is_the_first_law():
    ids = {claim.id for claim in foundational_laws()}
    assert ids == {"A0"}



def test_bilinearity_residual_has_only_product_and_module_dependencies():
    assert dependency_closure("DEF_BILINEARITY_RESIDUAL") == frozenset(
        {"PRIM_PRODUCT", "PRIM_MODULE"}
    )


def test_orbital_coherence_residual_has_only_orbit_and_module_dependencies():
    assert dependency_closure("DEF_ORBITAL_COHERENCE") == frozenset(
        {"PRIM_ORBIT", "PRIM_MODULE"}
    )



def test_scale_orbit_residual_depends_on_scale_orbit_and_module():
    assert dependency_closure("DEF_SCALE_ORBIT_RESIDUAL") == frozenset(
        {"PRIM_SCALE", "PRIM_ORBIT", "PRIM_MODULE"}
    )




def test_cross_operation_coherence_dependencies_are_explicit():
    assert dependency_closure("DEF_TRANSPORT_PRODUCT_COHERENCE") == frozenset(
        {"PRIM_TRANSPORT", "DEF_BINARY_REL", "PRIM_PRODUCT", "PRIM_MODULE"}
    )
    assert dependency_closure("DEF_SCALE_PRODUCT_COHERENCE") == frozenset(
        {"PRIM_SCALE", "PRIM_PRODUCT", "PRIM_MODULE"}
    )
    assert dependency_closure("DEF_ORBIT_PRODUCT_COHERENCE") == frozenset(
        {"PRIM_ORBIT", "PRIM_PRODUCT", "PRIM_MODULE"}
    )
    assert dependency_closure("DEF_REFINEMENT_TRANSPORT_COHERENCE") == frozenset(
        {
            "A0",
            "PRIM_REFINEMENT_MAP",
            "RR1",
            "DEF_POINT",
            "DEF_BINARY_DISTINCTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
            "PRIM_TRANSPORT",
            "DEF_BINARY_REL",
            "PRIM_MODULE",
        }
    )

def test_tensor_and_contraction_coherence_dependencies():
    assert dependency_closure("DEF_TENSOR_MAP_COHERENCE") == frozenset(
        {"PRIM_TENSOR_PRODUCT", "PRIM_MODULE"}
    )
    assert dependency_closure("DEF_CONTRACTION_MAP_COHERENCE") == frozenset(
        {"PRIM_CONTRACTION", "PRIM_MODULE"}
    )




def test_remaining_first_order_naturality_dependencies():
    assert dependency_closure("DEF_SCALE_TRANSPORT_COHERENCE") == frozenset(
        {
            "PRIM_SCALE",
            "PRIM_TRANSPORT",
            "DEF_BINARY_REL",
            "PRIM_MODULE",
        }
    )
    assert dependency_closure("DEF_ORBIT_TRANSPORT_COHERENCE") == frozenset(
        {
            "PRIM_ORBIT",
            "PRIM_TRANSPORT",
            "DEF_BINARY_REL",
            "PRIM_MODULE",
        }
    )
    assert dependency_closure("DEF_REFINEMENT_SCALE_COHERENCE") == frozenset(
        {
            "A0",
            "PRIM_REFINEMENT_MAP",
            "RR1",
            "DEF_POINT",
            "DEF_BINARY_DISTINCTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
            "PRIM_SCALE",
            "PRIM_MODULE",
        }
    )
    assert dependency_closure("DEF_REFINEMENT_ORBIT_COHERENCE") == frozenset(
        {
            "A0",
            "PRIM_REFINEMENT_MAP",
            "RR1",
            "DEF_POINT",
            "DEF_BINARY_DISTINCTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
            "PRIM_ORBIT",
            "PRIM_MODULE",
        }
    )

def test_tensor_monoidal_coherence_dependencies():
    assert dependency_closure("DEF_TENSOR_MONOIDAL_COHERENCE") == frozenset(
        {"PRIM_TENSOR_PRODUCT", "PRIM_MODULE"}
    )




def test_cp1_recursive_realization_is_reference_layer():
    claims = claim_map()
    assert claims["REF_CP1_REFINEMENT"].kind is ClaimKind.REFERENCE_REALIZATION
    assert dependency_closure("REF_CP1_REFINEMENT") == frozenset(
        {
            "A0",
            "REF_CP1",
            "RR1",
            "DEF_POINT",
            "DEF_BINARY_DISTINCTION",
            "DEF_CP1_PROJECTIVE_EQUIVALENCE",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )


def test_singleton_cp1_occurrence_realization_dependencies():
    claims = claim_map()
    assert claims["REF_SINGLETON_CP1_OCCURRENCE_REALIZATION"].kind is ClaimKind.REFERENCE_REALIZATION
    closure = dependency_closure("REF_SINGLETON_CP1_OCCURRENCE_REALIZATION")
    assert {
        "REF_MINIMAL_SINGLE_RELATION_VALUE_MODEL",
        "REF_CP1_REFINEMENT",
        "META0",
        "RA0_REL_STAR",
        "RR1",
        "REF_CP1",
        "DEF_POINT",
        "DEF_BINARY_DISTINCTION",
        "DEF_CP1_PROJECTIVE_EQUIVALENCE",
        "DEF_RELATIONAL_DISTINCTION",
        "DEF_RELATION_OCCURRENCE",
        "DEF_BINARY_REL",
        "DEF_CARRIER_OCCURRENCE_SEPARATION",
        "DEF_OCCURRENCE_ADDRESS_SPACE",
    } <= closure

def test_holonomy_u1_representation_is_independent_of_zero_axis():
    claims = claim_map()
    assert claims["REF_HOLONOMY_U1"].kind is ClaimKind.REFERENCE_REALIZATION
    assert dependency_closure("REF_HOLONOMY_U1") == frozenset(
        {
            "DER_HOLONOMY",
            "PRIM_TRANSPORT",
            "DEF_BINARY_REL",
            "PRIM_MODULE",
        }
    )


def test_zero_axis_lift_is_separate_reference_bridge():
    claims = claim_map()
    assert claims["REF_HOLONOMY_ZERO_AXIS"].kind is ClaimKind.REFERENCE_REALIZATION
    assert dependency_closure("REF_HOLONOMY_ZERO_AXIS") == frozenset(
        {
            "REF_HOLONOMY_U1",
            "DER_HOLONOMY",
            "PRIM_TRANSPORT",
            "DEF_BINARY_REL",
            "PRIM_MODULE",
            "ZA_BRIDGE",
        }
    )



def test_relational_potential_is_definition_not_physical_axiom():
    claims = claim_map()
    assert claims["PRIM_SEMANTIC_WEIGHTING"].kind is ClaimKind.STRUCTURAL_PRIMITIVE
    assert claims["DEF_RELATIONAL_POTENTIAL"].kind is ClaimKind.DEFINITION
    assert dependency_closure("PRIM_SEMANTIC_WEIGHTING") == frozenset(
        {"PRIM_SCALE"}
    )
    assert dependency_closure("DEF_RELATIONAL_POTENTIAL") == frozenset(
        {"PRIM_SEMANTIC_WEIGHTING", "PRIM_SCALE"}
    )


def test_semantic_potential_shift_and_attractor_are_derived():
    claims = claim_map()
    assert claims["DER_SEMANTIC_POTENTIAL_SHIFT"].kind is ClaimKind.DERIVED
    assert claims["DER_RELATIONAL_ATTRACTOR"].kind is ClaimKind.DERIVED
    assert dependency_closure("DER_SEMANTIC_POTENTIAL_SHIFT") == frozenset(
        {
            "DEF_RELATIONAL_POTENTIAL",
            "PRIM_SEMANTIC_WEIGHTING",
            "PRIM_SCALE",
        }
    )
    assert dependency_closure("DER_RELATIONAL_ATTRACTOR") == frozenset(
        {
            "DEF_RELATIONAL_POTENTIAL",
            "PRIM_SEMANTIC_WEIGHTING",
            "PRIM_SCALE",
        }
    )



def test_typed_zero_depends_on_exact_sector_primitives():
    claims = claim_map()
    assert claims["DEF_TYPED_ZERO"].kind is ClaimKind.DEFINITION
    assert dependency_closure("DEF_TYPED_ZERO") == frozenset(
        {
            "PRIM_MODULE",
            "DEF_POINT",
            "PRIM_SCALE",
        }
    )



def test_meta0_is_model_formation_rule_not_object_level_nothing():
    claims = claim_map()
    assert claims["META0"].kind is ClaimKind.FORMATION_RULE
    assert claims["META0"].depends_on == ("A0",)
    assert set(claim.id for claim in formation_rules()) == {
        "META0",
        "DEF_SOURCE_MINIMAL_PARITY_DYNAMICS_SIGNATURE",
    }


def test_ex0_is_theorem_of_model_formation_not_extra_object_axiom():
    claims = claim_map()
    assert claims["EX0"].kind is ClaimKind.THEOREM
    assert dependency_closure("EX0") == frozenset({"A0", "META0"})
    assert "EX0" not in {claim.id for claim in foundational_axioms()}




def test_ra0_rr1_do_not_imply_ra0_rel_star():
    claims = claim_map()

    assert claims["REF_RA0_RR1_UNBOUND_MODEL"].kind is ClaimKind.REFERENCE_REALIZATION
    assert dependency_closure("REF_RA0_RR1_UNBOUND_MODEL") == frozenset(
        {
            "A0",
            "META0",
            "RA0",
            "RR1",
            "DEF_POINT",
            "DEF_BINARY_DISTINCTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

    assert claims["THM_RA0_RR1_NOT_RA0_REL_STAR"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_RA0_RR1_NOT_RA0_REL_STAR") == frozenset(
        {
            "A0",
            "REF_RA0_RR1_UNBOUND_MODEL",
            "META0",
            "RA0",
            "RR1",
            "DEF_POINT",
            "DEF_BINARY_DISTINCTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )


def test_binary_occurrence_growth_and_countability_theorems():
    claims = claim_map()

    assert claims["THM_BINARY_OCCURRENCE_COUNT"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_BINARY_OCCURRENCE_COUNT") == frozenset(
        {
            "A0",
            "RR1",
            "DEF_POINT",
            "DEF_BINARY_DISTINCTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

    assert claims["THM_FINITE_WORD_OCCURRENCE_COUNTABILITY"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_FINITE_WORD_OCCURRENCE_COUNTABILITY") == frozenset(
        {
            "A0",
            "THM_BINARY_OCCURRENCE_COUNT",
            "RR1",
            "DEF_POINT",
            "DEF_BINARY_DISTINCTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )


def test_ideal_occurrence_boundary_claims():
    claims = claim_map()

    assert claims["DEF_OCCURRENCE_BOUNDARY"].kind is ClaimKind.DEFINITION
    assert dependency_closure("DEF_OCCURRENCE_BOUNDARY") == frozenset(
        {"DEF_OCCURRENCE_ADDRESS_SPACE"}
    )

    boundary_base = frozenset(
        {
            "DEF_OCCURRENCE_BOUNDARY",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

    assert claims["THM_BOUNDARY_CYLINDER_COUNT"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_BOUNDARY_CYLINDER_COUNT") == boundary_base

    assert claims["THM_OCCURRENCE_BOUNDARY_CONTINUUM"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_OCCURRENCE_BOUNDARY_CONTINUUM") == boundary_base

    assert claims["THM_RR1_REALIZES_BOUNDARY_PREFIX_CHAINS"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_RR1_REALIZES_BOUNDARY_PREFIX_CHAINS") == frozenset(
        {
            "A0",
            "RR1",
            "DEF_BINARY_DISTINCTION",
            "DEF_POINT",
            "DEF_OCCURRENCE_BOUNDARY",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )


def test_relation_value_cardinality_minimality():
    claims = claim_map()

    base = frozenset(
        {
            "A0",
            "META0",
            "RA0_REL_STAR",
            "DEF_POINT",
            "DEF_RELATIONAL_DISTINCTION",
            "DEF_BINARY_DISTINCTION",
            "DEF_RELATION_OCCURRENCE",
            "DEF_BINARY_REL",
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

    assert claims["THM_RELATION_VALUE_CARDINALITY_LOWER_BOUND"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_RELATION_VALUE_CARDINALITY_LOWER_BOUND") == base

    assert claims["REF_MINIMAL_SINGLE_RELATION_VALUE_MODEL"].kind is ClaimKind.REFERENCE_REALIZATION
    assert dependency_closure("REF_MINIMAL_SINGLE_RELATION_VALUE_MODEL") == base

    assert claims["THM_SINGLE_RELATION_VALUE_MINIMALITY"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_SINGLE_RELATION_VALUE_MINIMALITY") == frozenset(
        {
            "THM_RELATION_VALUE_CARDINALITY_LOWER_BOUND",
            "REF_MINIMAL_SINGLE_RELATION_VALUE_MODEL",
            *base,
        }
    )


def test_relation_occurrence_cardinality_minimality():
    claims = claim_map()

    base = frozenset(
        {
            "A0",
            "META0",
            "RA0_REL_STAR",
            "DEF_POINT",
            "DEF_RELATIONAL_DISTINCTION",
            "DEF_BINARY_DISTINCTION",
            "DEF_RELATION_OCCURRENCE",
            "DEF_BINARY_REL",
            "DEF_CARRIER_OCCURRENCE_SEPARATION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

    assert claims["THM_RELATION_OCCURRENCE_CARDINALITY_LOWER_BOUND"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_RELATION_OCCURRENCE_CARDINALITY_LOWER_BOUND") == base

    assert claims["THM_TWO_RELATION_OCCURRENCE_MINIMALITY"].kind is ClaimKind.THEOREM
    occurrence_min_closure = dependency_closure("THM_TWO_RELATION_OCCURRENCE_MINIMALITY")
    assert {
        "THM_RELATION_OCCURRENCE_CARDINALITY_LOWER_BOUND",
        "REF_MINIMAL_SINGLE_RELATION_VALUE_MODEL",
        *base,
    } <= occurrence_min_closure

    assert claims["THM_MINIMAL_RELATIONAL_ATOM_SIGNATURE"].kind is ClaimKind.THEOREM
    atom_closure = dependency_closure("THM_MINIMAL_RELATIONAL_ATOM_SIGNATURE")
    assert {
        "THM_SINGLETON_FOUNDATION_MINIMALITY",
        "THM_SINGLE_RELATION_VALUE_MINIMALITY",
        "THM_TWO_RELATION_OCCURRENCE_MINIMALITY",
    } <= atom_closure


def test_occurrence_address_free_monoid_and_refinement_action_dependencies():
    claims = claim_map()

    assert claims["DEF_OCCURRENCE_ADDRESS_SPACE"].kind is ClaimKind.DEFINITION
    assert dependency_closure("DEF_OCCURRENCE_ADDRESS_SPACE") == frozenset()

    assert claims["THM_OCCURRENCE_ADDRESS_FREE_MONOID"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_OCCURRENCE_ADDRESS_FREE_MONOID") == frozenset(
        {"DEF_OCCURRENCE_ADDRESS_SPACE"}
    )

    assert claims["THM_REFINEMENT_RIGHT_ACTION"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_REFINEMENT_RIGHT_ACTION") == frozenset(
        {"DEF_OCCURRENCE_ADDRESS_SPACE"}
    )

    assert claims["THM_RR1_REALIZES_FINITE_WORDS"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_RR1_REALIZES_FINITE_WORDS") == frozenset(
        {
            "A0",
            "RR1",
            "DEF_BINARY_DISTINCTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
            "DEF_POINT",
        }
    )


def test_refinement_level_grading_theorem():
    claims = claim_map()

    assert claims["THM_REFINEMENT_LEVEL_GRADING"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_REFINEMENT_LEVEL_GRADING") == frozenset(
        {
            "THM_REFINEMENT_RIGHT_ACTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )


def test_occurrence_prefix_meet_and_tree_metric_dependencies():
    claims = claim_map()

    assert claims["DEF_OCCURRENCE_PREFIX_ORDER"].kind is ClaimKind.DEFINITION
    assert dependency_closure("DEF_OCCURRENCE_PREFIX_ORDER") == frozenset(
        {"DEF_OCCURRENCE_ADDRESS_SPACE"}
    )

    assert claims["THM_OCCURRENCE_MEET_SEMILATTICE"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_OCCURRENCE_MEET_SEMILATTICE") == frozenset(
        {
            "DEF_OCCURRENCE_PREFIX_ORDER",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

    assert claims["DEF_OCCURRENCE_TREE_DISTANCE"].kind is ClaimKind.DEFINITION
    assert dependency_closure("DEF_OCCURRENCE_TREE_DISTANCE") == frozenset(
        {
            "THM_OCCURRENCE_MEET_SEMILATTICE",
            "DEF_OCCURRENCE_PREFIX_ORDER",
            "THM_REFINEMENT_LEVEL_GRADING",
            "THM_REFINEMENT_RIGHT_ACTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

    assert claims["THM_OCCURRENCE_TREE_METRIC"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_OCCURRENCE_TREE_METRIC") == frozenset(
        {
            "DEF_OCCURRENCE_TREE_DISTANCE",
            "THM_OCCURRENCE_MEET_SEMILATTICE",
            "DEF_OCCURRENCE_PREFIX_ORDER",
            "THM_REFINEMENT_LEVEL_GRADING",
            "THM_REFINEMENT_RIGHT_ACTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )



def test_canonical_reduction_claims_are_non_foundational():
    claims = claim_map()

    assert claims["DEF_CANONICAL_NORMAL_FORM"].kind is ClaimKind.DEFINITION
    assert claims["DEF_CANONICAL_NORMAL_FORM"].depends_on == ()

    assert claims["DEF_REDUCTION_RELATION_KIND"].kind is ClaimKind.DEFINITION
    assert dependency_closure("DEF_REDUCTION_RELATION_KIND") == frozenset(
        {"DEF_CANONICAL_NORMAL_FORM"}
    )

    assert claims["DEF_REDUCTION_INFORMATION_EFFECT"].kind is ClaimKind.DEFINITION
    assert dependency_closure("DEF_REDUCTION_INFORMATION_EFFECT") == frozenset(
        {
            "DEF_REDUCTION_RELATION_KIND",
            "DEF_CANONICAL_NORMAL_FORM",
        }
    )

    assert claims["DEF_REDUCTION_TRACE"].kind is ClaimKind.DEFINITION
    assert dependency_closure("DEF_REDUCTION_TRACE") == frozenset(
        {
            "DEF_REDUCTION_INFORMATION_EFFECT",
            "DEF_REDUCTION_RELATION_KIND",
            "DEF_CANONICAL_NORMAL_FORM",
        }
    )

    assert claims["THM_STRICT_NORMAL_FORM_IDEMPOTENCE"].kind is ClaimKind.THEOREM
    assert dependency_closure(
        "THM_STRICT_NORMAL_FORM_IDEMPOTENCE"
    ) == frozenset({"DEF_CANONICAL_NORMAL_FORM"})

    assert {
        "DEF_CANONICAL_NORMAL_FORM",
        "DEF_REDUCTION_RELATION_KIND",
        "DEF_REDUCTION_INFORMATION_EFFECT",
        "DEF_REDUCTION_TRACE",
        "THM_STRICT_NORMAL_FORM_IDEMPOTENCE",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_canonical_signature_claims_are_non_foundational():
    claims = claim_map()

    assert claims["DEF_RDSS_CANONICAL_SIGNATURE"].kind is ClaimKind.DEFINITION
    assert dependency_closure("DEF_RDSS_CANONICAL_SIGNATURE") == frozenset(
        {"DEF_CANONICAL_NORMAL_FORM"}
    )

    assert claims["DEF_SIGNATURE_AXIS_STRATIFICATION"].kind is ClaimKind.DEFINITION
    assert dependency_closure("DEF_SIGNATURE_AXIS_STRATIFICATION") == frozenset(
        {
            "DEF_RDSS_CANONICAL_SIGNATURE",
            "DEF_CANONICAL_NORMAL_FORM",
        }
    )

    assert claims["DEF_SIGNATURE_COMPARISON"].kind is ClaimKind.DEFINITION
    assert "DEF_SIGNATURE_AXIS_STRATIFICATION" in dependency_closure(
        "DEF_SIGNATURE_COMPARISON"
    )

    assert claims["DEF_SIGNATURE_NOVELTY_CLASSIFICATION"].kind is ClaimKind.DEFINITION
    assert "DEF_SIGNATURE_COMPARISON" in dependency_closure(
        "DEF_SIGNATURE_NOVELTY_CLASSIFICATION"
    )

    assert {
        "DEF_RDSS_CANONICAL_SIGNATURE",
        "DEF_SIGNATURE_AXIS_STRATIFICATION",
        "DEF_SIGNATURE_COMPARISON",
        "DEF_SIGNATURE_NOVELTY_CLASSIFICATION",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_signature_catalog_claim_depends_on_novelty_classification():
    claims = claim_map()

    assert claims["DEF_SIGNATURE_CATALOG"].kind is ClaimKind.DEFINITION
    closure = dependency_closure("DEF_SIGNATURE_CATALOG")
    assert "DEF_SIGNATURE_NOVELTY_CLASSIFICATION" in closure
    assert "DEF_SIGNATURE_COMPARISON" in closure
    assert "DEF_SIGNATURE_AXIS_STRATIFICATION" in closure
    assert "DEF_RDSS_CANONICAL_SIGNATURE" in closure
    assert "DEF_CANONICAL_NORMAL_FORM" in closure
    assert "DEF_SIGNATURE_CATALOG" not in {
        claim.id for claim in foundational_axioms()
    }


def test_reduction_termination_and_confluence_claims_are_scoped():
    claims = claim_map()

    assert claims["DEF_LEXICOGRAPHIC_REDUCTION_ORDER"].kind is ClaimKind.DEFINITION
    assert claims["THM_STRICT_LEX_DESCENT_TERMINATES"].kind is ClaimKind.THEOREM
    assert "DEF_LEXICOGRAPHIC_REDUCTION_ORDER" in dependency_closure(
        "THM_STRICT_LEX_DESCENT_TERMINATES"
    )

    assert claims["DEF_FINITE_CONFLUENCE_AUDIT"].kind is ClaimKind.DEFINITION
    assert "DEF_REDUCTION_TRACE" in dependency_closure(
        "DEF_FINITE_CONFLUENCE_AUDIT"
    )

    assert {
        "DEF_LEXICOGRAPHIC_REDUCTION_ORDER",
        "THM_STRICT_LEX_DESCENT_TERMINATES",
        "DEF_FINITE_CONFLUENCE_AUDIT",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_bridge_registry_claims_preserve_semantic_sort_separation():
    claims = claim_map()

    assert claims["DEF_BRIDGE_REGISTRY"].kind is ClaimKind.DEFINITION
    assert "DEF_SIGNATURE_COMPARISON" in dependency_closure(
        "DEF_BRIDGE_REGISTRY"
    )

    assert claims["DEF_BRIDGE_ROUTE"].kind is ClaimKind.DEFINITION
    assert "DEF_BRIDGE_REGISTRY" in dependency_closure(
        "DEF_BRIDGE_ROUTE"
    )

    assert claims["DEF_BRIDGE_COMPARISON"].kind is ClaimKind.DEFINITION
    assert "DEF_BRIDGE_ROUTE" in dependency_closure(
        "DEF_BRIDGE_COMPARISON"
    )

    assert claims["REF_OCCURRENCE_POINT_BRIDGE"].kind is ClaimKind.REFERENCE_REALIZATION
    closure = dependency_closure("REF_OCCURRENCE_POINT_BRIDGE")
    assert "DEF_CARRIER_OCCURRENCE_SEPARATION" in closure
    assert "REF_RELATIONAL_POINT_BINARY_COORDINATE" in closure
    assert "DEF_BRIDGE_REGISTRY" in closure

    assert claims["THM_REFERENCE_COORDINATE_ROUNDTRIP"].kind is ClaimKind.THEOREM
    assert "REF_OCCURRENCE_POINT_BRIDGE" in dependency_closure(
        "THM_REFERENCE_COORDINATE_ROUNDTRIP"
    )

    assert {
        "DEF_BRIDGE_REGISTRY",
        "DEF_BRIDGE_ROUTE",
        "DEF_BRIDGE_COMPARISON",
        "REF_OCCURRENCE_POINT_BRIDGE",
        "THM_REFERENCE_COORDINATE_ROUNDTRIP",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_bridge_equivalence_graph_claims_keep_lossy_edges_out_of_components():
    claims = claim_map()

    assert claims["DEF_BRIDGE_EQUIVALENCE_GRAPH"].kind is ClaimKind.DEFINITION
    closure = dependency_closure("DEF_BRIDGE_EQUIVALENCE_GRAPH")
    assert "DEF_BRIDGE_COMPARISON" in closure
    assert "DEF_SIGNATURE_COMPARISON" in closure

    assert claims["DEF_BRIDGE_EQUIVALENCE_COMPONENT"].kind is ClaimKind.DEFINITION
    assert "DEF_BRIDGE_EQUIVALENCE_GRAPH" in dependency_closure(
        "DEF_BRIDGE_EQUIVALENCE_COMPONENT"
    )

    assert claims["THM_LOSSY_BRIDGE_NONUNION"].kind is ClaimKind.THEOREM
    assert "DEF_BRIDGE_EQUIVALENCE_COMPONENT" in dependency_closure(
        "THM_LOSSY_BRIDGE_NONUNION"
    )

    assert {
        "DEF_BRIDGE_EQUIVALENCE_GRAPH",
        "DEF_BRIDGE_EQUIVALENCE_COMPONENT",
        "THM_LOSSY_BRIDGE_NONUNION",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_bridge_gap_report_is_diagnostic_not_foundational():
    claims = claim_map()

    assert claims["DEF_BRIDGE_GAP_REPORT"].kind is ClaimKind.DEFINITION
    closure = dependency_closure("DEF_BRIDGE_GAP_REPORT")
    assert "DEF_BRIDGE_EQUIVALENCE_GRAPH" in closure
    assert "DEF_BRIDGE_GAP_REPORT" not in {
        claim.id for claim in foundational_axioms()
    }


def test_reference_corpus_scan_claims_are_diagnostic():
    claims = claim_map()

    assert claims["DEF_REFERENCE_CORPUS"].kind is ClaimKind.DEFINITION
    assert "DEF_RDSS_CANONICAL_SIGNATURE" in dependency_closure(
        "DEF_REFERENCE_CORPUS"
    )

    assert claims["DEF_REFERENCE_CORPUS_SCAN"].kind is ClaimKind.DEFINITION
    closure = dependency_closure("DEF_REFERENCE_CORPUS_SCAN")
    assert "DEF_REFERENCE_CORPUS" in closure
    assert "DEF_SIGNATURE_CATALOG" in closure
    assert "DEF_BRIDGE_EQUIVALENCE_GRAPH" in closure
    assert "DEF_BRIDGE_GAP_REPORT" in closure

    assert {
        "DEF_REFERENCE_CORPUS",
        "DEF_REFERENCE_CORPUS_SCAN",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_zero_sector_and_distinction_bridge_claims_are_scoped():
    claims = claim_map()

    assert claims["REF_TYPED_ZERO_ELEMENT_BRIDGE"].kind is ClaimKind.REFERENCE_REALIZATION
    closure = dependency_closure("REF_TYPED_ZERO_ELEMENT_BRIDGE")
    assert "DEF_TYPED_ZERO" in closure
    assert "DEF_TS" in closure
    assert "DEF_BRIDGE_REGISTRY" in closure

    assert claims["THM_TYPED_ZERO_ELEMENT_ROUNDTRIP"].kind is ClaimKind.THEOREM
    assert "REF_TYPED_ZERO_ELEMENT_BRIDGE" in dependency_closure(
        "THM_TYPED_ZERO_ELEMENT_ROUNDTRIP"
    )

    assert claims["DEF_RELATIONAL_DISTINCTION_FORGETFUL_PROJECTION"].kind is ClaimKind.DEFINITION
    closure = dependency_closure(
        "DEF_RELATIONAL_DISTINCTION_FORGETFUL_PROJECTION"
    )
    assert "DEF_RELATIONAL_DISTINCTION" in closure
    assert "DEF_BINARY_DISTINCTION" in closure
    assert "DEF_BRIDGE_REGISTRY" in closure

    assert {
        "REF_TYPED_ZERO_ELEMENT_BRIDGE",
        "THM_TYPED_ZERO_ELEMENT_ROUNDTRIP",
        "DEF_RELATIONAL_DISTINCTION_FORGETFUL_PROJECTION",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_relational_generative_projection_claim_is_non_foundational():
    claims = claim_map()

    assert claims["DEF_RELATIONAL_GENERATIVE_FORGETFUL_PROJECTION"].kind is ClaimKind.DEFINITION
    closure = dependency_closure(
        "DEF_RELATIONAL_GENERATIVE_FORGETFUL_PROJECTION"
    )
    assert "THM_RA0_STAR_FROM_RA0_REL_STAR" in closure
    assert "DEF_BRIDGE_REGISTRY" in closure
    assert "DEF_RELATIONAL_GENERATIVE_FORGETFUL_PROJECTION" not in {
        claim.id for claim in foundational_axioms()
    }


def test_bridge_gap_triage_is_diagnostic_and_non_foundational():
    claims = claim_map()

    assert claims["DEF_BRIDGE_GAP_TRIAGE"].kind is ClaimKind.DEFINITION
    closure = dependency_closure("DEF_BRIDGE_GAP_TRIAGE")
    assert "DEF_BRIDGE_GAP_REPORT" in closure
    assert "DEF_BRIDGE_REGISTRY" in closure
    assert "DEF_BRIDGE_GAP_TRIAGE" not in {
        claim.id for claim in foundational_axioms()
    }


def test_u1_zero_axis_bridge_claims_are_scoped():
    claims = claim_map()

    assert claims["REF_U1_PHASE_VALUE"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["DEF_BRIDGE_ROUNDTRIP_VALIDATOR"].kind is ClaimKind.DEFINITION
    assert "DEF_BRIDGE_REGISTRY" in dependency_closure(
        "DEF_BRIDGE_ROUNDTRIP_VALIDATOR"
    )

    assert claims["REF_U1_ZERO_AXIS_FINITE_BRIDGE"].kind is ClaimKind.REFERENCE_REALIZATION
    closure = dependency_closure("REF_U1_ZERO_AXIS_FINITE_BRIDGE")
    assert "REF_U1_PHASE_VALUE" in closure
    assert "ZA_BRIDGE" in closure
    assert "DEF_BRIDGE_ROUNDTRIP_VALIDATOR" in closure

    assert claims["THM_U1_ZERO_AXIS_FINITE_ROUNDTRIP"].kind is ClaimKind.THEOREM
    assert "REF_U1_ZERO_AXIS_FINITE_BRIDGE" in dependency_closure(
        "THM_U1_ZERO_AXIS_FINITE_ROUNDTRIP"
    )

    assert {
        "REF_U1_PHASE_VALUE",
        "DEF_BRIDGE_ROUNDTRIP_VALIDATOR",
        "REF_U1_ZERO_AXIS_FINITE_BRIDGE",
        "THM_U1_ZERO_AXIS_FINITE_ROUNDTRIP",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_contextual_bridge_claims_are_scoped_and_lossy():
    claims = claim_map()

    assert claims["DEF_CONTEXTUAL_BRIDGE_REGISTRY"].kind is ClaimKind.DEFINITION
    assert "DEF_BRIDGE_REGISTRY" in dependency_closure(
        "DEF_CONTEXTUAL_BRIDGE_REGISTRY"
    )

    assert claims["DEF_CARRIER_MAP_CONTEXT"].kind is ClaimKind.DEFINITION
    closure = dependency_closure("DEF_CARRIER_MAP_CONTEXT")
    assert "DEF_POINT" in closure
    assert "DEF_CONTEXTUAL_BRIDGE_REGISTRY" in closure

    assert claims["DEF_CONTEXTUAL_BRANCH_RELATION_MATERIALIZATION"].kind is ClaimKind.DEFINITION
    closure = dependency_closure(
        "DEF_CONTEXTUAL_BRANCH_RELATION_MATERIALIZATION"
    )
    assert "DEF_RELATIONAL_DISTINCTION" in closure
    assert "DEF_BINARY_REL" in closure
    assert "DEF_CARRIER_MAP_CONTEXT" in closure

    assert claims["THM_CONTEXTUAL_BRANCH_SLOT_NONINJECTIVE"].kind is ClaimKind.THEOREM
    assert "DEF_CONTEXTUAL_BRANCH_RELATION_MATERIALIZATION" in dependency_closure(
        "THM_CONTEXTUAL_BRANCH_SLOT_NONINJECTIVE"
    )

    assert {
        "DEF_CONTEXTUAL_BRIDGE_REGISTRY",
        "DEF_CARRIER_MAP_CONTEXT",
        "DEF_CONTEXTUAL_BRANCH_RELATION_MATERIALIZATION",
        "THM_CONTEXTUAL_BRANCH_SLOT_NONINJECTIVE",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_executable_bridge_invariant_claims_are_non_foundational():
    claims = claim_map()

    assert claims["DEF_EXECUTABLE_BRIDGE_INVARIANT"].kind is ClaimKind.DEFINITION
    assert "DEF_BRIDGE_REGISTRY" in dependency_closure(
        "DEF_EXECUTABLE_BRIDGE_INVARIANT"
    )
    assert claims["THM_REFERENCE_BRIDGE_INVARIANT_ENFORCEMENT"].kind is ClaimKind.THEOREM
    assert "DEF_EXECUTABLE_BRIDGE_INVARIANT" in dependency_closure(
        "THM_REFERENCE_BRIDGE_INVARIANT_ENFORCEMENT"
    )

    assert claims["DEF_EXECUTABLE_CONTEXTUAL_BRIDGE_INVARIANT"].kind is ClaimKind.DEFINITION
    closure = dependency_closure(
        "DEF_EXECUTABLE_CONTEXTUAL_BRIDGE_INVARIANT"
    )
    assert "DEF_CONTEXTUAL_BRIDGE_REGISTRY" in closure
    assert "DEF_EXECUTABLE_BRIDGE_INVARIANT" in closure

    assert claims["THM_REFERENCE_CONTEXTUAL_INVARIANT_ENFORCEMENT"].kind is ClaimKind.THEOREM
    assert "DEF_EXECUTABLE_CONTEXTUAL_BRIDGE_INVARIANT" in dependency_closure(
        "THM_REFERENCE_CONTEXTUAL_INVARIANT_ENFORCEMENT"
    )

    assert {
        "DEF_EXECUTABLE_BRIDGE_INVARIANT",
        "THM_REFERENCE_BRIDGE_INVARIANT_ENFORCEMENT",
        "DEF_EXECUTABLE_CONTEXTUAL_BRIDGE_INVARIANT",
        "THM_REFERENCE_CONTEXTUAL_INVARIANT_ENFORCEMENT",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_priority_free_rewrite_claims_do_not_assert_canonicality():
    claims = claim_map()

    assert claims["DEF_REWRITE_RULE"].kind is ClaimKind.DEFINITION
    closure = dependency_closure("DEF_REWRITE_RULE")
    assert "DEF_EXECUTABLE_BRIDGE_INVARIANT" in closure

    assert claims["DEF_PRIORITY_FREE_REWRITE_SYSTEM"].kind is ClaimKind.DEFINITION
    assert "DEF_REWRITE_RULE" in dependency_closure(
        "DEF_PRIORITY_FREE_REWRITE_SYSTEM"
    )

    assert claims["DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER"].kind is ClaimKind.DEFINITION
    closure = dependency_closure(
        "DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER"
    )
    assert "DEF_PRIORITY_FREE_REWRITE_SYSTEM" in closure
    assert "DEF_BRIDGE_REGISTRY" in closure

    assert claims["THM_NO_IMPLICIT_REWRITE_PRIORITY"].kind is ClaimKind.THEOREM
    assert "DEF_PRIORITY_FREE_REWRITE_SYSTEM" in dependency_closure(
        "THM_NO_IMPLICIT_REWRITE_PRIORITY"
    )

    assert claims["THM_REWRITE_CYCLE_FAIL_CLOSED"].kind is ClaimKind.THEOREM
    assert "DEF_PRIORITY_FREE_REWRITE_SYSTEM" in dependency_closure(
        "THM_REWRITE_CYCLE_FAIL_CLOSED"
    )

    assert {
        "DEF_REWRITE_RULE",
        "DEF_PRIORITY_FREE_REWRITE_SYSTEM",
        "DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER",
        "THM_NO_IMPLICIT_REWRITE_PRIORITY",
        "THM_REWRITE_CYCLE_FAIL_CLOSED",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_rewrite_termination_certificate_claims_are_scoped():
    claims = claim_map()

    assert claims["DEF_FAMILY_RANK_TERMINATION_CERTIFICATE"].kind is ClaimKind.DEFINITION
    assert "DEF_PRIORITY_FREE_REWRITE_SYSTEM" in dependency_closure(
        "DEF_FAMILY_RANK_TERMINATION_CERTIFICATE"
    )

    assert claims["THM_STRICT_FAMILY_RANK_TERMINATION"].kind is ClaimKind.THEOREM
    assert "DEF_FAMILY_RANK_TERMINATION_CERTIFICATE" in dependency_closure(
        "THM_STRICT_FAMILY_RANK_TERMINATION"
    )

    assert claims["REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE"].kind is ClaimKind.REFERENCE_REALIZATION
    closure = dependency_closure(
        "REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE"
    )
    assert "DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER" in closure
    assert "DEF_FAMILY_RANK_TERMINATION_CERTIFICATE" in closure

    assert claims["THM_REFERENCE_FORGETFUL_REWRITE_TERMINATES"].kind is ClaimKind.THEOREM
    closure = dependency_closure(
        "THM_REFERENCE_FORGETFUL_REWRITE_TERMINATES"
    )
    assert "REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE" in closure
    assert "THM_STRICT_FAMILY_RANK_TERMINATION" in closure

    assert {
        "DEF_FAMILY_RANK_TERMINATION_CERTIFICATE",
        "THM_STRICT_FAMILY_RANK_TERMINATION",
        "REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE",
        "THM_REFERENCE_FORGETFUL_REWRITE_TERMINATES",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_confluence_certificate_claims_preserve_selected_system_scope():
    claims = claim_map()

    assert claims["DEF_RULE_SOURCE_FAMILY_OVERLAP_AUDIT"].kind is ClaimKind.DEFINITION
    assert "DEF_PRIORITY_FREE_REWRITE_SYSTEM" in dependency_closure(
        "DEF_RULE_SOURCE_FAMILY_OVERLAP_AUDIT"
    )

    assert claims["DEF_DISTINCT_SOURCE_FAMILY_CONFLUENCE_CERTIFICATE"].kind is ClaimKind.DEFINITION
    assert "DEF_RULE_SOURCE_FAMILY_OVERLAP_AUDIT" in dependency_closure(
        "DEF_DISTINCT_SOURCE_FAMILY_CONFLUENCE_CERTIFICATE"
    )

    assert claims["THM_DISTINCT_SOURCE_FAMILY_DETERMINISM"].kind is ClaimKind.THEOREM
    assert "DEF_DISTINCT_SOURCE_FAMILY_CONFLUENCE_CERTIFICATE" in dependency_closure(
        "THM_DISTINCT_SOURCE_FAMILY_DETERMINISM"
    )

    assert claims["THM_DETERMINISTIC_REWRITE_CONFLUENCE"].kind is ClaimKind.THEOREM
    assert "THM_DISTINCT_SOURCE_FAMILY_DETERMINISM" in dependency_closure(
        "THM_DETERMINISTIC_REWRITE_CONFLUENCE"
    )

    assert claims["REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE"].kind is ClaimKind.REFERENCE_REALIZATION
    assert "DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER" in dependency_closure(
        "REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE"
    )

    assert claims["THM_REFERENCE_FORGETFUL_REWRITE_CONFLUENT"].kind is ClaimKind.THEOREM
    closure = dependency_closure(
        "THM_REFERENCE_FORGETFUL_REWRITE_CONFLUENT"
    )
    assert "REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE" in closure
    assert "THM_DETERMINISTIC_REWRITE_CONFLUENCE" in closure

    assert claims["THM_TERMINATING_CONFLUENT_UNIQUE_IRREDUCIBLE"].kind is ClaimKind.THEOREM
    closure = dependency_closure(
        "THM_TERMINATING_CONFLUENT_UNIQUE_IRREDUCIBLE"
    )
    assert "THM_STRICT_FAMILY_RANK_TERMINATION" in closure
    assert "THM_DETERMINISTIC_REWRITE_CONFLUENCE" in closure

    assert claims["THM_REFERENCE_FORGETFUL_UNIQUE_IRREDUCIBLE"].kind is ClaimKind.THEOREM
    closure = dependency_closure(
        "THM_REFERENCE_FORGETFUL_UNIQUE_IRREDUCIBLE"
    )
    assert "THM_REFERENCE_FORGETFUL_REWRITE_TERMINATES" in closure
    assert "THM_REFERENCE_FORGETFUL_REWRITE_CONFLUENT" in closure

    assert {
        "DEF_RULE_SOURCE_FAMILY_OVERLAP_AUDIT",
        "DEF_DISTINCT_SOURCE_FAMILY_CONFLUENCE_CERTIFICATE",
        "THM_DISTINCT_SOURCE_FAMILY_DETERMINISM",
        "THM_DETERMINISTIC_REWRITE_CONFLUENCE",
        "REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE",
        "THM_REFERENCE_FORGETFUL_REWRITE_CONFLUENT",
        "THM_TERMINATING_CONFLUENT_UNIQUE_IRREDUCIBLE",
        "THM_REFERENCE_FORGETFUL_UNIQUE_IRREDUCIBLE",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_scoped_normal_form_claims_do_not_promote_global_canonicality():
    claims = claim_map()

    assert claims["DEF_SCOPED_REWRITE_NORMAL_FORM"].kind is ClaimKind.DEFINITION
    assert "THM_TERMINATING_CONFLUENT_UNIQUE_IRREDUCIBLE" in dependency_closure(
        "DEF_SCOPED_REWRITE_NORMAL_FORM"
    )

    assert claims["REF_FORGETFUL_SCOPED_NORMAL_FORM"].kind is ClaimKind.REFERENCE_REALIZATION
    closure = dependency_closure(
        "REF_FORGETFUL_SCOPED_NORMAL_FORM"
    )
    assert "DEF_SCOPED_REWRITE_NORMAL_FORM" in closure
    assert "REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE" in closure
    assert "REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE" in closure

    assert claims["THM_REFERENCE_FORGETFUL_NORMAL_FORM_IDEMPOTENT"].kind is ClaimKind.THEOREM
    closure = dependency_closure(
        "THM_REFERENCE_FORGETFUL_NORMAL_FORM_IDEMPOTENT"
    )
    assert "REF_FORGETFUL_SCOPED_NORMAL_FORM" in closure
    assert "THM_REFERENCE_FORGETFUL_UNIQUE_IRREDUCIBLE" in closure

    assert {
        "DEF_SCOPED_REWRITE_NORMAL_FORM",
        "REF_FORGETFUL_SCOPED_NORMAL_FORM",
        "THM_REFERENCE_FORGETFUL_NORMAL_FORM_IDEMPOTENT",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_semantic_factorization_claims_reuse_signature_semantics():
    claims = claim_map()

    assert claims["DEF_SEMANTIC_FACTORIZATION"].kind is ClaimKind.DEFINITION
    closure = dependency_closure("DEF_SEMANTIC_FACTORIZATION")
    assert "DEF_RDSS_CANONICAL_SIGNATURE" in closure
    assert "DEF_SIGNATURE_AXIS_STRATIFICATION" in closure

    assert claims["THM_FACTORIZATION_RECONSTRUCTS_SEMANTIC_KEY"].kind is ClaimKind.THEOREM
    assert "DEF_SEMANTIC_FACTORIZATION" in dependency_closure(
        "THM_FACTORIZATION_RECONSTRUCTS_SEMANTIC_KEY"
    )

    assert claims["DEF_FACTORIZATION_COMPARISON"].kind is ClaimKind.DEFINITION
    assert "DEF_SEMANTIC_FACTORIZATION" in dependency_closure(
        "DEF_FACTORIZATION_COMPARISON"
    )

    assert claims["REF_REFERENCE_CORPUS_FACTORIZATION_SUMMARY"].kind is ClaimKind.REFERENCE_REALIZATION
    closure = dependency_closure(
        "REF_REFERENCE_CORPUS_FACTORIZATION_SUMMARY"
    )
    assert "DEF_REFERENCE_CORPUS" in closure
    assert "DEF_SEMANTIC_FACTORIZATION" in closure

    assert {
        "DEF_SEMANTIC_FACTORIZATION",
        "THM_FACTORIZATION_RECONSTRUCTS_SEMANTIC_KEY",
        "DEF_FACTORIZATION_COMPARISON",
        "REF_REFERENCE_CORPUS_FACTORIZATION_SUMMARY",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_claim_provenance_graph_is_a_projection_of_existing_ledger():
    claims = claim_map()

    assert claims["DEF_CLAIM_DEPENDENCY_PROJECTION"].kind is ClaimKind.DEFINITION
    assert "DEF_RDSS_CANONICAL_SIGNATURE" in dependency_closure(
        "DEF_CLAIM_DEPENDENCY_PROJECTION"
    )

    assert claims["THM_PROVENANCE_TOPOLOGICAL_ORDER"].kind is ClaimKind.THEOREM
    assert "DEF_CLAIM_DEPENDENCY_PROJECTION" in dependency_closure(
        "THM_PROVENANCE_TOPOLOGICAL_ORDER"
    )

    assert claims["DEF_VALUE_CLAIM_PROVENANCE"].kind is ClaimKind.DEFINITION
    closure = dependency_closure("DEF_VALUE_CLAIM_PROVENANCE")
    assert "DEF_CLAIM_DEPENDENCY_PROJECTION" in closure
    assert "DEF_SEMANTIC_FACTORIZATION" in closure
    assert "DEF_RDSS_CANONICAL_SIGNATURE" in closure

    assert claims["DEF_TRANSFORMATION_CLAIM_PROVENANCE"].kind is ClaimKind.DEFINITION
    closure = dependency_closure(
        "DEF_TRANSFORMATION_CLAIM_PROVENANCE"
    )
    assert "DEF_CLAIM_DEPENDENCY_PROJECTION" in closure
    assert "DEF_BRIDGE_ROUTE" in closure
    assert "DEF_PRIORITY_FREE_REWRITE_SYSTEM" in closure
    assert "DEF_SCOPED_REWRITE_NORMAL_FORM" in closure

    assert {
        "DEF_CLAIM_DEPENDENCY_PROJECTION",
        "THM_PROVENANCE_TOPOLOGICAL_ORDER",
        "DEF_VALUE_CLAIM_PROVENANCE",
        "DEF_TRANSFORMATION_CLAIM_PROVENANCE",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_object_reduction_certificate_claims_are_scoped():
    claims = claim_map()

    assert claims["DEF_OBJECT_REDUCTION_CERTIFICATE"].kind is ClaimKind.DEFINITION
    closure = dependency_closure("DEF_OBJECT_REDUCTION_CERTIFICATE")
    assert "DEF_VALUE_CLAIM_PROVENANCE" in closure
    assert "DEF_TRANSFORMATION_CLAIM_PROVENANCE" in closure
    assert "DEF_SCOPED_REWRITE_NORMAL_FORM" in closure
    assert "DEF_EXECUTABLE_BRIDGE_INVARIANT" in closure

    assert claims["REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE"].kind is ClaimKind.REFERENCE_REALIZATION
    closure = dependency_closure(
        "REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE"
    )
    assert "DEF_OBJECT_REDUCTION_CERTIFICATE" in closure
    assert "REF_FORGETFUL_SCOPED_NORMAL_FORM" in closure
    assert "REF_FORGETFUL_REWRITE_TERMINATION_CERTIFICATE" in closure
    assert "REF_FORGETFUL_REWRITE_CONFLUENCE_CERTIFICATE" in closure

    assert claims["THM_REFERENCE_OBJECT_REDUCTION_CERTIFICATE_CONSISTENT"].kind is ClaimKind.THEOREM
    closure = dependency_closure(
        "THM_REFERENCE_OBJECT_REDUCTION_CERTIFICATE_CONSISTENT"
    )
    assert "REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE" in closure
    assert "THM_REFERENCE_FORGETFUL_NORMAL_FORM_IDEMPOTENT" in closure
    assert "THM_PROVENANCE_TOPOLOGICAL_ORDER" in closure

    assert {
        "DEF_OBJECT_REDUCTION_CERTIFICATE",
        "REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE",
        "THM_REFERENCE_OBJECT_REDUCTION_CERTIFICATE_CONSISTENT",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_reduction_certificate_scan_claims_are_diagnostic():
    claims = claim_map()

    assert claims["DEF_REFERENCE_REDUCTION_CERTIFICATE_SCAN"].kind is ClaimKind.DEFINITION
    closure = dependency_closure(
        "DEF_REFERENCE_REDUCTION_CERTIFICATE_SCAN"
    )
    assert "DEF_REFERENCE_CORPUS" in closure
    assert "DEF_OBJECT_REDUCTION_CERTIFICATE" in closure

    assert claims["REF_REFERENCE_REDUCTION_CERTIFICATE_SCAN"].kind is ClaimKind.REFERENCE_REALIZATION
    closure = dependency_closure(
        "REF_REFERENCE_REDUCTION_CERTIFICATE_SCAN"
    )
    assert "DEF_REFERENCE_REDUCTION_CERTIFICATE_SCAN" in closure
    assert "REF_FORGETFUL_OBJECT_REDUCTION_CERTIFICATE" in closure

    assert {
        "DEF_REFERENCE_REDUCTION_CERTIFICATE_SCAN",
        "REF_REFERENCE_REDUCTION_CERTIFICATE_SCAN",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_loss_witness_claims_prove_reference_noninjectivity():
    claims = claim_map()

    assert claims["DEF_LOSS_WITNESS"].kind is ClaimKind.DEFINITION
    closure = dependency_closure("DEF_LOSS_WITNESS")
    assert "DEF_REWRITE_RULE" in closure
    assert "DEF_EXECUTABLE_BRIDGE_INVARIANT" in closure

    assert claims["REF_FORGETFUL_LOSS_WITNESSES"].kind is ClaimKind.REFERENCE_REALIZATION
    closure = dependency_closure(
        "REF_FORGETFUL_LOSS_WITNESSES"
    )
    assert "DEF_LOSS_WITNESS" in closure
    assert "DEF_FORGETFUL_BRIDGE_REWRITE_ADAPTER" in closure

    assert claims["THM_REFERENCE_FORGETFUL_REWRITES_NONINJECTIVE"].kind is ClaimKind.THEOREM
    assert "REF_FORGETFUL_LOSS_WITNESSES" in dependency_closure(
        "THM_REFERENCE_FORGETFUL_REWRITES_NONINJECTIVE"
    )

    assert {
        "DEF_LOSS_WITNESS",
        "REF_FORGETFUL_LOSS_WITNESSES",
        "THM_REFERENCE_FORGETFUL_REWRITES_NONINJECTIVE",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_cp1_projective_claims_separate_raw_representation_from_quotient():
    claims = claim_map()

    assert claims["DEF_CP1_PROJECTIVE_EQUIVALENCE"].kind is ClaimKind.DEFINITION
    assert dependency_closure("DEF_CP1_PROJECTIVE_EQUIVALENCE") == frozenset()
    assert "DEF_CP1_PROJECTIVE_EQUIVALENCE" in dependency_closure("REF_CP1")

    assert claims["THM_CP1_GLOBAL_PHASE_QUOTIENT"].kind is ClaimKind.THEOREM
    closure = dependency_closure(
        "THM_CP1_GLOBAL_PHASE_QUOTIENT"
    )
    assert "DEF_CP1_PROJECTIVE_EQUIVALENCE" in closure
    assert "REF_U1_PHASE_VALUE" in closure

    assert claims["REF_CP1_PROJECTIVE_CHART_QUOTIENT"].kind is ClaimKind.REFERENCE_REALIZATION
    assert "DEF_CP1_PROJECTIVE_EQUIVALENCE" in dependency_closure(
        "REF_CP1_PROJECTIVE_CHART_QUOTIENT"
    )

    assert claims["REF_REFERENCE_CORPUS_CP1_PROJECTIVE_QUOTIENT"].kind is ClaimKind.REFERENCE_REALIZATION
    closure = dependency_closure(
        "REF_REFERENCE_CORPUS_CP1_PROJECTIVE_QUOTIENT"
    )
    assert "DEF_REFERENCE_CORPUS" in closure
    assert "REF_CP1_PROJECTIVE_CHART_QUOTIENT" in closure

    assert {
        "DEF_CP1_PROJECTIVE_EQUIVALENCE",
        "THM_CP1_GLOBAL_PHASE_QUOTIENT",
        "REF_CP1_PROJECTIVE_CHART_QUOTIENT",
        "REF_REFERENCE_CORPUS_CP1_PROJECTIVE_QUOTIENT",
    }.isdisjoint(
        {claim.id for claim in foundational_axioms()}
    )


def test_unique_foundational_law_is_a0_legacy_identifier() -> None:
    claims = claim_map()
    assert claims["A0"].kind is ClaimKind.FOUNDATIONAL_LAW
    assert claims["A0"].depends_on == ()
    assert tuple(claim.id for claim in foundational_laws()) == ("A0",)
    assert tuple(claim.id for claim in foundational_axioms()) == ("A0",)
    assert claims["RA0"].kind is ClaimKind.DERIVATION_GATE
    assert claims["RR1"].kind is ClaimKind.DERIVATION_GATE
    assert claims["RA0_STAR"].kind is ClaimKind.DERIVATION_GATE
    assert claims["RA0_REL_STAR"].kind is ClaimKind.DERIVATION_GATE


def test_algebraic_geometric_cell_claims_do_not_add_axioms() -> None:
    claims = claim_map()

    assert claims["DEF_STATIC_CUBIC_FRAME"].kind is ClaimKind.DEFINITION
    assert claims["BRIDGE_TIR_EULER_BERRY_SPIN_HALF_POLARIZATION"].kind is ClaimKind.BRIDGE
    assert claims["DEF_STELLA_CUBIC_VERTEX_PARTITION"].kind is ClaimKind.DEFINITION
    assert claims["DEF_DYNAMIC_TETRAHEDRAL_PAIR"].kind is ClaimKind.DEFINITION
    assert claims["REF_STELLA_OCTANGULA_CUBIC_EMBEDDING"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["REF_OCTAHEDRAL_RELATIONAL_CORE"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["DEF_CUBIC_FACE_ADJACENCY_COMPLEX"].kind is ClaimKind.DEFINITION
    assert claims["REF_ALGEBRAIC_GEOMETRIC_INFORMATION_CELL"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["DEF_CUBIC_FACE_FRAME_TRANSPORT"].kind is ClaimKind.DEFINITION
    assert claims["DER_STELLA_SECTOR_TRANSPORT"].kind is ClaimKind.DERIVED
    assert claims["DER_CELL_RELATIVE_STATE_TO_MOIRE"].kind is ClaimKind.DERIVED
    assert claims["GATE_MOIRE_DYNAMICAL_LAW"].kind is ClaimKind.DERIVATION_GATE

    assert tuple(claim.id for claim in foundational_laws()) == ("A0",)

def test_pre_audit_existence_chain_claims_are_explicitly_typed() -> None:
    claims = claim_map()

    assert claims["DEF_EXISTENCE_POTENTIAL"].kind is ClaimKind.DEFINITION
    assert claims["DEF_EXISTENCE_POTENTIAL"].depends_on == ("A0",)

    assert claims["DEF_NONTRIVIAL_INFORMATION_STATE"].kind is ClaimKind.DEFINITION
    assert claims["DEF_PRIMITIVE_INDISTINCTION"].kind is ClaimKind.DEFINITION
    assert claims["DEF_DISTINCTION_PERSISTENCE_PREDICATE"].kind is ClaimKind.DEFINITION
    assert claims["THM_FIRST_HAMLET_DISPERSION_STRUCTURE"].kind is ClaimKind.THEOREM
    assert claims["DEF_CANONICAL_FIRST_HAMLET_NONDEGENERATE"].kind is ClaimKind.DEFINITION
    assert claims["THM_CANONICAL_FIRST_HAMLET_TWO_BRANCHES"].kind is ClaimKind.THEOREM
    assert claims["GATE_FIRST_HAMLET_NONDEGENERACY_FROM_PE_I0"].kind is ClaimKind.DERIVATION_GATE
    assert claims["THM_RELATIONAL_DEFORMATION_POTENTIAL_IS_DOWNSTREAM"].kind is ClaimKind.THEOREM
    assert claims["THM_BINARY_CLOSURE_MODEL_IS_DOWNSTREAM"].kind is ClaimKind.THEOREM
    assert claims["DEF_REFERENCE_DISTINCTION_AMPLITUDE"].kind is ClaimKind.DEFINITION
    assert claims["REF_PRIMITIVE_PERSISTENCE_GRADIENT_FLOW"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["THM_REF_PERSISTENCE_FLOW_DISPERSION"].kind is ClaimKind.THEOREM
    assert claims["THM_REF_PERSISTENCE_FLOW_STRUCTURE"].kind is ClaimKind.THEOREM
    assert claims["THM_REF_PERSISTENCE_FLOW_REALIZES_BOTH_HAMLET_REGIMES"].kind is ClaimKind.THEOREM
    assert claims["DEF_COLLATZ_ASSOCIATION_DISSOCIATION_CYCLE"].kind is ClaimKind.DEFINITION
    assert claims["THM_COLLATZ_ASSOCIATION_BALANCE"].kind is ClaimKind.THEOREM
    assert claims["REF_COLLATZ_DERIVED_PERSISTENCE_CONTROL"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["THM_COLLATZ_BALANCE_MATCHES_HAMLET_REGIMES"].kind is ClaimKind.THEOREM
    assert claims["GATE_BIND_PRIMITIVE_INDISTINCTION_TO_COLLATZ_STATE"].kind is ClaimKind.DERIVATION_GATE
    assert claims["DEF_SOURCE_MINIMAL_PARITY_DYNAMICS_SIGNATURE"].kind is ClaimKind.FORMATION_RULE
    assert claims["THM_DYAD_FORCES_ASSOCIATION_DIVISOR_TWO"].kind is ClaimKind.THEOREM
    assert claims["THM_MINIMAL_ODD_DISSOCIATION_MULTIPLIER_THREE"].kind is ClaimKind.THEOREM
    assert claims["THM_MINIMAL_POSITIVE_ODD_REPAIR_ONE"].kind is ClaimKind.THEOREM
    assert claims["THM_SOURCE_MINIMAL_AFFINE_PARITY_DYNAMICS_IS_COLLATZ"].kind is ClaimKind.THEOREM
    assert claims["GATE_SOURCE_MINIMALITY_APPLIES_TO_PRIMITIVE_DYNAMICS"].kind is ClaimKind.DERIVATION_GATE
    assert claims["GATE_DERIVE_COLLATZ_BRANCHES_FROM_RELATION_ALGEBRA"].kind is ClaimKind.DERIVATION_GATE
    assert claims["REF_COLLATZ_BRANCH_MOBIUS_PSL2_LIFT"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["THM_COLLATZ_BRANCH_SIGNED_LOG_JACOBIANS"].kind is ClaimKind.THEOREM
    assert claims["THM_FIRST_HAMLET_Z2"].kind is ClaimKind.THEOREM
    assert claims["THM_FIRST_HAMLET_HARTLEY_LN2"].kind is ClaimKind.THEOREM
    assert claims["THM_DISPERSION_RETURNS_INDISTINCTION"].kind is ClaimKind.THEOREM
    assert claims["DEF_NONTRIVIAL_INFORMATION_POINT"].kind is ClaimKind.DEFINITION
    assert claims["THM_STRUCTURE_BRANCH_MINIMAL_INFORMATION_POINT"].kind is ClaimKind.THEOREM
    assert claims["DEF_STRUCTURE_AS_PERSISTENT_RELATION"].kind is ClaimKind.DEFINITION
    assert claims["THM_STRUCTURE_BRANCH_MINIMAL_RELATION"].kind is ClaimKind.THEOREM
    assert claims["DEF_RELATION_ORIENTATION_REVERSAL"].kind is ClaimKind.DEFINITION
    assert claims["THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT"].kind is ClaimKind.THEOREM
    assert claims["THM_RELATION_ORIENTATION_Z2"].kind is ClaimKind.THEOREM
    assert claims["THM_RELATION_ROLE_HARTLEY_LN2"].kind is ClaimKind.THEOREM
    assert claims["THM_FIRST_HAMLET_NOT_PROJECTIVE_BINARY_CARRIER"].kind is ClaimKind.THEOREM
    assert claims["GATE_EXISTENCE_POTENTIAL_INFORMATIONALITY"].kind is ClaimKind.DERIVATION_GATE
    assert claims["THM_MINIMAL_INFORMATION_STATE_BINARY"].kind is ClaimKind.THEOREM
    assert claims["THM_TWO_STATE_AUTOMORPHISM_Z2"].kind is ClaimKind.THEOREM
    assert claims["THM_Z2_UNIQUE_NONTRIVIAL_REAL_CHARACTER"].kind is ClaimKind.THEOREM
    assert claims["GATE_EXISTENCE_POTENTIAL_HAMLET_BINARY"].kind is ClaimKind.DERIVATION_GATE
    assert claims["GATE_HAMLET_RELATIONAL_BINDING"].kind is ClaimKind.DERIVATION_GATE
    assert claims["THM_CANONICAL_REALIZED_EXISTENCE_RELATIONAL_BINARY"].kind is ClaimKind.THEOREM
    assert claims["THM_BINARY_BRANCH_SWAP_INVOLUTION"].kind is ClaimKind.THEOREM
    assert claims["THM_Z2_UNIQUE_SWAP_INVARIANT_PROBABILITY"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_HALF_HALF"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_LN2"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_RELATIONAL_ZETA_ZERO"].kind is ClaimKind.THEOREM
    assert claims["THM_BARE_CARRIER_POINT_DISTINCT_FROM_RELATIONAL_ZETA"].kind is ClaimKind.THEOREM
    assert claims["DEF_HAMLET_REAL_LINEAR_SPAN"].kind is ClaimKind.DEFINITION
    assert claims["THM_HAMLET_SWAP_POLARITY_ANTICOMMUTE"].kind is ClaimKind.THEOREM
    assert claims["THM_FIRST_HAMLET_SWAP_INVARIANT_UNIT_VECTOR"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_IMAGINARY_GENERATOR"].kind is ClaimKind.THEOREM
    assert claims["THM_IMAGINARY_GENERATOR_U1"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_COMPLEX_SCALAR_ALGEBRA"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_FULL_OPERATOR_ALGEBRA_M2R"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_OPERATOR_ALGEBRA_C2_MODULE"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_OPERATOR_FROBENIUS_NORM"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_OPERATOR_PROJECTIVE_CP1"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_S3_SU2_BIJECTION"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_SU2_U1_QUOTIENT_S2"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_BALANCED_ORBIT_BLOCH_EQUATOR"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_PAULI_TRIPLE"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_SU2_GENERATORS"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_SU2_CASIMIR_HALF"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_SPINOR_2PI_4PI_RETURN"].kind is ClaimKind.THEOREM
    assert claims["DEF_HAMLET_COMPLEX_BRANCH_SPACE"].kind is ClaimKind.DEFINITION
    assert claims["THM_HAMLET_UNIQUE_SYMMETRY_HERMITIAN_FORM"].kind is ClaimKind.THEOREM
    assert claims["REF_HAMLET_COUNTING_HERMITIAN_FORM"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["THM_HAMLET_PROJECTIVE_CP1"].kind is ClaimKind.THEOREM
    assert claims["REF_EXISTENCE_POTENTIAL_CP1_SPHERE"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["REF_RELATIONAL_ZETA_POTENTIAL_SPHERE_CENTER"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["REF_CP1_BERRY_GEOMETRIC_PHASE"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["REF_BERRY_PHASE_CONNECTION_POTENTIAL_CLASS"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["BRIDGE_EXISTENCE_POTENTIAL_AHARONOV_BOHM"].kind is ClaimKind.BRIDGE
    assert claims["THM_HAMLET_CANONICAL_PROJECTIVE_LOOP"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_PROJECTIVE_SIGN_CLOSURE"].kind is ClaimKind.THEOREM
    assert claims["THM_EULER_BERRY_MINIMAL_SPIN_HALF"].kind is ClaimKind.THEOREM

    spin_closure = dependency_closure("THM_EULER_BERRY_MINIMAL_SPIN_HALF")
    assert "DEF_EXISTENCE_POTENTIAL" in spin_closure
    assert "THM_HAMLET_IMAGINARY_GENERATOR" in spin_closure
    assert "REF_CP1_BERRY_GEOMETRIC_PHASE" in spin_closure
    assert "THM_HAMLET_PROJECTIVE_SIGN_CLOSURE" in spin_closure
    assert "REF_BERRY_PHASE_CONNECTION_POTENTIAL_CLASS" not in spin_closure

def test_structure_to_relation_uses_tir_minimum_structure_theorem() -> None:
    claims = claim_map()

    assert claims["BRIDGE_TIR_MIN_NONTRIVIAL_STRUCTURE_IS_RELATION"].kind is ClaimKind.BRIDGE
    assert claims["THM_STRUCTURE_BRANCH_MINIMAL_RELATION"].kind is ClaimKind.THEOREM

    closure = dependency_closure("THM_STRUCTURE_BRANCH_MINIMAL_RELATION")
    assert "BRIDGE_TIR_MIN_NONTRIVIAL_STRUCTURE_IS_RELATION" in closure
    assert "DEF_STRUCTURE_AS_PERSISTENT_RELATION" not in closure


def test_first_hamlet_selects_persistence_then_structure_yields_durable_relation_roles() -> None:
    claims = claim_map()

    hamlet_closure = dependency_closure("THM_FIRST_HAMLET_DISPERSION_STRUCTURE")
    assert "DEF_PRIMITIVE_INDISTINCTION" in hamlet_closure
    assert "DEF_DISTINCTION_PERSISTENCE_PREDICATE" in hamlet_closure
    assert "DEF_POINT" not in hamlet_closure

    structure_closure = dependency_closure("THM_STRUCTURE_BRANCH_MINIMAL_RELATION")
    assert "THM_FIRST_HAMLET_DISPERSION_STRUCTURE" in structure_closure
    assert "BRIDGE_TIR_MIN_NONTRIVIAL_STRUCTURE_IS_RELATION" in structure_closure
    assert "THM_STRUCTURE_BRANCH_MINIMAL_INFORMATION_POINT" not in structure_closure
    assert "DEF_BINARY_REL" not in structure_closure

    role_closure = dependency_closure("THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT")
    assert "THM_STRUCTURE_BRANCH_MINIMAL_RELATION" in role_closure
    assert "DEF_RELATION_ORIENTATION_REVERSAL" in role_closure

    durable_ln2 = dependency_closure("THM_RELATION_ROLE_HARTLEY_LN2")
    assert "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT" in durable_ln2
    assert "THM_HAMLET_HALF_HALF" not in durable_ln2
    assert "THM_Z2_UNIQUE_SWAP_INVARIANT_PROBABILITY" not in durable_ln2

    no_carrier = dependency_closure("THM_FIRST_HAMLET_NOT_PROJECTIVE_BINARY_CARRIER")
    assert "THM_DISPERSION_RETURNS_INDISTINCTION" in no_carrier
    assert "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT" in no_carrier

    assert claims["GATE_EXISTENCE_POTENTIAL_INFORMATIONALITY"].kind is ClaimKind.DERIVATION_GATE
    assert claims["GATE_DERIVE_COLLATZ_BRANCHES_FROM_RELATION_ALGEBRA"].kind is ClaimKind.DERIVATION_GATE


def test_half_half_is_downstream_of_first_hamlet_not_foundation_for_ln2() -> None:
    closure = dependency_closure("THM_HAMLET_HALF_HALF")
    assert "THM_FIRST_HAMLET_Z2" in closure
    assert "THM_Z2_UNIQUE_SWAP_INVARIANT_PROBABILITY" in closure
    assert "GATE_EXISTENCE_POTENTIAL_INFORMATIONALITY" not in closure
    assert "GATE_EXISTENCE_POTENTIAL_HAMLET_BINARY" not in closure
    assert "DEF_OCCURRENCE_ADDRESS_SPACE" not in closure

    shannon_closure = dependency_closure("THM_HAMLET_LN2")
    assert "THM_FIRST_HAMLET_HARTLEY_LN2" in shannon_closure
    assert "THM_HAMLET_HALF_HALF" in shannon_closure

def test_first_law_reaches_singleton_but_not_binary_without_extra_gate() -> None:
    claims = claim_map()

    assert claims["THM_FIRST_LAW_MINIMAL_NONTRIVIAL_CARRIER"].kind is ClaimKind.THEOREM
    carrier_closure = dependency_closure("THM_FIRST_LAW_MINIMAL_NONTRIVIAL_CARRIER")
    assert "A0" in carrier_closure
    assert "META0" in carrier_closure
    assert "REF_META0_SINGLETON_POINT_PRESENTATION" in carrier_closure

    assert claims["THM_FIRST_LAW_NONEMPTY_NOT_BINARY"].kind is ClaimKind.THEOREM
    no_binary_closure = dependency_closure("THM_FIRST_LAW_NONEMPTY_NOT_BINARY")
    assert "REF_META0_SINGLETON_POINT_PRESENTATION" in no_binary_closure
    assert "DEF_EXISTENCE_POTENTIAL" in no_binary_closure
    assert "GATE_EXISTENCE_POTENTIAL_HAMLET_BINARY" not in no_binary_closure

def test_first_hamlet_does_not_silently_assume_relational_binding() -> None:
    claims = claim_map()

    abstract_closure = dependency_closure("THM_FIRST_HAMLET_Z2")
    assert "RA0_REL_STAR" not in abstract_closure
    assert "DEF_RELATIONAL_DISTINCTION" not in abstract_closure

    assert claims["GATE_HAMLET_RELATIONAL_BINDING"].kind is ClaimKind.DERIVATION_GATE
    binding_closure = dependency_closure("GATE_HAMLET_RELATIONAL_BINDING")
    assert "THM_FIRST_HAMLET_Z2" in binding_closure
    assert "DEF_RELATIONAL_DISTINCTION" in binding_closure

def test_relation_direction_alone_does_not_supply_hamlet_branch_identity() -> None:
    claims = claim_map()

    assert claims["THM_RELATION_DIRECTION_NOT_BRANCH_DUPLICATION"].kind is ClaimKind.THEOREM
    closure = dependency_closure("THM_RELATION_DIRECTION_NOT_BRANCH_DUPLICATION")
    assert "DEF_BINARY_REL" in closure
    assert "DEF_RELATION_OCCURRENCE" in closure
    assert "DEF_CARRIER_OCCURRENCE_SEPARATION" in closure
    assert "GATE_HAMLET_RELATIONAL_BINDING" not in closure

def test_z2_nontrivial_character_closes_algebraic_minus_one_not_berry_loop_mapping() -> None:
    claims = claim_map()

    assert claims["THM_Z2_UNIQUE_NONTRIVIAL_REAL_CHARACTER"].kind is ClaimKind.THEOREM
    assert claims["THM_Z2_SIGN_EMBEDS_U1"].kind is ClaimKind.THEOREM
    sign_closure = dependency_closure("THM_Z2_UNIQUE_NONTRIVIAL_REAL_CHARACTER")
    assert "THM_RELATION_ORIENTATION_Z2" in sign_closure
    assert "THM_FIRST_HAMLET_Z2" not in sign_closure
    assert "REF_CP1_BERRY_GEOMETRIC_PHASE" not in sign_closure

    loop_gate = claims["THM_HAMLET_PROJECTIVE_SIGN_CLOSURE"]
    assert loop_gate.kind is ClaimKind.THEOREM
    loop_closure = dependency_closure("THM_HAMLET_PROJECTIVE_SIGN_CLOSURE")
    assert "THM_Z2_UNIQUE_NONTRIVIAL_REAL_CHARACTER" in loop_closure
    assert "THM_Z2_SIGN_EMBEDS_U1" in loop_closure
    assert "THM_HAMLET_CANONICAL_PROJECTIVE_LOOP" in loop_closure
    assert "REF_CP1_BERRY_GEOMETRIC_PHASE" in loop_closure

def test_hamlet_swap_and_polarity_generate_complex_structure_without_upstream_u1() -> None:
    claims = claim_map()

    assert claims["DEF_HAMLET_REAL_LINEAR_SPAN"].kind is ClaimKind.DEFINITION
    assert claims["THM_HAMLET_SWAP_POLARITY_ANTICOMMUTE"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_IMAGINARY_GENERATOR"].kind is ClaimKind.THEOREM

    j_closure = dependency_closure("THM_HAMLET_IMAGINARY_GENERATOR")
    assert "THM_RELATION_ORIENTATION_Z2" in j_closure
    assert "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT" in j_closure
    assert "THM_FIRST_HAMLET_Z2" not in j_closure
    assert "THM_BINARY_BRANCH_SWAP_INVOLUTION" not in j_closure
    assert "DEF_OCCURRENCE_ADDRESS_SPACE" not in j_closure
    assert "THM_Z2_UNIQUE_NONTRIVIAL_REAL_CHARACTER" in j_closure
    assert "THM_IMAGINARY_GENERATOR_U1" not in j_closure
    assert "REF_U1_PHASE_VALUE" not in j_closure

    u1_closure = dependency_closure("THM_IMAGINARY_GENERATOR_U1")
    assert "THM_HAMLET_IMAGINARY_GENERATOR" in u1_closure

def test_projective_geometry_uses_durable_relation_roles_not_persistence_classes() -> None:
    cp1_closure = dependency_closure("THM_HAMLET_OPERATOR_PROJECTIVE_CP1")
    spin_closure = dependency_closure("THM_EULER_BERRY_MINIMAL_SPIN_HALF")

    for closure in (cp1_closure, spin_closure):
        assert "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT" in closure
        assert "THM_RELATION_ORIENTATION_Z2" in closure
        assert "THM_FIRST_HAMLET_Z2" not in closure
        assert "THM_FIRST_HAMLET_NOT_PROJECTIVE_BINARY_CARRIER" in closure


def test_source_minimal_collatz_theorem_is_conditional_and_inheritance_gate_stays_open() -> None:
    claims = claim_map()

    theorem = claims["THM_SOURCE_MINIMAL_AFFINE_PARITY_DYNAMICS_IS_COLLATZ"]
    assert theorem.kind is ClaimKind.THEOREM
    closure = dependency_closure("THM_SOURCE_MINIMAL_AFFINE_PARITY_DYNAMICS_IS_COLLATZ")
    assert "DEF_SOURCE_MINIMAL_PARITY_DYNAMICS_SIGNATURE" in closure
    assert "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT" in closure
    assert "GATE_SOURCE_MINIMALITY_APPLIES_TO_PRIMITIVE_DYNAMICS" not in closure

    gate = claims["GATE_SOURCE_MINIMALITY_APPLIES_TO_PRIMITIVE_DYNAMICS"]
    assert gate.kind is ClaimKind.DERIVATION_GATE
    gate_closure = dependency_closure("GATE_SOURCE_MINIMALITY_APPLIES_TO_PRIMITIVE_DYNAMICS")
    assert "A0" in gate_closure
    assert "THM_STRUCTURE_BRANCH_MINIMAL_RELATION" in gate_closure
    assert "DEF_SOURCE_MINIMAL_PARITY_DYNAMICS_SIGNATURE" in gate_closure

    collatz_def = claims["DEF_COLLATZ_ASSOCIATION_DISSOCIATION_CYCLE"]
    assert "THM_SOURCE_MINIMAL_AFFINE_PARITY_DYNAMICS_IS_COLLATZ" in collatz_def.depends_on


def test_canonical_collatz_operations_use_named_operator_sectors() -> None:
    claims = claim_map()

    assert claims["DEF_DISSOCIATION_AS_ACTIVE_OPERATOR_PRODUCT"].kind is ClaimKind.DEFINITION
    assert claims["THM_ACTIVE_OPERATOR_PRODUCT_CARDINALITY"].kind is ClaimKind.THEOREM
    assert claims["DEF_REPAIR_AS_IDENTITY_RESTORATION"].kind is ClaimKind.DEFINITION
    assert claims["THM_IDENTITY_REPAIR_CARDINALITY"].kind is ClaimKind.THEOREM
    assert claims["THM_RELATION_ALGEBRA_DETERMINISTICALLY_GENERATES_COLLATZ_MAP"].kind is ClaimKind.THEOREM

    collatz_closure = dependency_closure("THM_RELATION_ALGEBRA_DETERMINISTICALLY_GENERATES_COLLATZ_MAP")
    assert "THM_ASSOCIATION_QUOTIENT_CARDINALITY" in collatz_closure
    assert "THM_ACTIVE_OPERATOR_PRODUCT_CARDINALITY" in collatz_closure
    assert "THM_IDENTITY_REPAIR_CARDINALITY" in collatz_closure
    assert "THM_PARITY_FORCES_COLLATZ_BRANCH_SELECTION" in collatz_closure

    # Generic F3/singleton helpers are retained, but the canonical theorem
    # must not depend on them.
    assert "DEF_DISSOCIATION_AS_THREE_FIBRE_EXTENSION" not in collatz_closure
    assert "DEF_REPAIR_AS_SINGLETON_COPRODUCT" not in collatz_closure


def test_active_seed_three_is_double_closed() -> None:
    claims = claim_map()

    assert claims["DEF_MINIMAL_NONTRIVIAL_DISSOCIATION_SEED"].kind is ClaimKind.DEFINITION
    assert claims["THM_MINIMAL_NONTRIVIAL_DISSOCIATION_SEED_IS_THREE"].kind is ClaimKind.THEOREM
    assert claims["THM_ACTIVE_SEED_IS_THREE"].kind is ClaimKind.THEOREM
    assert claims["THM_ACTIVE_SEED_PROVENANCE_DOUBLE_CLOSED"].kind is ClaimKind.THEOREM

    closure = dependency_closure("THM_ACTIVE_SEED_PROVENANCE_DOUBLE_CLOSED")
    assert "THM_MINIMAL_NONTRIVIAL_DISSOCIATION_SEED_IS_THREE" in closure
    assert "THM_ACTIVE_SEED_IS_THREE" in closure
    assert "THM_ASSOCIATION_QUOTIENT_CARDINALITY" in closure
    assert "DEF_ACTIVE_SEED_AS_NONIDENTITY_OPERATOR_COUNT" in closure


def test_gaussian_integer_lattice_is_downstream_of_phase_winding() -> None:
    claims = claim_map()

    assert claims["BRIDGE_TIR_CLOSED_PHASE_WINDING_INTEGERS"].kind is ClaimKind.BRIDGE
    assert claims["THM_RELATION_ROLE_GAUSSIAN_INTEGER_LATTICE"].kind is ClaimKind.THEOREM

    lattice_closure = dependency_closure("THM_RELATION_ROLE_GAUSSIAN_INTEGER_LATTICE")
    assert "THM_HAMLET_COMPLEX_SCALAR_ALGEBRA" in lattice_closure
    assert "BRIDGE_TIR_CLOSED_PHASE_WINDING_INTEGERS" in lattice_closure
    assert "THM_IMAGINARY_GENERATOR_U1" in lattice_closure

    lift_closure = dependency_closure("THM_MINIMAL_RELATION_ROLE_GAUSSIAN_GENERATOR")
    assert "THM_RELATION_ROLE_GAUSSIAN_INTEGER_LATTICE" in lift_closure


def test_l_constants_have_single_gaussian_generator_closure() -> None:
    claims = claim_map()

    theorem = claims["THM_L_CONSTANTS_SINGLE_GENERATOR_CLOSURE"]
    assert theorem.kind is ClaimKind.THEOREM
    closure = dependency_closure("THM_L_CONSTANTS_SINGLE_GENERATOR_CLOSURE")
    assert "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT" in closure
    assert "THM_MINIMAL_RELATION_ROLE_GAUSSIAN_GENERATOR" in closure
    assert "THM_GAUSSIAN_L45_SOURCE" in closure
    assert "BRIDGE_TIR_ROOT_EXTENSION_L3_FROM_GAUSSIAN_L45" in closure


def test_collatz_is_downstream_of_relation_roles_but_branch_derivation_remains_open() -> None:
    claims = claim_map()

    gate = claims["GATE_DERIVE_COLLATZ_BRANCHES_FROM_RELATION_ALGEBRA"]
    assert gate.kind is ClaimKind.DERIVATION_GATE
    gate_closure = dependency_closure("GATE_DERIVE_COLLATZ_BRANCHES_FROM_RELATION_ALGEBRA")
    assert "THM_RELATION_ORIENTATION_Z2" in gate_closure
    assert "THM_RELATION_ALGEBRA_DETERMINISTICALLY_GENERATES_COLLATZ_MAP" in gate_closure
    assert "THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ" in gate_closure
    assert "GATE_BIND_RELATIONAL_CARDINALITY_NORMALIZATION_TO_PRIMITIVE_NATURAL_DYNAMICS" in gate_closure
    assert "THM_RELATION_ROLE_HARTLEY_LN2" not in gate_closure

    psl2 = dependency_closure("REF_COLLATZ_BRANCH_MOBIUS_PSL2_LIFT")
    assert "DEF_COLLATZ_ASSOCIATION_DISSOCIATION_CYCLE" in psl2
    assert "GATE_DERIVE_COLLATZ_BRANCHES_FROM_RELATION_ALGEBRA" not in psl2

    sig = dependency_closure("THM_COLLATZ_BRANCH_SIGNED_LOG_JACOBIANS")
    assert "DEF_COLLATZ_ASSOCIATION_DISSOCIATION_CYCLE" in sig


def test_cp1_factorization_keeps_scalar_phase_and_branch_dimension_distinct() -> None:
    claims = claim_map()

    assert claims["THM_HAMLET_COMPLEX_SCALAR_ALGEBRA"].kind is ClaimKind.THEOREM
    scalar_closure = dependency_closure("THM_HAMLET_COMPLEX_SCALAR_ALGEBRA")
    assert "THM_HAMLET_IMAGINARY_GENERATOR" in scalar_closure

    assert claims["DEF_HAMLET_COMPLEX_BRANCH_SPACE"].kind is ClaimKind.DEFINITION
    branch_closure = dependency_closure("DEF_HAMLET_COMPLEX_BRANCH_SPACE")
    assert "THM_HAMLET_COMPLEX_SCALAR_ALGEBRA" in branch_closure
    assert "THM_MINIMAL_INFORMATION_STATE_BINARY" in branch_closure

    assert claims["THM_HAMLET_UNIQUE_SYMMETRY_HERMITIAN_FORM"].kind is ClaimKind.THEOREM
    hermitian_closure = dependency_closure("THM_HAMLET_UNIQUE_SYMMETRY_HERMITIAN_FORM")
    assert "THM_HAMLET_SWAP_POLARITY_ANTICOMMUTE" in hermitian_closure
    assert "THM_HAMLET_HALF_HALF" in hermitian_closure

    assert claims["REF_HAMLET_COUNTING_HERMITIAN_FORM"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["THM_HAMLET_PROJECTIVE_CP1"].kind is ClaimKind.THEOREM
    cp1_closure = dependency_closure("THM_HAMLET_PROJECTIVE_CP1")
    assert "DEF_HAMLET_COMPLEX_BRANCH_SPACE" in cp1_closure
    assert "THM_HAMLET_UNIQUE_SYMMETRY_HERMITIAN_FORM" in cp1_closure
    assert "REF_HAMLET_COUNTING_HERMITIAN_FORM" in cp1_closure
    assert "THM_IMAGINARY_GENERATOR_U1" in cp1_closure

def test_structure_branch_defines_realized_information_and_point_is_downstream() -> None:
    claims = claim_map()

    assert claims["DEF_RDSS_REALIZED_EXISTENCE_INFORMATION_STATE"].kind is ClaimKind.DEFINITION
    semantic_closure = dependency_closure("DEF_RDSS_REALIZED_EXISTENCE_INFORMATION_STATE")
    assert "THM_FIRST_HAMLET_DISPERSION_STRUCTURE" in semantic_closure
    assert "DEF_NONTRIVIAL_INFORMATION_STATE" in semantic_closure

    assert claims["THM_CANONICAL_REALIZED_EXISTENCE_BINARY"].kind is ClaimKind.THEOREM
    binary_closure = dependency_closure("THM_CANONICAL_REALIZED_EXISTENCE_BINARY")
    assert "THM_FIRST_HAMLET_Z2" in binary_closure
    assert "THM_STRUCTURE_BRANCH_MINIMAL_INFORMATION_POINT" in binary_closure

    strict_gate = claims["GATE_EXISTENCE_POTENTIAL_INFORMATIONALITY"]
    assert strict_gate.kind is ClaimKind.DERIVATION_GATE


def test_canonical_relational_information_realization_does_not_close_strict_binding_gate() -> None:
    claims = claim_map()

    assert claims["DEF_RDSS_RELATIONAL_INFORMATION_REALIZATION"].kind is ClaimKind.DEFINITION
    assert claims["REF_CANONICAL_HAMLET_RELATIONAL_REALIZATION"].kind is ClaimKind.REFERENCE_REALIZATION

    ref_closure = dependency_closure("REF_CANONICAL_HAMLET_RELATIONAL_REALIZATION")
    assert "DEF_RDSS_RELATIONAL_INFORMATION_REALIZATION" in ref_closure
    assert "DEF_RDSS_REALIZED_EXISTENCE_INFORMATION_STATE" in ref_closure

    assert claims["GATE_HAMLET_RELATIONAL_BINDING"].kind is ClaimKind.DERIVATION_GATE
    assert "GATE_HAMLET_RELATIONAL_BINDING" not in ref_closure

def test_canonical_relational_binary_is_semantic_theorem_not_strict_ra0_rel_star_proof() -> None:
    claims = claim_map()

    theorem = claims["THM_CANONICAL_REALIZED_EXISTENCE_RELATIONAL_BINARY"]
    assert theorem.kind is ClaimKind.THEOREM

    closure = dependency_closure("THM_CANONICAL_REALIZED_EXISTENCE_RELATIONAL_BINARY")
    assert "DEF_RDSS_REALIZED_EXISTENCE_INFORMATION_STATE" in closure
    assert "DEF_RDSS_RELATIONAL_INFORMATION_REALIZATION" in closure
    assert "THM_CANONICAL_REALIZED_EXISTENCE_BINARY" in closure
    assert "REF_CANONICAL_HAMLET_RELATIONAL_REALIZATION" in closure

    assert "RA0_REL_STAR" not in closure
    assert claims["RA0_REL_STAR"].kind is ClaimKind.DERIVATION_GATE
    assert claims["GATE_HAMLET_RELATIONAL_BINDING"].kind is ClaimKind.DERIVATION_GATE

def test_canonical_cp1_uses_full_hamlet_operator_algebra_without_binary_duplication() -> None:
    claims = claim_map()

    assert claims["THM_HAMLET_FULL_OPERATOR_ALGEBRA_M2R"].kind is ClaimKind.THEOREM
    m2_closure = dependency_closure("THM_HAMLET_FULL_OPERATOR_ALGEBRA_M2R")
    assert "THM_HAMLET_SWAP_POLARITY_ANTICOMMUTE" in m2_closure
    assert "THM_HAMLET_IMAGINARY_GENERATOR" in m2_closure

    assert claims["THM_HAMLET_OPERATOR_ALGEBRA_C2_MODULE"].kind is ClaimKind.THEOREM
    c2_closure = dependency_closure("THM_HAMLET_OPERATOR_ALGEBRA_C2_MODULE")
    assert "THM_HAMLET_COMPLEX_SCALAR_ALGEBRA" in c2_closure
    assert "THM_HAMLET_FULL_OPERATOR_ALGEBRA_M2R" in c2_closure
    assert "DEF_HAMLET_COMPLEX_BRANCH_SPACE" not in c2_closure

    assert claims["THM_HAMLET_OPERATOR_FROBENIUS_NORM"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_OPERATOR_PROJECTIVE_CP1"].kind is ClaimKind.THEOREM

    cp1_closure = dependency_closure("REF_EXISTENCE_POTENTIAL_CP1_SPHERE")
    assert "THM_HAMLET_OPERATOR_PROJECTIVE_CP1" in cp1_closure
    assert "THM_HAMLET_OPERATOR_ALGEBRA_C2_MODULE" in cp1_closure
    assert "DEF_HAMLET_COMPLEX_BRANCH_SPACE" not in cp1_closure

    loop_closure = dependency_closure("THM_HAMLET_CANONICAL_PROJECTIVE_LOOP")
    assert "THM_HAMLET_OPERATOR_PROJECTIVE_CP1" in loop_closure

def test_canonical_spin_chain_is_independent_of_occurrence_address_representation() -> None:
    closure = dependency_closure("THM_EULER_BERRY_MINIMAL_SPIN_HALF")

    assert "DEF_OCCURRENCE_ADDRESS_SPACE" not in closure
    assert "THM_OCCURRENCE_ADDRESS_FREE_MONOID" not in closure
    assert "THM_BINARY_BRANCH_SWAP_INVOLUTION" not in closure

def test_bare_nonvacuity_point_is_not_the_relational_zeta_point() -> None:
    claims = claim_map()

    assert claims["THM_BARE_CARRIER_POINT_DISTINCT_FROM_RELATIONAL_ZETA"].kind is ClaimKind.THEOREM
    closure = dependency_closure("THM_BARE_CARRIER_POINT_DISTINCT_FROM_RELATIONAL_ZETA")
    assert "THM_FIRST_LAW_MINIMAL_NONTRIVIAL_CARRIER" in closure
    assert "THM_HAMLET_RELATIONAL_ZETA_ZERO" in closure


def test_canonical_spin_chain_does_not_depend_on_bare_singleton_point() -> None:
    closure = dependency_closure("THM_EULER_BERRY_MINIMAL_SPIN_HALF")

    assert "THM_FIRST_LAW_MINIMAL_NONTRIVIAL_CARRIER" not in closure
    assert "REF_META0_SINGLETON_POINT_PRESENTATION" not in closure
    assert "DEF_POINT" not in closure

def test_half_representation_label_is_derived_from_hamlet_su2_before_berry_matching() -> None:
    claims = claim_map()

    assert claims["THM_HAMLET_PAULI_TRIPLE"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_SU2_GENERATORS"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_SU2_CASIMIR_HALF"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_SPINOR_2PI_4PI_RETURN"].kind is ClaimKind.THEOREM

    casimir_closure = dependency_closure("THM_HAMLET_SU2_CASIMIR_HALF")
    assert "THM_HAMLET_PAULI_TRIPLE" in casimir_closure
    assert "THM_HAMLET_SU2_GENERATORS" in casimir_closure
    assert "REF_CP1_BERRY_GEOMETRIC_PHASE" not in casimir_closure
    assert "THM_HAMLET_PROJECTIVE_SIGN_CLOSURE" not in casimir_closure

    final_closure = dependency_closure("THM_EULER_BERRY_MINIMAL_SPIN_HALF")
    assert "THM_HAMLET_SU2_CASIMIR_HALF" in final_closure
    assert "THM_HAMLET_SPINOR_2PI_4PI_RETURN" in final_closure
    assert "THM_HAMLET_PROJECTIVE_SIGN_CLOSURE" in final_closure

def test_s3_su2_and_hopf_quotient_are_inside_canonical_spin_closure() -> None:
    claims = claim_map()

    assert claims["THM_HAMLET_S3_SU2_BIJECTION"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_SU2_U1_QUOTIENT_S2"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_BALANCED_ORBIT_BLOCH_EQUATOR"].kind is ClaimKind.THEOREM

    quotient_closure = dependency_closure("THM_HAMLET_SU2_U1_QUOTIENT_S2")
    assert "THM_HAMLET_S3_SU2_BIJECTION" in quotient_closure
    assert "THM_HAMLET_OPERATOR_PROJECTIVE_CP1" in quotient_closure

    spin_closure = dependency_closure("THM_EULER_BERRY_MINIMAL_SPIN_HALF")
    assert "THM_HAMLET_BALANCED_ORBIT_BLOCH_EQUATOR" in spin_closure
    assert "THM_HAMLET_SU2_U1_QUOTIENT_S2" in spin_closure

def test_spin_closure_uses_swap_invariant_amplitude_not_probability_half_half() -> None:
    closure = dependency_closure("THM_EULER_BERRY_MINIMAL_SPIN_HALF")

    assert "THM_FIRST_HAMLET_SWAP_INVARIANT_UNIT_VECTOR" in closure
    assert "THM_HAMLET_HALF_HALF" not in closure
    assert "THM_Z2_UNIQUE_SWAP_INVARIANT_PROBABILITY" not in closure
    assert "THM_FIRST_HAMLET_HARTLEY_LN2" not in closure

def test_hartley_ln2_requires_two_nonempty_first_hamlet_branches() -> None:
    claims = claim_map()

    schema_closure = dependency_closure("THM_FIRST_HAMLET_DISPERSION_STRUCTURE")
    assert "DEF_CANONICAL_FIRST_HAMLET_NONDEGENERATE" not in schema_closure

    two_branch_closure = dependency_closure("THM_CANONICAL_FIRST_HAMLET_TWO_BRANCHES")
    assert "DEF_CANONICAL_FIRST_HAMLET_NONDEGENERATE" in two_branch_closure

    ln2_closure = dependency_closure("THM_FIRST_HAMLET_HARTLEY_LN2")
    assert "THM_CANONICAL_FIRST_HAMLET_TWO_BRANCHES" in ln2_closure
    assert "GATE_FIRST_HAMLET_NONDEGENERACY_FROM_PE_I0" not in ln2_closure

    strict_gate = claims["GATE_FIRST_HAMLET_NONDEGENERACY_FROM_PE_I0"]
    assert strict_gate.kind is ClaimKind.DERIVATION_GATE

def test_existing_potential_and_binary_closure_cannot_be_used_upstream_for_first_hamlet() -> None:
    claims = claim_map()

    assert claims["THM_RELATIONAL_DEFORMATION_POTENTIAL_IS_DOWNSTREAM"].kind is ClaimKind.THEOREM
    potential_closure = dependency_closure("THM_RELATIONAL_DEFORMATION_POTENTIAL_IS_DOWNSTREAM")
    assert "DEF_RELATIONAL_POTENTIAL" in potential_closure
    assert "PRIM_SEMANTIC_WEIGHTING" in potential_closure

    assert claims["THM_BINARY_CLOSURE_MODEL_IS_DOWNSTREAM"].kind is ClaimKind.THEOREM
    closure_closure = dependency_closure("THM_BINARY_CLOSURE_MODEL_IS_DOWNSTREAM")
    assert "DEF_OCCURRENCE_ADDRESS_SPACE" in closure_closure

    first_hamlet_closure = dependency_closure("THM_FIRST_HAMLET_DISPERSION_STRUCTURE")
    assert "DEF_RELATIONAL_POTENTIAL" not in first_hamlet_closure
    assert "PRIM_SEMANTIC_WEIGHTING" not in first_hamlet_closure
    assert "DEF_OCCURRENCE_ADDRESS_SPACE" not in first_hamlet_closure
    assert "THM_RELATIONAL_DEFORMATION_POTENTIAL_IS_DOWNSTREAM" not in first_hamlet_closure
    assert "THM_BINARY_CLOSURE_MODEL_IS_DOWNSTREAM" not in first_hamlet_closure

def test_reference_persistence_flow_is_consistency_witness_not_foundational_derivation() -> None:
    claims = claim_map()

    both = claims["THM_REF_PERSISTENCE_FLOW_REALIZES_BOTH_HAMLET_REGIMES"]
    assert both.kind is ClaimKind.THEOREM
    both_closure = dependency_closure("THM_REF_PERSISTENCE_FLOW_REALIZES_BOTH_HAMLET_REGIMES")
    assert "REF_PRIMITIVE_PERSISTENCE_GRADIENT_FLOW" in both_closure
    assert "THM_REF_PERSISTENCE_FLOW_DISPERSION" in both_closure
    assert "THM_REF_PERSISTENCE_FLOW_STRUCTURE" in both_closure
    assert "THM_CANONICAL_FIRST_HAMLET_TWO_BRANCHES" in both_closure

    strict_gate = claims["GATE_FIRST_HAMLET_NONDEGENERACY_FROM_PE_I0"]
    assert strict_gate.kind is ClaimKind.DERIVATION_GATE
    strict_closure = dependency_closure("GATE_FIRST_HAMLET_NONDEGENERACY_FROM_PE_I0")
    assert "REF_PRIMITIVE_PERSISTENCE_GRADIENT_FLOW" not in strict_closure

    legacy_gate = claims["GATE_BIND_PRIMITIVE_INDISTINCTION_TO_COLLATZ_STATE"]
    assert legacy_gate.kind is ClaimKind.DERIVATION_GATE
    legacy_closure = dependency_closure("GATE_BIND_PRIMITIVE_INDISTINCTION_TO_COLLATZ_STATE")
    assert "DEF_PRIMITIVE_INDISTINCTION" in legacy_closure
    assert "THM_FIRST_HAMLET_NOT_PROJECTIVE_BINARY_CARRIER" in legacy_closure
    assert "REF_PRIMITIVE_PERSISTENCE_GRADIENT_FLOW" not in legacy_closure

def test_collatz_balance_is_downstream_and_operation_semantics_remain_the_gate() -> None:
    claims = claim_map()

    assert claims["DEF_COLLATZ_ASSOCIATION_DISSOCIATION_CYCLE"].kind is ClaimKind.DEFINITION
    assert claims["THM_COLLATZ_ASSOCIATION_BALANCE"].kind is ClaimKind.THEOREM
    assert claims["REF_COLLATZ_DERIVED_PERSISTENCE_CONTROL"].kind is ClaimKind.REFERENCE_REALIZATION
    assert claims["THM_COLLATZ_BALANCE_MATCHES_HAMLET_REGIMES"].kind is ClaimKind.THEOREM
    assert claims["THM_SOURCE_MINIMAL_AFFINE_PARITY_DYNAMICS_IS_COLLATZ"].kind is ClaimKind.THEOREM
    assert claims["GATE_SOURCE_MINIMALITY_APPLIES_TO_PRIMITIVE_DYNAMICS"].kind is ClaimKind.DERIVATION_GATE
    assert claims["GATE_DERIVE_COLLATZ_BRANCHES_FROM_RELATION_ALGEBRA"].kind is ClaimKind.DERIVATION_GATE

    balance_closure = dependency_closure("THM_COLLATZ_BALANCE_MATCHES_HAMLET_REGIMES")
    assert "THM_COLLATZ_ASSOCIATION_BALANCE" in balance_closure
    assert "REF_PRIMITIVE_PERSISTENCE_GRADIENT_FLOW" in balance_closure

    gate_closure = dependency_closure("GATE_DERIVE_COLLATZ_BRANCHES_FROM_RELATION_ALGEBRA")
    assert "THM_RELATION_ALGEBRA_DETERMINISTICALLY_GENERATES_COLLATZ_MAP" in gate_closure
    assert "THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ" in gate_closure
    assert "GATE_BIND_RELATIONAL_CARDINALITY_NORMALIZATION_TO_PRIMITIVE_NATURAL_DYNAMICS" in gate_closure
    assert "THM_COLLATZ_COEFFICIENT_PROVENANCE_TRIPLE_CLOSED" not in gate_closure


def test_gaussian_bombelli_route_is_independent_of_collatz_and_recovers_l_constants() -> None:
    claims = claim_map()

    assert claims["DEF_RELATION_ROLE_GAUSSIAN_LIFT_CLASS"].kind is ClaimKind.DEFINITION
    assert claims["THM_MINIMAL_RELATION_ROLE_GAUSSIAN_GENERATOR"].kind is ClaimKind.THEOREM
    assert claims["THM_GAUSSIAN_GENERATES_COLLATZ_COEFFICIENTS"].kind is ClaimKind.THEOREM
    assert claims["THM_GAUSSIAN_BOMBELLI_LADDER"].kind is ClaimKind.THEOREM
    assert claims["THM_GAUSSIAN_L45_SOURCE"].kind is ClaimKind.THEOREM
    assert claims["BRIDGE_TIR_ROOT_EXTENSION_L3_FROM_GAUSSIAN_L45"].kind is ClaimKind.BRIDGE
    assert claims["THM_GAUSSIAN_L3_24_CLOSURE_CROSSCHECK"].kind is ClaimKind.THEOREM
    assert claims["THM_COLLATZ_COEFFICIENT_PROVENANCE_DOUBLE_CLOSED"].kind is ClaimKind.THEOREM
    assert claims["THM_RELATION_OPERATOR_DIMENSION_COEFFICIENT_ROUTE"].kind is ClaimKind.THEOREM
    assert claims["THM_BINARY_UNIVERSAL_REPAIR_ONE"].kind is ClaimKind.THEOREM
    assert claims["THM_COLLATZ_COEFFICIENT_PROVENANCE_TRIPLE_CLOSED"].kind is ClaimKind.THEOREM
    assert claims["THM_L_CONSTANTS_SINGLE_GENERATOR_CLOSURE"].kind is ClaimKind.THEOREM
    assert claims["DEF_ACTIVE_SEED_AS_NONIDENTITY_OPERATOR_COUNT"].kind is ClaimKind.DEFINITION
    assert claims["THM_ACTIVE_SEED_IS_THREE"].kind is ClaimKind.THEOREM
    assert claims["THM_RELATIONAL_COLLATZ_L_CONSTANT_CERTIFICATE"].kind is ClaimKind.THEOREM
    assert claims["THM_L_CONSTANT_PROVENANCE_CROSSCHECK"].kind is ClaimKind.THEOREM
    assert claims["DEF_ASSOCIATION_AS_FREE_DYAD_QUOTIENT"].kind is ClaimKind.DEFINITION
    assert claims["THM_ASSOCIATION_QUOTIENT_CARDINALITY"].kind is ClaimKind.THEOREM
    assert claims["DEF_DISSOCIATION_AS_THREE_FIBRE_EXTENSION"].kind is ClaimKind.DEFINITION
    assert claims["THM_DISSOCIATION_FIBRE_CARDINALITY"].kind is ClaimKind.THEOREM
    assert claims["DEF_REPAIR_AS_SINGLETON_COPRODUCT"].kind is ClaimKind.DEFINITION
    assert claims["THM_SINGLETON_REPAIR_CARDINALITY"].kind is ClaimKind.THEOREM
    assert claims["THM_PARITY_FORCES_COLLATZ_BRANCH_SELECTION"].kind is ClaimKind.THEOREM
    assert claims["THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ"].kind is ClaimKind.THEOREM
    assert claims["GATE_BIND_RELATIONAL_CARDINALITY_NORMALIZATION_TO_PRIMITIVE_NATURAL_DYNAMICS"].kind is ClaimKind.DERIVATION_GATE

    gaussian_closure = dependency_closure("THM_GAUSSIAN_GENERATES_COLLATZ_COEFFICIENTS")
    assert "THM_HAMLET_IMAGINARY_GENERATOR" in gaussian_closure
    assert "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT" in gaussian_closure
    assert "THM_SOURCE_MINIMAL_AFFINE_PARITY_DYNAMICS_IS_COLLATZ" not in gaussian_closure
    assert "DEF_COLLATZ_ASSOCIATION_DISSOCIATION_CYCLE" not in gaussian_closure

    l_closure = dependency_closure("THM_GAUSSIAN_L3_24_CLOSURE_CROSSCHECK")
    assert "THM_GAUSSIAN_BOMBELLI_LADDER" in l_closure
    assert "BRIDGE_TIR_ROOT_EXTENSION_L3_FROM_GAUSSIAN_L45" in l_closure

    double_closure = dependency_closure("THM_COLLATZ_COEFFICIENT_PROVENANCE_DOUBLE_CLOSED")
    assert "THM_SOURCE_MINIMAL_AFFINE_PARITY_DYNAMICS_IS_COLLATZ" in double_closure
    assert "THM_GAUSSIAN_GENERATES_COLLATZ_COEFFICIENTS" in double_closure

    triple_closure = dependency_closure("THM_COLLATZ_COEFFICIENT_PROVENANCE_TRIPLE_CLOSED")
    assert "THM_COLLATZ_COEFFICIENT_PROVENANCE_DOUBLE_CLOSED" in triple_closure
    assert "THM_RELATION_OPERATOR_DIMENSION_COEFFICIENT_ROUTE" in triple_closure
    assert "THM_BINARY_UNIVERSAL_REPAIR_ONE" in triple_closure

    seed_closure = dependency_closure("THM_RELATIONAL_COLLATZ_L_CONSTANT_CERTIFICATE")
    assert "THM_ACTIVE_SEED_IS_THREE" in seed_closure
    assert "THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ" in seed_closure
    assert "BRIDGE_TIR_ROOT_EXTENSION_L3_FROM_GAUSSIAN_L45" not in seed_closure

    l_crosscheck = dependency_closure("THM_L_CONSTANT_PROVENANCE_CROSSCHECK")
    assert "THM_RELATIONAL_COLLATZ_L_CONSTANT_CERTIFICATE" in l_crosscheck
    assert "BRIDGE_TIR_ROOT_EXTENSION_L3_FROM_GAUSSIAN_L45" in l_crosscheck

def test_relational_cardinality_semantics_closes_collatz_operations_not_physical_binding() -> None:
    claims = claim_map()

    normalization = claims["THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ"]
    assert normalization.kind is ClaimKind.THEOREM

    closure = dependency_closure("THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ")
    assert "THM_ASSOCIATION_QUOTIENT_CARDINALITY" in closure
    assert "THM_ACTIVE_OPERATOR_PRODUCT_CARDINALITY" in closure
    assert "THM_IDENTITY_REPAIR_CARDINALITY" in closure
    assert "THM_DISSOCIATION_FIBRE_CARDINALITY" not in closure
    assert "THM_SINGLETON_REPAIR_CARDINALITY" not in closure
    assert "THM_COLLATZ_COEFFICIENT_PROVENANCE_TRIPLE_CLOSED" not in closure

    gate = claims["GATE_BIND_RELATIONAL_CARDINALITY_NORMALIZATION_TO_PRIMITIVE_NATURAL_DYNAMICS"]
    assert gate.kind is ClaimKind.DERIVATION_GATE
    gate_closure = dependency_closure("GATE_BIND_RELATIONAL_CARDINALITY_NORMALIZATION_TO_PRIMITIVE_NATURAL_DYNAMICS")
    assert "THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ" in gate_closure
    assert "A0" in gate_closure

def test_collatz_dyadic_phase_is_downstream_of_collatz_and_u1_embedding_is_separate() -> None:
    claims = claim_map()

    for claim_id in (
        "DEF_COLLATZ_PARITY_ITINERARY",
        "THM_COLLATZ_PARITY_FORBIDS_11",
        "DEF_COLLATZ_DYADIC_NORMALIZED_PHASE",
        "THM_COLLATZ_DYADIC_SHIFT_IS_DOUBLING",
        "THM_COLLATZ_TERMINAL_CYCLE_LENGTH_THREE",
        "THM_COLLATZ_TERMINAL_PHASE_DENOMINATOR_SEVEN",
        "THM_COLLATZ_TERMINAL_PHASE_ANCHORS",
        "THM_COLLATZ_PHASE_DENOMINATOR_EQUALS_L3",
        "THM_COLLATZ_ADMISSIBLE_WORD_COUNT_FIBONACCI",
    ):
        assert claims[claim_id].kind in {ClaimKind.DEFINITION, ClaimKind.THEOREM}

    assert claims["BRIDGE_COLLATZ_NORMALIZED_PHASE_TO_U1"].kind is ClaimKind.BRIDGE

    phase_closure = dependency_closure("THM_COLLATZ_DYADIC_SHIFT_IS_DOUBLING")
    assert "THM_RELATIONAL_CARDINALITY_NORMALIZATION_IS_COLLATZ" in phase_closure
    assert "THM_IMAGINARY_GENERATOR_U1" not in phase_closure
    assert "THM_HAMLET_OPERATOR_PROJECTIVE_CP1" not in phase_closure

    terminal_closure = dependency_closure("THM_COLLATZ_PHASE_DENOMINATOR_EQUALS_L3")
    assert "THM_COLLATZ_TERMINAL_PHASE_DENOMINATOR_SEVEN" in terminal_closure
    assert "THM_RELATIONAL_COLLATZ_L_CONSTANT_CERTIFICATE" in terminal_closure

    u1_bridge = dependency_closure("BRIDGE_COLLATZ_NORMALIZED_PHASE_TO_U1")
    assert "THM_COLLATZ_DYADIC_SHIFT_IS_DOUBLING" in u1_bridge
    assert "THM_IMAGINARY_GENERATOR_U1" in u1_bridge

    grammar = dependency_closure("THM_COLLATZ_ADMISSIBLE_WORD_COUNT_FIBONACCI")
    assert "THM_COLLATZ_PARITY_FORBIDS_11" in grammar



def test_tetrahedral_operator_binding_is_exact_but_downstream():
    claims = claim_map()

    assert claims["DEF_HAMLET_OPERATOR_BASIS_SIMPLEX"].kind is ClaimKind.DEFINITION
    assert claims["THM_HAMLET_OPERATOR_BASIS_REGULAR_TETRAHEDRON"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_OPERATOR_TETRAHEDRON_VOLUME"].kind is ClaimKind.THEOREM
    assert claims["THM_HAMLET_OPERATOR_TETRAHEDRON_STELLA_ISOMETRY"].kind is ClaimKind.THEOREM
    assert claims["THM_TETRAHEDRAL_ONE_PLUS_THREE_SPLIT"].kind is ClaimKind.THEOREM
    assert claims["THM_TETRAHEDRAL_COMPLETION_CARDINALITY_3N_PLUS_1"].kind is ClaimKind.THEOREM
    assert claims["THM_TETRAHEDRAL_GEOMETRY_MATCHES_COLLATZ_ODD_CARDINALITY"].kind is ClaimKind.THEOREM
    assert claims["THM_TETRAHEDRAL_BINDING_IS_DOWNSTREAM_NOT_UPSTREAM_CLOSURE"].kind is ClaimKind.THEOREM

    tetra_closure = dependency_closure("THM_HAMLET_OPERATOR_BASIS_REGULAR_TETRAHEDRON")
    assert "THM_HAMLET_OPERATOR_FROBENIUS_NORM" in tetra_closure
    assert "THM_RELATION_ORIENTATION_TWO_ROLE_ORBIT" in tetra_closure

    odd_closure = dependency_closure("THM_TETRAHEDRAL_GEOMETRY_MATCHES_COLLATZ_ODD_CARDINALITY")
    assert "THM_ACTIVE_OPERATOR_PRODUCT_CARDINALITY" in odd_closure
    assert "THM_IDENTITY_REPAIR_CARDINALITY" in odd_closure
    assert "THM_RELATION_ALGEBRA_DETERMINISTICALLY_GENERATES_COLLATZ_MAP" in odd_closure

    scope = claims["THM_TETRAHEDRAL_BINDING_IS_DOWNSTREAM_NOT_UPSTREAM_CLOSURE"].statement
    assert "cannot be used non-circularly" in scope
    assert "remains open" in scope
