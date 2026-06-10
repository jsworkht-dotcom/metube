# Clean Package Generator Contract Addendum

## Purpose

Y-06W adds a docs-only contract addendum for a future clean package generator.
It uses the Y-06V notice source index and existing notice / inventory source
drafts as future dry-run and preview inputs.

This addendum does not implement a generator, create package files, copy notice
or license text, generate guide output, build, package, install, change
dependencies, change backend/frontend code, change Docker/CI, or approve actual
distribution.

## Sources Checked

Read-only sources checked for this addendum:

- `docs/llmwiki/package-notices/notice-source-index.source.md`
- `docs/llmwiki/clean-package-dry-run-contract.md`
- `docs/llmwiki/license-notice-plan.md`
- `docs/llmwiki/codex-automation-policy.md`
- `docs/llmwiki/safety-boundaries.md`
- `scripts/clean_package_dry_run.py`
- `scripts/check_repo_safety.py`

No external references are required for this docs-only contract addendum.

## Facts / Assumptions / Needs Verification

Facts:

- `notice-source-index.source.md` is source material only.
- The clean-package dry-run script is report-only and currently emits a
  sanitized text report.
- The repo safety checker is report-only and classifies docs-only LLMwiki work
  as Low or High-low when no blockers are present.
- `動画保存ツール_ローカル専用/` must not exist during docs-only or dry-run-only
  work.
- Upstream PR #1001 files must not be mixed into fork-only work.

Assumptions:

- A future generator will first gain preview/report behavior before any actual
  generation command is approved.
- The notice source index can be used as a review map, not as final legal
  approval.
- Future reports should remain package-relative and sanitized.

Needs verification before any implementation:

- Exact generator command names and output modes.
- Exact package input artifacts, source commit, and OS-specific runtime
  selections.
- Exact license text, notice text, versions, source URLs, and source-offer
  requirements for selected artifacts.
- Whether preview output should be text only, JSON, Markdown, or a combination.

## Addendum Scope

Allowed by this addendum:

- Treat the notice source index as a future generator input candidate.
- Define dry-run and preview checks for notice, license, manifest, guide notice,
  developer review, diff prediction, manifest preview, cleanup, and rollback
  review.
- Define no-generation and generated-artifact exclusion rules.
- Define human review gates before actual generation.
- Clarify High-low / High-mid / High-high boundaries for future package work.
- Outline future implementation phases.

Not allowed by this addendum:

- Creating `動画保存ツール_ローカル専用/`.
- Creating notice bundles, license bundles, dependency inventories, manifests,
  or guide HTML/TXT output.
- Copying license text.
- Running build, package, install, dependency install/update, Docker image
  retrieval/build, or package manager commands.
- Changing backend, frontend, Docker, CI, package, or lockfile files.
- Reading, printing, storing, transforming, or handling real cookie, token,
  secret, credential, private URL, or private config values.
- Touching upstream PR #1001 files.
- Adding public hosting, ads, monetization, or external-user service behavior.
- Implementing a High-mid generator body.
- Implementing 更新適用機能.

## Notice Source Index As Generator Input Candidate

A future clean package generator preview may read:

```text
docs/llmwiki/package-notices/notice-source-index.source.md
```

The source index may be used to:

- discover reviewed notice, license, manifest, and inventory source drafts;
- map source drafts to future package-relative output candidates;
- identify unresolved package-time review items;
- keep review status vocabulary consistent;
- keep beginner-facing notice copy short and separate from developer material.

Rules:

- The source index is an input map only.
- The source index does not approve generated output.
- The generator must not copy from generated package output back into source.
- The generator must keep package-relative paths separate from repository paths.
- Legal and redistribution review remains package-time human review.

## Dry-Run / Preview Checks

Future dry-run or preview output should report these items before generation is
approved:

- source commit and branch used for preview;
- notice source index presence and review status;
- source draft presence for MeTube, yt-dlp, FFmpeg, Python runtime, frontend
  dependencies, desktop shell, and bundled Python dependencies;
