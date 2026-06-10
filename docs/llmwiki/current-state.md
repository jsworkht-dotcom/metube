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

### Y-06N safe-use HTML source draft

- Scope: source-only safe-use HTML guide draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-guides/05-safe-use.html.source.md`
- Outcome:
  - Added the HTML source candidate for future
    `動画保存ツール_ローカル専用/05_安全な使い方.html`.
  - Structured the draft for future HTML conversion with hero copy, safe-use
    cards, do / do-not cards, a sensitive-data warning box, an update-safety
    note, and a footer note.
  - Covered local-only personal use, allowed examples, prohibited uses,
    sensitive-data sharing boundaries, safe trouble actions, and update safety.
  - Reduced clean-package dry-run warning output by satisfying the planned
    safe-use HTML source and safe-use boundary source checks.
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

### Y-06O MeTube notice source draft

- Scope: source-only MeTube notice draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/metube-notice.source.md`
- Outcome:
  - Added the first notice source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/notices/MeTube-notice.txt`.
  - Kept the draft as Markdown source material only, not a generated notice
    file or license bundle.
  - Recorded local source candidates, package placement candidates, a short
    beginner-facing license pointer, a developer-facing notice draft, manifest
    candidate fields, and future review checklist items.
  - Reduced clean-package dry-run warning output by satisfying the planned
    MeTube notice source candidate check.
- Not implemented:
  - generated distribution folder
  - actual notice files
  - actual license bundle
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - 更新適用機能

### Y-06P yt-dlp notice source draft

- Scope: source-only yt-dlp notice draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/yt-dlp-notice.source.md`
- Outcome:
  - Added the yt-dlp notice source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/notices/yt-dlp-notice.txt`.
  - Kept the draft as Markdown source material only, not a generated notice
    file or license bundle.
  - Recorded local dependency candidates from `pyproject.toml`, `uv.lock`, and
    previous runtime `/version` verification.
  - Recorded official project and package source URL candidates, a short
    beginner-facing notice pointer, a developer-facing notice draft, manifest
    candidate fields, and future review checklist items.
  - Preserved separate future review for yt-dlp extras and transitive
    dependencies such as `curl-cffi` and Deno-related pieces.
- Not implemented:
  - generated distribution folder
  - actual notice files
  - actual license bundle
  - transitive dependency license inventory
  - standalone yt-dlp executable review
  - yt-dlp install or update behavior
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - 更新適用機能

### Y-06Q FFmpeg notice source draft

- Scope: source-only FFmpeg notice draft.
- Source draft:
  `docs/llmwiki/package-notices/ffmpeg-notice.source.md`
- Outcome:
  - Added the FFmpeg notice source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/notices/ffmpeg-notice.txt`.
  - Recorded OS-specific notice placement candidates for
    `Windows用/notices/ffmpeg-notice.txt` and
    `Mac用/notices/ffmpeg-notice.txt`.
  - Kept the draft as Markdown source material only, not a generated notice
    file or license bundle.
  - Recorded current local FFmpeg usage candidates from `Dockerfile`,
    `app/dl_formats.py`, `app/ytdl.py`, and Dockerless package planning docs.
  - Preserved required future review for selected binary provider, version,
    target OS, architecture, build configuration, LGPL/GPL status, source
    availability, and patent-sensitive/nonfree options.
- Not implemented:
  - generated distribution folder
  - actual notice files
  - actual license bundle
  - selected FFmpeg binary approval
  - FFmpeg download, install, or update behavior
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - 更新適用機能

### Y-06R Python runtime notice source draft

- Scope: source-only Python runtime notice draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/python-runtime-notice.source.md`
- Outcome:
  - Added the Python runtime notice source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/notices/python-runtime-notice.txt`.
  - Recorded OS-specific notice placement candidates for
    `Windows用/notices/python-runtime-notice.txt` and
    `Mac用/notices/python-runtime-notice.txt`.
  - Kept the draft as Markdown source material only, not a generated notice
    file, notice bundle, runtime bundle, or legal conclusion.
  - Recorded local runtime candidates from `pyproject.toml`, `Dockerfile`, and
    Dockerless package planning docs.
  - Recorded official Python source / license URL candidates and kept the
    exact bundled runtime artifact as a future review item.
  - Preserved separate future review for bundled Python dependencies,
    standard-library incorporated software, native libraries, and any bundler
    runtime pieces.
