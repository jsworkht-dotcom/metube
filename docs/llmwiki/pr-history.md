# PR History

## Upstream PR #1001

- Target repository: `alexta69/metube`
- Purpose: local-only Docker profile documentation and compose support
- Status: Ready for review
- Keep its files out of unrelated fork PRs while it remains open.

## Fork PR #1

- Target repository: `jsworkht-dotcom/metube`
- Purpose: Japanese static UI copy for the local-only fork
- Status: merged
- Merge commit: `0cc8dd602ccaa0944630c56322e6b753133f6961`

## Fork PR #2

- Target repository: `jsworkht-dotcom/metube`
- Purpose: readonly update-status baseline
- Status: merged
- Merge commit: `37256d5b8a885aac0f7e323f413409769055cc83`

## Fork PR #4

- Target repository: `jsworkht-dotcom/metube`
- Purpose: show `METUBE_VERSION=dev` as development status instead of an
  update-check failure
- Status: merged
- PR URL: `https://github.com/jsworkht-dotcom/metube/pull/4`
- Merge commit: `af6987532a741cd680d8b747562b2f2971b9c229`

## Fork PR #7

- Target repository: `jsworkht-dotcom/metube`
- Purpose: readonly update preflight report for backup and rollback readiness
- Status: merged
- PR URL: `https://github.com/jsworkht-dotcom/metube/pull/7`
- Merge commit: `bfbecdb`
- Changed files:
  - `app/main.py`
  - `app/update_preflight.py`
  - `app/tests/test_update_preflight.py`
- Not included: update execution, backup creation, rollback creation, Docker pull,
  git pull / merge / rebase, restart, or pip install / package update.
