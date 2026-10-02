#!/usr/bin/env python3
"""Static/local repository audit for RTOFA.

Uses only the Python standard library and the checked-out repository.
No network and no GitHub Actions are required.
"""

from __future__ import annotations

import ast
import importlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = ROOT / "tests"
MONOGRAPH = ROOT / "monograph" / "main.tex"

AUDITED_DOCS = (
    ROOT / "docs" / "ALGEBRAIC_GEOMETRIC_CELL_MAP.md",
    ROOT / "README.md",
    ROOT / "docs" / "ARCHITECTURE.md",
    ROOT / "docs" / "AXIOM_AUDIT.md",
    ROOT / "docs" / "AXIOM_CLOSURE_AUDIT.md",
    ROOT / "docs" / "CANONICAL_REDUCTION_GATE.md",
    ROOT / "docs" / "REFERENCE_CORPUS_SCAN.md",
    ROOT / "docs" / "BRIDGE_GAP_TRIAGE.md",
    ROOT / "docs" / "CARRIER_OCCURRENCE_SEPARATION.md",
    ROOT / "docs" / "COHERENCE_MATRIX.md",
    ROOT / "docs" / "FOUNDATIONAL_NONVACUITY_GATE.md",
    ROOT / "docs" / "INDEPENDENCE_WITNESSES.md",
    ROOT / "docs" / "INDEXED_TENSOR_GATE.md",
    ROOT / "docs" / "MONOIDAL_COHERENCE_GATE.md",
    ROOT / "docs" / "RELATIONAL_ADMISSIBILITY_REDUCTION_GATE.md",
    ROOT / "docs" / "RELATIONAL_DISTINCTION_BINDING_GATE.md",
    ROOT / "docs" / "RELATIONAL_POTENTIAL.md",
    ROOT / "docs" / "SEMANTIC_WEIGHTING_GATE.md",
    ROOT / "docs" / "VALIDATION_STATUS.md",
)


class AuditFailure(RuntimeError):
    pass


def parse_python_tree(path: Path) -> ast.AST:
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        raise AuditFailure(f"python syntax error in {path}: {exc}") from exc


def public_defs(path: Path) -> set[str]:
    tree = parse_python_tree(path)
    out: set[str] = set()
    for node in tree.body:  # type: ignore[attr-defined]
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                out.add(node.name)
    return out


def test_inventory() -> dict[str, int]:
    inventory: dict[str, int] = {}
    for path in sorted(TESTS.glob("test_*.py")):
        tree = parse_python_tree(path)
        count = sum(
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
            for node in tree.body  # type: ignore[attr-defined]
        )
        inventory[str(path.relative_to(ROOT))] = int(count)
    return inventory


def package_exports() -> set[str]:
    path = SRC / "rdss" / "__init__.py"
    tree = parse_python_tree(path)
    names: list[str] | None = None
    for node in tree.body:  # type: ignore[attr-defined]
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            continue
        if not isinstance(node.value, (ast.List, ast.Tuple)):
            raise AuditFailure("__all__ must be a literal list/tuple")
        names = []
        for elt in node.value.elts:
            if not isinstance(elt, ast.Constant) or not isinstance(elt.value, str):
                raise AuditFailure("__all__ entries must be literal strings")
            names.append(elt.value)
    if names is None:
        raise AuditFailure("package __all__ not found")
    if len(names) != len(set(names)):
        raise AuditFailure("duplicate package __all__ entries")
    return set(names)


