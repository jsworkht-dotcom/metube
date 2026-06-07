# Update Rollback Plan

## Purpose

This document fixes the backup and rollback requirements that must exist before
any future manually approved update-apply feature is designed or implemented.

The current approved scope is audit and planning only. The readonly
`/update-status` endpoint may report update state, but it must not apply
updates.

## Non-Goals

- No automatic update application
- No update execution button
- No Docker image replacement
- No source merge, rebase, or pull automation
- No restart automation
- No pip install, package update, or yt-dlp downgrade automation
- No cookie, token, or secret handling
- No public hosting or ad workflow

## Rollback Principles

- Prefer explicit manual rollback steps over complex self-healing automation.
- Stop on uncertainty instead of trying to repair multiple failure modes.
- Record rollback targets before changing anything.
- Keep source, Docker image, state/data, and yt-dlp rollback decisions separate.
- Do not continue if any backup or rollback target is missing.

## Source Rollback

### What To Record

- Current fork `master` commit.
- Current local branch and worktree cleanliness.
- Candidate update commit or branch.
- Whether the update comes from fork-only work or upstream.
- Any fork-only differences that may conflict with upstream changes.

### Backup Target

Before future update application, create or record a rollback target that points
to the exact pre-update fork `master` commit. A backup branch or tag is
acceptable if it is local-only and clearly named for the update attempt.

### Rollback Policy

- Roll back source only to the recorded pre-update commit, tag, or backup branch.
- Do not mix source rollback with Docker image or state rollback unless the
  operator explicitly chooses that combined rollback.
- Do not use automated pull, merge, or rebase steps as part of rollback.
- If conflicts appear before applying an update, stop before changing source.

## Docker Rollback

### What To Record

- Current image repository, tag, and image ID or digest when available.
- Whether the runtime uses the official upstream image or a fork-built image.
- Current bind mounts and environment file locations.
- Current `METUBE_VERSION` value if set by the image or runtime environment.

### Registry Boundary

GHCR and Docker Hub can publish different tags, metadata, or timing. Future
automation must not infer equivalence between registries unless the digest is
explicitly verified and recorded.

### Rollback Policy

- Prefer returning to the recorded image tag or digest.
- Do not replace an official image with a fork-built image without an explicit
  operator decision.
- Do not run image pulls automatically.
- If the existing image reference cannot be identified, stop before applying an
  image update.

## State And Data Rollback

### What To Record

- `STATE_DIR`.
- `DOWNLOAD_DIR`.
- `AUDIO_DOWNLOAD_DIR`.
- `TEMP_DIR`.
- Config and environment source locations.
- Whether `YTDL_OPTIONS_FILE` or `YTDL_OPTIONS_PRESETS_FILE` is used.

### State Files

MeTube stores persistent state under `STATE_DIR`, including:

- `queue.json`
- `pending.json`
- `completed.json`
- `subscriptions.json`
- uploaded cookie state if present

Do not inspect, print, copy into docs, or expose secret-bearing file contents.
For any cookie or secret-bearing file, record only presence, path category, and
backup status.

### Backup Target

Before future update application, back up `STATE_DIR` as a unit. Downloaded
media under `DOWNLOAD_DIR` may be large; the operator must explicitly decide
whether to back it up, snapshot it, or leave it unchanged.

### Rollback Policy

- Restore `STATE_DIR` only from the backup taken immediately before the update.
- Treat downloads as user data and avoid deleting or overwriting media during
  automated rollback.
- If state schema, queue shape, or subscription format is unclear, stop before
  applying the update.
- If running jobs exist, stop before backup and do not apply the update.

## yt-dlp Rollback

### What To Record

- Current `/version` response for `yt-dlp`.
- Current `uv.lock` version relationship when using a source or fork-built
  runtime.
- Current image tag or digest when using Docker.
- Whether `YTDL_NIGHTLY_UPDATE_TIME` is enabled.

### Rollback Policy

- Prefer rolling back by returning to the previous source commit or Docker image.
- Avoid pip downgrade as a rollback mechanism.
- If nightly yt-dlp updates are enabled, require the operator to disable or
  account for them before update application.
- Do not change extractor code as part of rollback.

## Update Preflight

All future update-apply work must stop unless every item below is true:

- Worktree is clean.
- Source rollback target is recorded.
- Docker image rollback target is recorded when Docker is in use.
- `STATE_DIR` backup completed.
- Download backup or no-backup decision is recorded.
- Queue is empty or the app is stopped with no active jobs.
- Current `/version` and `/update-status` are recorded.
- Candidate version and changelog are reviewed.
- Local-only scope is confirmed.
- Manual approval is explicit and current for this specific update.
- No cookie, token, or secret value has been read or displayed.

## Update Post-Check

After any future manually approved update, verify:

- `/version` responds.
- `/update-status` responds and does not crash the app.
- Footer displays the expected update state.
- Queue, completed list, and subscriptions can load.
- A small no-op UI navigation works.
- Logs do not show secret values.
- No unexpected update loop or restart loop is active.

## Stop Conditions

Stop immediately before applying or continuing an update if any condition below
is true:

- Dirty worktree.
- Source conflict.
- CI or local verification failure.
- Backup failure.
- Missing rollback target.
- Unclear version, tag, digest, or changelog.
- Active downloads, queued jobs, or subscription checks that cannot be paused.
- Unknown config or environment source.
- Secret, token, or cookie value appears in output.
- Docker image registry ambiguity.
- Any step would require public hosting, ads, DRM bypass, authentication bypass,
  restriction circumvention, or mass-download optimization.

## Minimal Future Implementation Candidate

The next safe implementation step is not update application. It is a local-only
preflight report that checks and displays whether the required rollback
information is present. It should not apply updates, change source, pull images,
restart the app, install packages, or inspect secret values.
