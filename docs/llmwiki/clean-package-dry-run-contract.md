# Clean Package Dry-Run Contract

## Purpose

Y-06D defines the documentation-only dry-run contract for a future clean-package
generator.

The generator is intended to plan a beginner-friendly local-only distribution
package before any files are copied. This contract fixes the report shape,
planned output manifest, include/exclude rules, validation gates, blocked
conditions, and implementation sequence.

This document does not approve or implement a package generator, desktop shell,
installer, build script, dependency change, backend change, frontend change,
Docker change, CI change, or lockfile change.

## Scope

Allowed in Y-06D:

- Define future dry-run command candidates.
- Define JSON and Markdown dry-run report candidates.
- Define exit-code behavior.
- Define warning, error, and blocked classifications.
- Define a planned output manifest shape for the future package root.
- Define include and exclude validation rules.
- Define safety gates for secrets, caches, local state, generated folders, and
  upstream PR #1001 file leakage.
- Define examples for OK, warning, blocked, secret-like pattern found, and
  excluded path inclusion cases.
- Propose exactly one next implementation candidate.

Not allowed in Y-06D:

- Creating the actual `動画保存ツール_ローカル専用/` distribution folder.
- Creating actual beginner `.html` or `.txt` package files.
- Creating package generation scripts.
- Adding Tauri, Electron, WebView2, installer, signing, or notarization code.
- Running build, package, install, Docker pull, git pull / merge / rebase,
  update apply, or dependency update commands.
- Changing backend, frontend, yt-dlp, extractor, Docker, CI, package, or
  lockfile files.
- Reading, storing, displaying, or transforming real cookie, token, secret, or
  credential values.
- Mixing upstream PR #1001 files into fork-only work.

## Sources Checked

Repository sources checked:

- `docs/llmwiki/current-state.md`
- `docs/llmwiki/roadmap.md`
- `docs/llmwiki/handoff.md`
- `docs/llmwiki/safety-boundaries.md`
- `docs/llmwiki/dockerless-desktop-distribution-feasibility.md`
- `docs/llmwiki/desktop-sidecar-lifecycle-contract.md`
- `docs/llmwiki/desktop-package-manifest.md`
- `docs/llmwiki/beginner-guide-skeleton.md`
- `docs/llmwiki/dry-run-update-contract.md`
- `docs/llmwiki/codex-automation-policy.md`

No external references are required for this docs-only contract.

## Dry-Run Definition

Dry-run means report-only planning.

A future dry-run may:

- Read an approved manifest contract.
- Read repository file paths and metadata.
- Classify candidate source files into include, exclude, warning, or blocked
  groups.
- Build a planned output manifest.
- Produce JSON and/or Markdown reports.
- Report missing package sections, missing guides, missing notices, and safety
  blockers.
- Report whether a future generation step would be blocked.

A future dry-run must not:

- Create, copy, move, modify, delete, or package files.
- Create `動画保存ツール_ローカル専用/` or any generated distribution folder.
- Run frontend or backend builds.
- Install, update, or download dependencies.
- Pull Docker images.
- Run git pull / merge / rebase.
- Apply updates.
- Create backups or rollback targets.
- Read or print real cookie, token, secret, credential, or private config
  values.
- Treat a passing dry-run as approval to generate a package.

The dry-run result is advisory. A later explicit task must approve any generator
implementation, and another later explicit task must approve actual package
generation.

## Initial Command Contract

Y-06E implements a script-only report generator. Location:

```text
scripts/clean_package_dry_run.py
```

Initial commands:

```text
python scripts/clean_package_dry_run.py
python scripts/clean_package_dry_run.py --format text
```

Rules:

- `--format text` writes a human-readable report to stdout.
- JSON and Markdown report modes remain future candidates.
- The initial implementation does not write report files.
- `--strict` is not implemented in Y-06E.
- No command may create the package root or copy package files.

## Exit Codes

Y-06E initial script exit codes:

| Code | Status | Meaning |
| --- | --- | --- |
| `0` | `ok` | Dry-run completed and no blockers were found. |
| `1` | `blocked` | Dry-run completed and package generation must not proceed. |
| `2` | `usage_error` | CLI arguments were invalid. |

Rules:

- `blocked` takes precedence over `warning`.
- Non-blocking warning items remain review notes in Y-06E text output.
- A future actual generation command must refuse to run after exit code `1`
  unless a later task defines an explicit override policy.
- Future JSON, Markdown, strict, or CI-oriented modes may define richer warning
  or error codes only after a later task approves them.
- No override policy is approved by this document.

## Status Classification

`ok`:

