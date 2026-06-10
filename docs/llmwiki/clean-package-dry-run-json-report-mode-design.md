# Clean Package Dry-Run JSON Report Mode Design

## Purpose

Y-07A defines a docs-only design for a future JSON report mode in
`scripts/clean_package_dry_run.py`.

The goal is to preserve the current text report while designing a structured
machine-readable shape that future local review tools, PR checklists, or
handoff notes can parse without changing the dry-run safety boundary.

This document is design material only. It does not implement JSON output,
does not change the dry-run script, does not write report files, and does not
create package output.

## Current Inputs

Read-only context checked for this design:

- `scripts/clean_package_dry_run.py`
- `scripts/check_repo_safety.py`
- `docs/llmwiki/clean-package-dry-run-contract.md`
- `docs/llmwiki/clean-package-generator-contract-addendum.md`
- `docs/llmwiki/clean-package-dry-run-markdown-report-mode-design.md`
- `docs/llmwiki/codex-automation-policy.md`
- `docs/llmwiki/handoff.md`
- `docs/llmwiki/roadmap.md`

Current dry-run text sections to preserve in structured form:

- package root;
- status;
- repository branch and commit;
- planned entries;
- planned Windows entries;
- planned macOS entries;
- planned developer entries;
- package manifest preview;
- package output diff prediction;
- excluded rules and currently-present excluded paths;
- checks;
- warnings;
- blocked reasons;
- safety flags;
- no-files-generated closing line.

## Facts / Assumptions / Needs Verification

Facts:

- `scripts/clean_package_dry_run.py` currently accepts `--format text` only.
- The current default output is human-readable text on stdout.
- The current script does not write report files.
- Existing status semantics are `Status: OK` or `Status: BLOCKED`.
- Existing exit codes are `0` for OK, `1` for blocked, and `2` for usage
  errors.
- `scripts/check_repo_safety.py` owns repository-diff risk classification.
- Upstream PR #1001 files must stay out of fork-only package work.

Assumptions:

- The first future JSON mode should reuse the existing collected dry-run data.
- JSON output consumers will prefer stable keys, arrays, booleans, and simple
  string enums over prose parsing.
- JSON output is for local review and automation input, not for public
  publishing.

Needs verification before implementation:

- Exact schema version value and compatibility policy.
- Whether any consumer needs a wall-clock timestamp.
- Whether risk classification should be injected from a separate
  `scripts/check_repo_safety.py` run or left explicitly out of scope.
- Whether report-file writing is ever needed. It is not approved by this
  design.

## Non-Goals

Y-07A does not:

- change `scripts/clean_package_dry_run.py`;
- change `scripts/check_repo_safety.py`;
- add JSON output;
- add Markdown output;
- add report-file output;
- create `manifest.json`, `NOTICE.txt`, or `LICENSES/`;
- create `動画保存ツール_ローカル専用/`;
- copy package files;
- generate notice bundles, license bundles, inventories, manifests, or
  HTML/TXT guide output;
- ビルド、パッケージ、インストール、dependency、Docker、backend、
  frontend、CI に関する実行系操作を追加する;
- change package or lock files;
- handle cookie/token/secret values;
- touch upstream PR #1001 files;
- add automation wrapper, CI integration, PR comment automation, or merge
  policy behavior;
- add High-mid implementation work;
- add 更新適用機能.

## Output Mode Candidates

Preferred future CLI candidate:

```text
python scripts/clean_package_dry_run.py --format json
```

Reasons:

- The script already has `--format text`.
- Y-06Z already recommends `--format markdown` for the future Markdown mode.
- `text`, `json`, and `markdown` can share one report selector.
- `text` can remain the default without adding a second mode selector.

Alternative future CLI candidate:

```text
python scripts/clean_package_dry_run.py --json
```

Tradeoffs:

- Short and familiar for command-line users.
- Larger future CLI surface because it overlaps with `--format`.
- Harder to extend consistently if Markdown is later implemented.

Recommendation:

