# Automation Efficiency Policy

## Purpose

Y-AUTO-06 adopts the Automation / Efficiency Expansion Plan while preserving the
local-only and no-generation safety boundaries.

The policy is meant to:

- expand safe one-PR scope when changes share the same purpose and risk level;
- define Codex auto lanes for repeatable docs, report, checker, and PR-ready
  work;
- reduce local helper noise by keeping known handoff helpers out of Git status;
- aggregate safety gates into a future local runner;
- standardize PR body, verification, and handoff material;
- prepare future CI, branch protection, CODEOWNERS, and worktree operations.

## Non-Goals

This policy does not approve:

- actual package generation;
- `動画保存ツール_ローカル専用/`;
- ZIP, package, or installer output;
- dependency install or update;
- Docker pull or Docker build is not approved;
- backend, frontend, Docker, CI, package, or lockfile changes;
- cookie, token, secret, or credential handling;
- public hosting;
- ads or monetization;
- upstream PR #1001 files;
- 更新適用機能.

## Current Baseline

- Fork `master` remains the source of truth.
- Local `master` tracks `fork/master`.
- `scripts/check_repo_safety.py` remains report-only.
- `scripts/clean_package_dry_run.py` remains dry-run-only and stdout-only.
- `scripts/check_clean_package_dry_run_reports.py` remains report-only.
- Actual package generation remains blocked.

## Local Helper Policy

`export_context_updated.py` is a local-only WebGPT handoff/context export
helper.

```text
export_context_updated.py:
  purpose: WebGPT handoff/context export helper
  location: repo root local helper
  tracking: local-only via .git/info/exclude
  not committed
  not deleted
  not moved
  not added to .gitignore
```

Y-LOCAL-01 is local setup only. It adds the helper to `.git/info/exclude`, creates
no repository diff, and does not create a PR.

## One-PR Scope Expansion Rules

Allowed same-purpose combinations:

- docs-only + docs-only;
- report-only script + checker + docs sync;
- dry-run preview field addition + checker update + docs sync.

Disallowed mixed-risk combinations:

- report-only + actual generation;
- docs-only + launcher or runtime implementation;
- preview + package folder generation;
- checker + CI + generator prototype;
- runtime selection + package generation;
- dependency, package, or lockfile changes with report-only tasks.

One-PR expansion is allowed only when all changed files remain inside the
approved scope and the safety gates pass.

## Codex Auto Lane Rules

Lane definitions:

- Lane A: docs-only planning lane.
- Lane B: report-only dry-run implementation lane.
- Lane C: checker-only hardening lane.
- Lane D: docs/report/checker combined lane.
- Lane E: High-mid PR-ready-only lane.

Automation rules:

- Low, Medium, and qualifying High-low work may auto PR and auto merge when the
  required gates pass.
- High-mid may proceed to PR-ready only when explicitly approved.
- High-mid auto merge is prohibited.
- High-high stops before implementation.
- Actual generation remains separate and human-reviewed.

## Lane Definitions

- Lane A is for `docs/llmwiki/` planning, source-of-truth sync, roadmap, and
  handoff updates.
- Lane B is for stdout-only report or dry-run behavior that creates no files and
  does not change runtime behavior.
- Lane C is for checker-only hardening with no CI wiring and no generated output.
- Lane D may combine docs, report-only scripts, and checkers when they share one
  safety purpose and stay within the same risk boundary.
- Lane E may prepare a High-mid PR for human review only. It must not auto merge.

## Closeout PR Policy

A closeout PR is allowed only for short lanes when all of these are true:

- the lane can close within 2 to 4 PRs;
- minimal handoff is maintained;
- `current-state.md` is not badly stale;
- no High-mid or High-high risk is introduced;
- no actual generation is performed.

Do not use closeout deferral for generation-adjacent risk increases.

## Safety Gate Aggregator Candidate

Future candidates:

```text
Y-AUTO-08: local safety gate aggregator design
Y-AUTO-09: local safety gate aggregator implementation
```

Candidate scripts:

```text
scripts/run_local_safety_gates.py
scripts/run_local_safety_gates.ps1
```

The local aggregator should run:

```text
git diff --check
scripts/check_repo_safety.py
scripts/check_repo_safety.py --base fork/master
scripts/check_clean_package_dry_run_reports.py
scripts/clean_package_dry_run.py
scripts/clean_package_dry_run.py --format text
scripts/clean_package_dry_run.py --format markdown
scripts/clean_package_dry_run.py --format json
generated folder absence check
PR #1001 file check
changed file scope check
```

The aggregator must remain local, report-only, and non-deploying unless a later
task explicitly approves a narrower implementation.

## PR Body Generator Candidate

Future candidates:

```text
Y-AUTO-11: PR body generator design
Y-AUTO-12: PR body generator stdout-only implementation
```

Candidate script:

```text
scripts/generate_pr_body.py
```

Initial mode:

- stdout-only;
- no default file write;
- no GitHub API;
- no PR creation;
- no token or secret output.

## Codex Prompt Template Candidate

Implemented candidate:

```text
Y-AUTO-13: Codex run prompt templates
```

Candidate doc:

```text
docs/llmwiki/codex-run-prompt-templates.md
```

Initial templates:

- docs-only PR template;
- report-only script PR template;
- checker update PR template;
- combined report / checker / docs PR template;
- High-mid PR-ready-only template;
- human-reviewed merge template;
- recovery / finalize template;
- closeout PR template.
- new app bootstrap template.

The templates reduce repeated Codex prompt writing. They do not replace safety
gates, authorize higher risk, or replace human review.

Follow-up candidate after Y-AUTO-13:

```text
Y-AUTO-14: preflight environment checker design
```

New app bootstrap work remains available as a separate lane:

```text
APP-BOOT-01: new app bootstrap template design
```

APP-BOOT-01 adds `docs/llmwiki/new-app-bootstrap-template-design.md` as a
docs-only reusable bootstrap design. Its purpose is to reuse this project's
safe development method in future apps: repo-local LLMwiki, risk tiers, Codex
auto lanes, preflight, wording check, safety gate aggregation, PR body
generation, and prompt templates.

APP-BOOT-01 does not create a new app, create a new app directory, copy files
into another repo, add scripts, add CI, create generated package output, or
perform dependency installation operations or container image operations.
Future APP-BOOT-02 remains separate and requires explicit approval.

## Preflight Environment Checker Candidate

Y-AUTO-14 adds a docs-only preflight environment checker design.

Purpose:

- catch environment readiness issues before work starts;
- cover Python runtime discovery, Git write-permission checks, GitHub CLI session
  state, local helper exclusion, generated package folder absence, branch
  baseline checks, and local safety tool availability;
- keep safety gates authoritative after changes.

Y-AUTO-15 implements the standalone read-only
`scripts/check_local_dev_environment.py` checker. Future Codex tasks may run it
before file modification to catch local readiness issues early. It does not
replace existing safety gates.

## Future CI / Branch Protection / CODEOWNERS Candidates

Later phases:

```text
Y-CI-01 docs-only safety workflow design
Y-CI-02 minimal safety workflow implementation
Y-CI-03 reusable workflow design
Y-CI-03B reusable workflow implementation
Y-CI-04 concurrency導入
Y-GH-01 branch protection design
Y-CI-05 post-workflow-change observation PR
Y-GH-02 required checks design
Y-GH-03 branch protection implementation, only after explicit human approval
Y-GH-04 required checks implementation, only after explicit human approval and accepted rollback path
```

Y-AUTO-06 does not implement CI, branch protection, or CODEOWNERS.

Y-CI-01 designs `local-fork-safety` as a lightweight PR visibility layer. It
does not replace local gates, implement `.github/workflows/`, add required
checks, mutate branch protection, or add CODEOWNERS.

Y-CI-03 documents reusable workflow structure only. Y-CI-03B is the first
candidate allowed to change `.github/workflows/`, and should still keep the
workflow read-only, non-generating, non-deploying, and separate from branch
protection, required-check, and CODEOWNERS work.

Y-CI-04 is a narrow CI-scope implementation lane for caller-owned
`local-fork-safety` concurrency. It may add only workflow-level concurrency to
`.github/workflows/local-fork-safety.yml` with
`group: ${{ github.workflow }}-${{ github.ref }}` and
`cancel-in-progress: true`. It must leave
`.github/workflows/reusable-local-safety.yml` safety steps unchanged, keep
`permissions: contents: read`, and avoid dependency install/update, Docker,
artifact upload/cache, package or generated output, branch protection,
required-check configuration, CODEOWNERS, secrets, `pull_request_target`, and
PR #1001 files. Existing repo safety may still report workflow-file changes as
an expected CI-scope blocker requiring human review.

Y-GH-01 is design-only and records future branch protection / ruleset
candidates in `docs/llmwiki/branch-protection-design.md`. It does not mutate
GitHub settings, create rulesets, configure required checks, add CODEOWNERS, or
change workflow files. Required-check configuration remains deferred until the
displayed `local-fork-safety` check name is observed and stable.

Y-GH-02 is design-only and records the required checks strategy in
`docs/llmwiki/required-checks-design.md`. It may record
`local fork safety / local fork safety` as the current candidate based on PR
#98 and PR #99 observations, but it does not mutate GitHub settings, create
rulesets, configure required checks, add CODEOWNERS, or change workflow files.
Required-check implementation remains deferred until a later explicit
human-approved lane accepts the exact check name, workflow-change exception
policy, and rollback path.

## Worktree Operation Candidate

Later phase:

```text
Y-AUTO-later worktree operation design
```

Candidate layout:

```text
main:
  master同期・確認専用

worktree/codex:
  Codex作業用

worktree/review:
  PR差分確認用
```

Y-AUTO-06 does not implement worktree operation.

## Stop Condition Checker Candidate

Later phase:

```text
Y-AUTO-later stop condition checker design
```

Candidate script:

```text
scripts/check_stop_conditions.py
```

Y-AUTO-06 does not implement this checker.

## Generation Readiness Score Candidate

Future Y-08G, Y-08H, or later work may add advisory readiness summary fields:

```text
overall: blocked
score: advisory_only
blockers
unresolved_review_items
next_required_action
```

Rules:

- advisory only;
- never approval for generation;
- blockers and human review take precedence.

## Allowed Auto-Merge Scope

Allowed auto-merge scope is limited to Low, Medium, and qualifying High-low work
when all required gates pass and GitHub reports a clean merge state with no
failed checks.

Examples:

- docs-only planning updates;
- report-only script changes;
- checker-only hardening;
- same-purpose docs/report/checker sync that stays inside the approved lane.

## Human Review Required Scope

Human review is required for:

- High-mid PR-ready-only work;
- High-high work before implementation;
- any actual generation task;
- any task that needs dependency, Docker, package, lockfile, backend, frontend,
  CI, secret, public hosting, ads, or update-apply scope;
- any task that touches PR #1001 files.

## Stop Conditions

Stop and report facts if any of these occur:

- `scripts/check_repo_safety.py` reports `BLOCKED`;
- `scripts/check_clean_package_dry_run_reports.py` fails;
- `scripts/clean_package_dry_run.py` reports `BLOCKED`;
- changed files include scripts in a docs-only lane;
- changed files include backend, frontend, Docker, CI, package, or lockfile
  files without explicit scope;
- `動画保存ツール_ローカル専用/` exists;
- PR #1001 files appear;
- cookie, token, or secret values appear;
- `.gitignore` changes for the local helper;
- report files are written;
- package output is generated;
- dependency install/update is required;
- Docker pull/build is prohibited when required.

## Y-AUTO-07 implementation

`docs/llmwiki/codex-auto-lanes.md` was added to make lane execution concrete.

- Y-AUTO-07 ties abstract lane ideas to practical auto lane rules.
- It adds concrete lane permissions, gates, stop conditions, closeout rules, and PR
  body requirements for docs-only/report-only/checker workflow.
- Y-AUTO-08 and Y-AUTO-09 remain the next high-level candidates in this
  stream.

## Recommended Execution Order

```text
Y-LOCAL-01:
  export_context_updated.py local exclude

Y-AUTO-06:
  automation efficiency policy

Y-AUTO-07:
  codex auto lanes (implemented)

Y-AUTO-08:
  safety gate aggregator design

Y-AUTO-09:
  safety gate aggregator implementation

Y-AUTO-11:
  PR body generator design

Y-AUTO-12:
  PR body generator stdout-only implementation

Y-AUTO-13:
  Codex run prompt templates

Y-AUTO-14:
  preflight environment checker design

APP-BOOT-01:
  new app bootstrap template design (implemented docs-only)

APP-BOOT-02:
  bootstrap skeleton design / packet

Y-CI-01:
  lightweight CI design
```

CI, branch protection, CODEOWNERS, worktree, and stop condition checker work
comes after that sequence unless explicitly approved earlier.

## Verification Checklist

For Y-AUTO-06:

- `git diff --check`
- `python scripts/check_repo_safety.py`
- `python scripts/check_repo_safety.py --base fork/master`
- `python scripts/check_clean_package_dry_run_reports.py`
- `python scripts/clean_package_dry_run.py`
- `python scripts/clean_package_dry_run.py --format text`
- `python scripts/clean_package_dry_run.py --format markdown`
- `python scripts/clean_package_dry_run.py --format json`
- confirm `動画保存ツール_ローカル専用/` is absent;
- confirm changed files are approved docs only;
- confirm `export_context_updated.py` remains locally excluded and uncommitted.

## Rollback / Cleanup Note

Rollback is a docs-only revert of the Y-AUTO-06 commit.

The local helper setup can be undone by removing the `export_context_updated.py`
entry from `.git/info/exclude`.

No generated package output exists to clean up.

## Y-AUTO-08 Local Safety Gate Aggregator Design Note

Y-AUTO-08 adds the docs-only design for a future local safety gate aggregator in `docs/llmwiki/local-safety-gate-aggregator-design.md`.

The aggregator remains a future implementation candidate. It would orchestrate the existing local gates, not replace them:

- `scripts/check_repo_safety.py` remains the repo-diff safety gate.
- `scripts/check_clean_package_dry_run_reports.py` remains the report regression gate.
- `scripts/clean_package_dry_run.py` remains the clean-package preview dry-run gate.
- The manual gate baseline remains required until Y-AUTO-09 or later implements the aggregator.