- Not implemented:
  - generated distribution folder
  - actual notice files
  - actual license bundle
  - selected Python runtime approval
  - Python download, install, build, or update behavior
  - PyInstaller spec files
  - Python dependency license inventory
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - 更新適用機能

### Y-06S frontend dependency notice source draft

- Scope: source-only frontend dependency notice draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/frontend-deps-notice.source.md`
- Outcome:
  - Added the frontend dependency notice source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/notices/frontend-deps-notice.txt`.
  - Kept the draft as Markdown source material only, not a generated notice
    file, notice bundle, frontend build artifact, package output, or legal
    conclusion.
  - Recorded read-only local candidate sources from `ui/package.json` and
    `ui/pnpm-lock.yaml`.
  - Recorded direct runtime dependency candidates, developer/build-tool
    candidates, lockfile review candidates, package placement candidates,
    beginner-facing notice copy, developer-facing notice draft, manifest fields,
    future generated notice-bundle requirements, and review checklist items.
  - Preserved exact license and bundled dependency classification for a later
    package generation / license review task.
- Not implemented:
  - generated distribution folder
  - actual notice files
  - actual license bundle
  - generated dependency license inventory
  - frontend build artifact manifest
  - package or lockfile changes
  - dependency changes
  - package manager operations
  - HTML/TXT package guide output
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - 更新適用機能

### Y-06T desktop shell notice source draft

- Scope: source-only desktop shell notice draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/desktop-shell-notice.source.md`
- Outcome:
  - Added the desktop shell notice source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/notices/desktop-shell-notice.txt`.
  - Recorded Windows and macOS notice placement candidates for future
    `Windows用/notices/desktop-shell-notice.txt` and
    `Mac用/notices/desktop-shell-notice.txt`.
  - Kept the draft as Markdown source material only, not a generated notice
    file, notice bundle, desktop shell implementation, package output, or
    legal conclusion.
  - Recorded Tauri, Electron, WebView2 direct host, and native launcher plus
    browser tab as candidates only.
  - Recorded official reference candidates for later recheck, beginner-facing
    notice copy, developer-facing notice draft, manifest fields, future
    generated notice-bundle requirements, and review checklist items.
  - Preserved actual desktop shell selection and exact license/runtime review
    for a later package generation / license review task.
- Not implemented:
  - generated distribution folder
  - actual notice files
  - actual license bundle
  - generated desktop shell dependency inventory
  - desktop shell build artifact manifest
  - Tauri implementation
  - Electron implementation
  - WebView2 implementation
  - installer implementation
  - signing or notarization
  - package or lockfile changes
  - dependency changes
  - package manager operations
  - HTML/TXT package guide output
  - package build, copy, zip, or generator behavior
  - backend/frontend/Docker/CI/package/lockfile changes
  - 更新適用機能

### Y-06U bundled Python dependency inventory source draft

- Scope: source-only bundled Python/backend dependency inventory draft and
  minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/bundled-python-dependency-inventory.source.md`
- Outcome:
  - Added the bundled Python dependency inventory source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/inventory/bundled-python-dependency-inventory.json`
    and related developer-facing notice / license review material.
  - Recorded read-only dependency source files checked: `pyproject.toml` and
    `uv.lock` present; `poetry.lock`, `requirements*.txt`, `setup.py`,
    `setup.cfg`, Pipenv, Conda environment, constraints, tox, and nox
    dependency source files not present.
  - Recorded runtime dependency candidates, developer-only candidates,
    optional / indirect candidates, manifest candidate fields, license review
    checklist items, notice bundle review checklist items, and generated
    inventory requirements.
  - Kept all license values except the existing yt-dlp source draft candidate
    as `needs_verification` until a later selected package artifact review.
  - Kept the draft as Markdown source material only, not generated inventory,
    not a notice bundle, not a package output, and not a legal conclusion.
