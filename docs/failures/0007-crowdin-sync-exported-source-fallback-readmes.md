# 0007. Crowdin Sync Exported Source Fallback READMEs

## Date Observed

2026-06-03

## Failure Type

Failed harness check and localization automation bug path.

## Goal

Crowdin synchronization should preserve localized README invariants that are
part of the repository source of truth, including:

- each localized README's language switcher highlighting its own language
- required `/harness review` command table entries
- the English adoption prompt blocks that intentionally stay untranslated

## What Happened Or Was Tried

After fixing the README filename mapping, the Crowdin workflow generated a
translation PR that touched the expected files:

- `README.ko.md`
- `README.ja.md`
- `README.zh-CN.md`

However, the manual `Harness Check` run for that PR failed. The downloaded
localized README files reset the language switcher to the English source form
and changed command table formatting enough to break repository hygiene tests.

## Why It Failed

- The workflow uploaded `README.md` as a source but did not upload the existing
  localized README files into Crowdin first.
- A new or under-seeded Crowdin project can export source-English fallback
  content for untranslated target strings.
- The repository has localized README sections that are intentionally
  file-specific and cannot be derived from the English source README alone.

## Current Replacement

`.github/workflows/crowdin-sync.yml` now sets `upload_translations: true` so the
existing localized README files are uploaded to Crowdin before translations are
downloaded. This treats the repository's current localized READMEs as the
source of truth when seeding a Crowdin project.

Regression coverage lives in `tests/test_repository_hygiene.py`.

## Detection Or Prevention Check

`tests/test_repository_hygiene.py` checks that the Crowdin workflow keeps
`upload_translations: true` and that `docs/validation.md` documents seeding from
existing localized README files. The `Harness Check` CI gate catches generated
README output that breaks language switcher or `/harness review` invariants.

## Agent Guidance

Do not disable `upload_translations` for README localization unless the Crowdin
project is already seeded and the replacement workflow includes another
explicit seeding or approval gate. After any Crowdin workflow change, run the
Crowdin sync and then run `Harness Check` against the generated localization PR
before merging translation output.
