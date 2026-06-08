# Current State

## Project

- Project: `youtubeダウンロード / MeTube local-only fork`
- Repository: `C:\Users\tomikyo\_projects\youtubeダウンロード`
- Upstream remote: `origin -> https://github.com/alexta69/metube.git`
- Fork remote: `fork -> https://github.com/jsworkht-dotcom/metube.git`
- Local `master` tracks `fork/master`
- Current source of truth: fork `master`

## Repository State

- This project is local-only and for personal use.
- Do not open PRs against upstream `alexta69/metube` unless explicitly requested for a
  separate upstream contribution.
- Do not mix upstream PR #1001 files into fork-only work.

## Completed Work

### Y-03 local-only Docker profile

- Upstream PR #1001 is Ready for review.
- Branch `local-only-docker-profile` remains while PR #1001 is open.
- Keep `docker-compose.local.yml` and `docs/local-only.md` out of unrelated fork work.

### Y-04 Japanese static UI copy

- Fork PR #1 was merged.
- Merge commit: `0cc8dd602ccaa0944630c56322e6b753133f6961`
- Scope: static Japanese UI copy for the fork.

### Y-05 readonly update-status

- Fork PR #2 was merged.
- Merge commit: `37256d5b8a885aac0f7e323f413409769055cc83`
- Scope: readonly update-status baseline.

### Y-05D runtime verification

- Runtime verification confirmed `/update-status` remains readonly.
- `METUBE_VERSION=dev` was found to display `更新確認失敗` even when metadata
  fetches succeeded, because `dev` could not be compared with release tags.
- `METUBE_VERSION=2026.06.06` displayed `最新`.
- `METUBE_VERSION=0.0.0` displayed `更新あり`.
- No update execution, Docker pull, git pull, restart, pip install, or
  cookie/token/secret exposure was observed.

### Y-05E dev version status fix

- Fork PR #4 was merged.
- Merge commit: `af6987532a741cd680d8b747562b2f2971b9c229`
- Scope: treat `METUBE_VERSION=dev` as `development` and show `開発版` in
  the footer while preserving real `check_failed` behavior.

### Y-05G readonly update preflight report

- Fork PR #7 was merged.
- PR URL: `https://github.com/jsworkht-dotcom/metube/pull/7`
- Merge commit: `bfbecdb`
- Scope: readonly update preflight report for backup and rollback readiness.
- Changed files:
  - `app/main.py`
  - `app/update_preflight.py`
  - `app/tests/test_update_preflight.py`
- Implemented:
  - readonly `/update-preflight` report
  - backup / rollback readiness JSON report
  - update apply readiness as information only with `can_apply_update: false`
- Not implemented:
  - update execution
  - backup creation
  - rollback creation
  - Docker pull
  - git pull / merge / rebase
  - restart
  - pip install / package update

### Y-05H manual-approval update apply design audit

- Scope: docs-only design audit for future manual-approval update apply.
- Design document: `docs/llmwiki/manual-update-apply-design.md`
- Defines:
  - update target classification for source, Docker, yt-dlp, and state/data
  - manual approval flow
  - future UI/API boundaries
  - stop conditions
  - rollback hand-off requirements
- Not implemented:
  - update execution
  - update apply endpoint
  - update button
  - backup creation
  - rollback creation
  - Docker pull
  - git pull / merge / rebase
  - restart
  - pip install / package update

### Y-05I dry-run / prepare-only update apply contract audit

- Scope: docs-only dry-run / prepare-only contract audit.
- Contract document: `docs/llmwiki/dry-run-update-contract.md`
- Defines:
  - dry-run as readonly planning only
  - prepare-only as validation only, with no backup or rollback creation in the
    first prepare stage
  - future `/update-plan`, `/update-prepare`, `/update-apply`, and
    `/update-rollback` endpoint boundaries
  - conservative response fields, stop conditions, and UI constraints
- Not implemented:
  - update execution
  - update prepare endpoint
  - update apply endpoint
  - update button
  - backup creation
  - rollback creation
  - Docker pull
  - git pull / merge / rebase
  - restart
  - pip install / package update

### Y-05J readonly update-plan contract-only endpoint

- Scope: readonly `/update-plan` contract-only endpoint.
- Implemented:
  - readonly update-plan helper
  - `GET /update-plan` endpoint
  - blocked-by-default response contract
  - update-plan tests
- Contract behavior:
  - `can_prepare` remains `false`
  - `can_apply` remains `false`
  - planned steps and blocked reasons are reported as information only