- Not implemented:
  - generated distribution folder
  - generated dependency inventory files
  - actual notice files
  - actual license bundle
  - package generation
  - backend/frontend/Docker/CI/package/lockfile changes
  - package manager operations
  - dependency install, update, audit, build, or package commands
  - HTML/TXT package guide output
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能

### Y-06V notice source index draft

- Scope: source-only notice / license / dependency inventory source index and
  minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/notice-source-index.source.md`
- Outcome:
  - Added a hand-reviewed source index for future clean-package notice,
    license, manifest, beginner guide notice section, developer checklist, and
    dependency inventory review.
  - Read-only checked the existing MeTube, yt-dlp, FFmpeg, Python runtime,
    frontend dependency, desktop shell, and bundled Python dependency inventory
    source drafts.
  - Recorded future output mapping candidates for aggregate notices,
    license directories, manifest files, beginner guide notice sections, and
    developer review checklist items.
  - Standardized review status vocabulary: `source draft`, `legal-not-final`,
    `candidate only`, and `package-time review required`.
  - Kept unresolved questions and generated notice-bundle requirements as
    package-time review inputs only.
- Not implemented:
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - backend/frontend/Docker/CI/package/lockfile changes
  - package manager operations
  - dependency install, update, audit, build, or package commands
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能

### Y-06W clean package generator contract addendum

- Scope: docs-only / no-generation contract addendum for future clean package
  generator dry-run and preview behavior.
- Addendum:
  `docs/llmwiki/clean-package-generator-contract-addendum.md`
- Read-only sources checked:
  - `docs/llmwiki/package-notices/notice-source-index.source.md`
  - `docs/llmwiki/clean-package-dry-run-contract.md`
  - `docs/llmwiki/license-notice-plan.md`
  - `docs/llmwiki/codex-automation-policy.md`
  - `docs/llmwiki/safety-boundaries.md`
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_repo_safety.py`
- Outcome:
  - Treats the Y-06V notice source index as a future generator input candidate
    for dry-run / preview review.
  - Defines future output mapping checks for `NOTICE.txt`, `LICENSES/`,
    `manifest.json`, beginner guide notice sections, and developer review
    checklist items.
  - Defines no-generation boundary, generated artifact exclusion,
    cookie/token/secret value non-disclosure, package output before/after diff
    prediction candidate, package manifest preview candidate, cleanup /
    rollback candidate, and human review gate before actual generation.
  - Clarifies High-low / High-mid / High-high boundaries and future
    implementation phases.
- Not implemented:
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能

### Y-06X package manifest preview in clean package dry-run

- Scope: High-low / report-only dry-run preview enhancement.
- Script:
  `scripts/clean_package_dry_run.py`
- Read-only sources checked:
  - `docs/llmwiki/clean-package-generator-contract-addendum.md`
  - `docs/llmwiki/package-notices/notice-source-index.source.md`
  - `docs/llmwiki/clean-package-dry-run-contract.md`
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_repo_safety.py`
- Outcome:
  - Added a `Package manifest preview` section to the text dry-run report.
  - Reports package name/type candidates, `local_only: true`,
    `generated_artifacts: false`, notice source count/list, guide source
    count/list, excluded path summary, and future output candidates for
    `NOTICE.txt`, `LICENSES/`, `manifest.json`, and beginner guide notice
    section.
  - Reports `human_review_required_before_generation: true`,
    `legal_final: false`, non-disclosure flags for secret/token/cookie values,
    and a no-generation boundary note.
  - Preserves existing `Status: OK`, warnings, blockers, and exit-code
    behavior.
- Not implemented:
  - real `manifest.json` generation
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能

### Y-06Y package output diff prediction in clean package dry-run

- Scope: High-low / report-only dry-run preview enhancement.
- Script:
  `scripts/clean_package_dry_run.py`
- Read-only sources checked:
  - `docs/llmwiki/clean-package-generator-contract-addendum.md`
  - `docs/llmwiki/package-notices/notice-source-index.source.md`
  - `docs/llmwiki/clean-package-dry-run-contract.md`
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_repo_safety.py`
- Outcome:
  - Added a `Package output diff prediction` section to the text dry-run
    report.
  - Reports the future package root candidate, would-create directory
    candidates, would-create file candidates, would-copy source groups,
    future output candidates, excluded path summary, currently-present excluded
    path count, no-files-generated state, human review requirement before
    generation, and a cleanup / rollback candidate note.
  - Preserves the existing `Package manifest preview`, `Status: OK`, warnings,
    blockers, exit-code behavior, and no-files-generated behavior.
