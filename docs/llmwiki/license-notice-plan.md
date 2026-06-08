# License Notice Plan

## Purpose

Y-06F reviews license and notice candidates for a future clean beginner
package.

This is documentation-only planning. It does not copy license texts, generate
notice bundles, build packages, create `動画保存ツール_ローカル専用/`, or perform
legal review.

## Scope

Allowed in Y-06F:

- Identify likely license and notice categories for future package review.
- Identify local source-of-truth candidates.
- Define future package placement candidates.
- Define dry-run warning candidates for missing guide/notice sources.
- Choose one next implementation candidate.

Not allowed in Y-06F:

- Copying third-party license bodies into package folders.
- Creating a license bundle.
- Creating generated package files.
- Running dependency license scanners.
- Installing or updating dependencies.
- Changing backend, frontend, Docker, CI, package, or lockfile files.
- Adding Tauri, Electron, WebView2, installer, signing, or notarization code.

## Sources Checked Locally

Local files checked for this planning pass:

- `LICENSE`
- `README.md`
- `pyproject.toml`
- `ui/package.json`
- `Dockerfile`
- `docs/llmwiki/dockerless-desktop-distribution-feasibility.md`
- `docs/llmwiki/desktop-sidecar-lifecycle-contract.md`
- `docs/llmwiki/desktop-package-manifest.md`
- `docs/llmwiki/clean-package-dry-run-contract.md`

Existing LLMwiki notes already list external reference URLs for Tauri,
Electron, PyInstaller, yt-dlp, FFmpeg, WebView2, SmartScreen, and macOS signing
in `docs/llmwiki/dockerless-desktop-distribution-feasibility.md`.

## Important Boundary

This plan is not legal advice and does not decide redistribution readiness.

Before any beginner package is generated, a later task must verify exact
licenses, copyright notices, source-offer requirements, binary redistribution
terms, and attribution requirements against the selected package inputs.

## Notice Inventory Categories

Future clean package notice review should cover these categories:

- MeTube source license and copyright attribution.
- Fork-local modifications and source commit reference.
- Python runtime license.
- Bundled Python dependency licenses.
- yt-dlp package or executable license/notice.
- yt-dlp optional extra dependencies, including curl-cffi and Deno-related
  pieces if bundled.
- ffmpeg binary license, configuration, source/build attribution, and source
  availability requirements for the selected binary.
- Frontend dependency licenses for built Angular assets.
- Font and icon notices, including Font Awesome assets if included.
- Bootstrap, Popper, RxJS, Zone.js, and other frontend runtime notices.
- Desktop shell runtime notices if Tauri or Electron is later approved.
- WebView2 notice/distribution terms if Windows WebView2 is bundled or
  redistributed later.
- Deno, aria2, curl, tini, gosu, or other helper binary notices only if those
  pieces are included in a future desktop package.

## Current Local Candidate Facts

From local repository files:

- Root `LICENSE` contains GNU Affero General Public License Version 3 text.
- `pyproject.toml` declares Python runtime requirement `>=3.13`.
- Runtime Python dependencies declared locally:
  - `aiohttp`
  - `python-socketio`
  - `yt-dlp[default,curl-cffi,deno]`
  - `mutagen`
  - `curl-cffi`
  - `watchfiles`
- `ui/package.json` declares Angular, Bootstrap, Font Awesome, ng-bootstrap,
  ng-select, ngx-socket-io, ngx-cookie-service, RxJS, tslib, Zone.js, Popper,
  and related build tooling dependencies.
- `Dockerfile` currently installs ffmpeg and Deno-related tooling for the
  Docker image, but Y-06F does not change Docker or choose desktop binaries.

These facts identify notice inventory starting points only. Exact license
metadata must be regenerated and reviewed from lockfiles and selected bundled
artifacts in a later package task.

## Package Placement Candidates

Future generated package paths:

```text
動画保存ツール_ローカル専用/
  開発者向け/
    licenses/
      MeTube-LICENSE.txt
      third-party/
    notices/
      NOTICE.txt
      third-party-notices.txt
      ffmpeg-notice.txt
      python-runtime-notice.txt
      frontend-notices.txt
      desktop-shell-notice.txt
    manifest/
      license-notice-manifest.json
  Windows用/
    notices/
      runtime-notices.txt
      ffmpeg-notice.txt
  Mac用/
    notices/
      runtime-notices.txt
      ffmpeg-notice.txt
```

Rules:

- Beginner first-open guides should point to `開発者向け/` for license details,
  not paste long license text into the first screen.
- OS-specific runtime notices belong near the OS runtime they describe.
- Shared source and dependency notices belong under `開発者向け/`.
- Notice manifests must use package-relative paths.
- Notice manifests must not contain real cookie values, token values, secret
  values, private URLs, submitted video URLs, or private local paths.

## Candidate Notice Manifest

Future manifest path:

```text
動画保存ツール_ローカル専用/開発者向け/manifest/license-notice-manifest.json
```

Candidate fields:

