# Local Safety Gate Aggregator Design

## Purpose

This design defines a future local safety gate aggregator for the current manual verification sequence. The aggregator should run the same local safety gates, produce a concise human-readable result, and reduce repeated command overhead without weakening any existing gate.

The design is docs-only. It does not add implementation, report files, generated package output, CI wiring, or package generation behavior.

## Relationship To Existing Gates

The aggregator is an orchestrator only.

- `scripts/check_repo_safety.py` remains the repo-diff safety gate.
- `scripts/check_clean_package_dry_run_reports.py` remains the report regression gate.
- `scripts/clean_package_dry_run.py` remains the package-preview dry-run gate.
- Each individual gate remains directly callable for narrow debugging and review.
- The aggregator does not approve merge readiness by itself; it reports local gate results for human review.

## Non-Goals

This Y-AUTO-08 task does not implement an aggregator script.

Out of scope:

- Script, test, CI, app, UI, Docker, package, or lockfile changes.
- Report files, package files, archive files, installer files, or generated package folders.
- `動画保存ツール_ローカル専用/` creation.
- `manifest.json`, `NOTICE.txt`, `LICENSES/`, guide output, inventory output, or similar generated outputs.
- Dependency additions or version changes.
- Container image operations.
- PR #1001 file changes: `docker-compose.local.yml` and `docs/local-only.md`.
- `.gitignore` changes.
- Cookie, token, credential, or secret handling.
- Public hosting, ads, or 更新適用機能.

## Current Manual Gate Baseline

The current manual baseline remains authoritative until a later implementation PR lands.

```powershell
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

When PATH does not expose Python, the same sequence should be run with the known Codex bundled Python executable.

## Aggregator Command Candidate

A later implementation candidate is:

```powershell
python scripts/run_local_safety_gates.py --base fork/master
```

Potential options:

- `--base <ref>` selects the comparison base, defaulting to `fork/master`.
- `--json` emits a machine-readable summary to stdout without writing a file.
- `--markdown` emits a PR-body-friendly markdown summary to stdout without writing a file.
- `--strict` treats warnings as failures for manually selected lanes.
- `--scope docs-only` checks that only approved documentation files changed.
- `--scope report-only` checks report-contract-only work.
- `--scope checker-only` checks safety-checker-only work.

The first implementation should stay simple: text output only, stdlib-only, no writes.

## Execution Model

The future aggregator should:

- Use only the Python standard library.
- Resolve the repository root from the script path, not from the caller's current directory alone.
- Run child Python commands through `sys.executable` so bundled Python works consistently.
- Run gates in deterministic order.
- Capture stdout and stderr from each child command.
- Preserve each child exit code in the final summary.
- Continue far enough to report already-run gate results, while still returning failure if any required gate fails.
- Print only concise excerpts needed for diagnosis.
- Avoid printing secret-like values.
- Avoid writing files or creating directories.

## Python Runtime Resolution

This environment may not expose `python`, `python3`, `py`, or `uv` on PATH. A later implementation should not try to add or modify a runtime. It should use the interpreter already running the aggregator via `sys.executable`.

For manual verification before implementation, use the bundled Codex Python executable when available.

## Gate List

The first aggregator implementation should cover these gates:

- Whitespace and patch hygiene: `git diff --check`.
- Repo safety default scan: `scripts/check_repo_safety.py`.
- Repo safety base comparison: `scripts/check_repo_safety.py --base fork/master`.
- Dry-run report regression: `scripts/check_clean_package_dry_run_reports.py`.
- Clean package dry-run default mode.
- Clean package dry-run text mode.
- Clean package dry-run markdown mode.
- Clean package dry-run JSON mode.
- Generated package folder absence.
- Changed file scope check.
- PR #1001 leakage check.
- Untracked helper exclusion check.

## Changed File Scope Check

The aggregator should compare changed files against the selected lane scope.

Initial scope candidates:

- `docs-only`: documentation-only policy, design, state, roadmap, and handoff updates.
- `report-only`: dry-run report contract and source-material documentation updates.
- `checker-only`: safety checker documentation or checker implementation work after explicit approval.
- `combined-report-checker-docs`: coordinated report/checker/docs updates after explicit approval.
- `high-mid-pr-ready-only`: PR-ready work that still requires human review before merge.

The aggregator reports lane scope status. It does not authorize higher risk work by itself.

## Generated Package Folder Check

The aggregator should fail when `動画保存ツール_ローカル専用/` exists unless a later task explicitly approves generated package output. Y-AUTO-08 does not approve that output.

## PR #1001 Leakage Check

The aggregator should flag these files if they appear in a branch that is not intentionally working on upstream PR #1001:

- `docker-compose.local.yml`
- `docs/local-only.md`

## Report Mode Regression Check

The aggregator should keep `scripts/check_clean_package_dry_run_reports.py` as the dedicated report regression gate. This avoids duplicating report assertions in the orchestrator.

## Clean Package Dry-Run Checks

The aggregator should call `scripts/clean_package_dry_run.py` in default, text, markdown, and JSON modes. All modes must remain read-only and must not create package output.

## Repository Safety Checks

The aggregator should call both repository safety modes:

- Default mode for current working tree safety.
- Base comparison mode for changed-line and changed-file safety against `fork/master`.

The existing safety script remains the source of truth for blockers.

## Output Format

Initial text output should be compact and copyable.

Example:

```text
Local safety gates
base: fork/master
scope: docs-only

