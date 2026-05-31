# Changelog

Notable project changes should be recorded here before release tags are cut.

## v0.1.3 - 2026-05-31

Patch release for `/harness review` reviewer-mode routing. This release keeps
the command diagnostic-only while making subagent availability and fallback
reporting harder to skip silently.

### Added

- Explicit `/harness review sub-agent` invocation mode that treats the request
  as permission to call a read-only reviewer subagent when the active runtime
  and tool instructions allow it.
- Review report `Invocation`, `Reviewer mode`, and `Fallback reason` fields in
  the template and example report.
- Regression coverage for subagent fallback guidance, prompt drift, localized
  README wiring, and route precedence between `/harness review sub-agent` and
  `/harness review`.

### Changed

- Clarify `/harness review` fallback behavior when a subagent tool is present
  but not permitted by active tool instructions.
- Route the more specific `/harness review sub-agent` command before the
  generic `/harness review` command in agent-facing prompts and command
  routing.

## v0.1.2 - 2026-05-31

Governance release for change-set review. This release adds a diagnostic
`/harness review` workflow so maintainers can challenge current changes before
completion without adding runtime hooks, policy enforcement, CI adapters, or
more automatic installer behavior.

### Added

- `/harness review` command workflow for opposing harness-engineering review of
  the current change set.
- Harness review report template and example report.
- Quick Start, full adoption prompt, localized README, static site, and
  component-map wiring for `/harness review`.
- Regression tests that keep `/harness review` command routing, localized docs,
  report-template sections, and prompt drift covered.

### Changed

- Clarify that the existing harness review checklist is a periodic maintenance
  checklist, distinct from the `/harness review` change-set command.
- Update the roadmap from adding `/harness review` to refining it through real
  target-repository use.

## v0.1.1 - 2026-05-30

Stabilization release for the initial harness workflow. This release strengthens
the theory, evaluation, failure-memory, and contributor guidance added around
the `v0.1.0` early release.

### Added

- Harness engineering theory document that separates repository harness health
  from observed agent effectiveness.
- Task outcome record template for comparable agent-work observations.
- Roadmap and expanded contributor guidance for profiles, drift checks,
  adoption examples, and release validation.
- Regression coverage that keeps the static site copy prompt aligned with the
  README adoption prompt.

### Changed

- Compact root and generic `AGENTS.md` guidance while preserving command
  routing, analysis, validation, and commit rules.
- Clarify `python3` validation commands for macOS/Linux environments where
  `python` is unavailable.
- Clarify Harness Doctor score scope and non-scored evaluation/governance
  signals.
- Strengthen adoption and update guidance around failure-memory records for
  user-visible runtime failures, high-risk bug paths, failed checks, repeated
  agent mistakes, and cross-environment mismatches.

## v0.1.0 - 2026-05-29

Initial early release of `harness-starter-kit`.

This release is for maintainers who want to make repositories safer for AI
coding agents through durable instructions, project memory, feedback loops, and
drift checks. The kit is prompt-first by design; the installer is a conservative
bootstrap helper, not a full automatic migration tool.

### Added

- Prompt-first adoption workflow for applying the kit from a target repository.
- Generic harness templates for `AGENTS.md`, knowledge storage, and drift
  checks.
- Stack profile snippets for Python, TypeScript, Node.js, Next.js, React, Vue,
  Django, Flask, FastAPI, Spring Boot, and Android.
- `/harness doctor`, `/harness update`, and `/harness refresh` command
  workflows.
- Drift checks for documentation references, structure hygiene, encoding
  hygiene, and effectiveness measurement plans.
- Harness Doctor baseline scoring across agent instructions, feedback loops,
  durable memory, structural safety, and adoption clarity.
- Fixture smoke tests and an opt-in FastAPI profile E2E test.
- Adoption report and effectiveness report templates.
- Lifecycle pilot notes, launch essay link, and Django dogfood repository link.
