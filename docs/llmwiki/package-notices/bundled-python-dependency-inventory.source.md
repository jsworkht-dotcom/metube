# Bundled Python Dependency Inventory Source

## Purpose

This file is source material for a future bundled Python/backend dependency
inventory in a clean beginner package.

It is not a generated notice file. It does not copy full license texts,
generate a notice bundle, create `動画保存ツール_ローカル専用/`, install or update
dependencies, run a dependency audit, change package or lock files, build a
backend package, create HTML or TXT package guide output, or decide final
redistribution readiness.

This source is not final legal advice.

## Future Package Role

Future user-facing package:

```text
動画保存ツール_ローカル専用/
```

Future inventory / notice / license placement candidates:

```text
動画保存ツール_ローカル専用/
  開発者向け/
    inventory/
      bundled-python-dependency-inventory.json
      bundled-python-dependency-inventory.md
    licenses/
      third-party/
        python-dependencies/
    notices/
      python-deps-notice.txt
      third-party-notices.txt
    manifest/
      license-notice-manifest.json
  Windows用/
    runtime/
      backend/
    notices/
      runtime-notices.txt
  Mac用/
    runtime/
      backend/
    notices/
      runtime-notices.txt
```

Rules:

- Beginner guide pages should point to `開発者向け/` for dependency, license,
  and notice details.
- Runtime notices should describe only dependencies actually bundled into the
  selected Windows or macOS backend runtime.
- Development dependencies should remain out of beginner runtime notices unless
  their code, generated output, or license text is actually bundled.
- A later approved generator may transform this source into generated
  inventory and notice output.
- This source alone does not approve package generation.

## Read-Only Dependency Source Files Inspected

Repository files checked read-only for this draft:

| Source candidate | Status | Notes |
| --- | --- | --- |
| `pyproject.toml` | present | Declares Python requirement, runtime dependencies, and `dev` dependency group. |
| `uv.lock` | present | Records resolved package versions and selected yt-dlp extras for the current lock graph. |
| `poetry.lock` | not present | No Poetry lockfile was found in this repository. |
| `requirements*.txt` | not present | No requirements or constraints text files were found. |
| `setup.py` | not present | No setuptools script was found. |
| `setup.cfg` | not present | No setuptools config dependency source was found. |
| `Pipfile` | not present | No Pipenv dependency source was found. |
| `Pipfile.lock` | not present | No Pipenv lockfile was found. |
| `environment*.yml` / `environment*.yaml` | not present | No Conda environment dependency source was found. |
| `constraints*.txt` | not present | No pip constraints file was found. |
| `tox.ini` | not present | No tox dependency source was found. |
| `noxfile.py` | not present | No nox dependency source was found. |

No package manager install, dependency update, dependency audit, build, package
generation, or lockfile write was performed for this draft.

## Local Candidate Facts

From `pyproject.toml`:

- Project name: `metube`
- Project version: `0.1.0`
- Python requirement: `>=3.13`
- Runtime dependency declarations:
  - `aiohttp`
  - `python-socketio>=5.0,<6.0`
  - `yt-dlp[default,curl-cffi,deno]`
  - `mutagen`
  - `curl-cffi`
  - `watchfiles`
- Developer dependency group:
  - `pylint`
  - `pytest>=8.0`
  - `pytest-aiohttp>=1.0`
  - `pytest-asyncio>=0.24`

From `uv.lock`:

- Lockfile version: `1`
- Lockfile revision: `3`
- Lockfile Python requirement: `>=3.13`
- Root package `metube` is a virtual local package.
- Root package runtime dependencies match the local `pyproject.toml`
  dependency declarations.
- Root package `dev` dependencies match the local `pyproject.toml`
  developer dependency group.
- `yt-dlp` optional dependency groups selected by the root dependency include
  `default`, `curl-cffi`, and `deno`.

Current selection status:

```text
No exact future backend runtime bundle, dependency inventory, license bundle,
or generated notice set has been selected.
```

## Runtime Dependency Candidates

Direct runtime dependency candidates from `pyproject.toml`, with versions
currently resolved in `uv.lock`:

| Package | Declared role | Resolved version candidate | License candidate | Source URL candidate |
| --- | --- | --- | --- | --- |
| `aiohttp` | backend HTTP server/runtime framework | `3.13.5` | `needs_verification` | `https://pypi.org/project/aiohttp/3.13.5/` |
| `curl-cffi` | curl-impersonation / request helper candidate | `0.14.0` | `needs_verification` | `https://pypi.org/project/curl-cffi/0.14.0/` |
| `mutagen` | media metadata helper candidate | `1.47.0` | `needs_verification` | `https://pypi.org/project/mutagen/1.47.0/` |
| `python-socketio` | Socket.IO backend realtime runtime | `5.16.2` | `needs_verification` | `https://pypi.org/project/python-socketio/5.16.2/` |
| `watchfiles` | filesystem watch / reload helper candidate | `1.2.0` | `needs_verification` | `https://pypi.org/project/watchfiles/1.2.0/` |
| `yt-dlp` | downloader / extractor runtime library | `2026.3.17` | `Unlicense` from existing yt-dlp source draft; recheck required | `https://pypi.org/project/yt-dlp/2026.3.17/` |

Notes:

- `yt-dlp` already has a separate source-only notice draft at
  `docs/llmwiki/package-notices/yt-dlp-notice.source.md`.
- `curl-cffi`, `mutagen`, and selected yt-dlp extras may require separate
  notice entries if actually bundled.
- License candidates remain non-final until a later review checks selected
  package metadata, source distributions, wheels, license files, and notice
  files.

## Optional / Indirect Dependency Candidates

Optional or indirect candidates currently present in `uv.lock` through the
runtime graph and selected yt-dlp extras:

| Package | Resolved version candidate | Initial relationship | License candidate | Source URL candidate |
| --- | --- | --- | --- | --- |
| `aiohappyeyeballs` | `2.6.2` | `aiohttp` transitive | `needs_verification` | `https://pypi.org/project/aiohappyeyeballs/2.6.2/` |
| `aiosignal` | `1.4.0` | `aiohttp` transitive | `needs_verification` | `https://pypi.org/project/aiosignal/1.4.0/` |
| `anyio` | `4.13.0` | `watchfiles` transitive | `needs_verification` | `https://pypi.org/project/anyio/4.13.0/` |
| `attrs` | `26.1.0` | `aiohttp` / `aiosignal` transitive | `needs_verification` | `https://pypi.org/project/attrs/26.1.0/` |
| `bidict` | `0.23.1` | `python-socketio` transitive | `needs_verification` | `https://pypi.org/project/bidict/0.23.1/` |
| `brotli` | `1.2.0` | `yt-dlp[default]` optional candidate | `needs_verification` | `https://pypi.org/project/brotli/1.2.0/` |
| `brotlicffi` | `1.2.0.1` | `yt-dlp[default]` optional candidate | `needs_verification` | `https://pypi.org/project/brotlicffi/1.2.0.1/` |
| `certifi` | `2026.5.20` | `curl-cffi` / `requests` / `yt-dlp[default]` candidate | `needs_verification` | `https://pypi.org/project/certifi/2026.5.20/` |
| `cffi` | `2.0.0` | `curl-cffi` / `brotlicffi` transitive | `needs_verification` | `https://pypi.org/project/cffi/2.0.0/` |
| `charset-normalizer` | `3.4.7` | `requests` transitive | `needs_verification` | `https://pypi.org/project/charset-normalizer/3.4.7/` |
| `deno` | `2.8.1` | `yt-dlp[deno]` optional candidate | `needs_verification` | `https://pypi.org/project/deno/2.8.1/` |
| `frozenlist` | `1.8.0` | `aiohttp` / `aiosignal` / `yarl` transitive | `needs_verification` | `https://pypi.org/project/frozenlist/1.8.0/` |
| `h11` | `0.16.0` | `wsproto` transitive | `needs_verification` | `https://pypi.org/project/h11/0.16.0/` |
| `idna` | `3.17` | `yarl` / `requests` / `anyio` transitive | `needs_verification` | `https://pypi.org/project/idna/3.17/` |
| `multidict` | `6.7.1` | `aiohttp` / `yarl` transitive | `needs_verification` | `https://pypi.org/project/multidict/6.7.1/` |
| `propcache` | `0.5.2` | `aiohttp` / `yarl` transitive | `needs_verification` | `https://pypi.org/project/propcache/0.5.2/` |
| `pycparser` | `3.0` | `cffi` transitive | `needs_verification` | `https://pypi.org/project/pycparser/3.0/` |
| `pycryptodomex` | `3.23.0` | `yt-dlp[default]` optional candidate | `needs_verification` | `https://pypi.org/project/pycryptodomex/3.23.0/` |
| `python-engineio` | `4.13.2` | `python-socketio` transitive | `needs_verification` | `https://pypi.org/project/python-engineio/4.13.2/` |
| `requests` | `2.34.2` | `yt-dlp[default]` optional candidate | `needs_verification` | `https://pypi.org/project/requests/2.34.2/` |
| `simple-websocket` | `1.1.0` | `python-engineio` transitive | `needs_verification` | `https://pypi.org/project/simple-websocket/1.1.0/` |
| `urllib3` | `2.7.0` | `requests` / `yt-dlp[default]` candidate | `needs_verification` | `https://pypi.org/project/urllib3/2.7.0/` |
| `websockets` | `16.0` | `yt-dlp[default]` optional candidate | `needs_verification` | `https://pypi.org/project/websockets/16.0/` |
| `wsproto` | `1.3.2` | `simple-websocket` transitive | `needs_verification` | `https://pypi.org/project/wsproto/1.3.2/` |
| `yarl` | `1.24.2` | `aiohttp` transitive | `needs_verification` | `https://pypi.org/project/yarl/1.24.2/` |
| `yt-dlp-ejs` | `0.8.0` | `yt-dlp[default]` optional candidate | `needs_verification` | `https://pypi.org/project/yt-dlp-ejs/0.8.0/` |