- All required package sections are present in the planned manifest.
- No excluded paths are selected for inclusion.
- No forbidden filenames are selected for inclusion.
- No forbidden content patterns are found in included text-like files.
- Required local-only and safety notices are present in planned guide entries.
- No upstream PR #1001 files are selected.
- No generated distribution folder already exists in the repository root.

`warning`:

- A required beginner-facing guide entry is planned but its future source is not
  yet implemented.
- License, notice, checksum, or manifest entries are planned but unresolved.
- A large runtime file would need future owner review.
- Platform-specific package completeness is incomplete but not unsafe.
- Source maps or diagnostics are present and require explicit future review.

`blocked`:

- Any excluded path is selected for inclusion.
- Any forbidden filename is selected for inclusion.
- Any secret-like, cookie-like, token-like, or credential-like content is found
  in an included candidate.
- `.git`, `.github`, caches, local downloads, state, logs, temp files, private
  env files, personal backups, or command logs would be included.
- `docker-compose.local.yml` or `docs/local-only.md` would be included.
- A generated `動画保存ツール_ローカル専用/` folder already exists and might be
  mistaken for a clean output.
- Public hosting, ads, update apply, Docker pull, package install/update, or
  credential handling is implied by a planned entry.

`error`:

- The repository root cannot be determined safely.
- The current branch or source commit cannot be read.
- Required docs contracts are missing.
- The scan cannot read a candidate file well enough to classify it.
- Path resolution cannot prove that planned output is outside forbidden source
  locations.

## JSON Report Candidate

Candidate top-level fields:

```text
schema_version
mode
status
exit_code
checked_at
repository_root
source_commit
source_branch
package_root
planned_manifest_path
planned_outputs
include_rules
exclude_rules
validation
warnings
errors
blocked_reasons
safety_flags
next_step
```

Candidate safety flags:

```text
local_only=true
public_hosting=false
ads=false
update_apply=false
docker_pull=false
git_update=false
package_install=false
credential_handling=false
generated_folder_created=false
implementation_changes=false
```

Rules:

- Paths in reports should be repository-relative or package-relative.
- Reports must not include real personal local paths except the known repository
  root when explicitly needed for operator orientation.
- Reports must not include submitted video URLs, cookie contents, tokens,
  secrets, private environment values, or private filesystem values.
- Secret-like findings should identify the file path, line number when safe, and
  pattern family only. They must not echo the matched value.

## Markdown Report Candidate

Candidate sections:

```text
# Clean Package Dry-Run Report

## Summary
## Planned Package Root
## Planned Output Manifest
## Included Candidates
## Excluded Matches
## Validation Results
## Warnings
## Blocked Reasons
## Safety Flags
## Next Step
```

Rules:

- Markdown is for human review only.
- Markdown must remain sanitized.
- Markdown must not normalize bypassing OS warnings, site restrictions,
  authentication, DRM, or credentials.
- Markdown must clearly state that no package files were generated.

## Planned Output Manifest

The future generator should emit a planned manifest during dry-run. Candidate
future path inside a generated package:

```text
動画保存ツール_ローカル専用/開発者向け/manifest/planned-output-manifest.json
```

The dry-run may report the same structure without creating the file.

Candidate package root:

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

Candidate manifest entry fields:

```text
package_relative_path
source
kind
target_os
target_arch
include_reason
required
generated
checksum_candidate
license_notice_required
safety_notes
```

Candidate root-level entries:

- `00_最初に開いてください.html`
- `00_最初に開いてください.txt`
- `Windows用/`
- `Mac用/`
- `保存先/`
- `困ったとき/`
- `開発者向け/`
- `開発者向け/manifest/package-manifest.json`
- `開発者向け/manifest/checksums.json`
- `開発者向け/licenses/`
- `開発者向け/notices/`
- `Windows用/notices/`
- `Mac用/notices/`

The dry-run must distinguish planned future generated entries from source files
that already exist. Planned guide entries do not mean actual guide files are
created in Y-06D.

## Include Rules

Future clean packages may include these categories only after implementation is
explicitly approved:

- Desktop launcher shell.
- Backend sidecar bundle.
- Built Angular frontend assets.
- Python runtime and dependency bundle required by the sidecar.
- yt-dlp Python package and required dependencies.
- Platform-specific ffmpeg binaries.
- Optional Deno/bgutil parity assets after platform-specific review.
- User-facing `.html` beginner guide.
- User-facing `.txt` fallback guide.
- Developer docs under `開発者向け/`, including selected `docs/llmwiki/`
  planning material.
- License files and notice files.
- Package manifest, planned output manifest, and checksum files.

Source repository include candidates for the first dry-run script:

- `app/` only as a source classification input, not as copied package output.
- `ui/` only as a source classification input, not as copied package output.
- `docs/llmwiki/desktop-sidecar-lifecycle-contract.md`
- `docs/llmwiki/desktop-package-manifest.md`
- `docs/llmwiki/beginner-guide-skeleton.md`
- `docs/llmwiki/clean-package-dry-run-contract.md`
- `LICENSE`, `NOTICE`, or equivalent license/notice files when present.

Rules:

- Source code should not be copied into a beginner package unless a future
  developer-material decision explicitly approves it.
- `docs/llmwiki/` material belongs under `開発者向け/`, never as the first
  beginner entry point.
- Markdown files are developer-facing planning material, not the normal
  beginner guide.
- User-facing guide entries must be `.html` and `.txt`.

## Exclude Rules

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
- generated distribution folders
- unrelated upstream PR #1001 files:
  - `docker-compose.local.yml`
  - `docs/local-only.md`

Filename families that should default to blocked when selected for inclusion:

- names containing `cookie`
- names containing `token`
- names containing `secret`
- names containing `credential`
- names containing `password`
- names ending in `.pem`, `.key`, `.p12`, or `.pfx`
- names beginning with `.env`

## Validation Rules

Path validation:

- Resolve every candidate path under the repository root before classification.
- Reject path traversal such as `..` escaping the intended root.
- Preserve non-ASCII paths.
- Preserve spaces in paths.
- Treat symlinks, junctions, and shortcuts as requiring explicit future review.
- Block if a candidate path points into excluded directories.
- Block if `動画保存ツール_ローカル専用/` already exists in the repository root.

Filename validation:

- Block forbidden filename families listed in the exclude rules.
- Warn on ambiguous backup names such as `backup`, `old`, `copy`, `tmp`, or
  dated personal archive names.
- Warn on source maps unless a future task proves they are safe for beginner
  packages.

Content validation:

- Scan included text-like files for secret-like, cookie-like, token-like,
  credential-like, private URL, and private env assignment patterns.
- Do not scan binary payload contents into logs.
- Do not echo matched values.
- Report only path, line number when safe, and pattern family.
- Block if a forbidden content pattern is found in an included candidate.

Completeness validation:

- Warn if the planned HTML guide is missing.
- Warn if the planned TXT fallback guide is missing.
- Warn if local-only notice is missing from planned guide entries.
- Warn if Windows package section is incomplete.
- Warn if macOS package section is incomplete.
- Warn if license, notice, checksum, or manifest candidates are missing.

Large-file validation:

- Warn on large files that are not known runtime binaries.
- Block extremely large files unless a later task classifies them as required
  runtime artifacts.
- Do not include local downloads as large runtime artifacts.

Safety validation:

- Block public hosting, LAN service mode, public tunnel, reverse proxy, ads,
  monetization, update apply, Docker pull, git update, package install/update,
  credential handling, DRM bypass, authentication bypass, restriction
  circumvention, and mass-download optimization.
- Block PR #1001 leakage by detecting `docker-compose.local.yml` and
  `docs/local-only.md`.
- Block generated distribution files when this task is docs-only.

## Dry-Run Output Examples

These JSON examples remain future report-shape examples. Y-06E initial output is
human-readable text only.

### OK

```json
{
  "schema_version": "0.1",
  "mode": "dry_run",
  "status": "ok",
  "exit_code": 0,
  "package_root": "動画保存ツール_ローカル専用/",
  "planned_outputs": 13,
  "warnings": [],
  "blocked_reasons": [],
  "safety_flags": {
    "local_only": true,
    "generated_folder_created": false,
    "credential_handling": false
  },
  "next_step": "Review the dry-run report; do not generate package files yet."
}
```

### Non-Blocking Review Note

```json
{
  "schema_version": "0.1",
  "mode": "dry_run",
  "status": "ok",
  "exit_code": 0,
  "warnings": [
    {
      "kind": "missing_notice_candidate",
      "path": "開発者向け/notices/",
      "message": "Notice location is planned but no approved source has been selected."
    }
  ],
  "blocked_reasons": []
}
```

### Blocked

```json
{
  "schema_version": "0.1",
  "mode": "dry_run",
  "status": "blocked",
  "exit_code": 1,
  "warnings": [],
  "blocked_reasons": [
    {
      "kind": "generated_folder_present",
      "path": "動画保存ツール_ローカル専用/",
      "message": "A generated package root already exists and must not be mixed into docs-only work."
    }
  ]
}
```

### Secret-Like Pattern Found

