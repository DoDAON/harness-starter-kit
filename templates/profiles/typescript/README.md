# TypeScript Harness Profile

Use these snippets when the target project is JavaScript or TypeScript.

These files are agent reference material, not automatic transformations. Merge
only the pieces that fit the target project's existing tools.

Apply this profile by priority: always preserve the target package manager,
generated-file rules, and exact local checks; document API/auth/service fixtures
when present; consider decision records only when changing module boundaries,
runtime, state, or integration policy; use a short report/check note for narrow
fixes.

## Recommended Checks

- ESLint for linting.
- TypeScript compiler for type checking.
- Dependency boundary rules for architecture constraints.
- Unused export checks such as `ts-prune` or `knip`.
- `python scripts/check_harness.py` as a small local verification entrypoint
  when the target project has no existing task runner.

## Suggested Check Script

Copy or adapt `check_harness.py` into the target repository's `scripts/`
directory when the project has no existing task runner. It detects npm, pnpm,
or yarn, then runs whichever of `lint`, `typecheck`, `test`, and `build` are
already present in `package.json`, followed by the generic drift checks.

## Profile Absorption Notes

When JavaScript or TypeScript is introduced after generic adoption:

- Merge useful scripts from `package-scripts.harness.json` into `package.json`
  instead of replacing the target's scripts.
- Merge ESLint rules from `eslint.config.harness.mjs` only when the target
  already uses ESLint or intentionally adopts it.
- Keep the target package manager as source of truth; do not add npm, pnpm, or
  yarn only because this profile mentions them.
- Copy or adapt `check_harness.py` into `scripts/` only when the target has no
  equivalent local verification command.
- Update `AGENTS.md` with the chosen package manager and check commands.
- Update `docs/conventions/coding.md` with module layout, import, testing, and
  type-checking conventions that agents should repeat.
- Consider a decision record when changing or selecting module boundaries,
  runtime, state, integration policy, input semantics, fallback behavior, or
  displayed decision criteria. When the task only follows the existing
  architecture or makes a narrow fix, a final report or check note is enough.
- In the final report, list which snippets were adopted, adapted, skipped, or
  deferred.

## Integration Notes

Do not replace existing ESLint or package manager configuration blindly. Merge
the relevant rules into the target project.
