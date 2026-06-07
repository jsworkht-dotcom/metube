# Roadmap

## Immediate Next

### Backup and rollback design

- Define the backup and rollback requirements for any future manually approved
  update-apply flow.
- Keep this as design and audit work only until explicitly approved for
  implementation.

## Future Automatic Update Stages

These are candidate stages, not approved implementation work:

- Stage 1: readonly version/status visibility (implemented)
- Stage 2: local changelog and update availability confirmation
- Stage 3: backup and rollback design
- Stage 4: manual approval flow for applying updates
- Stage 5: guarded local-only update execution

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
