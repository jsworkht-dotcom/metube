# Desktop Shell Notice Source

## Purpose

This file is source material for a future desktop shell notice entry in a clean
beginner package.

It is not a generated notice file. It does not copy full license texts,
generate a notice bundle, create `動画保存ツール_ローカル専用/`, create HTML or
TXT package guide output, implement Tauri, implement Electron, implement
WebView2, run a build, install dependencies, change package or lock files, or
decide final redistribution readiness.

This source is not final legal advice.

## Future Package Role

Future user-facing package:

```text
動画保存ツール_ローカル専用/
```

Future notice / license placement candidates:

```text
動画保存ツール_ローカル専用/
  開発者向け/
    licenses/
      third-party/
        desktop-shell/
    notices/
      desktop-shell-notice.txt
      third-party-notices.txt
    manifest/
      license-notice-manifest.json
  Windows用/
    notices/
      desktop-shell-notice.txt
      runtime-notices.txt
  Mac用/
    notices/
      desktop-shell-notice.txt
      runtime-notices.txt
```

Rules:

- Beginner guide pages should point to `開発者向け/` for license and notice
  details.
- OS-specific runtime notices may live beside the Windows or macOS launcher
  pieces if a later package task selects platform-specific shell artifacts.
- A later approved generator may transform this source into package notice
  output.
- This source alone does not select a desktop shell or approve package
  generation.

## Placement Candidates

Shared developer-facing notice candidate:

```text
動画保存ツール_ローカル専用/開発者向け/notices/desktop-shell-notice.txt
```

OS-specific notice candidates:

```text
動画保存ツール_ローカル専用/Windows用/notices/desktop-shell-notice.txt
動画保存ツール_ローカル専用/Mac用/notices/desktop-shell-notice.txt
```

License directory candidate:

```text
動画保存ツール_ローカル専用/開発者向け/licenses/third-party/desktop-shell/
```

Placement notes:

- Use the shared developer notice for cross-platform shell review notes.
- Add OS-specific notices only for runtime pieces actually included in each
  future package.
- Keep WebView2 runtime distribution notes Windows-specific.
- Keep signing, notarization, installer, and bundler tool notices separate
  unless their output or runtime payload is bundled.

## Desktop Shell Candidates

Current selection status:

```text
No desktop shell has been selected, implemented, bundled, or approved.
```

Candidate families for future review:

| Candidate | Initial role | Future review need |
| --- | --- | --- |
| Tauri | desktop wrapper candidate | Review Rust crates, JavaScript packages, platform webview behavior, sidecar handling, updater exclusion, installer output, signing, and notices only if selected. |
| Electron | fallback desktop wrapper candidate | Review Electron, bundled Chromium / Node.js runtime pieces, npm dependency graph, package size, security settings, installer output, signing, and notices only if selected. |
| WebView2 direct host | Windows-only host candidate | Review Microsoft WebView2 Runtime distribution mode, loader/runtime files, installer behavior, fixed vs evergreen runtime choices, and Windows-specific notices only if selected. |
| Native launcher plus browser tab | limited fallback candidate | Review whether a native launcher without embedded webview can meet beginner UX, sidecar lifecycle, local-only binding, and notice requirements. |

Rules:

- Do not record any candidate as adopted until a later implementation task
  selects it explicitly.
- Do not include Tauri notices unless Tauri is actually implemented and bundled.
- Do not include Electron notices unless Electron is actually implemented and
  bundled.
- Do not include WebView2 redistribution notices unless WebView2 runtime files,
  installers, or loader pieces are actually part of the Windows package plan.

## Candidate-Specific Review Notes

### Tauri

Official reference candidates checked for this source:

- `https://tauri.app/reference/webview-versions/`
- `https://tauri.app/reference/acl/core-permissions/`

Review notes:

- Tauri's Windows webview story should be rechecked against current official
  docs before implementation or packaging.
- The selected Tauri major version, Rust crate graph, JavaScript package graph,
  generated installer payload, shell permissions, sidecar permissions, and
  updater configuration need separate review.