- expected aggregate notice outputs;
- expected license output roots and component license candidates;
- expected manifest outputs and manifest field completeness;
- expected beginner guide notice section placement;
- expected developer review checklist items;
- missing source drafts, missing package paths, or unresolved review statuses;
- OS-specific runtime notice differences for Windows and macOS;
- package output before/after diff prediction candidate;
- package manifest preview candidate;
- cleanup / rollback candidate;
- blocker state for generated package folder presence;
- blocker state for PR #1001 file leakage;
- blocker state for forbidden path, filename, and content pattern families;
- sanitized safety flags.

Preview reports must not create or modify files. A passing preview is not
approval to generate package output.

## Future Output Mapping

### NOTICE.txt

Future preview mapping should include:

```text
開発者向け/notices/NOTICE.txt
開発者向け/notices/third-party-notices.txt
Windows用/notices/runtime-notices.txt
Mac用/notices/runtime-notices.txt
```

Rules:

- Aggregate notices must preserve component-level traceability.
- OS-specific runtime notices must include only pieces present in that OS
  package.
- Missing component notices should be warnings in preview, then blockers before
  actual generation.

### LICENSES/

Future preview mapping should include:

```text
開発者向け/licenses/
開発者向け/licenses/MeTube-LICENSE.txt
開発者向け/licenses/third-party/
開発者向け/licenses/third-party/yt-dlp-LICENSE.txt
開発者向け/licenses/third-party/ffmpeg-LICENSE.txt
開発者向け/licenses/third-party/python-runtime-LICENSE.txt
開発者向け/licenses/third-party/python-dependencies/
開発者向け/licenses/third-party/frontend/
開発者向け/licenses/third-party/desktop-shell/
```

Rules:

- Preview may list license path candidates.
- Preview must not copy full license bodies.
- Exact license body source and component version must remain review items until
  package-time human review.

### manifest.json

Future preview mapping should include:

```text
開発者向け/manifest/license-notice-manifest.json
開発者向け/manifest/planned-output-manifest.json
```

Candidate preview fields:

```text
schema_version
package_name
source_commit
review_status
component_name
component_kind
source_path
source_url
package_notice_path
package_license_path
inventory_path
target_os
target_arch
requires_source_offer
requires_attribution
requires_review
review_notes
```

Rules:

- Manifest preview must use repository-relative or package-relative paths only.
- Manifest preview must not include private local paths, submitted media URLs,
  cookies, tokens, secrets, credentials, or private config values.
- `review_status` must remain non-final until a later package-time review.

### Beginner Guide Notice Section

Future preview should confirm a short beginner notice pointer for:

```text
00_最初に開いてください.html
00_最初に開いてください.txt
困ったとき/
開発者向け/README.md
```

Rules:

- Beginner guide notice copy must stay short.
- Long license text belongs in developer-facing material only after a later
  approved notice-bundle task.
- Beginner copy must not imply public redistribution readiness.

### Developer Review Checklist

Future preview should include developer review checklist candidates for:

- source commit and fork-local modification notes;
- exact package artifacts and selected runtime files;
- FFmpeg provider, version, build configuration, and source access;
- Python runtime artifact, standard-library notices, and native library notes;
- Python dependency inventory tied to exact bundled versions;
- frontend build artifacts, source map decision, fonts, icons, and styles;
- desktop shell choice and runtime payload only if implemented later;
- package-relative notices, licenses, inventories, and manifests;
- no-private-data review.

## No-Generation Boundary

This addendum authorizes only documentation, dry-run planning, and preview
contract work.

A future dry-run / preview must not:

- create `動画保存ツール_ローカル専用/`;
- create or copy files into package output paths;
- generate notice bundles, license bundles, dependency inventories, manifests,
  or guide HTML/TXT output;
- run build, package, install, dependency install/update, or Docker commands;
- change backend, frontend, Docker, CI, package, or lockfile files;
- treat a passing preview as permission to generate package files.

Actual generation requires a later explicit task and human review gate.

## Generated Artifact Exclusion Rule

Generated artifacts must be excluded from source-only, docs-only, report-only,
and dry-run-only work.

The future generator preview must block or stop if it detects:

- an existing `動画保存ツール_ローカル専用/` folder in the repository root;
- changed files inside the generated package root;
- generated notice, license, inventory, manifest, HTML, TXT, ZIP, package, or
  installer output in the diff;
- package output mixed with docs-only or dry-run-only work.

