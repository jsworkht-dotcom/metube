# Roadmap

## Immediate Next

### Use Y-CHECK-02 repo safety script

- Run `scripts/check_repo_safety.py` before the next low- or medium-risk fork
  PR.
- Keep the script report-only.
- Keep any automation wrapper, CI integration, PR comment automation, or JSON
  report mode as a later explicitly approved task.
- Keep package generation, update execution, dependency install/update, Docker
  pull, backend/frontend/Docker/CI changes, package/lockfile changes,
  generated distribution folders, and cookie/token/secret handling out of
  scope unless explicitly approved.

### Draft ffmpeg notice source

- Draft `docs/llmwiki/package-notices/ffmpeg-notice.source.md` as the next
  notice source candidate for future clean-package notice review.
- Keep the next PR source-material only unless explicitly approved otherwise.
- Do not create guide outputs, copy license text, generate notice bundles, or
  create package files.
- Do not create `動画保存ツール_ローカル専用/`, copy files, build packages, install
  dependencies, add Tauri/Electron/WebView2, change backend/frontend/Docker/CI,
  or change package/lockfile files.

## Y-06P yt-dlp Notice Source Outcome

- Notice source draft:
  `docs/llmwiki/package-notices/yt-dlp-notice.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/開発者向け/notices/yt-dlp-notice.txt`.
- The draft is source-only and review-oriented, with:
  - future notice / license placement candidates
  - yt-dlp component summary
  - local dependency candidates from `pyproject.toml`, `uv.lock`, and previous
    runtime `/version` verification
  - short beginner-facing notice pointer
  - developer-facing notice draft
  - manifest candidate fields
  - required future review checklist
- Covered official project and package source URL candidates, the Unlicense
  candidate, selected extras, and separate future review for transitive
  dependency notices.
- No actual notice output, license bundle, generated package folder,
  yt-dlp install/update behavior, package build/copy behavior,
  Tauri/Electron implementation, backend/frontend/Docker/CI change, or
  package/lockfile change was added.

## Y-CHECK-01 Safety Gate Checker Design Outcome

- Design document:
  `docs/llmwiki/safety-gate-checker-design.md`
- Defined a future repository safety checker and automation gate for low- and
  medium-risk Codex work.
- Designed checks for:
  - changed files scope
  - forbidden paths
  - secret-like pattern families without printing matched values
  - generated `動画保存ツール_ローカル専用/` folder presence
  - upstream PR #1001 file leakage
  - dangerous behavior
  - update execution
  - package guide / notice completeness warnings
  - LLMwiki consistency
  - PR safety gate summary
- The design is docs-only and does not add scripts, CI, package generation,
  update execution, generated distribution folders, backend/frontend/Docker/CI
  changes, package/lockfile changes, or credential handling.

## Y-CHECK-02 Repo Safety Check Script Outcome

- Script:
  `scripts/check_repo_safety.py`
- Added the first stdlib-only report-only implementation of the repository
  safety gate.
- Default mode checks the current working tree diff against `HEAD`, including
  untracked files.
- Optional `--base` can include committed branch diff context such as
  `fork/master`.
- Implemented checks for changed-file scope, forbidden paths, generated
  distribution folder presence, upstream PR #1001 leakage, secret-like changed
  content, dangerous behavior patterns, required LLMwiki basics, and package
  guide/notice source warnings.
- Reports are sanitized: secret-like findings show path, line, and pattern
  family only.
- Exit codes are `0` for OK or warning-only, `1` for blocked, and `2` for
  usage errors.
- No automation gate, CI integration, PR bot/comment automation, package
  generation, generated distribution folder, backend/frontend/Docker/CI change,
  package/lockfile change, update execution, or cookie/token/secret value
  output was added.

## Y-06O MeTube Notice Source Outcome

- Notice source draft:
  `docs/llmwiki/package-notices/metube-notice.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/開発者向け/notices/MeTube-notice.txt`.
- The draft is source-only and review-oriented, with:
  - future notice / license placement candidates
  - MeTube component summary
  - short beginner-facing license pointer
  - developer-facing notice draft
  - future manifest candidate fields
  - required future review checklist
- Covered local source candidates, AGPLv3 license candidate from root
  `LICENSE`, fork/upstream source URL candidates, source commit placeholder,
  and no-private-data notice hygiene.
