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
6. `docs/llmwiki/dry-run-update-contract.md`
7. `docs/llmwiki/codex-gh-auth-runbook.md` if GitHub CLI auth, PR creation,
   checks, or merge commands fail inside Codex

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
- Y-05I dry-run / prepare-only contract is docs-only. It defines dry-run as
  readonly planning only and prepare-only as validation only, with no backup or
  rollback creation in the first prepare stage.
- `update-plan` is readonly. It reports a blocked-by-default update plan with
  `can_prepare: false` and `can_apply: false`. It must not execute updates,
  prepare updates, create backups, create rollback targets, pull Docker images,
  run git updates, restart the app, or install packages.
- Y-05K-R runtime verification succeeded after Docker recovery. `/update-plan`
  returned `overall: blocked`, `can_prepare: false`, `can_apply: false`,
  non-empty `blocked_reasons`, non-empty `planned_steps`, and rollback/doc
  references. `/update-status` was `latest`; `/update-preflight` was
  `not_ready` with `can_apply_update: false`; `/version` reported
  `2026.06.06` and yt-dlp `2026.03.17`.
- Y-05 readonly update readiness is closed out for now. Update execution,
  prepare, apply, rollback, update buttons, backup creation, Docker pull, git
  pull / merge / rebase, restart, pip install, and package update remain out of
  scope.
- Y-06A Dockerless desktop distribution feasibility audit is documented in
  `docs/llmwiki/dockerless-desktop-distribution-feasibility.md`.
- Y-06A outcome: Dockerless Windows/macOS desktop distribution is feasible for
  local-only personal use, but not beginner-ready from the current repository
  state.
- Tauri is the preferred first candidate. Electron remains the fallback.
  WebView2 is Windows-only and not the primary cross-platform path.
- Key desktop blockers: backend sidecar lifecycle, close safety, desktop path
  defaults, ffmpeg / yt-dlp / Deno / bgutil packaging, signing/notarization, and
  excluding cookie/token/secret features from the beginner desktop flow.
- GitHub CLI auth note: in this Windows Codex desktop environment, sandboxed
  `gh auth status` may report an invalid `default` token while escalated
  `gh auth status` succeeds through `keyring`. Root cause is sandbox access to
  the Windows keyring, not project state. For PR create/view/checks/merge work,
  verify escalated `gh auth status` and then use narrowly scoped escalated `gh`
  commands. Do not read, paste, or store token values.

## Next Step

Proceed to Y-06B desktop sidecar lifecycle and package contract docs. Do not
implement Tauri, Electron, packaging, installers, signing, updater logic,
backend/frontend changes, Docker changes, CI changes, or package/lockfile
changes yet.
