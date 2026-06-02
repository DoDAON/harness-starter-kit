from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_decision_memory.py"


class CheckDecisionMemoryTests(unittest.TestCase):
    def run_checker(
        self, root: Path, *args: str
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), *args],
            cwd=root,
            capture_output=True,
            text=True,
        )

    def run_git(self, root: Path, *args: str) -> None:
        subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )

    def git_output(self, root: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def init_repo(self, root: Path) -> None:
        self.run_git(root, "init")
        self.run_git(root, "config", "user.email", "agent@example.com")
        self.run_git(root, "config", "user.name", "Harness Agent")
        (root / "README.md").write_text("# Sample\n", encoding="utf-8")
        self.run_git(root, "add", "README.md")
        self.run_git(root, "commit", "-m", "initial")

    def write_rules(self, root: Path) -> None:
        rules_dir = root / ".harness"
        rules_dir.mkdir()
        (rules_dir / "decision-memory-rules.json").write_text(
            json.dumps(
                {
                    "watched_paths": ["src/**"],
                    "decision_paths": ["docs/decisions/**"],
                    "ignored_paths": ["**/*.test.*"],
                }
            ),
            encoding="utf-8",
        )

    def test_watched_change_without_decision_record_warns_but_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            self.write_rules(root)
            app_file = root / "src" / "app" / "page.tsx"
            app_file.parent.mkdir(parents=True)
            app_file.write_text("export const label = 'new';\n", encoding="utf-8")

            result = self.run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Decision memory review warning", result.stdout)
            self.assertIn("input semantics", result.stdout)
            self.assertIn("displayed decision criteria", result.stdout)
            self.assertIn("src/app/page.tsx", result.stdout)
            self.assertIn("cite the existing ADR", result.stdout)

    def test_fail_on_warning_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            self.write_rules(root)
            source = root / "src" / "workflow.ts"
            source.parent.mkdir()
            source.write_text("export const state = 'changed';\n", encoding="utf-8")

            result = self.run_checker(root, "--fail-on-warning")

            self.assertEqual(1, result.returncode)
            self.assertIn("Decision memory review warning", result.stdout)

    def test_deleted_watched_file_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            self.write_rules(root)
            source = root / "src" / "workflow.ts"
            source.parent.mkdir()
            source.write_text("export const state = 'old';\n", encoding="utf-8")
            self.run_git(root, "add", "src/workflow.ts")
            self.run_git(root, "commit", "-m", "add workflow")

            source.unlink()
            result = self.run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Decision memory review warning", result.stdout)
            self.assertIn("src/workflow.ts", result.stdout)

    def test_committed_diff_against_base_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            self.write_rules(root)
            base = self.git_output(root, "rev-parse", "HEAD")
            source = root / "src" / "workflow.ts"
            source.parent.mkdir()
            source.write_text("export const state = 'changed';\n", encoding="utf-8")
            self.run_git(root, "add", "src/workflow.ts")
            self.run_git(root, "commit", "-m", "change workflow")

            result = self.run_checker(root, "--base", base)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Decision memory review warning", result.stdout)
            self.assertIn("src/workflow.ts", result.stdout)

    def test_committed_deletion_against_base_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            self.write_rules(root)
            source = root / "src" / "workflow.ts"
            source.parent.mkdir()
            source.write_text("export const state = 'old';\n", encoding="utf-8")
            self.run_git(root, "add", "src/workflow.ts")
            self.run_git(root, "commit", "-m", "add workflow")
            base = self.git_output(root, "rev-parse", "HEAD")

            source.unlink()
            self.run_git(root, "add", "src/workflow.ts")
            self.run_git(root, "commit", "-m", "remove workflow")
            result = self.run_checker(root, "--base", base)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Decision memory review warning", result.stdout)
            self.assertIn("src/workflow.ts", result.stdout)

    def test_invalid_explicit_base_fails_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            self.write_rules(root)

            result = self.run_checker(root, "--base", "missing-base")

            self.assertEqual(2, result.returncode)
            self.assertIn("could not diff against missing-base", result.stdout)
            self.assertIn("pass a valid --base", result.stdout)

    def test_decision_record_change_suppresses_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            self.write_rules(root)
            source = root / "src" / "workflow.ts"
            source.parent.mkdir()
            source.write_text("export const state = 'changed';\n", encoding="utf-8")
            decision = root / "docs" / "decisions" / "0002-workflow.md"
            decision.parent.mkdir(parents=True)
            decision.write_text("# Workflow\n\n## Context\n\n## Decision\n", encoding="utf-8")

            result = self.run_checker(root, "--fail-on-warning")

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_ignored_watched_path_does_not_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            self.write_rules(root)
            source = root / "src" / "workflow.test.ts"
            source.parent.mkdir()
            source.write_text("test('workflow', () => {});\n", encoding="utf-8")

            result = self.run_checker(root, "--fail-on-warning")

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_non_git_repository_skips(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.run_checker(root)

            self.assertEqual(0, result.returncode)
            self.assertIn("not inside a Git repository", result.stdout)


if __name__ == "__main__":
    unittest.main()