- Keep default output as text.
- Prefer `--format json` for the first JSON implementation.
- Do not write report files in the first JSON implementation.
- Keep JSON output on stdout only unless a later explicit task approves a
  report-file path contract.
- Keep stdout valid JSON only in JSON mode; do not print a human-readable
  preamble or trailing note outside the JSON object.

## Proposed Top-Level Object

The first JSON mode should use one top-level object.

Candidate top-level keys:

```text
schema_version
report_kind
report_format
mode
status
exit_code
repository
package
planned_entries
package_manifest_preview
package_output_diff_prediction
excluded_paths
checks
warnings
blocked_reasons
safety_flags
risk_classification
no_generation_boundary
next_step
```

Suggested top-level constants:

```json
{
  "schema_version": "0.1",
  "report_kind": "clean_package_dry_run",
  "report_format": "json",
  "mode": "dry_run"
}
```

Status rules:

- JSON `status` should use a stable lower-case enum: `ok` or `blocked`.
- `exit_code` should preserve existing dry-run behavior: `0`, `1`, or `2`.
- If a display string is needed later, it should be derived from `status`
  rather than stored as a second source of truth.

Timestamp rule:

- The first implementation should avoid a wall-clock field unless a consumer
  explicitly needs it.
- If `checked_at` is added later, use ISO 8601 UTC and document that it is
  intentionally nondeterministic.

## Proposed Object Shape

Illustrative shape only:

```json
{
  "schema_version": "0.1",
  "report_kind": "clean_package_dry_run",
  "report_format": "json",
  "mode": "dry_run",
  "status": "ok",
  "exit_code": 0,
  "repository": {
    "branch": "master",
    "commit": "de1e2b0"
  },
  "package": {
    "root": "動画保存ツール_ローカル専用/",
    "local_only": true,
    "generated_artifacts": false
  },
  "planned_entries": {
    "top_level": [],
    "windows": [],
    "macos": [],
    "developer": []
  },
  "warnings": [],
  "blocked_reasons": [],
  "safety_flags": {
    "local_only": true,
    "public_hosting": false,
    "ads": false,
    "update_apply": false,
    "docker_pull": false,
    "git_update": false,
    "package_install": false,
    "credential_handling": false,
    "generated_folder_created": false
  },
  "no_generation_boundary": {
    "files_generated": false,
    "files_copied": false,
    "package_root_created": false
  },
  "next_step": "Review the dry-run report; do not generate package files yet."
}
```

Rules:

- Examples may omit long arrays for readability, but implementation output
  should include the same information as the text report.
- Object keys should remain snake_case.
- Arrays should preserve the existing text report order where ordering helps
  review.
- Missing optional data should use `null`, `[]`, or an explicit status string
  rather than omitting required keys unpredictably.

## Repository Object

Purpose:

- Preserve current branch and commit information.
- Avoid printing private local filesystem values.

Candidate fields:

```text
branch
commit
base
root_included
```

Rules:

- `branch` and `commit` should come from the same git reads as the text report.
- Repository root should be omitted by default or represented only as
  `root_included: false`.
- If a later task needs `repository_root`, it must document why the local path
  is needed and how private-path leakage is avoided.

## Package Object

Purpose:

- Preserve the future package root candidate and local-only package boundary.

Candidate fields:

```text
root
package_name_candidate
package_type_candidate
local_only
generated_artifacts
human_review_required_before_generation
legal_final
```

Rules:

- `root` remains `動画保存ツール_ローカル専用/`.
- `generated_artifacts` must be `false` in dry-run JSON output.
- `human_review_required_before_generation` must be `true`.
- `legal_final` must be `false` until a later package-time legal review.

## Planned Entries Object

Purpose:

- Preserve planned top-level, Windows, macOS, and developer entries.

Candidate fields:

```text
top_level
windows
macos
developer
```

Rules:

- Values should be arrays of package-relative path strings.
- The arrays should match the text report order.
- Planned paths must not imply that files were created.

## Package Manifest Preview Object

Purpose:

- Preserve the Y-06X package manifest preview in structured form.

Candidate fields:

