# Roadmap

## Immediate Next

### Y-05I dry-run / prepare-only update apply contract audit

- Audit the contract for a future dry-run or prepare-only update apply step.
- Keep it docs-only or readonly contract-only unless a later task explicitly
  approves implementation.
- Do not add update execution, update buttons, Docker pull, git pull / merge /
  rebase, restart, pip install, or package updates.

## Future Automatic Update Stages

These are candidate stages, not approved implementation work:

- Stage 1: readonly version/status visibility (implemented)
- Stage 2: local changelog and update availability confirmation
- Stage 3: backup and rollback design (documented)
- Stage 4: readonly backup / rollback readiness preflight report (implemented)
- Stage 5: manual approval flow for applying updates (documented)
- Stage 6: dry-run / prepare-only update apply contract
- Stage 7: guarded local-only update execution

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