```json
{
  "schema_version": "0.1",
  "mode": "dry_run",
  "status": "blocked",
  "exit_code": 1,
  "blocked_reasons": [
    {
      "kind": "forbidden_content_pattern",
      "path": "example/config-template.txt",
      "line": 12,
      "pattern_family": "secret_like_assignment",
      "message": "A secret-like assignment was found. The value is intentionally omitted."
    }
  ]
}
```

### Excluded Path Would Be Included

```json
{
  "schema_version": "0.1",
  "mode": "dry_run",
  "status": "blocked",
  "exit_code": 1,
  "blocked_reasons": [
    {
      "kind": "excluded_path_selected",
      "path": "ui/node_modules/",
      "message": "Excluded dependency cache path would be included."
    }
  ]
}
```

## Safety Gates Before Actual Generation

A future actual generation task must remain blocked until all of these are true:

- Dry-run script exists and is reviewed.
- Dry-run has succeeded repeatedly from a clean `fork/master`-based branch.
- Dry-run reports are sanitized.
- Planned output manifest is accepted.
- Include and exclude rules are explicit.
- Forbidden path and filename detection is implemented.
- Forbidden content pattern detection is implemented.
- Large file warnings are reviewed.
- HTML and TXT guide source material is approved.
- Local-only notice is present.
- Windows and macOS package sections are complete enough for the selected next
  package stage.
- License, notice, checksum, and manifest locations are reviewed.
- No generated package folder exists in the repository before generation.
- No backend/frontend/Docker/CI/package/lockfile changes are mixed into the
  generator task unless explicitly approved.
- No PR #1001 files are included.
- No cookie/token/secret handling is added.
- No update apply, Docker pull, git pull / merge / rebase, restart, pip install,
  package install, or package update is added.

## Guide And Notice Source Plans

Y-06E implemented only the report-only dry-run script:

- Script path: `scripts/clean_package_dry_run.py`
- Input: repository tree and accepted LLMwiki contracts.
- Output: sanitized human-readable text report. JSON and Markdown report modes
  remain future candidates.
- Behavior: no file generation, no copying, no build, no install, no package
  creation, no generated `動画保存ツール_ローカル専用/` folder.
- Validation: forbidden paths, forbidden filenames, forbidden content pattern
  families, package section completeness, local-only notice, and PR #1001 leakage
  checks.

Y-06F added docs-only source plans for future dry-run warning inputs:

- Guide source plan: `docs/llmwiki/beginner-guide-source-plan.md`
- License/notice plan: `docs/llmwiki/license-notice-plan.md`

These plans do not approve guide generation, license body copying, notice bundle
generation, package generation, build/package commands, Tauri/Electron
implementation, backend/frontend/Docker/CI changes, or package/lockfile
changes.

## Y-06G Warning Hardening

Y-06G adds advisory warning output to `scripts/clean_package_dry_run.py`.

Warning categories:

- Missing beginner guide source candidates.
- Missing license/notice source candidates.
- Missing local-only safety notice source candidates.
- Missing Windows/macOS section source coverage.

Rules:

- Keep the warnings non-blocking.
- Keep dry-run `Status: OK` and exit code `0` when warnings are the only
  findings.
- Preserve existing blockers for generated package folders, forbidden filename
  families, secret-like content findings, and PR #1001 leakage.
- Do not generate guide files.
- Do not copy license text.
- Do not create notice bundles.
- Do not create `動画保存ツール_ローカル専用/`.
- Do not change backend, frontend, Docker, CI, package, or lockfile files.

## Y-06H First Guide Source

Y-06H adds the first approved beginner guide source candidate:

```text
docs/llmwiki/package-guides/00-first-open.html.source.md
```

This source is intended for a future generated package path:

```text
動画保存ツール_ローカル専用/00_最初に開いてください.html
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying the planned first-open HTML
  source candidate and related local-only / Windows / macOS section source
  warnings.
- This does not create actual `.html` or `.txt` files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not approve guide generation, package generation, notice bundle
  generation, Tauri/Electron implementation, backend/frontend/Docker/CI
  changes, package/lockfile changes, or update apply.

## Y-06I First TXT Fallback Source

Y-06I adds the first-open TXT fallback source candidate:

```text
docs/llmwiki/package-guides/00-first-open.txt.source.md
```

This source is intended for a future generated package path:

```text
動画保存ツール_ローカル専用/00_最初に開いてください.txt
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying the planned first-open TXT
  source candidate and local-only TXT safety source warnings.
- This does not create actual `.html` or `.txt` files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not approve guide generation, package generation, notice bundle
  generation, Tauri/Electron implementation, backend/frontend/Docker/CI
  changes, package/lockfile changes, or update apply.

