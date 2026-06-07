# Manual Update Apply Design

## Purpose

This document audits the future manual-approval update apply flow for the
local-only MeTube fork. It is a design record only. It does not approve or
implement update execution.

The current allowed behavior remains:

- `/update-status` reports readonly update metadata.
- `/update-preflight` reports readonly backup / rollback readiness.
- Future update apply work must stop unless manual approval, backup, rollback,
  and local-only safety gates are all satisfied.

## Non-Goals

- No update execution.
- No update apply endpoint.
- No update button.
- No backup creation.
- No rollback creation.
- No Docker pull.
- No git pull, merge, or rebase.
- No restart.
- No pip install or package update.
- No cookie, token, or secret handling.
- No public hosting, ads, DRM bypass, authentication bypass, restriction
  circumvention, or mass-download optimization.

## Update Target Classification

### Source / Fork Update

Source updates cover fork `master`, local branches, and any future upstream
merge candidate. A future apply flow must treat source updates as explicit
operator actions, not automatic git operations.

Required records before any future source apply:

- Current fork `master` commit.
- Current local branch.
- Worktree cleanliness result.
- Tracking relationship to `fork/master`.
- Candidate source commit, tag, branch, or PR.
- Whether the candidate is fork-only or upstream-derived.
- Backup branch or tag pointing to the exact pre-update source commit.

Stop if the worktree is dirty, the branch is unclear, upstream PR #1001 files
appear in an unrelated update, or the candidate cannot be compared safely.

### Docker Image Update

Docker image updates are separate from source updates. A future apply flow must
not assume GHCR and Docker Hub are equivalent unless the image digest is
explicitly recorded and compared.

Required records before any future Docker apply:

- Current image repository, tag, and digest or image ID when available.
- Whether the runtime uses an official image or fork-built image.
- Current bind mounts and environment source locations.
- Current `METUBE_VERSION` value.
- Rollback image tag or digest.

Stop if the current image cannot be identified, the registry is ambiguous, or
the operator has not chosen whether Docker image updates are in scope.

### yt-dlp Update

yt-dlp updates may arrive through the image, source dependency lockfile, or the
existing nightly startup update behavior. A future apply flow must not use pip
downgrade as rollback and must not change extractor code.

Required records before any future yt-dlp apply:

- Current `/version` response.
- Current yt-dlp version source: image, lockfile, or runtime behavior.
- Whether `YTDL_NIGHTLY_UPDATE_TIME` is enabled.
- Rollback mechanism, preferably source commit or Docker image rollback.

Stop if the version source is unclear or a change would require package
installation from the app path.

### State / Data Backup

State and downloaded media must be handled separately. `STATE_DIR` should be
backed up as a unit before future update apply work. Downloaded media may be
large, so the operator must decide whether to back it up, snapshot it, or leave
it unchanged.

Required records before any future state/data apply:

- `STATE_DIR` backup status.
- `DOWNLOAD_DIR`, `AUDIO_DOWNLOAD_DIR`, and `TEMP_DIR` existence.
- Download backup or no-backup decision.
- Config and environment source locations.
- Queue, pending, completed, and subscription store readability.

Do not inspect, print, store, or document secret-bearing file contents. For
cookie or secret-bearing files, record only presence, category, and backup
status.

## Manual Approval Flow

### 1. Scope Confirmation

The operator confirms the update is local-only, personal-use only, and not
related to public hosting, monetization, external users, DRM bypass,
authentication bypass, restriction circumvention, or mass-download
optimization.

### 2. Update Status Review

The operator reviews `/version` and `/update-status`.

Required outcomes:

- Metadata check succeeds, or the failure is treated as a stop condition.
- `METUBE_VERSION=dev` is treated as development / manual review, not as a
  metadata failure.
- Docker image status remains separate when it is not checked automatically.

### 3. Preflight Review

The operator reviews `/update-preflight`.

Required outcomes:

- Queue is empty or the app is stopped with no active jobs.
- State/download directories are configured and exist.
- Source, backup, Docker, and update status checks are reviewed.
- `can_apply_update` remains informational and must not override manual gates.

### 4. Backup And Rollback Confirmation

The operator confirms:

