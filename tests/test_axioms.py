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


def test_binary_distinction_is_occurrence_level_not_label_inequality():
    claims = claim_map()
    assert claims["DEF_BINARY_DISTINCTION"].kind is ClaimKind.DEFINITION
    assert claims["DEF_BINARY_DISTINCTION"].depends_on == ("DEF_POINT",)


def test_relation_occurrence_and_occurrence_path_are_explicit_definitions():
    claims = claim_map()

    assert claims["DEF_RELATION_OCCURRENCE"].kind is ClaimKind.DEFINITION
    assert set(claims["DEF_RELATION_OCCURRENCE"].depends_on) == {
        "DEF_POINT",
        "DEF_BINARY_REL",
    }

    assert claims["DEF_OCCURRENCE_PATH"].kind is ClaimKind.DEFINITION
    assert claims["DEF_OCCURRENCE_PATH"].depends_on == (
        "DEF_RELATION_OCCURRENCE",
    )

    assert dependency_closure("DEF_OCCURRENCE_PATH") == frozenset(
        {
            "DEF_RELATION_OCCURRENCE",
            "DEF_POINT",
            "DEF_BINARY_REL",
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
        {"RA0_STAR", "DEF_POINT", "DEF_BINARY_DISTINCTION"}
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
            "PRIM_TRANSPORT",
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
        {"REF_CP1", "RR1", "DEF_POINT", "DEF_BINARY_DISTINCTION"}
    )



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
        }
    )
