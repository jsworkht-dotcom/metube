# Safety Boundaries

## Project Scope

- Local-only per-recipient use
- Controlled distribution to known recipients is allowed only through a future
  CLEAN portable distribution process
- No web publication
- No external user offering
- No external SaaS/service offering
- No monetization or ad workflow
- Markdown-only project documentation for this LLMwiki

## Prohibited Work

- No DRM bypass
- No authentication bypass
- No restriction circumvention
- No cookie/token/secret handling
- No public hosting
- No ads
- No mass-download optimization
- No bundled downloads, logs, state, cookies, tokens, secrets, or recipient data
- No generated package output until an explicit package-generation approval task
- Distribution work does not approve DRM/auth bypass, cookie handling, or
  mass-download optimization

## Local-Only Runtime Security Boundary

Y-SEC-01 adds runtime guardrails for the local-only fork. These guardrails are a
defense against accidental exposure and unsafe local configuration, not a
replacement for an OS firewall or authentication.

Current local-only runtime boundaries:

- Default runtime mode is `LOCAL_ONLY_MODE=true`.
- Default bind is `HOST=127.0.0.1`.
- Non-loopback bind targets are blocked in local-only mode.
- Normal HTTP and static UI requests are expected to use local Host values such
  as `localhost`, `127.0.0.1`, or `::1`.
- Core local-only host/source/public-host/config guard decisions have
  dependency-free helper coverage runnable with standard-library `unittest`.
- Dependency-free helper tests reduce the verification gap, but do not replace
  full aiohttp/pytest backend verification.
- Browser-originated requests with a non-local `Origin` are rejected regardless
  of method in local-only mode.
- Browser state-changing requests with a non-local `Origin` or `Referer` are
  rejected in local-only mode.
- Wildcard CORS origins are blocked in local-only mode.
- Per-download yt-dlp option overrides require the explicit unsafe escape hatch
  `ALLOW_UNSAFE_YTDL_OPTIONS_OVERRIDES=true` when local-only mode is enabled.
- Nightly automatic yt-dlp updates require the explicit unsafe escape hatch
  `ALLOW_UNSAFE_NIGHTLY_UPDATE=true` when local-only mode is enabled.
- Non-local absolute public host URLs are blocked in local-only mode.
- URL intake for downloads and subscriptions must reject local, private,
  internal, metadata-style, non-HTTP(S), malformed, and userinfo-bearing
  targets by default.
- URL intake protection is first-pass request validation. Do not claim complete
  protection against all DNS rebinding, downstream redirects, or later URLs
  fetched internally by yt-dlp.
- Logs and user-facing errors should not expose raw submitted URLs, query
  strings, token-like values, cookies, authorization headers, or local
  filesystem paths.
- Filename inputs must be sanitized before use in filesystem-affecting fields.
- Filename sanitization is first-pass input hardening. Do not claim all
  downstream yt-dlp filenames are fully controlled unless that is separately
  proven.
- Security response headers are added as a minimal browser hardening baseline.
- Do not describe the Host guard as complete protection against manually forged
  Host headers.
- These runtime checks are still not authentication.

## Update-Status Boundary

`update-status` must remain readonly unless a future manually approved task explicitly
changes that scope.

Do not include any of the following in `update-status` behavior:

- Docker pull
- git pull
- restart
- pip install
- package install or package update
- automatic update application

## Automatic Update Boundary

Do not add automatic update application unless all of these are designed, reviewed, and
explicitly approved by the user in a future task:

- Backup
- Rollback
- Version display
- Changelog or confirmation screen
- Local-only scope
- Explicit manual approval before applying changes

The backup and rollback requirements are tracked in
`docs/llmwiki/update-rollback-plan.md`. Future update-apply work must satisfy
that plan before implementation begins.

## Manual Update Apply Boundary

The manual-approval update apply design is tracked in
`docs/llmwiki/manual-update-apply-design.md`. The design does not approve
implementation.

Future update apply work must remain stopped unless all of these are explicit
for the specific update attempt:

- `/update-status` reviewed
- `/update-preflight` reviewed
- Backup completed
- Rollback targets recorded
- Candidate version or changelog reviewed
- Local-only scope confirmed
- Manual confirmation provided for the current target

Do not add an update apply endpoint, update button, backup creation, rollback
creation, Docker pull, git pull / merge / rebase, restart, pip install, or
package update unless a later task explicitly approves that exact scope.

## Dry-Run / Prepare Boundary

The dry-run / prepare-only contract is tracked in
`docs/llmwiki/dry-run-update-contract.md`. The contract does not approve
implementation.

Dry-run means readonly planning only. Prepare-only means validating a specific
plan and required confirmations only. In the first prepare stage, prepare-only
must not create backups or rollback targets.

Future dry-run or prepare work must not add update execution, update buttons,
backup creation, rollback creation, Docker pull, git pull / merge / rebase,
restart, pip install, package update, or credential handling unless a later task
explicitly approves that exact scope.

## Secret Hygiene

Do not read, paste, store, transform, or document real credential values. If credentials
or private values appear in a chat or file, stop and separate the issue as requiring
verification and redaction.

## Repository Safety Gate Boundary

The Y-CHECK-01 safety gate checker design is tracked in
`docs/llmwiki/safety-gate-checker-design.md`. The design does not approve
implementation.

A future repository safety checker may report on changed-file scope, forbidden
paths, secret-like pattern families, generated distribution folder presence, PR
#1001 file leakage, dangerous behavior, update execution, package guide /
notice completeness warnings, LLMwiki consistency, and PR safety summary fields.

The checker must remain report-only until a later task explicitly approves an
implementation stage. It must not create files, modify the repository, change
CI, install dependencies, run Docker pull, generate packages, apply updates,
send external notifications, or print secret/cookie/token values.

The checker must not weaken existing human approval gates for destructive,
credential, deployment, infrastructure, install/update, push, merge, release, or
customer-data actions.

## CLEAN Portable Distribution Checker Boundary

Y-DIST-01 adds a report-only candidate-directory checker at
`scripts/check_clean_distribution.py` and a manifest contract at
`docs/llmwiki/clean-portable-distribution-manifest.md`.

The checker may inspect only the candidate path explicitly provided by the
operator. It must remain read-only, must not follow symlinks, must not create or
delete files, must not generate `動画保存ツール_ローカル専用/`, must not create ZIP,
installer, or package output, and must not install dependencies or run Docker.

The checker must block forbidden distribution contents such as repository
metadata, `.env`, cookies, tokens, secrets, logs, state, downloads, databases,
build output, caches, editor folders, private key material, backup/temp/swap
files, obvious sensitive filenames, and conservative secret-like content pattern
families. Content reports must include only path, line, and pattern family; they
must not print file contents or matched secret values.

Passing the checker does not approve package generation, public hosting, ZIP or
installer output, external sharing, or future unchecked manual copying. Future
CLEAN share/upload/generation work must pass the checker first and still needs
explicit package-generation approval.

## CLEAN Distribution Metadata Checker Boundary

Y-DIST-02 adds a report-only candidate-directory metadata checker at
`scripts/check_distribution_metadata.py` and the contract at
`docs/llmwiki/distribution-metadata-verification.md`.

The checker must remain read-only and must not create metadata files, generate
checksums, create `動画保存ツール_ローカル専用/`, create ZIP or installer output,
install dependencies, run Docker, or modify repository files. It verifies only
an explicitly provided candidate directory.

The checker requires candidate-root `VERSION.txt`, `MANIFEST.json`,
`checksums.sha256`, `LICENSE`, and `NOTICE`. It blocks missing required files,
invalid manifest fields, `local_only` values other than `true`, unsupported
distribution types, version mismatches, malformed checksum lines, unsafe
checksum paths, missing listed files, duplicate listed paths, non-regular or
symlink listed paths, checksum mismatches, empty license / notice files, and
secret-like metadata content patterns. Reports must not print file contents or
matched secret values.

