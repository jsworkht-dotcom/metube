# MeTube Notice Source

## Purpose

This file is source material for a future MeTube notice entry in a clean
beginner package.

It is not a generated notice file. It does not copy the full license text,
generate a notice bundle, create `動画保存ツール_ローカル専用/`, or decide final
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
      MeTube-LICENSE.txt
    notices/
      MeTube-notice.txt
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
MeTube
```

Package role:

```text
Local-only video saving application base.
```

Source candidates:

- Root `LICENSE`
- Root `README.md`
- Future package manifest source commit
- Fork repository: `https://github.com/jsworkht-dotcom/metube`
- Upstream project: `https://github.com/alexta69/metube`

License candidate from local repository:

```text
GNU Affero General Public License Version 3
```

Review status:

```text
needs final license / notice review before package generation
```

## Beginner-Facing Short Notice

Future beginner guides may use short wording like this:

```text
ライセンスと著作権表示は「開発者向け」フォルダに入ります。
通常の利用では読む必要はありませんが、配布物の内容を確認できます。
```

Rules:

- Keep this short.
- Do not make license review part of the normal first-start flow.
- Do not imply public redistribution readiness.

## Developer-Facing Notice Draft

Candidate future notice text:

```text
MeTube notice

この配布物は MeTube を元にしたローカル専用フォークのソースを使用します。
MeTube のライセンス候補は、リポジトリ直下の LICENSE にある
GNU Affero General Public License Version 3 です。

このフォークには、日本語 UI、readonly 更新状態表示、初心者向けガイド原稿、
ローカル専用配布計画などの変更が含まれる場合があります。

実際の配布パッケージを作成する前に、対象 commit、含めるファイル、
ライセンス本文、著作権表示、ソース参照、第三者依存関係の notice を
あらためて確認してください。
```

This draft is intentionally short. The full license body should come from the
reviewed source license file in a later approved notice-bundle task.

## Manifest Candidate Fields

A future `license-notice-manifest.json` entry for MeTube should include:

```text
component_name: MeTube
component_kind: application_source
source_path: LICENSE
package_license_path: 開発者向け/licenses/MeTube-LICENSE.txt
package_notice_path: 開発者向け/notices/MeTube-notice.txt
license_name: GNU Affero General Public License Version 3
source_url: https://github.com/alexta69/metube
fork_source_url: https://github.com/jsworkht-dotcom/metube
source_commit: generated manifest should insert the selected package commit
requires_source_offer: needs_verification
requires_attribution: needs_verification
requires_review: true
```

Rules:

- Use package-relative paths in generated manifests.
- Insert the exact source commit during a later generation step.
- Do not include private local paths.
- Do not include submitted media URLs.
- Do not include cookie, token, secret, credential, or private config values.

## Required Future Review

Before any generated beginner package is created:

- Confirm the exact MeTube license text from the selected source commit.
- Confirm copyright and attribution wording.
- Confirm whether source-link, source-offer, or modified-source notes are
  required for the selected distribution shape.
- Confirm which fork-local changes are included in the package.
- Confirm that package notices do not contain private paths, submitted URLs,
  cookies, tokens, secrets, or credential values.
- Confirm third-party notices separately for yt-dlp, ffmpeg, Python runtime,
  Python dependencies, frontend dependencies, and any future desktop shell.

## Not Included In This Source

This source does not include:

- Full AGPL license text copying.
- Third-party dependency notices.
- yt-dlp notice text.
- ffmpeg notice text.
- Python runtime notice text.
- Frontend dependency notice text.
- Tauri or Electron notice text.
- Generated `NOTICE.txt`.
- Generated license bundle.
- Generated package folder.

## Source Notes

- Future package notice candidate:
  `動画保存ツール_ローカル専用/開発者向け/notices/MeTube-notice.txt`
- Future package license candidate:
  `動画保存ツール_ローカル専用/開発者向け/licenses/MeTube-LICENSE.txt`
- Source status: draft candidate only.
- This file must stay source material until a later task explicitly approves
  notice bundle generation.
