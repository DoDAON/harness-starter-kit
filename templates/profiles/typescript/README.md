# TypeScript Harness Profile

Use these snippets when the target project is JavaScript or TypeScript.

These files are agent reference material, not automatic transformations. Merge
only the pieces that fit the target project's existing tools.

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

## Integration Notes

Do not replace existing ESLint or package manager configuration blindly. Merge
the relevant rules into the target project.