- Not implemented:
  - real `manifest.json` generation
  - real `NOTICE.txt` generation
  - real `LICENSES/` generation
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能

### Y-06Z clean package dry-run Markdown report mode design

- Scope: docs-only / High-low report mode design.
- Design document:
  `docs/llmwiki/clean-package-dry-run-markdown-report-mode-design.md`
- Read-only sources checked:
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_repo_safety.py`
  - `docs/llmwiki/clean-package-dry-run-contract.md`
  - `docs/llmwiki/clean-package-generator-contract-addendum.md`
  - `docs/llmwiki/codex-automation-policy.md`
  - `docs/llmwiki/handoff.md`
  - `docs/llmwiki/roadmap.md`
- Outcome:
  - Designed a future Markdown report mode for clean-package dry-run output.
  - Recommends `--format markdown` as the first future selector and keeps text
    output as the default.
  - Defines Markdown sections for Summary, Status, Risk Classification,
    Package Manifest Preview, Package Output Diff Prediction, Notice / Guide
    Source Coverage, Excluded Paths Summary, Blockers, Warnings, Human Review
    Checklist, and No-Generation Boundary.
  - Defines PR body reuse, handoff reuse, safety boundaries, future
    implementation checklist, future verification checklist, cleanup /
    rollback note, and High-low / High-mid boundary.
- Not implemented:
  - `scripts/clean_package_dry_run.py` changes
  - `scripts/check_repo_safety.py` changes
  - JSON output
  - Markdown output
  - real `manifest.json` generation
  - real `NOTICE.txt` generation
  - real `LICENSES/` generation
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - ビルド/パッケージ/インストール操作
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能

### Y-07A clean package dry-run JSON report mode design

- Scope: docs-only / High-low report mode design.
- Design document:
  `docs/llmwiki/clean-package-dry-run-json-report-mode-design.md`
- Read-only sources checked:
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_repo_safety.py`
  - `docs/llmwiki/clean-package-dry-run-contract.md`
  - `docs/llmwiki/clean-package-generator-contract-addendum.md`
  - `docs/llmwiki/clean-package-dry-run-markdown-report-mode-design.md`
  - `docs/llmwiki/codex-automation-policy.md`
  - `docs/llmwiki/handoff.md`
  - `docs/llmwiki/roadmap.md`
- Outcome:
  - Designed a future JSON report mode for clean-package dry-run output.
  - Recommends `--format json` as the first future selector and keeps text
    output as the default.
  - Defines one stdout JSON object with structured repository, package,
    planned entries, package manifest preview, package output diff prediction,
    excluded paths, checks, warnings, blocked reasons, safety flags,
    risk-classification relationship, no-generation boundary, and next-step
    fields.
  - Defines schema compatibility guidance, PR/handoff reuse guidance, safety
    boundaries, future implementation checklist, future verification checklist,
    cleanup / rollback note, and High-low / High-mid boundary.
- Not implemented:
  - `scripts/clean_package_dry_run.py` changes
  - `scripts/check_repo_safety.py` changes
  - JSON output
  - Markdown output
  - report-file output
  - real `manifest.json` generation
  - real `NOTICE.txt` generation
  - real `LICENSES/` generation
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - ビルド/パッケージ/インストール操作
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - automation wrapper / CI / PR-comment integration
  - 更新適用機能

### Y-07B clean package dry-run Markdown report mode

- Scope: report-only `--format markdown` implementation.
- Script:
  `scripts/clean_package_dry_run.py`
- Behavior:
  - Preserves the default text report.
  - Preserves `--format text` as text output.
  - Adds `--format markdown` as stdout-only Markdown output.
  - Markdown output includes Summary, Status, Risk Classification, Package
    Manifest Preview, Package Output Diff Prediction, Notice / Guide Source
    Coverage, Excluded Paths Summary, Blockers, Warnings, Human Review
    Checklist, and No-Generation Boundary sections.
  - Existing blockers, warnings, and exit codes are preserved.
  - Markdown mode reuses existing dry-run data and does not write files.
