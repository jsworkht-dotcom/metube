# Frontend Dependency Notice Source

## Purpose

This file is source material for a future frontend dependency notice entry in a
clean beginner package.

It is not a generated notice file. It does not copy full license texts,
generate a notice bundle, create `動画保存ツール_ローカル専用/`, create HTML or
TXT package guide output, run a frontend build, change package or lock files,
or decide final redistribution readiness.

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
        frontend/
    notices/
      frontend-deps-notice.txt
      frontend-notices.txt
      third-party-notices.txt
    manifest/
      license-notice-manifest.json
  Windows用/
    runtime/
      frontend/
    notices/
      runtime-notices.txt
  Mac用/
    runtime/
      frontend/
    notices/
      runtime-notices.txt
```

Rules:

- Beginner guide pages should point to `開発者向け/` for license and notice
  details.
- The first-open guide should not paste long dependency notices into the normal
  beginner flow.
- OS-specific runtime notices may point to the shared frontend notice when the
  built frontend assets are identical across Windows and macOS packages.
- A later approved generator may transform this source into package notice
  output.
- This source alone does not approve package generation.

## Frontend Dependency Candidate Sources

Local source candidates checked read-only for this draft:

- `ui/package.json`
- `ui/pnpm-lock.yaml`

Local candidate facts:

- `ui/package.json` is marked `private: true`.
- `ui/package.json` declares Angular 21 frontend dependencies.
- `ui/package.json` declares Bootstrap, Font Awesome, ng-bootstrap, ng-select,
  Popper, RxJS, tslib, Zone.js, Socket.IO frontend integration, and a browser
  cookie helper package.
- `ui/package.json` declares Angular build, Angular CLI, Angular compiler CLI,
  Angular localize, ESLint, TypeScript, jsdom, TypeScript ESLint, and Vitest as
  development / build-tool candidates.
- `ui/pnpm-lock.yaml` exists and uses `lockfileVersion: '9.0'`.
- `ui/pnpm-lock.yaml` records resolved direct dependency versions and many
  transitive dependency candidates.

Current selection status:

```text
No exact future frontend build artifact, dependency notice inventory, or
generated package dependency set has been selected.
```

Assumptions for this source draft:

- Future beginner packages will include built Angular frontend assets, not the
  full `ui/` source tree or package manager cache.
- Runtime notices should be based on the exact built assets and resolved
  dependency graph used by a later package generation task.
- Development and build tools should remain developer-only unless their code,
  generated output, fonts, icons, styles, source maps, or helper assets are
  actually bundled into the beginner package.

Needs future verification:

- Which direct dependencies are present in the built frontend output.
- Which transitive dependencies are present in the built frontend output.
- Whether source maps are excluded or explicitly reviewed.
- Whether Font Awesome icons, fonts, SVG data, Bootstrap CSS, Popper logic,
  service worker files, localization files, or other static assets require
  separate notices.
- Whether build tooling notices are needed because a tool's runtime code or
  generated asset is bundled.

## Package / Lockfile Review Candidate

Direct runtime dependency candidates from `ui/package.json`:

```text
@angular/animations
@angular/common
@angular/compiler
@angular/core
@angular/forms
@angular/platform-browser
@angular/platform-browser-dynamic
@angular/service-worker
@fortawesome/angular-fontawesome
@fortawesome/fontawesome-svg-core
@fortawesome/free-brands-svg-icons
@fortawesome/free-regular-svg-icons
@fortawesome/free-solid-svg-icons
@ng-bootstrap/ng-bootstrap
@ng-select/ng-select
@popperjs/core
bootstrap
ngx-cookie-service
ngx-socket-io
rxjs
tslib
zone.js
```

Direct developer / build-tool dependency candidates from `ui/package.json`:

```text
@angular-eslint/builder
@angular/build
@angular/cli
@angular/compiler-cli
@angular/localize
@eslint/js
angular-eslint
eslint
jsdom
typescript
typescript-eslint
vitest
```

Lockfile review candidates:

- Use `ui/pnpm-lock.yaml` to identify exact resolved versions for direct
  dependencies.
- Use `ui/pnpm-lock.yaml` to identify transitive packages, including build-tool
  transitive candidates such as Vite, Sass, PostCSS, and other packages
  recorded through the Angular build graph.
- Use package manager metadata or package tarballs in a later review step to
  confirm exact license names, license text files, notice files, repository
  URLs, and attribution requirements.
- Use future built artifact metadata to decide whether each package is
  runtime-included, generated-output-only, developer-only, or not bundled.

Classification candidates:

| Candidate group | Initial classification | Future review need |
| --- | --- | --- |
| Angular runtime packages | runtime candidate | Confirm exact built output and Angular license notices. |
| RxJS, tslib, Zone.js | runtime candidate | Confirm exact versions and bundled code paths. |
| Bootstrap and Popper | runtime / style candidate | Confirm CSS, JS, source map, and attribution handling. |
| Font Awesome packages | icon / asset candidate | Confirm icon families actually used and license text required. |
| ng-bootstrap and ng-select | runtime UI library candidate | Confirm exact included code and styles. |
| ngx-socket-io | runtime communication candidate | Confirm browser bundle inclusion. |
| ngx-cookie-service | runtime helper candidate | Confirm whether the package remains in built assets. |
| Angular build / CLI / compiler tooling | build-tool candidate | Include notices only if tool runtime or generated assets require it. |
| ESLint, TypeScript, Vitest, jsdom | developer-only candidate | Exclude from runtime notices unless bundled artifacts require review. |
| Vite, Sass, PostCSS, and other transitive build tools | transitive build-tool candidate | Review from lockfile and built artifact manifest later. |

## Upstream / Registry URL Candidates

Package URL candidates should be generated from package names in a later review
step. Candidate registry URL shape:

```text
https://www.npmjs.com/package/<package-name>
```

Project source URL candidates should come from selected package metadata, not
from guesses in this source file.

Rules:

- Prefer package tarball metadata, package registry metadata, and repository
  metadata tied to the selected lockfile versions.
- Do not use private local paths in generated manifests.
- Do not include submitted media URLs.
- Do not include cookie, token, secret, credential, or private config values.
- Keep exact license names as `needs_verification` until a later license
  inventory confirms them.

## Beginner-Facing Short Notice

Future beginner guides may use short wording like this:

```text
このツールの画面表示には、Angular、Bootstrap、Font Awesome などの
フロントエンド部品を使用する場合があります。
ライセンスと著作権表示は「開発者向け」フォルダで確認できます。
```

Rules:

- Keep this short.
- Do not make dependency review part of the normal first-start flow.
- Do not imply public redistribution readiness.
- Do not ask beginners to run package manager commands, inspect lockfiles, or
  review build artifacts during normal use.

## Developer-Facing Notice Draft

Candidate future notice text:

```text
Frontend dependency notice

