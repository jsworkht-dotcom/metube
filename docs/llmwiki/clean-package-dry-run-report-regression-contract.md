# Clean Package Dry-Run Report Regression Contract

## Purpose

Y-07D fixes the regression contract for the clean-package dry-run report modes:

```text
python scripts/clean_package_dry_run.py
python scripts/clean_package_dry_run.py --format text
python scripts/clean_package_dry_run.py --format markdown
python scripts/clean_package_dry_run.py --format json
```

The purpose is to make future changes preserve the text, Markdown, and JSON
report behavior added through Y-07B and Y-07C.

This document is docs-only. It does not implement tests, change scripts, write
report files, or create package output.

## Current Report Modes

- Default output is a human-readable text report.
- `--format text` is a human-readable text report.
- `--format markdown` is a Markdown report on stdout.
- `--format json` is one valid JSON object on stdout.

All modes are report-only and dry-run-only.

## Non-Goals

Y-07D does not:

- change `scripts/clean_package_dry_run.py`;
- change `scripts/check_repo_safety.py`;
- add tests;
- add CI;
- add report file writing;
- generate package files;
- create `動画保存ツール_ローカル専用/`;
- create `manifest.json`, `NOTICE.txt`, or `LICENSES/`;
- generate notice, license, inventory, manifest, or guide output;
- change backend, frontend, Docker, CI, package, or lockfile files;
- handle cookie, token, secret, credential, private env, or private config
  values;
- touch upstream PR #1001 files;
- add 更新適用機能.

## Regression Invariants

Future changes must preserve these invariants:

- Default output remains text and must not look like JSON.
- `--format text` remains text and must not look like JSON.
- `--format markdown` includes the required Markdown sections.
- `--format json` parses with `json.loads()` as one dict/object over the
  entire stdout.
- JSON output includes the required top-level fields.
- Warning and blocker classification does not differ across formats.
- Exit-code behavior does not differ across formats.
- Clean repo expected status remains OK.
- No generated artifacts are created by any format.
- No format writes a report file unless a later explicit task approves a report
  file contract.

## Text Report Contract

Text output is the default compatibility surface.

Required behavior:

- `python scripts/clean_package_dry_run.py` prints text.
- `python scripts/clean_package_dry_run.py --format text` prints text.
- Text output must preserve the meaning of the current package root, status,
  repository, planned entries, preview sections, checks, warnings, blocked
  reasons, safety flags, and no-files-generated closing note.
- Text output must not start with `{`.
- Text output must not require JSON or Markdown parsing.

## Markdown Report Contract

Markdown output is for human review, PR body reuse, and handoff reuse.

Required sections:

```text
# Clean Package Dry-Run Report
## Summary
## Status
## Risk Classification
## Package Manifest Preview
## Package Output Diff Prediction
## Notice / Guide Source Coverage
## Excluded Paths Summary
## Blockers
## Warnings
## Human Review Checklist
## No-Generation Boundary
```

Markdown output must remain stdout-only and report-only.

## JSON Report Contract

JSON output is for local structured review and future lightweight checks.

Required behavior:

- stdout contains exactly one valid JSON object followed by a newline;
- no text preamble appears before `{`;
- no Markdown headings appear in JSON mode;
- `json.loads()` over the entire stdout returns a dict/object;
- warning and blocker arrays contain sanitized objects only.

Required top-level fields:

```text
schema_version
report_type
report_format
mode
status
exit_code
generated_artifacts
checked_at
repository
package
package_manifest_preview
package_output_diff_prediction
source_coverage
excluded_paths_summary
validation
warnings
blockers
safety_flags
human_review
next_step
```

## Cross-Format Consistency Rules

These values should stay consistent across text, Markdown, and JSON:

- status;
- warning count;
- blocker count;
- package root candidate;
- notice source coverage;
- guide source coverage;
- generated_artifacts / no_files_generated;
- human_review_required_before_generation.

If a future change intentionally changes one of these values, it must update the
script contract and this regression contract in the same reviewed task.

## Exit Code Contract

Exit codes:

```text
0: OK
1: blockers found
2: CLI usage error
```

No report format may change this behavior.

## Warning / Blocker Contract

Warnings and blockers are shared dry-run findings, not per-format findings.

Rules:

- Formats may render findings differently, but classification must stay the
  same.
- A warning in text must not become a blocker in Markdown or JSON.
- A blocker in JSON must also be represented as blocked in text and Markdown.
- Clean repo expectation is warnings none and blockers none.
- Existing blockers must not be weakened.

## Sanitization Contract

Reports must never print real:

- cookie values;
- token values;
- secret values;
- credential values;
- private env values;
- submitted media URLs;
- private config values.

Secret-like findings must report only:

- path;
- line number when safe;
- pattern family;
- sanitized message.

Matched secret, cookie, token, credential, URL, or private config values must be
omitted.

## No-Generation Boundary

All report modes remain no-generation modes.

They must not:

- create `動画保存ツール_ローカル専用/`;
- create `manifest.json`;
- create `NOTICE.txt`;
- create `LICENSES/`;
- create ZIP, package, installer, or generated guide output;
- copy source files into a package root;
- write report files;
- run build, package, install, dependency update, Docker image retrieval, or
  Docker build
  commands.

## Verification Matrix

Manual verification commands for future report-mode changes:

