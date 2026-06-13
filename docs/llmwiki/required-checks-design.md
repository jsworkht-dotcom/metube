# Y-GH-02 Required Checks Design

## Purpose

Y-GH-02 records a docs-only required status checks strategy for future fork
`master` protection.

This PR does not enable branch protection, rulesets, required checks,
CODEOWNERS, repository settings, workflow files, or GitHub settings APIs. It
only records the current required-check candidate, risks, approval fields,
rollback expectations, stop conditions, and recommended next lane.

## Sources Checked

Repository sources:

- `docs/llmwiki/branch-protection-design.md`
- `docs/llmwiki/post-workflow-change-observation.md`
- `docs/llmwiki/current-state.md`
- `docs/llmwiki/roadmap.md`
- `docs/llmwiki/handoff.md`
- `docs/llmwiki/lightweight-safety-workflow-design.md`
- `docs/llmwiki/reusable-local-safety-workflow-design.md`
- `docs/llmwiki/codex-automation-policy.md`
- `docs/llmwiki/automation-efficiency-policy.md`
- `.github/workflows/local-fork-safety.yml`
- `.github/workflows/reusable-local-safety.yml`

Official GitHub docs checked on 2026-06-13:

- Protected branches:
  `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches`
- Managing a branch protection rule:
  `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule`
- About status checks:
  `https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks`
- Rulesets:
  `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets`
- Available rules for rulesets:
  `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets`
- Troubleshooting rulesets and required status checks:
  `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/troubleshooting-rules`

## Facts / Assumptions / Needs Verification

Facts:

- Canonical branch: fork `master`.
- Latest fork `master` baseline before Y-GH-02:
  `e77e68c56a369c3ae962cf0abcbe958ce36a2101` from fork PR #99.
- Current PR-facing workflow: `.github/workflows/local-fork-safety.yml`.
- Current reusable workflow:
  `.github/workflows/reusable-local-safety.yml`.
- Current caller workflow name: `local-fork-safety`.
- Current reusable workflow name: `reusable-local-safety`.
- Current visible job name in both workflow files: `local fork safety`.
- Y-GH-01 PR #98 was docs-only branch protection design. It observed
  `local fork safety / local fork safety` as passing.
- Y-CI-05 PR #99 was a normal docs-only observation PR. It observed
  `local fork safety / local fork safety` as passing.
- Y-CI-05 changed no workflow files and no GitHub settings.
- GitHub Actions generates checks, not commit statuses.
- GitHub required status checks can be required by branch protection or by
  rulesets.
- GitHub required status checks must pass before merge when enabled.
- GitHub docs describe reusable workflow required-check names as
  `<job name> / <reusable job name>`.
- GitHub docs warn that non-unique job names across workflows can make status
  checks ambiguous and block pull requests.
- GitHub branch protection can require pull requests and status checks, and
  force pushes and deletions are blocked by default unless allowed.
- Branch protection restrictions do not apply to admins by default, but can be
  applied to admins.
- Rulesets can work alongside branch protection rules.

Assumptions:

- Future governance should first target fork `master`.
- The observed check name is the current candidate, but two observations are
  still design evidence, not implementation approval.
- Human-approved workflow-file PRs must remain possible.
- The first governance implementation may be safer if it requires pull requests
  before merging before adding required checks.

Needs verification immediately before any future implementation:

- Exact check name in the GitHub UI/API.
- Source app or integration GitHub associates with the check.
- Whether GitHub still displays
  `local fork safety / local fork safety` after any later workflow edits.
- Whether the future implementation path uses branch protection or rulesets.
- Whether branches must be up to date before merging.
- Whether admins are included.
- Workflow-change PR exception policy.
- Rollback plan and manual recovery steps.

## Current Observations

Candidate required check name observed twice:

```text
local fork safety / local fork safety
```

Observation count:

- PR #98: Y-GH-01 docs-only branch protection design, result pass.
- PR #99: Y-CI-05 normal docs-only observation, result pass.

Current conclusion:

```text
The check name is promising, but not enough to implement required checks
automatically.
```

## Required Check Candidate

Candidate required check:

```text
local fork safety / local fork safety
```

Source:

- Observed on PR #98.
- Observed again on PR #99.

Candidate target:

```text
fork/master
```

Candidate use:

- Future branch protection required status check.
- Future ruleset required status check.

Y-GH-02 boundary:

- Y-GH-02 does not enable this check.
- Y-GH-02 does not mutate GitHub settings.
- Exact check name must be verified in the GitHub UI/API immediately before
  any future implementation.

## Main Risk: Workflow-Change PRs

Workflow-file PRs intentionally fail or block local safety because
`.github/workflows/*` is CI-scope. That is a useful safety boundary: workflow
changes should be human-reviewed and should not be treated as routine docs-only
work.

If `local fork safety / local fork safety` becomes required, future
human-approved workflow-change PRs may be blocked at merge time. The workflow
change may be correct and approved, but the required check may still fail
because local safety intentionally classifies workflow changes as CI-scope.

### Option A: Do Not Require Local Fork Safety Yet

Pros:

- Workflow changes remain possible with human review.
- No immediate branch protection or ruleset rollback pressure.
- No risk from a check name that later changes in GitHub UI/API.

Cons:

- `master` still lacks required check enforcement.
- Protection against accidental merge of failing local safety remains process
  based rather than settings enforced.

### Option B: Require Local Fork Safety With Manual Temporary Rollback

Pros:

- Stronger protection for normal PRs.
- The current candidate has two successful observations.

Cons:

- Human-approved workflow changes may require temporarily removing the required
  check or disabling a rule.
- Operational overhead increases.
- Forgetting to re-enable the check would weaken protection.
- A rushed rollback could obscure why the workflow-change PR was blocked.

### Option C: Split Workflow-Change Governance First

Pros:

- Cleaner policy before required checks are enforced.
- Workflow-change exception, manual approval, and recovery steps can be
  accepted before any settings mutation.
- Avoids weakening local safety scripts to satisfy a required check.

Cons:

- More process docs before implementation.
- Required checks remain deferred.

Recommended option:

```text
Defer actual required-check implementation until a dedicated Y-GH-03/Y-GH-04
human-approved implementation lane.
```

## Required Checks Implementation Candidate

Implementation lane:

```text
Y-GH-03 or Y-GH-04 only after explicit human approval
```

Candidate settings:

```text
target branch: master
require pull request before merging: yes
required status check: local fork safety / local fork safety
require branches to be up to date before merging: human decision
include administrators: human decision
allow force pushes: no
allow deletions: no
```

Y-GH-02 does not set these values in GitHub. They are only future
implementation candidates.

## Human Approval Fields

Any future required-check implementation must record:

- `approval_id`
- `approver`
- `date`
- target repository
- target branch pattern
- exact required check name
- source of observed check name
- whether branches must be up to date
- whether admins are included
- workflow-change PR exception policy
- rollback plan
- expected blocked scenarios
- manual recovery steps
- stop conditions

The approval must explicitly cover GitHub settings mutation. General approval
for docs, local safety, or PR creation is not enough to configure branch
protection, rulesets, required checks, or CODEOWNERS.

## Rollback Plan

Before any mutation:

- Record current branch protection and ruleset settings.
- Record whether required checks are already enabled.
- Record exact existing required-check names, if any.
- Enable one setting at a time.
- Avoid combining required checks with CODEOWNERS, required reviews, or
  rulesets in the same first implementation.

If workflow-change PRs become blocked unexpectedly:

- Temporarily remove the required check or disable the rule.
- Record the exact reason and blocked scenario.
- Merge or rework only after human approval.
- Re-enable only after confirming a normal docs-only PR passes.
- Do not weaken local safety scripts to bypass required checks.

## Recommended Decision

Recommended decision for Y-GH-02:

```text
Do not implement required checks yet.
Record local fork safety / local fork safety as the current candidate.
Proceed next to either:
  Y-DIST-07 artifact generation approval packet
  Y-GH-03 minimal branch protection implementation without required checks,
    only if explicitly approved.
```

Reason:

```text
The check name has two observations, but required checks can block expected
human-approved workflow PRs.

A minimal branch protection rule requiring PRs may be safer before requiring
checks.
```

## Stop Conditions

Stop and report facts if any of these occur:

- Actual GitHub settings mutation becomes necessary.
- Branch protection API/action is about to be called.
- Ruleset API/action is about to be called.
- Required-check API/action is about to be called.
- Required check name differs from observed value.
- Check name cannot be verified.
- Workflow-change PR exception policy is missing.
- Rollback plan is missing.
- Admin inclusion decision is unclear.
- Required checks would block expected human-approved workflow PRs without a
  recovery path.
- CODEOWNERS is requested in the same lane.
- Branch protection implementation is requested without explicit approval.
- Ruleset implementation is requested without explicit approval.
- Token, secret, cookie, or credential handling becomes necessary.
- `.github/workflows/` change becomes necessary.
- Dependency install/update, Docker operation, package output, generated
  metadata/checksum, real download, backend/frontend/package/lockfile change,
  or `.gitignore` change becomes necessary.
- PR #1001 files appear:
  `docker-compose.local.yml` or `docs/local-only.md`.
- Generated package folder appears:
  `動画保存ツール_ローカル専用/`.

## Next Candidates

```text
Y-DIST-07 artifact generation approval packet
Y-GH-03 minimal branch protection implementation without required checks,
  only with explicit human approval
Y-GH-04 required checks implementation, only with explicit human approval after
  rollback path is accepted
```

## Not Included In Y-GH-02

- No GitHub settings mutation.
- No branch protection mutation.
- No ruleset creation or mutation.
- No required-check configuration.
- No CODEOWNERS addition.
- No GitHub API or `gh` settings mutation.
- No `.github/workflows/` changes.
- No dependency install or update.
- No Docker pull/build or container image operation.
- No frontend build/test.
- No backend pytest.
- No CLEAN folder.
- No `動画保存ツール_ローカル専用/`.
- No ZIP, installer, package output, metadata, or checksum generation.
- No real download.
- No backend, frontend, Docker, package, lockfile, workflow, or `.gitignore`
  change.
- No token, secret, cookie, or credential handling.
- No PR #1001 files.
