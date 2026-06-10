# Codex Run Prompt Templates

## Purpose

This document standardizes reusable Codex prompts for the local-only MeTube fork.
The goal is to make future Codex runs faster to start while preserving the
existing safety gates, review checkpoints, and stop conditions.

These templates reduce repeated prompt writing. They do not remove review, lower
risk classification, replace local verification, or authorize higher-risk work.

## Relationship To Existing Automation Tools

- `scripts/run_local_safety_gates.py` is the local verification orchestrator.
- `scripts/check_safety_wording.py` is the docs and PR wording preflight helper.
- `scripts/generate_pr_body.py` can generate a reviewable PR body draft.
- `scripts/check_local_dev_environment.py` can verify local readiness before
  task edits begin.
- `docs/llmwiki/codex-automation-policy.md` remains the risk policy.
- `docs/llmwiki/codex-auto-lanes.md` remains the lane execution policy.
- Prompt templates do not authorize higher risk.
- Prompt templates do not replace human review.

## Non-Goals

Y-AUTO-13 does not:

- implement new scripts;
- change existing scripts;
- add CI;
- call the GitHub API;
- create PRs automatically;
- edit PRs automatically;
- auto merge;
- perform report file writing;
- generate package files;
- create `動画保存ツール_ローカル専用/`;
- generate package manifests, notices, licenses, guides, or inventory;
- run dependency installation operations;
- run container image operations;
- change backend/frontend/Docker/CI/package/lockfile files;
- touch upstream PR #1001 files;
- perform credential-bearing file handling;
- perform secret-like value handling;
- add public hosting or ads;
- add update application operations.

## Global Template Rules

Every template should include:

```text
purpose
scope
allowed files
forbidden files
read-first list
verification commands
stop conditions
PR body requirements
merge rules
final report format
```

Every template should also include:

```text
Do not reset or discard work unless explicitly instructed.
Do not delete local helper files.
Do not weaken safety gates.
```

## Common Start Block

Use this block only when the task explicitly instructs Codex to start from
`fork/master` and discard local branch state:

```powershell
$ErrorActionPreference = "Stop"
Set-Location "C:\Users\tomikyo\_projects\youtubeダウンロード"

git fetch fork --prune
git switch master
git reset --hard fork/master
git status --short --branch
git ls-files --others --exclude-standard
```

Expected state:

```text
## master...fork/master
```

Stop if modified or untracked files remain after the start block.

Optional readiness-only preflight before branch creation:

```powershell
python scripts/check_local_dev_environment.py --base fork/master --expected-branch master
```

## Preflight Block

Use this block after the manual start checks and before file modification:

```powershell
python scripts/check_local_dev_environment.py --base fork/master --expected-branch master
```

If the preflight reports `ERROR`, stop before modifying files. WARN findings
must be reviewed and summarized in recovery or final reports.

## Common Read-First Block

Standard read-first docs:

```text
docs/llmwiki/README.md
docs/llmwiki/current-state.md
docs/llmwiki/safety-boundaries.md
docs/llmwiki/codex-automation-policy.md
docs/llmwiki/automation-efficiency-policy.md
docs/llmwiki/codex-auto-lanes.md
docs/llmwiki/roadmap.md
docs/llmwiki/handoff.md
```

Add specialized docs depending on the task:

```text
docs/llmwiki/local-safety-gate-aggregator-design.md
docs/llmwiki/safety-wording-checker-design.md
docs/llmwiki/pr-body-generator-design.md
docs/llmwiki/clean-package-* docs
```

Read scripts only for context unless the task explicitly allows script changes.

## Common Stop Conditions

Stop and report facts if any of these occur:

```text
safety gate BLOCKED
wording checker blocking ERROR
aggregator failure
changed files outside scope
existing gate scripts changed unexpectedly
backend/frontend/Docker/CI/package/lockfile changed
PR #1001 files appear
generated package folder exists
package output generated
credential-bearing file handling appears
secret-like value handling appears
.gitignore changed unexpectedly
dependency installation operation required
container image operation required
```

## Template 1: Docs-Only PR

```text
Purpose:
  Add or update LLMwiki documentation only.

Branch:
  codex/<task-id>-<short-docs-topic>

Allowed files:
  docs/llmwiki/**

Forbidden files:
  scripts/
  app/
  ui/
  .github/
  Dockerfile
  docker-entrypoint.sh
  pyproject.toml
  uv.lock
  ui/package.json
  ui/pnpm-lock.yaml
  docker-compose.local.yml
  docs/local-only.md
  .gitignore
  動画保存ツール_ローカル専用/

Read first:
  Use the common read-first block plus any task-specific design docs.

Rules:
  Do not reset or discard work unless explicitly instructed.
  Do not delete local helper files.
  Do not weaken safety gates.
  Use safe abstract vocabulary for prohibited operation families.

Verification:
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

PR body:
  Generate a draft, review it manually, and keep the standard sections.

Merge:
  Auto merge OK only if gates pass, GitHub merge state is clean, checks have no
  failures, changed files stay in approved docs scope, and risk is not High-mid.

Final report:
  Include PR URL, local commit, merge commit if merged, changed files, gate
  summaries, generated PR body summary, and confirmation that no scripts or
  package output changed.
```

