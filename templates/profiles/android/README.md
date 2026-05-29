# Android Harness Profile

Use these snippets when the target project is an Android or Kotlin app,
especially when the Android project lives under a nested directory.

These files are agent reference material, not automatic transformations. Merge
only the pieces that fit the target project's existing Gradle setup and local
development workflow.

## Recommended Checks

- `./gradlew test` or `.\gradlew.bat test` for JVM unit tests.
- `./gradlew assembleDebug` or `.\gradlew.bat assembleDebug` to verify the
  debug APK builds.
- `python scripts/check_docs_drift.py` for stale documentation references.
- `python scripts/check_structure.py` for temporary or drift-prone files.
- `python scripts/check_encoding_hygiene.py` when Korean, Japanese, Chinese, or
  other localized source/XML text has shown mojibake or non-UTF-8 risk.

Prefer the project Gradle wrapper over global `gradle`. On Windows PowerShell,
that is often:

```powershell
.\gradlew.bat test
.\gradlew.bat assembleDebug
python scripts\check_harness.py --project-dir app-or-android-project-folder
```

## Suggested Check Script

Copy or adapt `check_harness.py` into the target repository's `scripts/`
directory when the project has no existing task runner. It detects a nested
Android Gradle project, runs `test` and `assembleDebug` by default, then runs
generic drift checks when they are present.

## Local Server And Data Fixtures

If the repository includes a local server JAR, SQL seed files, docker-compose
file, or backend fixture used by the app:

- Document the server start command, working directory, Java version, ports,
  seed data, and shutdown steps in `README.md`, `AGENTS.md`, or
  `docs/domain/`.
- Add a small server verification plan before implementing app behavior. At
  minimum, record how to prove the server started and which endpoint or log
  line confirms readiness.
- If the server cannot be run locally, explain why and list the manual or
  emulator/device checks that remain.
- Keep Retrofit or HTTP client base URLs behind the existing project
  configuration boundary. Do not hard-code machine-specific hostnames or ports
  into feature code.

## Scenario Test Plan

Before feature implementation, write a small scenario matrix or explicitly say
why build-only validation is enough. For mobile training apps, common scenarios
include:

- login and session handling
- product list and product detail loading
- cart and order flows
- comments, reviews, or other write flows
- NFC behavior, including devices without NFC
- Bluetooth or beacon behavior, including permissions and unavailable hardware

## Profile Absorption Notes

When Android or Kotlin is introduced after generic adoption:

- Copy or adapt `check_harness.py` into `scripts/` only when the target has no
  equivalent local verification command.
- Merge relevant ignores from `gitignore.harness.txt`, especially Gradle and
  Android generated outputs, local SDK files, IDE metadata, and the local
  `harness-starter-kit/` clone.
- Update `AGENTS.md` with the Android project path, Gradle commands, generated
  paths, local server commands, emulator/device expectations, and completion
  checks.
- Update `docs/conventions/coding.md` with package boundaries, ViewModel or
  UI-layer rules, Retrofit/API boundaries, coroutine/threading expectations,
  resource naming, and testing conventions.
- Add a decision record when choosing Android/Kotlin app structure, networking
  boundaries, persistence strategy, NFC/Bluetooth behavior, permission
  fallbacks, or local-server integration policy is an architectural decision.
- In the final report, list which snippets were adopted, adapted, skipped, or
  deferred.

## Android Notes

- Do not commit `local.properties`; document `ANDROID_HOME` or Android SDK
  setup requirements instead.
- Do not edit or commit generated outputs such as `build/`, `.gradle/`,
  `.cxx/`, `captures/`, APK/AAB files, or generated resource outputs.
- Treat emulator/device checks as manual verification unless the target already
  has instrumentation tests wired into CI.
- Document runtime permission checks for camera, location, Bluetooth, NFC, and
  notifications when behavior depends on them.
- Document NFC and Bluetooth/beacon caveats for unsupported devices, disabled
  radios, denied permissions, and simulator limitations.
