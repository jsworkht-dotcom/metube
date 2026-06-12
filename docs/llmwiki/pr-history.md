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

## Fork PR #11

- Target repository: `jsworkht-dotcom/metube`
- Purpose: readonly `/update-plan` contract-only endpoint
- Status: merged
- PR URL: `https://github.com/jsworkht-dotcom/metube/pull/11`
- Merge commit: `341ca569492315f03ac234de75f1fb72646b7e30`
- Changed files:
  - `app/main.py`
  - `app/update_plan.py`
  - `app/tests/test_update_plan.py`
  - `docs/llmwiki/current-state.md`
  - `docs/llmwiki/handoff.md`
  - `docs/llmwiki/roadmap.md`
- Runtime verification: Y-05K-R succeeded with blocked defaults and
  `can_prepare: false` / `can_apply: false`.
- Not included: update execution, prepare/apply/rollback endpoints, update
  button, backup creation, rollback creation, Docker pull, git pull / merge /
  rebase, restart, or pip install / package update.

## Fork PR #12

- Target repository: `jsworkht-dotcom/metube`
- Purpose: close out successful readonly `/update-plan` runtime verification
- Status: merged
- PR URL: `https://github.com/jsworkht-dotcom/metube/pull/12`
- Merge commit: `c9e14bf3a14a12be47b02304e02ecece13b2f5e7`
- Scope: docs-only Y-05K-R runtime verification closeout.
- Result: `/update-plan` was verified at runtime with `overall: blocked`,
  `can_prepare: false`, `can_apply: false`, non-empty blocked reasons, planned
  steps, and rollback/doc references.
- Not included: update execution, backup creation, rollback creation, Docker
  pull, git pull / merge / rebase, restart, or pip install / package update.

## Fork PR #86

- Target repository: `jsworkht-dotcom/metube`
- Purpose: add a report-only CLEAN portable distribution metadata checker.
- Status: merged
- PR URL: `https://github.com/jsworkht-dotcom/metube/pull/86`
- Merge commit: `00a90bfa1efd11935aa46b07848d05614d1c744e`
- Changed files:
  - `scripts/check_distribution_metadata.py`
  - `app/tests/test_distribution_metadata_checker_unittest.py`
  - `docs/llmwiki/distribution-metadata-verification.md`
  - `docs/llmwiki/clean-portable-distribution-manifest.md`
  - `docs/llmwiki/current-state.md`
  - `docs/llmwiki/handoff.md`
  - `docs/llmwiki/roadmap.md`
  - `docs/llmwiki/safety-boundaries.md`
- GitHub operations note:
  - connector ready-for-review failed with
    `Resource not accessible by integration`;
  - human-approved escalated `gh` fallback marked the PR ready;
  - squash merge used an expected head SHA guard;
  - remote branch `codex/y-dist-02-metadata-checker` was deleted.
- Not included: metadata generation, checksum generation, CLEAN folder, ZIP,
  installer, package output, dependency installation operations, Docker
  operations, real download, or token/secret/cookie value handling.
