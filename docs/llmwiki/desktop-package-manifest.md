# Desktop Package Manifest Contract

## Purpose

Y-06C defines the documentation-only package manifest contract for a future
Level 3 beginner desktop distribution.

This contract fixes the visible package shape before any clean-package
generator, Tauri/Electron project, installer, build script, or distribution
folder is created.

This document does not create packages, generate files, add dependencies, change
application behavior, or approve implementation.

## Scope

Allowed in Y-06C:

- Document the beginner-facing package root layout.
- Document Windows and macOS package boundaries.
- Document include and exclude rules.
- Document generated path candidates for future implementation.
- Document user data, state, download, temp, config, license, notice, checksum,
  and manifest path contracts.
- Keep `.html` as the primary beginner guide, `.txt` as fallback, and `.md` as
  developer/LLMwiki planning only.

Not allowed in Y-06C:

- Creating the actual distribution folder.
- Creating actual `.html` or `.txt` guide files.
- Adding package generation scripts.
- Adding Tauri, Electron, WebView2, installer, signing, or notarization code.
- Running build, package, install, Docker pull, git pull, update apply, or
  dependency update commands.
- Changing backend, frontend, yt-dlp, extractor, Docker, CI, package, or
  lockfile files.

## Beginner Package Root

The future generated package root should be:

```text
動画保存ツール_ローカル専用/
  00_最初に開いてください.html
  00_最初に開いてください.txt
  Windows用/
  Mac用/
  保存先/
  困ったとき/
  開発者向け/
```

Rules:

- The root name must communicate local-only use.
- User-facing names may be Japanese.
- Developer-facing internals should stay under `開発者向け/`.
- The root must not include source control metadata, local state, logs,
  downloads, cookies, tokens, secrets, or personal backups.
- The root must be readable even when the user never opens a terminal.

## Root Files

### `00_最初に開いてください.html`

Purpose:

- Primary beginner guide.
- Opened first by normal users.
- Japanese-first, short, concrete, and local-only.
- Must avoid Docker, terminal, git, Python, Node.js, pnpm, npm, uv, Tauri, and
  Electron jargon in the visible beginner flow.

Future generated path:

```text
動画保存ツール_ローカル専用/00_最初に開いてください.html
```

### `00_最初に開いてください.txt`

Purpose:

- Plain-text fallback when the HTML guide cannot be opened.
- Shorter than the HTML guide.
- Copy/paste-friendly.
- No Markdown-specific formatting is required.

Future generated path:

```text
動画保存ツール_ローカル専用/00_最初に開いてください.txt
```

## Windows Package Skeleton

Future Windows package candidate:

```text
動画保存ツール_ローカル専用/
  Windows用/
    動画保存ツール.exe
    予備_起動する.bat
    予備_停止する.bat
    予備_保存先を開く.bat
    runtime/
    notices/
```

Required boundaries:

- `動画保存ツール.exe` is the primary beginner launch target.
- `.bat` files are fallback helpers only, not the normal beginner path.
- `.bat` helpers must not require the user to understand command-line tools.
- Package must not require Docker Desktop.
- Package must not require user-installed Python, Node.js, pnpm, npm, uv, or
  ffmpeg for the beginner path.
- Package must not create firewall exceptions or LAN service configuration.
- Backend launch must force `HOST=127.0.0.1`.

SmartScreen and signing notes:

- Unsigned packages are expected to show stronger warnings.
- Signed packages may still show reputation warnings for new or rare apps.
- The guide should explain that a warning is a platform trust signal and should
  not be clicked through casually.
- Beginner release readiness requires a reviewed signing/warning story.

Install model:

- Portable `.zip` may be acceptable for personal fallback testing.
- Installer/MSI/setup may be considered later for beginner distribution.
- Y-06C does not choose or implement either model.

## macOS Package Skeleton

Future macOS package candidate:

```text
動画保存ツール_ローカル専用/
  Mac用/
    動画保存ツール.app
    予備_起動する.command
    予備_停止する.command
    予備_保存先を開く.command
    runtime/
    notices/
```

Required boundaries:

- `動画保存ツール.app` is the primary beginner launch target.
- `.command` files are fallback helpers only, not the normal beginner path.
- Package must not require Docker Desktop, Homebrew, user-installed Python,
  Node.js, pnpm, npm, uv, or ffmpeg for the beginner path.
- Backend launch must force `HOST=127.0.0.1`.
- Helper executables inside the app/runtime must be considered part of signing
  and notarization planning.

