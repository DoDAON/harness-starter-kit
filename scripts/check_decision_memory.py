#!/usr/bin/env python3
"""Warn when implementation diffs may need decision-memory review."""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
from pathlib import Path


DEFAULT_RULES = {
    "watched_paths": [
        "src/**",
        "app/**",
        "lib/**",
        "components/**",
        "pages/**",
    ],
    "decision_paths": [
        "docs/decisions/**",
    ],
    "ignored_paths": [
        "**/*.test.*",
        "**/*.spec.*",
        "**/__snapshots__/**",
        "docs/**",
        "scripts/**",
        "templates/**",
    ],
}

TRIGGER_QUESTION = (
    "Does this change user workflow, input contract, input semantics, state "
    "normalization, API request or response shape, fallback policy, or displayed "
    "decision criteria?"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Warn when watched implementation paths changed without a matching "
            "decision-record diff."
        )
    )
    parser.add_argument(
        "--base",
        help=(
            "Git revision to compare against. Defaults to HEAD for local "
            "working-tree checks. Pass a PR base SHA in CI."
        ),
    )
    parser.add_argument(
        "--rules",
        default=".harness/decision-memory-rules.json",
        help="Path to the decision-memory rules JSON file.",
    )
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Exit nonzero when decision-memory review is needed.",
    )
    return parser.parse_args()


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )


def is_git_repository(root: Path) -> bool:
    result = run_git(root, "rev-parse", "--is-inside-work-tree")
    return result.returncode == 0 and result.stdout.strip() == "true"


def normalize_path(value: str) -> str:
    return value.strip().replace("\\", "/")


def load_rules(root: Path, rules_path: Path) -> dict[str, list[str]]:
    path = rules_path if rules_path.is_absolute() else root / rules_path
    if not path.exists():
        return DEFAULT_RULES
    data = json.loads(path.read_text(encoding="utf-8"))
    rules: dict[str, list[str]] = {}
    for key, default in DEFAULT_RULES.items():
        value = data.get(key, default)
        rules[key] = [str(item) for item in value] if isinstance(value, list) else default
    return rules


def matches_any(path: str, patterns: list[str]) -> bool:
    normalized = normalize_path(path)
    return any(fnmatch.fnmatchcase(normalized, pattern) for pattern in patterns)


def changed_paths(root: Path, base: str, explicit_base: bool) -> tuple[list[str], str | None]:
    diff = run_git(
        root,
        "diff",
        "--name-only",
        "--diff-filter=ACDMRTUXB",
        base,
        "--",
    )
    paths: set[str] = set()
    if diff.returncode == 0:
        paths.update(
            normalize_path(line) for line in diff.stdout.splitlines() if line.strip()
        )
    elif explicit_base:
        message = diff.stderr.strip() or diff.stdout.strip() or f"invalid base: {base}"
        return [], f"Decision memory check failed: could not diff against {base}: {message}"

    status = run_git(root, "status", "--porcelain")
    if status.returncode == 0:
        for line in status.stdout.splitlines():
            if line.startswith("?? "):
                status_path = root / line[3:]
                if status_path.is_dir():
                    paths.update(
                        normalize_path(str(path.relative_to(root)))
                        for path in status_path.rglob("*")
                        if path.is_file()
                    )
                else:
                    paths.add(normalize_path(line[3:]))

    return sorted(paths), None


def check_decision_memory(
    root: Path,
    base: str,
    explicit_base: bool,
    rules_path: Path,
    fail_on_warning: bool,
) -> int:
    if not is_git_repository(root):
        print("Decision memory check skipped: not inside a Git repository.")
        return 0

    rules = load_rules(root, rules_path)
    paths, error = changed_paths(root, base, explicit_base)
    if error:
        print(error)
        print("Fetch the base revision or pass a valid --base value.")
        return 2

    watched_paths = [
        path
        for path in paths
        if matches_any(path, rules["watched_paths"])
        and not matches_any(path, rules["ignored_paths"])
    ]
    decision_paths = [
        path for path in paths if matches_any(path, rules["decision_paths"])
    ]

    if not watched_paths or decision_paths:
        return 0

    print(
        "Decision memory review warning: watched implementation paths changed "
        "without a docs/decisions change."
    )
    print(f"Question: {TRIGGER_QUESTION}")
    print("Changed watched paths:")
    for path in watched_paths[:10]:
        print(f"- {path}")
    if len(watched_paths) > 10:
        print(f"- ... {len(watched_paths) - 10} more")
    print()
    print("Before the final report, do one of the following:")
    print("- add or update a decision record")
    print("- cite the existing ADR that covers the change")
    print("- explain why no decision memory is needed")

    return 1 if fail_on_warning else 0


def main() -> int:
    args = parse_args()
    base = args.base or "HEAD"
    return check_decision_memory(
        Path.cwd(),
        base,
        args.base is not None,
        Path(args.rules),
        args.fail_on_warning,
    )


if __name__ == "__main__":
    raise SystemExit(main())