Passing the metadata checker does not approve package generation, checksum
generation, metadata generation, public hosting, ZIP or installer output,
external sharing, or legal sufficiency of license / notice material. Future
CLEAN share/upload/generation work must pass both Y-DIST-01 and Y-DIST-02 and
still needs explicit package-generation approval and human review.

## Recipient Runbook And First-Run Verification Boundary

Y-DIST-03 adds recipient-safe documentation at
`docs/llmwiki/recipient-safe-runbook.md` and
`docs/llmwiki/first-run-local-only-verification.md`.

These documents are procedural source-of-truth material for future recipient
handoff and first-run review. They must remain docs-only unless a later task
explicitly approves a different scope.

Y-DIST-03 does not approve:

- No CLEAN folder generation.
- No ZIP, installer, or package output.
- No metadata generation.
- No checksum generation.
- No real download verification.
- No dependency install/update operations.
- No Docker pull/build operations.
- No backend/frontend runtime changes.
- No yt-dlp extractor or download queue changes.
- No public hosting.
- No cookie/token/secret handling.
- No PR #1001 file inclusion.

Future first-run confirmation must stop if the app listens on an external host,
`0.0.0.0`, a LAN IP, or a public IP; if the browser URL is not loopback; if
credential-bearing file handling becomes necessary; if DRM bypass,
authentication bypass, or restriction circumvention becomes necessary; if update
application operations run automatically; or if distribution artifact creation
occurs without explicit human approval.

## Distribution Readiness Matrix Boundary

Y-DIST-04 adds advisory documentation at
`docs/llmwiki/distribution-readiness-matrix.md`.

The matrix may summarize ready, blocked, human-review-required, not-started,
not-applicable-yet, and warning-only items. It must remain advisory and must not
approve CLEAN folder generation, ZIP / installer / package output, metadata
generation, checksum generation, real download verification, dependency
installation operations, container image operations, backend/frontend runtime
changes, public hosting, credential-bearing file handling, or PR #1001 file
inclusion.

Future distribution readiness must stop if external/public hosting appears,
non-loopback bind or public URL appears, DRM/auth/restriction bypass is needed,
credential-bearing file handling is needed, PR #1001 files appear, generated
package output appears without approval, metadata/checksum generation appears
without approval, local-fork-safety fails unexpectedly, Y-DIST-01 fails,
Y-DIST-02 fails, or recipient first-run verification fails.

## Artifact Generation Approval Checklist Boundary

Y-DIST-05 adds docs-only approval documentation at
`docs/llmwiki/artifact-generation-approval-checklist.md`.

The checklist must remain a gate definition only. It does not approve CLEAN
folder generation, metadata file generation, checksum generation, ZIP output,
installer output, first-run verification, real download verification, recipient
handoff, sharing, dependency installation, Docker image operations, image pull
or image build operations, backend/frontend runtime changes, public hosting,
credential-bearing file handling, or PR #1001 file inclusion.

Artifact generation remains blocked by default. Any future approval must name
the exact source commit, exact candidate or output path, exact artifact scope,
required checks, required manual reviews, stop conditions, and explicitly
forbidden operations. Any category not named in the approval remains forbidden.

## Approved Clean Candidate Dry-Run Plan Boundary

Y-DIST-06 adds docs-only dry-run planning documentation at
`docs/llmwiki/approved-clean-candidate-dry-run-plan.md`.

The plan must remain a future execution plan only. It does not approve CLEAN
folder generation, ZIP / installer / package output, metadata generation,
checksum generation, real downloads, dependency installation, no Docker pull/build
operations, backend/frontend runtime changes, public hosting,
credential-bearing file handling, or PR #1001 file inclusion.

Candidate-directory checker execution remains `not_applicable_yet` until a
future explicit Y-DIST-05 approval names the exact source commit, candidate
path, output path, artifact scope, and forbidden operations.

## Codex Automation Boundary

The Codex automation policy is tracked in
`docs/llmwiki/codex-automation-policy.md`.

