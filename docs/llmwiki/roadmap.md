# Roadmap

## Immediate Next

### Review Y-06E report-only clean-package dry-run output

- Re-run `scripts/clean_package_dry_run.py` from a clean `fork/master`-based
  branch when needed.
- Review the planned beginner package manifest before any future package
  generation task.
- Keep guide source material, license/notice sources, checksums, and manifest
  details in review until a later task explicitly approves generation.
- Do not create `動画保存ツール_ローカル専用/`, copy files, build packages, install
  dependencies, add Tauri/Electron/WebView2, change backend/frontend/Docker/CI,
  or change package/lockfile files.

## Y-06E Dry-Run Script Outcome

- Report-only dry-run script:
  `scripts/clean_package_dry_run.py`
- Output is a human-readable sanitized text report.
- The script reports the planned `動画保存ツール_ローカル専用/` package root,
  top-level entries, Windows entries, macOS entries, developer entries,
  excluded path rules, validation checks, safety flags, and blocker details.
- Implemented safety checks:
  - forbidden path and generated-folder checks
  - forbidden filename family checks
  - forbidden content pattern family checks without printing matched values
  - required LLMwiki contract presence checks
  - PR #1001 leakage checks for `docker-compose.local.yml` and
    `docs/local-only.md`
- Exit codes are `0` for OK, `1` for blockers, and `2` for CLI usage errors.
- JSON/Markdown report modes remain future candidates, not implemented in the
  initial Y-06E script.

## Y-06D Dry-Run Contract Outcome

- Clean-package generator dry-run contract is documented in
  `docs/llmwiki/clean-package-dry-run-contract.md`.
- Dry-run is fixed as report-only planning before any package files are copied
  or generated.
- Future command candidates, JSON/Markdown report shape, exit code policy,
  warning/error/blocked classifications, planned output manifest,
  include/exclude rules, validation rules, and output examples are defined.
- Secret-like content, forbidden paths, forbidden filenames, generated package
  folders, local-only notice gaps, Windows/macOS section gaps, large file review,
  and upstream PR #1001 leakage are explicit safety gates.
- Actual package generation, clean-package generator implementation,
  Tauri/Electron/WebView2, installers, signing, build/package commands,
  dependency install/update, Docker pull, update apply, cookie/token/secret
  handling, public hosting, ads, backend/frontend/Docker/CI changes, and
  package/lockfile changes remain unapproved.

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
