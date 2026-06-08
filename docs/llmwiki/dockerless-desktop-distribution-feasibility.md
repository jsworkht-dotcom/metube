# Dockerless Desktop Distribution Feasibility

## Scope

Y-06A audits whether this local-only MeTube fork can be distributed as a
beginner-friendly desktop-app-like package without Docker Desktop.

This is documentation only. It does not implement Tauri, Electron, WebView2,
packaging, installers, signing, notarization, updater logic, backend changes,
frontend changes, Docker changes, CI changes, dependency installation, or build
artifacts.

Safety scope:

- Local-only personal use.
- Windows and macOS are the target desktop platforms.
- No public hosting.
- No external-user service.
- No ads or monetization.
- No DRM bypass, authentication bypass, restriction circumvention, or
  mass-download optimization.
- No cookie, token, or secret handling.
- Update apply remains not implemented.
- Upstream PR #1001 files stay out of this fork-only work.

## Sources Checked

Repository sources checked:

- `docs/llmwiki/current-state.md`
- `docs/llmwiki/safety-boundaries.md`
- `docs/llmwiki/roadmap.md`
- `docs/llmwiki/handoff.md`
- `pyproject.toml`
- `ui/package.json`
- `app/main.py`
- `app/ytdl.py`
- `app/state_store.py`
- `app/subscriptions.py`
- `Dockerfile`
- `.github/workflows/main.yml`

External official references checked on 2026-06-08:

- Tauri overview and app size:
  https://v2.tauri.app/start/
- Tauri prerequisites:
  https://v2.tauri.app/start/prerequisites/
- Tauri WebView versions:
  https://v2.tauri.app/reference/webview-versions/
- Tauri external binaries / sidecars:
  https://v2.tauri.app/develop/sidecar/
- Tauri opener plugin:
  https://v2.tauri.app/plugin/opener/
- Tauri Windows installer:
  https://v2.tauri.app/distribute/windows-installer/
- Tauri macOS signing:
  https://v2.tauri.app/distribute/sign/macos/
- Electron overview:
  https://www.electronjs.org/
- Electron process model:
  https://www.electronjs.org/docs/latest/tutorial/process-model
- Electron security:
  https://www.electronjs.org/docs/latest/tutorial/security/
- Electron utilityProcess:
  https://www.electronjs.org/docs/latest/api/utility-process
- Electron shell:
  https://www.electronjs.org/docs/latest/api/shell
- Electron app paths:
  https://www.electronjs.org/docs/latest/api/app
- PyInstaller spec files:
  https://pyinstaller.org/en/latest/spec-files.html
- yt-dlp README:
  https://github.com/yt-dlp/yt-dlp
- FFmpeg legal notes:
  https://www.ffmpeg.org/legal.html
- Microsoft WebView2 distribution:
  https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution
- Microsoft SmartScreen reputation:
  https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation
- Apple macOS code-signing security guide:
  https://support.apple.com/guide/security/app-code-signing-process-sec3ad8e6e53/web
- Apple Xcode outside-Mac-App-Store distribution guide:
  https://help.apple.com/xcode/mac/current/en.lproj/dev033e997ca.html

## Existing Baseline

Backend:

- Python 3.13+ aiohttp app with python-socketio 5.x.
- `yt-dlp[default,curl-cffi,deno]` is a Python dependency, and the backend uses
  the yt-dlp Python API rather than shelling out to the standalone executable.
- `Config._DEFAULTS` currently uses `HOST=0.0.0.0`, `PORT=8081`,
  `DOWNLOAD_DIR=.`, `STATE_DIR=.`, and `TEMP_DIR=%%DOWNLOAD_DIR` outside the
  Docker image.
- The Docker image overrides paths to `/downloads` and installs `ffmpeg`.
- Download work uses multiprocessing around yt-dlp work.
- Persistent state is JSON via `AtomicJsonStore`; legacy shelve import support
  still exists.

Frontend:

- Angular 21 standalone app.
- Static assets are served by aiohttp from `ui/dist/metube/browser`.
- The UI uses relative HTTP endpoints and Socket.IO events.
- The existing UI already has readonly version/update-status footer visibility.