Example PR body draft command:

```powershell
python scripts/generate_pr_body.py --title "docs: add ..." --risk high-low --scope docs-only --changed-files
```

## Template 2: Report-Only Script PR

```text
Purpose:
  Update report-only or dry-run-only script behavior without generated output.

Allowed files:
  scripts/clean_package_dry_run.py
  scripts/check_clean_package_dry_run_reports.py
  docs/llmwiki/**

Forbidden files:
  app/
  ui/
  .github/
  Dockerfile
  package/lockfile files
  docker-compose.local.yml
  docs/local-only.md
  .gitignore
  動画保存ツール_ローカル専用/

Rules:
  stdout-only unless explicitly approved otherwise.
  No report file writing.
  No generated package output.
  No backend/frontend/Docker/CI/package/lockfile changes.

Verification:
  git diff --check
  python -m py_compile <changed-script>
  python scripts/check_safety_wording.py --base fork/master
  python scripts/run_local_safety_gates.py --base fork/master
  python scripts/check_clean_package_dry_run_reports.py
  python scripts/clean_package_dry_run.py
  python scripts/clean_package_dry_run.py --format text
  python scripts/clean_package_dry_run.py --format markdown
  python scripts/clean_package_dry_run.py --format json

Merge:
  Auto merge OK only if the risk remains Medium or qualifying High-low and all
  gates pass.
```

## Template 3: Checker-Only PR

```text
Purpose:
  Add or harden read-only checker behavior.

Allowed files:
  scripts/check_*.py
  docs/llmwiki/**

Forbidden files:
  app/
  ui/
  .github/
  Dockerfile
  package/lockfile files
  docker-compose.local.yml
  docs/local-only.md
  .gitignore
  動画保存ツール_ローカル専用/

Rules:
  Read-only checker behavior.
  No CI wiring unless separately approved.
  No generated output.
  Do not weaken existing safety gates.

Verification:
  git diff --check
  python -m py_compile <changed-checker>
  python scripts/check_safety_wording.py --base fork/master
  python scripts/run_local_safety_gates.py --base fork/master

Merge:
  New scripts may classify as High-mid / pr-only-human-merge depending on scope.
  Stop before merge if the risk classification or task scope requires human
  review.
```

## Template 4: Combined Report / Checker / Docs PR

```text
Purpose:
  Combine report-only, checker-only, and docs updates for one safety purpose.

Allowed files:
  scripts/clean_package_dry_run.py
  scripts/check_clean_package_dry_run_reports.py
  scripts/check_*.py
  docs/llmwiki/**

Rules:
  Same purpose.
  Same risk band.
  No generated output.
  No report file writing unless explicitly approved.
  No backend/frontend/Docker/CI/package/lockfile changes.

Verification:
  Use the union of report-only, checker-only, and docs-only checks.

Merge:
  Auto merge OK only if the combined risk remains Low, Medium, or qualifying
  High-low and all gates pass.
```

## Template 5: High-Mid PR-Ready Only

```text
Purpose:
  Prepare prototype or automation-adjacent work for human review.

Risk tier:
  High-mid

Automation decision:
  PR-ready only
  automation: pr-only-human-merge
  human-review-required

Rules:
  Auto merge prohibited.
  Merge prohibited until explicit human approval.
  No package/lockfile changes unless separately approved.
  No dependency installation operations.
  No container image operations.
  No credential-bearing file handling.
  No secret-like value handling.

PR body must include:
  Risk tier: High-mid
  Automation decision: PR-ready only
  automation: pr-only-human-merge
  human-review-required
  Why High-mid
  Explicitly not performed
  Verification
  Rollback / cleanup candidates
  Residual risks
  Human review checklist
```

## Template 6: Human-Reviewed Merge

```text
Purpose:
  Merge a PR only after human review approval.

Required facts:
  expected head commit
  mergeStateStatus CLEAN
  failed checks none
  approved changed files only
  local verification passed
  PR target is jsworkht-dotcom/metube:master

Rules:
  Use a head-commit match guard such as --match-head-commit.
  Do not merge if conditions changed.
  Do not merge if changed files exceed approved scope.
  Do not merge if checks fail.
  Do not merge High-mid work without explicit human approval for that PR.

After merge:
  fetch fork
  switch master
  reset local master to fork/master
  confirm final status
```

## Template 7: Recovery / Finalize

