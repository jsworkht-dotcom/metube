# yt-dlp Notice Source

## Purpose

This file is source material for a future yt-dlp notice entry in a clean
beginner package.

It is not a generated notice file. It does not copy the full license text,
generate a notice bundle, create `動画保存ツール_ローカル専用/`, install or update
yt-dlp, or decide final redistribution readiness.

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
        yt-dlp-LICENSE.txt
    notices/
      yt-dlp-notice.txt
    manifest/
      license-notice-manifest.json
```

Rules:

- Beginner guide pages should point to `開発者向け/` for license and notice
  details.
- The first-open guide should not paste long license text into the normal
  beginner flow.
- A later approved generator may transform this source into package notice
  output.
- This source alone does not approve package generation.

## Component Summary

Component name:

```text
yt-dlp
```

Package role:

```text
Downloader and extractor library used by the backend for supported media sites.
```

Local dependency candidates:

- `pyproject.toml` declares `yt-dlp[default,curl-cffi,deno]`.
- `uv.lock` currently resolves `yt-dlp` to `2026.3.17`.
- `uv.lock` currently includes `curl-cffi` and `deno` entries used by selected
  yt-dlp extras.
- Runtime `/version` verification previously reported `yt-dlp: 2026.03.17`.

Source candidates:

- `pyproject.toml`
- `uv.lock`
- Runtime `/version` report from the selected package build
- Official project repository: `https://github.com/yt-dlp/yt-dlp`
- Official package page: `https://pypi.org/project/yt-dlp/`

License candidate from official project metadata:

```text
Unlicense
```

Review status:

```text
needs final license / notice review before package generation
```

Notes:

- The current local application uses yt-dlp through the Python dependency path,
  not by selecting a standalone yt-dlp executable for the beginner package.
- Optional extras and transitive runtime dependencies require separate notice
  review.
- If a later package switches to a standalone yt-dlp executable, that binary
  artifact must be reviewed separately from this Python dependency source.

## Beginner-Facing Short Notice

Future beginner guides may use short wording like this:

```text
このツールは、保存処理の一部で yt-dlp を使用します。
ライセンスと著作権表示は「開発者向け」フォルダで確認できます。
```

Rules:

- Keep this short.
- Do not make dependency review part of the normal first-start flow.
- Do not imply public redistribution readiness.

## Developer-Facing Notice Draft

Candidate future notice text:

```text
yt-dlp notice

この配布物は、対応サイトからの情報取得と保存処理のために yt-dlp を
使用する場合があります。

現在のローカル依存関係では、pyproject.toml に
yt-dlp[default,curl-cffi,deno] が宣言されています。実際の配布
パッケージを作成する前に、選択された lockfile、実行時バージョン、
同梱される追加依存関係、ライセンス本文、著作権表示、第三者 notice を
あらためて確認してください。

この notice 原稿は、DRM bypass、認証 bypass、制限回避、cookie/token/secret
共有、または公開ホスティングを許可するものではありません。
```

This draft is intentionally short. The full license body and transitive
dependency notices should come from reviewed source files in a later approved
notice-bundle task.

## Manifest Candidate Fields

A future `license-notice-manifest.json` entry for yt-dlp should include:

```text
component_name: yt-dlp
component_kind: python_runtime_dependency
source_path: pyproject.toml / uv.lock
package_license_path: 開発者向け/licenses/third-party/yt-dlp-LICENSE.txt
package_notice_path: 開発者向け/notices/yt-dlp-notice.txt
license_name: Unlicense
source_url: https://github.com/yt-dlp/yt-dlp
package_url: https://pypi.org/project/yt-dlp/
version: generated manifest should insert the selected package version
extras: default, curl-cffi, deno
requires_source_offer: needs_verification
requires_attribution: needs_verification
requires_review: true
```

Rules:

- Use package-relative paths in generated manifests.
- Insert the exact version during a later generation step.
- Include selected extras and transitive dependency notice links separately.
- Do not include private local paths.
- Do not include submitted media URLs.
- Do not include cookie, token, secret, credential, or private config values.

## Required Future Review

Before any generated beginner package is created:

- Confirm the exact yt-dlp version from the selected lockfile and runtime
  report.
- Confirm the exact yt-dlp license text from the selected source package,
  wheel, or other selected artifact.
- Confirm whether selected extras add bundled files or runtime dependency
  notice obligations.
- Confirm separate notices for `curl-cffi`, Deno-related pieces, and other
  transitive dependencies if they are bundled.
- Confirm whether the package uses the Python library path or a standalone
  yt-dlp executable.
- Confirm that the notice does not imply DRM bypass, authentication bypass,
  restriction circumvention, public hosting, ads, or mass-download workflows.
- Confirm that package notices do not contain private paths, submitted URLs,
  cookies, tokens, secrets, or credential values.

## Not Included In This Source

This source does not include:

- Full Unlicense text copying.
- Generated `yt-dlp-notice.txt`.
- Generated license bundle.
- Transitive dependency license inventory.
- Deno runtime notice text.
- curl-cffi notice text.
- Standalone yt-dlp executable review.
- Generated `NOTICE.txt`.
- Generated package folder.
- yt-dlp installation or update behavior.

## Source Notes

- Future package notice candidate:
  `動画保存ツール_ローカル専用/開発者向け/notices/yt-dlp-notice.txt`
- Future package license candidate:
  `動画保存ツール_ローカル専用/開発者向け/licenses/third-party/yt-dlp-LICENSE.txt`
- Source status: draft candidate only.
- This file must stay source material until a later task explicitly approves
  notice bundle generation.
