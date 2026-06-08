# Desktop Sidecar Lifecycle Contract

## Purpose

Y-06B defines the documentation-only contract for a future Dockerless desktop
distribution of this local-only MeTube fork.

The goal is to prevent the next implementation step from getting stuck on the
same root issues: backend lifecycle ownership, local-only binding, sidecar
readiness, close behavior, bundled runtime expectations, path defaults, package
contents, and beginner-facing distribution boundaries.

This document is a contract for future work. It does not approve or implement a
desktop shell, package build, installer, updater, backend change, frontend
change, Docker change, CI change, dependency change, or lockfile change.

## Baseline

The current repository has these relevant properties:

- Backend: Python aiohttp / Socket.IO server launched from `app/main.py`.
- Default backend bind is controlled by `HOST` and `PORT`, currently defaulting
  to `0.0.0.0` and `8081`.
- Existing local runtime paths are controlled by `DOWNLOAD_DIR`,
  `AUDIO_DOWNLOAD_DIR`, `TEMP_DIR`, and `STATE_DIR`.
- Persistent queue/state data is stored as JSON through `AtomicJsonStore`.
- Download work is managed by backend queue/process logic in `app/ytdl.py`.
- Frontend: Angular static app connecting to the backend through Socket.IO.
- Existing readonly update diagnostics are `/update-status`,
  `/update-preflight`, and `/update-plan`.
- Existing cookie-related UI/API exists in the project, but is excluded from the
  beginner desktop flow by this contract.

## Target Architecture

- Desktop shell: Tauri is the first candidate.
- Fallback shell: Electron remains acceptable if Tauri sidecar, WebView, or
  signing friction becomes unacceptable.
- Windows-only fallback: WebView2 may be reconsidered only if macOS parity is no
  longer required.
- Backend: packaged Python sidecar owned by the desktop shell process.
- Frontend: existing Angular build served locally by the backend for the first
  prototype unless a later task explicitly changes that plan.
- Runtime: packaged backend dependencies, bundled platform-specific ffmpeg, and
  yt-dlp available inside the packaged backend environment.
- Scope: local-only personal use, beginner-friendly launch, no public hosting.

## Lifecycle State Machine

The desktop wrapper owns the lifecycle. The backend sidecar must be treated as a
child process, not as an independently managed system service.

| State | Meaning | Allowed Next States |
| --- | --- | --- |
| `not_started` | Desktop shell is open but backend has not been started. | `initializing_paths`, `failed` |
| `initializing_paths` | Per-user app, state, download, temp, and log paths are being checked or created. | `starting_backend`, `failed` |
| `starting_backend` | Backend sidecar process has been spawned with desktop env overrides. | `waiting_for_ready`, `failed` |
| `waiting_for_ready` | Wrapper is polling local readiness and has not loaded the main UI yet. | `ready`, `failed` |
| `ready` | Backend is reachable and frontend can connect. | `active_work`, `stopping`, `failed` |
| `active_work` | Downloads, conversions, or queue work are active. | `ready`, `stopping`, `failed` |
| `stopping` | Wrapper is shutting down UI and backend sidecar. | `stopped`, `failed` |
| `stopped` | Backend sidecar has exited and wrapper can quit. | `not_started` |
| `failed` | Startup, readiness, runtime, or shutdown failed. | `stopping`, `recoverable_previous_exit` |
| `recoverable_previous_exit` | Previous run exited unexpectedly but persisted state is available. | `initializing_paths`, `failed` |

`active_work` is a user-visible lifecycle condition. It does not imply a second
backend mode or a background daemon.

## Desktop Wrapper Responsibilities

Future desktop implementation must handle all of the following before it is
considered beginner-ready:

- Enforce a single visible app instance per user profile.
- Select a local port for the backend and never expose an external bind option
  in the beginner flow.
- Start the backend sidecar with desktop-specific environment overrides.
- Create or verify per-user app, state, download, temp, and log directories
  before spawning the backend.
- Wait for backend readiness before loading the primary UI.
- Display startup failure details in beginner-readable language while keeping
  raw logs available from a local help/troubleshooting action.