## Secret / Token / Cookie Non-Disclosure Rule

Reports must never print real cookie, token, secret, credential, private URL,
submitted media URL, private local path, or private config values.

If a future preview detects a forbidden content pattern, it should report only:

```text
path
line number when safe
pattern family
sanitized message
```

The matched value must be omitted. Explanatory safety prose may mention these
families, but not real values.

## Diff Prediction Candidate

Future dry-run / preview may include a package output before/after diff
prediction candidate without creating files.

Candidate fields:

```text
predicted_added_paths
predicted_changed_paths
predicted_removed_paths
predicted_generated_paths
predicted_excluded_paths
predicted_blockers
prediction_inputs
```

Rules:

- Prediction must use package-relative paths.
- Prediction must state that no filesystem changes were made.
- Prediction must flag any generated output that would require human approval.

Y-06Y implementation note:

- `scripts/clean_package_dry_run.py` now prints this as a text-only
  `Package output diff prediction` section.
- The prediction reports future package root, would-create path candidates,
  source group candidates, future output candidates, excluded path summary,
  no-files-generated state, and human review requirement before generation.
- It does not create `manifest.json`, `NOTICE.txt`, `LICENSES/`, the package
  root, or any package file.

## Package Manifest Preview Candidate

Future dry-run / preview may include a package manifest preview candidate
without writing `manifest.json`.

Candidate fields:

```text
package_relative_path
source_candidate
kind
target_os
target_arch
generated
license_notice_required
review_status
safety_notes
```

Rules:

- `generated` may describe a future planned output, but must not mean the file
  was created.
- Missing required source candidates should remain warnings in preview and
  become blockers before actual generation.
- Manifest preview must include enough context for human review without
  exposing private values.

Y-06X implementation note:

- `scripts/clean_package_dry_run.py` now prints this as a text-only
  `Package manifest preview` section.
- The preview reports source counts and candidate future outputs only.
- It does not create `manifest.json` or any package file.

## JSON Report Mode Design Candidate

Future dry-run / preview may include JSON output for local review tooling,
structured handoff data, and machine-readable package planning summaries.

Y-07A design note:

- `docs/llmwiki/clean-package-dry-run-json-report-mode-design.md` defines the
  JSON report mode design.
- The design keeps text output as the default.
- The design prefers `--format json` for the first future selector.
- The design requires one valid JSON object on stdout and no report-file
  writing in the first implementation.
- The design keeps repository-diff risk classification owned by
  `scripts/check_repo_safety.py` unless a later wrapper task explicitly
  combines reports.
- The design does not implement JSON output, write report files, create package
  output, or weaken existing blockers.

Y-07C implementation note:

- `scripts/clean_package_dry_run.py --format json` now prints one valid JSON
  object to stdout.
- The JSON report is machine-readable dry-run output only, not generated
  package output.
- Default text output, `--format text`, and `--format markdown` remain
  supported.
- The implementation does not write report files, create package output, or
  weaken existing blockers.

## Markdown Report Mode Design Candidate

Future dry-run / preview may include Markdown output for PR body reuse,
handoff reuse, and human review notes.

Y-06Z design note:

- `docs/llmwiki/clean-package-dry-run-markdown-report-mode-design.md` defines
  the Markdown report mode design.
- The design keeps text output as the default.
- The design prefers `--format markdown` for the first future selector.
- The design requires Summary, Status, Risk Classification, Package Manifest
  Preview, Package Output Diff Prediction, Notice / Guide Source Coverage,
  Excluded Paths Summary, Blockers, Warnings, Human Review Checklist, and
  No-Generation Boundary sections.
- The design does not implement Markdown output, write report files, create
  package output, or weaken existing blockers.

Y-07B implementation note:

- `scripts/clean_package_dry_run.py --format markdown` now prints a
  stdout-only Markdown report.
- Default text output and `--format text` remain supported.
- The Markdown report includes Summary, Status, Risk Classification, Package
  Manifest Preview, Package Output Diff Prediction, Notice / Guide Source
  Coverage, Excluded Paths Summary, Blockers, Warnings, Human Review
  Checklist, and No-Generation Boundary sections.
- The implementation does not write report files, create package output, or
  weaken existing blockers.

## Report Regression Contract

