# Handoff

## Short Context

This is `youtubeダウンロード / MeTube local-only fork`, a personal local-only fork of
MeTube. The canonical branch is fork `master`, and local `master` tracks
`fork/master`.

## Read First

1. `docs/llmwiki/current-state.md`
2. `docs/llmwiki/safety-boundaries.md`
3. `docs/llmwiki/roadmap.md`
4. `docs/llmwiki/update-rollback-plan.md`
5. `docs/llmwiki/manual-update-apply-design.md`

## Key Points For Codex

- Keep work local-only and personal-use scoped.
- Do not touch upstream PR #1001 unless explicitly asked.
- Do not mix `docker-compose.local.yml` or `docs/local-only.md` into fork-only work.
- Do not handle real cookies, tokens, secrets, DRM bypass, authentication bypass, or
  restriction circumvention.
- `update-status` is readonly. It must not apply updates, pull Docker images,
  run git updates, restart the app, or install packages.
- Backup and rollback requirements must be satisfied before any update-apply
  implementation begins.
- `update-preflight` is readonly. It reports backup / rollback readiness and
  must not execute updates, create backups, create rollback targets, pull Docker
  images, run git updates, restart the app, or install packages.
- Y-05G readonly update preflight report was merged in fork PR #7
  (`bfbecdb`).
- Y-05H manual-approval update apply design is docs-only. It defines future
  confirmation flow, stop conditions, rollback hand-off, and API/UI boundaries
  without approving update execution.

## Next Step

Proceed to Y-05I dry-run / prepare-only update apply contract audit. Keep it
docs-only or readonly contract-only unless a later task explicitly approves
implementation.
