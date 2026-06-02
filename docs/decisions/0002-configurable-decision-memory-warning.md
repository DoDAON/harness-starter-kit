# 0002. Use A Configurable Warning Gate For Decision Memory

## Status

Accepted

## Date

2026-06-02

## Context

The kit already asks agents to handle decision memory when implementation work
changes product structure, workflow, integration boundaries, data models,
state classifications, or UX principles.

In practice, agents can still miss the final-report step while focused on
implementation and verification. Small UI-looking changes can also change input
semantics, state normalization, API request or response shape, fallback policy,
or displayed decision criteria. Those changes may deserve a new ADR, an
existing ADR citation, or a short explanation that no decision memory is
needed.

A hard generic rule would be too noisy because repository layouts and product
contract boundaries vary. Common JavaScript application paths under source,
component, app, or library directories fit some projects but not every target
repository.

## Decision

Add `scripts/check_decision_memory.py` as an optional diff-based warning gate.

The check watches implementation paths configured in
`.harness/decision-memory-rules.json`. When watched paths changed and
`docs/decisions/` did not, it prints a warning that asks the agent to do one of
three things before the final report:

- add or update a decision record
- cite the existing ADR that covers the change
- explain why no decision memory is needed

The default behavior exits successfully after printing the warning. Targets
that want stricter enforcement can run the script with `--fail-on-warning`.

## Rationale

- The goal is to force the decision-memory judgment to be visible, not to write
  an ADR for every UI or implementation change.
- A warning preserves the prompt-first model and keeps the target repository as
  the source of truth.
- Configurable watched paths avoid baking one stack layout into the generic
  kit.
- An opt-in failure mode lets mature target repositories promote the warning
  after they tune the rule to their own architecture.

## Consequences

- Generic adoption gets a lightweight sensor for a known agent omission path.
- Target repositories may need to adjust `.harness/decision-memory-rules.json`
  to match their source directories and ignored paths.
- CI use requires an explicit diff base when the default local `HEAD`
  comparison is not meaningful for the workflow. The generic GitHub Actions
  template passes the pull request base SHA for PR events and keeps the default
  local smoke check for non-PR runs.
- The starter kit repository may tune its root
  `.harness/decision-memory-rules.json` differently from
  `templates/generic/.harness/decision-memory-rules.json`, because scripts,
  command docs, templates, and profile snippets are product behavior in this
  repository but may be reference-only paths in a target repository.
- Reviewers should still apply judgment. A clean script result is not proof
  that no decision memory is needed.

## Agent Guidance

When the warning appears, do not silence it by changing watched paths unless
the paths are genuinely wrong for the target repository. Add or update an ADR,
cite an existing ADR, or explain why the change is too narrow to need decision
memory.

Before relying on the check, tune the watched and ignored paths to the target
repository. If scripts, generated fixtures, smoke checks, or CLI commands carry
product behavior or workflow contracts, do not leave those paths ignored.

For UI-heavy work, treat changed input semantics, state normalization,
fallback behavior, and displayed decision criteria as decision-memory
candidates even when the visual diff is small.