- Not implemented:
  - update execution
  - update prepare endpoint
  - update apply endpoint
  - update rollback endpoint
  - update button
  - backup creation
  - rollback creation
  - Docker pull
  - git pull / merge / rebase
  - restart
  - pip install / package update

### Y-05K-R update-plan runtime verification

- Runtime verification succeeded after Docker Desktop / Docker daemon recovery.
- Docker: Docker Desktop `4.76.0`, Engine `29.5.2`.
- Image: existing local `ghcr.io/alexta69/metube:latest` used with
  `--pull=never`.
- Bind: `127.0.0.1:18082` only.
- Mounts: app and built UI were mounted read-only.
- `/update-plan` response:
  - `overall: blocked`
  - `can_prepare: false`
  - `can_apply: false`
  - `blocked_reasons` present
  - `planned_steps` present
  - rollback/doc references present
- Related endpoints:
  - `/update-status`: `latest`
  - `/update-preflight`: `not_ready`, `can_apply_update: false`
  - `/version`: `version: 2026.06.06`, `yt-dlp: 2026.03.17`
- No secret/token/cookie values appeared in responses or logs.
- No update execution, Docker pull, git pull / merge / rebase, restart, pip
  install/update, backup creation, or rollback creation occurred.
- Temporary container was stopped and removed.
- Read-only mount `chown ... Read-only file system` warnings were observed
  during verification and are expected for that test launch style.

### Y-05 readonly update readiness phase closeout

- Y-05 readonly update readiness is complete for now.
- Completed scope:
  - readonly `/update-status`
  - readonly `/update-preflight`
  - readonly `/update-plan`
  - backup / rollback planning
  - manual approval design
  - dry-run / prepare-only contract
  - runtime verification for `/update-plan`
- Update execution remains intentionally not implemented.
- Still not implemented:
  - update apply
  - update prepare
  - update rollback
  - update button
  - backup creation
  - rollback creation
  - Docker pull
  - git pull / merge / rebase
  - restart
  - pip install / package update

### Y-06A Dockerless desktop distribution feasibility audit

- Scope: docs-only feasibility audit for Dockerless desktop distribution.
- Audit document:
  `docs/llmwiki/dockerless-desktop-distribution-feasibility.md`
- Outcome:
  - Dockerless Windows/macOS desktop distribution is feasible for local-only
    personal use, but not beginner-ready from the current repository state.
  - Tauri is the preferred first candidate.
  - Electron remains the fallback if Tauri sidecar, WebView, or signing friction
    becomes unacceptable.
  - WebView2 is a Windows-only fallback and is not the primary path because
    macOS parity is required.
- Recommended architecture:
  - Tauri shell
  - existing Angular UI reused as built static assets
  - Python backend packaged as a sidecar, likely PyInstaller one-folder output
  - bundled platform-specific ffmpeg
  - desktop launcher forcing `HOST=127.0.0.1` and per-user state/download/temp
    paths
- Main blockers before beginner distribution:
  - backend lifecycle and close-safety contract
  - desktop-specific path contract
  - ffmpeg / yt-dlp / Deno / bgutil packaging and license review
  - Windows SmartScreen and macOS Gatekeeper / notarization story
  - cookie/token/secret features excluded from the beginner desktop flow
- Not implemented:
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06B desktop sidecar lifecycle and package contract docs

- Scope: docs-only lifecycle and package contract for a future Level 3
  Dockerless desktop-like distribution.
- Contract document:
  `docs/llmwiki/desktop-sidecar-lifecycle-contract.md`
- Outcome:
  - Defined desktop wrapper ownership for backend sidecar start, readiness,
    monitoring, stop, close confirmation, and abnormal-exit recovery.
  - Defined required desktop env overrides, including `HOST=127.0.0.1` and
    per-user download/state/temp paths.
  - Defined package contents, package exclusions, Windows/macOS package
    boundaries, and beginner `.html` / `.txt` guide requirements.
  - Kept cookie/token/secret handling, update apply, Docker pull, package
    install/update, public hosting, ads, and implementation work out of scope.
- Not implemented:
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06C desktop package manifest and beginner guide skeleton docs

- Scope: docs-only package manifest and beginner guide skeleton for a future
  Level 3 beginner desktop distribution.
- Manifest document:
  `docs/llmwiki/desktop-package-manifest.md`
- Guide skeleton document:
  `docs/llmwiki/beginner-guide-skeleton.md`
