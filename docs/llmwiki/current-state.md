# Current State

## Project

- Project: `youtubeダウンロード / MeTube local-only fork`
- Repository: `C:\Users\tomikyo\_projects\youtubeダウンロード`
- Upstream remote: `origin -> https://github.com/alexta69/metube.git`
- Fork remote: `fork -> https://github.com/jsworkht-dotcom/metube.git`
- Local `master` tracks `fork/master`
- Current source of truth: fork `master`

## Repository State

- This project is local-only and for personal use.
- Do not open PRs against upstream `alexta69/metube` unless explicitly requested for a
  separate upstream contribution.
- Do not mix upstream PR #1001 files into fork-only work.

## Completed Work

### Y-03 local-only Docker profile

- Upstream PR #1001 is Ready for review.
- Branch `local-only-docker-profile` remains while PR #1001 is open.
- Keep `docker-compose.local.yml` and `docs/local-only.md` out of unrelated fork work.

### Y-04 Japanese static UI copy

- Fork PR #1 was merged.
- Merge commit: `0cc8dd602ccaa0944630c56322e6b753133f6961`
- Scope: static Japanese UI copy for the fork.

### Y-05 readonly update-status

- Fork PR #2 was merged.
- Merge commit: `37256d5b8a885aac0f7e323f413409769055cc83`
- Scope: readonly update-status baseline.

### Y-05D runtime verification

- Runtime verification confirmed `/update-status` remains readonly.
- `METUBE_VERSION=dev` was found to display `更新確認失敗` even when metadata
  fetches succeeded, because `dev` could not be compared with release tags.
- `METUBE_VERSION=2026.06.06` displayed `最新`.
- `METUBE_VERSION=0.0.0` displayed `更新あり`.
- No update execution, Docker pull, git pull, restart, pip install, or
  cookie/token/secret exposure was observed.

### Y-05E dev version status fix

- Fork PR #4 was merged.
- Merge commit: `af6987532a741cd680d8b747562b2f2971b9c229`
- Scope: treat `METUBE_VERSION=dev` as `development` and show `開発版` in
  the footer while preserving real `check_failed` behavior.

### Y-05G readonly update preflight report

- Fork PR #7 was merged.
- PR URL: `https://github.com/jsworkht-dotcom/metube/pull/7`
- Merge commit: `bfbecdb`
- Scope: readonly update preflight report for backup and rollback readiness.
- Changed files:
  - `app/main.py`
  - `app/update_preflight.py`
  - `app/tests/test_update_preflight.py`
- Implemented:
  - readonly `/update-preflight` report
  - backup / rollback readiness JSON report
  - update apply readiness as information only with `can_apply_update: false`
- Not implemented:
  - update execution
  - backup creation
  - rollback creation
  - Docker pull
  - git pull / merge / rebase
  - restart
  - pip install / package update

### Y-05H manual-approval update apply design audit

- Scope: docs-only design audit for future manual-approval update apply.
- Design document: `docs/llmwiki/manual-update-apply-design.md`
- Defines:
  - update target classification for source, Docker, yt-dlp, and state/data
  - manual approval flow
  - future UI/API boundaries
  - stop conditions
  - rollback hand-off requirements
- Not implemented:
  - update execution
  - update apply endpoint
  - update button
  - backup creation
  - rollback creation
  - Docker pull
  - git pull / merge / rebase
  - restart
  - pip install / package update

## Current Next Step

Proceed to Y-05I dry-run / prepare-only update apply contract audit. Keep it
docs-only or readonly contract-only unless a later task explicitly approves
implementation.
