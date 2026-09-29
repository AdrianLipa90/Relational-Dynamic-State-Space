#!/usr/bin/env python3
"""Local RTOFA validation runner.

No network access and no GitHub Actions are required.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MONOGRAPH = ROOT / "monograph"
MAIN_TEX = MONOGRAPH / "main.tex"


def run(command: list[str], *, cwd: Path = ROOT) -> int:
    print("+", " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=cwd, check=False)
    return int(completed.returncode)


def validate_tests() -> int:
    return run([sys.executable, "-m", "pytest", "-q"])


def validate_latex(*, require_latex: bool) -> int:
    latexmk = shutil.which("latexmk")
    if latexmk:
        return run(
            [
                latexmk,
                "-pdf",
                "-interaction=nonstopmode",
                "-halt-on-error",
                MAIN_TEX.name,
            ],
            cwd=MONOGRAPH,
        )

    pdflatex = shutil.which("pdflatex")
    if pdflatex:
        command = [
            pdflatex,
            "-interaction=nonstopmode",
            "-halt-on-error",
            MAIN_TEX.name,
        ]
        first = run(command, cwd=MONOGRAPH)
        if first != 0:
            return first
        return run(command, cwd=MONOGRAPH)

    message = "LATEX SKIP: neither latexmk nor pdflatex is installed"
    if require_latex:
        print(message + " (required)", file=sys.stderr)
        return 2
    print(message)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tests-only",
        action="store_true",
        help="run pytest only",
    )
    parser.add_argument(
        "--latex-only",
        action="store_true",
        help="compile monograph only",
    )
    parser.add_argument(
        "--require-latex",
        action="store_true",
        help="fail if no LaTeX compiler is available",
    )
    args = parser.parse_args()

    if args.tests_only and args.latex_only:
        parser.error("--tests-only and --latex-only are mutually exclusive")

    if not args.latex_only:
        code = validate_tests()
        if code != 0:
            print(f"PYTEST FAIL: exit={code}", file=sys.stderr)
            return code
        print("PYTEST PASS")

    if not args.tests_only:
        code = validate_latex(require_latex=args.require_latex)
        if code != 0:
            print(f"LATEX FAIL: exit={code}", file=sys.stderr)
            return code
        print("LATEX PASS/SKIP according to availability policy")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