```text
Purpose:
  Recover or finish work after an environment issue, gate failure, or interrupted
  Codex run.

Rules:
  Do not reset until a patch backup exists.
  Use an external patch backup path outside the repository when needed.
  Detect the available Python runtime before gate reruns.
  Check lock files before deciding that the repository is stuck.
  Identify preflight failure categories before resuming:
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
  Summarize preflight findings before resuming or finalizing.
  Recover the intended branch before continuing commits or PR work.
  Rerun gates after recovery.
  Continue commit or PR work only when the diff is understood and in scope.
  Do not delete unknown local files.
```

## Template 8: Closeout / Handoff Sync

```text
Purpose:
  Close a safe short lane and sync the LLMwiki source of truth.

Allowed files:
  docs/llmwiki/current-state.md
  docs/llmwiki/roadmap.md
  docs/llmwiki/handoff.md
  docs/llmwiki/pr-history.md if present and directly relevant

Rules:
  current-state sync.
  roadmap sync.
  handoff sync.
  summary of completed PRs.
  next candidate.
  no implementation.
  no generated output.
```

## Template 9: New App Bootstrap

This generic template can be reused beyond this repository.

APP-BOOT-01 records the detailed reusable design in
`docs/llmwiki/new-app-bootstrap-template-design.md`. It is design-only: it does
not create a new app, copy files, add scripts, add CI, create generated package
output, or authorize MVP implementation. APP-BOOT-02 may define skeleton
creation or a bootstrap document packet separately after approval.

```text
APP-00A:
  Define purpose, user, local safety needs, and MVP.

APP-00B:
  Define safety boundaries before implementation.

APP-00C:
  Create initial LLMwiki source-of-truth docs.

APP-00D:
  Define Codex automation policy.

APP-00E:
  Define Codex auto lanes.

APP-00F:
  Design local safety gates.

APP-00G:
  Set up PR body and prompt template policy.

APP-01A:
  Confirm MVP skeleton readiness.

APP-01B:
  Add MVP skeleton only after the docs foundation exists and the scope is
  approved.
```

Rules:

```text
Keep the bootstrap generic.
Start with documentation and safety boundaries.
Do not add generated output or deployment behavior by default.
Do not add dependency installation operations without explicit approval.
Do not add public exposure operations by default.
```

## PR Body Generation Pattern

Use the generator to draft text, then review it manually:

```powershell
python scripts/generate_pr_body.py `
  --title "docs: add Codex prompt templates" `
  --risk high-low `
  --scope docs-only `
  --summary-line "Add docs-only Codex prompt templates." `
  --summary-line "Sync LLMwiki source-of-truth docs." `
  --changed-files
```

Generated text remains a reviewable draft only. It does not replace safety gates
or approve merge.

## Verification Pattern

For Y-AUTO-14 docs-only work:

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

Use bundled Codex Python if `python` is unavailable. Do not install Python.

## Safety Wording Pattern

Prompt templates must use safe abstract vocabulary and avoid risky command-like
examples for prohibited operation families.

Preferred vocabulary:

```text
container image operations
dependency installation operations
network retrieval operations
credential-bearing file handling
secret-like value handling
update application operations
runtime lifecycle operations
public exposure operations
distribution artifact creation
generated package output
```

## Local Helper Pattern

```text
export_context_updated.py remains locally excluded via .git/info/exclude.
.gitignore was not changed.
helper remains uncommitted.
```

## High-low / High-mid / High-high Boundary

High-low:

```text
docs-only prompt template design
docs-only preflight checker design
```

Medium / High-low:

```text
future script that prints prompt text to stdout only
standalone read-only preflight checker implementation
```

High-mid:

```text
prompt tool that writes files
prompt tool that creates PRs
prompt tool that edits PRs
prompt tool that stages commits
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

## Maintenance Rules

Update prompt templates when:

```text
risk policy changes
lane policy changes
new safety gate added
new common stop condition discovered
new app bootstrap flow changes
```

Keep templates concise enough to paste into Codex without unnecessary old
history.

## Verification Checklist

- Only approved docs changed.
- No scripts changed.
- No backend/frontend/Docker/CI/package/lockfile files changed.
- `.gitignore` was not changed.
- PR #1001 files are absent.
- `動画保存ツール_ローカル専用/` is absent.
- Wording checker reports `Status: OK`.
- Local safety gate aggregator reports `Status: OK`.
- PR body generator prints Markdown to stdout only.
- `export_context_updated.py` remains locally excluded and uncommitted.

## Stop Conditions

Stop and report if:

- wording checker has blocking ERROR;
- aggregator fails;
- repo safety reports `BLOCKED`;
- report checker fails;
- dry-run reports `BLOCKED`;
- PR body generator fails;
- changed files leave the approved scope;
- scripts change in a docs-only task;
- backend/frontend/Docker/CI/package/lockfile files change;
- `.gitignore` changes;
- PR #1001 files appear;
- generated package folder exists;
- package output is generated;
- credential-bearing file handling appears;
- secret-like value handling appears;
- dependency installation operation is required;
- container image operation is required.

## Rollback / Cleanup Note

Rollback for Y-AUTO-14 is a docs-only revert.

No generated package output exists to clean up.