## Y-06J How-To-Use HTML Source

Y-06J adds the everyday-use HTML source candidate:

```text
docs/llmwiki/package-guides/03-how-to-use.html.source.md
```

This source is intended for a future generated package path:

```text
動画保存ツール_ローカル専用/03_使い方.html
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying the planned how-to-use HTML
  source candidate warning.
- This does not create actual `.html` or `.txt` files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not approve guide generation, package generation, notice bundle
  generation, Tauri/Electron implementation, backend/frontend/Docker/CI
  changes, package/lockfile changes, or update apply.

## Y-06K How-To-Use TXT Fallback Source

Y-06K adds the everyday-use TXT fallback source candidate:

```text
docs/llmwiki/package-guides/03-how-to-use.txt.source.md
```

This source is intended for a future generated package path:

```text
動画保存ツール_ローカル専用/03_使い方.txt
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying the planned how-to-use TXT
  source candidate warning.
- This does not create actual `.html` or `.txt` files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not approve guide generation, package generation, notice bundle
  generation, Tauri/Electron implementation, backend/frontend/Docker/CI
  changes, package/lockfile changes, or update apply.

## Y-06L Troubleshooting HTML Source

Y-06L adds the troubleshooting HTML source candidate:

```text
docs/llmwiki/package-guides/04-troubleshooting.html.source.md
```

This source is intended for a future generated package path:

```text
動画保存ツール_ローカル専用/04_困ったとき.html
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying the planned troubleshooting
  HTML source candidate warning.
- This does not create actual `.html` or `.txt` files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not approve guide generation, package generation, notice bundle
  generation, Tauri/Electron implementation, backend/frontend/Docker/CI
  changes, package/lockfile changes, or update apply.

## Y-06M Troubleshooting TXT Fallback Source

Y-06M adds the troubleshooting TXT fallback source candidate:

```text
docs/llmwiki/package-guides/04-troubleshooting.txt.source.md
```

This source is intended for a future generated package path:

```text
動画保存ツール_ローカル専用/04_困ったとき.txt
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying the planned troubleshooting TXT
  source candidate warning.
- This does not create actual `.html` or `.txt` files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not approve guide generation, package generation, notice bundle
  generation, Tauri/Electron implementation, backend/frontend/Docker/CI
  changes, package/lockfile changes, or update apply.

## Y-06N Safe-Use HTML Source

Y-06N adds the safe-use HTML source candidate:

```text
docs/llmwiki/package-guides/05-safe-use.html.source.md
```

This source is intended for a future generated package path:

```text
動画保存ツール_ローカル専用/05_安全な使い方.html
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying the planned safe-use HTML source
  candidate warning and safe-use boundary source warning.
- This does not create actual `.html` or `.txt` files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not approve guide generation, package generation, notice bundle
  generation, Tauri/Electron implementation, backend/frontend/Docker/CI
  changes, package/lockfile changes, or update apply.

## Y-06O MeTube Notice Source

Y-06O adds the first notice source candidate:

```text
docs/llmwiki/package-notices/metube-notice.source.md
```

This source is intended for future generated package paths:

```text
動画保存ツール_ローカル専用/開発者向け/notices/MeTube-notice.txt
動画保存ツール_ローカル専用/開発者向け/licenses/MeTube-LICENSE.txt
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying the planned MeTube notice
  source candidate warning.
- This does not copy full license text.
- This does not create actual notice files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not approve notice bundle generation, guide generation, package
  generation, Tauri/Electron implementation, backend/frontend/Docker/CI
  changes, package/lockfile changes, or update apply.

## Y-06P yt-dlp Notice Source

Y-06P adds the yt-dlp notice source candidate:

```text
docs/llmwiki/package-notices/yt-dlp-notice.source.md
```

This source is intended for future generated package paths:

```text
動画保存ツール_ローカル専用/開発者向け/notices/yt-dlp-notice.txt
動画保存ツール_ローカル専用/開発者向け/licenses/third-party/yt-dlp-LICENSE.txt
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying the planned yt-dlp notice
  source candidate warning.
- This does not copy full license text.
- This does not create actual notice files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not approve notice bundle generation, guide generation, package
  generation, Tauri/Electron implementation, backend/frontend/Docker/CI
  changes, package/lockfile changes, dependency install/update, or
  更新適用機能.

## Y-06Q FFmpeg Notice Source

Y-06Q adds the FFmpeg notice source candidate:

```text
docs/llmwiki/package-notices/ffmpeg-notice.source.md
```

This source is intended for future generated package paths:

```text
動画保存ツール_ローカル専用/開発者向け/notices/ffmpeg-notice.txt
動画保存ツール_ローカル専用/Windows用/notices/ffmpeg-notice.txt
動画保存ツール_ローカル専用/Mac用/notices/ffmpeg-notice.txt
動画保存ツール_ローカル専用/開発者向け/licenses/third-party/ffmpeg-LICENSE.txt
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying the planned FFmpeg notice
  source candidate warning.
