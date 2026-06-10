# Safety Wording Checker Design

## Purpose

This design defines a future safety wording checker for LLMwiki documentation. Its purpose is to prevent docs-only PRs from being blocked by unsafe wording that merely describes prohibited operation families.

The future checker should reduce review churn and handoff retries without weakening `scripts/check_repo_safety.py` or any other safety gate.

## Background

Y-AUTO-07 exposed a docs-only wording problem: a prohibition list used literal tool/action wording, and the repository safety gate treated that text conservatively. The resolution was to keep the checker strict and reword the docs with safe abstract vocabulary.

Y-AUTO-10A makes that approach repeatable. It documents how future docs should describe prohibited work without embedding command-like phrasing.

## Relationship To Existing Safety Gates

- `scripts/check_repo_safety.py` remains authoritative for risky repository changes.
- The future wording checker is only a preflight/helper for documentation wording.
- The wording checker must not weaken existing safety gates.
- It may run before or inside `scripts/run_local_safety_gates.py` in a later task.
- Existing gates remain directly callable.

## Non-Goals

Y-AUTO-10A does not:

- implement the checker;
- change scripts;
- change `scripts/check_repo_safety.py`;
- add CI;
- write report files;
- generate package files;
- create `動画保存ツール_ローカル専用/`;
- generate package manifests, notices, licenses, guides, or inventory;
- run dependency installation operations;
- run container image operations;
- change backend, frontend, Docker, CI, package, or lockfile files;
- touch PR #1001 files;
- handle cookie, token, or secret values;
- add public hosting or ads;
- add 更新適用機能.

## Problem Pattern

A docs-only file may include literal risky wording while explaining what is prohibited. The wording can be detected by repo safety gates as if it were an actual operation. This is useful conservatism, but it creates avoidable handoff and retry work.

The future checker should identify those wording patterns before the stronger repo safety gate becomes the first place they are discovered.

## Safe Wording Policy

- Prefer abstract operation names.
- Avoid exact command-like phrases.
- Avoid combining tool names with execution verbs on one line.
- Avoid including sample commands for prohibited operation families.
- Use "not performed" lists with safe vocabulary.
- When exact command text is necessary, isolate it in a purpose-built allowlisted design only after human review.

## Replacement Vocabulary

| Risk area | Avoid raw wording style | Preferred safe wording | Notes |
| --- | --- | --- | --- |
| Container image work | tool-name plus retrieval or build verb | container image operations | Use as a category label, not as command text. |
| Dependency setup | package-manager name plus action verb | dependency installation operations | Avoid command-like examples. |
| Network retrieval | tool-name plus fetch-style action | network retrieval operations | Prefer a broad operation family. |
| Runtime lifecycle | service-control wording | runtime restart operations | Use only with safe context; not as a command example. |
| Update behavior | apply-style update wording | update application operations | Keep this as policy vocabulary, not endpoint behavior. |
| Credentials | file names or values that imply auth material | credential-bearing file handling | Do not include sample values. |
| Secrets | literal secret-like examples | secret-like value handling | Mention only pattern families. |
| Public exposure | public endpoint or broad access wording | public exposure operations | Keep local-only scope explicit. |
| Generated output | concrete package artifact names | generated package output | Use when discussing absent outputs. |
| Distribution artifacts | archive or installer specifics | distribution artifact creation | Use as a risk category only. |

## Future Checker Candidate

Candidate script:

```text
scripts/check_safety_wording.py
```

Y-AUTO-10B can implement this later.

Requirements:

- stdlib-only;
- read-only;
- text output only;
- no file writes;
- no network;
- no GitHub API;
- no dependency changes;
- no package output;
- scan changed docs by default;
- optionally scan all `docs/llmwiki/**`.

## Initial Scan Scope

The future checker should scan:

- changed docs files;
- `docs/llmwiki/**`;
- PR body template docs;
- handoff docs;
- automation policy docs.

It should not scan generated package output because actual generation remains blocked.

## Detection Categories

Suggested safe category names:

- `container_image_wording`
- `dependency_operation_wording`
- `credential_wording`
- `secret_like_wording`
- `update_application_wording`
- `public_exposure_wording`
- `generated_artifact_wording`

## Severity Levels

ERROR:

- wording likely to trigger repo safety or looks command-like.

WARN:

- wording may be acceptable but should be rephrased.

INFO:

- safe replacement suggestion.

## Output Format

Example success output:

```text
Safety Wording Check

Status: OK

Scanned:
- docs/llmwiki/...

Findings:
- none
```

Example failure output:

```text
Safety Wording Check

Status: FAILED

Findings:
- docs/llmwiki/example.md:12 category=container_image_wording severity=ERROR
  suggestion: use "container image operations"
```

Failure output should not print risky literal phrases unless they are sanitized.

## Exit Code Contract

Future exit codes:

- `0`: no ERROR findings.
- `1`: one or more ERROR findings.
- `2`: usage or runtime error.

## Integration With Local Safety Gate Aggregator

Future integration path:

- Y-AUTO-10B: implement standalone checker.
- Y-AUTO-10C or later: integrate the checker into `scripts/run_local_safety_gates.py`.

Y-AUTO-10A does not integrate anything. The aggregator remains read-only and does not generate output.

## PR Body / Handoff Usage

Future PR body generation should use safe vocabulary in:

- Explicitly not performed;
- Human review note;
- Stop conditions;
- Rollback note.

This reduces false BLOCKED results while preserving conservative safety gates.

## False Positive Handling

- Do not weaken repo safety gates first.
- Prefer rewording docs.
- If exact text is unavoidable, require a separate docs-only exception design.
- Exceptions must be narrow, documented, and human-reviewed.

## High-low / High-mid / High-high Boundary

High-low:

- docs-only wording checker design.

Medium / High-low:

- standalone read-only wording checker implementation.

High-mid:

- checker that rewrites files;
- checker that writes reports;
- checker that stages changes;
- checker integrated with PR creation.

High-high:

- actual package generation;
- distribution artifact creation;
- dependency installation operations;
- container image operations;
- credential, token, or secret handling;
- public exposure or ads;
- update application operations.

## Verification Checklist

For Y-AUTO-10A docs-only PR:

```powershell
python scripts/run_local_safety_gates.py --base fork/master --scope docs-only
git diff --check
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

Use bundled Codex Python if PATH does not expose Python. Do not install Python.

## Stop Conditions

Stop if:

- repo safety is blocked;
- aggregator fails;
- report checker fails;
- dry-run is blocked;
- changed files are outside docs scope;
- scripts changed;
- backend, frontend, Docker, CI, package, or lockfile files changed;
- PR #1001 files appear;
- generated package folder exists;
- cookie, token, or secret values appear;
- `.gitignore` changed;
- report file is written;
- package output is generated;
- dependency installation operation is required;
- container image operation is required.

## Rollback / Cleanup Note

For Y-AUTO-10A:

- revert the docs-only commit;
- no generated output exists to clean up.

For future Y-AUTO-10B:

- revert the checker script and docs;
- no generated output should exist.

## Y-AUTO-10B Implementation Note

Y-AUTO-10B implements `scripts/check_safety_wording.py` as a standalone safety wording checker.

The implementation follows this design boundary:

- stdlib-only;
- read-only;
- text-output-only;
- scans changed docs by default;
- supports `--base`, `--all`, and explicit paths;
- prints sanitized category, severity, and suggestion fields without printing raw matched phrases;
- does not weaken `scripts/check_repo_safety.py`;
- is not yet integrated into `scripts/run_local_safety_gates.py`.