```text
schema_version
package_name
source_commit
generated_at
review_status
components
component_name
component_kind
source_path
package_notice_path
license_name
license_text_path
source_url
version
target_os
target_arch
binary_build_id
requires_source_offer
requires_attribution
requires_review
review_notes
```

Rules:

- `license_name` may remain `needs_verification` until exact metadata is
  reviewed.
- `source_url` must be an official project URL or package registry URL when
  used.
- Do not include private local paths.
- Do not include downloaded media URLs or user-submitted URLs.
- Do not include credential-bearing URLs.

## Component Review Notes

### MeTube

Candidate source:

- Root `LICENSE`
- Root `README.md`
- Source commit in generated package manifest

Required future review:

- Confirm the source license and attribution requirements for the fork.
- Decide whether a source-offer or source-link note is needed for a local
  personal distribution package.
- Include fork modification and source commit information in developer material.

### yt-dlp

Candidate source:

- `pyproject.toml`
- `uv.lock`
- Runtime import/version report

Required future review:

- Confirm exact bundled yt-dlp version.
- Confirm yt-dlp license text and notice requirements from the selected
  package or executable source.
- Include notices for bundled yt-dlp dependencies and extras.
- Decide whether Deno-related support is bundled, omitted, or documented as not
  included in the beginner package.

### ffmpeg

Candidate source:

- Selected future ffmpeg binary distribution.
- Selected future binary build configuration.
- Existing FFmpeg legal reference listed in the Dockerless feasibility audit.

Required future review:

- Identify exact binary provider, version, target OS, and architecture.
- Identify whether the selected binary is LGPL-only or GPL-enabled.
- Include source/build attribution appropriate to the selected binary.
- Review source availability and patent-risk notes before distribution.
- Ensure helper binaries can be signed/notarized where needed.

### Python Runtime And Python Dependencies

Candidate source:

- `pyproject.toml`
- `uv.lock`
- Future bundled Python runtime files
- Future dependency license scanner output

Required future review:

- Confirm Python runtime license and bundled standard-library notices.
- Generate dependency license inventory from the resolved lockfile used for the
  package.
- Include runtime native library notices when applicable.
- Keep dev-only dependencies out of beginner runtime notices unless they are
  actually bundled.

### Frontend Runtime

Candidate source:

- `ui/package.json`
- `ui/pnpm-lock.yaml`
- Future built frontend artifact manifest

Required future review:

- Generate frontend dependency license inventory from the resolved lockfile.
- Include Angular, Bootstrap, Font Awesome, Popper, RxJS, Zone.js, and other
  runtime notices if built assets include or require them.
- Exclude source maps from beginner packages unless explicitly reviewed.

### Tauri Or Electron

Candidate source:

- Future desktop shell choice.
- Future desktop package lockfile or dependency manifest.
- Official references listed in the Dockerless feasibility audit.

Required future review:

- Include Tauri notices only if Tauri is actually implemented and bundled.
- Include Electron notices only if Electron is actually implemented and bundled.
- Include WebView2 distribution terms only if WebView2 runtime distribution is
  part of the Windows package plan.
- Include installer/signing tool notices only if those tools produce bundled
  runtime artifacts requiring notice.

## Beginner-Facing Notice Copy

Beginner guide pages should use a short pointer rather than legal detail:

```text
ライセンスと著作権表示は「開発者向け」フォルダに入ります。
通常の利用では読む必要はありませんが、配布物の内容を確認できます。
```

Rules:

- Do not make license review part of the normal beginner start flow.
- Do not describe command-line verification as required for beginners.
- Do not imply public redistribution readiness until a later legal/package
  review is complete.

## Dry-Run Warning Candidates

Y-06F does not change `scripts/clean_package_dry_run.py`.

A later dry-run enhancement PR should warn when these notice sources are
missing:

- Root source license candidate.
- Third-party notice plan candidate.
- Python runtime notice source candidate.
- Python dependency license inventory candidate.
- yt-dlp notice source candidate.
- ffmpeg notice source candidate.
- Frontend dependency notice source candidate.
- Desktop shell notice source candidate when Tauri/Electron is selected.
- OS-specific runtime notice paths for Windows and macOS.
- `license-notice-manifest.json` planned output.

The warning should stay non-blocking until actual package generation is
approved.

## Stop Conditions

Future package generation must remain blocked if:

- License or notice text contains real cookies, tokens, secrets, credential
  values, submitted media URLs, private URLs, or private local paths.
- The selected ffmpeg binary cannot be matched to a reviewable license/source
  attribution story.
- Runtime dependency inventory cannot be tied to the exact bundled versions.
- Any notice source requires copying from an unverified or unofficial source.
- PR #1001 files appear in the package plan.
- A generated `動画保存ツール_ローカル専用/` folder already exists before the
  generation task starts.

## Next PR Candidate

Add non-blocking missing guide-source and missing notice-source warnings to
`scripts/clean_package_dry_run.py`.

Keep the next PR dry-run only:

- No license body copying.
- No generated package folder.
- No guide generation.
- No build or package output.
- No backend/frontend/Docker/CI/package/lockfile changes.
