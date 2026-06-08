# Dry-Run Update Contract

## Purpose

This document fixes the dry-run and prepare-only contract before any future
update apply implementation. It is an audit and planning record only.

No endpoint, button, backup creation, rollback creation, Docker pull, git pull /
merge / rebase, restart, pip install, package update, or update execution is
approved by this document.

## Current Readonly Inputs

The current readonly update surface is:

- `GET /update-status`
- `GET /update-preflight`

These endpoints may be used as inputs for a future plan, but they must remain
readonly. They must not apply updates, create backups, create rollback targets,
pull images, run git operations, restart the app, or install packages.

## Dry-Run Definition

Dry-run means planning only.

A future dry-run may:

- Read current update metadata.
- Read current preflight status.
- Compare current and candidate versions.
- Build a proposed plan.
- Report required confirmations.
- Report blocked reasons and stop conditions.
- Link to rollback plan requirements.

A future dry-run must not:

- Modify source, state, config, queues, downloads, Docker images, or packages.
- Create backup branches, tags, snapshots, archives, or restore points.
- Create rollback targets.
- Pull Docker images.
- Run git pull, merge, or rebase.
- Restart the app.
- Install or update packages.
- Store cookie, token, secret, or environment values.
- Treat `can_apply` as approval.

Dry-run may report whether a plan appears eligible for prepare, but its result
is advisory. Manual approval remains required for any later step.

## Prepare-Only Definition

Prepare-only means validating a specific dry-run plan and recording that the
operator has reviewed the required gates. In the initial contract, prepare-only
must not create backups or rollback targets.

A future prepare-only step may:

- Accept a dry-run plan identifier or plan digest.
- Re-run readonly checks to prevent stale approval.
- Validate that required confirmations are present.
- Return a prepare result and remaining blockers.

A future prepare-only step must not:

- Apply the update.
- Create backups.
- Create rollback targets.
- Pull Docker images.
- Run git pull, merge, or rebase.
- Restart the app.
- Install or update packages.
- Mutate download, queue, subscription, or state stores.

Backup creation and rollback target creation should remain separate operator
actions until a later task explicitly approves a narrow implementation.

## Target Classification

Future dry-run plans should classify exactly one primary target:

- `source`: fork source update or upstream-derived source candidate.
- `docker_image`: Docker image tag or digest candidate.
- `yt_dlp`: yt-dlp version candidate.
- `state_data`: state or data backup readiness plan.
- `combined`: multiple targets; should default to blocked until each target has
  its own rollback path.

Combined plans are higher risk and should not be the first implementation.

## Response Contract Candidate

A future readonly `/update-plan` response should be explicit and conservative.

Candidate fields:

- `status`: `ready`, `blocked`, `manual_required`, or `check_failed`.
- `checked_at`: ISO timestamp.
- `target`: target classification.
- `current_version`: current source version, image digest, or package version.
- `candidate_version`: candidate version, tag, digest, or commit.
- `source`: metadata source used for the candidate.
- `required_confirmations`: confirmations that must be provided later.
- `blocked_reasons`: reasons the plan cannot proceed.
- `planned_steps`: human-readable planned steps, with no execution.
- `rollback_plan_reference`: link or key for the required rollback record.
- `preflight_reference`: summary from `/update-preflight`.
- `update_status_reference`: summary from `/update-status`.
- `can_prepare`: advisory boolean for prepare-only eligibility.
- `can_apply`: must be `false` in the first readonly contract.

Initial conservative defaults:

- `can_prepare` should be `false` if any required confirmation, rollback target,
  backup decision, queue gate, version gate, or metadata gate is missing.
- `can_apply` should remain `false` until a later task explicitly approves an
  apply implementation.
- `check_failed` must be returned instead of crashing the app when metadata or
  preflight linkage fails.
- Failure details must not include credential values, environment values, URLs
  from user queues, or cookie file contents.

## Future Endpoint Boundaries

Candidate endpoint names:

- `GET /update-plan`
- `POST /update-prepare`
- `POST /update-apply`
- `POST /update-rollback`

This task does not add any of them.

Recommended boundary:

- `GET /update-plan`: readonly dry-run contract-only endpoint.
- `POST /update-prepare`: future prepare-only validation, no backup or rollback
  creation in the first prepare stage.
- `POST /update-apply`: future execution endpoint, not approved now.
- `POST /update-rollback`: future rollback endpoint, not approved now.

The first future implementation candidate should be `GET /update-plan` only.
It should not include prepare, apply, rollback, backup creation, Docker pull,
git pull / merge / rebase, restart, pip install, package update, or UI buttons.

## Stop Conditions

Dry-run and prepare-only must stop or return blocked if any condition is true:

- Dirty worktree or unclear branch.
- Current branch is upstream PR #1001 work or PR #1001 files appear in an
  unrelated fork update.
- Running downloads, queued jobs, pending jobs, or active subscription work.
- Backup not confirmed.
- Rollback target not recorded.
- Metadata check failed.
- `METUBE_VERSION=dev` requires manual review.
- Candidate version, tag, digest, commit, or changelog is unclear.
- Public bind or external exposure is detected or cannot be ruled out.
- Config or environment source is unknown.
- Cookie, token, or secret value appears in output.
- Docker registry ambiguity.
- CI or local verification failure.
- Any step would require update execution outside the approved scope.

## UI Constraints

Future UI should start with display only.

Allowed candidates:

- Readonly update plan display.
- Required confirmations list.
- Blocked reasons list.
- Planned steps preview.
- Rollback plan reference display.

Not allowed for the first dry-run / prepare stage:

- Apply button.
- Prepare button.
- Rollback button.
- Automatic background update.
- Any view that exposes cookie, token, secret, or environment values.

## Minimum Next PR Candidate

Y-05J implemented the readonly `GET /update-plan` contract-only endpoint, and
Y-05K-R verified it at runtime with blocked defaults, `can_prepare: false`, and
`can_apply: false`.

The next safest candidate is Y-05L planning. Prefer a small readonly
plan/preflight UI display or a closeout decision. The scope must still exclude:

- update execution
- update prepare endpoint
- update apply endpoint
- update rollback endpoint
- backup creation
- rollback creation
- Docker pull
- git pull / merge / rebase
- restart
- pip install or package update