def audit_layer_ownership() -> dict[str, int]:
    module_paths = {
        "algebraic_geometry_cell": SRC / "rdss" / "algebraic_geometry_cell.py",
        "core": SRC / "rdss" / "algebra.py",
        "canonical": SRC / "rdss" / "canonical.py",
        "certificate_scan": SRC / "rdss" / "certificate_scan.py",
        "corpus": SRC / "rdss" / "corpus.py",
        "cp1_projective": SRC / "rdss" / "cp1_projective.py",
        "contextual_bridges": SRC / "rdss" / "contextual_bridges.py",
        "confluence": SRC / "rdss" / "confluence.py",
        "bridges": SRC / "rdss" / "bridges.py",
        "equivalence_graph": SRC / "rdss" / "equivalence_graph.py",
        "factorization": SRC / "rdss" / "factorization.py",
        "loss_witness": SRC / "rdss" / "loss_witness.py",
        "normal_form": SRC / "rdss" / "normal_form.py",
        "signature": SRC / "rdss" / "signature.py",
        "rewrite": SRC / "rdss" / "rewrite.py",
        "triage": SRC / "rdss" / "triage.py",
        "operations": SRC / "rdss" / "operations.py",
        "phase": SRC / "rdss" / "phase.py",
        "potential": SRC / "rdss" / "potential.py",
        "provenance": SRC / "rdss" / "provenance.py",
        "realizations": SRC / "rdss" / "realizations.py",
        "reduction_certificate": SRC / "rdss" / "reduction_certificate.py",
        "zero_axis": SRC / "rdss" / "zero_axis.py",
    }
    defs = {name: public_defs(path) for name, path in module_paths.items()}

    forbidden_core = {
        "CP1State",
        "MinimalDistinction",
        "MoireRotation",
        "ZeroAxisPoint",
        "finite_zero_axis_lift",
        "wrap_phase",
        "winding_and_residual",
        "closed_path_winding",
        "RelationalPotentialProfile",
        "semantic_potential_shift",
        "relational_attractor_set",
    }
    leaks = sorted(defs["core"] & forbidden_core)
    if leaks:
        raise AuditFailure(f"representation/diagnostic leak into algebra core: {leaks}")

    exported = package_exports()
    expected = set().union(*defs.values())
    missing = sorted(expected - exported)
    if missing:
        raise AuditFailure(f"public layer definitions missing from package exports: {missing}")

    return {name: len(values) for name, values in defs.items()} | {
        "package_exports": len(exported)
    }


def audit_claim_graph() -> dict[str, int]:
    sys.path.insert(0, str(SRC))
    try:
        axioms = importlib.import_module("rdss.axioms")
        axioms.validate_dependency_dag()
        claims = axioms.CLAIMS
        ids = [claim.id for claim in claims]
        if len(ids) != len(set(ids)):
            raise AuditFailure("duplicate claim ids")
        return {"claims": len(ids)}
    finally:
        try:
            sys.path.remove(str(SRC))
        except ValueError:
            pass