- Monitor the sidecar process and surface abnormal exit status.
- Own close/quit behavior, including active-download confirmation.
- Stop the sidecar on normal app quit.
- Avoid automatic restart loops after repeated backend failures.
- Keep update diagnostics readonly. The desktop shell must not apply updates.

## Required Backend Environment Overrides

The desktop shell must not rely on container defaults. A future implementation
must set a minimal explicit desktop environment for the sidecar:

- `HOST=127.0.0.1`
- `PORT=<wrapper-selected-local-port>`
- `DOWNLOAD_DIR=<per-user-default-download-folder>`
- `AUDIO_DOWNLOAD_DIR=<per-user-default-audio-folder-or-download-folder>`
- `TEMP_DIR=<per-user-temp-folder>`
- `STATE_DIR=<per-user-state-folder>`
- `DOWNLOAD_DIRS_INDEXABLE=false`
- `ALLOW_YTDL_OPTIONS_OVERRIDES=false`

The wrapper must not set a public host, public tunnel, reverse proxy, LAN mode,
or hosted mode in the beginner desktop path.

## Readiness Contract

The first prototype may use existing endpoints and static asset behavior for
readiness, but future implementation must document the exact checks before code
lands.

Minimum readiness checks:

- Backend process is alive.
- Local TCP connection to `127.0.0.1:<port>` succeeds.
- `GET /version` returns a successful response.
- Frontend static entry can be loaded.
- Socket.IO connection succeeds or the UI reports a controlled retry state.

Failure behavior:

- Do not open a blank webview as if startup succeeded.
- Show a local-only failure screen with a way to copy sanitized diagnostics.
- Do not include cookie, token, secret, or private URL values in diagnostics.
- Do not try Docker pull, git pull, package install, or update apply as a
  startup repair action.

## Close And Stop Contract

The beginner desktop app needs explicit, predictable close behavior.

Idle close:

- Window close may stop the sidecar and quit.
- Quit must wait for a bounded graceful backend shutdown attempt.
- If graceful stop times out, the wrapper may terminate the child process and
  report that state will be recovered on next launch.

Active work close:

- Window close must ask for confirmation while downloads, conversions, or queue
  work are active.
- The prompt must make the consequence concrete: keep the app open, stop and
  quit, or cancel closing.
- No hidden background-daemon behavior is approved for the beginner flow.
- Queue and completed state must remain persisted by the backend state store.

Abnormal backend exit:

- The wrapper must detect child process exit.
- The UI must move to a failed or recoverable state instead of continuing as if
  downloads are still running.
- Next launch should treat persisted queue/state as recoverable data.

OS shutdown:

- The wrapper should attempt graceful stop.
- It must not block indefinitely.
- It must not create backups, rollback targets, update attempts, or package
  installs during shutdown.

## Path Contract

Future desktop implementation must keep runtime data out of the install
directory.

Windows candidate paths:

- App data/config/logs: `%LOCALAPPDATA%\MeTube`
- State: `%LOCALAPPDATA%\MeTube\state`
- Temp: `%LOCALAPPDATA%\MeTube\temp`
- Default downloads: `%USERPROFILE%\Downloads\MeTube`

macOS candidate paths:

- App data/config/logs: `~/Library/Application Support/MeTube`
- State: `~/Library/Application Support/MeTube/state`
- Temp: `~/Library/Caches/MeTube`
- Default downloads: `~/Downloads/MeTube`

Path rules:

- Do not write mutable data into the installed app bundle or program folder.
- Allow the user to choose a download folder later, but start with one safe
  beginner default per OS.
- Store config as local app settings only, not as credentials.
- Do not store cookie, token, or secret values in the beginner desktop flow.
- Clean temp files only inside the known per-user temp directory.
- Never recursively delete a computed path unless it has been resolved and
  verified under the intended app-owned directory.

## Package Contract

Y-06B does not package the app. A future packaging task must produce an explicit
manifest before build scripts are added. Y-06C refines that manifest in
`docs/llmwiki/desktop-package-manifest.md`.

Required package contents:

- Desktop launcher shell.
- Backend sidecar bundle.
- Built frontend assets.
- Platform-specific ffmpeg binary or documented ffmpeg bundle.
- Required backend Python runtime/dependencies.
- License notices for bundled third-party runtime pieces.
- Beginner `.html` guide.
- Plain `.txt` troubleshooting or offline help guide.

