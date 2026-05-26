<pre align="center">
 _   _    _    ____  _   _ _____ ____ ____
| | | |  / \  |  _ \| \ | | ____/ ___/ ___|
| |_| | / _ \ | |_) |  \| |  _| \___ \___ \
|  _  |/ ___ \|  _ <| |\  | |___ ___) |__) |
|_| |_/_/   \_\_| \_\_| \_|_____|____/____/

 ____ _____  _    ____ _____ _____ ____    _  _____ _____
/ ___|_   _|/ \  |  _ \_   _| ____|  _ \  | |/ /_ _|_   _|
\___ \ | | / _ \ | |_) || | |  _| | |_) | | ' / | |  | |
 ___) || |/ ___ \|  _ < | | | |___|  _ <  | . \ | |  | |
|____/ |_/_/   \_\_| \_\|_| |_____|_| \_\ |_|\_\___| |_|
</pre>

# harness-starter-kit

<p align="center">
  <img alt="Generic profile" src="https://img.shields.io/badge/profile-generic-6b7280?style=flat-square" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
  <img alt="Spring Boot" src="https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white" />
</p>

<p align="center">
  <img alt="Django" src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white" />
  <img alt="Flask" src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img alt="Next.js" src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" />
  <img alt="React" src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=111111" />
  <img alt="Vue" src="https://img.shields.io/badge/Vue-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white" />
</p>

**English** | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

