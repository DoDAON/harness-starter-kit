# React Harness Profile

Use these snippets when the target project is a React app such as Vite, CRA, or
a similar client-side project.

These files are agent reference material, not automatic transformations. Merge
only the pieces that fit the target project's existing tools.

Apply this profile by priority: always preserve the target package manager,
generated-file rules, and exact local checks; document API/auth setup when
present; consider decision records only when changing routing, state, rendering,
or integration policy; use a short report/check note for narrow fixes.

## Recommended Checks

- `npm run lint` for ESLint including react-hooks rules.
- `npm run typecheck` for TypeScript type checks without emitting files.
- `npm test` for unit and component tests.
- `npm run build` to confirm the production bundle compiles.
- `python scripts/check_docs_drift.py` for stale documentation references.
- `python scripts/check_structure.py` for temporary or drift-prone files.

## Suggested package.json Scripts

Merge the scripts from `package-scripts.harness.json` into the target
project's `package.json`.

## Suggested Check Script

Copy or adapt `check_harness.py` into the target repository's `scripts/`
directory when the project has no existing task runner. It detects npm, pnpm,
or yarn, then runs whichever of `lint`, `typecheck`, `test`, and `build` are
already present in `package.json`, followed by the generic drift checks.

## ESLint Config

Merge rules from `eslint.config.harness.mjs` into the target project's ESLint
config. The snippet enables `eslint-plugin-react-hooks` and
`eslint-plugin-react-refresh`, which are the most impactful React-specific
rules.

## Profile Absorption Notes

When React is introduced after generic adoption:

- Merge useful scripts from `package-scripts.harness.json` into `package.json`
  instead of replacing the target's scripts.
- Merge relevant ignores from `gitignore.harness.txt`, especially generated
  build output, dependency directories, local env files, and the local
  `harness-starter-kit/` clone.
- Merge React ESLint rules only when the target already uses ESLint or
  intentionally adopts it.
- Copy or adapt `check_harness.py` into `scripts/` only when the target has no
  equivalent local verification command.
- Update `AGENTS.md` with React commands, source directories, generated paths,
  and completion checks.
- Update `docs/conventions/coding.md` with component, hook, state, routing,
  styling, and testing conventions.
- Consider a decision record when changing or selecting React, a routing
  approach, state management approach, input semantics, fallback behavior, or
  displayed decision criteria. When the task only follows the existing
  architecture or makes a narrow fix, a final report or check note is enough.
- In the final report, list which snippets were adopted, adapted, skipped, or
  deferred.

## React Notes

- Name components in PascalCase; name hooks with the `use` prefix.
- Keep side effects inside `useEffect`; never perform data fetching directly
  inside render.
- Satisfy the react-hooks/exhaustive-deps rule because missing dependencies in
  `useEffect` are a common source of stale-closure bugs.
- Prefer small, focused components; extract reusable logic into custom hooks.
- Treat UI-only looking changes as decision-memory candidates when they alter
  input meaning, state normalization, or the criteria shown to users for a
  product decision.
- Do not import from more than two parent levels deep; use path aliases only
  when they already exist or are intentionally added.
- Do not edit or commit `dist/`, `node_modules/`, Vite cache directories, or
  the local `harness-starter-kit/` clone.
