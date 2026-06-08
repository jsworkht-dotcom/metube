# Roadmap

## Immediate Next

### Y-06D clean-package generator dry-run contract docs

- Write the docs-only dry-run contract required before any clean-package
  generator implementation.
- Scope: Windows + macOS, local-only personal use, Tauri-first unless a later
  checkpoint explicitly changes that.
- Define dry-run report shape, safe path validation, include/exclude checks,
  secret scanning boundaries, generated-folder stop conditions, and PR #1001
  leakage checks.
- Do not implement Tauri, Electron, packaging, installers, signing, updater
  logic, backend changes, frontend changes, Docker changes, CI changes, or
  package/lockfile changes in Y-06D.

## Y-06C Manifest And Guide Outcome

- Desktop package manifest is documented in
  `docs/llmwiki/desktop-package-manifest.md`.
- Beginner HTML/TXT guide skeleton is documented in
  `docs/llmwiki/beginner-guide-skeleton.md`.
- Future package root is fixed as `動画保存ツール_ローカル専用/`.
- Primary guide is `00_最初に開いてください.html`; fallback guide is
  `00_最初に開いてください.txt`; Markdown is developer/LLMwiki material.
- Windows and macOS package skeletons, include/exclude rules, generated
  manifest candidates, user data paths, notices, checksums, and safe beginner
  copy boundaries are defined.
- Generated distribution folders, package scripts, Tauri/Electron/WebView2
  implementation, package builds, installers, signing,
  backend/frontend/Docker/CI/package/lockfile changes, and update apply remain
  unapproved.

## Y-06B Contract Outcome

- Desktop sidecar lifecycle and package boundaries are documented in
  `docs/llmwiki/desktop-sidecar-lifecycle-contract.md`.
- The desktop wrapper owns backend sidecar start, readiness checks, monitoring,
  stop, close confirmation, and abnormal-exit recovery.
- Future desktop launch must force `HOST=127.0.0.1` and per-user
  download/state/temp paths.
- Package contents, exclusions, Windows/macOS boundaries, and beginner
  `.html` / `.txt` guide requirements are defined at contract level.
- Tauri/Electron/WebView2 implementation, package builds, installers, signing,
  backend/frontend/Docker/CI/package/lockfile changes, and update apply remain
  unapproved.

## Y-06A Feasibility Outcome

- Dockerless desktop distribution is feasible, but not beginner-ready from the
  current repository state.
- Tauri is the preferred first candidate.
- Electron remains the fallback if Tauri WebView, sidecar, or signing friction
  becomes unacceptable.
- WebView2 is a Windows-only fallback and not the primary cross-platform path.
- The main blockers are backend lifecycle, close safety, desktop path defaults,
  ffmpeg / yt-dlp / Deno / bgutil packaging, signing/notarization, and excluding
  cookie/token/secret features from the beginner desktop flow.

## Beginner UX Source Of Truth

Y-06 should optimize for a non-developer local desktop user:

- Start MeTube without understanding Docker.
- Keep setup language short, Japanese, and concrete.
- Prefer one clear local launch path per OS.
- Make storage location, app status, and stop/quit behavior obvious.
- Avoid public hosting, account setup, ads, background sync, or external-user
  assumptions.
- Preserve the existing readonly update readiness work as diagnostic support,
  not as update execution.

## Future Automatic Update Stages

Y-05 readiness work is complete for now. These remain historical or candidate
stages, not approved update execution work:

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
- Update apply implementation
- Desktop installer or packaging implementation
- Tauri/Electron implementation
