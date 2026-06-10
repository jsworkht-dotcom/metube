# Codex Auto Lanes

## Purpose

This document converts the automation efficiency policy into concrete Codex auto lane
execution rules.

Its goal is to let Codex safely continue across related low/medium/high-low tasks
without asking for manual confirmation after every tiny step, while preserving stop
conditions and PR/merge restrictions for High-mid and High-high outcomes.

## Relationship To Existing Policies

`docs/llmwiki/codex-automation-policy.md` remains the core risk policy.
`docs/llmwiki/automation-efficiency-policy.md` defines efficiency expansion and
lane intent.
`docs/llmwiki/codex-auto-lanes.md` defines practical lane execution rules.
Safety boundaries remain unchanged.
Actual generation remains blocked.

## Non-Goals

Y-AUTO-07 does not approve:

- actual package generation;
- generated distribution folder creation;
- ZIP / package / installer output;
- dependency install/update;
- container image operations;
- backend/frontend/Docker/CI/package/lockfile changes;
- cookie/token/secret handling;
- public hosting;
- ads/monetization;
- PR #1001 files;
- 更新適用機能;
- CI implementation;
- safety aggregator implementation;
- PR body generator implementation;
- worktree operation implementation.

## Global Prerequisites

Codex auto lane may start only when:

```text
local master is reset to fork/master
working tree is clean
export_context_updated.py is locally excluded if present
no generated package folder exists
no PR #1001 files are modified
no secret/token/cookie values appear
required safety gates pass
```

## Lane Summary

Codex execution lanes are:

```text
Lane A:
  docs-only planning lane

Lane B:
  report-only dry-run implementation lane

Lane C:
  checker-only hardening lane

Lane D:
  combined report/checker/docs lane

Lane E:
  High-mid PR-ready-only lane
```

## Lane A: Docs-Only Planning

Allowed:

```text
docs/llmwiki/**
planning docs
policy docs
roadmap/handoff/current-state sync
contract docs
readiness docs
```

Not allowed:

```text
scripts/
app/
ui/
Dockerfile
.github/
package/lockfile
generated folder
actual package output
```

Automation:

```text
auto PR: OK
auto merge: OK if gates pass
risk: Low / High-low depending on topic
```

Example tasks:

```text
Y-AUTO-07 codex auto lanes
Y-CI-01 docs-only safety workflow design
Y-GH-01 branch protection design
Y-08Z closeout
```

## Lane B: Report-Only Dry-Run Implementation

Allowed:

```text
scripts/clean_package_dry_run.py
docs/llmwiki/**
```

Only when:

```text
stdout-only
report-only
no files generated
no package output
no report file writing
exit codes preserved unless explicitly approved
text/markdown/json contract preserved
```

Automation:

```text
auto PR: OK
auto merge: OK if gates pass
risk: Medium / High-low
```

Required verification:

```text
py_compile for changed script
check_clean_package_dry_run_reports.py
check_repo_safety.py
check_repo_safety.py --base fork/master
clean_package_dry_run.py all formats
no generated folder
```

Examples:

```text
Y-08F readiness checklist preview report-only
Y-08G readiness unresolved item summary
Y-08H readiness summary polish
```

## Lane C: Checker-Only Hardening

Allowed:

```text
scripts/check_clean_package_dry_run_reports.py
docs/llmwiki/**
```

Only when:

```text
stdlib-only
read-only checks
no generated files
no package output
no dependency changes
```

Automation:

```text
auto PR: OK
auto merge: OK if gates pass
risk: Medium / High-low
```

## Lane D: Combined Report / Checker / Docs

Allowed:

```text
scripts/clean_package_dry_run.py
scripts/check_clean_package_dry_run_reports.py
docs/llmwiki/**
```

Only when:

```text
same purpose
same risk band
report-only / checker-only / docs-only
no generation
no report file writing
no backend/frontend/Docker/CI/package/lockfile changes
```

Automation:

```text
auto PR: OK
auto merge: OK if gates pass
risk: Medium / High-low
```

## Lane E: High-Mid PR-Ready Only

Allowed only when explicitly approved:

```text
generator prototype script
launcher prototype
desktop shell scaffold
generated artifact cleanup script
package output staging logic
```

Automation:

```text
auto PR: OK only if explicitly approved
auto merge: prohibited
merge: human review required
risk: High-mid
```

PR body must include:

```text
Risk tier: High-mid
Automation decision: PR-ready only
automation: pr-only-human-merge
human-review-required
```

## One-PR Bundle Rules

Allowed bundles:

```text
docs-only + docs-only
report-only script + checker + docs sync
checker-only + docs sync
dry-run preview field addition + checker update + docs sync
```

Disallowed bundles:

```text
report-only + actual generation
docs-only + runtime/launcher implementation
preview + generated package folder
checker + CI + generator prototype
runtime selection + package generation
dependency/package/lockfile + report-only
backend/frontend behavior changes + package preview
```

## Continuous Execution Rules

Codex may continue through multiple tasks in the same lane when all are true:

```text
tasks are explicitly listed in the lane plan
risk band remains Low / Medium / High-low
each PR passes gates
GitHub changed files match approved scope
mergeStateStatus is CLEAN
no failed checks
no generated folder
no stop condition occurs
```

Suggested limit:

```text
2 to 4 PRs per auto lane before closeout
```

Stop after closeout or if risk increases.

## Auto PR Gate

Before PR creation:

```text
git diff --check
check_repo_safety.py
check_repo_safety.py --base fork/master
check_clean_package_dry_run_reports.py
clean_package_dry_run.py all formats
changed files match lane scope
no generated folder
no PR #1001 files
no secret/token/cookie values
```

## Auto Merge Gate

Before auto merge:

```text
PR target is jsworkht-dotcom/metube:master
PR is not draft
GitHub changed files match lane scope
mergeStateStatus is CLEAN
no failed checks
local verification passed
no High-mid / High-high scope
```

Docs-only PRs may have no checks reported if paths are ignored; this is
acceptable when local gates pass and no failed checks exist.

## Human Review Gate

Human review required for:

```text
High-mid work
High-high work
actual package generation
generated package folder creation
ZIP/package/installer
dependency install/update
container image operations
backend/frontend behavior changes
package/lockfile changes
cookie/token/secret handling
public hosting/ads
更新適用機能
```

## Closeout PR Rules

Closeout PR is allowed for short safe lanes:

```text
2 to 4 PRs
Low / Medium / High-low only
no actual generation
minimal handoff maintained after each step
full current-state/roadmap/contract sync at closeout
```

Closeout PR is not allowed for:

```text
High-mid
High-high
generation-adjacent risk increase
credential/security-sensitive changes
runtime/dependency/package changes
```

## Branch / Commit / Merge Rules

Branch naming examples:

```text
codex/y-auto-07-codex-auto-lanes
codex/y-08f-readiness-preview
codex/y-auto-09-safety-gate-aggregator
```

Commit messages:

```text
docs: add Codex auto lane policy
feat: add readiness checklist preview
test: extend dry-run report regression checker
```

Merge:

```text
squash merge
delete remote branch
reset local master to fork/master
```

## Verification Matrix

Lane A docs-only:

```text
git diff --check
check_repo_safety.py
check_repo_safety.py --base fork/master
check_clean_package_dry_run_reports.py
clean_package_dry_run.py all formats
```

Lane B / D script changes:

```text
git diff --check
py_compile changed scripts
check_clean_package_dry_run_reports.py
check_repo_safety.py
check_repo_safety.py --base fork/master
clean_package_dry_run.py all formats
spot checks for changed fields
```

Lane C checker-only:

```text
git diff --check
py_compile checker
check_clean_package_dry_run_reports.py
check_repo_safety.py
check_repo_safety.py --base fork/master
clean_package_dry_run.py all formats
```

## Stop Conditions

Stop if:

```text
repo safety BLOCKED
dry-run BLOCKED
report checker fails
changed files outside lane scope
scripts changed in docs-only lane
backend/frontend/Docker/CI/package/lockfile changes appear
PR #1001 files appear
cookie/token/secret values appear
generated package folder exists
noisy report file is written
package output is generated
dependency install/update required
container image operation required
mergeStateStatus not CLEAN
failed checks exist
risk tier High-mid without explicit PR-ready-only approval
risk tier High-high
```

## PR Body Requirements

Every auto lane PR must include:

```text
Summary
Risk / automation
Why this is not higher risk
Explicitly not performed
Verification
Cleanup / rollback
Human review note
```

High-mid PRs must include the stricter High-mid template from
`codex-automation-policy.md`.

## Current Recommended Auto Lane

After Y-AUTO-07, recommended lane:

```text
Y-AUTO-08:
  safety gate aggregator design

Y-AUTO-09:
  safety gate aggregator implementation

Y-AUTO-10:
  PR body generator design

Y-AUTO-11:
  PR body generator stdout-only implementation

Y-AUTO-12:
  Codex run prompt templates
```

This may be run as a planned efficiency lane only if each PR stays in allowed
scope and passes gates.

## Future Lane Candidates

```text
Y-08F to Y-08Z preview readiness lane
Y-CI-01 to Y-CI-04 CI design/implementation lane
Y-GH-01 to Y-GH-02 GitHub governance design lane
Y-AUTO-13 worktree design lane
Y-AUTO-14 stop condition checker design lane
```

## Rollback / Cleanup Note

For docs-only lane work:

```text
revert docs commit
no generated output to clean up
```

For report/checker lane work:

```text
revert script/checker/docs commit
rerun gates
no generated output should exist
```

Actual generated package cleanup remains outside auto lane unless explicitly
approved.

## Y-AUTO-08 Local Safety Gate Aggregator Relationship

Y-AUTO-08 documents a future local safety gate aggregator. The design is docs-only and does not add implementation or generated output.

After a later Y-AUTO-09 implementation, Lane B, Lane C, and Lane D tasks may use the aggregator as a convenience wrapper for existing local gates. Until that implementation lands, the manual gate sequence remains required.

The aggregator does not authorize higher-risk work by itself. Lane risk still depends on changed file scope, generated output, dependency scope, container image operations, credential handling, and whether a human review boundary is crossed.

Current recommended auto lane after Y-AUTO-08:

- Y-AUTO-09: implement a read-only local safety gate aggregator with stdlib-only text output.
- Y-AUTO-10: add PR-body integration guidance for aggregator output after Y-AUTO-09 is merged.
- Y-AUTO-11: refine lane-specific scope presets if Y-AUTO-09 output proves stable.
- Y-AUTO-12: revisit package-readiness workflow only after gate aggregation is stable.
## Y-AUTO-09 Aggregator Use In Auto Lanes

Lane verification may now use `scripts/run_local_safety_gates.py --base fork/master` as a local convenience wrapper.

The underlying gate scripts remain authoritative:

- `scripts/check_repo_safety.py`
- `scripts/check_clean_package_dry_run_reports.py`
- `scripts/clean_package_dry_run.py`

The aggregator does not authorize higher risk by itself. It does not change lane boundaries, does not approve generated output, and does not turn High-mid work into auto-merge work.

Current recommended auto lane after Y-AUTO-09:

- Y-AUTO-10: PR body generator design.
- Y-AUTO-11: PR body generator stdout-only implementation.
- Y-AUTO-12: Codex run prompt templates.
- Y-08F: readiness checklist preview implementation, if explicitly approved.
## Y-AUTO-10A Safe Wording Relation

Lane A docs-only tasks should use the safe wording policy from `docs/llmwiki/safety-wording-checker-design.md` when listing prohibited operation families.

A future wording checker may become part of lane preflight. It does not authorize higher risk, does not approve generated output, and does not weaken the underlying repo safety gate.

Current recommended auto lane after Y-AUTO-10A:

- Y-AUTO-10B: safety wording checker implementation.
- Y-AUTO-11: PR body generator design.
- Y-AUTO-12: PR body generator stdout-only implementation.
- Y-AUTO-13: Codex prompt templates.
## Y-AUTO-10B Wording Checker Use In Lane A

Lane A docs-only tasks may run `scripts/check_safety_wording.py --base fork/master` before the normal safety gate sequence.

The wording checker is a preflight helper, not a replacement for repo safety. It does not authorize higher risk, does not approve generated output, and does not change auto-merge boundaries.

Current recommended auto lane after Y-AUTO-10B:

- Y-AUTO-11: PR body generator design.
- Y-AUTO-12: PR body generator stdout-only implementation.
- Y-AUTO-13: Codex prompt templates.
- APP-BOOT-01: new app bootstrap template design.