[Site](https://baskduf.github.io/harness-starter-kit/) |
[Adoption prompt](docs/prompts/apply-to-target-repo.md)

`harness-starter-kit` is a prompt-first starter kit for applying harness
engineering to any software project. It is meant to be cloned into a target
repository, read by an agent, and adapted to that repository's actual tools and
constraints.

The intended workflow is simple:

```text
Clone harness-starter-kit into a target project.
Ask an agent: "Read ./harness-starter-kit and apply its harness engineering guidelines
to this repo. Preserve the existing architecture and add only the minimum
missing harness files."
```

This is not primarily an automatic installer. The target project should end up
with a practical agent harness because an agent inspected the repository and
added the smallest useful set of durable artifacts:

- `AGENTS.md` for durable agent instructions
- architecture constraints through linting, type checks, import boundaries, or
  project-specific rules
- feedback loops through tests, CI, pre-commit hooks, and clear failure messages
- a knowledge store under `docs/` for decisions, failures, conventions, and
  domain context
- garbage-collection checks that detect code, document, and structure drift

## Why This Exists

Prompting is temporary. Context is session-scoped. A harness is project-scoped.

Good harness engineering moves repeated instructions out of chat and into the
repository so agents can work inside stable rules. When an agent makes a
mistake, the long-term fix is not only to correct that output. The better fix is
to add a rule, test, document, or automated check that makes the same mistake
less likely next time.

## Quick Start

Clone or download this repository inside the target project:

```text
workspace/
`-- target-repo/
    |-- harness-starter-kit/
    `-- existing-project-files
```

Then open `target-repo`, not `target-repo/harness-starter-kit`, with your
coding agent. The target repository is the working directory; the nested
`harness-starter-kit/` directory is read-only reference material.

Give the agent this prompt:

```text
Read ./harness-starter-kit first, then apply the harness engineering starter kit
to this repository.

Treat the current working directory as the target repository. Treat
./harness-starter-kit as read-only reference material unless I explicitly ask
you to edit the kit itself.

Preserve this repository's existing architecture, tools, package manager,
commands, and conventions. Add only the minimum missing harness files. Prefer
updating existing docs/configs over duplicating them. Do not overwrite or delete
existing files without explaining why.

Finish with a short adoption report listing files changed, checks I can run,
assumptions made, and remaining manual steps.
```

The prompt-first workflow is the main way to use this kit because the agent can
inspect the target repository and adapt to its existing tools. During adoption,
the agent should inspect the stack, package manager, test and lint commands,
existing docs, agent instruction files, CI, and repository layout before
editing.

Before committing the target repository, decide what to do with the local
`harness-starter-kit/` clone: remove it, add it to the target `.gitignore`, or
keep it intentionally as a submodule/reference. Do not accidentally commit the
nested clone as ordinary project content.

### Optional Skeleton Bootstrap

`apply_harness.py` is a skeleton bootstrapper, not a full harness adoption
engine. It creates generic starter files and profile reference snippets. It does
not inspect, merge, or validate the target repository's architecture.

Use it only when you want a quick initial file structure before agent-driven
adaptation. Preview the generated files first:

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

The script never overwrites existing files unless `--force` is provided. By
default it installs local harness skeleton files only; add `--with-ci` only when
the target repository should also receive the optional GitHub Actions harness
workflow.

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --with-ci
```

## Agent-Driven Adoption

In a new or existing project, the agent-driven path is the real adoption path.
The agent should inspect first, adapt second, and report the result. Give your
coding agent this prompt:

```text
Read ./harness-starter-kit first. Apply the harness engineering starter kit to this
repository.

Requirements:
- Inspect the target repository before editing.
- Identify the language, framework, package manager, test command, lint command,
  build command, CI provider, docs structure, and monorepo layout if present.
- Read existing AGENTS.md, CLAUDE.md, README, CONTRIBUTING, and CI configs if
  they exist.
- Preserve existing architecture, tools, and conventions.
- Add or update AGENTS.md with project-specific rules.
- Add docs/decisions, docs/failures, docs/conventions, and docs/domain if they
  are missing and no equivalent knowledge store exists.
- Add lightweight drift checks under scripts/ only when they reflect real target
  repo rules, then wire stable checks into the closest existing verification
  path.
- Prefer existing linters, tests, CI, and package managers over introducing new
  ones.
- Do not overwrite existing files without explaining why.
- Finish with a short report listing files changed, checks added, assumptions,
  remaining manual integration steps, and what to do with ./harness-starter-kit
  before committing.
```

The longer version lives in
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md).

## Repository Layout

```text
harness-starter-kit/
|-- AGENTS.md
|-- docs/
|   |-- adoption-workflow.md
|   |-- component-map.md
|   |-- overview.md
|   |-- checklists/
|   `-- prompts/
|-- scripts/
|   `-- apply_harness.py
|-- tests/
`-- templates/
    |-- generic/
    `-- profiles/
```

## Adoption Modes

Use `generic` for any project. It installs the durable harness skeleton without
assuming a language or framework.

Use `python` when the target project uses Python. It adds Python-focused
reference snippets for Ruff, mypy, vulture, and pre-commit.

Use `typescript` when the target project uses JavaScript or TypeScript. It adds
reference snippets for ESLint, dependency boundaries, unused export checks, and
package scripts.

Use `nextjs` when the target project is a Next.js app. It adds reference
snippets for `next build`, non-emitting TypeScript checks, generated-file
ignores, and current Next.js lint caveats.

Use `django` when the target project is a Django app. It adds reference
snippets for `manage.py check`, `manage.py test`, virtual environment ignores,
SQLite development database ignores, and a Python `check_harness.py` entrypoint.

Use `flask` when the target project is a Flask app. It adds reference snippets
for `unittest` discovery, Flask route checks, instance-data ignores, and a
Python `check_harness.py` entrypoint.

Use `spring` when the target project is a Spring Boot app. It adds reference
snippets for Maven or Gradle wrapper checks, Spring test commands, generated
build output ignores, local config ignores, and a Python `check_harness.py`
entrypoint.

Profiles are intentionally conservative reference material for the agent. They
are not automatic project transformations. The installer copies profile files
under `docs/harness/profiles/<profile>/` so an agent or maintainer can merge,
adapt, or ignore the relevant snippets while preserving the target project's
existing build system.

The generic drift checks are baseline hygiene checks:

- `scripts/check_docs_drift.py` catches broken local Markdown links and stale
  file references in docs.
- `scripts/check_structure.py` catches temporary and drift-prone filenames.

Useful architecture drift checks must come from the target repository's actual
rules. For example, if `AGENTS.md` says routes must not access the database
directly, add a check for forbidden database imports in route files. If an ADR
chooses Zustand instead of Redux, add a check that fails when Redux dependencies
appear. If generated files must live under one directory, add a structure rule
that rejects generated files elsewhere.

If a repository starts with the generic harness and later introduces a concrete
stack, run the
[`profile-absorption` checklist](docs/checklists/profile-absorption.md). It
helps decide which profile snippets should become real project scripts,
configuration, ignores, documentation, or checks.

## Tested Scenarios

Automated fixture smoke tests cover harness installation for:

- Node.js / TypeScript
- Next.js
- Django
- FastAPI
- Flask
- React
- Spring Boot
- Vue

These fixture tests verify that the installer preserves existing files, writes
the expected profile snippets, and produces runnable generic drift checks.

Additional end-to-end adoption checks have been run manually against:

- a Node.js ES module project using `node --test`, repeated installer runs,
  the TypeScript profile `check_harness.py`, and intentional drift failures
- a FastAPI project using pytest, mypy, generated drift checks, and the FastAPI
  profile `check_harness.py`

FastAPI E2E coverage is also available as an opt-in automated test because it
creates a virtual environment and installs dependencies:

```powershell
$env:RUN_FASTAPI_E2E = "1"
python -m unittest tests.test_fastapi_profile_e2e
```

In GitHub Actions, run the `Harness Check` workflow manually and enable
`run_fastapi_e2e` to execute the same dependency-installing test.

See `examples/node-adoption-report.md` and
`examples/nextjs-adoption-report.md`, `examples/django-adoption-report.md`, or
`examples/flask-adoption-report.md` for example adoption reports. See
`examples/spring-adoption-report.md` for a Spring example.

## Local Checks

Run these checks before changing the starter kit templates or installer:

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
```

## License

This project is licensed under the [MIT License](LICENSE).

## Core Principle

Every recurring agent failure should be converted into at least one durable
artifact:

- a clearer instruction in `AGENTS.md`
- an automated constraint
- a test or CI check
- a decision or failure record
- a drift check

That is the heart of harness engineering.