```powershell
git diff --check
python scripts/check_repo_safety.py
python scripts/check_repo_safety.py --base fork/master
python scripts/clean_package_dry_run.py
python scripts/clean_package_dry_run.py --format text
python scripts/clean_package_dry_run.py --format markdown
python scripts/clean_package_dry_run.py --format json
```

JSON parse check:

```powershell
$json = python scripts/clean_package_dry_run.py --format json
$json | python -c "import json,sys; data=json.load(sys.stdin); assert isinstance(data, dict); print('json parse ok')"
```

Markdown section check:

```powershell
$md = python scripts/clean_package_dry_run.py --format markdown
$required = @(
  "# Clean Package Dry-Run Report",
  "## Summary",
  "## Status",
  "## Risk Classification",
  "## Package Manifest Preview",
  "## Package Output Diff Prediction",
  "## Notice / Guide Source Coverage",
  "## Excluded Paths Summary",
  "## Blockers",
  "## Warnings",
  "## Human Review Checklist",
  "## No-Generation Boundary"
)
foreach ($item in $required) {
  if ($md -notmatch [regex]::Escape($item)) {
    throw "Missing Markdown section: $item"
  }
}
```

Text regression check:

```powershell
$default = python scripts/clean_package_dry_run.py
$text = python scripts/clean_package_dry_run.py --format text

if ($default.TrimStart().StartsWith("{")) {
  throw "default output unexpectedly looks like JSON"
}
if ($text.TrimStart().StartsWith("{")) {
  throw "--format text unexpectedly looks like JSON"
}
```

No generated folder check:

```powershell
Test-Path "動画保存ツール_ローカル専用"
```

Expected:

```text
False
```

## Future Test Implementation Candidate

Possible future task:

```text
Y-07E:
  add lightweight regression tests or script self-checks for dry-run report modes
```

Possible future test forms:

- stdlib-only Python unit tests for `clean_package_dry_run.py` helpers;
- small script-level smoke checks;
- docs-only checklist first, implementation later;
- no package generation during tests.

Y-07D does not implement these tests.

## Y-07E Lightweight Checker Implementation

Y-07E implements the first lightweight checker for this contract:

```text
scripts/check_clean_package_dry_run_reports.py
```

The checker is stdlib-only and report-only.

It runs:

```text
python scripts/clean_package_dry_run.py
python scripts/clean_package_dry_run.py --format text
python scripts/clean_package_dry_run.py --format markdown
python scripts/clean_package_dry_run.py --format json
```

It validates:

- default output remains text;
- `--format text` remains text;
- current default and `--format text` output are identical;
- Markdown includes the required sections;
- JSON parses as one object over the full stdout;
- JSON includes the required top-level fields;
- key JSON values match the dry-run clean-repo expectation;
- simple cross-format status, warning, and blocker consistency holds;
- `動画保存ツール_ローカル専用/` is absent.

The checker prints a sanitized human-readable report and does not print full
mode stdout on failure.

Y-07E does not:

- write output files;
- create temp files;
- create package folders;
- create package output;
- change `scripts/clean_package_dry_run.py`;
- change `scripts/check_repo_safety.py`;
- add CI wiring;
- approve actual package generation.

## PR Review Checklist

Before merging future report-mode changes, confirm:

- changed files are inside the approved task scope;
- `scripts/check_clean_package_dry_run_reports.py` passes when report modes are
  in scope;
- `scripts/check_repo_safety.py` has no blockers;
- `scripts/check_repo_safety.py --base fork/master` has no blockers;
- `scripts/clean_package_dry_run.py` has no blockers;
- default text output remains text;
- `--format text` remains text;
- `--format markdown` includes the required sections;
- `--format json` parses as one JSON object;
- JSON includes the required top-level fields;
- no generated package folder exists;
- no backend, frontend, Docker, CI, package, or lockfile files are mixed in;
- upstream PR #1001 files are absent;
- no cookie, token, secret, credential, private env, private config, or
  submitted media URL values are printed.

## Stop Conditions

Stop and report facts if any of these occur:

- `scripts/check_repo_safety.py` reports BLOCKED;
- `scripts/clean_package_dry_run.py` reports BLOCKED;
- changed files are outside approved scope;
- script changes appear in a docs-only task;
- backend, frontend, Docker, CI, package, or lockfile files changed outside an
  explicitly approved task;
- generated package folder exists;
- upstream PR #1001 files appear;
- cookie, token, secret, credential, private env, private config, or submitted
  media URL values appear;
- report file writing is added without explicit approval;
- package output is generated;
- dependency install/update is required;
- Docker image retrieval/build is required.

## Rollback / Cleanup Note

For Y-07D, rollback is a docs-only revert of this contract and synchronized
LLMwiki references.

No generated package output exists to clean up.

## High-low / High-mid Boundary

High-low:

- docs-only report regression contract;
- report-only verification checklist;
- no script changes;
- no generated output.

Medium / High-low future:

- lightweight stdlib tests that only parse stdout;
- no generated files;
- no dependency changes.

High-mid:

- report file writing;
- generated output staging checks;
- package output cleanup scripts;
- generator-adjacent implementation.

High-high:

- actual package generation;
- ZIP, package, or installer creation;
- dependency install/update;
- Docker image retrieval/build;
- backend, frontend, package, or lockfile changes;
- cookie/token/secret handling;
- public hosting or ads;
- 更新適用機能.
