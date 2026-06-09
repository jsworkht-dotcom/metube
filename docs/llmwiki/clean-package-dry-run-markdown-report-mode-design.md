# Clean Package Dry-Run Markdown Report Mode Design

## Purpose

Y-06Z defines a docs-only design for a future Markdown report mode in
`scripts/clean_package_dry_run.py`.

The goal is to preserve the current text report while designing a Markdown
shape that can be pasted into a fork PR body, handoff note, or human review
record.

This document is design material only. It does not implement Markdown output,
does not change the dry-run script, and does not create package output.

## Current Inputs

Read-only context checked for this design:

- `scripts/clean_package_dry_run.py`
- `scripts/check_repo_safety.py`
- `docs/llmwiki/clean-package-dry-run-contract.md`
- `docs/llmwiki/clean-package-generator-contract-addendum.md`
- `docs/llmwiki/codex-automation-policy.md`
- `docs/llmwiki/handoff.md`
- `docs/llmwiki/roadmap.md`

Current dry-run text sections to preserve:

- package root;
- status;
- repository branch and commit;
- planned entries;
- package manifest preview;
- package output diff prediction;
- excluded rules and currently-present excluded paths;
- checks;
- warnings;
- blocked reasons;
- safety flags;
- no-files-generated closing line.

## Non-Goals

Y-06Z does not:

- change `scripts/clean_package_dry_run.py`;
- change `scripts/check_repo_safety.py`;
- add JSON output;
- add Markdown output;
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
- add High-mid implementation work;
- add 更新適用機能.

## Output Mode Candidates

Preferred future CLI candidate:

```text
python scripts/clean_package_dry_run.py --format markdown
```

Reasons:

- The script already has `--format text`.
- Extending the existing option is the smallest future interface change.
- `text` can remain the default without adding a second mode selector.

Alternative future CLI candidate:

```text
python scripts/clean_package_dry_run.py --report markdown
```

Tradeoffs:

- Clearer wording for report selection.
- Larger future CLI change because `--format` already exists.
- More risk of two overlapping options if both are retained.

Recommendation:

- Keep default output as text.
- Prefer `--format markdown` for the first Markdown implementation.
- Do not write report files in the first Markdown implementation.
- Keep Markdown output on stdout only unless a later explicit task approves a
  report-file path contract.

## Proposed Markdown Sections

The Markdown report should keep the same information order as the text report,
with headings suitable for PR body reuse.

```md
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

### Summary

Purpose:

- Identify repository branch and commit.
- State local-only package planning scope.
- State whether the report is OK or blocked.
- State that the report is dry-run-only and no-generation.

Suggested fields:

```text
repository_branch
repository_commit
package_root_candidate
report_mode
status
no_files_generated
```

### Status

Purpose:

- Preserve the current `Status: OK` / `Status: BLOCKED` meaning.
- Keep warnings nonblocking unless existing blocker rules say otherwise.
- Keep exit-code meaning unchanged.

Suggested presentation:

```md
## Status

- Status: OK
- Blockers: none
- Warnings: none
```

### Risk Classification

Purpose:

- Provide a PR-ready place to paste the paired repo safety gate result.
- Avoid pretending that the clean-package dry-run itself owns repository risk
  classification.

Rules:

- The section may be filled from `scripts/check_repo_safety.py`.
- If the dry-run runs alone, show `not included by dry-run alone`.
- Do not compute a second, conflicting risk tier inside the Markdown report
  unless a later task explicitly changes the contract.

Suggested presentation:

```md
## Risk Classification

- tier: High-low
- automation: auto-merge-ok
- source: scripts/check_repo_safety.py --base fork/master
```

### Package Manifest Preview

Purpose:

- Preserve Y-06X preview content in Markdown.
- Keep source counts and candidate future outputs reviewable.

Suggested fields:

- package name candidate;
- package type candidate;
- `local_only: true`;
- `generated_artifacts: false`;
- notice source count and list;
- guide source count and list;
- future output candidates;
- `human_review_required_before_generation: true`;
- `legal_final: false`;
- secret/token/cookie non-disclosure flags.

### Package Output Diff Prediction

Purpose:

- Preserve Y-06Y prediction content in Markdown.
- Make future package effects reviewable without writing package output.

Suggested fields:

- future package root candidate;
- would-create directory candidates;
- would-create file candidates;
- would-copy source groups;
- would-generate future outputs;
- would-exclude path summary;
- currently-present excluded path count;
- `no_files_generated: true`;
- `human_review_required_before_generation: true`;
- cleanup / rollback candidate note.

### Notice / Guide Source Coverage

Purpose:

- Keep source coverage visible for human review.
- Separate missing source warnings from blockers.

Suggested fields:

- notice sources present / total;
- guide sources present / total;
- missing notice sources;
- missing guide sources;
- local-only safety source coverage;
- Windows/macOS section source coverage.

Rules:

- Source coverage remains warning-oriented in report-only mode.
- Actual generation remains a later human-reviewed task.

### Excluded Paths Summary

Purpose:

- Preserve excluded rule count and currently-present excluded path count.
- Make generated artifact exclusion easy to review.

Suggested fields:

- excluded rule count;
- currently-present excluded path count;
- generated package root present / not present;
- PR #1001 leakage status;
- forbidden path status;
- forbidden filename status;
- secret-like content status.

### Blockers

Purpose:

- Preserve blocker details in a pasteable form.
- Keep secret-like findings sanitized.

Rules:

- If none, print `none`.
- If present, list path, line number when safe, pattern family, and sanitized
  message.
- Do not print real cookie/token/secret values.

### Warnings

Purpose:

- Preserve nonblocking review notes.
- Keep warning count visible.

Rules:

- If none, print `none`.
- If present, list source path and sanitized message.
- Do not upgrade or downgrade warning behavior in the Markdown mode.

### Human Review Checklist

Purpose:

- Provide a reusable PR/handoff checklist before any later generation task.

Checklist candidate:

```md
## Human Review Checklist

