#!/usr/bin/env python3
"""Run local harness checks for a JavaScript or TypeScript project."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def repo_root() -> Path:
    current = Path(__file__).resolve()
    if current.parent.name == "scripts":
        return current.parents[1]

    cwd = Path.cwd()
    if (cwd / "package.json").exists():
        return cwd

    for candidate in (current.parent, *current.parents):
        if (candidate / "package.json").exists():
            return candidate
    return cwd


ROOT = repo_root()


def load_scripts() -> dict[str, str]:
    package_json = ROOT / "package.json"
    if not package_json.exists():
        raise SystemExit(f"package.json was not found under {ROOT}")

    data: dict[str, Any] = json.loads(package_json.read_text(encoding="utf-8"))
    scripts = data.get("scripts", {})
    if not isinstance(scripts, dict):
        return {}
    return {str(name): str(command) for name, command in scripts.items()}


def package_manager(name: str) -> str:
    if name != "auto":
        executable = shutil.which(name)
        if executable:
            return executable
        raise SystemExit(f"{name} executable was not found.")

    candidates = (
        ("pnpm-lock.yaml", "pnpm"),
        ("yarn.lock", "yarn"),
        ("package-lock.json", "npm"),
    )
    for lockfile, executable_name in candidates:
        executable = shutil.which(executable_name)
        if (ROOT / lockfile).exists() and executable:
            return executable

    executable = shutil.which("npm")
    if executable:
        return executable
    raise SystemExit("No npm, pnpm, or yarn executable was found.")


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def run_script(manager: str, script: str) -> None:
    run([manager, "run", script])


def run_python_check(script: str) -> None:
    path = ROOT / "scripts" / script
    if path.exists():
        run([sys.executable, str(path)])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run frontend harness checks.")
    parser.add_argument(
        "--package-manager",
        choices=("auto", "npm", "pnpm", "yarn"),
        default="auto",
        help="Package manager to run. Defaults to lockfile-based detection.",
    )
    parser.add_argument("--skip-lint", action="store_true")
    parser.add_argument("--skip-typecheck", action="store_true")
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--skip-build", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    scripts = load_scripts()
    manager = package_manager(args.package_manager)

    script_plan = (
        ("lint", args.skip_lint),
        ("typecheck", args.skip_typecheck),
        ("test", args.skip_tests),
        ("build", args.skip_build),
    )
    for script, should_skip in script_plan:
        if not should_skip and script in scripts:
            run_script(manager, script)

    run_python_check("check_docs_drift.py")
    run_python_check("check_structure.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
