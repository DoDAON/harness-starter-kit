from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "apply_harness.py"


def should_run_fastapi_e2e() -> bool:
    return os.environ.get("RUN_FASTAPI_E2E", "").lower() in {"1", "true", "yes"}


def venv_python(venv: Path) -> Path:
    if sys.platform == "win32":
        return venv / "Scripts" / "python.exe"
    return venv / "bin" / "python"


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


@unittest.skipUnless(
    should_run_fastapi_e2e(),
    "Set RUN_FASTAPI_E2E=1 to run dependency-installing FastAPI E2E test.",
)
class FastApiProfileE2ETests(unittest.TestCase):
    def run_command(self, command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )

    def create_target(self, root: Path) -> None:
        write_file(
            root / "README.md",
            """
            # FastAPI E2E Target

            Minimal FastAPI project used to verify harness-starter-kit adoption.

            ## Checks

            ```powershell
            .\\.venv\\Scripts\\python.exe -m pytest tests -v
            .\\.venv\\Scripts\\python.exe scripts\\check_harness.py
            ```
            """,
        )
        write_file(
            root / "AGENTS.md",
            """
            # AGENTS.md

            Existing project instructions. Harness adoption must preserve this
            file unless an explicit maintainer request says otherwise.
            """,
        )
        write_file(
            root / ".gitignore",
            """
            .venv/
            __pycache__/
            *.pyc
            .pytest_cache/
            .mypy_cache/
            .ruff_cache/
            harness-starter-kit/
            """,
        )
        write_file(
            root / "sample_fastapi" / "__init__.py",
            """
            from .main import create_app

            __all__ = ["create_app"]
            """,
        )
        write_file(
            root / "sample_fastapi" / "main.py",
            """
            from fastapi import FastAPI
            from pydantic import BaseModel


            class HealthResponse(BaseModel):
                status: str


            def create_app() -> FastAPI:
                app = FastAPI(title="Harness FastAPI E2E")

                @app.get("/health", response_model=HealthResponse)
                def health() -> HealthResponse:
                    return HealthResponse(status="ok")

                return app


            app = create_app()
            """,
        )
        write_file(
            root / "tests" / "test_app.py",
            """
            from fastapi.testclient import TestClient

            from sample_fastapi import create_app


            def test_health_endpoint_returns_ok() -> None:
                client = TestClient(create_app())

                response = client.get("/health")

                assert response.status_code == 200
                assert response.json() == {"status": "ok"}
            """,
        )

    def test_fastapi_profile_adoption_runs_generated_harness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.create_target(target)

            venv = target / ".venv"
            self.run_command([sys.executable, "-m", "venv", str(venv)], cwd=target)
            python = venv_python(venv)
            self.run_command(
                [
                    str(python),
                    "-m",
                    "pip",
                    "install",
                    "fastapi",
                    "httpx",
                    "mypy",
                    "pytest",
                ],
                cwd=target,
            )

            install_result = self.run_command(
                [
                    sys.executable,
                    str(INSTALLER),
                    "--target",
                    str(target),
                    "--profile",
                    "fastapi",
                ],
                cwd=REPO_ROOT,
            )
            self.assertIn("skip-existing", install_result.stdout)
            self.assertIn(str(target / "AGENTS.md"), install_result.stdout)

            repeat_result = self.run_command(
                [
                    sys.executable,
                    str(INSTALLER),
                    "--target",
                    str(target),
                    "--profile",
                    "fastapi",
                ],
                cwd=REPO_ROOT,
            )
            self.assertIn("Summary: 0 created, 0 overwritten", repeat_result.stdout)

            shutil.copy2(
                target / "docs" / "harness" / "profiles" / "fastapi" / "check_harness.py",
                target / "scripts" / "check_harness.py",
            )

            self.run_command([str(python), "scripts/check_docs_drift.py"], cwd=target)
            self.run_command([str(python), "scripts/check_structure.py"], cwd=target)
            harness_result = self.run_command(
                [str(python), "scripts/check_harness.py"],
                cwd=target,
            )
            self.assertIn("Success: no issues found", harness_result.stdout)


if __name__ == "__main__":
    unittest.main()
