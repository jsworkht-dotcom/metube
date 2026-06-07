# Roadmap

## Immediate Next

### Y-05D runtime verification

- Verify `/update-status` behavior at runtime.
- Verify footer display against the readonly update-status baseline.
- Keep this as verification work only unless a separate change request is made.

## Future Automatic Update Stages

These are candidate stages, not approved implementation work:

- Stage 1: readonly version/status visibility
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