Gatekeeper and signing notes:

- Unsigned or unnotarized apps are not beginner-friendly.
- The guide should explain that a warning is a platform trust signal and should
  not be treated as a normal setup step.
- Future work must decide between separate arm64/x64 packages and a universal
  package.
- `.dmg` is the preferred beginner candidate, but Y-06C does not create one.

## Shared User Folders

### `保存先/`

Purpose:

- Visible place that explains where downloads will be saved.
- May be a placeholder folder or guide location in a future generated package.
- Must not contain downloaded media in the clean package.

Rules:

- The actual default download path should be per-user and outside the install
  directory.
- Future implementation should prefer a safe OS default:
  - Windows: `%USERPROFILE%\Downloads\MeTube`
  - macOS: `~/Downloads/MeTube`
- The package root must not ship personal downloads.

### `困ったとき/`

Purpose:

- Beginner troubleshooting material.
- Sanitized local diagnostics guide.
- Platform warning explanations.

Candidate future files:

```text
動画保存ツール_ローカル専用/困ったとき/
  Windowsの警告について.html
  Macの警告について.html
  保存できないとき.html
  起動しないとき.html
  ログの見方.txt
```

Rules:

- Troubleshooting docs must not include real URLs, cookies, tokens, secrets, or
  private filesystem values.
- Troubleshooting must not recommend Docker pull, git pull, package install,
  update apply, public hosting, or credential handling.

### `開発者向け/`

Purpose:

- Developer and LLMwiki-oriented material.
- Not the normal beginner entry point.

Candidate future files:

```text
動画保存ツール_ローカル専用/開発者向け/
  README.md
  docs/
  docs/llmwiki/
  licenses/
  notices/
  manifest/
```

Rules:

- `.md` belongs here or in source docs, not as the primary beginner guide.
- Developer docs may mention Python, Angular, yt-dlp, ffmpeg, Tauri, Electron,
  package manifests, and diagnostics.
- Developer docs must still avoid real secrets and private values.

## Runtime Include Contract

A future clean package may include these categories after implementation is
explicitly approved:

- Desktop launcher shell.
- Backend sidecar bundle.
- Built Angular frontend assets.
- Python runtime/dependency bundle required by the sidecar.
- yt-dlp Python package and required dependencies.
- Platform-specific ffmpeg binaries.
- Optional Deno/bgutil parity assets only after platform-specific review.
- License files and notice files for bundled runtime pieces.
- Version manifest.
- Checksums or package manifest files.
- Primary `.html` guide and fallback `.txt` guide.

Y-06C does not create or validate any of these artifacts.

## Runtime Exclude Contract

Future clean packages must exclude:

- `.git/`
- `.github/`
- `.pytest_cache/`
- `.ruff_cache/`
- `.mypy_cache/`
- `.coverage`
- `node_modules/`
- `ui/node_modules/`
- `ui/.angular/`
- build caches
- test caches
- `downloads/`
- `state/`
- `logs/`
- `temp/`
- `.env`
- `.env.*`
- `cookies.txt`
- cookie files
- token files
- secret files
- private config values
- personal backups
- local virtual environments
- package manager caches
- local command logs
- dev branch metadata
- unrelated upstream PR #1001 files:
  - `docker-compose.local.yml`
  - `docs/local-only.md`

Source maps should be excluded from beginner packages unless a later task
explicitly confirms they do not expose local paths, private internals, or
unnecessary implementation detail.

## Generated Manifest Candidate

A future package generator should emit a manifest file, but Y-06C only defines
the candidate shape.

Candidate future path:

```text
動画保存ツール_ローカル専用/開発者向け/manifest/package-manifest.json
```

Candidate fields:

```text
package_name
package_kind
target_os
target_arch
app_version
metube_version
yt_dlp_version
ffmpeg_bundle_id
created_at
source_commit
included_files
excluded_patterns
runtime_paths
user_data_paths
download_paths
state_paths
config_paths
license_notice_paths
checksum_paths
safety_flags
```

Required safety flags:

- `local_only=true`
- `backend_bind=127.0.0.1`
- `public_hosting=false`
- `ads=false`
- `update_apply=false`
- `cookie_secret_handling=false`
- `docker_required=false`
- `user_python_required=false`
- `user_node_required=false`

The manifest must not store real cookie values, token values, secret values,
private URLs, personal download URLs, or private local paths beyond package
relative paths and documented default path templates.

