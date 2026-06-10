# PR Body Generator Design

## Purpose

This design defines a future PR body generator for the local-only MeTube fork.
Its purpose is to reduce repeated manual PR body writing while preserving
explicit safety evidence for reviewers.

The future generator should produce reviewable Markdown text only. It should not
replace local verification, human review, merge decisions, or repository safety
classification.

## Background

Recent fork PRs have repeatedly used the same PR body sections:

- Summary
- Risk / automation
- Local helper note
- Explicitly not performed
- Verification
- Cleanup / rollback
- Human review note

The goal is to standardize these sections without weakening human review or
removing explicit safety evidence from each PR.

## Relationship To Existing Tools

- `scripts/run_local_safety_gates.py` produces a local safety verification
  summary.
- `scripts/check_safety_wording.py` helps keep PR body and docs language in the
  safe abstract vocabulary.
- `scripts/check_repo_safety.py` remains authoritative for repository safety
  classification.
- A future PR body generator may consume outputs or facts from these tools.
- The generator does not replace verification.
- The generator does not approve merge.

## Non-Goals

Y-AUTO-11 does not:

- implement the generator;
- change scripts;
- add CI;
- call the GitHub API;
- create PRs;
- edit PRs;
- auto merge;
- write PR body files;
- generate package files;
- create `動画保存ツール_ローカル専用/`;
- generate package manifests, notices, licenses, guides, or inventory;
- run dependency installation operations;
- run container image operations;
- change backend, frontend, Docker, CI, package, or lockfile files;
- touch upstream PR #1001 files;
- handle cookie, token, or secret values;
- add public hosting or ads;
- add 更新適用機能.

## Future Script Candidate

Candidate future script:

```text
scripts/generate_pr_body.py
```

Y-AUTO-12 implements this script as the first stdout-only generator.

Initial implementation requirements:

- stdlib-only;
- read-only;
- stdout-only;
- no file writes by default;
- no GitHub API;
- no PR creation;
- no merge actions;
- no package output.

## Input Sources

Future generator may accept:

```text
--title
--risk
--automation
--scope
--base
--summary-line
--not-performed-preset
--verification-preset
--human-review
```

It may also read:

```text
git diff --name-only
git status --short --branch
run_local_safety_gates summary
check_safety_wording summary
```

Initial Y-AUTO-12 should stay simple and avoid parsing complex logs unless that
parsing is easy and deterministic.

## Output Sections

Future output must include:

```md
## Summary
## Risk / automation
## Local helper note
## Explicitly not performed
## Verification
## Cleanup / rollback
## Human review note
```

Optional sections:

```md
## Changed files
## Residual risks
## Follow-up
```

## Risk / Automation Section Rules

The generator should define templates for:

- Low / auto-merge-ok
- Medium / auto-merge-ok
- High-low / auto-merge-ok
- High-mid / pr-only-human-merge
- High-high / stop-before-implementation

High-mid template requirements:

```text
Risk tier: High-mid
Automation decision: PR-ready only
automation: pr-only-human-merge
human-review-required
```

The High-high template must not suggest PR merge.

## Explicitly Not Performed Section Rules

Use safe abstract vocabulary.

Common entries:

- no script changes
- no checker changes
- no CI integration
- no report file writing
- no generated distribution folder
- no package manifest output
- no generated notice/license/inventory/guide output
- no ZIP/package/installer output
- no dependency installation operations
- no package/lockfile changes
- no container image operations
- no backend/frontend/Docker/CI changes
- no backend download/extractor changes
- no cookie/token/secret handling
- no public hosting or ads
- no PR #1001 files
- no update application operations

The generator should allow presets by scope:

- docs-only
- report-only
- checker-only
- combined
- high-mid-pr-ready

## Verification Section Rules

Templates should include:

```text
git diff --check
python scripts/run_local_safety_gates.py --base fork/master
python scripts/check_safety_wording.py --base fork/master
```

For script changes:

```text
python -m py_compile <changed-script>
```

For dry-run/report changes:

```text
python scripts/check_clean_package_dry_run_reports.py
python scripts/clean_package_dry_run.py all formats
```

## Human Review Section Rules

Docs-only, Low, and High-low:

```text
Future high-risk work still requires human review.
Actual generation remains blocked.
```

High-mid:

```text
This PR is PR-ready only.
Human review is required before merge.
Auto merge is prohibited.
```

High-high:

```text
Implementation must not proceed without explicit human approval.
```

## Local Helper Note Rules

Default note:

```text
export_context_updated.py remains locally excluded via .git/info/exclude.
.gitignore was not changed.
helper remains uncommitted.
```

The generator should allow omitting this section if no helper policy applies in
another project.

## Safety Wording Rules

The generator must use safe wording from
`docs/llmwiki/safety-wording-checker-design.md`.

It must avoid command-like risky examples.

Future implementation should be checked by:

```powershell
python scripts/check_safety_wording.py --base fork/master
```

## CLI Design

Future candidate commands:

```powershell
python scripts/generate_pr_body.py --risk high-low --scope docs-only --title "docs: design PR body generator"
python scripts/generate_pr_body.py --risk medium --scope checker-only --title "feat: add safety wording checker"
python scripts/generate_pr_body.py --risk high-mid --scope high-mid-pr-ready --title "feat: add package prototype"
```