def audit_test_imports() -> None:
    module_defs = {
        "rdss.algebraic_geometry_cell": public_defs(SRC / "rdss" / "algebraic_geometry_cell.py") | {
            "CUBE_FACE_COUNT",
            "CUBE_VERTEX_COUNT",
            "CUBE_VERTICES",
            "OCTAHEDRAL_CORE_VERTEX_COUNT",
            "OCTAHEDRAL_CORE_VERTICES",
            "SPIN_HALF",
            "SPINOR_FULL_RETURN",
            "SPINOR_SIGN_RETURN",
            "TETRAHEDRON_NEGATIVE_VERTICES",
            "TETRAHEDRON_POSITIVE_VERTICES",
        },
        "rdss.algebra": public_defs(SRC / "rdss" / "algebra.py"),
        "rdss.axioms": public_defs(SRC / "rdss" / "axioms.py") | {
            "CANONICAL_PROVENANCE",
            "CLAIMS",
        },
        "rdss.canonical": public_defs(SRC / "rdss" / "canonical.py"),
        "rdss.certificate_scan": public_defs(SRC / "rdss" / "certificate_scan.py"),
        "rdss.corpus": public_defs(SRC / "rdss" / "corpus.py"),
        "rdss.cp1_projective": public_defs(SRC / "rdss" / "cp1_projective.py"),
        "rdss.contextual_bridges": public_defs(SRC / "rdss" / "contextual_bridges.py"),
        "rdss.confluence": public_defs(SRC / "rdss" / "confluence.py"),
        "rdss.bridges": public_defs(SRC / "rdss" / "bridges.py"),
        "rdss.equivalence_graph": public_defs(SRC / "rdss" / "equivalence_graph.py"),
        "rdss.factorization": public_defs(SRC / "rdss" / "factorization.py"),
        "rdss.loss_witness": public_defs(SRC / "rdss" / "loss_witness.py"),
        "rdss.normal_form": public_defs(SRC / "rdss" / "normal_form.py"),
        "rdss.closure": public_defs(SRC / "rdss" / "closure.py"),
        "rdss.operations": public_defs(SRC / "rdss" / "operations.py"),
        "rdss.phase": public_defs(SRC / "rdss" / "phase.py"),
        "rdss.potential": public_defs(SRC / "rdss" / "potential.py"),
        "rdss.provenance": public_defs(SRC / "rdss" / "provenance.py"),
        "rdss.realizations": public_defs(SRC / "rdss" / "realizations.py"),
        "rdss.reduction_certificate": public_defs(SRC / "rdss" / "reduction_certificate.py"),
        "rdss.signature": public_defs(SRC / "rdss" / "signature.py"),
        "rdss.rewrite": public_defs(SRC / "rdss" / "rewrite.py"),
        "rdss.triage": public_defs(SRC / "rdss" / "triage.py"),
        "rdss.witnesses": public_defs(SRC / "rdss" / "witnesses.py"),
        "rdss.zero_axis": public_defs(SRC / "rdss" / "zero_axis.py"),
        "rdss": package_exports(),
    }
    errors: list[str] = []
    for path in sorted(TESTS.glob("test_*.py")):
        tree = parse_python_tree(path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or node.module not in module_defs:
                continue
            available = module_defs[node.module]
            for alias in node.names:
                if alias.name == "*":
                    continue
                if alias.name not in available:
                    errors.append(
                        f"{path.relative_to(ROOT)} imports undefined "
                        f"{node.module}.{alias.name}"
                    )
    if errors:
        raise AuditFailure("; ".join(errors))


def audit_markdown() -> None:
    for path in AUDITED_DOCS:
        if not path.exists():
            raise AuditFailure(f"audited document missing: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        for ch in text:
            code = ord(ch)
            if code < 32 and ch not in "\n\r\t":
                raise AuditFailure(
                    f"control character U+{code:04X} in {path.relative_to(ROOT)}"
                )
        for lineno, line in enumerate(text.splitlines(), start=1):
            if line.strip() in {"[", "]"}:
                raise AuditFailure(
                    f"bare math delimiter in {path.relative_to(ROOT)}:{lineno}"
                )


def strip_tex_comments(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        chars: list[str] = []
        backslashes = 0
        for ch in line:
            if ch == "%" and backslashes % 2 == 0:
                break
            chars.append(ch)
            if ch == "\\":
                backslashes += 1
            else:
                backslashes = 0
        out.append("".join(chars))
    return "\n".join(out)


def audit_monograph() -> dict[str, int]:
    text = MONOGRAPH.read_text(encoding="utf-8")
    clean = strip_tex_comments(text)

    stack: list[str] = []
    for match in re.finditer(r"\\(begin|end)\{([^}]+)\}", clean):
        kind, name = match.groups()
        if kind == "begin":
            stack.append(name)
        else:
            if not stack:
                raise AuditFailure(f"unmatched \\end{{{name}}}")
            expected = stack.pop()
            if expected != name:
                raise AuditFailure(
                    f"environment mismatch: expected {expected}, found {name}"
                )
    if stack:
        raise AuditFailure(f"unclosed LaTeX environments: {stack}")

    balance = 0
    escaped = False
    for ch in clean:
        if ch == "\\":
            escaped = not escaped
            continue
        if ch == "{" and not escaped:
            balance += 1
        elif ch == "}" and not escaped:
            balance -= 1
            if balance < 0:
                raise AuditFailure("LaTeX brace balance went negative")
        escaped = False
    if balance != 0:
        raise AuditFailure(f"LaTeX brace balance is {balance}")

    display_open = len(re.findall(r"(?<!\\)\\\[", clean))
    display_close = len(re.findall(r"(?<!\\)\\\]", clean))
    if display_open != display_close:
        raise AuditFailure(
            f"display math mismatch: open={display_open}, close={display_close}"
        )

    return {
        "monograph_lines": len(text.splitlines()),
        "display_math_pairs": display_open,
    }


def main() -> int:
    try:
        layers = audit_layer_ownership()
        claims = audit_claim_graph()
        audit_test_imports()
        inventory = test_inventory()
        audit_markdown()
        tex = audit_monograph()
    except AuditFailure as exc:
        print(f"STATIC AUDIT FAIL: {exc}", file=sys.stderr)
        return 1

    report = {
        "status": "PASS",
        "layers": layers,
        "claims": claims,
        "tests": {
            "files": inventory,
            "total": sum(inventory.values()),
        },
        "monograph": tex,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