- Outcome:
  - Defined the future user-facing package root:
    `動画保存ツール_ローカル専用/`.
  - Fixed primary beginner guide as `00_最初に開いてください.html`, fallback as
    `00_最初に開いてください.txt`, and Markdown as developer/LLMwiki material.
  - Defined Windows and macOS package skeletons, warning/signing boundaries,
    include/exclude rules, generated manifest candidates, user data path
    templates, config sample boundaries, notices, and checksum candidates.
  - Kept build/package generation, Tauri/Electron/WebView2 implementation,
    installers, signing, update apply, Docker pull, dependency install/update,
    cookie/token/secret handling, public hosting, ads, and implementation work
    out of scope.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package generator
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06D clean-package generator dry-run contract docs

- Scope: docs-only dry-run contract for a future clean beginner package
  generator.
- Contract document:
  `docs/llmwiki/clean-package-dry-run-contract.md`
- Outcome:
  - Defined dry-run as report-only planning before any clean package files are
    copied or generated.
  - Defined future command candidates, JSON/Markdown report shape, exit code
    policy, planned output manifest, include/exclude rules, validation gates,
    and blocked conditions.
  - Fixed safety checks for forbidden paths, forbidden filenames,
    secret-like content patterns, large files, missing guides/notices,
    local-only notice requirements, Windows/macOS package section completeness,
    generated folder presence, and PR #1001 leakage.
  - Kept actual package generation, clean-package generator implementation,
    Tauri/Electron/WebView2 implementation, build/package commands,
    dependency install/update, Docker pull, update apply, cookie/token/secret
    handling, public hosting, ads, and upstream PR #1001 work out of scope.
- Not implemented:
  - clean-package generator script
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build or copy behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06E report-only clean-package dry-run script

- Scope: stdlib-only dry-run script and minimal LLMwiki sync.
- Script:
  `scripts/clean_package_dry_run.py`
- Outcome:
  - Prints a human-readable clean-package dry-run report.
  - Reports the planned `動画保存ツール_ローカル専用/` package root and manifest.
  - Treats forbidden repository paths as excluded, not copied.
  - Blocks generated package-folder presence, forbidden filename families,
    forbidden content pattern families, and PR #1001 file leakage.
  - Reports only sanitized path, line, and pattern-family details for
    secret-like content checks. Matched values are not printed.
  - Uses exit code `0` for OK, `1` for blockers, and `2` for CLI usage errors.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06F beginner guide source and license notice review

- Scope: docs-only review for future beginner guide source candidates and
  license/notice planning.
- Guide source plan:
  `docs/llmwiki/beginner-guide-source-plan.md`
- License/notice plan:
  `docs/llmwiki/license-notice-plan.md`
- Outcome:
  - Defined future source candidates for `00_最初に開いてください.html`,
    `00_最初に開いてください.txt`, `03_使い方.*`, `04_困ったとき.*`, and
    `05_安全な使い方.html`.
  - Defined beginner wording rules: Japanese-first, local-only, concrete
    actions, and no normal-flow Docker / terminal / Git / Python / Node.js /
    package-manager jargon.
  - Defined package placement candidates for guides, troubleshooting pages,
    developer docs, license directories, notice directories, and a future
    license-notice manifest.
  - Identified notice categories for MeTube, yt-dlp, ffmpeg, Python runtime,
    Python dependencies, frontend dependencies, and future Tauri/Electron
    runtime pieces if implemented later.
  - Selected the next PR candidate: add non-blocking missing guide-source and
    missing notice-source warnings to `scripts/clean_package_dry_run.py`.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - license text copying
  - notice bundle generation
  - dry-run script changes
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06G clean-package dry-run guide/notice warning hardening

- Scope: dry-run script warning hardening and minimal LLMwiki sync.
- Script:
  `scripts/clean_package_dry_run.py`
- Outcome:
  - Added nonblocking warnings for planned-but-missing beginner guide source
    candidates.
  - Added nonblocking warnings for planned-but-missing license/notice source
    candidates.
  - Added nonblocking warnings for local-only safety notice and Windows/macOS
    section source coverage.
  - Kept dry-run `Status: OK` and exit code `0` when only warnings are present.
  - Preserved existing blocking behavior for generated package folders,
    forbidden filename families, secret-like content findings, and PR #1001
    leakage.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - license text copying
  - notice bundle generation
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06H first beginner guide source draft