- This does not copy full license text.
- This does not create actual notice files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not approve notice bundle generation, selected FFmpeg binary
  approval, guide generation, package generation, Tauri/Electron
  implementation, backend/frontend/Docker/CI changes, package/lockfile
  changes, dependency install/update, or 更新適用機能.

## Y-06R Python Runtime Notice Source

Y-06R adds the Python runtime notice source candidate:

```text
docs/llmwiki/package-notices/python-runtime-notice.source.md
```

This source is intended for future generated package paths:

```text
動画保存ツール_ローカル専用/開発者向け/notices/python-runtime-notice.txt
動画保存ツール_ローカル専用/Windows用/notices/python-runtime-notice.txt
動画保存ツール_ローカル専用/Mac用/notices/python-runtime-notice.txt
動画保存ツール_ローカル専用/開発者向け/licenses/third-party/python-runtime-LICENSE.txt
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying the planned Python runtime
  notice source candidate warning.
- This does not copy full license text.
- This does not create actual notice files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not choose, download, install, build, update, or bundle Python.
- This does not approve notice bundle generation, selected Python runtime
  approval, guide generation, package generation, PyInstaller spec files,
  Tauri/Electron implementation, backend/frontend/Docker/CI changes,
  package/lockfile changes, dependency install/update, or 更新適用機能.

## Y-06S Frontend Dependency Notice Source

Y-06S adds the frontend dependency notice source candidate:

```text
docs/llmwiki/package-notices/frontend-deps-notice.source.md
```

This source is intended for future generated package paths:

```text
動画保存ツール_ローカル専用/開発者向け/notices/frontend-deps-notice.txt
動画保存ツール_ローカル専用/開発者向け/notices/frontend-notices.txt
動画保存ツール_ローカル専用/開発者向け/licenses/third-party/frontend/
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as frontend dependency notice source material
  after the warning contract is updated in a later approved script task.
- This does not copy full license text.
- This does not create actual notice files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not generate frontend build artifacts.
- This does not change package or lock files.
- This does not change dependencies or run package manager operations.
- This does not approve notice bundle generation, selected frontend dependency
  inventory approval, guide generation, package generation, Tauri/Electron
  implementation, backend/frontend/Docker/CI changes, package/lockfile changes,
  dependency changes, or 更新適用機能.

## Y-06T Desktop Shell Notice Source

Y-06T adds the desktop shell notice source candidate:

```text
docs/llmwiki/package-notices/desktop-shell-notice.source.md
```

This source is intended for future generated package paths:

```text
動画保存ツール_ローカル専用/開発者向け/notices/desktop-shell-notice.txt
動画保存ツール_ローカル専用/Windows用/notices/desktop-shell-notice.txt
動画保存ツール_ローカル専用/Mac用/notices/desktop-shell-notice.txt
動画保存ツール_ローカル専用/開発者向け/licenses/third-party/desktop-shell/
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying the planned future
  Tauri/Electron notice source candidate warning.
- This does not copy full license text.
- This does not create actual notice files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not select, implement, build, install, package, or bundle Tauri,
  Electron, WebView2, installer output, signing output, or notarization output.
- This does not approve notice bundle generation, selected desktop shell
  approval, guide generation, package generation, backend/frontend/Docker/CI
  changes, package/lockfile changes, dependency changes, or 更新適用機能.

## Y-06U Bundled Python Dependency Inventory Source

Y-06U adds the bundled Python dependency inventory source candidate:

```text
docs/llmwiki/package-notices/bundled-python-dependency-inventory.source.md
```

This source is intended for future generated package paths:

```text
動画保存ツール_ローカル専用/開発者向け/inventory/bundled-python-dependency-inventory.json
動画保存ツール_ローカル専用/開発者向け/inventory/bundled-python-dependency-inventory.md
動画保存ツール_ローカル専用/開発者向け/notices/python-deps-notice.txt
動画保存ツール_ローカル専用/開発者向け/licenses/third-party/python-dependencies/
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying a planned future bundled
  Python dependency inventory source candidate warning.
- This does not copy full license text.
- This does not create generated dependency inventory files.
- This does not create actual notice files.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not install, update, audit, build, package, or bundle Python
  dependencies.
