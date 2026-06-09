# Notice Source Index Source

## Purpose

This file is source material for a future notice / license / dependency
inventory index in a clean beginner package.

It is not a generated notice bundle, generated license bundle, generated
dependency inventory, generated manifest, beginner guide output, package
folder, build artifact, or legal conclusion.

This source is hand-reviewed planning material. It is not automatically
generated output.

## Future Package Role

Future user-facing package:

```text
動画保存ツール_ローカル専用/
```

Future package output categories this index may help review:

```text
動画保存ツール_ローカル専用/
  00_最初に開いてください.html
  00_最初に開いてください.txt
  開発者向け/
    licenses/
      MeTube-LICENSE.txt
      third-party/
    notices/
      NOTICE.txt
      third-party-notices.txt
      MeTube-notice.txt
      yt-dlp-notice.txt
      ffmpeg-notice.txt
      python-runtime-notice.txt
      python-deps-notice.txt
      frontend-deps-notice.txt
      frontend-notices.txt
      desktop-shell-notice.txt
    inventory/
      bundled-python-dependency-inventory.json
      bundled-python-dependency-inventory.md
    manifest/
      license-notice-manifest.json
  Windows用/
    notices/
      runtime-notices.txt
      ffmpeg-notice.txt
      python-runtime-notice.txt
      desktop-shell-notice.txt
  Mac用/
    notices/
      runtime-notices.txt
      ffmpeg-notice.txt
      python-runtime-notice.txt
      desktop-shell-notice.txt
```

Rules:

- Beginner guide pages should contain only short notice pointers.
- Developer-facing folders should carry detailed notice, license, manifest, and
  inventory output after a later approved generator task.
- OS-specific notices should describe only runtime pieces actually included in
  that OS package.
- This index alone does not approve package generation.

## Read-Only Source Files Inspected

The following files were checked read-only for this source index:

- `docs/llmwiki/package-notices/metube-notice.source.md`
- `docs/llmwiki/package-notices/yt-dlp-notice.source.md`
- `docs/llmwiki/package-notices/ffmpeg-notice.source.md`
- `docs/llmwiki/package-notices/python-runtime-notice.source.md`
- `docs/llmwiki/package-notices/frontend-deps-notice.source.md`
- `docs/llmwiki/package-notices/desktop-shell-notice.source.md`
- `docs/llmwiki/package-notices/bundled-python-dependency-inventory.source.md`

No notice bundle, license bundle, package folder, HTML/TXT guide output,
dependency install, dependency update, lockfile update, build, package, or
distribution artifact was generated for this index.

## Source File Inventory

| Source file | Future role | Future output candidates | Review status |
| --- | --- | --- | --- |
| `metube-notice.source.md` | MeTube / fork source notice | `開発者向け/notices/MeTube-notice.txt`, `開発者向け/licenses/MeTube-LICENSE.txt`, manifest component entry | source draft; legal-not-final; candidate only; package-time review required |
| `yt-dlp-notice.source.md` | yt-dlp runtime dependency notice | `開発者向け/notices/yt-dlp-notice.txt`, `開発者向け/licenses/third-party/yt-dlp-LICENSE.txt`, manifest component entry | source draft; legal-not-final; candidate only; package-time review required |
| `ffmpeg-notice.source.md` | FFmpeg native runtime notice | `開発者向け/notices/ffmpeg-notice.txt`, `Windows用/notices/ffmpeg-notice.txt`, `Mac用/notices/ffmpeg-notice.txt`, `開発者向け/licenses/third-party/ffmpeg-LICENSE.txt`, manifest component entry | source draft; legal-not-final; candidate only; package-time review required |
| `python-runtime-notice.source.md` | CPython / Python runtime notice | `開発者向け/notices/python-runtime-notice.txt`, `Windows用/notices/python-runtime-notice.txt`, `Mac用/notices/python-runtime-notice.txt`, `開発者向け/licenses/third-party/python-runtime-LICENSE.txt`, manifest component entry | source draft; legal-not-final; candidate only; package-time review required |
| `frontend-deps-notice.source.md` | Built frontend dependency notice | `開発者向け/notices/frontend-deps-notice.txt`, `開発者向け/notices/frontend-notices.txt`, `開発者向け/licenses/third-party/frontend/`, manifest component entries | source draft; legal-not-final; candidate only; package-time review required |
| `desktop-shell-notice.source.md` | Future desktop shell notice | `開発者向け/notices/desktop-shell-notice.txt`, `Windows用/notices/desktop-shell-notice.txt`, `Mac用/notices/desktop-shell-notice.txt`, `開発者向け/licenses/third-party/desktop-shell/`, manifest component entries | source draft; legal-not-final; candidate only; package-time review required |
| `bundled-python-dependency-inventory.source.md` | Bundled Python/backend dependency inventory | `開発者向け/inventory/bundled-python-dependency-inventory.json`, `開発者向け/inventory/bundled-python-dependency-inventory.md`, `開発者向け/notices/python-deps-notice.txt`, `開発者向け/licenses/third-party/python-dependencies/`, manifest component entries | source draft; legal-not-final; candidate only; package-time review required |

## Future Output Mapping

### NOTICE.txt Candidates

Candidate aggregate notice outputs:

```text
開発者向け/notices/NOTICE.txt
開発者向け/notices/third-party-notices.txt
Windows用/notices/runtime-notices.txt
Mac用/notices/runtime-notices.txt
```

Mapping rules:

- `NOTICE.txt` may summarize MeTube source, local fork notes, and pointers to
  detailed third-party notices.
- `third-party-notices.txt` may aggregate or link to yt-dlp, FFmpeg, Python
  runtime, Python dependency, frontend dependency, and desktop shell notices.