Low-risk work may use auto PR and auto merge when the current task scope and
required gates pass.

Medium-risk work may use auto PR and auto merge only when safety gates pass and
the diff does not add package output, dependency changes, generated
distribution folders, credential handling, public hosting, ads, or PR #1001
file leakage.

High-low work may use auto PR and auto merge only when it remains docs-only,
report-only, or dry-run-only and all high-low mandatory conditions pass.
Generated distribution folders, ZIP/package/installer creation, dependency
install/update, package/lockfile changes, and Docker pull/build are prohibited
in high-low auto-merge work. Backend download or queue logic changes, yt-dlp
logic changes, cookie/token/secret handling, public hosting, and ads are also
prohibited.

High-mid work may be implemented, verified, opened as a PR, and marked ready for
review only after an explicit task approves the scope. Auto merge is prohibited,
the PR must state `human-review-required`, and merge is allowed only after human
confirmation.

High-mid work must stop instead of proceeding if it requires package/lockfile
changes or dependency install/update. Docker pull/build is prohibited and must
stop the task. Backend download or queue logic changes, yt-dlp or extractor
changes, cookie/token/secret handling, public hosting, ads, real distribution
output, ZIP/package/installer output, or generated artifacts created during
verification without separate human approval must also stop the task.

High-high work is automatic-execution prohibited. Codex must stop before
implementation and request explicit human confirmation.

## Dockerless Desktop Distribution Boundary

Y-06 desktop work may discuss Dockerless desktop distribution for Windows and
macOS, but it must not implement packaging, installers, code signing,
notarization, updater logic, backend changes, frontend changes, Docker changes,
CI changes, package changes, or lockfile changes unless a later task explicitly
approves that exact scope.

Beginner-friendly UX planning is allowed as documentation. Public hosting,
external-user offering, ads, DRM bypass, authentication bypass, restriction
circumvention, and mass-download optimization remain out of scope.

The Y-06B contract is tracked in
`docs/llmwiki/desktop-sidecar-lifecycle-contract.md`. That contract defines
future desktop sidecar lifecycle and package boundaries, but it does not approve
implementation, build scripts, installers, signing, updater behavior, dependency
changes, or lockfile changes.

The Y-06C package and guide contracts are tracked in
`docs/llmwiki/desktop-package-manifest.md` and
`docs/llmwiki/beginner-guide-skeleton.md`. Those contracts define future
package layout and guide shape, but they do not approve generated distribution
folders, package generation scripts, Tauri/Electron/WebView2 implementation,
build/package commands, installers, signing, updater behavior, dependency
changes, or lockfile changes.

The Y-06D clean-package dry-run contract is tracked in
`docs/llmwiki/clean-package-dry-run-contract.md`. That contract defines future
dry-run report shape, planned output manifest, include/exclude rules,
validation gates, warning/error/blocked classification, and stop conditions, but
it does not approve a generator implementation or any generated package files.

Desktop planning must preserve these safety rules:

- Backend must be planned as local-only and bound to `127.0.0.1`.
- No public tunnel, reverse proxy, LAN service mode, or hosted mode.
- No cookie/token/secret handling in the beginner desktop flow.
- No generated beginner package may contain `.git`, `.github`, caches,
  `node_modules`, local downloads, state, logs, temp files, `.env`, `cookies.txt`,
  cookie files, token files, secret files, personal backups, command logs, dev
  branch metadata, or upstream PR #1001 files.
- Future clean-package dry-run must block forbidden paths, forbidden filenames,
  forbidden content pattern families, generated package folder presence, PR
  #1001 leakage, and any planned output that implies public hosting, ads, update
  apply, Docker pull, git update, package install/update, or credential handling.
- No logs, diagnostics, package manifests, or guide examples may contain real
  cookie, token, secret, or private URL values.
- No automatic update apply.
- No Docker pull, git pull / merge / rebase, restart, pip install, package
  install, or package update from a desktop app.
- No Tauri/Electron/WebView2 implementation until a later task explicitly
  approves that exact implementation scope.
