from rdss.axioms import (
    ClaimKind,
    claim_map,
    dependency_closure,
    foundational_axioms,
    validate_dependency_dag,
)


def test_dependency_graph_is_acyclic_and_resolved():
    validate_dependency_dag()


def test_binary_relation_is_explicit_signature_definition():
    claims = claim_map()
    assert claims["DEF_BINARY_REL"].kind is ClaimKind.DEFINITION
    assert claims["DEF_BINARY_REL"].depends_on == ()


def test_cp1_is_not_mislabeled_as_foundational_axiom():
    claims = claim_map()
    assert claims["REF_CP1"].kind is ClaimKind.REFERENCE_REALIZATION
    assert set(claims["REF_CP1"].depends_on) == {"DEF_POINT", "DEF_BINARY_REL"}


def test_recursive_refinement_is_independent_foundational_axiom():
    claims = claim_map()
    assert claims["RR1"].kind is ClaimKind.AXIOM
    assert "RA0" not in dependency_closure("RR1")
    assert set(claims["RR1"].depends_on) == {"DEF_POINT", "DEF_BINARY_REL"}


def test_structural_primitives_do_not_silently_depend_on_ra0():
    claims = claim_map()
    for claim_id in ("PRIM_MODULE", "PRIM_PRODUCT", "PRIM_SCALE", "PRIM_TRANSPORT", "PRIM_ORBIT"):
        assert claims[claim_id].kind is ClaimKind.STRUCTURAL_PRIMITIVE
        assert "RA0" not in dependency_closure(claim_id)


def test_moire_is_derived_from_orbital_primitive():
    claims = claim_map()
    assert claims["DER_MOIRE"].kind is ClaimKind.DERIVED
    assert dependency_closure("DER_MOIRE") == frozenset({"PRIM_ORBIT"})


def test_refinement_residual_depends_on_refinement_and_product():
    assert dependency_closure("DEF_REFINEMENT_RESIDUAL") == frozenset(
        {"RR1", "DEF_POINT", "DEF_BINARY_REL", "PRIM_PRODUCT", "PRIM_MODULE"}
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


def test_winding_is_zero_axis_phase_representation_of_holonomy():
    claims = claim_map()
    assert claims["DER_WINDING"].kind is ClaimKind.DERIVED
    assert dependency_closure("DER_WINDING") == frozenset(
        {
            "ZA_BRIDGE",
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
    assert set(claims["RA0_STAR"].depends_on) == {"DEF_POINT", "DEF_BINARY_REL"}
    assert claims["THM_RR1_FROM_RA0_STAR"].kind is ClaimKind.THEOREM
    assert dependency_closure("THM_RR1_FROM_RA0_STAR") == frozenset(
        {"RA0_STAR", "DEF_POINT", "DEF_BINARY_REL"}
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