- Any future updater support should remain outside beginner package scope until
  explicitly approved as 更新適用機能.
- Tauri can remain a candidate without creating Rust files, Tauri config, npm
  packages, lockfile entries, installer output, or notice output in this task.

### Electron

Official reference candidates checked for this source:

- `https://www.electronjs.org/`
- `https://www.electronjs.org/docs/latest/tutorial/electron-timelines`

Review notes:

- Electron's bundled Chromium and Node.js runtime pieces should be reviewed as
  package contents if Electron is selected.
- The selected Electron version, packaging tool, npm dependency graph,
  security settings, preload / IPC boundaries, installer payload, and notices
  need separate review.
- Electron can remain a fallback candidate without creating Electron source,
  package entries, lockfile entries, build output, installer output, or notice
  output in this task.

### WebView2

Official reference candidates checked for this source:

- `https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution`

Review notes:

- WebView2 is a Windows-specific candidate and is not a cross-platform shell by
  itself.
- A future Windows package must decide whether it relies on an installed
  Evergreen runtime, includes an installer, or ships a fixed runtime.
- Fixed-runtime choices may change package size, update responsibility,
  security review, permissions, and notice requirements.
- WebView2 can remain a candidate without adding WebView2 loader files,
  runtime files, installers, project files, package output, or notice output in
  this task.

## Beginner-Facing Short Notice

Future beginner guides may use short wording like this:

```text
このツールは、将来のデスクトップ版で Tauri、Electron、WebView2 などの
デスクトップ表示部品を使用する場合があります。
実際に含まれる部品のライセンスと著作権表示は「開発者向け」フォルダで
確認できます。
```

Rules:

- Keep this short.
- Do not make desktop shell review part of the normal first-start flow.
- Do not imply that Tauri, Electron, or WebView2 has already been selected.
- Do not imply public redistribution readiness.
- Do not ask beginners to run build, package, installer, or dependency
  commands during normal use.

## Developer-Facing Notice Draft

Candidate future notice text:

```text
Desktop shell notice

この配布物は、将来のデスクトップ版でローカル画面を表示し、バックエンド
sidecar を起動・停止するために、Tauri、Electron、WebView2、または別の
デスクトップ shell を使用する場合があります。

現在のリポジトリでは、実際の desktop shell、runtime、installer、
WebView、sidecar bundle、署名・notarization tool、package artifact、
および notice 一式はまだ確定していません。

実際の配布パッケージを作成する前に、選択された desktop shell、
target OS、target architecture、runtime files、installer payload、
license text、copyright notice、third-party notice、source URL、
WebView/runtime distribution terms、および security settings を
あらためて確認してください。

この notice 原稿は、Web 公開、広告収益化、外部ユーザー向けサービス化、
cookie/token/secret 共有、DRM bypass、認証 bypass、または制限回避を
許可するものではありません。
```

This draft is intentionally short. Full license bodies, runtime notices,
installer notices, and dependency notices should come from reviewed selected
artifacts in a later approved notice-bundle task.

## Manifest Candidate Fields

A future `license-notice-manifest.json` entry for the desktop shell should
include one entry per selected shell component, runtime component, installer
component, and webview/runtime payload actually included.

Candidate aggregate entry:

```text
component_name: desktop shell
component_kind: desktop_shell_candidate
selected_shell: needs_verification
source_path: selected desktop shell manifest / lockfile / build artifact manifest
package_notice_path: 開発者向け/notices/desktop-shell-notice.txt
windows_notice_path: Windows用/notices/desktop-shell-notice.txt
macos_notice_path: Mac用/notices/desktop-shell-notice.txt
package_license_dir: 開発者向け/licenses/third-party/desktop-shell/
license_name: needs_verification
source_url: needs_verification
package_url: needs_verification
version: needs_verification
target_os: windows / macos / needs_verification
target_arch: x64 / arm64 / needs_verification
runtime_payload: none_selected
webview_runtime_distribution: none_selected
installer_payload: none_selected
signing_or_notarization_tooling: needs_verification
dependency_inventory_path: generated manifest should insert reviewed inventory path
requires_attribution: needs_verification
requires_license_text: needs_verification
requires_source_offer: needs_verification
requires_review: true
```