- [ ] Status is OK.
- [ ] Repo safety gate has no blockers.
- [ ] Clean-package dry-run has no blockers.
- [ ] Package manifest preview is acceptable.
- [ ] Package output diff prediction is acceptable.
- [ ] Notice and guide source coverage is acceptable for this phase.
- [ ] Excluded paths summary is acceptable.
- [ ] No generated package folder exists.
- [ ] No cookie/token/secret values are printed.
- [ ] PR #1001 files are absent.
- [ ] No backend/frontend/Docker/CI/package/lockfile changes are mixed in.
- [ ] Human review is complete before any actual generation task.
```

### No-Generation Boundary

Purpose:

- Make the Markdown report impossible to confuse with generated package output.

Required statements:

- This is a report-only dry-run.
- No package files were generated.
- No package files were copied.
- No generated artifact was created.
- Default text output remains supported.
- Markdown mode is not permission to generate package output.

## PR Body Reuse Guidance

For future report-only package-adjacent PRs, the Markdown report may be pasted
under a PR section named:

```md
## Clean Package Dry-Run Summary
```

PR body reuse rules:

- Include Summary, Status, Risk Classification, Blockers, Warnings, and
  No-Generation Boundary at minimum.
- Include Package Manifest Preview and Package Output Diff Prediction when the
  PR changes those report sections.
- Keep the pasted report sanitized.
- Do not paste private local paths, submitted media URLs, or real
  cookie/token/secret values.

## Handoff Reuse Guidance

For future handoff notes, keep the Markdown report shorter than the full dry-run
output.

Recommended handoff subset:

- Summary;
- Status;
- Risk Classification;
- Package Manifest Preview summary;
- Package Output Diff Prediction summary;
- Blockers;
- Warnings;
- Human Review Checklist;
- No-Generation Boundary.

The handoff subset should point to `scripts/clean_package_dry_run.py` for the
full report source.

## Safety Boundary

Markdown report mode must remain report-only and dry-run-only.

It must not:

- write Markdown report files by default;
- create package output paths;
- generate notice, license, manifest, inventory, or guide output;
- change backend, frontend, Docker, CI, package, or lockfile files;
- read, transform, store, or print real cookie/token/secret values;
- include PR #1001 files;
- treat a passing report as approval for actual generation.

## Future Implementation Checklist

A later implementation PR should:

- keep `text` as the default output;
- add exactly one Markdown selector, preferably `--format markdown`;
- reuse existing collected dry-run data instead of adding new scan behavior;
- keep `Status: OK` / `Status: BLOCKED` behavior unchanged;
- keep blocker and warning classification unchanged;
- keep secret-like findings sanitized;
- keep generated artifact exclusion unchanged;
- keep stdout-only behavior unless a later report-file path contract is
  explicitly approved;
- update docs/llmwiki source-of-truth files in the same PR;
- avoid backend/frontend/Docker/CI/package/lockfile changes.

## Future Verification Checklist

A later implementation PR should verify:

- `git diff --check`;
- `python -m py_compile scripts/clean_package_dry_run.py`;
- `python scripts/check_repo_safety.py`;
- `python scripts/check_repo_safety.py --base fork/master`;
- `python scripts/clean_package_dry_run.py`;
- `python scripts/clean_package_dry_run.py --format markdown`;
- default output remains text;
- Markdown output includes all required sections;
- warnings and blockers do not change unexpectedly;
- no generated package folder exists;
- no cookie/token/secret values are printed;
- changed files remain inside the approved scope.

## Rollback / Cleanup Note

For this design, there is no generated artifact to clean up.

For a later implementation PR, rollback should be limited to reverting the
Markdown mode implementation and related docs. Any cleanup of generated package
output remains outside this design because no package output should exist.

## High-low / High-mid Boundary

High-low:

- docs-only Markdown report design;
- report-only Markdown implementation that writes nothing;
- stdout-only Markdown preview with unchanged blockers and warnings;
- auto PR / auto merge may proceed only when all gates pass.

High-mid:

- implementation-adjacent report-file writing;
- package-output staging behavior;
- generated artifact cleanup implementation;
- generator prototype behavior close to actual package generation.

High-mid work requires explicit task approval, PR-ready handoff, and human
review before merge. Actual package generation remains outside this design.