Review notes:

- This table is an inventory starting point, not a final bundled set.
- A later package generator must decide whether Python wheels, source
  distributions, native extension files, certificates, helper binaries, or
  optional extras are actually present in the package.
- `brotli` and `brotlicffi` are both recorded in the lock graph; a later review
  must classify platform and implementation markers before notices are
  generated.
- `deno` here is the Python package candidate selected by the yt-dlp extra, not
  an approved Deno runtime binary bundle.

## Developer-Only Dependency Candidates

Direct developer dependency candidates from `pyproject.toml`, with versions
currently resolved in `uv.lock`:

| Package | Declared role | Resolved version candidate | License candidate | Source URL candidate |
| --- | --- | --- | --- | --- |
| `pylint` | lint / static analysis | `4.0.5` | `needs_verification` | `https://pypi.org/project/pylint/4.0.5/` |
| `pytest` | backend test runner | `9.0.3` | `needs_verification` | `https://pypi.org/project/pytest/9.0.3/` |
| `pytest-aiohttp` | aiohttp test helper | `1.1.0` | `needs_verification` | `https://pypi.org/project/pytest-aiohttp/1.1.0/` |
| `pytest-asyncio` | asyncio test helper | `1.4.0` | `needs_verification` | `https://pypi.org/project/pytest-asyncio/1.4.0/` |

Developer-only transitive candidates currently present in `uv.lock` outside
the runtime candidate graph:

| Package | Resolved version candidate | Initial relationship | License candidate | Source URL candidate |
| --- | --- | --- | --- | --- |
| `astroid` | `4.0.4` | `pylint` transitive | `needs_verification` | `https://pypi.org/project/astroid/4.0.4/` |
| `colorama` | `0.4.6` | `pylint` / `pytest` transitive | `needs_verification` | `https://pypi.org/project/colorama/0.4.6/` |
| `dill` | `0.4.1` | `pylint` transitive | `needs_verification` | `https://pypi.org/project/dill/0.4.1/` |
| `iniconfig` | `2.3.0` | `pytest` transitive | `needs_verification` | `https://pypi.org/project/iniconfig/2.3.0/` |
| `isort` | `8.0.1` | `pylint` transitive | `needs_verification` | `https://pypi.org/project/isort/8.0.1/` |
| `mccabe` | `0.7.0` | `pylint` transitive | `needs_verification` | `https://pypi.org/project/mccabe/0.7.0/` |
| `packaging` | `26.2` | `pytest` transitive | `needs_verification` | `https://pypi.org/project/packaging/26.2/` |
| `platformdirs` | `4.10.0` | `pylint` transitive | `needs_verification` | `https://pypi.org/project/platformdirs/4.10.0/` |
| `pluggy` | `1.6.0` | `pytest` transitive | `needs_verification` | `https://pypi.org/project/pluggy/1.6.0/` |
| `pygments` | `2.20.0` | `pytest` transitive | `needs_verification` | `https://pypi.org/project/pygments/2.20.0/` |
| `tomlkit` | `0.15.0` | `pylint` transitive | `needs_verification` | `https://pypi.org/project/tomlkit/0.15.0/` |

Review notes:

- These are developer-only candidates unless a later package task proves that
  their code, generated output, license text, or notice file is included in the
  beginner package.
- Test and lint packages should normally be excluded from runtime notices for a
  clean beginner package.
- If a future source package includes developer tooling or complete source
  trees, this classification must be reviewed again.

## Manifest Candidate Fields

A future generated inventory entry should include fields like:

```text
schema_version
package_name
source_commit
generated_at
review_status
component_name
normalized_package_name
component_kind
declared_dependency_group
resolved_version
specifier
extras
markers
direct_dependency
transitive_dependency
optional_dependency
developer_only
runtime_included
source_path
lockfile_path
registry_url
package_url
source_distribution_url
wheel_urls
repository_url
license_name
license_expression
license_text_path
notice_path
copyright_holders
requires_source_offer
requires_attribution
contains_native_code
contains_certificates
contains_helper_binary
target_os
target_arch
requires_review
review_notes
```

Rules:

- Use package-relative paths in generated manifests.
- Use the exact selected lockfile and bundled artifact set.
- Do not include private local paths.
- Do not include submitted media URLs.
- Do not include cookie, token, secret, credential, or private config values.
- Keep `license_name` or `license_expression` as `needs_verification` until a
  later license review confirms exact metadata and license text.
- Record separate entries for OS-specific wheels or native artifacts when the
  generated package differs between Windows and macOS.

## License Review Checklist

Before any generated beginner package is created:

- Confirm the exact lockfile revision and source commit used for packaging.
- Confirm exact resolved versions from the selected lockfile, not from this
  draft alone.
- Confirm license metadata from selected package metadata, wheels, source
  distributions, license files, and notice files.
- Confirm whether each package is runtime-included, optional, indirect,
  developer-only, generated-output-only, or excluded.
- Confirm selected yt-dlp extras and their transitive dependency obligations.
- Confirm whether `curl-cffi`, `cffi`, `brotli`, `brotlicffi`, `watchfiles`,
  or other packages include native code requiring OS-specific review.
- Confirm whether `certifi` or other packages include certificate bundles or
  data files requiring distinct notice handling.
- Confirm whether Deno-related support is a Python package dependency only, a
  helper binary, or excluded from the beginner package.
- Confirm whether any package requires source-offer, attribution, NOTICE file,
  copyright file, or license-copy handling.
- Confirm that developer-only dependencies are not bundled into the runtime
  package unless deliberately selected and reviewed.
- Confirm that package notices do not contain private paths, submitted URLs,
  cookies, tokens, secrets, or credential values.

## Notice Bundle Review Checklist

Before generating notice bundle output:

- Generate the final dependency inventory from the selected package inputs.
- Include one notice entry per bundled Python/backend dependency or aggregate
  entries with a manifest that preserves each package's version and license.
- Include separate notice entries for selected yt-dlp extras if required.
- Include OS-specific notes for wheels, native extension modules, helper
  binaries, certificates, or runtime payloads that differ by platform.
- Keep beginner-facing guide text short and point to `開発者向け/`.
- Keep full license bodies in reviewed license files, not inline in beginner
  guide pages.
- Keep generated manifests free of secret-like values and private local paths.
- Re-run repository safety and clean-package dry-run checks before creating any
  package output in a later approved task.

## Not Included / Legal-Not-Final Boundary

This draft does not include:

- final legal advice
- final bundled dependency selection
- generated dependency inventory files
- actual notice files
- actual license files
- copied license text
- generated distribution folders
- backend or frontend changes
- Docker or CI changes
- package or lockfile changes
- dependency install, update, audit, build, or package commands
- secret, token, cookie, credential, or private URL handling
- public hosting, advertising, monetization, or external-user service support
- PR #1001 file changes
- 更新適用機能

## Future Generated Inventory Requirements

A later approved package generation or license review task should:

- Start from the exact branch, source commit, and lockfile selected for the
  package.
- Resolve direct, optional, transitive, and developer-only dependencies from
  structured package metadata.
- Preserve package names, normalized names, versions, extras, markers,
  dependency group, source URLs, package URLs, license metadata, and artifact
  URLs.
- Record whether each dependency is actually bundled in Windows, macOS, both,
  or neither package outputs.
- Record license text and notice file paths using package-relative paths.
- Record review status per package instead of using one global approval flag.
- Emit sanitized output only.
- Fail or block package generation if final license data, notice files, secret
  hygiene, or package scope checks are incomplete.