## OS-Specific Runtime Paths

Windows candidate runtime paths inside the package:

```text
Windows用/runtime/backend/
Windows用/runtime/frontend/
Windows用/runtime/ffmpeg/
Windows用/runtime/licenses/
Windows用/runtime/notices/
```

macOS candidate runtime paths inside the package:

```text
Mac用/runtime/backend/
Mac用/runtime/frontend/
Mac用/runtime/ffmpeg/
Mac用/runtime/licenses/
Mac用/runtime/notices/
```

Rules:

- Runtime paths inside the package are immutable after install/extraction.
- Mutable state must be outside the package root.
- Runtime files must be treated as signed/notarized package contents in future
  implementation work.

## User Data Path Templates

Future desktop implementation should keep mutable data outside the package.

Windows:

```text
App data/config/logs: %LOCALAPPDATA%\MeTube
State: %LOCALAPPDATA%\MeTube\state
Temp: %LOCALAPPDATA%\MeTube\temp
Default downloads: %USERPROFILE%\Downloads\MeTube
```

macOS:

```text
App data/config/logs: ~/Library/Application Support/MeTube
State: ~/Library/Application Support/MeTube/state
Temp: ~/Library/Caches/MeTube
Default downloads: ~/Downloads/MeTube
```

Rules:

- Package generation must not prefill these paths with personal data.
- The beginner guide may show these as templates, not as private values.
- Future implementation must verify resolved paths before cleanup operations.
- Future implementation must preserve non-ASCII paths and spaces.

## Config Sample Contract

Future package docs may include a config sample only if it contains safe
templates and no secrets.

Candidate future path:

```text
動画保存ツール_ローカル専用/開発者向け/manifest/config-sample.json
```

Allowed sample content:

- Local bind template.
- Port strategy description.
- Default download path template.
- State/temp path templates.
- Safe boolean flags such as local-only and no update apply.

Not allowed:

- `.env` files.
- Real personal paths.
- Real URLs submitted by the user.
- Cookie file references.
- Tokens, secrets, credentials, API keys, or private config values.

## License And Notice Contract

Future package work must include license and notice material for bundled pieces.

Candidate future paths:

```text
動画保存ツール_ローカル専用/開発者向け/licenses/
動画保存ツール_ローカル専用/開発者向け/notices/
Windows用/notices/
Mac用/notices/
```

Candidate notice categories:

- MeTube source license.
- yt-dlp license/notice.
- Python runtime and bundled Python dependency notices.
- Angular/frontend dependency notices.
- ffmpeg binary license and source/build attribution.
- Desktop shell runtime notices after Tauri/Electron choice is approved.
- Deno/bgutil notices only if those runtime pieces are included later.

Y-06C does not perform legal review. It only reserves the notice locations and
requires future review before beginner distribution.

## Checksum Contract

A future clean package may include checksums for generated artifacts.

Candidate future paths:

```text
動画保存ツール_ローカル専用/開発者向け/manifest/checksums.txt
動画保存ツール_ローカル専用/開発者向け/manifest/checksums.json
```

Rules:

- Checksums should cover package files, not user data.
- Checksums must not include secret values.
- Checksums must not be described to beginners as a required terminal workflow.

## Clean Package Gate

Before any package generator is implemented, a later task should verify:

- This manifest contract is still accepted.
- Beginner guide skeleton is accepted.
- The sidecar lifecycle contract is accepted.
- Package includes/excludes are explicit.
- Runtime license/notice plan has an owner.
- Windows warning/signing language is drafted.
- macOS warning/signing language is drafted.
- No generated distribution folder is added by the docs task.
- No backend/frontend/Docker/CI/package/lockfile change is mixed into package
  planning.

## Next PR Candidate

Y-06D added the docs-only clean-package generator dry-run contract in
`docs/llmwiki/clean-package-dry-run-contract.md`.

The next candidate is Y-06E report-only dry-run script implementation:

- Read this manifest contract and the related LLMwiki contracts.
- Emit sanitized JSON/Markdown reports only.
- Validate unsafe paths, excluded files, forbidden filename families, forbidden
  content pattern families, generated distribution folders, local-only notice
  requirements, Windows/macOS section completeness, and PR #1001 leakage.
- Keep actual package generation, file copying, build scripts, installers,
  signing, backend changes, frontend changes, Docker changes, CI changes,
  package changes, and lockfile changes out of scope.
