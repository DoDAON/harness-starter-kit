# React Harness Profile

Use these snippets when the target project is a React app such as Vite, CRA, or
a similar client-side project.

These files are agent reference material, not automatic transformations. Merge
only the pieces that fit the target project's existing tools.

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

## React Notes

- Name components in PascalCase; name hooks with the `use` prefix.
- Keep side effects inside `useEffect`; never perform data fetching directly
  inside render.
- Satisfy the react-hooks/exhaustive-deps rule because missing dependencies in
  `useEffect` are a common source of stale-closure bugs.
- Prefer small, focused components; extract reusable logic into custom hooks.
- Do not import from more than two parent levels deep; use path aliases only
  when they already exist or are intentionally added.
- Do not edit or commit `dist/`, `node_modules/`, Vite cache directories, or
  the local `harness-starter-kit/` clone.
