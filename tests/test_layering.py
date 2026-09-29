import rdss
import rdss.algebra as core
import rdss.phase as phase
import rdss.potential as potential
import rdss.realizations as realizations
import rdss.zero_axis as zero_axis


def test_algebra_core_is_representation_free():
    forbidden = (
        "CP1State",
        "MinimalDistinction",
        "MoireRotation",
        "ZeroAxisPoint",
        "wrap_phase",
        "winding_and_residual",
        "closed_path_winding",
        "finite_zero_axis_lift",
        "RelationalPotentialProfile",
        "relational_attractor_set",
        "semantic_potential_shift",
    )
    for name in forbidden:
        assert not hasattr(core, name)


def test_representation_ownership_is_explicit():
    assert hasattr(realizations, "CP1State")
    assert hasattr(realizations, "MinimalDistinction")
    assert hasattr(realizations, "MoireRotation")
    assert hasattr(phase, "wrap_phase")
    assert hasattr(phase, "winding_and_residual")
    assert hasattr(phase, "closed_path_winding")
    assert hasattr(zero_axis, "ZeroAxisPoint")
    assert hasattr(zero_axis, "finite_zero_axis_lift")
    assert hasattr(potential, "RelationalPotentialProfile")
    assert hasattr(potential, "relational_attractor_set")
    assert hasattr(potential, "semantic_potential_shift")


def test_public_api_reexports_without_changing_layer_ownership():
    assert rdss.CP1State is realizations.CP1State
    assert rdss.MinimalDistinction is realizations.MinimalDistinction
    assert rdss.MoireRotation is realizations.MoireRotation
    assert rdss.wrap_phase is phase.wrap_phase
    assert rdss.winding_and_residual is phase.winding_and_residual
    assert rdss.closed_path_winding is phase.closed_path_winding
    assert rdss.ZeroAxisPoint is zero_axis.ZeroAxisPoint
    assert rdss.finite_zero_axis_lift is zero_axis.finite_zero_axis_lift
    assert rdss.RelationalPotentialProfile is potential.RelationalPotentialProfile
    assert rdss.relational_attractor_set is potential.relational_attractor_set
    assert rdss.semantic_potential_shift is potential.semantic_potential_shift
