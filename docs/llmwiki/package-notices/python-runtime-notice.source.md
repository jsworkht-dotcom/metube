# Python Runtime Notice Source

## Purpose

This file is source material for a future Python runtime notice entry in a
clean beginner package.

It is not a generated notice file. It does not copy the full Python license
text, generate a notice bundle, choose a runtime artifact, create
`動画保存ツール_ローカル専用/`, install or update Python, build a package, or
decide final redistribution readiness.

This source is not final legal advice.

## Future Package Role

Future user-facing package:

```text
動画保存ツール_ローカル専用/
```

Future runtime / notice / license placement candidates:

```text
動画保存ツール_ローカル専用/
  開発者向け/
    licenses/
      third-party/
        python-runtime-LICENSE.txt
    notices/
      python-runtime-notice.txt
    manifest/
      license-notice-manifest.json
  Windows用/
    runtime/
      backend/
    notices/
      python-runtime-notice.txt
      runtime-notices.txt
  Mac用/
    runtime/
      backend/
    notices/
      python-runtime-notice.txt
      runtime-notices.txt
```

Rules:

- Beginner guide pages should point to `開発者向け/` for license and notice
  details.
- OS-specific runtime notices may also live beside the packaged backend
  runtime.
- The first-open guide should not paste long license text into the normal
  beginner flow.
- A later approved generator may transform this source into package notice
  output.
- This source alone does not approve package generation.

## Python / Runtime Candidate

Component name:

```text
CPython / Python runtime
```

Package role:

```text
Interpreter and standard-library runtime used by the packaged backend sidecar
if a future beginner package bundles Python instead of requiring a user
installation.
```

Local candidate facts:

- `pyproject.toml` declares `requires-python = ">=3.13"`.
- `Dockerfile` currently uses `python:3.13-slim` for the Docker runtime image.
- Existing Dockerless package planning expects the beginner package not to
  require user-installed Python.
- Existing Dockerless package planning lists PyInstaller one-folder output, or
  another Python runtime bundle, as a future backend sidecar candidate.

Current selection status:

```text
No exact Windows or macOS Python runtime artifact has been selected.
```

Candidate runtime family:

```text
CPython 3.13.x or newer, selected later to match the packaged backend and the
approved desktop sidecar build method.
```

Upstream / source URL candidates:

- Official Python site: `https://www.python.org/`
- Official Python license documentation:
  `https://docs.python.org/3/license.html`
- Official Python source releases:
  `https://www.python.org/downloads/source/`
- CPython source repository candidate:
  `https://github.com/python/cpython`

License candidate from official Python documentation:

```text
Python Software Foundation License Version 2, with historical license-stack
and incorporated-software notice review required for the exact selected
runtime.
```

Review status:

```text
needs final license / notice review before package generation
```

Notes:

- The current Docker image runtime does not decide the future desktop package
  runtime.
- A future beginner package should not ask the user to install Python manually
  for the normal path.
- If PyInstaller or another bundler is used, the bundled interpreter,
  standard-library files, native libraries, and bootloader/runtime pieces must
  be reviewed together.
- Python dependency notices are separate from this runtime notice and require a
  later inventory from the exact resolved package inputs.

## Beginner-Facing Short Notice

Future beginner guides may use short wording like this:

```text
このツールは、内部の動作に Python 実行環境を同梱する場合があります。
ライセンスと著作権表示は「開発者向け」フォルダで確認できます。
```

Rules:

- Keep this short.
- Do not make runtime review part of the normal first-start flow.
- Do not imply public redistribution readiness.
- Do not ask beginners to install Python, run Python commands, or inspect
  runtime files during normal use.

## Developer-Facing Notice Draft

Candidate future notice text:

```text
Python runtime notice

この配布物は、バックエンドを動かすために Python 実行環境を同梱する
場合があります。

現在のリポジトリでは、pyproject.toml が Python >=3.13 を要求し、
Dockerfile は Docker 実行環境として python:3.13-slim を使用しています。
ただし、初心者向けデスクトップ配布物に同梱する Windows / macOS 向け
Python 実行環境、正確なバージョン、配布元、bundler、標準ライブラリ、
ネイティブライブラリ、および notice 一式はまだ確定していません。

実際の配布パッケージを作成する前に、選択された Python runtime artifact、
ライセンス本文、著作権表示、incorporated software notice、標準ライブラリ、
ネイティブライブラリ、PyInstaller 等の sidecar packaging 要件、および
Python dependency notice をあらためて確認してください。

この notice 原稿は、Web 公開、広告収益化、外部ユーザー向けサービス化、
cookie/token/secret 共有、DRM bypass、認証 bypass、または制限回避を
許可するものではありません。
```