Rules:

- Use package-relative paths in generated manifests.
- Insert exact versions during a later generation step.
- Include component-specific entries rather than only one aggregate entry when
  the final notice bundle is generated.
- Separate shell framework notices from backend sidecar, Python runtime,
  frontend dependency, ffmpeg, yt-dlp, and installer-tool notices.
- Do not include private local paths.
- Do not include submitted media URLs.
- Do not include cookie, token, secret, credential, or private config values.

## Review Checklist

Before any generated beginner package is created:

- Confirm whether a desktop shell is selected at all.
- Confirm the selected shell family, exact version, package manager metadata,
  lockfile state, source URL, license text, notice text, and copyright
  attribution.
- Confirm exact target OS and architecture combinations.
- Confirm whether Tauri, Electron, WebView2, or another shell is actually
  present in the package.
- Confirm which runtime files, webview files, loader files, installer files,
  signing outputs, notarization outputs, helper binaries, or sidecar bridge
  files are included.
- Confirm the dependency graph for selected shell code and packaging tools.
- Confirm whether any shell updater feature exists in the selected framework
  and that it remains disabled or out of scope unless a later task approves
  更新適用機能.
- Confirm local-only binding, sidecar lifecycle, close behavior, and user data
  path defaults separately from license notices.
- Confirm that no package manager cache, source tree, local command log,
  private file, generated distribution folder, or unrelated PR #1001 file is
  included.
- Confirm that the notice does not imply public hosting, ads, external-user
  service operation, DRM bypass, authentication bypass, restriction
  circumvention, or mass-download workflows.
- Confirm that package notices do not contain private paths, submitted URLs,
  cookies, tokens, secrets, or credential values.

## Future Generated Notice Bundle Requirements

A later approved notice-bundle task should:

- Read the exact selected desktop shell manifest, lockfile, and build artifact
  manifest.
- Produce a package-relative dependency inventory for selected shell runtime
  pieces.
- Produce package-specific notice entries for selected framework, runtime,
  webview, installer, and helper pieces.
- Preserve candidate-only status for unselected desktop shells.
- Include full license text only from reviewed package artifacts, official
  project files, official runtime terms, or package metadata.
- Record unresolved items as `needs_verification` rather than guessing.
- Keep reports sanitized and free of private paths, submitted URLs, cookies,
  tokens, secrets, and credential values.
- Avoid creating package files until a later package generation task is
  explicitly approved.

## Not Included / Legal-Not-Final Boundary

This source does not include:

- Final legal advice.
- Full license text copying.
- Generated `desktop-shell-notice.txt`.
- Generated `third-party-notices.txt`.
- Generated license bundle.
- Generated desktop shell dependency inventory.
- Generated desktop build artifact manifest.
- Tauri implementation.
- Electron implementation.
- WebView2 implementation.
- Installer implementation.
- Signing or notarization implementation.
- HTML or TXT package guide output.
- Generated package folder.
- Dependency changes or package manager operations.
- Backend, frontend, Docker, CI, package, or lockfile changes.
- Approval for public redistribution readiness.

## Source Notes

- Future package notice candidate:
  `動画保存ツール_ローカル専用/開発者向け/notices/desktop-shell-notice.txt`
- Future Windows notice candidate:
  `動画保存ツール_ローカル専用/Windows用/notices/desktop-shell-notice.txt`
- Future macOS notice candidate:
  `動画保存ツール_ローカル専用/Mac用/notices/desktop-shell-notice.txt`
- Future package license directory candidate:
  `動画保存ツール_ローカル専用/開発者向け/licenses/third-party/desktop-shell/`
- Source status: draft candidate only.
- This file must stay source material until a later task explicitly approves
  notice bundle generation.
