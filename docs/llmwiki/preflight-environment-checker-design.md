# Preflight Environment Checker Design

## Purpose

This design defines a future local development environment preflight checker for
Codex work in the local-only MeTube fork.

The future checker should detect local readiness issues before a Codex task
starts. It should reduce avoidable failures from missing Python runtime access,
Git metadata permission issues, GitHub CLI session state issues, branch lock
issues, local helper noise, generated package output leftovers, and fork/master
baseline mismatch.

The checker is readiness-only. It does not replace safety gates, approve merge,
authorize higher risk, or perform corrective actions.

## Background

Recent automation work exposed recurring local environment issue types:

- Python command not available on PATH.
- Bundled Codex Python required for local verification.
- Branch creation blocked by Git permission or lock issue.
- GitHub merge operation blocked by session issue.
- Docs wording gate blocked by risky wording.
- Local helper had to be excluded from Git status noise.

These are environment-readiness problems, not implementation requirements. A
future checker should make them visible before a task edits files.

## Relationship To Existing Automation Tools

- `scripts/run_local_safety_gates.py` verifies repository safety after changes.
- `scripts/check_safety_wording.py` checks docs and PR wording.
- `scripts/generate_pr_body.py` drafts reviewable PR body text.
- The future preflight checker runs before a task begins.
- The future preflight checker does not approve merge.
- The future preflight checker does not replace repo safety gates.
- The future preflight checker should be directly callable and may later be
  referenced by prompt templates.

## Non-Goals

Y-AUTO-14 does not:

- implement the checker;
- change scripts;
- add CI;
- call the GitHub API;
- create PRs;
- edit PRs;
- auto merge;
- write report files;
- generate package files;
- create `動画保存ツール_ローカル専用/`;
- generate package manifests, notices, licenses, guides, or inventory;
- run dependency installation operations;
- run container image operations;
- change backend/frontend/Docker/CI/package/lockfile files;
- touch upstream PR #1001 files;
- perform credential-bearing file handling;
- perform secret-like value handling;
- add public exposure operations or ads;
- add update application operations.

## Problem Cases To Prevent

The future checker should report these cases before task work begins:

- Python runtime unavailable.
- Bundled Python path not detected.
- Git branch creation permission issue.
- Stale Git lock files.
- Current branch not expected.
- Local master not synced with fork/master.
- Fork remote missing or incorrect.
- Origin/upstream remote unexpected.
- GitHub CLI session unavailable.
- GitHub read works but merge or write action fails.
- Local helper not excluded.
- Generated package folder already present.
- PR #1001 files modified unintentionally.
- Required local helper scripts missing.

## Future Script Candidate

Candidate future script:

```text
scripts/check_local_dev_environment.py
```

Y-AUTO-15 may implement it later.

Y-AUTO-15 implements this script as the first standalone read-only preflight
checker.

Initial implementation requirements:

- stdlib-only;
- read-only;
- text output only;
- no file writes;
- no GitHub API write actions;
- no PR creation or editing;
- no merge actions;
- no package output;
- no dependency installation operations;
- no container image operations.

## Initial Check Categories

Suggested categories:

```text
python_runtime
git_repository
git_branch
git_metadata_access
git_lock_files
github_cli_session
remote_configuration
baseline_ref
working_tree_summary
local_helper_exclusion
generated_output_absence
pr1001_leakage_precheck
tooling_availability
```

## Python Runtime Discovery

The future checker should detect:

- `sys.executable`;
- Python on PATH if available;
- bundled Codex Python candidates;
- required Python scripts present.

Rules:

- Do not install Python.
- Do not modify PATH.
- Report the discovered runtime path.
- Prefer `sys.executable` when running from Python.

## Git Repository / Branch Checks

The future checker should verify:

- inside expected repo;
- current branch;
- local master exists;
- fork/master reachable;
- working tree status;
- untracked files summary.

It should not reset, discard work, or create branches.

## Git Write-Permission Checks

The future checker should detect likely Git write-permission issues safely.

Allowed read-only checks:

- `.git` path exists;
- `refs/heads` path readable;
- lock files list;
- current user can read required Git metadata.

The first implementation should avoid creating test branches unless a later task
separately approves that behavior.

## GitHub CLI Session Checks

The future checker may verify:

- GitHub CLI installed;
- session state is available;
- repo can be read.

It should not perform write actions, PR actions, or merge actions.

Do not print secrets, credentials, or private values.

If GitHub CLI is unavailable, report a warning instead of modifying the
environment.

## Remote / Branch Baseline Checks

The future checker should verify:

- fork remote exists;
- fork remote URL matches expected fork;
- origin/upstream remote is known;
- master tracks fork/master.

It should not modify remotes.

## Local Helper Exclusion Checks

The future checker should verify:

- `export_context_updated.py` does not appear in untracked output;
- `.git/info/exclude` contains the local helper rule when the helper exists;
- `.gitignore` remains unchanged.