- OS-specific `runtime-notices.txt` should include only runtime pieces present
  in that OS package.
- Aggregate notices must preserve component-level manifest links so individual
  license and source records are not lost.

### LICENSES/ Candidates

Candidate license output roots:

```text
開発者向け/licenses/
開発者向け/licenses/third-party/
```

Candidate subpaths:

```text
開発者向け/licenses/MeTube-LICENSE.txt
開発者向け/licenses/third-party/yt-dlp-LICENSE.txt
開発者向け/licenses/third-party/ffmpeg-LICENSE.txt
開発者向け/licenses/third-party/python-runtime-LICENSE.txt
開発者向け/licenses/third-party/python-dependencies/
開発者向け/licenses/third-party/frontend/
開発者向け/licenses/third-party/desktop-shell/
```

Rules:

- Do not copy full license bodies until a later approved notice-bundle task
  selects exact artifacts and verifies license text.
- Keep generated paths package-relative.
- Preserve OS-specific license notes where Windows and macOS bundled artifacts
  differ.

### manifest.json Candidates

Candidate manifest outputs:

```text
開発者向け/manifest/license-notice-manifest.json
開発者向け/manifest/planned-output-manifest.json
```

Candidate manifest fields:

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
source_url
package_url
version
target_os
target_arch
package_notice_path
package_license_path
inventory_path
license_name
license_expression
requires_source_offer
requires_attribution
requires_review
review_notes
```

Rules:

- `review_status` should remain non-final until package-time review completes.
- Manifest entries must not include private local paths, submitted media URLs,
  cookies, tokens, secrets, credentials, or private config values.
- The manifest should cross-reference generated notices, licenses, inventories,
  and source files.

### Beginner Guide Notice Section Candidates

Candidate beginner-facing notice sections:

```text
00_最初に開いてください.html
00_最初に開いてください.txt
困ったとき/
開発者向け/README.md
```

Beginner-facing text should stay short:

```text
ライセンスと著作権表示は「開発者向け」フォルダに入ります。
通常の利用では読む必要はありませんが、配布物の内容を確認できます。
```

Rules:

- Do not paste long license text into beginner guides.
- Do not make dependency review part of normal first-start flow.
- Do not imply public redistribution readiness.
- Keep local-only and personal-use boundaries separate from legal notice
  details, while preserving both in guide source material.

### Developer Review Checklist Candidates

Future developer-facing review output should cover:

- selected source commit and fork-local modification notes
- exact dependency lockfiles and package artifacts used
- exact bundled runtime files for Windows and macOS
- exact FFmpeg binary provider, version, build configuration, and source access
- exact Python runtime artifact, standard-library notices, and bundler pieces
- exact Python dependency graph and native extension / certificate data review
- exact frontend build artifact, source map decision, fonts, icons, and style
  assets
- exact desktop shell choice, runtime payload, WebView/runtime terms,
  installer payload, signing, and notarization notes
- package-relative notice, license, inventory, and manifest paths
- no-private-data review for private paths, submitted URLs, cookies, tokens,
  secrets, credentials, and private config values

## Review Status Vocabulary

Use these status labels consistently in future review material:

| Status | Meaning |
| --- | --- |
| `source draft` | Hand-authored source material exists for future review. |
| `legal-not-final` | The text is not legal advice and does not determine redistribution readiness. |
| `candidate only` | Component, output path, license, or source URL is a candidate until package-time selection. |
| `package-time review required` | A later approved package task must verify exact artifacts, versions, license text, notices, and generated outputs. |

## Unresolved Questions

- Which exact source commit will be used for the clean beginner package?
- Which OS-specific runtime artifacts will be bundled for Windows and macOS?
- Will FFmpeg be bundled, externally located, or omitted from a particular
  package variant?
- Which Python runtime bundling approach will be selected?
- Which Python dependency wheels, source distributions, native extensions,
  certificate bundles, helper binaries, or optional extras will be included?
- Which frontend assets, source maps, fonts, icons, CSS, and JavaScript chunks
  will be included?
- Which desktop shell, if any, will be selected?
- Will any selected component require source-offer, attribution, NOTICE file,
  or OS-specific license handling?
- How will generated manifests preserve package-relative paths without private
  local paths?
- Which guide files should point to detailed developer material without making
  legal review part of normal beginner use?

## Future Generated Notice Bundle Requirements

A later approved generator should:

- Read source materials from reviewed paths, not from generated package output.
- Generate or copy only after exact package inputs are selected.
- Preserve component-level entries for MeTube, yt-dlp, FFmpeg, Python runtime,
  bundled Python dependencies, frontend dependencies, and desktop shell pieces.
- Emit aggregate notices only when component notice links remain traceable.
- Emit license files from verified source artifacts only.
- Emit dependency inventories from exact lockfiles and bundled artifacts only.
- Emit OS-specific runtime notices when Windows and macOS package contents
  differ.
- Emit manifest entries with package-relative paths and sanitized metadata.
- Block generation if required license text, notice text, source URL, version,
  target OS/architecture, or review status is missing.
- Block generation if private paths, submitted URLs, cookies, tokens, secrets,
  credentials, or private config values would be included.

## Not Included / No Generation Boundary

This source index does not include:

- final legal advice
- final redistribution approval
- actual notice bundle output
- actual license bundle output
- generated dependency inventory output
- generated manifest output
- generated beginner guide HTML or TXT output
- generated package folder
- backend, frontend, Docker, CI, package, or lockfile changes
- build, package, install, dependency install, dependency update, or lock update
  commands
- cookie, token, secret, credential, or private URL handling
- public hosting, advertising, monetization, or external-user service support
- PR #1001 file changes
- 更新適用機能
