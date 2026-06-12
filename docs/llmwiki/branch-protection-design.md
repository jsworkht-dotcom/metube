# Y-GH-01 Branch Protection / Ruleset Design

## Purpose

Y-GH-01 records a docs-only candidate strategy for protecting fork `master`.

This PR does not change GitHub branch protection, repository rulesets, required
checks, CODEOWNERS, repository settings, or workflow files. It only records
candidate settings, risks, staged adoption, approval requirements, rollback
expectations, and stop conditions for a later explicit human-approved lane.

## Sources Checked

Repository sources:

- `docs/llmwiki/current-state.md`
- `docs/llmwiki/roadmap.md`
- `docs/llmwiki/handoff.md`
- `docs/llmwiki/reusable-local-safety-workflow-design.md`
- `docs/llmwiki/lightweight-safety-workflow-design.md`
- `docs/llmwiki/codex-automation-policy.md`
- `docs/llmwiki/automation-efficiency-policy.md`
- `.github/workflows/local-fork-safety.yml`
- `.github/workflows/reusable-local-safety.yml`

Official GitHub docs checked on 2026-06-12:

- Protected branches:
  `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches`
- Rulesets:
  `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets`
- Available rules for rulesets:
  `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets`

## Facts / Assumptions / Needs Verification

Facts:

- Canonical branch: fork `master`.
- Latest Y-CI-04 merge baseline: `becdf346956cb61b985df93637ab5c121884e49c`.
- Current PR-facing workflow: `.github/workflows/local-fork-safety.yml`.
- Current reusable workflow:
  `.github/workflows/reusable-local-safety.yml`.
- Current workflow name: `local-fork-safety`.
- Current reusable workflow name: `reusable-local-safety`.
- Current visible job name in both workflow files: `local fork safety`.
- Initial Y-GH-01 PR observation: GitHub displayed the passing check as
  `local fork safety / local fork safety` on PR #98. Treat this as one
  observation, not enough stability evidence to configure required checks.
- Y-CI-05 is the follow-up normal docs-only observation lane. It records one
  more displayed check-name observation before Y-GH-02.
- Y-CI-05 PR #99 observed the same displayed passing check name:
  `local fork safety / local fork safety`. This is useful input for Y-GH-02,
  but it still does not enable required checks by itself.
- Current caller uses workflow-level concurrency:
  `group: ${{ github.workflow }}-${{ github.ref }}` and
  `cancel-in-progress: true`.
- Both workflows keep `permissions: contents: read`.
- Normal docs-only PRs are expected to pass `local-fork-safety`.
- Workflow-file PRs can be expected CI-scope blockers unless a human approves
  that scope.
- `local-fork-safety` is a PR visibility layer. It is not approval for package,
  ZIP, installer, metadata, checksum, or CLEAN folder generation.
- GitHub protected branches can require pull requests, reviews, status checks,
  conversation resolution, signed commits, linear history, merge queue, and
  deployment success, and can block or allow force pushes and deletions.
- GitHub branch protection docs warn that required status check job names
  should be unique enough to avoid ambiguous status check results.
- Only one branch protection rule applies to a branch at a time.
- Rulesets can work alongside branch protection rules.
- Multiple rulesets can apply at the same time and their rules are aggregated.
- Rulesets have enforcement statuses, including active and disabled.

Assumptions:

- Future branch governance should first target only fork `master`.
- The first useful protection is preventing accidental direct changes to
  `master`, not requiring reviews or CODEOWNERS.
- Required status checks are valuable only after check naming is observed to be
  stable on normal PRs.
- Human-approved workflow-file PRs must remain possible.

Needs verification before any future implementation:

- Repeat observation of the exact displayed check name on at least one later
  normal docs-only PR after Y-CI-04 / Y-GH-01.
- Whether GitHub presents the required-check candidate as
  `local-fork-safety / local fork safety`, `reusable-local-safety / local fork
  safety`, `local fork safety / local fork safety`, or another nested check
  name.
- Whether the displayed check name remains stable across docs-only PRs and
  workflow-file PRs.
- Whether requiring the local safety check would block a later human-approved
  workflow change.
- Whether the repository owner wants admins included in enforcement.
- Whether the repository owner wants branch protection rules or rulesets for
  the first implementation.

## Current State

The current canonical branch is fork `master`. The current safety signal is the
`local-fork-safety` pull request workflow:

```text
.github/workflows/local-fork-safety.yml
.github/workflows/reusable-local-safety.yml
```

`local-fork-safety.yml` is the PR visibility layer. It runs on pull requests
targeting `master`, owns workflow-level concurrency, and calls
`reusable-local-safety.yml`. The reusable workflow owns the local safety job
steps.

Current check behavior:

- Normal docs-only PRs are expected to pass.
- Workflow-file PRs can be expected CI-scope blockers because
  `.github/workflows/*` changes require human review.
- The safety workflow reports PR risk and blockers, but success does not
  approve artifact generation, GitHub settings changes, workflow changes, or
  merge.

## Design Goals

- Protect fork `master` from accidental direct changes.
- Keep the local-only and no-generation policy visible.
- Avoid blocking safe docs-only work unnecessarily.
- Avoid making expected workflow-change blockers impossible to merge after
  human approval.
- Avoid branch protection changes before check naming is stable.
- Keep human approval explicit for CI-scope, artifact-generation, workflow,
  package, branch-governance, required-check, or CODEOWNERS changes.
- Keep branch governance separate from workflow implementation and package
  generation lanes.

## Branch Protection Candidate

Status for Y-GH-01: do not configure this yet.

Future candidate target:

```text
target branch: master
repository: jsworkht-dotcom/metube
```

Candidate settings for a later human-approved implementation:

- Require pull request before merging: candidate yes.
- Require status checks before merging: candidate only after check naming is
  stable.
- Require conversation resolution before merging: optional human decision.
- Require linear history: optional human decision; consider the current
  squash-only practice before enabling.
- Allow force pushes: no.
- Allow deletions: no.
- Apply restrictions to administrators / do not allow bypassing: human
  decision.
- Required reviews: do not enable in the first branch-protection pass unless a
  separate human approval says so.
- CODEOWNERS review: do not enable in this lane.
- Merge queue: do not enable in this lane.
- Required deployments: do not enable in this lane.
- Required signed commits: do not enable in this lane.

Recommended first implementation, if approved later:

1. Add a single minimal branch protection rule for `master`.
2. Require pull requests before merging.
3. Keep required checks disabled until a later required-check decision.
4. Keep required reviews and CODEOWNERS disabled.
5. Keep force pushes and deletions blocked.
6. Record previous settings before mutation.

## Required Checks Candidate

Status for Y-GH-01: do not enable required status checks yet.

Initial observed check on PR #98:

```text
local fork safety / local fork safety
```

Earlier design candidates expected a workflow/job-shaped display such as
`local-fork-safety / local fork safety`. The PR #98 observation confirms that
the reusable workflow split can produce a less obvious check name. Do not use
this single observation as enough evidence to configure required checks.

Known issue:

- Workflow-change PRs intentionally touch `.github/workflows/*`.
- Repository safety may classify workflow-file changes as CI-scope blockers.
- If `local-fork-safety` becomes required immediately, a future
  human-approved workflow PR may become impossible to merge without changing
  settings first.

Check-name ambiguity risk:

- Required check names must be unique enough.
- The reusable workflow split can affect displayed check names.
- The caller workflow and reusable workflow both use the job name
  `local fork safety`.
- GitHub may display workflow/job names in a way that makes the exact required
  check unclear.
- Do not configure required checks until the exact displayed check name is
  observed and stable across normal PRs.

Design recommendation:

- Do not enable required checks in Y-GH-01.
- First observe a normal docs-only PR after Y-CI-04.
- Record the exact displayed check name and GitHub check conclusion.
- Consider a later Y-GH-02 required checks design before any implementation.
- If required checks are later approved, start with one exact check name and a
  documented rollback path.

## Branch Protection vs Rulesets

Branch protection:

- Simpler for one protected branch.
- Familiar PR settings for requiring PRs, status checks, linear history, and
  conversation resolution.
- GitHub applies only one branch protection rule at a time to a branch.
- Good first fit if the only target is fork `master`.

Rulesets:

- Can coexist with branch protection.
- Multiple rulesets can apply at the same time.
- Rules from applicable rulesets are aggregated.
- Enforcement status can be active or disabled.
- Useful for future auditability and staged activation.
- May be more than this local-only fork needs for the first branch governance
  step.

Current recommendation:

```text
Y-GH-01: design-only
Y-GH-02: required checks design, if needed
Y-GH-03: actual branch protection / ruleset implementation only after explicit human approval
```