This draft is intentionally short. The full license body, incorporated-software
notices, and runtime dependency notices should come from reviewed source files
and selected runtime metadata in a later approved notice-bundle task.

## Manifest Candidate Fields

A future `license-notice-manifest.json` entry for the Python runtime should
include:

```text
component_name: CPython / Python runtime
component_kind: python_interpreter_runtime
source_path: selected runtime artifact metadata / pyproject.toml / Dockerfile
package_license_path: 開発者向け/licenses/third-party/python-runtime-LICENSE.txt
package_notice_path: 開発者向け/notices/python-runtime-notice.txt
windows_notice_path: Windows用/notices/python-runtime-notice.txt
macos_notice_path: Mac用/notices/python-runtime-notice.txt
license_name: Python Software Foundation License Version 2 / needs_verification
license_url: https://docs.python.org/3/license.html
source_url: https://www.python.org/
source_release_url: https://www.python.org/downloads/source/
source_repository: https://github.com/python/cpython
version: generated manifest should insert the selected runtime version
target_os: generated manifest should insert Windows or macOS
target_arch: generated manifest should insert the selected architecture
runtime_provider: generated manifest should insert the selected provider
binary_build_id: generated manifest should insert the selected build identifier
packaging_method: generated manifest should insert PyInstaller or selected method
stdlib_included: needs_verification
incorporated_software_notices_path: needs_verification
native_library_notices_path: needs_verification
python_dependency_notice_path: separate future inventory
requires_source_offer: needs_verification
requires_attribution: needs_verification
requires_review: true
```

Rules:

- Use package-relative paths in generated manifests.
- Insert exact version, provider, target OS, target architecture, and packaging
  method during a later generation step.
- Include separate entries for Windows and macOS if the selected runtimes
  differ.
- Keep Python dependency notices separate from the interpreter/runtime notice.
- Do not include private local paths.
- Do not include submitted media URLs.
- Do not include cookie, token, secret, credential, or private config values.

## Required Future Review

Before any generated beginner package is created:

- Confirm the exact Python runtime version, provider, target OS, target
  architecture, and build identifier.
- Confirm whether the runtime is CPython from python.org, a PyInstaller output,
  a platform-provided runtime, or another approved artifact.
- Confirm the exact Python license text from the selected runtime source or
  binary distribution.
- Confirm historical license-stack and incorporated-software acknowledgements
  for the selected Python version.
- Confirm notices for bundled standard-library third-party components and
  native libraries, such as OpenSSL, expat, libffi, zlib, SQLite, Tcl/Tk, or
  other pieces when present in the selected runtime.
- Confirm whether PyInstaller, its bootloader, or another bundler adds separate
  notice obligations.
- Confirm that the beginner package does not rely on user-installed Python for
  the normal path unless that behavior is explicitly approved and documented.
- Confirm separate Python dependency notices from the exact resolved lockfile
  and bundled dependency set.
- Confirm whether separate Windows and macOS notices are required.
- Confirm signing and notarization requirements for bundled native runtime
  files.
- Confirm that the notice does not imply public hosting, ads, external-user
  service operation, DRM bypass, authentication bypass, restriction
  circumvention, or mass-download workflows.
- Confirm that package notices do not contain private paths, submitted URLs,
  cookies, tokens, secrets, or credential values.

## Not Included / Not Final Legal Advice

This source does not include:

- Final legal advice.
- Full Python license text copying.
- Generated `python-runtime-notice.txt`.
- Generated OS-specific runtime notices.
- Generated license bundle.
- Selected Python runtime artifact approval.
- Selected Python runtime download, install, build, or update behavior.
- PyInstaller spec files or package build behavior.
- Python dependency license inventory.
- Native library notice inventory.
- Generated `NOTICE.txt`.
- Generated package folder.

## Source Notes

- Future package notice candidate:
  `動画保存ツール_ローカル専用/開発者向け/notices/python-runtime-notice.txt`
- Future Windows runtime notice candidate:
  `動画保存ツール_ローカル専用/Windows用/notices/python-runtime-notice.txt`
- Future macOS runtime notice candidate:
  `動画保存ツール_ローカル専用/Mac用/notices/python-runtime-notice.txt`
- Future package license candidate:
  `動画保存ツール_ローカル専用/開発者向け/licenses/third-party/python-runtime-LICENSE.txt`
- Source status: draft candidate only.
- This file must stay source material until a later task explicitly approves
  notice bundle generation.