- Scope: source-only first-open beginner guide draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-guides/00-first-open.html.source.md`
- Outcome:
  - Added the first source candidate for future
    `動画保存ツール_ローカル専用/00_最初に開いてください.html`.
  - Kept the draft as Markdown source material only, not a generated package
    guide.
  - Structured the draft for a future HTML page with hero copy, first-step
    cards, a warning box, in-app help cards, troubleshooting cards, and a
    footer note.
  - Covered local-only use, allowed-content boundaries, start, URL paste,
    save, open save folder, and stop/quit behavior.
  - Covered the close-safety note that users should use `停止して終了` because
    closing with X may not stop the background process cleanly.
  - Reduced clean-package dry-run warning output by satisfying the planned
    first-open HTML source, local-only safety source, and Windows/macOS section
    source candidate checks.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06I first-open TXT fallback source draft

- Scope: source-only first-open TXT fallback draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-guides/00-first-open.txt.source.md`
- Outcome:
  - Added the TXT fallback source candidate for future
    `動画保存ツール_ローカル専用/00_最初に開いてください.txt`.
  - Kept the draft shorter than the HTML source and readable in a normal text
    editor.
  - Covered what the tool is, the short start/save/open-folder/stop flow,
    safe-use boundaries, troubleshooting entry points, and the HTML guide
    hand-off.
  - Reduced clean-package dry-run warning output by satisfying the planned
    first-open TXT source and local-only TXT safety source checks.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06J how-to-use HTML guide source draft

- Scope: source-only everyday-use HTML guide draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-guides/03-how-to-use.html.source.md`
- Outcome:
  - Added the HTML source candidate for future
    `動画保存ツール_ローカル専用/03_使い方.html`.
  - Structured the draft for a future HTML page with hero copy, quick steps,
    action cards, format cards, status explanation cards, a warning box,
    troubleshooting link cards, and a footer note.
  - Covered start, URL paste, save-format selection, save, open save folder,
    status reading, retry guidance, and stop/quit behavior.
  - Kept beginner-facing copy short, local-only, and reusable for future
    in-app help wording.
  - Reduced clean-package dry-run warning output by satisfying the planned
    how-to-use HTML source candidate check.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06K how-to-use TXT fallback source draft

- Scope: source-only everyday-use TXT fallback draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-guides/03-how-to-use.txt.source.md`
- Outcome:
  - Added the TXT fallback source candidate for future
    `動画保存ツール_ローカル専用/03_使い方.txt`.
  - Kept the draft shorter than the HTML source and readable in a normal text
    editor.
  - Covered basic save steps, save-format choices, saving/completion behavior,
    stop/quit behavior, safe-use boundaries, and the HTML guide hand-off.
  - Reduced clean-package dry-run warning output by satisfying the planned
    how-to-use TXT source candidate check.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06L troubleshooting HTML source draft

- Scope: source-only troubleshooting HTML guide draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-guides/04-troubleshooting.html.source.md`
- Outcome:
  - Added the HTML source candidate for future
    `動画保存ツール_ローカル専用/04_困ったとき.html`.
  - Structured the draft for future HTML conversion with hero copy, a quick
    checklist, trouble cards, a warning box, a safe-use reminder, and a footer
    note.
  - Covered first checks, common beginner trouble cases, gentle error-message
    examples, safe stop/quit behavior, save-folder guidance, update-display
    uncertainty, and safe-use boundaries.
  - Reduced clean-package dry-run warning output by satisfying the planned
    troubleshooting HTML source candidate check.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06M troubleshooting TXT fallback source draft

- Scope: source-only troubleshooting TXT fallback draft and minimal LLMwiki
  sync.
- Source draft:
  `docs/llmwiki/package-guides/04-troubleshooting.txt.source.md`
- Outcome:
  - Added the TXT fallback source candidate for future
    `動画保存ツール_ローカル専用/04_困ったとき.txt`.
  - Kept the draft shorter than the HTML source and readable in a normal text
    editor.
  - Covered first actions, common trouble cases, stop/quit behavior, safe-use
    boundaries, and the HTML guide hand-off.
  - Reduced clean-package dry-run warning output by satisfying the planned
    troubleshooting TXT source candidate check.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

## Current Next Step

Draft the safe-use HTML source:
`docs/llmwiki/package-guides/05-safe-use.html.source.md`.

Next scope:

- Keep the safe-use guide short, Japanese-first, beginner-safe, and
  source-material only.
- Keep guide files as source material only; do not generate package outputs.
- Keep Tauri/Electron implementation, packaging, installer, signing, updater,
  backend changes, frontend changes, Docker changes, CI changes, package
  changes, and lockfile changes out of scope unless explicitly approved later.