- This does not change package or lock files.
- This does not approve notice bundle generation, selected dependency
  inventory approval, guide generation, package generation,
  backend/frontend/Docker/CI changes, package/lockfile changes, dependency
  changes, or 更新適用機能.

## Y-06V Notice Source Index

Y-06V adds the notice source index candidate:

```text
docs/llmwiki/package-notices/notice-source-index.source.md
```

This source is intended for future package review mapping across:

```text
動画保存ツール_ローカル専用/開発者向け/notices/NOTICE.txt
動画保存ツール_ローカル専用/開発者向け/notices/third-party-notices.txt
動画保存ツール_ローカル専用/開発者向け/licenses/
動画保存ツール_ローカル専用/開発者向け/manifest/license-notice-manifest.json
動画保存ツール_ローカル専用/開発者向け/inventory/
```

Rules:

- The source remains Markdown planning/source material only.
- The dry-run may treat this file as satisfying a planned future notice source
  index candidate warning.
- This does not copy full license text.
- This does not create generated notice bundle files.
- This does not create generated license bundle files.
- This does not create generated dependency inventory files.
- This does not create generated manifest files.
- This does not create actual HTML/TXT guide output.
- This does not create `動画保存ツール_ローカル専用/`.
- This does not install, update, audit, build, package, or bundle
  dependencies.
- This does not change package or lock files.
- This does not approve notice bundle generation, license bundle generation,
  selected dependency inventory approval, guide generation, package
  generation, backend/frontend/Docker/CI changes, package/lockfile changes,
  dependency changes, or 更新適用機能.

## Y-06W Generator Contract Addendum

Y-06W adds a clean package generator contract addendum:

```text
docs/llmwiki/clean-package-generator-contract-addendum.md
```

This addendum treats the Y-06V notice source index as a future generator input
candidate for dry-run / preview review across:

```text
NOTICE.txt
LICENSES/
manifest.json
beginner guide notice sections
developer review checklist items
```

Rules:

- The addendum is docs-only and no-generation.
- The notice source index remains source material, not generated output or
  legal approval.
- Future preview reports may describe package manifest candidates, package
  output before/after diff prediction candidates, cleanup / rollback
  candidates, and human review gates.
- Preview reports must not create files, copy license text, generate notice
  bundles, generate HTML/TXT guide output, create `動画保存ツール_ローカル専用/`,
  run build/package/install commands, change dependencies, change package or
  lock files, change backend/frontend/Docker/CI files, touch PR #1001 files, or
  handle cookie/token/secret values.
- Actual generation remains a later human-reviewed task.

## Y-06X Package Manifest Preview

Y-06X adds a report-only package manifest preview to:

```text
scripts/clean_package_dry_run.py
```

The dry-run text report now includes:

```text
Package manifest preview
```

Preview fields:

- `package_name candidate`
- `package_type candidate`
- `local_only: true`
- `generated_artifacts: false`
- notice source count and source list
- guide source count and source list
- excluded path rule count and currently-present excluded path count
- future output candidates for `NOTICE.txt`, `LICENSES/`, `manifest.json`, and
  beginner guide notice section
- `human_review_required_before_generation: true`
- `legal_final: false`
- non-disclosure flags for secret/token/cookie values
- no-generation boundary note

Rules:

- The preview is text-only and report-only.
- The script does not create `manifest.json`.
- The script does not create `動画保存ツール_ローカル専用/`.
- The script does not generate notice bundles, license bundles, inventories,
  manifest files, or HTML/TXT guide output.
- Existing `Status: OK`, warnings, blockers, and exit-code behavior remain
  unchanged.
- Existing blockers must not be weakened.

## Y-06Y Package Output Diff Prediction

Y-06Y adds a report-only package output diff prediction to:

```text
scripts/clean_package_dry_run.py
```

The dry-run text report now includes:

```text
Package output diff prediction
```

Prediction fields:

- `future_package_root`
- `would_create_directories`
- `would_create_files`
- `would_copy_source_groups`
- `would_generate_future_outputs`
- excluded path rule count and currently-present excluded path count
- `no_files_generated: true`
- `human_review_required_before_generation: true`
- cleanup / rollback candidate note

Rules:

- The prediction is text-only and report-only.
- The script does not create `manifest.json`, `NOTICE.txt`, `LICENSES/`, or
  `動画保存ツール_ローカル専用/`.
- The script does not generate notice bundles, license bundles, inventories,
  manifest files, or HTML/TXT guide output.
- The prediction must not imply actual package generation approval.
- Existing `Package manifest preview`, `Status: OK`, warnings, blockers, and
  exit-code behavior remain unchanged.
- Existing blockers must not be weakened.

## Y-06Z Markdown Report Mode Design

