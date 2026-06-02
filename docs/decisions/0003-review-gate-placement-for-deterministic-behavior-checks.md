# 0003. Review Gate Placement For Deterministic Behavior Checks

## Status

Accepted

## Date

2026-06-02

## Context

The kit already tells agents to add useful verification and to keep live API
smoke checks separate from default verification when credentials, quota,
network access, or provider uptime make them unsafe as normal gates.

During TodayBus dogfood work, this guidance caught the live-smoke side of the
problem but missed the complementary case. `npm run test:planner` was
deterministic, local, non-network, and reasonably fast, and it verified planner
fallback behavior that agents were expected to check repeatedly. It was
initially grouped with focused live smoke commands instead of being reviewed as
a normal completion gate candidate.

The target repository remains the source of truth. Different targets may use
`make test`, `just check`, package scripts, CI workflows,
`scripts/check_harness.py`, or another local command as the normal completion
gate. A generic parser that infers gate placement from `test:*` or `check:*`
script names would be noisy and would misclassify live API, visual, device,
watcher, slow, or provider-dependent checks.

## Decision

Add gate-placement review as a prompt-first governance and reporting rule.

When adoption, review, refresh, or target harness maintenance discovers a
deterministic, local, non-network, reasonably fast check for product behavior
that agents are expected to verify repeatedly, the check should be included in
the documented normal completion gate or have a documented reason for remaining
focused or manual.

Keep live API, credential, quota, provider-uptime, visual, device, watcher,
slow, hardware-dependent, or otherwise fragile checks outside the normal gate
unless they are stable, safe, and expected in the target repository's normal
environment.

The normal completion gate must be named from the target repository's actual
workflow. Do not assume it is called `check:harness`.

Validate saved adoption reports for the presence of gate-placement fields, but
do not add generic script-name parsing or automatic gate inference yet.

## Rationale

- The rule closes a real dogfood gap without making the kit installer-first or
  parser-first.
- It keeps the target repository as the source of truth by asking agents to
  name the target's actual normal gate.
- It distinguishes stable local behavior checks from live, slow, device, or
  provider-dependent checks instead of pushing every check into the default
  gate.
- Report-field validation catches incomplete saved adoption reports without
  guessing which commands belong in the gate.
- A future manifest or stricter doctor check can build on this once more
  target repositories produce comparable gate-placement records.

## Alternatives Considered

- Parse package scripts such as `test:*` or `check:*`: rejected for now because
  script names do not reliably distinguish deterministic behavior checks from
  live API, visual, watcher, device, or slow checks.
- Require every verification script to enter the normal gate: rejected because
  it would make normal verification brittle in repositories with credentials,
  network dependencies, quota, hardware, or provider uptime concerns.
- Leave gate placement only in failure memory: rejected because failure notes
  record what went wrong, but they do not make the accepted governance and
  reporting rule durable.

## Agent Guidance

When adding or reviewing verification, separate gate placement from check
existence. If a check is deterministic, local, non-network, reasonably fast, and
covers product behavior that agents should verify repeatedly, include it in the
documented normal completion gate or explain why it remains focused or manual.

Do not assume the gate is named `check:harness`; use the target repository's
actual documented workflow. Do not add broad automatic parsing for script names
without a new decision record or stronger target evidence.