- Not implemented:
  - JSON output
  - report file writing
  - real `manifest.json` generation
  - real `NOTICE.txt` generation
  - real `LICENSES/` generation
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - ビルド/パッケージ/インストール操作
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能
- Next candidate:
  - Y-07C implement `--format json` report-only, if explicitly approved.

### Y-CHECK-01 safety gate checker design

- Scope: docs-only design for a future repository safety checker and automation
  gate.
- Design document:
  `docs/llmwiki/safety-gate-checker-design.md`
- Outcome:
  - Defined a future diff-oriented safety gate for low- and medium-risk Codex
    work.
  - Covered changed files scope, forbidden paths, secret-like pattern handling,
    generated distribution folder detection, PR #1001 leakage, dangerous
    behavior, update execution, package guide / notice completeness warnings,
    LLMwiki consistency, and PR safety summary output.
  - Kept reports sanitized: paths, line numbers, and pattern families only for
    secret-like findings.
  - Positioned package guide / notice completeness as warning-only unless actual
    package generation is attempted.
  - Clarified that the gate does not override human approval requirements for
    destructive, credential, deployment, install/update, push, merge, or release
    actions.
- Not implemented:
  - repo safety checker script
  - automation gate implementation
  - CI integration
  - PR bot/comment automation
  - generated distribution folder
  - package generation
  - backend/frontend/Docker/CI/package/lockfile changes
  - update execution
  - cookie/token/secret handling

### Y-CHECK-02 repo safety check script

- Scope: stdlib-only, report-only repository safety checker and minimal
  LLMwiki sync.
- Script:
  `scripts/check_repo_safety.py`
- Outcome:
  - Added a local report-only safety gate script for low- and medium-risk Codex
    work.
  - Default mode checks the current working tree diff against `HEAD`, including
    untracked files.
  - Optional `--base` can include committed branch diff context, for example
    `--base fork/master`.
  - Reports changed files, scope classification, warnings, blockers, and check
    statuses.
  - Checks changed-file scope, forbidden paths, generated distribution folder
    presence, upstream PR #1001 leakage, secret-like changed content,
    dangerous behavior patterns, required LLMwiki basics, and package
    guide/notice source presence.
  - Secret-like findings are sanitized and report only path, line, and pattern
    family.
  - Exit codes are `0` for OK or warning-only, `1` for blocked, and `2` for
    usage errors.
- Not implemented:
  - automation gate implementation
  - CI integration
  - PR bot/comment automation
  - generated distribution folder
  - package generation
  - backend/frontend/Docker/CI/package/lockfile changes
  - update execution
  - cookie/token/secret value output

### Y-AUTO-01 Codex automation expansion policy

- Scope: docs-only Codex automation policy for low-, medium-, and qualifying
  high-low-risk work.
- Policy document:
  `docs/llmwiki/codex-automation-policy.md`
- Outcome:
  - Defined five risk levels: Low, Medium, High-low, High-mid, and High-high.
  - Kept Low work eligible for auto PR and auto merge when the current task
    scope and required gates pass.
  - Kept Medium work eligible for auto PR and auto merge when safety gates pass.
  - Added conditional High-low auto PR / auto merge for docs-only,
    report-only, or dry-run-only work that passes the full mandatory gate set.
  - Required High-low work to pass `check_repo_safety.py`,
    `check_repo_safety.py --base fork/master`, `clean_package_dry_run.py`,
    `git diff --check`, GitHub clean merge state, and no failed checks.
  - Kept High-mid work PR-capable but auto-merge prohibited.
  - Kept High-high work automatic-execution prohibited until explicit human
    confirmation.
- Not implemented:
  - generated distribution folder
  - generated guide, notice, manifest, ZIP, package, or installer output
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - public hosting or ads
  - 更新適用機能

### Y-AUTO-02 repo safety risk classification

- Scope: report-only checker improvement and minimal LLMwiki sync.
- Script:
  `scripts/check_repo_safety.py`
