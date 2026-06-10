# Clean Package Generation Readiness Checklist

## Purpose

Y-08E fixes the readiness checklist that must be reviewed before any later clean
package generation task.

Passing dry-run previews do not approve generation. Actual generation remains a
later explicit human-reviewed task. This PR is docs-only and does not implement
generation, generation previews, script changes, checker changes, CI wiring, or
package output.

## Current Preview Baseline

The current report-only baseline includes:

- text, Markdown, and JSON clean-package dry-run reports;
- a report regression checker;
- manifest entry preview data;
- output group preview data;
- source coverage status preview data;
- generated package folder absence checks;
- no actual package generation implementation.

The generated package folder candidate remains:

```text
動画保存ツール_ローカル専用/
```

It must stay absent until a later explicitly approved generation task.

## Non-Goals

Y-08E does not:

- change scripts;
- add tests;
- add CI;
- write report files;
- generate package files;
- create `動画保存ツール_ローカル専用/`;
- generate `manifest.json`;
- generate `NOTICE.txt`;
- generate `LICENSES/`;
- generate guide HTML/TXT output;
- generate inventory output;
- copy license text;
- select runtime binaries;
- select desktop shell implementation;
- build, package, or install;
- install or update dependencies;
- run container image retrieval or Docker build;
- change backend/frontend/Docker/CI/package/lockfile files;
- touch upstream PR #1001 files;
- handle cookie/token/secret values;
- add public hosting or ads;
- add 更新適用機能.

## Readiness Gate Summary

Generation readiness is blocked until all gates pass:

1. report mode gates
2. source coverage gates
3. manifest preview gates
4. output diff prediction gates
5. notice/license/inventory gates
6. beginner guide gates
7. runtime/desktop shell gates
8. security/privacy gates
9. cleanup/rollback gates
10. human review gate

Any failed gate stops the generation task. A passing checklist is still only a
readiness signal; actual generation requires explicit human approval for that
later task.

## Required Passing Reports

Before any generation implementation or generation run, these commands must pass:

```powershell
git diff --check
python scripts/check_repo_safety.py
python scripts/check_repo_safety.py --base fork/master
python scripts/check_clean_package_dry_run_reports.py
python scripts/clean_package_dry_run.py
python scripts/clean_package_dry_run.py --format text
python scripts/clean_package_dry_run.py --format markdown
python scripts/clean_package_dry_run.py --format json
```

If `python` is unavailable, the bundled Codex Python executable may be used. Do
not install Python to satisfy this gate.

## Required Source Coverage

Before generation:

- guide sources must be present as source drafts;
- notice sources must be present as source drafts or review candidates;
- license sources must be reviewed before generation;
- inventory sources must be reviewed before generation;
- runtime selections must be explicit before generation;
- desktop shell selection must be explicit before generation;
- package-time review required items must be resolved or explicitly accepted by
  human review.

Missing source material may remain acceptable for report-only previews, but it
must not be silently carried into actual generation.

## Required Manifest Preview Readiness

Before generation:

- `manifest_entries` must be complete enough for the selected package stage;
- every generated future output must have a package-relative path;
- every entry must have source/review status;
- every entry must be reviewed for local-only scope;
- `generated` in preview must not be treated as a created-file claim;
- `human_review_required` remains true until explicit approval.

## Required Output Diff Prediction Readiness

Before generation:

- `output_groups` must show planned created directories and files;
- excluded outputs must remain excluded;
- cleanup/rollback candidates must be reviewed;
- no generated root may exist before generation starts;
- output diff must not include upstream PR #1001 files;
- output diff must not include secrets, cookies, tokens, logs, caches,
  downloads, state, or private env files.

## Notice / License / Inventory Readiness

Before generation:

- exact component versions must be known;
- exact license text sources must be selected;
- notice text must be reviewed;
- legal final must not be claimed unless reviewed;
- source-offer requirements, if any, must be reviewed;
- bundled Python dependency inventory must be tied to exact bundled versions;
- frontend dependency inventory must be tied to exact bundled build artifacts;
- FFmpeg provider, version, and build configuration must be reviewed;
- Python runtime artifact must be reviewed;
- desktop shell license/runtime pieces must be reviewed only after shell
  selection.

## Beginner Guide Readiness

Before generation:

- HTML guide sources are reviewed;
- TXT fallback sources are reviewed;
- local-only / personal-use boundary is visible;
- no Docker/Git/Python/Node jargon appears in the beginner flow;
- no cookie/token/secret instructions appear;
- no DRM/auth/restriction bypass instructions appear;
- no public hosting or ads language appears;
- Windows/macOS warning language is safe and does not normalize bypassing
  protections;
- stop/quit and save folder guidance is clear.

## Runtime / Desktop Shell Readiness

Before generation:

- Windows runtime selection is explicit;
- macOS runtime selection is explicit;
- FFmpeg binary/provider is explicit;
- Python runtime packaging approach is explicit;
- desktop shell selection is explicit, or the task remains limited to
  docs/preview only;
- signing/notarization status is not overstated;
- no `.exe`, `.app`, or runtime artifact is claimed until selected and
  reviewed.

## Security And Privacy Readiness

Before generation:

- no cookie/token/secret handling;
- no private env files;
- no submitted video URLs;
- no local downloads/state/logs/temp/cache files;
- no public hosting;
- no ads or monetization;
- no mass-download optimization;
- no DRM/auth/restriction bypass;
- no upstream PR #1001 files;
- generated output stays local-only / personal-use.

## Generated Artifact Readiness

Before actual generation:

- `動画保存ツール_ローカル専用/` must not already exist;
- output root must be explicit;
- generated path list must be previewed;
- cleanup path must be scoped only to the generated root;
- no source paths may be removed by cleanup;
- no output ZIP/package/installer may be created without separate approval.

## Cleanup / Rollback Readiness

Before generation:

- abort cleanup candidate is documented;
- generated-root-only cleanup boundary is documented;
- non-generated source cleanup is prohibited;
- post-cleanup safety gates are documented;
- rollback remains revert/cleanup only until actual generation design exists.

## Human Review Gate

Human review must explicitly confirm:

```text
dry-run reports reviewed
regression checker passes
manifest entries reviewed
output groups reviewed
source coverage reviewed
notice/license/inventory status reviewed
beginner guide status reviewed
runtime/desktop shell status reviewed
security/privacy boundary reviewed
cleanup/rollback boundary reviewed
actual generation scope approved
```

Actual generation remains blocked unless this human review is explicit for the
later generation task.

## Stop Conditions

Stop if any of these occur:

- checker blocked or failed;
- dry-run blocked;
- repo safety blocked;
- generated package folder exists;
- upstream PR #1001 files appear;
- backend/frontend/Docker/CI/package/lockfile changes appear without explicit
  scope;
- scripts changed in this docs-only task;
- cookie/token/secret values appear;
- report file output appears;
- package output appears;
- dependency install/update is required;
- container image retrieval or Docker build is required;
- any future generation task lacks explicit human approval.

## Future Report-Only Implementation Candidate

Do not implement now.

Future candidate:

```text
Y-08F:
  add generation readiness checklist preview to clean_package_dry_run.py
```

Y-08F should be report-only, stdout-only, no-generation, and checker-backed.

## High-low / High-mid / High-high Boundary

High-low:

- docs-only generation readiness checklist;
- report-only readiness preview design;
- no script changes;
- no generated output.

Medium / High-low future:

- report-only readiness checklist implementation;
- checker update for readiness fields;
- no generated files;
- no dependency changes.

High-mid:

- generator prototype script;
- generated-root cleanup script;
- package output staging logic;
- report file writing.

High-high:

- actual package generation;
- ZIP/package/installer creation;
- dependency install/update;
- container image retrieval or Docker build;
- backend/frontend/package/lockfile changes;
- cookie/token/secret handling;
- public hosting/ads;
- 更新適用機能.

## Recommended Next Step

Recommended next candidate:

```text
Y-08F implement generation readiness checklist preview in report-only mode
```

Actual package generation remains blocked.

## Verification Checklist

For this docs-only task:

- `git diff --check`
- `python scripts/check_repo_safety.py`
- `python scripts/check_repo_safety.py --base fork/master`
- `python scripts/check_clean_package_dry_run_reports.py`
- `python scripts/clean_package_dry_run.py`
- `python scripts/clean_package_dry_run.py --format text`
- `python scripts/clean_package_dry_run.py --format markdown`
- `python scripts/clean_package_dry_run.py --format json`
- Confirm `動画保存ツール_ローカル専用/` is absent.
- Confirm changed files are approved docs only.

## Rollback / Cleanup Note

Rollback is a docs-only revert of the Y-08E checklist commit.

No generated package output exists to clean up.
