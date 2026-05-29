#!/usr/bin/env python3
"""Run local harness checks for an Android or Kotlin Gradle project."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ANDROID_MARKERS = (
    "settings.gradle",
    "settings.gradle.kts",
    "build.gradle",
    "build.gradle.kts",
)


def repo_root() -> Path:
    current = Path(__file__).resolve()
    if current.parent.name == "scripts":
        return current.parents[1]

    cwd = Path.cwd()
    if (cwd / "scripts" / "check_docs_drift.py").exists():
        return cwd

    return cwd


ROOT = repo_root()


def existing_path(root: Path, *names: str) -> Path | None:
    for name in names:
        path = root / name
        if path.exists():
            return path
    return None


def looks_like_android_project(path: Path) -> bool:
    if not any((path / marker).exists() for marker in ANDROID_MARKERS):
        return False
    return (
        (path / "gradlew").exists()
        or (path / "gradlew.bat").exists()
        or (path / "app" / "build.gradle").exists()
        or (path / "app" / "build.gradle.kts").exists()
        or "com.android.application" in read_text(path / "build.gradle")
        or "com.android.application" in read_text(path / "build.gradle.kts")
    )


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def detect_project_dir(explicit: str | None) -> Path:
    if explicit:
        project_dir = (ROOT / explicit).resolve()
        if not project_dir.exists() or not project_dir.is_dir():
            raise SystemExit(f"Android project directory was not found: {project_dir}")
        return project_dir

    if looks_like_android_project(ROOT):
        return ROOT

    candidates = [
        path
        for path in sorted(ROOT.rglob("*"))
        if path.is_dir()
        and ".git" not in path.parts
        and "harness-starter-kit" not in path.parts
        and looks_like_android_project(path)
    ]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise SystemExit("Could not detect an Android Gradle project.")

    relative = ", ".join(str(path.relative_to(ROOT)) for path in candidates[:5])
    raise SystemExit(
        "Multiple Android-like Gradle projects were found. "
        f"Pass --project-dir. Candidates: {relative}"
    )


def gradle_command(project_dir: Path) -> list[str]:
    wrapper = existing_path(
        project_dir,
        "gradlew.bat" if os.name == "nt" else "gradlew",
        "gradlew.bat",
        "gradlew",
    )
    if wrapper:
        return [str(wrapper)]

    executable = shutil.which("gradle")
    if executable:
        return [executable]
    raise SystemExit("Gradle wrapper or gradle executable was not found.")


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def run_python_check(script: str) -> None:
    path = ROOT / "scripts" / script
    if path.exists():
        run([sys.executable, str(path)], ROOT)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Android harness checks.")
    parser.add_argument(
        "--project-dir",
        help="Android Gradle project directory relative to the repository root.",
    )
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--skip-assemble", action="store_true")
    parser.add_argument(
        "--skip-encoding",
        action="store_true",
        help="Skip optional encoding/mojibake hygiene check.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_dir = detect_project_dir(args.project_dir)
    gradle = gradle_command(project_dir)

    if not args.skip_tests:
        run([*gradle, "test"], project_dir)
    if not args.skip_assemble:
        run([*gradle, "assembleDebug"], project_dir)

    run_python_check("check_docs_drift.py")
    run_python_check("check_structure.py")
    if not args.skip_encoding:
        run_python_check("check_encoding_hygiene.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