この配布物は、画面表示とブラウザ内の動作のために Angular、Bootstrap、
Font Awesome、RxJS、Zone.js、Popper、およびその他のフロントエンド
依存関係を使用する場合があります。

現在のリポジトリでは、ui/package.json と ui/pnpm-lock.yaml が
フロントエンド依存関係と開発用ツールの候補ソースです。ただし、実際の
初心者向け配布物に含まれる frontend build、静的 asset、直接依存関係、
推移的依存関係、source map、font/icon asset、および notice 一式はまだ
確定していません。

実際の配布パッケージを作成する前に、選択された lockfile、build artifact、
runtime dependency graph、developer-only dependency の除外範囲、ライセンス
本文、著作権表示、第三者 notice、および font/icon/style asset の条件を
あらためて確認してください。

この notice 原稿は、Web 公開、広告収益化、外部ユーザー向けサービス化、
cookie/token/secret 共有、DRM bypass、認証 bypass、または制限回避を
許可するものではありません。
```

This draft is intentionally short. The full license body and transitive
dependency notices should come from reviewed package files, lockfile metadata,
and selected build artifact metadata in a later approved notice-bundle task.

## Manifest Candidate Fields

A future `license-notice-manifest.json` entry for frontend dependencies should
include one entry per reviewed package or asset family.

Candidate aggregate entry:

```text
component_name: frontend dependencies
component_kind: frontend_dependency_inventory
source_path: ui/package.json / ui/pnpm-lock.yaml / selected build artifact manifest
package_notice_path: 開発者向け/notices/frontend-deps-notice.txt
package_notice_aggregate_path: 開発者向け/notices/frontend-notices.txt
package_license_dir: 開発者向け/licenses/third-party/frontend/
lockfile_path: ui/pnpm-lock.yaml
lockfile_version: 9.0
build_artifact_manifest: generated manifest should insert selected artifact report
dependency_inventory_path: generated manifest should insert reviewed inventory path
license_name: needs_verification
source_url: generated manifest should insert package-specific source URLs
package_url: generated manifest should insert package-specific registry URLs
version: generated manifest should insert each selected package version
dependency_scope: runtime_candidate / build_tool_candidate / developer_only_candidate
included_in_package: needs_verification
asset_family: js / css / font / svg / service_worker / source_map / other
requires_attribution: needs_verification
requires_license_text: needs_verification
requires_source_offer: needs_verification
requires_review: true
```

Rules:

- Use package-relative paths in generated manifests.
- Insert exact versions during a later generation step.
- Include package-specific entries rather than only one aggregate entry when
  the final notice bundle is generated.
- Separate runtime dependencies from developer-only and build-tool candidates.
- Identify font, icon, style, service worker, and source map assets separately.
- Do not include private local paths.
- Do not include submitted media URLs.
- Do not include cookie, token, secret, credential, or private config values.

## Required Future Review

Before any generated beginner package is created:

- Confirm the exact frontend build artifact selected for the package.
- Confirm the exact `ui/package.json` and `ui/pnpm-lock.yaml` versions used for
  that build.
- Generate a dependency license inventory from the resolved lockfile used for
  the package.
- Identify which direct and transitive dependencies are present in the built
  frontend output.
- Classify each package as runtime-included, generated-output-only,
  developer-only, build-tool-only, or not bundled.
- Confirm exact license names, license text files, notice files, copyright
  notices, and repository/source URLs from selected package artifacts.
- Confirm separate notices for Angular, Bootstrap, Font Awesome, Popper, RxJS,
  Zone.js, tslib, ng-bootstrap, ng-select, Socket.IO frontend integration, and
  any included transitive dependencies.
- Confirm whether Font Awesome icon families, SVG paths, fonts, CSS files,
  source maps, service worker files, and localization outputs require separate
  notice entries.
- Confirm whether developer/build tools such as Angular CLI, Angular build,
  TypeScript, ESLint, Vitest, jsdom, Vite, Sass, or PostCSS are excluded from
  the beginner runtime package or need notices because of bundled output.
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

- Read the exact selected `ui/package.json` and `ui/pnpm-lock.yaml`.
- Read a generated frontend build artifact manifest if one is approved later.
- Produce a package-relative dependency inventory.
- Produce package-specific notice entries for runtime-included frontend
  dependencies and asset families.
- Preserve developer-only classifications for build tools that are not bundled.
- Include full license text only from reviewed package artifacts or official
  package metadata.
- Record unresolved items as `needs_verification` rather than guessing.
- Keep reports sanitized and free of private paths, submitted URLs, cookies,
  tokens, secrets, and credential values.
- Avoid creating package files until a later package generation task is
  explicitly approved.

## Not Included / Legal-Not-Final Boundary

This source does not include:

- Final legal advice.
- Full license text copying.
- Generated `frontend-deps-notice.txt`.
- Generated `frontend-notices.txt`.
- Generated `third-party-notices.txt`.
- Generated license bundle.
- Generated dependency license inventory.
- Generated frontend build artifact manifest.
- Package or lockfile changes.
- Frontend build output.
- HTML or TXT package guide output.
- Generated package folder.
- Dependency changes or package manager operations.
- Tauri or Electron notices.
- Desktop shell runtime notices.
- Approval for public redistribution readiness.

## Source Notes

- Future package notice candidate:
  `動画保存ツール_ローカル専用/開発者向け/notices/frontend-deps-notice.txt`
- Future aggregate notice candidate:
  `動画保存ツール_ローカル専用/開発者向け/notices/frontend-notices.txt`
- Future package license directory candidate:
  `動画保存ツール_ローカル専用/開発者向け/licenses/third-party/frontend/`
- Source status: draft candidate only.
- This file must stay source material until a later task explicitly approves
  notice bundle generation.