- Source rollback target is recorded.
- Docker rollback target is recorded when Docker is in use.
- `STATE_DIR` backup is complete.
- Download backup or no-backup decision is recorded.
- yt-dlp rollback path is identified.

Any missing backup or rollback target is a stop condition.

### 5. Version And Changelog Review

The operator reviews the candidate version, source diff or changelog, and any
fork-only conflict risk.

Stop if the candidate version is unclear, the changelog cannot be reviewed, or
the change scope crosses into forbidden areas.

### 6. Explicit Confirmation

Future apply work must require explicit, current, single-use confirmation for
the specific update target. The confirmation should include:

- Target type: source, Docker image, yt-dlp, or state/data.
- Current version or commit.
- Candidate version or commit.
- Recorded rollback target.
- Acknowledgement that backup has completed.

Confirmation must not be stored with credential values and must not approve a
different later update attempt.

### 7. Apply Boundary

This design does not approve an apply endpoint or apply button. A future apply
task must separately define the exact command boundaries, execution environment,
failure behavior, and rollback handoff before implementation.

If an apply attempt fails, stop and report the failed gate or command. Do not
attempt complex automatic recovery in the first implementation.

### 8. Post-Check

After any future approved update, verify:

- `/version` responds.
- `/update-status` responds and does not crash the app.
- `/update-preflight` responds and still reports any remaining manual gates.
- Footer displays the expected update state.
- Queue, completed list, and subscriptions can load.
- Logs do not show secret values.
- No unexpected update loop or restart loop is active.

## UI / UX Candidates

The UI should stay quiet and local-only. Future update controls should live in a
small settings/status area, not in the download workflow.

Safe candidates:

- Readonly update status display.
- Readonly preflight report display.
- Manual confirmation checklist.
- Disabled apply affordance until all gates are satisfied.

Not for the first apply-related implementation:

- Automatic apply button.
- Background update scheduler.
- One-click update without showing rollback targets.
- Public admin surface.
- Any UI that displays cookie, token, secret, or environment values.

## Future API Candidates

Existing readonly endpoints remain:

- `GET /update-status`
- `GET /update-preflight`

Future API boundaries should keep planning, preparation, and execution
separate. Candidate names:

- `GET /update-plan`: compute a proposed plan only.
- `POST /update-prepare`: validate a specific plan and record operator
  confirmation only after all gates pass.
- `POST /update-apply`: future execution endpoint, not approved now.

The first future API step should be dry-run or prepare-only. It must not run
Docker pull, git pull / merge / rebase, restart, pip install, package update, or
backup/rollback creation unless a later task explicitly approves that specific
behavior.

## Stop Conditions

Stop before applying or continuing if any condition is true:

- Dirty worktree.
- Current branch or tracking relationship is unclear.
- Upstream PR #1001 files appear in unrelated fork work.
- Running downloads, queued jobs, pending jobs, or active subscription work.
- Backup not confirmed.
- Rollback target not recorded.
- Version, tag, digest, changelog, or candidate source is unclear.
- Metadata check failed.
- Public bind or external exposure is detected or cannot be ruled out.
- Config or environment source is unknown.
- Cookie, token, or secret value appears in output.
- Docker registry ambiguity.
- CI or local verification failure.
- Any required step would need update execution outside the approved scope.

## Rollback Hand-Off

Future apply work should hand rollback to explicit operator steps:

- Source: return to the recorded pre-update commit, tag, or backup branch.
- Docker: return to the recorded image tag or digest.
- State/data: restore `STATE_DIR` from the immediate pre-update backup.
- yt-dlp: return through source or Docker rollback, avoiding pip downgrade.

The first implementation should stop after reporting a failure. It should not
chain automatic rollback actions unless a later design explicitly narrows and
approves that behavior.

## Minimum Future PR Candidate

Y-05I documents the dry-run / prepare-only contract in
`docs/llmwiki/dry-run-update-contract.md`.

The next safe PR candidate is Y-05J readonly `/update-plan` contract-only
endpoint. It must remain readonly, use blocked defaults, and exclude prepare,
apply, rollback, backup creation, Docker pull, git pull / merge / rebase,
restart, pip install, and package update.