- Outcome:
  - Added a `Risk classification` section to the repo safety report.
  - The report now includes `tier`, `automation`, and `reason`.
  - Supported tiers are `Low`, `Medium`, `High-low`, `High-mid`,
    `High-high`, and `Unknown`.
  - Supported automation outputs are `auto-merge-ok`,
    `pr-only-human-merge`, `stop-before-pr`, and `unknown`.
  - Existing `Status: OK` / `Status: BLOCKED` behavior is unchanged.
  - Existing blockers for forbidden paths, generated distribution folders,
    PR #1001 leakage, secret-like content, dangerous behavior, and required
    LLMwiki basics are unchanged.
  - For this report-only checker task, the working-tree report classified the
    change as `Medium` with `automation: auto-merge-ok`.
- Not implemented:
  - automation gate implementation
  - CI integration
  - PR bot/comment automation
  - generated distribution folder
  - generated guide, notice, manifest, ZIP, package, or installer output
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - public hosting or ads
  - 更新適用機能

### Y-AUTO-03 High-mid PR-ready automation policy

- Scope: docs-only policy expansion for High-mid Codex work.
- Policy document:
  `docs/llmwiki/codex-automation-policy.md`
- Outcome:
  - Clarified that Low, Medium, and qualifying High-low work may still use auto
    PR / auto merge when gates pass.
  - Clarified that High-mid work may proceed through Codex implementation,
    verification, PR creation, and Ready-for-review handoff when the task
    explicitly approves the High-mid scope.
  - Kept High-mid auto merge prohibited.
  - Required High-mid PRs to state `human-review-required`.
  - Required High-mid PR bodies to explain why the work is High-mid, what was
    not performed, rollback/cleanup candidates, and remaining risk.
  - Added a High-mid PR body template.
  - Reconfirmed that High-high work must stop before implementation without
    explicit human confirmation.
- Not implemented:
  - generated distribution folder
  - generated guide, notice, manifest, ZIP, package, or installer output
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - public hosting or ads
  - 更新適用機能

### Y-AUTO-04 High-mid PR-only checker guidance

- Scope: report-only checker improvement and minimal LLMwiki sync.
- Script:
  `scripts/check_repo_safety.py`
- Outcome:
  - Added path and filename based High-mid-like scope detection.
  - High-mid-like scopes now report `tier: High-mid`.
  - High-mid-like scopes without blockers now report
    `automation: pr-only-human-merge`.
  - High-mid-like reasons explicitly state that auto merge is disabled, human
    review is required before merge, and the PR body must include
    `human-review-required`.
  - Known report-only checker / dry-run script changes remain `Medium` with
    `automation: auto-merge-ok` when no blockers are present.
  - Existing `Status: OK` / `Status: BLOCKED` behavior is unchanged.
  - Existing blockers for forbidden paths, generated distribution folders,
    PR #1001 leakage, secret-like content, dangerous behavior, and required
    LLMwiki basics are unchanged.
- Not implemented:
  - automation gate implementation
  - CI integration
  - PR bot/comment automation
  - generated distribution folder
  - generated guide, notice, manifest, ZIP, package, or installer output
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - public hosting or ads
  - 更新適用機能

## Current Next Step

Use the `Risk classification` section from `scripts/check_repo_safety.py` as the
first local summary before auto PR or auto merge.

Use `scripts/check_repo_safety.py` and `scripts/clean_package_dry_run.py` as
local report-only gates before the next low-, medium-, or qualifying
high-low-risk fork PR.

The previous package-material next step is complete through Y-07B.

The next package-material candidate should be selected explicitly. A good next
candidate is Y-07C `--format json` report-only implementation if explicitly
approved.

Next scope:

- Keep any further Y-CHECK automation, CI, or PR-comment integration separate
  until explicitly approved.
- Keep notice material source-only, sanitized, and review-oriented.
- Keep guide and notice files as source material only; do not generate package
  outputs.
- Keep clean-package preview work report-only / dry-run-only until actual
  generation is explicitly approved.
- Keep Tauri/Electron implementation, packaging, installer, signing, updater,
  backend changes, frontend changes, Docker changes, CI changes, package
  changes, and lockfile changes out of scope unless explicitly approved later.