Y-07D fixes the regression contract for the current clean-package dry-run
report modes:

```text
docs/llmwiki/clean-package-dry-run-report-regression-contract.md
```

Future generator, preview, or report work must preserve:

- default text output;
- `--format text` output;
- `--format markdown` required sections;
- `--format json` one-object parseability and required top-level fields;
- shared warning/blocker classification;
- shared exit-code behavior;
- sanitized findings with no cookie/token/secret/credential values;
- no-generation behavior unless a later explicit human-reviewed task approves
  actual generation.

Y-07D is docs-only. It does not implement tests, change scripts, write report
files, create package output, or weaken existing blockers.

Y-07E implementation note:

- `scripts/check_clean_package_dry_run_reports.py` now provides stdlib-only
  checker coverage for the clean-package dry-run report modes.
- Future generator, preview, or report work should run this checker before PR
  creation and before merge when report modes are in scope.
- The checker validates text, Markdown, JSON, cross-format, and no-generation
  report invariants.
- The checker does not write report files, create package output, add CI
  wiring, or weaken existing blockers.

Actual clean-package generation remains a later human-reviewed task.

## Cleanup / Rollback Candidate

Future implementation planning should include cleanup and rollback candidates
before any actual generation step is approved.

Candidate cleanup / rollback checks:

- confirm no generated package root exists before generation begins;
- define the exact generated root to remove if a generation attempt is aborted;
- record generated path list before cleanup;
- keep cleanup scoped to the generated package root only;
- require human review before removing any non-generated source path;
- re-run repo safety and clean-package dry-run after cleanup.

No cleanup command is approved by this addendum.

## Human Review Gate Before Actual Generation

Actual generation must wait for a later explicit task and human review.

Before actual generation, a human reviewer must confirm:

- dry-run / preview output is sanitized and complete;
- package manifest preview is acceptable;
- package output diff prediction is acceptable;
- notice source index and source drafts are still current;
- exact artifacts, versions, source URLs, and license text have been reviewed;
- no generated package folder exists before generation begins;
- no backend/frontend/Docker/CI/package/lockfile changes are mixed in unless
  explicitly approved;
- no PR #1001 files are included;
- no cookie/token/secret/credential handling is introduced;
- local-only and personal-use boundaries remain intact.

## Risk Boundary

High-low:

- docs-only addenda, contract updates, dry-run report design, preview report
  design, manifest preview design, output diff prediction design, cleanup /
  rollback design, and report-only checker planning;
- auto PR / auto merge may proceed only when safety gates pass.

High-mid:

- implementation-adjacent generator prototypes, real generation scripts that do
  not run generation, package output staging logic, generated artifact cleanup
  scripts, or launcher / desktop shell adjacent prototypes;
- PR-ready handoff is allowed only when the task explicitly approves High-mid
  scope;
- auto merge is prohibited and `human-review-required` must appear in the PR
  body.

High-high:

- actual package generation, generated distribution folder creation, ZIP /
  package / installer creation, dependency install/update, package or lockfile
  changes, Docker image retrieval/build, backend/frontend implementation changes,
  credential handling, public hosting, ads, or 更新適用機能;
- Codex must stop before implementation unless explicit human approval changes
  the task scope.

## Future Implementation Phases

Candidate phases, each requiring a separate explicit task:

1. Add report-only preview fields to `scripts/clean_package_dry_run.py`.
2. Add a package manifest preview mode that writes nothing. Completed by Y-06X.
3. Add a package output diff prediction report that writes nothing. Completed
   by Y-06Y.
4. Add JSON or Markdown report output, still without writing package files.
   Markdown report mode is implemented by Y-07B. JSON report mode is
   implemented by Y-07C.
4a. Add docs-only report regression contract hardening for the current text,
    Markdown, and JSON modes. Completed by Y-07D.
4b. Add a lightweight stdlib-only checker for the current text, Markdown, and
    JSON report modes. Completed by Y-07E.
5. Add a human-reviewed generator prototype that can be inspected but does not
   run actual generation in automated checks.
6. Add actual generation only after human approval, clean dry-runs, reviewed
   license/notice inputs, and cleanup/rollback planning.

Each phase must preserve local-only personal-use scope and must not weaken
existing blockers.