Container-only assumptions that matter for desktop:

- The Docker image installs `ffmpeg`, Deno, aria2, curl, tini, gosu, and a Linux
  bgutil POT provider.
- Docker entrypoint performs container-specific ownership and startup behavior.
- Desktop packaging must replace those container assumptions with explicit
  Windows/macOS runtime assets and desktop launcher environment.

## Feasibility Verdict

Dockerless desktop distribution is feasible for a local-only personal-use fork,
but it is not beginner-ready from the current repository state.

Recommended candidate:

- Tauri desktop shell.
- Existing Angular UI reused as built static assets.
- Python backend packaged as a sidecar, likely via PyInstaller one-folder
  output.
- Bundled platform-specific ffmpeg binaries.
- App-controlled `127.0.0.1` backend launch, readiness wait, status display,
  close confirmation, and controlled shutdown.

Why Tauri is preferred:

- It supports Windows and macOS.
- It can use the existing Angular web UI.
- It avoids bundling a full browser engine and keeps framework overhead low.
- Its sidecar and opener capabilities match the required backend launch and
  "open save folder" workflows.

Why this is not ready to ship yet:

- There is no desktop shell.
- There is no packaged backend sidecar.
- There is no desktop-specific path contract.
- There is no backend lifecycle contract for app close / stop / quit.
- There is no signing or notarization pipeline.
- ffmpeg, yt-dlp, Deno, and the bgutil provider need platform-specific packaging
  and license review.
- Cookie/token/secret features must remain out of the beginner desktop flow.

## Candidate Matrix

| Candidate | Fit | Strengths | Risks | Verdict |
| --- | --- | --- | --- | --- |
| Tauri | Best fit | Windows/macOS, Angular-compatible, low shell overhead, sidecars, opener plugin | Rust/toolchain learning curve, OS webview variance, sidecar packaging and signing complexity | Primary candidate |
| Electron | Feasible fallback | Windows/macOS, Angular-compatible, bundled Chromium consistency, mature desktop APIs | Larger package, stricter IPC/security work, Node/Chromium update surface | Keep as fallback |
| WebView2 native wrapper | Windows-only | Good Windows integration, small when runtime already exists | Not macOS, runtime detection/installation needed on some systems, separate macOS solution still required | Windows-only fallback, not primary |

## Tauri Feasibility

### Platform Support

Tauri documentation targets Windows and macOS desktop apps. Current Tauri docs
list macOS Catalina 10.15+ and Windows 7+ in prerequisites. Tauri uses WebView2
on Windows and WKWebView/WebKit on macOS.

Implications:

- Windows 11 includes WebView2; Windows 10 and older Windows targets still need
  runtime presence checked or handled by the installer.
- macOS WebKit is an OS component, so very old unsupported macOS versions may
  have outdated web platform behavior.
- The existing Angular app should stay within ordinary WebView-compatible
  browser APIs.

### Existing Angular UI

The existing UI can be reused because it builds to static HTML, CSS, and JS.
Two possible models exist:

1. Keep aiohttp serving `ui/dist/metube/browser` and let the Tauri window load
   `http://127.0.0.1:<port>/`.
2. Let Tauri serve frontend assets and proxy or configure API/socket endpoints
   to the backend.

Lower-risk first prototype:

- Keep the backend serving the existing built UI.
- Start the backend sidecar first.
- Wait for readiness.
- Open the Tauri window to the local backend URL.

This preserves current HTTP and Socket.IO behavior and avoids rewriting the UI
transport boundary in the first desktop prototype.

### Backend Launch And Stop

Tauri sidecars are designed for bundling external binaries. Common documented
use cases include Python CLI applications or API servers packaged by tools such
as PyInstaller.

Feasible launch contract:

- Bundle one backend executable per OS/architecture.
- Launch it as a Tauri sidecar.
- Set desktop-specific environment variables:
  - `HOST=127.0.0.1`
  - `PORT=<reserved local port>`
  - `DOWNLOAD_DIR=<user downloads folder>/MeTube`
  - `AUDIO_DOWNLOAD_DIR=<same or user-selected folder>`
  - `STATE_DIR=<per-user app data>/state`
  - `TEMP_DIR=<per-user app data>/temp`
  - `DOWNLOAD_DIRS_INDEXABLE=false`
  - `ALLOW_YTDL_OPTIONS_OVERRIDES=false`
- Wait until `/version` or another readonly health endpoint responds.
- Load the window only after the backend is ready.
- Track the child process PID and exit status.

Stop/quit still needs design:

- The current backend does not expose a desktop shutdown contract.
- Future work should define how the shell distinguishes idle, queued, active,
  failed, and shutting-down states.
- Close should be intercepted when downloads are active.
- Quit should prefer graceful shutdown, then bounded forced termination only
  after explicit user confirmation.

### Open Save Folder

Tauri's opener plugin can open files/URLs and reveal files in the system file
explorer. This matches the desktop UX requirement for "open save folder".

Required future boundary:

- The frontend must not receive broad filesystem powers.
- The shell should expose only a narrow "open configured download folder" command
  or "reveal this completed file" command.
- Paths should come from backend-controlled completed-download records or desktop
  settings, not arbitrary UI text.

### In-App Help

The current app has UI help popovers for some advanced options, but not a full
desktop first-run guide. Tauri does not block adding this; the work is frontend
UX planning and copy.

Minimum Level 3 help areas:

- First launch confirmation that the app is local-only.
- Where files are saved.
- How to stop safely.
- What update status means.
- What Windows/macOS security warnings mean.
- What is intentionally unsupported, including cookies, public hosting, and
  update apply.

### Close Safety

Tauri can own window close behavior, but the product rule must be documented
before implementation.

Required close states:

- No active work: quit after stopping backend.
- Queued but not active: ask whether to keep queue for next launch or clear it.
- Active download: show "finish current download", "cancel and quit", and
  "keep running" choices.
- Backend not responding: show a recovery prompt and preserve state if possible.

### Package Size And Development Load

Tauri's shell overhead is likely smaller than Electron because it uses the
system webview instead of bundling a browser engine. However, this app's real
package size will be dominated by:

- Python runtime and Python dependencies.
- yt-dlp and its dependencies.
- ffmpeg binaries.
- Optional Deno/bgutil parity assets.
- Codesigning and notarization metadata.

No package size should be claimed until a future prototype is built and measured.

Development load is medium-high:

- Rust/Tauri project setup.
- PyInstaller or equivalent backend packaging.
- Per-platform ffmpeg/yt-dlp/runtime packaging.
- App lifecycle and close safety.
- Signing/notarization.
- Beginner documentation in `.html` and `.txt` forms.

## Electron Feasibility

Electron is also feasible for Windows/macOS and can reuse the Angular UI.

Strengths:

- It bundles Chromium and Node.js, making browser behavior more predictable than
  OS webviews.
- The main process can own native desktop integration, app windows, and process
  launching.
- Electron's `shell` module can open paths or reveal files in the file manager.
- Electron has mature desktop packaging ecosystems, though none are currently
  added to this repository.

Required security boundary:

- Keep Node integration disabled in renderer windows.
- Keep context isolation enabled.
- Use a narrow preload IPC bridge.
- Do not expose shell execution, arbitrary path open, or arbitrary filesystem
  access to Angular.
- Load local app content only.
- Keep public hosting and remote content out of scope.

Tradeoffs:

- The package will be larger because Electron embeds Chromium and Node.js.
- The desktop shell will add a second JavaScript runtime/tooling layer.
- Security review is more demanding because renderer-to-main IPC can easily
  become too broad.
- The backend sidecar, ffmpeg, signing, and beginner UX risks remain the same as
  Tauri.

Verdict:

- Use Electron only if a Tauri prototype hits unacceptable WebView, sidecar, or
  signing friction.

## WebView2 Feasibility

WebView2 is useful only as a Windows-specific option.

Strengths:

- Strong Windows integration.
- Windows 11 includes the Evergreen WebView2 Runtime.
- Microsoft documents runtime detection and installation workflows for older or
  incomplete systems.

Risks:

- It does not solve macOS distribution.
- Some Windows systems may still need runtime detection or installation.
- A native WebView2 shell would create a separate Windows implementation unless
  paired with another macOS framework.

Verdict:

- Do not choose WebView2 as the primary Y-06 path because Windows/macOS parity is
  a requirement.
- Keep it as a Windows-only fallback if Tauri and Electron are both rejected.

## Dockerless Backend Runtime

### Python Backend

Preferred first packaging model:

- PyInstaller one-folder backend executable.
- Include Python modules and dynamic libraries inside the sidecar folder.
- Include the built Angular UI if the backend continues to serve static assets.
- Launch through the desktop shell with explicit environment variables.

Why one-folder is preferred for the first prototype:

- It is easier to inspect and sign/notarize bundled native binaries.
- ffmpeg and other helper executables can live at stable paths.
- It avoids one-file temporary extraction surprises for a long-running local
  server.

Needs verification:

- PyInstaller compatibility with Python 3.13, aiohttp, python-socketio,
  watchfiles, curl-cffi, yt-dlp extras, multiprocessing, and Windows/macOS
  signing.
- Whether multiprocessing startup needs special frozen-app handling on Windows
  or macOS.
- Whether the backend should continue serving frontend assets or hand that to
  the shell.

### yt-dlp

The current backend imports and calls yt-dlp as a Python library. Therefore the
lowest-risk desktop plan is to bundle the Python package dependency inside the
backend sidecar.

yt-dlp also publishes standalone Windows and macOS executables, but switching
the backend to those executables would be an implementation change and should
not be part of Y-06A.

Desktop update posture:

- Show included yt-dlp version.
- Keep update status readonly.
- Do not add automatic update apply.
- Do not download or replace yt-dlp from the desktop app in this phase.

Needs verification:

- License notices for yt-dlp release files and bundled dependencies.
- Whether Deno support from `yt-dlp[default,curl-cffi,deno]` requires bundling a
  Deno executable for parity with the Docker image.
- Whether the current Linux-only bgutil provider install has a supported
  Windows/macOS desktop equivalent.

### ffmpeg

ffmpeg is currently installed by the Docker image. A Dockerless desktop build
must explicitly bundle or locate ffmpeg.

Preferred beginner distribution:

- Bundle known ffmpeg binaries per OS/architecture.
- Configure yt-dlp to find the bundled ffmpeg path.
- Include FFmpeg license notices and source/build attribution appropriate to the
  selected binary distribution.
- Sign/notarize bundled native binaries where required.

Needs verification:

- Whether selected ffmpeg binaries are LGPL-only or GPL-enabled.
- Whether redistribution terms, patent risk, source offer requirements, and
  attribution are acceptable for this personal local-only fork.
- Whether macOS notarization accepts the selected binaries after signing.

### App State And Downloads

Do not write mutable state into the install directory or app bundle.

Recommended desktop defaults:

- Windows state: per-user app data, for example under `%APPDATA%` or
  `%LOCALAPPDATA%`.
- macOS state: `~/Library/Application Support/<app-name>`.
- Downloads: `~/Downloads/MeTube` or a user-selected folder.
- Temp: per-user app data temp folder or OS temp under an app-specific
  subdirectory.

The desktop launcher should override current backend defaults explicitly.

Path requirements:

- Use platform path APIs, not shell string concatenation.
- Preserve non-ASCII paths.
- Handle spaces in paths.
- Handle Windows drive letters and backslashes.
- Avoid long-path surprises on Windows.
- Validate that "open folder" operations are limited to configured download
  roots or completed-file paths.

## Beginner UX Requirements

Level 3 desktop-app-like UX is possible, but it requires more than packaging.

Minimum UX contract:

- First-run guide in Japanese with short, concrete copy.
- Clear local-only statement.
- Download folder selection or a clearly shown default folder.
- "Open save folder" button.
- Startup status:
  - Starting backend.
  - Checking tools.
  - Ready.
  - Backend failed.
