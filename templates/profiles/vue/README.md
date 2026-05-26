# Vue Harness Profile

Use these snippets when the target project is a Vue 3 app such as Vite + Vue,
Nuxt, or a similar client-side project.

These files are agent reference material, not automatic transformations. Merge
only the pieces that fit the target project's existing tools.

## Recommended Checks

- `npm run lint` for ESLint including eslint-plugin-vue rules.
- `npm run typecheck` for TypeScript type checks via vue-tsc.
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
config. The snippet enables `eslint-plugin-vue` with Vue 3 recommended rules.

## Profile Absorption Notes

When Vue or Vite is introduced after generic adoption:

- Merge useful scripts from `package-scripts.harness.json` into `package.json`
  instead of replacing the target's scripts.
- Merge relevant ignores from `gitignore.harness.txt`, especially `.vite/`,
  `dist/`, `node_modules/`, local env files, and the local
  `harness-starter-kit/` clone.
- Merge Vue ESLint rules only when the target already uses ESLint or
  intentionally adopts it.
- Copy or adapt `check_harness.py` into `scripts/` only when the target has no
  equivalent local verification command.
- Update `AGENTS.md` with Vue/Vite commands, source directories, generated
  paths, and completion checks.
- Update `docs/conventions/coding.md` with component, state, routing, styling,
  and testing conventions.
- Add a decision record when choosing Vue/Vite, a routing approach, or a state
  management approach is an architectural decision.
- In the final report, list which snippets were adopted, adapted, skipped, or
  deferred.

## Vue Notes

- Prefer script setup syntax with the Composition API for new components.
- Name single-file components in PascalCase, and use PascalCase in templates.
- Keep component files in the target project's established component directory.
- Manage shared state with Pinia stores in Vue 3 projects unless the project
  already uses another state approach.
- Use `defineProps` and `defineEmits` with TypeScript generics for typed
  component contracts.
- Do not access `$parent` or mutate props directly; communicate via emits or
  shared stores.
- Do not edit or commit `dist/`, `node_modules/`, Vite cache directories, or
  the local `harness-starter-kit/` clone.