Optional flags:

```text
--base fork/master
--automation auto-merge-ok
--automation pr-only-human-merge
--human-review-required
--include-local-helper-note
--no-local-helper-note
--changed-files
```

Initial Y-AUTO-12 implementation should keep this minimal.

## Output Format

Future generator outputs Markdown to stdout.

No file write by default.

Example:

```md
## Summary

- Add docs-only PR body generator design.
- Sync LLMwiki source-of-truth docs.

## Risk / automation

Risk tier: High-low
Automation decision: auto-merge-ok if all gates pass
```

## Exit Code Contract

Future exit codes:

```text
0: generated PR body successfully
1: validation failed or unsafe option combination
2: usage/runtime error
```

## Sanitization Rules

The generator must not print real:

- cookie values
- token values
- secret values
- credential values
- private env values
- submitted media URLs
- private config values

It should not read env secret values.

## Scope / Risk Templates

### docs-only

Changed files should normally be:

```text
docs/llmwiki/**
README.md
```

### report-only

May include:

```text
scripts/clean_package_dry_run.py
scripts/check_clean_package_dry_run_reports.py
docs/llmwiki/**
```

### checker-only

May include:

```text
scripts/check_*.py
docs/llmwiki/**
```

### combined

May include report/checker/docs combinations only when they share the same
purpose and the same risk band.

### high-mid-pr-ready

Must include human-review-required wording.

## Integration With Local Safety Gate Aggregator

Future generator may use aggregator output summary.

It must not run gates by default unless explicitly requested.

Candidate future option:

```text
--from-aggregator-output
```

or:

```text
--include-verification-preset local-safety-gates
```

## Integration With Safety Wording Checker

Future generator output should be compatible with the wording checker.

Later task may add a stdin validation path:

```text
python scripts/generate_pr_body.py ... | python scripts/check_safety_wording.py --stdin
```

Do not implement stdin mode now; this is only documented as future work.

## Future GitHub API Boundary

The generator must not call the GitHub API in the initial implementation.

If future integration is desired:

```text
Y-AUTO-later:
  GitHub PR body update design
```

This would be High-mid or higher depending on write behavior and must be
reviewed separately.

## High-low / High-mid / High-high Boundary

High-low:

```text
docs-only PR body generator design
```

Medium / High-low:

```text
stdout-only generator implementation
read-only git metadata collection
no file writes
```

High-mid:

```text
generator that writes PR body files
generator that edits GitHub PRs
generator that creates PRs
generator that stages commits
```

High-high:

```text
actual package generation
distribution artifact creation
dependency installation operations
container image operations
credential/token/secret handling
public exposure/ads
update application operations
```

## Verification Checklist

For Y-AUTO-11 docs-only PR:

```powershell
git diff --check
python scripts/check_safety_wording.py --base fork/master
python scripts/check_safety_wording.py --all
python scripts/run_local_safety_gates.py --base fork/master --scope docs-only
python scripts/check_repo_safety.py
python scripts/check_repo_safety.py --base fork/master
python scripts/check_clean_package_dry_run_reports.py
python scripts/clean_package_dry_run.py
python scripts/clean_package_dry_run.py --format text
python scripts/clean_package_dry_run.py --format markdown
python scripts/clean_package_dry_run.py --format json
Test-Path "動画保存ツール_ローカル専用"
git diff --name-only fork/master...HEAD
git status --short --branch
git ls-files --others --exclude-standard
```

Use bundled Codex Python if `python` is not on PATH. Do not install Python.

## Stop Conditions

Stop if:

- wording checker has blocking ERROR;
- aggregator fails;
- repo safety reports BLOCKED;
- report checker fails;
- dry-run reports BLOCKED;
- changed files are outside docs scope;
- scripts changed;
- backend/frontend/Docker/CI/package/lockfile files changed;
- PR #1001 files appear;
- generated package folder exists;
- cookie/token/secret values appear;
- `.gitignore` changed;
- report file is written;
- package output is generated;
- dependency installation operation is required;
- container image operation is required.

## Rollback / Cleanup Note

For Y-AUTO-11:

```text
revert docs-only commit
no generated output to clean up
```

For Y-AUTO-12:

```text
revert generator script and docs
no generated output should exist
```

## Y-AUTO-12 Implementation Note

Y-AUTO-12 implements `scripts/generate_pr_body.py`.

Implementation boundaries:

- stdout-only Markdown output;
- read-only behavior;
- Python stdlib only;
- no GitHub API;
- no PR creation or editing;
- no file writes by default;
- risk and scope templates;
- safe wording compatible with the safety wording checker;
- optional sanitized changed-file summary from read-only Git commands.

The generator does not replace safety gates, does not approve merge, and does
not authorize higher-risk work.

## Y-AUTO-13 Codex Prompt Template Relationship

`docs/llmwiki/codex-run-prompt-templates.md` may reference
`scripts/generate_pr_body.py` for PR body drafting patterns.

The generator output remains a reviewable draft only. Prompt templates must
still instruct Codex to review generated Markdown before PR use, run local
safety gates, keep safe abstract vocabulary, and preserve human review
requirements.

Prompt templates do not turn PR body generation into GitHub API integration, PR
creation/editing automation, merge approval, report file writing, or generated
package output.