- Runtime status:
  - Queue count.
  - Active download count.
  - Current speed.
  - Completed/errors.
- Stop/quit flow:
  - Quit now when idle.
  - Ask before quitting during active downloads.
  - Offer "finish current download first" if supported in future.
- Friendly errors:
  - Cannot write to save folder.
  - ffmpeg unavailable or unusable.
  - yt-dlp extraction failed.
  - Backend failed to start.
  - Local port unavailable.
  - macOS/Windows blocked app launch.
- Settings split:
  - Basic: save folder, theme, startup behavior, update visibility.
  - Advanced: output template and expert options, with safe defaults.
- Update display:
  - Show MeTube and yt-dlp versions.
  - Show readonly update availability.
  - Explain that applying updates is manual and not implemented.

Beginner package docs:

- `.html` guide for normal users.
- `.txt` fallback for users who cannot open the HTML.
- `.md` only for LLMwiki and developer planning.

## Distribution Package

### Windows

Candidate forms:

- Signed setup executable or MSI for beginner distribution.
- Portable `.zip` only as a personal fallback, not the preferred beginner path.

Expected contents:

- Desktop shell executable.
- Backend sidecar folder.
- ffmpeg binaries.
- Built UI assets, if served by the backend.
- License and notices for MeTube, yt-dlp, ffmpeg, bundled Python dependencies,
  and desktop shell dependencies.
- `.html` beginner guide.
- `.txt` fallback guide.
- Version manifest.

Warnings:

- Unsigned packages should be expected to trigger SmartScreen warnings.
- Even OV/EV signed binaries can show "unrecognized" warnings until reputation
  accumulates.
- Self-signed certificates behave like no trusted signature for normal users.

### macOS

Candidate forms:

- Signed and notarized `.dmg` for beginner distribution.
- Unsigned `.zip` or `.dmg` only as a personal fallback with clear warnings.

Expected contents:

- App bundle.
- Backend sidecar and helper binaries inside the bundle resources.
- ffmpeg binaries.
- Built UI assets, if served by the backend.
- License and notices.
- `.html` beginner guide.
- `.txt` fallback guide.
- Version manifest.

Warnings:

- macOS Gatekeeper expects Developer ID signing and notarization for apps
  distributed outside the Mac App Store under default settings.
- Bundled helper executables and native libraries need signing attention.
- Separate x64/arm64 packages or a universal package must be chosen and tested.

### Exclusions

Desktop distribution packages must exclude:

- `.git/`
- `.github/`
- `app/tests/`
- `ui/node_modules/`
- `ui/.angular/`
- build caches and test caches
- local downloads
- local state
- logs containing user URLs or filesystem paths when not needed
- cookies, tokens, secrets, or private config values
- Docker-only files unless explicitly needed for notices
- upstream PR #1001 files:
  - `docker-compose.local.yml`
  - `docs/local-only.md`
- package manager caches
- source maps if they expose unnecessary local paths or internals

## Security And Safety

Desktop mode must tighten local-only assumptions:

- Bind backend to `127.0.0.1`, not `0.0.0.0`.
- Prefer a shell-selected local port over a fixed public-facing default.
- Do not add firewall exceptions for inbound LAN access.
- Keep CORS limited to the desktop shell/local origin.
- Keep `DOWNLOAD_DIRS_INDEXABLE=false`.
- Keep `ALLOW_YTDL_OPTIONS_OVERRIDES=false`.
- Avoid `PUBLIC_HOST_URL` values that imply public hosting.
- Do not add public tunnels, reverse proxies, HTTPS hosting, or external service
  modes.

Credential boundary:

- Do not include cookie upload/import in the beginner desktop flow.
- Do not read, store, print, copy, or document real cookie/token/secret values.
- Existing cookie-related code is a release risk for this safety profile and
  needs a future desktop-mode decision before beginner distribution.

Downloader boundary:

- Do not add DRM bypass, authentication bypass, restriction bypass, or
  mass-download optimization.