Recommended next step: Y-AUTO-09 may implement a stdlib-only, read-only `scripts/run_local_safety_gates.py` with text output only.
## Y-AUTO-09 Local Safety Gate Aggregator Implementation Note

Y-AUTO-09 adds `scripts/run_local_safety_gates.py` as a stdlib-only, read-only, text-output-only local gate aggregator.

The aggregator runs existing repo safety, dry-run report regression, and clean-package dry-run gates in a deterministic order. It also checks generated package folder absence, PR #1001 leakage absence, local helper exclusion, and changed-file summary.

Future PR body generator work may consume the aggregator output, but that remains a later explicit task. The current design is recorded in Y-AUTO-11.
## Y-AUTO-10A Safety Wording Checker Design Note

Y-AUTO-10A adds `docs/llmwiki/safety-wording-checker-design.md` as a docs-only design for a future safety wording checker.

Purpose: prevent documentation wording false positives by preferring safe abstract vocabulary for prohibited operation families. The future checker must not weaken `scripts/check_repo_safety.py` or any existing safety gate.

Recommended next candidate: Y-AUTO-10B safety wording checker implementation as a standalone read-only checker.
## Y-AUTO-10B Safety Wording Checker Implementation Note

Y-AUTO-10B adds `scripts/check_safety_wording.py` as a standalone read-only safety wording checker.

The checker reduces docs wording false positives by scanning changed docs before stronger safety gates surface wording-only issues. It does not weaken repo safety gates.

Future aggregator integration remains separate. PR body generator design is recorded in Y-AUTO-11.

## Y-AUTO-11 PR Body Generator Design Note

Y-AUTO-11 adds `docs/llmwiki/pr-body-generator-design.md` as a docs-only design
for a future stdout-only PR body generator.

Purpose:

- reduce repeated PR body writing;
- preserve explicit safety evidence;
- standardize risk, verification, not-performed, local helper, cleanup, and
  human review sections.

Y-AUTO-12 implements `scripts/generate_pr_body.py` as a read-only,
stdout-only PR body generator.

The generator reduces repeated PR body drafting by emitting standard Markdown
sections for risk, verification, not-performed scope, local helper status,
cleanup, and human review notes. It does not replace safety gates, approve
merge, edit PRs, or call the GitHub API.

Y-AUTO-13 records the Codex prompt templates as the next automation aid.

## Y-AUTO-13 Codex Prompt Templates Note

Y-AUTO-13 adds `docs/llmwiki/codex-run-prompt-templates.md` as a docs-only
template library for future Codex runs.

Purpose:

- reduce repeated Codex prompt writing;
- standardize reusable prompt blocks for docs-only, report-only, checker-only,
  combined, High-mid PR-ready, human-reviewed merge, recovery, closeout, and new
  app bootstrap workflows;
- preserve safety gates and human review.

The templates do not replace `scripts/run_local_safety_gates.py`,
`scripts/check_safety_wording.py`, `scripts/generate_pr_body.py`,
`docs/llmwiki/codex-automation-policy.md`, or
`docs/llmwiki/codex-auto-lanes.md`.

Next candidate: Y-AUTO-15 preflight environment checker implementation if
continuing tooling hardening, or APP-BOOT-01 new app bootstrap template design
if moving to a new app workflow.

## Y-AUTO-14 Preflight Environment Checker Design Note

Y-AUTO-14 adds `docs/llmwiki/preflight-environment-checker-design.md` as a
docs-only design for a future task-start readiness checker.

Purpose:

- catch environment readiness issues before Codex edits files;
- document future checks for Python runtime discovery, Git metadata access,
  GitHub CLI session state, remote and branch baseline, local helper exclusion,
  generated package folder absence, PR #1001 leakage precheck, and local safety
  tool availability;
- clarify that preflight is readiness-only and does not replace safety gates.

Y-AUTO-15 implements the checker as a stdlib-only, read-only,
text-output-only script. Future tasks can run it before file modification, but
the checker remains readiness-only and does not replace safety gates.

## Y-AUTO-15 Preflight Environment Checker Implementation Note

Y-AUTO-15 adds `scripts/check_local_dev_environment.py` as a standalone
preflight environment checker.

Purpose:

- detect local readiness issues before task edits;
- check Python runtime discovery, Git repository/branch/metadata access, lock
  files, optional GitHub CLI session state, remotes, baseline ref, local helper
  exclusion, generated folder absence, PR #1001 leakage, and local safety tool
  availability;
- keep `scripts/run_local_safety_gates.py` and the underlying safety gates
  authoritative after changes.

The checker does not replace safety gates, approve merge, authorize higher
risk, write reports, create generated package output, or perform GitHub write
actions.