- No actual notice output, license bundle, generated package folder,
  package build/copy behavior, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06N Safe-Use HTML Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/05-safe-use.html.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/05_安全な使い方.html`.
- The draft is Japanese-first and structured for future HTML conversion with:
  - hero copy
  - safe-use cards
  - do / do-not cards
  - a sensitive-data warning box
  - an update-safety note
  - a footer note
- Covered local-only personal use, allowed examples, prohibited uses,
  sensitive-data sharing boundaries, safe trouble actions, and update safety.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06M Troubleshooting TXT Fallback Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/04-troubleshooting.txt.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/04_困ったとき.txt`.
- The draft is shorter than the HTML source and designed to remain readable in
  a normal text editor.
- Covered first actions, common trouble cases, stop/quit behavior, safe use,
  and the hand-off to `04_困ったとき.html`.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06L Troubleshooting HTML Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/04-troubleshooting.html.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/04_困ったとき.html`.
- The draft is Japanese-first and structured for future HTML conversion with:
  - hero copy
  - quick checklist
  - trouble cards
  - a warning box
  - a safe-use reminder
  - a footer note
- Covered first checks, common trouble cases, gentle error messages, save-folder
  guidance, stop/quit behavior, update-display uncertainty, and safe use.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06K How-To-Use TXT Fallback Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/03-how-to-use.txt.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/03_使い方.txt`.
- The draft is shorter than the HTML source and designed to remain readable in
  a normal text editor.
- Covered basic save steps, save-format choices, saving/completion behavior,
  stop/quit behavior, safe use, and the hand-off to `03_使い方.html`.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06J How-To-Use HTML Guide Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/03-how-to-use.html.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/03_使い方.html`.
- The draft is Japanese-first and structured for future HTML conversion with:
  - hero copy
  - quick steps
  - action cards
  - format cards
  - status explanation cards
  - a warning box
  - troubleshooting link cards
  - a footer note
- Covered start, URL paste, save-format selection, save, open save folder,
  status reading, retry guidance, stop/quit, and safe use.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06I First-Open TXT Fallback Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/00-first-open.txt.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/00_最初に開いてください.txt`.
- The draft is shorter than the HTML source and designed to remain readable in
  a normal text editor.
- Covered what the tool is, the short first-use steps, safe use,
  troubleshooting entry points, and the hand-off to
  `00_最初に開いてください.html`.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06H First-Open Guide Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/00-first-open.html.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/00_最初に開いてください.html`.
- The draft is Japanese-first and structured for future HTML conversion with:
  - hero copy
  - first-step cards
  - a local-only warning box
  - in-app help cards
  - troubleshooting cards
  - a footer note
- Covered start, URL paste, save, open save folder, stop/quit, safe use, and
  first troubleshooting actions.
- Covered the `停止して終了` close-safety note and kept X-close behavior as a
  caution, not the preferred exit path.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06G Dry-Run Warning Hardening Outcome

- Dry-run script:
  `scripts/clean_package_dry_run.py`
- Added nonblocking warning output for:
  - missing beginner guide source candidates
  - missing license/notice source candidates
  - missing local-only safety notice source candidates
  - missing Windows/macOS section source coverage
- Warning-only dry-runs keep `Status: OK` and exit code `0`.
- Existing blockers remain blockers:
  - generated package folder
  - forbidden filename families
  - secret-like content findings
  - upstream PR #1001 leakage
- No package generation, guide generation, notice copying, build/package output,
  backend/frontend/Docker/CI changes, or package/lockfile changes were added.

## Y-06F Guide Source And Notice Review Outcome

- Guide source plan:
  `docs/llmwiki/beginner-guide-source-plan.md`
- License/notice plan:
  `docs/llmwiki/license-notice-plan.md`
- Y-06F is docs-only and does not generate package files.
- Planned future guide outputs:
  - `00_最初に開いてください.html`
  - `00_最初に開いてください.txt`
  - `03_使い方.html`
  - `03_使い方.txt`
  - `04_困ったとき.html`
  - `04_困ったとき.txt`
  - `05_安全な使い方.html`
- Planned notice categories cover MeTube, yt-dlp, ffmpeg, Python runtime,
  bundled Python dependencies, frontend runtime dependencies, and future
  Tauri/Electron runtime pieces only if implemented later.
- License text copying, notice bundle generation, guide generation, package
  generation, Tauri/Electron implementation, backend/frontend/Docker/CI
  changes, and package/lockfile changes remain unapproved.
- Next PR candidate: add advisory dry-run warnings for missing guide and notice
  source candidates.

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
