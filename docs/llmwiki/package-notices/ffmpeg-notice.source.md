# FFmpeg Notice Source

## Purpose

This file is source material for a future FFmpeg notice entry in a clean
beginner package.

It is not a generated notice file. It does not copy the full license text,
generate a notice bundle, choose a binary provider, create
`動画保存ツール_ローカル専用/`, install or update FFmpeg, or decide final
redistribution readiness.

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
        ffmpeg-LICENSE.txt
    notices/
      ffmpeg-notice.txt
    manifest/
      license-notice-manifest.json
  Windows用/
    notices/
      ffmpeg-notice.txt
    runtime/
      ffmpeg/
  Mac用/
    notices/
      ffmpeg-notice.txt
    runtime/
      ffmpeg/
```

Rules:

- Beginner guide pages should point to `開発者向け/` for license and notice
  details.
- OS-specific FFmpeg runtime notices may also live beside the packaged runtime.
- The first-open guide should not paste long license text into the normal
  beginner flow.
- A later approved generator may transform this source into package notice
  output.
- This source alone does not approve package generation.

## Component Summary

Component name:

```text
FFmpeg
```

Package role:

```text
Media processing helper used by yt-dlp postprocessors for muxing, extraction,
metadata, thumbnails, subtitles, and related local processing.
```

Local dependency candidates:

- `Dockerfile` currently installs `ffmpeg` from the Debian package path in the
  Python runtime image.
- `app/dl_formats.py` configures yt-dlp FFmpeg postprocessors for audio,
  thumbnails, and metadata.
- `app/ytdl.py` may request FFmpeg-based chapter splitting through yt-dlp.
- The future Dockerless beginner package plans platform-specific bundled
  FFmpeg runtime paths for Windows and macOS.

Source candidates:

- `Dockerfile`
- `app/dl_formats.py`
- `app/ytdl.py`
- `docs/llmwiki/dockerless-desktop-distribution-feasibility.md`
- `docs/llmwiki/desktop-package-manifest.md`
- Selected future FFmpeg binary provider, version, target OS, architecture, and
  build configuration
- Runtime `ffmpeg -version` report from the selected package build
- Official project site: `https://ffmpeg.org/`
- Official legal reference: `https://ffmpeg.org/legal.html`
- Official source repository: `https://git.ffmpeg.org/ffmpeg.git`

License candidate from official FFmpeg legal documentation:

```text
LGPL-2.1-or-later by default, with GPL-2.0-or-later implications when GPL
components are enabled; exact license depends on the selected binary build.
```

Review status:

```text
needs final license / notice review before package generation
```

Notes:

- The current Docker image installs FFmpeg through the image package manager.
- A future beginner desktop package must either bundle selected FFmpeg binaries
  or document how FFmpeg is located outside the package.
- The license and source/build obligations depend on the selected binary and
  build flags, not only on the FFmpeg project name.
- GPL-enabled, nonfree, patent-sensitive, codec-specific, or externally linked
  builds require separate review before any redistribution.
- Windows and macOS binaries must be reviewed separately because provider,
  architecture, signing, notarization, and notice requirements may differ.

## Beginner-Facing Short Notice

Future beginner guides may use short wording like this:

```text
このツールは、保存した動画や音声の処理に FFmpeg を使用する場合があります。
ライセンスと著作権表示は「開発者向け」フォルダで確認できます。
```

Rules:

- Keep this short.
- Do not make dependency review part of the normal first-start flow.
- Do not imply public redistribution readiness.
- Do not ask beginners to inspect build flags during normal use.

## Developer-Facing Notice Draft

Candidate future notice text:

```text
FFmpeg notice

この配布物は、動画や音声の変換、結合、メタデータ処理、サムネイル処理、
字幕処理などのために FFmpeg を使用する場合があります。

現在の Docker ベースの実行環境では、Dockerfile が ffmpeg をパッケージ
マネージャ経由でインストールします。将来の初心者向けデスクトップ
パッケージでは、選択された Windows / macOS 向け FFmpeg バイナリ、
バージョン、ビルド構成、ライセンス本文、著作権表示、ソース入手方法、
および第三者 codec / library notice をあらためて確認してください。

この notice 原稿は、DRM bypass、認証 bypass、制限回避、cookie/token/secret
共有、公開ホスティング、または未確認バイナリの再配布を許可するものでは
ありません。
```