It should not edit `.git/info/exclude` unless a later explicit local setup task
approves that change.

## Generated Package Folder Checks

The future checker should fail if this repo-root path exists:

```text
動画保存ツール_ローカル専用/
```

The checker should report the blocker without deleting or modifying the path.

## PR #1001 Leakage Precheck

The future checker should report if these paths are changed:

```text
docker-compose.local.yml
docs/local-only.md
```

Use safe language and do not modify those files.

## Local Safety Tool Availability Checks

The future checker should verify existence of:

```text
scripts/run_local_safety_gates.py
scripts/check_safety_wording.py
scripts/generate_pr_body.py
scripts/check_repo_safety.py
scripts/check_clean_package_dry_run_reports.py
scripts/clean_package_dry_run.py
```

It should not run all gates. That remains the local safety gate aggregator's
role.

## Output Format

Example success output:

```text
Preflight Environment Check

Status: OK

Checks:
- Python runtime discovery: OK
- Git repository: OK
- Git branch baseline: OK
- Git metadata access: OK
- GitHub CLI session state: OK
- fork/master availability: OK
- local helper exclusion: OK
- generated package folder absent: OK
- PR #1001 leakage precheck: OK
- local safety tools present: OK
```

Failure example:

```text
Preflight Environment Check

Status: FAILED

Findings:
- python_runtime: ERROR
  action: use bundled Codex Python or restore configured runtime
- git_permissions: ERROR
  action: resolve Git metadata permission issue before branch creation
```

Do not print secrets.

## Exit Code Contract

Future exit codes:

```text
0: preflight passed
1: required environment check failed
2: usage/runtime error
```

Warnings should not fail unless they block safe execution.

## Sanitization Rules

The future checker must not print real:

- cookie values;
- token values;
- secret values;
- credential values;
- private environment values;
- submitted media URLs;
- private config values.

It should print only status, paths, categories, and safe remediation hints.

## Integration With Codex Prompt Templates

Update prompt templates so future tasks can start with:

```text
Run preflight environment checker first.
If it fails, stop before modifying files.
```

Do not require this until implementation exists. Until Y-AUTO-15 or a later
implementation lands, prompt templates should keep the manual start checks.

## Integration With Local Safety Gate Aggregator

Differentiate the two tools:

```text
preflight checker:
  before task, environment readiness

local safety gate aggregator:
  after changes, repo safety verification
```

Later, the aggregator may mention preflight results, but it should not replace
the preflight checker.

## High-low / High-mid / High-high Boundary

High-low:

```text
docs-only preflight checker design
```

Medium / High-low:

```text
standalone read-only preflight checker implementation
```

High-mid:

```text
checker that modifies local config
checker that creates test branches
checker that edits remotes
checker that performs GitHub write actions
checker that writes report files
```

High-high:

```text
actual package generation
distribution artifact creation
dependency installation operations
container image operations
credential-bearing file handling
secret-like value handling
public exposure operations
update application operations
```

## Verification Checklist

For Y-AUTO-14 docs-only PR:

```powershell
git diff --check
python scripts/check_safety_wording.py --base fork/master
python scripts/check_safety_wording.py --all
python scripts/run_local_safety_gates.py --base fork/master --scope docs-only
python scripts/generate_pr_body.py --title "docs: design preflight environment checker" --risk high-low --scope docs-only --changed-files
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

Use bundled Codex Python if `python` is not available. Do not install Python.

## Stop Conditions

Stop if:

- wording checker has blocking ERROR;
- aggregator fails;
- PR body generator fails;
- repo safety reports `BLOCKED`;
- report checker fails;
- dry-run reports `BLOCKED`;
- changed files outside docs scope;
- scripts changed;
- backend/frontend/Docker/CI/package/lockfile changed;
- PR #1001 files appear;
- generated package folder exists;
- cookie/token/secret values appear;
- `.gitignore` changed;
- report file is written;
- generated package output exists;
- dependency installation operation is required;
- container image operation is required.

## Rollback / Cleanup Note

For Y-AUTO-14:

```text
revert docs-only commit
no generated output to clean up
```

For future Y-AUTO-15:

```text
revert preflight checker script and docs
no generated output should exist
```

## Y-AUTO-15 Implementation Note

Y-AUTO-15 implements `scripts/check_local_dev_environment.py` as a standalone
read-only preflight checker.

The checker covers:

- Python runtime discovery;
- Git repository, branch, metadata access, and lock file checks;
- optional GitHub CLI session state checks;
- remote configuration and baseline ref checks;
- working tree summary;
- local helper exclusion;
- generated package folder absence;
- PR #1001 leakage precheck;
- required local safety tool availability.

The checker remains readiness-only:

- no file writes;
- no Git config changes;
- no branch creation;
- no GitHub write action;
- no PR creation or editing;
- no merge actions;
- no package output.
