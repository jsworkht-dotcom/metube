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