Y-06Z adds a docs-only design for a future Markdown report mode:

```text
docs/llmwiki/clean-package-dry-run-markdown-report-mode-design.md
```

The design recommends a future selector:

```text
python scripts/clean_package_dry_run.py --format markdown
```

Rules:

- Current text output remains the default.
- Y-06Z does not implement Markdown output.
- Y-06Z does not change `scripts/clean_package_dry_run.py`.
- Y-06Z does not change `scripts/check_repo_safety.py`.
- A future Markdown mode should write to stdout only in its first
  implementation.
- A future Markdown mode should preserve existing `Status: OK`,
  `Status: BLOCKED`, warnings, blockers, and exit-code behavior.
- A future Markdown mode should not create package files or generated
  artifacts.

Required future Markdown sections:

- Summary
- Status
- Risk Classification
- Package Manifest Preview
- Package Output Diff Prediction
- Notice / Guide Source Coverage
- Excluded Paths Summary
- Blockers
- Warnings
- Human Review Checklist
- No-Generation Boundary

## Y-07A JSON Report Mode Design

Y-07A adds a docs-only design for a future JSON report mode:

```text
docs/llmwiki/clean-package-dry-run-json-report-mode-design.md
```

The design recommends a future selector:

```text
python scripts/clean_package_dry_run.py --format json
```

Rules:

- Current text output remains the default.
- Y-07A does not implement JSON output.
- Y-07A does not change `scripts/clean_package_dry_run.py`.
- Y-07A does not change `scripts/check_repo_safety.py`.
- A future JSON mode should write one valid JSON object to stdout only in its
  first implementation.
- A future JSON mode should preserve existing `Status: OK`,
  `Status: BLOCKED`, warnings, blockers, and exit-code behavior.
- A future JSON mode should not create package files, generated artifacts, or
  report files.
- Repository-diff risk classification should remain owned by
  `scripts/check_repo_safety.py` unless a later wrapper task explicitly
  combines reports.

Required future JSON top-level keys:

- schema_version
- report_kind
- report_format
- mode
- status
- exit_code
- repository
- package
- planned_entries
- package_manifest_preview
- package_output_diff_prediction
- excluded_paths
- checks
- warnings
- blocked_reasons
- safety_flags
- risk_classification
- no_generation_boundary
- next_step

## Y-CHECK-01 Repository Safety Gate Relationship

Y-CHECK-01 is documented in:

```text
docs/llmwiki/safety-gate-checker-design.md
```

Relationship:

- The clean-package dry-run remains package-focused and plans future package
  output without creating files.
- The Y-CHECK-01 gate is repository-diff-focused and checks whether a task stays
  inside its approved scope.
- Both designs share forbidden path, secret-like pattern, generated package
  folder, PR #1001 leakage, and package guide / notice completeness concepts.
- Package guide / notice completeness should remain warning-only in the
  repository gate unless a task attempts actual package generation.

Y-CHECK-01 does not implement a checker, add scripts, change CI, generate a
package, create `動画保存ツール_ローカル専用/`, change backend/frontend/Docker/CI
files, change package/lockfile files, implement update execution, or handle
cookie/token/secret values.

## Codex Automation Policy Relationship

The Codex automation policy is documented in:

```text
docs/llmwiki/codex-automation-policy.md
```

Relationship:

- Low-risk and medium-risk work may use auto PR and auto merge only when the
  current task scope and required safety gates pass.
- High-low work may use auto PR and auto merge only when it remains docs-only,
  report-only, or dry-run-only.
- High-low auto merge requires both `scripts/check_repo_safety.py` and
  `scripts/clean_package_dry_run.py` to return OK.
- The dry-run is especially important for package-adjacent high-low work such
  as manifest preview design, notice bundle dry-run design, generated output
  preview design, desktop shell scaffold planning, backup/rollback design docs,
  package preflight checks, and output diff prediction reports.
- Actual package generation, generated distribution folders, ZIP/package/
  installer creation, and dependency install/update are prohibited.
- Docker pull/build is prohibited for high-low auto merge.
- Package/lockfile changes, backend download or queue logic changes, yt-dlp
  logic changes, cookie/token/secret handling, public hosting, ads, and
  更新適用機能 remain prohibited.

## Next Implementation Candidate

Review the existing report-only safety checker before low- or medium-risk fork
PRs, then select the next source-only package notice gap explicitly.

The next package-material candidate should be selected explicitly. Good next
candidates are a future report-only JSON implementation or a future report-only
Markdown implementation if explicitly approved.

Actual clean-package generation should wait until after repeated successful
dry-run reports and a later explicit generation task.