This draft is intentionally short. The full license body and source/build
attribution should come from reviewed source files and selected binary metadata
in a later approved notice-bundle task.

## Manifest Candidate Fields

A future `license-notice-manifest.json` entry for FFmpeg should include:

```text
component_name: FFmpeg
component_kind: native_media_runtime
source_path: selected binary provider metadata / selected source commit or release
package_license_path: 開発者向け/licenses/third-party/ffmpeg-LICENSE.txt
package_notice_path: 開発者向け/notices/ffmpeg-notice.txt
windows_notice_path: Windows用/notices/ffmpeg-notice.txt
macos_notice_path: Mac用/notices/ffmpeg-notice.txt
license_name: generated manifest should insert the selected binary license
source_url: https://ffmpeg.org/
legal_url: https://ffmpeg.org/legal.html
source_repository: https://git.ffmpeg.org/ffmpeg.git
version: generated manifest should insert the selected binary version
target_os: generated manifest should insert Windows or macOS
target_arch: generated manifest should insert the selected architecture
binary_provider: generated manifest should insert the selected provider
binary_build_id: generated manifest should insert the selected build identifier
build_configuration: generated manifest should link to or summarize reviewed build flags
requires_source_offer: needs_verification
requires_attribution: needs_verification
requires_patent_review: needs_verification
requires_review: true
```

Rules:

- Use package-relative paths in generated manifests.
- Insert exact version, provider, target OS, target architecture, and build
  configuration during a later generation step.
- Include separate entries for Windows and macOS if the selected binaries differ.
- Do not include private local paths.
- Do not include submitted media URLs.
- Do not include cookie, token, secret, credential, or private config values.

## Required Future Review

Before any generated beginner package is created:

- Confirm the exact FFmpeg binary provider, version, target OS, target
  architecture, and build identifier.
- Confirm whether the selected binary is LGPL-only, GPL-enabled, or otherwise
  unsuitable for redistribution.
- Confirm the exact license text from the selected source package, binary
  package, or provider notice files.
- Confirm FFmpeg source availability, source/build attribution, and any source
  offer obligations for the selected distribution shape.
- Confirm selected external libraries, codecs, hardware acceleration pieces,
  and nonfree or patent-sensitive build options.
- Confirm whether separate Windows and macOS notices are required.
- Confirm signing and notarization requirements for bundled native binaries.
- Confirm that yt-dlp is configured to find the packaged FFmpeg path without
  relying on a user-installed system copy unless that behavior is documented.
- Confirm that the notice does not imply DRM bypass, authentication bypass,
  restriction circumvention, public hosting, ads, or mass-download workflows.
- Confirm that package notices do not contain private paths, submitted URLs,
  cookies, tokens, secrets, or credential values.

## Not Included In This Source

This source does not include:

- Full LGPL or GPL license text copying.
- Generated `ffmpeg-notice.txt`.
- Generated OS-specific FFmpeg notices.
- Generated license bundle.
- Selected FFmpeg binary provider approval.
- Selected FFmpeg binary download, install, or update behavior.
- Build flag verification.
- Codec, patent, or nonfree-component approval.
- Generated `NOTICE.txt`.
- Generated package folder.

## Source Notes

- Future package notice candidate:
  `動画保存ツール_ローカル専用/開発者向け/notices/ffmpeg-notice.txt`
- Future Windows runtime notice candidate:
  `動画保存ツール_ローカル専用/Windows用/notices/ffmpeg-notice.txt`
- Future macOS runtime notice candidate:
  `動画保存ツール_ローカル専用/Mac用/notices/ffmpeg-notice.txt`
- Future package license candidate:
  `動画保存ツール_ローカル専用/開発者向け/licenses/third-party/ffmpeg-LICENSE.txt`
- Source status: draft candidate only.
- This file must stay source material until a later task explicitly approves
  notice bundle generation.