```text
package_name_candidate
package_type_candidate
local_only
generated_artifacts
notice_sources
guide_sources
excluded_paths_summary
future_outputs
human_review_required_before_generation
legal_final
non_disclosure
no_generation_note
```

Suggested source item shape:

```text
label
path
present
```

Rules:

- Source paths must be repository-relative.
- Future output paths must be package-relative or short logical names.
- Secret/token/cookie non-disclosure fields should be booleans, not prose.
- Legal status must remain non-final.

## Package Output Diff Prediction Object

Purpose:

- Preserve the Y-06Y package output diff prediction in structured form.

Candidate fields:

```text
future_package_root
would_create_directories
would_create_files
would_copy_source_groups
would_generate_future_outputs
would_exclude_paths_summary
no_files_generated
human_review_required_before_generation
cleanup_rollback_candidate
```

Rules:

- Values should describe predicted package output only.
- The object must clearly state `no_files_generated: true`.
- Cleanup / rollback wording must remain a candidate note, not approval to
  delete files.

## Excluded Paths Object

Purpose:

- Preserve excluded path rules and currently-present excluded paths.
- Keep generated artifact and PR #1001 leakage checks reviewable.

Candidate fields:

```text
rules
currently_present
generated_package_root_present
pr_1001_leakage
forbidden_filename_status
secret_like_content_status
```

Rules:

- `rules` should contain the same rule strings as the text report.
- `currently_present` should contain repository-relative or rule-relative
  paths only.
- `pr_1001_leakage` should report status without including or touching
  `docker-compose.local.yml` or `docs/local-only.md`.

## Checks Object

Purpose:

- Preserve the current text `Checks` section in predictable key/value form.

Candidate fields:

```text
forbidden_paths
forbidden_filenames
secret_like_content
generated_package_folder
beginner_guides
guide_notice_source_warnings
windows_mac_sections
pr_1001_leakage
```

Rules:

- Status values should use small enums such as `ok`, `blocked`, `warning`,
  `planned`, `present`, and `not_present`.
- The JSON mode should not invent new blocker rules.
- Warning-only source coverage must remain warning-only unless a later task
  changes the contract.

## Findings Arrays

Warnings and blocked reasons should share one finding object shape.

Candidate finding fields:

```text
kind
path
line
pattern_family
message
severity
```

Rules:

- `path` must be repository-relative or package-relative.
- `line` should be `null` when not applicable.
- `pattern_family` should be `null` when not applicable.
- `severity` should be `warning` or `blocked`.
- Secret-like findings must not echo matched values.
- Cookie/token/secret/credential values must never appear in JSON.

Example sanitized finding:

```json
{
  "kind": "forbidden_content_pattern",
  "path": "example/config-template.txt",
  "line": 12,
  "pattern_family": "secret_like_assignment",
  "message": "A secret-like assignment was found. The value is intentionally omitted.",
  "severity": "blocked"
}
```

## Risk Classification Relationship

Purpose:

- Make the boundary between package dry-run status and repository safety status
  explicit.

Rules:

- `scripts/check_repo_safety.py` remains the source for repository-diff risk
  classification.
- The clean-package dry-run JSON mode must not compute a second, conflicting
  risk tier by default.
- If the dry-run runs alone, `risk_classification` should say that it is not
  included by the clean-package dry-run.
- A later wrapper may combine both reports only after an explicit task approves
  that wrapper.

Suggested standalone value:

```json
{
  "source": "not_included_by_clean_package_dry_run",
  "tier": null,
  "automation": null,
  "reason": "Run scripts/check_repo_safety.py separately for repository-diff risk classification."
}
```

## Safety Flags Object

Purpose:

- Preserve the current text safety flags and make unsafe behavior easy to
  detect.

Required candidate flags:

```text
local_only=true
public_hosting=false
ads=false
update_apply=false
docker_pull=false
git_update=false
package_install=false
credential_handling=false
generated_folder_created=false
```

Rules:

- These booleans must describe the dry-run report behavior, not a future
  generator approval.
- A passing JSON report must not be treated as permission to generate package
  files.

## No-Generation Boundary

Purpose:

- Make JSON mode impossible to confuse with generated package output.

Required candidate fields:

```text
files_generated=false
files_copied=false
package_root_created=false
report_file_written=false
stdout_only=true
default_text_output_preserved=true
generation_approved=false
```

Rules:

- JSON output is a report only.
- No package files may be generated.
- No package files may be copied.
- No report file may be written by the first implementation.
- Markdown and text modes remain separate future/current report modes.

## Schema Compatibility Guidance

The first implementation should treat the JSON shape as a small local schema.

Recommended rules:

- Start at `schema_version: "0.1"`.
- Do not remove or rename keys within the same schema version.
- Additive keys are allowed only when they do not change existing meanings.
- Keep enum values documented.
- Prefer explicit `null` for unknown scalar values.
- Prefer empty arrays for no findings.
- Keep output deterministic except for explicitly approved nondeterministic
  fields such as a future `checked_at`.

## PR / Handoff Reuse Guidance

JSON is not intended to replace the Markdown report for human PR bodies.

For future PRs or handoff notes:

- Paste only a short summary unless a reviewer asks for full JSON.
- If full JSON is pasted, wrap it in a fenced `json` block.
- Keep JSON sanitized.
- Do not paste private local paths, submitted media URLs, or real
  cookie/token/secret values.
- Prefer the Markdown report mode for human-first PR summaries once that mode
  exists.

## Safety Boundary

JSON report mode must remain report-only and dry-run-only.

It must not:

- write JSON report files by default;
- create package output paths;
- generate notice, license, manifest, inventory, or guide output;
- change backend, frontend, Docker, CI, package, or lockfile files;
- read, transform, store, or print real cookie/token/secret values;
- include PR #1001 files;
- add CI, PR-comment, merge, or auto-approval behavior;
- treat a passing report as approval for actual generation.

## Future Implementation Checklist

A later implementation PR should:

- keep `text` as the default output;
- add exactly one JSON selector, preferably `--format json`;
- write one valid JSON object to stdout and nothing else in JSON mode;
- reuse existing collected dry-run data instead of adding new scan behavior;
- keep `Status: OK` / `Status: BLOCKED` semantics unchanged;
- keep blocker and warning classification unchanged;
- keep exit-code behavior unchanged;
- keep secret-like findings sanitized;
- keep generated artifact exclusion unchanged;
- keep report-file writing out of scope unless a later contract approves it;
- update docs/llmwiki source-of-truth files in the same PR;
- avoid backend/frontend/Docker/CI/package/lockfile changes.

## Future Verification Checklist

A later implementation PR should verify:

- `git diff --check`;
- `python -m py_compile scripts/clean_package_dry_run.py`;
- `python scripts/check_repo_safety.py`;
- `python scripts/check_repo_safety.py --base fork/master`;
- `python scripts/clean_package_dry_run.py`;
- `python scripts/clean_package_dry_run.py --format text`;
- `python scripts/clean_package_dry_run.py --format json`;
- JSON mode output parses as valid JSON;
- default output remains text;
- JSON output includes all required top-level keys;
- warnings and blockers do not change unexpectedly;
- no generated package folder exists;
- no report file is written;
- no cookie/token/secret values are printed;
- changed files remain inside the approved scope.

## Rollback / Cleanup Note

For this design, there is no generated artifact to clean up.

For a later implementation PR, rollback should be limited to reverting the JSON
mode implementation and related docs. Any cleanup of generated package output
remains outside this design because no package output should exist.

## High-low / High-mid Boundary

High-low:

- docs-only JSON report design;
- report-only JSON implementation that writes nothing;
- stdout-only JSON report with unchanged blockers, warnings, and exit codes;
- auto PR / auto merge may proceed only when all gates pass.

High-mid:

- report-file writing;
- automation wrapper combining JSON and repo safety reports;
- CI integration or PR comment automation;
- package-output staging behavior;
- generated artifact cleanup implementation;
- generator prototype behavior close to actual package generation.

High-mid work requires explicit task approval, PR-ready handoff, and human
review before merge. Actual package generation remains outside this design.