PASS git diff --check
PASS check_repo_safety.py
PASS check_repo_safety.py --base fork/master
PASS check_clean_package_dry_run_reports.py
PASS clean_package_dry_run.py
PASS clean_package_dry_run.py --format text
PASS clean_package_dry_run.py --format markdown
PASS clean_package_dry_run.py --format json
PASS generated package folder absent
PASS changed file scope
PASS PR #1001 leakage absent
PASS untracked helper exclusion

status: OK
```

Failure output should identify the failing gate, child exit code, and a short diagnostic excerpt.

## Exit Code Contract

- `0`: all required gates passed.
- `1`: one or more gates failed, or a stop condition was detected.
- `2`: usage error, unsupported option, or invalid scope.

## Sanitization Rules

The aggregator must not print raw cookie, token, secret, credential, private environment variable, submitted media URL, or private config values. If a gate needs to report such a finding, it should summarize the path, line, or pattern family without exposing the value.

## Windows / Bundled Python Notes

Windows PATH may not contain a Python launcher. The future aggregator should be launched with whichever Python executable is available and should use `sys.executable` for child Python gates. This keeps bundled Codex Python behavior explicit and avoids environment mutation.

## Future Implementation Candidate

Y-AUTO-09 can implement `scripts/run_local_safety_gates.py` if approved. The recommended first version is:

- Stdlib-only.
- Text output only.
- Read-only gate execution.
- No generated outputs.
- No CI or GitHub API integration.
- No PR creation or merge operation.
- Scope validation for docs-only first.

## Future PR Body Integration Candidate

Y-AUTO-10 or Y-AUTO-11 may consume aggregator output in PR body templates after Y-AUTO-09 lands. That integration should still preserve human review notes and explicit non-performed sections.

## High-low / High-mid / High-high Boundary

- High-low: docs-only aggregator design with no implementation and no output files.
- Medium or High-low: stdlib-only aggregator implementation that runs read-only checks and writes no generated output.
- High-mid: tasks that write report files, clean up package output, stage package output, or trigger PR/final-integration operations.
- High-high: actual generation, archive/package/installer output, dependency setup changes, container image operations, backend/frontend/package/lockfile changes, cookie/token/secret handling, public hosting, ads, or 更新適用機能.

## Verification Checklist

For Y-AUTO-08, verify:

- Only approved docs changed.
- No script, app, UI, Docker, CI, package, or lockfile changed.
- `.gitignore` did not change.
- `動画保存ツール_ローカル専用/` is absent.
- PR #1001 files are absent from the branch.
- No package output was generated.
- Existing manual gates still pass.

## Stop Conditions

Stop and report if:

- Python safety gates cannot run.
- `scripts/check_repo_safety.py` reports blocked status.
- Report regression checking fails.
- `scripts/clean_package_dry_run.py` reports blocked status.
- Scripts, app, UI, Docker, CI, package, lockfile, or `.gitignore` changes appear.
- PR #1001 files appear.
- `動画保存ツール_ローカル専用/` exists.
- Package output is generated.

## Rollback / Cleanup Note

Rollback for this docs-only task is limited to removing the Y-AUTO-08 documentation additions. No generated folder, report file, package output, dependency change, or runtime change should exist from this task.

## Y-AUTO-09 Implementation Note

Y-AUTO-09 implements `scripts/run_local_safety_gates.py` as the first local safety gate aggregator.

The implementation follows the Y-AUTO-08 design boundaries:

- It orchestrates existing gates and does not replace them.
- It is Python stdlib-only.
- It is read-only and text-output-only.
- It writes no report files and creates no package output.
- It checks generated package folder absence, PR #1001 leakage absence, local helper exclusion, and changed-file summary.
- It does not perform GitHub API usage, PR creation, merge actions, CI integration, dependency changes, or container image operations.

The underlying gates remain authoritative. The aggregator only reduces repeated local command overhead.