Required package exclusions:

- `.git`
- `.github`
- tests and test caches
- local virtual environments
- `node_modules`
- build caches
- downloaded media
- state files
- temp files
- logs containing private data
- cookie files
- tokens, secrets, private env files, and credentials
- unrelated upstream PR #1001 files

Windows package boundary:

- Installer and portable layouts may both be considered in future docs.
- SmartScreen/signing behavior must be documented before beginner release.
- Package must not require Docker Desktop.
- Package must not require the user to run `python`, `uv`, `pnpm`, or `npm`.

macOS package boundary:

- App bundle and disk image layouts may both be considered in future docs.
- Gatekeeper, signing, and notarization behavior must be documented before
  beginner release.
- Architecture strategy must be explicit: universal package or separate
  arm64/x64 packages.
- Package must not require Docker Desktop, Homebrew, Python setup, or Node.js
  setup for beginner use.

## Beginner Guide Contract

The beginner guide should be documentation-first and Japanese-first, but this
contract does not add user-facing copy to the app. Y-06C refines the guide
skeleton in `docs/llmwiki/beginner-guide-skeleton.md`.

The `.html` and `.txt` guides should cover:

- What the app does.
- Local-only behavior.
- How to start the app.
- Where downloaded files are saved.
- How to change the save folder when that feature is approved.
- How to see whether the backend is running.
- How to quit safely.
- What happens if the app is closed during a download.
- How to open logs or troubleshooting information.
- What update diagnostics mean.
- What the app intentionally does not do.

The guide must not encourage:

- Public hosting.
- LAN sharing.
- Ads or monetization.
- Cookie/token/secret handling.
- DRM bypass, authentication bypass, or restriction circumvention.
- Automatic update apply.

## Status And Monitoring Contract

The desktop shell may use readonly backend status signals, but it must not turn
diagnostics into mutating behavior.

Allowed status sources:

- Backend process state.
- Local readiness checks.
- `/version`
- Socket.IO queue/status events.
- Existing readonly update diagnostics.
- Sanitized local logs.

Not allowed:

- Update apply from a desktop status panel.
- Docker pull from a desktop status panel.
- git pull / merge / rebase from a desktop status panel.
- pip install, package install, or package update from a desktop status panel.
- Reading, uploading, transforming, or saving real cookie/token/secret values.

## Safety Gates For Future Implementation

Before any Tauri/Electron/WebView2 implementation begins, a later task should
confirm all of the following:

- This contract is still the accepted source of truth.
- Package manifest exists and has been reviewed.
- Beginner guide outline exists and has been reviewed.
- Sidecar bind is forced to `127.0.0.1`.
- State/download/temp paths are per-user and install-directory-safe.
- Close behavior has a testable active-work confirmation path.
- Failure diagnostics are sanitized.
- Cookie/token/secret features are excluded or disabled for beginner desktop
  mode.
- No update apply behavior is added.
- No Docker pull, git pull / merge / rebase, restart, pip install, package
  install, or package update is added.

## Open Items

These remain unresolved and must be treated as future design work:

- Exact sidecar packaging method, such as PyInstaller one-folder or another
  Python runtime bundle.
- Whether the first implementation PR uses Tauri directly or adds one more
  shell-choice design checkpoint.
- ffmpeg distribution, license notices, and per-OS binary sourcing.
- Whether Deno/bgutil-related runtime pieces are needed outside Docker for the
  beginner desktop package.
- Windows signing and SmartScreen plan.
- macOS signing, notarization, and architecture plan.
- Whether existing cookie UI/API is hidden, disabled, or left outside the
  beginner desktop entry path in a future frontend task.
- Exact local port lock or stale-process recovery mechanism.

## Y-06C Follow-Up

Y-06C refines this contract with docs-only package manifest and beginner guide
skeleton documents:

- `docs/llmwiki/desktop-package-manifest.md`
- `docs/llmwiki/beginner-guide-skeleton.md`

Implementation, build scripts, installers, signing, backend changes, frontend
changes, Docker changes, CI changes, package changes, and lockfile changes
remain out of scope until a later task explicitly approves them.
