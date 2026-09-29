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
    for claim_id in ("PRIM_PRODUCT", "PRIM_SCALE", "PRIM_ORBIT"):
        assert claims[claim_id].kind is ClaimKind.STRUCTURAL_PRIMITIVE
        assert "RA0" not in dependency_closure(claim_id)


def test_moire_is_derived_from_orbital_primitive():
    claims = claim_map()
    assert claims["DER_MOIRE"].kind is ClaimKind.DERIVED
    assert dependency_closure("DER_MOIRE") == frozenset({"PRIM_ORBIT"})


def test_refinement_residual_depends_on_refinement_and_product():
    assert dependency_closure("DEF_REFINEMENT_RESIDUAL") == frozenset(
        {"RR1", "DEF_POINT", "DEF_BINARY_REL", "PRIM_PRODUCT"}
    )


def test_zero_axis_is_a_bridge_not_an_axiom_of_general_algebra():
    claims = claim_map()
    assert claims["ZA_BRIDGE"].kind is ClaimKind.BRIDGE
    assert claims["ZA_BRIDGE"].depends_on == ()


def test_winding_depends_on_zero_axis_bridge_but_is_not_primitive_state():
    claims = claim_map()
    assert claims["DER_WINDING"].kind is ClaimKind.DERIVED
    assert dependency_closure("DER_WINDING") == frozenset({"ZA_BRIDGE"})


def test_foundational_axiom_set_is_small_and_explicit():
    ids = {claim.id for claim in foundational_axioms()}
    assert ids == {"RA0", "RR1"}
