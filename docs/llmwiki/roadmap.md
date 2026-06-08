# Roadmap

## Immediate Next

### Y-05L next update-safety planning

- Choose the next small local-only step after successful `/update-plan` runtime
  verification.
- Prefer either a small readonly plan/preflight UI display or a closeout
  decision.
- Do not implement update apply, prepare, rollback, backup creation, Docker pull,
  git pull / merge / rebase, restart, pip install, package update, or update
  buttons.

## Future Automatic Update Stages

These are candidate stages, not approved implementation work:

- Stage 1: readonly version/status visibility (implemented)
- Stage 2: local changelog and update availability confirmation
- Stage 3: backup and rollback design (documented)
- Stage 4: readonly backup / rollback readiness preflight report (implemented)
- Stage 5: manual approval flow for applying updates (documented)
- Stage 6: dry-run / prepare-only update apply contract (documented)
- Stage 7: readonly update-plan contract-only endpoint (implemented)
- Stage 8: readonly update-plan runtime verification (completed)
- Stage 9: optional readonly plan/preflight UI visibility or closeout decision
- Stage 10: guarded local-only update execution

Any automatic update stage must respect the safety boundaries in
`safety-boundaries.md`.

## Future UI Improvement Candidates

- Improve clarity of Japanese status and error copy
- Make local-only state visible without adding public hosting assumptions
- Improve update-status footer presentation after runtime verification
- Keep UI changes separate from backend, Docker, and CI changes unless a task explicitly
  requires a broader scope

## Not In Scope Now

- Public hosting
- Ads or monetization
- Mass-download optimization
- External wiki tooling
- Background daemons or automatic sync