- Do not add automation that retries around site restrictions.
- Do not expose arbitrary yt-dlp options to beginner users.

Update boundary:

- Update apply remains not implemented.
- No Docker pull.
- No git pull / merge / rebase.
- No restart-based updater.
- No pip install or package update from the desktop app.
- Version/update display remains readonly until a future explicitly approved
  update-apply phase.

## Signing And Warning UX

Windows:

- SmartScreen app reputation is separate from "the file is validly signed".
- New or rare apps can still show warnings until reputation accumulates.
- Unsigned apps show stronger warnings and may be blocked by enterprise policy.
- Beginner docs must explain exactly what warning may appear and when to stop.

macOS:

- Default Gatekeeper settings expect Developer ID signing and notarization for
  apps distributed outside the Mac App Store.
- Unsigned or unnotarized builds are not beginner-friendly.
- Beginner docs must explain that a warning is a platform trust signal, not a
  normal setup step to click through casually.

## Risk Register

| Risk | Severity | Notes | Mitigation |
| --- | --- | --- | --- |
| Backend lifecycle unclear | High | Active downloads must not be killed silently | Define desktop lifecycle contract before implementation |
| Local bind defaults too broad | High | Current backend default is `0.0.0.0` | Desktop launcher must force `127.0.0.1` |
| Cookie feature conflicts with safety scope | High | Current app has cookie upload/status/delete endpoints | Disable or exclude from desktop beginner flow in future work |
| ffmpeg redistribution/signing | High | License and native binary signing vary by build | Select known binaries, document notices, sign/notarize |
| PyInstaller compatibility | Medium | Python 3.13, multiprocessing, curl-cffi, yt-dlp extras need proof | Build a narrow prototype later |
| macOS Gatekeeper | Medium | Unsigned/unnotarized builds are poor beginner UX | Plan Developer ID/notarization or mark as personal fallback |
| Windows SmartScreen | Medium | Even signed apps may warn at first | Set beginner expectations and consider trusted signing |
| OS webview variance | Medium | Tauri uses system webviews | Keep Electron fallback; test Angular UI on both platforms |
| Deno/bgutil parity | Medium | Docker installs Linux-specific runtime/provider assets | Decide parity vs reduced support explicitly |
| Package size unknown | Low | No build performed in Y-06A | Measure in a future prototype |

## Acceptance Gates Before Beginner Distribution

A future implementation should not be considered Level 3 ready until all of
these are true:

- Windows app starts without Docker Desktop.
- macOS app starts without Docker Desktop.
- No user-installed Python is required.
- No user-installed Node.js or pnpm is required.
- No user-installed ffmpeg is required, unless explicitly documented as an
  advanced fallback.
- Backend binds only to `127.0.0.1`.
- Startup status is visible.
- Save folder is visible and openable.
- Active downloads trigger close confirmation.
- Backend shutdown is graceful or explicitly confirmed when forced.
- State survives restart.
- No cookies/tokens/secrets are requested in the beginner flow.
- Update apply is absent.
- Version/update display is readonly.
- Package includes `.html` user guide and `.txt` fallback.
- Package excludes development, secret, cache, test, and PR #1001 files.
- Windows signing/warning story is documented.
- macOS signing/notarization/warning story is documented.
- ffmpeg/yt-dlp licenses and notices are included.

## Recommendation

Adopt Tauri as the first desktop candidate.

Do not start by adding Tauri code. The safer next step is one more docs-only
contract that fixes the desktop process, path, package, and close-safety
boundaries before implementation begins.

Single next PR candidate:

- Y-06B desktop sidecar lifecycle and package contract docs.

Y-06B should define:

- backend sidecar start/ready/stop states
- close confirmation rules
- required desktop environment overrides
- state/download/temp directory contract
- local-only network contract
- package manifest and exclusions
- `.html` and `.txt` beginner guide outline
- explicit non-goals:
  - no Tauri/Electron implementation
  - no package/lockfile changes
  - no build/package creation
  - no updater implementation
  - no cookie/token/secret handling
