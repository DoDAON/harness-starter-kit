# FastAPI Harness Profile

Use these snippets when the target project is a FastAPI app or API.

These files are agent reference material, not automatic transformations. Merge
only the pieces that fit the target project's existing tools.

## Recommended Checks

- `pytest` for tests, or `python -m pytest` inside a virtual environment.
- `mypy .` for static type checks because FastAPI relies heavily on type
  annotations.
- A lightweight app import or route test to validate startup.
- `scripts/check_docs_drift.py` for stale documentation references.
- `scripts/check_structure.py` for temporary or drift-prone files.

Prefer the target repository's virtual environment path when documenting
commands. On Windows PowerShell, that is often:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mypy .
.\.venv\Scripts\python.exe scripts\check_harness.py
```

## Suggested Check Script

Copy or adapt `check_harness.py` into the target repository's `scripts/`
directory when the project has no existing task runner.
The script excludes generated harness profile snippets and local virtual
environments from mypy by default so copied reference files do not create
duplicate-module noise.

## Profile Absorption Notes

When FastAPI is introduced after generic adoption:

- Merge useful settings from `pyproject.harness.toml` into the target
  `pyproject.toml` instead of replacing existing configuration.
- Merge relevant ignores from `gitignore.harness.txt`, especially virtual
  environments, generated Python caches, test caches, and the local
  `harness-starter-kit/` clone.
- Copy or adapt `check_harness.py` into `scripts/` only when the target has no
  equivalent local verification command.
- Update `AGENTS.md` with FastAPI commands, app entrypoints, source
  directories, generated paths, and completion checks.
- Update `docs/conventions/coding.md` with router, dependency injection,
  schema, service, repository, testing, and error handling conventions.
- Add a decision record when choosing FastAPI, an app layout, persistence
  approach, or migration tool is an architectural decision.
- In the final report, list which snippets were adopted, adapted, skipped, or
  deferred.

## FastAPI Notes

- Define routes in router modules; keep business logic in a services layer and
  data access in a repositories layer.
- Use Pydantic models for request and response schemas; do not bypass
  validation with raw `dict` types.
- Prefer dependency injection with `Depends` over global state for database
  sessions, auth, and settings.
- Use `pytest` with `httpx.AsyncClient` or `TestClient` for HTTP behavior
  checks.
- Annotate route functions and service methods with return types so mypy can
  catch schema drift.
- Do not edit or commit `.venv/`, generated Python caches, or the local
  `harness-starter-kit/` clone.
- Add Ruff, pre-commit, or Alembic only when they fit the target repository's
  existing tooling.
