from rdss.axioms import (
    ClaimKind,
    claim_map,
    dependency_closure,
    foundational_axioms,
    formation_rules,
    validate_dependency_dag,
)


def test_dependency_graph_is_acyclic_and_resolved():
    validate_dependency_dag()


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
    assert set(claims["REF_CP1"].depends_on) == {"DEF_POINT", "DEF_BINARY_DISTINCTION"}



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

def test_recursive_refinement_is_independent_foundational_axiom():
    claims = claim_map()
    assert claims["RR1"].kind is ClaimKind.AXIOM
    assert "RA0" not in dependency_closure("RR1")
    assert set(claims["RR1"].depends_on) == {"DEF_POINT", "DEF_BINARY_DISTINCTION"}


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


def test_foundational_axiom_set_is_small_and_explicit():
    ids = {claim.id for claim in foundational_axioms()}
    assert ids == {"RA0", "RR1"}



def test_ra0_star_is_candidate_not_silent_replacement():
    claims = claim_map()

    assert claims["RA0_STAR"].kind is ClaimKind.CANDIDATE_AXIOM
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

    assert claims["RA0_REL_STAR"].kind is ClaimKind.CANDIDATE_AXIOM
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


def test_singleton_foundation_minimality_splits_lower_bound_and_attainability():
    claims = claim_map()

    assert claims["THM_META0_CARDINALITY_LOWER_BOUND"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_META0_CARDINALITY_LOWER_BOUND") == frozenset(
        {"META0"}
    )

    assert claims["REF_SINGLETON_RA0_REL_STAR_MODEL"].kind is ClaimKind.REFERENCE_REALIZATION
    witness_closure = dependency_closure("REF_SINGLETON_RA0_REL_STAR_MODEL")
    assert witness_closure == frozenset(
        {
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

def test_current_canonical_axioms_remain_ra0_and_rr1_until_promotion():
    ids = {claim.id for claim in foundational_axioms()}
    assert ids == {"RA0", "RR1"}



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
            "REF_CP1",
            "RR1",
            "DEF_POINT",
            "DEF_BINARY_DISTINCTION",
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
    assert claims["META0"].depends_on == ()
    assert tuple(claim.id for claim in formation_rules()) == ("META0",)


def test_ex0_is_theorem_of_model_formation_not_extra_object_axiom():
    claims = claim_map()
    assert claims["EX0"].kind is ClaimKind.THEOREM
    assert dependency_closure("EX0") == frozenset({"META0"})
    assert "EX0" not in {claim.id for claim in foundational_axioms()}




def test_ra0_rr1_do_not_imply_ra0_rel_star():
    claims = claim_map()

    assert claims["REF_RA0_RR1_UNBOUND_MODEL"].kind is ClaimKind.REFERENCE_REALIZATION
    assert dependency_closure("REF_RA0_RR1_UNBOUND_MODEL") == frozenset(
        {
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
            "RR1",
            "DEF_POINT",
            "DEF_BINARY_DISTINCTION",
            "DEF_OCCURRENCE_ADDRESS_SPACE",
        }
    )

    assert claims["THM_FINITE_WORD_OCCURRENCE_COUNTABILITY"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_FINITE_WORD_OCCURRENCE_COUNTABILITY") == frozenset(
        {
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