If branch protection is enough for fork `master`, prefer branch protection for
the first implementation. Use rulesets later only if auditability, layering, or
broader branch/tag targeting becomes necessary.

## What Not To Configure Yet

Do not configure any of these in Y-GH-01:

- Branch protection mutation.
- Ruleset creation.
- Ruleset mutation.
- Required status checks.
- Required reviews.
- CODEOWNERS.
- Admin bypass configuration.
- Force-push or deletion settings changes.
- Merge queue.
- Deployment requirement.
- Signed commit requirement.
- GitHub repository settings mutation.
- GitHub API or `gh` settings mutation.

## Recommended Staged Plan

Stage 0: Y-GH-01 docs-only design.

- Add this design doc.
- Keep existing docs updates limited to references.
- Do not mutate GitHub settings.

Stage 1: observe post-Y-CI-04 PR behavior.

- Use a normal docs-only PR. Y-CI-05 is the current candidate.
- Confirm exact displayed check name.
- Confirm `local-fork-safety` success for a non-workflow docs-only diff.

Stage 2: optional Y-GH-02 required checks design.

- Decide whether `local-fork-safety` should become required.
- Record the exact required check name.
- Decide how future human-approved workflow PRs would be handled.
- Define a rollback plan.

Stage 3: optional Y-GH-03 branch protection implementation.

- Requires explicit human approval.
- Start with the smallest branch-protection mutation.
- Prefer requiring pull requests before merging before adding required checks.

Stage 4: optional ruleset design or implementation.

- Use only if branch protection is insufficient.
- Consider disabled ruleset draft status for review before active enforcement.

## Human Approval Requirements

Any future GitHub settings change must record:

- `approval_id`
- `approver`
- `date`
- target repository
- target branch pattern
- exact setting to change
- required check names, if any
- whether admins are included
- bypass policy
- rollback plan
- expected effect on workflow-change PRs
- stop conditions

Approval must be explicit for branch protection, ruleset, required-check,
CODEOWNERS, repository settings, workflow, package, artifact-generation, or
CI-scope changes.

## Rollback / Escape Plan

Before mutation:

- Record current branch protection and ruleset settings.
- Record whether required checks are enabled.
- Record the exact required check names.
- Keep the first mutation small.
- Avoid combining branch protection with CODEOWNERS, required reviews, or
  required checks in the same first implementation.

If PRs become blocked unexpectedly:

- Do not weaken local safety scripts to work around GitHub settings.
- Revert the GitHub setting manually.
- Record the exact setting that caused the blockage.
- Re-run the previously blocked PR checks after rollback.
- Move any required-check follow-up back into design before retrying.

## Stop Conditions

Stop and report facts if any of these occur:

- Actual GitHub settings mutation becomes necessary.
- A branch protection or ruleset API/action is about to be called.
- Required status check name is ambiguous.
- `local-fork-safety` check name is not stable.
- Required checks would block expected human-approved workflow PRs.
- Admin bypass policy is unclear.
- Rollback plan is missing.
- CODEOWNERS is requested in the same lane.
- Branch protection implementation is requested without explicit approval.
- Ruleset implementation is requested without explicit approval.
- Token, secret, cookie, or credential handling becomes necessary.
- Dependency install/update, Docker operation, package output, generated
  metadata/checksum, real download, backend/frontend/package/lockfile change,
  workflow change, or `.gitignore` change becomes necessary.
- PR #1001 files appear:
  `docker-compose.local.yml` or `docs/local-only.md`.
- Generated package folder appears:
  `動画保存ツール_ローカル専用/`.

## Next Candidates

Recommended after Y-CI-05 if the observation succeeds:

```text
Y-GH-02 required checks design
```

Y-CI-05 is still only one additional observation. Required-check implementation
remains too early until Y-GH-02 explicitly designs the exact required-check
candidate and rollback path.

Other candidates:

```text
Y-GH-03 branch protection implementation, only with explicit human approval
Y-WIKI-CLEAN-01 current-state / handoff / archive整理
```

## Not Included In Y-GH-01

- No branch protection mutation.
- No ruleset creation or mutation.
- No required-check configuration.
- No required reviews.
- No CODEOWNERS addition.
- No GitHub repository settings mutation.
- No GitHub API or `gh` settings mutation.
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
