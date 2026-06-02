# Contributing

Thanks for helping improve `harness-starter-kit`. This project is a prompt-first
reference kit for adding durable agent rules, feedback loops, memory, and drift
checks to other repositories.

Before proposing broad automation, read
[`docs/decisions/0001-prompt-first-adoption.md`](docs/decisions/0001-prompt-first-adoption.md).
The target repository remains the source of truth.

## Good First Contribution Ideas

Good first contributions usually improve evidence, examples, or clarity without
changing the adoption model.

- Add or refine an adoption example.
- Improve Harness Doctor evidence messages.
- Add a GitLab CI or monorepo adoption note.
- Strengthen documentation around `/harness update` or `/harness refresh`.
- Improve localized README consistency.
- Add a new stack profile only when it includes a fixture and smoke test.

See [`ROADMAP.md`](ROADMAP.md) for the current project direction.

## Development

Use Python 3.11 or newer for local validation. On macOS/Linux, use `python3`
instead of `python` when `python` is unavailable. Before opening a pull request,
run:

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py scripts/check_encoding_hygiene.py scripts/check_effectiveness_plan.py scripts/check_decision_memory.py scripts/harness_doctor.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
python scripts/check_encoding_hygiene.py
python scripts/check_effectiveness_plan.py
python scripts/check_decision_memory.py
python scripts/harness_doctor.py --target .
```

## Change Guidelines

- Keep templates generic and conservative.
- Preserve prompt-first adoption: target repositories remain the source of
  truth.
- Do not blindly copy starter-kit defaults into profile guidance.
- When changing profile README files, also review
  `docs/templates/profile-readme.md`,
  `docs/checklists/profile-maintenance.md`, and
  `tests/test_profile_consistency.py`.
- Add or update tests for installer behavior, templates, drift scripts, command
  workflows, and scoring behavior.

## Adding A New Profile

Profiles are reference material, not automatic transformations. Do not add a
profile README by itself.

A profile contribution should usually include:

- `templates/profiles/<profile>/README.md` with conditional, practical guidance.
- Any merge-only snippets, such as `gitignore.harness.txt`,
  `package-scripts.harness.json`, `pyproject.harness.toml`, or
  `eslint.config.harness.mjs`.
- A minimal fixture under `tests/fixtures/<profile>-basic/`.
- Smoke coverage in `tests/test_smoke_fixtures.py`.
- Installer coverage in `tests/test_apply_harness.py` when the profile adds new
  snippet files.
- README and validation documentation updates when the public profile list
  changes.

Profile guidance should tell agents what to inspect, adopt, adapt, skip, or
defer. It should not assume that every target repository wants the same lint
rules, package scripts, CI workflow, or generated-file policy.

## Adding A Drift Check

Drift checks should enforce a real rule that future agents are likely to miss.

Before adding one:

- Name the repeated mistake, stale-doc risk, or architecture boundary it catches.
- Prefer a small Python script with clear failure output.
- Keep defaults safe for small repositories and easy to override.
- Add regression tests for false positives and expected failures.
- Document when maintainers should run the check locally or in CI.

If a check fixes a failed harness check, repeated agent mistake, or
cross-environment mismatch, add a `docs/failures/*.md` record unless the failure
was purely transient.

## Adding An Adoption Example

Adoption examples should be based on real or fixture-backed repository behavior.

Include:

- target stack, package manager, and verification commands
- files added or changed
- snippets adopted, adapted, skipped, or deferred
- checks run and their results
- effectiveness measurement plan or result location
- remaining manual steps and assumptions

Use `docs/templates/adoption-report.md` as the shape. If the example records
actual outcomes, use `docs/templates/effectiveness-report.md`.

## When Not To Add Automation

Do not add automation that makes the starter kit guess target-specific policy.

Avoid changes that:

- overwrite existing target files by default
- add package managers, CI providers, or framework tooling without target
  evidence
- treat stack profiles as mandatory migrations
- replace maintainer judgment with broad generated rewrites
- make `scripts/apply_harness.py` the primary adoption mechanism

Prefer better prompts, diagnostics, report templates, examples, and safe patch
guidance before adding mutation-heavy behavior.

## Required Tests By Change Type

Use the smallest relevant set, then run the full local validation before a
release.

| Change type | Required checks |
| --- | --- |
| Installer behavior | `python -m unittest tests.test_apply_harness` and `python -m py_compile scripts/apply_harness.py` |
| Drift scripts | Matching `tests/test_check_*.py`, `python -m py_compile scripts/check_*.py`, and the changed script directly |
| Harness Doctor scoring | `python -m unittest tests.test_harness_doctor` and `python scripts/harness_doctor.py --target .` |
| Profile README guidance | `python -m unittest tests.test_profile_consistency` plus profile fixture smoke coverage |
| New profile | `python -m unittest tests.test_apply_harness tests.test_smoke_fixtures tests.test_profile_consistency` |
| README prompt block | `python -m unittest tests.test_readme_prompt_drift` |
| Adoption or effectiveness reports | `python scripts/check_effectiveness_plan.py` |
| Release preparation | Full local validation from the Development section |

## Pull Requests

Keep each pull request focused on one logical harness change. Summarize changed
files, checks run, assumptions, and any manual follow-up needed.
