# Handoff

## Short Context

This is `youtubeダウンロード / MeTube local-only fork`, a local-only fork of MeTube.
The current premise is controlled CLEAN portable distribution to known
recipients, with each recipient running the app locally on their own PC. The
canonical branch is fork `master`, and local `master` tracks `fork/master`.

## Current Closeout State

- Current Y-DIST-02 work branch:
  `codex/y-dist-02-metadata-checker`.
- Baseline before Y-DIST-02: fork `master`
  `f2e2678e3dc986a34f2e5bb0bd65f56d54b2b415` from fork PR #85.
- Y-SEC-01 is complete via fork PR #82.
- Y-SEC-01 state:
  - local-only runtime guardrails implemented in backend startup/request
    handling
  - default bind is `HOST=127.0.0.1`
  - non-loopback bind targets are blocked when `LOCAL_ONLY_MODE=true`
  - dependency-free local-only security helper logic added with
    standard-library `unittest` coverage for host/source/public-host/config
    guard decisions
  - these dependency-free tests reduce the current verification gap, but full
    aiohttp/pytest backend verification remains pending in an environment with
    dependencies
  - local Host allowlist guard
  - non-local `Origin` headers are rejected for all local-only requests,
    including GET and browser handshake-style requests
  - requests without `Origin` remain allowed for local non-browser clients
  - Origin / Referer guard for state-changing requests
  - wildcard CORS blocked in local-only mode
  - yt-dlp option overrides and nightly auto updates require explicit unsafe
    escape hatches
  - non-local absolute public host URLs blocked in local-only mode
  - minimal security response headers added
  - controlled distribution is CLEAN portable local-only distribution, not
    public hosting, Cloudflare/public web deployment, or an external
    SaaS/service offering
  - no package output, dependency install/update, Docker, cookie/token/secret
    handling, public hosting, or safety gate changes
- Current Y-SEC-02 state:
  - completed via fork PR #83
  - merge commit: `e54058dc112ae6c29237738b21bff0e3253407ea`
  - `URL_INTAKE_GUARD=true` is default-on and must remain enabled when
    `LOCAL_ONLY_MODE=true`
  - dependency-free URL intake helper added in `app/local_only_security.py`
  - `/add` and `/subscribe` reject unsafe submitted URLs before enqueue or
    subscription creation
  - blocked targets include non-HTTP(S), malformed or missing-host URLs,
    URL userinfo, localhost/loopback, private/link-local/shared/multicast/
    reserved IP literals, IPv4-mapped IPv6 that points to blocked IPv4 ranges,
    obvious internal hostnames, and metadata hostnames
  - unsafe URL errors use a generic 400 reason and do not echo the submitted
    URL
  - DNS resolution is opt-in helper behavior only and is not enabled on the
    request path in this first pass
  - this does not claim complete DNS rebinding, downstream redirect, or
    yt-dlp-internal URL protection
  - dependency-free `unittest` passes with bundled Codex Python
  - focused pytest/aiohttp tests were added but not run here because `pytest`
    is unavailable and dependency installation was not performed
  - no package output, dependency install/update, Docker, frontend change,
    cookie/token/secret handling, real download, public hosting, or safety gate
    change
- Current Y-SEC-03 state:
  - completed via fork PR #84
  - merge commit: `aa0200b126d5cdc9d18617280fe733284bf990e6`
  - dependency-free privacy helpers added in `app/local_only_security.py`
  - URL log summaries remove userinfo, path details, query strings, and
    fragments
  - text redaction covers token-like key/value material, bearer authorization,
    cookies, and common local path material
  - non-empty `custom_name_prefix` values are sanitized before queue or
    subscription use
  - omitted or empty custom prefixes remain empty
  - unsafe URL errors remain generic and do not echo the submitted URL
  - downstream yt-dlp may still derive filenames internally; do not claim full
    final filename control
  - no package output, dependency install/update, Docker, frontend change,
    package/lockfile change, cookie/token/secret handling, real download,
    public hosting, or safety gate change
- Current Y-DIST-01 state:
  - completed via fork PR #85
  - merge commit: `f2e2678e3dc986a34f2e5bb0bd65f56d54b2b415`
  - report-only CLEAN portable distribution candidate checker added at
    `scripts/check_clean_distribution.py`
  - manifest contract added at
    `docs/llmwiki/clean-portable-distribution-manifest.md`
  - dependency-free unittest coverage added at
    `app/tests/test_clean_distribution_checker_unittest.py`
  - checker accepts only an explicit candidate directory and does not assume a
    generated package folder exists
  - checker blocks forbidden paths, obvious sensitive filenames, symlinks, and
    conservative secret-like content pattern families
  - reports path, line, and pattern family only for content findings; it does
    not print matched secret values or file contents
  - no CLEAN folder, ZIP, installer, package output, dependency install/update,
    Docker operation, real download, cookie/token/secret handling, frontend
    change, package/lockfile change, or existing safety gate behavior change
- Current Y-DIST-02 state:
  - report-only CLEAN portable distribution metadata checker added at
    `scripts/check_distribution_metadata.py`
  - metadata verification contract added at
    `docs/llmwiki/distribution-metadata-verification.md`
  - dependency-free unittest coverage added at
    `app/tests/test_distribution_metadata_checker_unittest.py`
  - checker requires candidate-root `VERSION.txt`, `MANIFEST.json`,
    `checksums.sha256`, `LICENSE`, and `NOTICE`
  - checker validates version shape, manifest fields, local-only distribution
    metadata, sha256sum-style checksum entries, recomputed SHA-256 matches,
    duplicate listed paths, missing listed files, unsafe checksum paths, and
    basic license / notice presence and safety
  - checker runs Y-DIST-01 as a prerequisite and includes those findings
  - no metadata generation, checksum generation, CLEAN folder, ZIP, installer,
    package output, dependency install/update, Docker operation, real download,
    cookie/token/secret handling, frontend change, package/lockfile change, or
    existing safety gate behavior change
- Next candidates:
  - `Y-DIST-03 recipient-safe runbook and first-run local-only verification`
  - `Y-SEC-04 CSP and frontend security header audit`
  - `Y-SEC-05 dependency / ffmpeg / yt-dlp version inventory and update review gate`
- Completed:
  - Y-08F generation readiness checklist preview via fork PR #70.
  - Y-08G readiness summary polish / advisory score refinement via fork PR #71.
  - Y-08Z preview hardening lane closeout via fork PR #72.
  - Y-UI-QUALITY-01 quality selector simple labels via fork PR #73.
  - Y-UI-QUALITY-01Z docs closeout via fork PR #74.
  - Y-UI-QUALITY-02 quality selector helper copy via fork PR #75.
  - Y-UI-QUALITY-02Z docs closeout via fork PR #76.
  - Y-UI-QUALITY-03 completed/result table quality label polish via fork PR
    #77.
  - Y-UI-QUALITY-03Z docs closeout via fork PR #78.
  - Y-UI-REVIEW-01 current UI review checklist via fork PR #79.
- PR #73 merge commit:
  `402996eba52f923be962e2fe69ebdaa6084363f2`.
- PR #74 merge commit:
  `708f2ca583b95bb25135e3463764ac547c75a084`.
- PR #75 merge commit:
  `eea1c861a62033b02255950491cd9e0f6ab2d77b`.
- PR #76 merge commit:
  `702cf9c231f21366267a9f3c181e90b6494ecb8e`.
- PR #77 merge commit:
  `c2f58fad237218d681414b51749bca6fe1bc734b`.
- PR #78 merge commit:
  `035ecce6f2c9964772bc6612ddba422309a73cd1`.
- PR #79 merge commit:
  `2c30cc28080e39949bb4a6ab8e646abb700ebfb1`.
- Y-UI-QUALITY-01 simplified visible video/audio quality labels while preserving
  numeric values, existing option ids, API payloads, backend validation, and
  download logic.
- Y-UI-QUALITY-02 clarified quality selector helper copy: video help now
  explains quality targets / upper limits, source-quality fallback, auto mode,
  and file-size tradeoff; audio help now explains audio quality / file-size
  tradeoff and auto mode; the audio selector label changed from `画質` to
  `音質`.
- Y-UI-QUALITY-02 preserved option ids, payloads, backend/API/download logic,
  validation, and yt-dlp selector behavior.
- Y-UI-QUALITY-03 polished completed/result table quality labels so they match
  selector wording, changed the result table column header from `画質` to
  `品質`, kept captions/thumbnails as `-`, preserved safe fallback behavior,
  and added focused UI spec coverage.
- Y-UI-QUALITY-03 preserved backend/API/download logic, option ids, payloads,
  validation, and yt-dlp selector behavior.
- PR #73, PR #75, and PR #77 were High-mid / human-reviewed frontend UI work
  because the current local safety aggregator forbids `ui/**`.
- This docs closeout does not weaken or modify the safety gate.
- Readiness preview remains report-only and advisory-only:
  - `overall: blocked`
  - `actual_generation_approved: false`
  - `score_basis: advisory_only`
  - `advisory_score: 23/100`
  - `approval_meaning: none`
- Actual generation remains blocked.
- No package output or `動画保存ツール_ローカル専用/` generated package folder should
  exist.
- Run preflight before the next task.
- Completed:
  - Y-UI-REVIEW-01 current UI review checklist.
  - Y-UI-REVIEW-02 screenshot review findings with partial static coverage.
- Current after this PR merges: `Y-UI-REVIEW-02R` rerun screenshot review is
  recorded docs-only.
- Review outcome: temporary screenshots with a local mock server captured the
  loaded form, video/audio helper popovers, audio mode, completed/result rows,
  video/audio quality labels, captions/thumbnail `-`, and narrow-width layout.
  No blocking UI findings were observed.
- Next: `Y-UI-REVIEW-02Z` review-complete closeout.
- Safety: no package generation, generated folder absent, frontend work remains
  human-reviewed, and safety gate policy changes remain separate.
- Frontend `ui/**` work remains human-reviewed unless safety gate policy is
  explicitly updated later.

## Read First

1. `docs/llmwiki/current-state.md`
2. `docs/llmwiki/safety-boundaries.md`
3. `docs/llmwiki/codex-automation-policy.md`
4. `docs/llmwiki/automation-efficiency-policy.md`
5. `docs/llmwiki/roadmap.md`
6. `docs/llmwiki/update-rollback-plan.md`
7. `docs/llmwiki/manual-update-apply-design.md`
8. `docs/llmwiki/dry-run-update-contract.md`
9. `docs/llmwiki/dockerless-desktop-distribution-feasibility.md`
10. `docs/llmwiki/desktop-sidecar-lifecycle-contract.md`
11. `docs/llmwiki/desktop-package-manifest.md`
12. `docs/llmwiki/beginner-guide-skeleton.md`
13. `docs/llmwiki/clean-package-dry-run-contract.md`
14. `docs/llmwiki/clean-package-generator-contract-addendum.md`
15. `docs/llmwiki/safety-gate-checker-design.md`
16. `docs/llmwiki/beginner-guide-source-plan.md`
17. `docs/llmwiki/license-notice-plan.md`
18. `docs/llmwiki/codex-gh-auth-runbook.md` if GitHub CLI auth, PR creation,
   checks, or merge commands fail inside Codex
19. `docs/llmwiki/preflight-environment-checker-design.md` before future
   preflight checker implementation work
20. `docs/llmwiki/privacy-redaction-security.md` before future log/error or
   filename privacy work

## Key Points For Codex

- Keep work local-only and personal-use scoped.
- Do not touch upstream PR #1001 unless explicitly asked.
- Do not mix `docker-compose.local.yml` or `docs/local-only.md` into fork-only work.
- Do not handle real cookies, tokens, secrets, DRM bypass, authentication bypass, or
  restriction circumvention.
- Y-AUTO-01 Codex automation policy is documented at
  `docs/llmwiki/codex-automation-policy.md`.
- Y-AUTO-06 automation efficiency policy is documented at
  `docs/llmwiki/automation-efficiency-policy.md`.
- Y-AUTO-06 allows same-risk, same-purpose one-PR scope expansion only when the
  lane scope and safety gates pass.
- Y-AUTO-07 adds codex lane execution rules in
  `docs/llmwiki/codex-auto-lanes.md`.
- Y-AUTO-06 defines Codex auto lanes A through E. Lane E is High-mid
  PR-ready-only and must not auto merge.
- Y-LOCAL-01 added `export_context_updated.py` to local `.git/info/exclude`.
  The helper remains uncommitted, undeleted, unmoved, and not listed in
  `.gitignore`.
- Y-AUTO-01 defines Low, Medium, High-low, High-mid, and High-high automation
  levels.
- Low and Medium work may use auto PR / auto merge when the current task scope
  and safety gates pass.
- High-low work may use auto PR / auto merge only when it remains docs-only,
  report-only, or dry-run-only and all mandatory gates pass.
- High-mid work may proceed through Codex implementation, verification, PR
  creation, and Ready-for-review handoff only when the task explicitly approves
  that scope.
- High-mid auto merge is prohibited. High-mid PRs must state
  `human-review-required`, and merge is allowed only after human confirmation.
- High-high work must stop before implementation and request explicit human
  confirmation.
- Y-AUTO-02 adds `Risk classification` to `scripts/check_repo_safety.py`.
- The checker now reports `tier`, `automation`, and `reason` while preserving
  existing `Status: OK` / `Status: BLOCKED` behavior.
- `auto-merge-ok` is advisory and valid only when the safety report has no
  blockers and the PR merge state / checks are clean.
- Y-AUTO-04 extends the checker so High-mid-like implementation-adjacent or
  generated-output-adjacent scopes report `automation: pr-only-human-merge`.
- When the checker reports `pr-only-human-merge`, do not auto merge. Prepare a
  Ready-for-review PR with `human-review-required` in the PR body.
- `update-status` is readonly. It must not apply updates, pull Docker images,
  run git updates, restart the app, or install packages.
- Backup and rollback requirements must be satisfied before any update-apply
  implementation begins.
- `update-preflight` is readonly. It reports backup / rollback readiness and
  must not execute updates, create backups, create rollback targets, pull Docker
  images, run git updates, restart the app, or install packages.
- Y-05G readonly update preflight report was merged in fork PR #7
  (`bfbecdb`).
- Y-05H manual-approval update apply design is docs-only. It defines future
  confirmation flow, stop conditions, rollback hand-off, and API/UI boundaries
  without approving update execution.
- Y-05I dry-run / prepare-only contract is docs-only. It defines dry-run as
  readonly planning only and prepare-only as validation only, with no backup or
  rollback creation in the first prepare stage.
- `update-plan` is readonly. It reports a blocked-by-default update plan with
  `can_prepare: false` and `can_apply: false`. It must not execute updates,
  prepare updates, create backups, create rollback targets, pull Docker images,
  run git updates, restart the app, or install packages.
- Y-05K-R runtime verification succeeded after Docker recovery. `/update-plan`
  returned `overall: blocked`, `can_prepare: false`, `can_apply: false`,
  non-empty `blocked_reasons`, non-empty `planned_steps`, and rollback/doc
  references. `/update-status` was `latest`; `/update-preflight` was
  `not_ready` with `can_apply_update: false`; `/version` reported
  `2026.06.06` and yt-dlp `2026.03.17`.
- Y-05 readonly update readiness is closed out for now. Update execution,
  prepare, apply, rollback, update buttons, backup creation, Docker pull, git
  pull / merge / rebase, restart, pip install, and package update remain out of
  scope.
- Y-06A Dockerless desktop distribution feasibility audit is documented in
  `docs/llmwiki/dockerless-desktop-distribution-feasibility.md`.
- Y-06A outcome: Dockerless Windows/macOS desktop distribution is feasible for
  local-only personal use, but not beginner-ready from the current repository
  state.
- Tauri is the preferred first candidate. Electron remains the fallback.
  WebView2 is Windows-only and not the primary cross-platform path.
- Key desktop blockers: backend sidecar lifecycle, close safety, desktop path
  defaults, ffmpeg / yt-dlp / Deno / bgutil packaging, signing/notarization, and
  excluding cookie/token/secret features from the beginner desktop flow.
- Y-06B desktop sidecar lifecycle and package contract is documented in
  `docs/llmwiki/desktop-sidecar-lifecycle-contract.md`.
- Y-06B outcome: the future desktop wrapper owns backend sidecar start,
  readiness, monitoring, stop, close confirmation, and abnormal-exit recovery.
- Future desktop launch must force `HOST=127.0.0.1`, use per-user
  download/state/temp paths, and keep runtime data out of the install
  directory.
- Package contents, package exclusions, Windows/macOS boundaries, and beginner
  `.html` / `.txt` guide requirements are contract-defined, but no
  implementation or packaging is approved yet.
- Y-06C desktop package manifest is documented in
  `docs/llmwiki/desktop-package-manifest.md`.
- Y-06C beginner guide skeleton is documented in
  `docs/llmwiki/beginner-guide-skeleton.md`.
- Y-06C outcome: future package root is `動画保存ツール_ローカル専用/`, with
  `00_最初に開いてください.html` as the primary beginner guide,
  `00_最初に開いてください.txt` as fallback, and `.md` material reserved for
  developer/LLMwiki use.
- Windows and macOS package skeletons, include/exclude rules, generated
  manifest candidates, user data paths, notices, checksums, and safe beginner
  copy boundaries are defined. No generated distribution folder, package
  generator, implementation, package build, or installer is approved yet.
- Y-06D clean-package generator dry-run contract is documented in
  `docs/llmwiki/clean-package-dry-run-contract.md`.
- Y-06D outcome: dry-run is report-only planning before any package files are
  copied or generated. The contract defines future command candidates,
  JSON/Markdown report shape, exit code policy, warning/error/blocked
  classifications, planned output manifest, include/exclude rules, validation
  gates, output examples, and the next implementation candidate.
- Future dry-run validation must block forbidden paths, forbidden filenames,
  forbidden content pattern families, generated package folders, PR #1001 file
  leakage, cookie/token/secret handling, public hosting, ads, update apply,
  Docker pull, git update, package install/update, and unrelated implementation
  behavior.
- Y-06E report-only clean-package dry-run script is implemented at
  `scripts/clean_package_dry_run.py`.
- Y-06E outcome: the script prints a sanitized text report for the planned
  `動画保存ツール_ローカル専用/` package root, planned top-level / Windows /
  macOS / developer entries, excluded path rules, validation checks, safety
  flags, and blocker details.
- Y-06E exit codes are `0` for OK, `1` for blockers, and `2` for CLI usage
  errors. JSON/Markdown report modes remain future candidates.
- Y-06E remains dry-run only. It does not create the package root, copy files,
  zip files, build packages, install dependencies, add Tauri/Electron/WebView2,
  change backend/frontend/Docker/CI/package/lockfile files, or implement update
  apply.
- Y-06F beginner guide source and license notice review is documented in
  `docs/llmwiki/beginner-guide-source-plan.md` and
  `docs/llmwiki/license-notice-plan.md`.
- Y-06F outcome: future beginner guide source candidates are defined for
  first-open, usage, troubleshooting, safe-use, and TXT fallback pages.
- Y-06F outcome: license/notice planning covers MeTube, yt-dlp, ffmpeg, Python
  runtime, Python dependencies, frontend runtime dependencies, and future
  Tauri/Electron runtime pieces only if they are later implemented and bundled.
- Y-06F remains docs-only. It does not create `.html` / `.txt` guide files,
  copy license text, generate notice bundles, change the dry-run script, create
  the package root, build packages, add Tauri/Electron/WebView2, change
  backend/frontend/Docker/CI/package/lockfile files, or implement update apply.
- The selected next PR candidate is to add non-blocking missing guide-source
  and missing notice-source warnings to `scripts/clean_package_dry_run.py`.
- Y-06G clean-package dry-run guide/notice warning hardening is implemented in
  `scripts/clean_package_dry_run.py`.
- Y-06G outcome: the dry-run now reports nonblocking warnings for missing
  beginner guide source candidates, missing license/notice source candidates,
  missing local-only safety notice source candidates, and missing Windows/macOS
  section source coverage.
- Y-06G warning-only runs keep `Status: OK` and exit code `0`.
- Y-06G preserves existing blockers for generated package folder presence,
  forbidden filename families, secret-like content findings, and PR #1001
  leakage.
- Y-06G does not create guide files, copy license text, generate notice bundles,
  create the package root, build packages, add Tauri/Electron/WebView2, change
  backend/frontend/Docker/CI/package/lockfile files, or implement update apply.
- Y-06H first beginner guide source draft is documented at
  `docs/llmwiki/package-guides/00-first-open.html.source.md`.
- Y-06H outcome: the first-open HTML source candidate is Japanese-first,
  source-only, local-only, and structured for future HTML conversion with hero
  copy, first-step cards, a warning box, in-app help cards, troubleshooting
  cards, and a footer note.
- Y-06H covers start, URL paste, save, open save folder, stop/quit, allowed-use
  boundaries, no public hosting/ads/credential sharing, no DRM/auth/restriction
  bypass, and the `停止して終了` close-safety note.
- Y-06H does not create actual `.html` / `.txt` files, generated package
  folders, package build/copy behavior, notice bundles, Tauri/Electron/WebView2
  implementation, backend/frontend/Docker/CI/package/lockfile changes, or
  update apply.
- Y-06I first-open TXT fallback source draft is documented at
  `docs/llmwiki/package-guides/00-first-open.txt.source.md`.
- Y-06I outcome: the first-open TXT source candidate is shorter than the HTML
  source, readable in a normal text editor, source-only, local-only, and focused
  on the first-use flow.
- Y-06I covers what the tool is, start, URL paste, save, open save folder,
  stop/quit, allowed-use boundaries, no public hosting/ads/credential sharing,
  no DRM/auth/restriction bypass, troubleshooting entry points, and the hand-off
  to `00_最初に開いてください.html`.
- Y-06I does not create actual `.html` / `.txt` files, generated package
  folders, package build/copy behavior, notice bundles, Tauri/Electron/WebView2
  implementation, backend/frontend/Docker/CI/package/lockfile changes, or
  update apply.
- Y-06J how-to-use HTML guide source draft is documented at
  `docs/llmwiki/package-guides/03-how-to-use.html.source.md`.
- Y-06J outcome: the everyday-use HTML source candidate is Japanese-first,
  source-only, local-only, and structured for future HTML conversion with hero
  copy, quick steps, action cards, format cards, status cards, a warning box,
  troubleshooting link cards, and a footer note.
- Y-06J covers start, URL paste, save-format selection, save, open save folder,
  status reading, retry guidance, stop/quit, allowed-use boundaries, no public
  hosting/ads/credential sharing, and no DRM/auth/restriction bypass.
- Y-06J does not create actual `.html` / `.txt` files, generated package
  folders, package build/copy behavior, notice bundles, Tauri/Electron/WebView2
  implementation, backend/frontend/Docker/CI/package/lockfile changes, or
  update apply.
- Y-06K how-to-use TXT fallback source draft is documented at
  `docs/llmwiki/package-guides/03-how-to-use.txt.source.md`.
- Y-06K outcome: the everyday-use TXT source candidate is shorter than the HTML
  source, readable in a normal text editor, source-only, local-only, and focused
  on what to press during the save flow.
- Y-06K covers basic save steps, save-format choices, saving/completion
  behavior, stop/quit behavior, allowed-use boundaries, no public
  hosting/ads/credential sharing, no DRM/auth/restriction bypass, and the
  hand-off to `03_使い方.html`.
- Y-06K does not create actual `.html` / `.txt` files, generated package
  folders, package build/copy behavior, notice bundles, Tauri/Electron/WebView2
  implementation, backend/frontend/Docker/CI/package/lockfile changes, or
  update apply.
- Y-06L troubleshooting HTML source draft is documented at
  `docs/llmwiki/package-guides/04-troubleshooting.html.source.md`.
- Y-06L outcome: the troubleshooting HTML source candidate is Japanese-first,
  source-only, local-only, and structured for future HTML conversion with hero
  copy, a quick checklist, trouble cards, a warning box, a safe-use reminder,
  and a footer note.
- Y-06L covers first checks, common trouble cases, gentle error messages,
  save-folder guidance, stop/quit behavior, update-display uncertainty,
  allowed-use boundaries, no public hosting/ads/credential sharing, and no
  DRM/auth/restriction bypass.
- Y-06L does not create actual `.html` / `.txt` files, generated package
  folders, package build/copy behavior, notice bundles, Tauri/Electron/WebView2
  implementation, backend/frontend/Docker/CI/package/lockfile changes, or
  update apply.
- Y-06M troubleshooting TXT fallback source draft is documented at
  `docs/llmwiki/package-guides/04-troubleshooting.txt.source.md`.
- Y-06M outcome: the troubleshooting TXT source candidate is shorter than the
  HTML source, readable in a normal text editor, source-only, local-only, and
  focused on what to do next when something fails.
- Y-06M covers first actions, common trouble cases, stop/quit behavior,
  allowed-use boundaries, no public hosting/ads/credential sharing, no
  DRM/auth/restriction bypass, and the hand-off to `04_困ったとき.html`.
- Y-06M does not create actual `.html` / `.txt` files, generated package
  folders, package build/copy behavior, notice bundles, Tauri/Electron/WebView2
  implementation, backend/frontend/Docker/CI/package/lockfile changes, or
  update apply.
- Y-06N safe-use HTML source draft is documented at
  `docs/llmwiki/package-guides/05-safe-use.html.source.md`.
- Y-06N outcome: the safe-use HTML source candidate is Japanese-first,
  source-only, local-only, and structured for future HTML conversion with hero
  copy, safe-use cards, do / do-not cards, a sensitive-data warning box, an
  update-safety note, and a footer note.
- Y-06N covers local-only personal use, allowed examples, prohibited uses,
  sensitive-data sharing boundaries, safe trouble actions, update safety, no
  public hosting/ads/external service, no update apply, and no
  DRM/auth/restriction bypass.
- Y-06N does not create actual `.html` / `.txt` files, generated package
  folders, package build/copy behavior, notice bundles, Tauri/Electron/WebView2
  implementation, backend/frontend/Docker/CI/package/lockfile changes, or
  update apply.
- Y-06O MeTube notice source draft is documented at
  `docs/llmwiki/package-notices/metube-notice.source.md`.
- Y-06O outcome: the MeTube notice source candidate is source-only,
  sanitized, and review-oriented for a future
  `動画保存ツール_ローカル専用/開発者向け/notices/MeTube-notice.txt`.
- Y-06O covers future notice / license placement candidates, component summary,
  short beginner-facing license pointer, developer-facing notice draft,
  manifest candidate fields, required future review, and no-private-data
  notice hygiene.
- Y-06O does not create actual notice files, copy license text, generate notice
  bundles, create generated package folders, add Tauri/Electron/WebView2,
  change backend/frontend/Docker/CI/package/lockfile files, or implement update
  apply.
- Y-06P yt-dlp notice source draft is documented at
  `docs/llmwiki/package-notices/yt-dlp-notice.source.md`.
- Y-06P outcome: the yt-dlp notice source candidate is source-only,
  sanitized, and review-oriented for a future
  `動画保存ツール_ローカル専用/開発者向け/notices/yt-dlp-notice.txt`.
- Y-06P covers local dependency candidates from `pyproject.toml`, `uv.lock`,
  and previous runtime `/version` verification; official project and package
  source URL candidates; a short beginner-facing notice pointer; developer
  notice draft; manifest candidate fields; and future review for extras and
  transitive dependency notices.
- Y-06P does not create actual notice files, copy license text, generate notice
  bundles, create generated package folders, install or update yt-dlp, add
  Tauri/Electron/WebView2, change backend/frontend/Docker/CI/package/lockfile
  files, or implement 更新適用機能.
- Y-06Q FFmpeg notice source draft is documented at
  `docs/llmwiki/package-notices/ffmpeg-notice.source.md`.
- Y-06Q outcome: the FFmpeg notice source candidate is source-only, sanitized,
  and review-oriented for a future
  `動画保存ツール_ローカル専用/開発者向け/notices/ffmpeg-notice.txt`.
- Y-06Q covers OS-specific notice placement candidates for Windows and macOS,
  local FFmpeg usage candidates, official FFmpeg source / legal URL
  candidates, a beginner-facing notice pointer, developer notice draft,
  manifest candidate fields, and future review for selected binary provider,
  version, build configuration, license status, source availability, and
  patent-sensitive/nonfree options.
- Y-06Q does not create actual notice files, copy license text, generate notice
  bundles, create generated package folders, install or update FFmpeg, choose a
  binary provider, add Tauri/Electron/WebView2, change
  backend/frontend/Docker/CI/package/lockfile files, or implement 更新適用機能.
- Y-06R Python runtime notice source draft is documented at
  `docs/llmwiki/package-notices/python-runtime-notice.source.md`.
- Y-06R outcome: the Python runtime notice source candidate is source-only,
  sanitized, and review-oriented for a future
  `動画保存ツール_ローカル専用/開発者向け/notices/python-runtime-notice.txt`.
- Y-06R covers OS-specific runtime notice placement candidates for Windows and
  macOS, local runtime candidates from `pyproject.toml`, `Dockerfile`, and
  Dockerless package planning docs, official Python source / license URL
  candidates, a beginner-facing notice pointer, developer notice draft,
  manifest candidate fields, and future review for exact runtime artifact,
  standard-library incorporated software, native libraries, bundler runtime
  pieces, and bundled Python dependency notices.
- Y-06R does not create actual notice files, copy license text, generate notice
  bundles, create generated package folders, install/build/update Python, choose
  a runtime artifact, add PyInstaller spec files, add Tauri/Electron/WebView2,
  change backend/frontend/Docker/CI/package/lockfile files, or implement
  更新適用機能.
- Y-06S frontend dependency notice source draft is documented at
  `docs/llmwiki/package-notices/frontend-deps-notice.source.md`.
- Y-06S outcome: the frontend dependency notice source candidate is
  source-only, sanitized, and review-oriented for a future
  `動画保存ツール_ローカル専用/開発者向け/notices/frontend-deps-notice.txt`.
- Y-06S covers read-only local candidate sources from `ui/package.json` and
  `ui/pnpm-lock.yaml`, frontend runtime dependency candidates,
  developer/build-tool dependency candidates, package / lockfile review
  candidates, beginner-facing notice copy, developer notice draft, manifest
  candidate fields, future generated notice-bundle requirements, and review
  checklist items.
- Y-06S does not create actual notice files, copy license text, generate notice
  bundles, create generated package folders, build frontend assets, change
  package or lock files, change dependencies, run package manager operations,
  add Tauri/Electron/WebView2, change backend/frontend/Docker/CI/package files,
  or implement 更新適用機能.
- Y-06T desktop shell notice source draft is documented at
  `docs/llmwiki/package-notices/desktop-shell-notice.source.md`.
- Y-06T outcome: the desktop shell notice source candidate is source-only,
  sanitized, and review-oriented for a future
  `動画保存ツール_ローカル専用/開発者向け/notices/desktop-shell-notice.txt`.
- Y-06T covers shared and OS-specific notice placement candidates, Tauri,
  Electron, WebView2 direct host, and native launcher candidate notes,
  official reference candidates for later recheck, beginner-facing notice copy,
  developer notice draft, manifest candidate fields, future generated
  notice-bundle requirements, and review checklist items.
- Y-06T does not create actual notice files, copy license text, generate notice
  bundles, create generated package folders, implement Tauri, implement
  Electron, implement WebView2, add installer behavior, add signing or
  notarization behavior, change package or lock files, change dependencies, run
  package manager operations, change backend/frontend/Docker/CI/package files,
  or implement 更新適用機能.
- Y-06U bundled Python dependency inventory source draft is documented at
  `docs/llmwiki/package-notices/bundled-python-dependency-inventory.source.md`.
- Y-06U outcome: the bundled Python/backend dependency inventory source
  candidate is source-only, sanitized, and review-oriented for future
  `動画保存ツール_ローカル専用/開発者向け/inventory/bundled-python-dependency-inventory.json`
  and related Python dependency notice / license review output.
- Y-06U covers read-only dependency source files inspected, runtime dependency
  candidates, developer-only dependency candidates, optional / indirect
  dependency candidates, manifest candidate fields, license review checklist,
  notice bundle review checklist, legal-not-final boundary, and future
  generated inventory requirements.
- Y-06U records `pyproject.toml` and `uv.lock` as present local dependency
  sources; records Poetry, requirements, setup, Pipenv, Conda environment,
  constraints, tox, and nox dependency source files as not present.
- Y-06U does not create generated inventory files, actual notice files, copy
  license text, generate notice bundles, create generated package folders,
  change package or lock files, change dependencies, run package manager
  operations, run dependency install/update/audit/build/package commands,
  change backend/frontend/Docker/CI/package files, handle cookie/token/secret
  values, touch PR #1001 files, or implement 更新適用機能.
- Y-06V notice source index draft is documented at
  `docs/llmwiki/package-notices/notice-source-index.source.md`.
- Y-06V outcome: the notice / license / dependency inventory source index is
  source-only, sanitized, and review-oriented for future clean-package notice
  bundle planning.
- Y-06V read-only checks the existing MeTube, yt-dlp, FFmpeg, Python runtime,
  frontend dependency, desktop shell, and bundled Python dependency inventory
  source drafts.
- Y-06V covers source file inventory, future output mapping for aggregate
  notices, license directories, manifests, beginner guide notice sections, and
  developer review checklist items, review status vocabulary, unresolved
  questions, future generated notice-bundle requirements, and no-generation
  boundaries.
- Y-06V does not create generated notice bundles, generated license bundles,
  generated inventory files, generated manifest files, generated package
  folders, HTML/TXT guide output, change package or lock files, change
  dependencies, run package manager operations, run dependency
  install/update/audit/build/package commands, change
  backend/frontend/Docker/CI/package files, handle cookie/token/secret values,
  touch PR #1001 files, or implement 更新適用機能.
- Y-06W clean package generator contract addendum is documented at
  `docs/llmwiki/clean-package-generator-contract-addendum.md`.
- Y-06W outcome: the notice source index is defined as a future generator input
  candidate for dry-run / preview review across `NOTICE.txt`, `LICENSES/`,
  `manifest.json`, beginner guide notice sections, and developer review
  checklist items.
- Y-06W also defines no-generation boundaries, generated artifact exclusion,
  cookie/token/secret value non-disclosure, output diff prediction candidates,
  package manifest preview candidates, cleanup / rollback candidates, human
  review gates, risk boundaries, and future implementation phases.
- Y-06W does not create generated package folders, notice bundles, license
  bundles, inventory files, manifest files, HTML/TXT guide output, build /
  package / install behavior, dependency changes, package/lockfile changes,
  backend/frontend/Docker/CI changes, cookie/token/secret handling, PR #1001
  file changes, or 更新適用機能.
- Y-06X package manifest preview is implemented in
  `scripts/clean_package_dry_run.py`.
- Y-06X outcome: the clean-package dry-run text report now includes a
  `Package manifest preview` section with package name/type candidates,
  `local_only: true`, `generated_artifacts: false`, notice source count/list,
  guide source count/list, excluded path summary, future output candidates,
  human review requirement before generation, legal-final status,
  non-disclosure flags, and a no-generation boundary note.
- Y-06X preserves existing dry-run `Status: OK`, warnings, blockers, exit-code
  behavior, and no-files-generated behavior.
- Y-06X does not create `manifest.json`, generated package folders, notice
  bundles, license bundles, inventory files, manifest files, HTML/TXT guide
  output, build / package / install behavior, dependency changes,
  package/lockfile changes, backend/frontend/Docker/CI changes,
  cookie/token/secret handling, PR #1001 file changes, or 更新適用機能.
- Y-06Y package output diff prediction is implemented in
  `scripts/clean_package_dry_run.py`.
- Y-06Y outcome: the clean-package dry-run text report now includes a
  `Package output diff prediction` section with the future package root
  candidate, would-create directory and file candidates, would-copy source
  groups, future output candidates, excluded path summary,
  currently-present excluded path count, no-files-generated state, human review
  requirement before generation, and cleanup / rollback candidate note.
- Y-06Y preserves existing dry-run `Status: OK`, warnings, blockers,
  `Package manifest preview`, exit-code behavior, and no-files-generated
  behavior.
- Y-06Y does not create `manifest.json`, `NOTICE.txt`, `LICENSES/`, generated
  package folders, notice bundles, license bundles, inventory files, manifest
  files, HTML/TXT guide output, build / package / install behavior, dependency
  changes, package/lockfile changes, backend/frontend/Docker/CI changes,
  cookie/token/secret handling, PR #1001 file changes, or 更新適用機能.
- Y-06Z clean package dry-run Markdown report mode design is documented at
  `docs/llmwiki/clean-package-dry-run-markdown-report-mode-design.md`.
- Y-06Z outcome: future Markdown report mode should keep text output as the
  default, prefer `--format markdown` as the first future selector, and produce
  PR/handoff-friendly sections for Summary, Status, Risk Classification,
  Package Manifest Preview, Package Output Diff Prediction, Notice / Guide
  Source Coverage, Excluded Paths Summary, Blockers, Warnings, Human Review
  Checklist, and No-Generation Boundary.
- Y-06Z also defines PR body reuse, handoff reuse, safety boundaries, future
  implementation checklist, future verification checklist, cleanup / rollback
  note, and High-low / High-mid boundary.
- Y-06Z is docs-only. It does not change `scripts/clean_package_dry_run.py` or
  `scripts/check_repo_safety.py`, implement JSON or Markdown output, create
  `manifest.json`, `NOTICE.txt`, `LICENSES/`, generated package folders,
  notice bundles, license bundles, inventory files, manifest files, HTML/TXT
  guide output, ビルド/パッケージ/インストール操作, dependency changes,
  package/lockfile changes, backend/frontend/Docker/CI changes,
  cookie/token/secret handling, PR #1001 file changes, or 更新適用機能.
- Y-07A clean package dry-run JSON report mode design is documented at
  `docs/llmwiki/clean-package-dry-run-json-report-mode-design.md`.
- Y-07A outcome: future JSON report mode should keep text output as the
  default, prefer `--format json` as the first future selector, and write one
  valid JSON object to stdout only in its first implementation.
- Y-07A defines structured top-level data for repository, package, planned
  entries, package manifest preview, package output diff prediction, excluded
  paths, checks, warnings, blocked reasons, safety flags, risk classification
  relationship, no-generation boundary, and next step.
- Y-07A also defines schema compatibility guidance, PR/handoff reuse guidance,
  safety boundaries, future implementation checklist, future verification
  checklist, cleanup / rollback note, and High-low / High-mid boundary.
- Y-07A is docs-only. It does not change `scripts/clean_package_dry_run.py` or
  `scripts/check_repo_safety.py`, implement JSON or Markdown output, write
  report files, create `manifest.json`, `NOTICE.txt`, `LICENSES/`, generated
  package folders, notice bundles, license bundles, inventory files, manifest
  files, HTML/TXT guide output, ビルド/パッケージ/インストール操作,
  dependency changes, package/lockfile changes, backend/frontend/Docker/CI
  changes, cookie/token/secret handling, PR #1001 file changes, automation
  wrapper / CI / PR-comment integration, or 更新適用機能.
- Y-07B clean package dry-run Markdown report mode is implemented in
  `scripts/clean_package_dry_run.py`.
- Y-07B outcome: default text output and `--format text` remain available, and
  `--format markdown` now prints a stdout-only Markdown report.
- Y-07B Markdown output includes Summary, Status, Risk Classification, Package
  Manifest Preview, Package Output Diff Prediction, Notice / Guide Source
  Coverage, Excluded Paths Summary, Blockers, Warnings, Human Review
  Checklist, and No-Generation Boundary sections.
- Y-07B preserves existing blockers, warnings, exit codes, and sanitized
  finding output.
- Verify Y-07B with `scripts/clean_package_dry_run.py`,
  `scripts/clean_package_dry_run.py --format text`, and
  `scripts/clean_package_dry_run.py --format markdown`.
- `export_context_updated.py` is a known local-only WebGPT handoff/context
  export helper. It remains untracked and outside Y-07B scope.
- Y-07B does not implement JSON output, write report files, create generated
  package folders, create package output, change backend/frontend/Docker/CI
  files, change package/lockfile files, handle cookie/token/secret values,
  touch PR #1001 files, or implement 更新適用機能.
- Y-07C clean package dry-run JSON report mode is implemented in
  `scripts/clean_package_dry_run.py`.
- Y-07C outcome: default text output, `--format text`, and `--format markdown`
  remain available, and `--format json` now prints one valid JSON object to
  stdout.
- Y-07C JSON output is report-only, machine-readable, sanitized, and includes
  repository, package, package manifest preview, package output diff
  prediction, source coverage, excluded path summary, validation, warnings,
  blockers, safety flags, human review, and next-step fields.
- Y-07C preserves existing blockers, warnings, exit codes, and sanitized
  finding output.
- Verify Y-07C with `scripts/clean_package_dry_run.py`,
  `scripts/clean_package_dry_run.py --format text`,
  `scripts/clean_package_dry_run.py --format markdown`,
  `scripts/clean_package_dry_run.py --format json`, and a `json.loads()` parse
  check over the full JSON stdout.
- `export_context_updated.py` is a known local-only WebGPT handoff/context
  export helper. It remains untracked and outside Y-07C scope.
- Y-07C does not write report files, create generated package folders, create
  package output, change backend/frontend/Docker/CI files, change
  package/lockfile files, handle cookie/token/secret values, touch PR #1001
  files, or implement 更新適用機能.
- Y-07D clean-package dry-run report regression contract is documented at
  `docs/llmwiki/clean-package-dry-run-report-regression-contract.md`.
- Y-07D outcome: the contract records the current default text,
  `--format text`, `--format markdown`, and `--format json` report modes.
- Y-07D fixes the required Markdown sections, required JSON top-level fields,
  cross-format consistency rules, exit-code behavior, warning/blocker
  invariants, sanitization rules, no-generation boundary, verification matrix,
  PR review checklist, stop conditions, rollback note, and High-low /
  High-mid boundary.
- Y-07D is docs-only. It does not change scripts, implement tests, add CI,
  write report files, create generated package folders, create package output,
  change backend/frontend/Docker/CI files, change package/lockfile files,
  handle cookie/token/secret values, touch PR #1001 files, or implement
  更新適用機能.
- Future recommended candidate: Y-07E lightweight regression checks for report
  modes, if explicitly approved, or pause and move to the next report-only
  package preview/planning task.
- `export_context_updated.py` is a known local-only WebGPT handoff/context
  export helper. It remains untracked and outside Y-07D scope.
- Y-07E lightweight clean-package dry-run report regression checker is
  implemented at `scripts/check_clean_package_dry_run_reports.py`.
- Y-07E outcome: the checker runs default text, `--format text`,
  `--format markdown`, and `--format json`, validates the Y-07D text,
  Markdown, JSON, cross-format, and no-generation contracts, and prints a
  sanitized human-readable report.
- Verify Y-07E with `scripts/check_clean_package_dry_run_reports.py`,
  `scripts/check_repo_safety.py`,
  `scripts/check_repo_safety.py --base fork/master`, and
  `scripts/clean_package_dry_run.py`.
- Y-07E does not change `scripts/clean_package_dry_run.py`, change
  `scripts/check_repo_safety.py`, add CI wiring, write report files, create
  generated package folders, create package output, change
  backend/frontend/Docker/CI files, change package/lockfile files, handle
  cookie/token/secret values, touch PR #1001 files, or implement 更新適用機能.
- Y-08A clean package preview hardening design is documented at
  `docs/llmwiki/clean-package-preview-hardening-design.md`.
- Y-08A outcome: docs-only package preview hardening design for the existing
  clean-package dry-run reports after text, Markdown, JSON, and regression
  checker stabilization.
- Y-08A defines richer manifest preview field candidates, package output diff
  prediction grouping candidates, source coverage statuses, notice/license/
  inventory mappings, beginner guide output mappings, and developer review
  checklist mappings.
- Y-08A does not change scripts, add tests, add CI, write report files, create
  generated package folders, create package output, change
  backend/frontend/Docker/CI files, change package/lockfile files, handle
  cookie/token/secret values, touch PR #1001 files, or implement 更新適用機能.
- Future recommended candidate: Y-08B richer manifest preview entries in
  report-only / stdout-only mode, if explicitly approved. Optional later CI
  wiring for the Y-07E checker remains separate.
- `export_context_updated.py` is a known local-only WebGPT handoff/context
  export helper. It remains untracked and outside Y-08A scope.
- Y-08B richer manifest preview entries are implemented in
  `scripts/clean_package_dry_run.py`.
- Y-08B outcome: text, Markdown, and JSON package manifest preview output now
  includes manifest entry candidates.
- Y-08B JSON output includes `manifest_entries` and
  `manifest_entry_summary` under `package_manifest_preview`.
- Y-08B checker coverage is implemented in
  `scripts/check_clean_package_dry_run_reports.py`.
- Verify Y-08B with `scripts/check_clean_package_dry_run_reports.py`, normal
  repo safety gates, and the clean-package dry-run text, Markdown, and JSON
  modes.
- Y-08B does not create an actual `manifest.json`, write report files, create
  generated package folders, create package output, change
  backend/frontend/Docker/CI files, change package/lockfile files, handle
  cookie/token/secret values, touch PR #1001 files, or implement 更新適用機能.
- Recommended candidate after Y-08B: Y-08C richer output diff prediction
  grouping in report-only / stdout-only mode. Optional later CI wiring for the
  Y-07E checker remains separate.
- `export_context_updated.py` is a known local-only WebGPT handoff/context
  export helper. It remains untracked and outside Y-08B scope.
- Y-08C richer output diff prediction grouping is implemented in
  `scripts/clean_package_dry_run.py`.
- Y-08C outcome: text, Markdown, and JSON package output diff prediction output
  now includes output group candidates.
- Y-08C JSON output includes `output_groups` and `output_group_summary` under
  `package_output_diff_prediction`.
- Y-08C checker coverage is implemented in
  `scripts/check_clean_package_dry_run_reports.py`.
- Verify Y-08C with `scripts/check_clean_package_dry_run_reports.py`, normal
  repo safety gates, and the clean-package dry-run text, Markdown, and JSON
  modes.
- Y-08C does not write report files, create generated package folders, create
  package output, change backend/frontend/Docker/CI files, change
  package/lockfile files, handle cookie/token/secret values, touch PR #1001
  files, or implement 更新適用機能.
- Recommended candidate after Y-08C: Y-08D source coverage status hardening in
  report-only / stdout-only mode. Optional later CI wiring for the Y-07E
  checker remains separate.
- `export_context_updated.py` is a known local-only WebGPT handoff/context
  export helper. It remains untracked and outside Y-08C scope.
- Y-08D source coverage status hardening is implemented in
  `scripts/clean_package_dry_run.py`.
- Y-08D outcome: text, Markdown, and JSON source coverage output now includes
  coverage item candidates and a coverage summary.
- Y-08D JSON output includes `coverage_items` and `coverage_summary` under
  `source_coverage`.
- Y-08D checker coverage is implemented in
  `scripts/check_clean_package_dry_run_reports.py`.
- Verify Y-08D with `scripts/check_clean_package_dry_run_reports.py`, normal
  repo safety gates, and the clean-package dry-run text, Markdown, and JSON
  modes.
- Y-08D does not write report files, create generated package folders, create
  package output, change backend/frontend/Docker/CI files, change
  package/lockfile files, handle cookie/token/secret values, touch PR #1001
  files, or implement 更新適用機能.
- Recommended candidate after Y-08D: Y-08E package generation readiness
  checklist in docs-only or report-only mode. Optional later CI wiring for the
  Y-07E checker remains separate.
- `export_context_updated.py` is a known local-only WebGPT handoff/context
  export helper. It remains untracked and outside Y-08D scope.
- Y-08E generation readiness checklist design is documented at
  `docs/llmwiki/clean-package-generation-readiness-checklist.md`.
- Y-08E outcome: docs-only readiness gates now cover reports, source coverage,
  manifest preview, output diff prediction, notices/licenses/inventory,
  beginner guides, runtime/desktop shell, security/privacy, cleanup/rollback,
  and human review.
- Y-08E confirms that passing dry-run previews does not approve actual
  generation.
- Y-08E does not change scripts, add tests, add CI, write report files, create
  generated package folders, create package output, change
  backend/frontend/Docker/CI files, change package/lockfile files, handle
  cookie/token/secret values, touch PR #1001 files, or implement 更新適用機能.
- Follow-up implemented by Y-08F generation readiness checklist preview.
- Actual package generation remains blocked.
- `export_context_updated.py` is a known local-only WebGPT handoff/context
  export helper. It remains untracked and outside Y-08E scope.
- Y-08F generation readiness checklist preview is implemented in
  `scripts/clean_package_dry_run.py`.
- Y-08F outcome: text and Markdown output now include `Generation Readiness
  Preview`, and JSON output includes top-level `generation_readiness`.
- Y-08F keeps `generation_readiness.overall: blocked`,
  `actual_generation_approved: false`, and `score_basis: advisory_only`.
- Y-08F checker coverage is implemented in
  `scripts/check_clean_package_dry_run_reports.py`.
- Verify Y-08F with `scripts/check_clean_package_dry_run_reports.py`, normal
  repo safety gates, and the clean-package dry-run text, Markdown, and JSON
  modes.
- Y-08F does not write report files, create generated package folders, create
  package output, change backend/frontend/Docker/CI files, change
  package/lockfile files, handle cookie/token/secret values, touch PR #1001
  files, or implement 更新適用機能.
- Recommended candidate after Y-08F: Y-08G readiness summary polish / advisory
  score refinement in report-only / stdout-only mode. Implemented by Y-08G.
- Actual package generation remains blocked.
- `export_context_updated.py` is a known local-only WebGPT handoff/context
  export helper. It remains untracked and outside Y-08F scope.
- Y-08G readiness summary polish / advisory score refinement is implemented in
  `scripts/clean_package_dry_run.py`.
- Y-08G outcome: text and Markdown output now include readiness summary polish
  with `advisory_score: 23/100`; JSON output includes
  `generation_readiness.advisory_score` and
  `generation_readiness.readiness_summary`.
- The advisory score is review-only, has `approval_meaning: none`, and does
  not approve generation.
- Y-08G keeps `generation_readiness.overall: blocked`,
  `actual_generation_approved: false`, and `score_basis: advisory_only`.
- Y-08G checker coverage is implemented in
  `scripts/check_clean_package_dry_run_reports.py`.
- Verify Y-08G with `scripts/check_clean_package_dry_run_reports.py`, normal
  repo safety gates, and the clean-package dry-run text, Markdown, and JSON
  modes.
- Y-08G does not write report files, create generated package folders, create
  package output, change backend/frontend/Docker/CI files, change
  package/lockfile files, handle cookie/token/secret values, touch PR #1001
  files, or implement 更新適用機能.
- Follow-up after Y-08G: Y-08Z preview hardening closeout, completed by this
  PR. Optional later CI wiring for the Y-07E checker remains separate.
- Next practical candidate after Y-08Z: Y-UI-QUALITY-01 quality selector simple
  labels with numeric values.
- Actual package generation remains blocked.
- `export_context_updated.py` is a known local-only WebGPT handoff/context
  export helper. It remains untracked and outside Y-08G scope.
- Y-CHECK-01 safety gate checker design is documented at
  `docs/llmwiki/safety-gate-checker-design.md`.
- Y-CHECK-01 outcome: the future checker should evaluate repository diffs for
  changed-file scope, forbidden paths, secret-like pattern families, generated
  distribution folder presence, upstream PR #1001 file leakage, dangerous
  behavior, update execution, package guide / notice completeness warnings,
  LLMwiki consistency, and a sanitized PR safety summary.
- Y-CHECK-01 is docs-only. It does not implement a checker script, automation
  gate, CI integration, PR bot/comment automation, package generation, generated
  distribution folder, backend/frontend/Docker/CI/package/lockfile changes,
  update execution, or cookie/token/secret handling.
- Y-CHECK-02 repo safety check script is implemented at
  `scripts/check_repo_safety.py`.
- Y-CHECK-02 outcome: the script is stdlib-only and report-only. It checks the
  current working tree diff by default, including untracked files, and supports
  optional `--base` diff context such as `fork/master`.
- Y-CHECK-02 checks changed-file scope, forbidden paths, generated distribution
  folder presence, upstream PR #1001 leakage, secret-like changed content,
  dangerous behavior patterns, required LLMwiki basics, and package
  guide/notice source warnings.
- Y-CHECK-02 reports secret-like findings only as path, line, and pattern
  family. It does not print matched values.
- Y-CHECK-02 does not implement automation gate behavior, CI integration, PR
  bot/comment automation, package generation, generated distribution folders,
  backend/frontend/Docker/CI/package/lockfile changes, update execution, or
  cookie/token/secret value output.
- Y-AUTO-02 extends Y-CHECK-02 with report-only risk classification. For the
  checker enhancement itself, the report shows `tier: Medium` and
  `automation: auto-merge-ok`.
- Y-AUTO-03 expands Codex execution scope to High-mid PR-ready work. It does not
  allow High-mid auto merge.
- High-mid PR bodies must explain why the work is High-mid, what was not
  performed, rollback/cleanup candidates, remaining risk, and verification.
- Y-AUTO-05 confirms the High-mid PR body dry-run template requirements:
  `Risk tier: High-mid`, `Automation decision: PR-ready only`,
  `automation: pr-only-human-merge`, `human-review-required`,
  `Why High-mid`, `Explicitly not performed`, `Verification`,
  `Rollback / cleanup candidates`, `Residual risks`, and
  `Human review checklist`.
- Y-AUTO-04 makes the checker surface High-mid PR-only guidance directly in the
  `Risk classification` section.
- Latest work: Y-LOCAL-01 local helper exclude, Y-AUTO-06 docs-only automation
  efficiency policy, and Y-AUTO-07 codex auto lanes docs.
- Next recommended automation candidate: Y-AUTO-08 safety gate aggregator design.
- GitHub CLI auth note: in this Windows Codex desktop environment, sandboxed
  `gh auth status` may report an invalid `default` token while escalated
  `gh auth status` succeeds through `keyring`. Root cause is sandbox access to
  the Windows keyring, not project state. For PR create/view/checks/merge work,
  verify escalated `gh auth status` and then use narrowly scoped escalated `gh`
  commands. Do not read, paste, or store token values.

## Next Step

Use `docs/llmwiki/current-state.md`, `docs/llmwiki/roadmap.md`, and this handoff
as the next-chat source of truth.

Recommended next candidates:

```text
Y-DIST-03 recipient-safe runbook and first-run local-only verification
Y-SEC-04 CSP and frontend security header audit
Y-SEC-05 dependency / ffmpeg / yt-dlp version inventory and update review gate
```

Alternative:

```text
pause for human review of Y-DIST-02
```

Use the `Risk classification` section from `scripts/check_repo_safety.py`
before auto PR or auto merge, then cross-check
`docs/llmwiki/codex-automation-policy.md` and
`docs/llmwiki/automation-efficiency-policy.md` for High-low, High-mid,
High-high, or Unknown outcomes.

For High-mid outcomes, stop after PR-ready handoff and wait for human review
before merge.

Frontend `ui/**` work remains human-reviewed unless a later policy PR explicitly
updates the local safety gate and automation policy. Do not modify safety gate
behavior or broaden auto-merge policy inside this closeout.

Run `scripts/check_repo_safety.py`,
`scripts/check_repo_safety.py --base fork/master`, and
`scripts/clean_package_dry_run.py` before the next low-, medium-, or qualifying
high-low-risk fork PR.

The Y-08 package-material lane is closed by Y-08Z. Y-UI-QUALITY-01,
Y-UI-QUALITY-01Z, Y-UI-QUALITY-02, Y-UI-QUALITY-02Z, and Y-UI-QUALITY-03 are
complete. Optional later CI wiring for the Y-07E checker remains separate.

Later clean-package work should resume as Y-09 human-reviewed generation
prototype planning only, not actual generation. Keep Y-09 blocked unless later
human-reviewed approval is given.

Do not create generated guide outputs, copy license text, create the generated
package folder, copy package files, implement actual package generation, add
Tauri/Electron/WebView2, run builds, install dependencies, change
backend/frontend/Docker/CI files, change package/lockfile files, implement
update execution, handle cookie/token/secret values, or add Y-CHECK automation /
CI / PR bot behavior yet.

Actual package generation remains blocked.

Safety-gate support for frontend copy-only or label-only lanes should remain a
separate policy/checker task, not bundled into this closeout.

## Y-AUTO-08 Handoff Update

Latest completed work: Y-AUTO-08 added the docs-only local safety gate aggregator design at `docs/llmwiki/local-safety-gate-aggregator-design.md`.

Read this design before starting Y-AUTO-09. It defines the manual gate baseline, future command candidate, execution model, Python runtime notes, scope checks, PR #1001 leakage checks, sanitization rules, exit-code contract, and stop conditions.

Next recommended work:

- Y-AUTO-09: implement `scripts/run_local_safety_gates.py` as a stdlib-only, read-only text-output wrapper for existing gates.
- Y-AUTO-10: add PR-body usage guidance for aggregator output after Y-AUTO-09.
- Y-AUTO-11: refine scope presets only after the aggregator is stable.

Carry forward these constraints:

- Do not create `動画保存ツール_ローカル専用/`.
- Do not touch PR #1001 files unless the task explicitly targets that PR.
- Do not change scripts, app, UI, Docker, CI, package files, lockfiles, or `.gitignore` during docs-only work.
- Keep `export_context_updated.py` local-only through `.git/info/exclude`; do not add it to commits.
- Actual package generation remains blocked until a later explicit human-reviewed task.
## Y-AUTO-09 Handoff Update

Latest work: Y-AUTO-09 safety gate aggregator implementation.

New command:

```powershell
python scripts/run_local_safety_gates.py --base fork/master
```

Use the bundled Codex Python executable if `python` is not available on PATH.

Next recommended candidate: Y-AUTO-10 PR body generator design.

Carry forward:

- `export_context_updated.py` remains locally excluded and uncommitted.
- Actual package generation remains blocked.
- The aggregator does not replace underlying gates or authorize higher-risk work.
## Y-AUTO-10A Handoff Update

Latest work: Y-AUTO-10A safety wording checker design.

New design doc:

```text
docs/llmwiki/safety-wording-checker-design.md
```

Next recommended candidate: Y-AUTO-10B safety wording checker implementation.

Aggregator command remains available:

```powershell
python scripts/run_local_safety_gates.py --base fork/master
```

Carry forward:

- `export_context_updated.py` remains locally excluded and uncommitted.
- Actual package generation remains blocked.
- The wording checker must not weaken repo safety gates or authorize higher-risk work.
## Y-AUTO-10B Handoff Update

Latest work: Y-AUTO-10B safety wording checker implementation.

New command:

```powershell
python scripts/check_safety_wording.py --base fork/master
```

Aggregator command remains:

```powershell
python scripts/run_local_safety_gates.py --base fork/master
```

Next recommended candidate: Y-AUTO-12 PR body generator stdout-only implementation.

Carry forward:

- `export_context_updated.py` remains locally excluded and uncommitted.
- Actual package generation remains blocked.
- The wording checker does not replace repo safety gates or authorize higher-risk work.
## Y-AUTO-11 Handoff Update

Latest work: Y-AUTO-11 PR body generator design.

New design doc:

```text
docs/llmwiki/pr-body-generator-design.md
```

Next recommended candidate: Y-AUTO-12 PR body generator stdout-only
implementation.

Available commands:

```powershell
python scripts/run_local_safety_gates.py --base fork/master
python scripts/check_safety_wording.py --base fork/master
```

Carry forward:

- `export_context_updated.py` remains locally excluded and uncommitted.
- Actual generation remains blocked.
- The future PR body generator must not replace safety gates or approve merge.

## Y-AUTO-12 Handoff Update

Latest work: Y-AUTO-12 PR body generator stdout-only implementation.

New command:

```powershell
python scripts/generate_pr_body.py --title "..." --risk high-low --scope docs-only
```

Available commands:

```powershell
python scripts/run_local_safety_gates.py --base fork/master
python scripts/check_safety_wording.py --base fork/master
```

Next recommended candidate: Y-AUTO-13 Codex prompt templates.

Carry forward:

- `export_context_updated.py` remains locally excluded and uncommitted.
- Actual generation remains blocked.
- The PR body generator does not replace safety gates or approve merge.

## Y-AUTO-13 Handoff Update

Latest work: Y-AUTO-13 Codex prompt templates.

Added:

```text
docs/llmwiki/codex-run-prompt-templates.md
```

The new doc provides reusable Codex prompt templates for docs-only,
report-only, checker-only, combined, High-mid PR-ready-only, human-reviewed
merge, recovery, closeout, and new app bootstrap workflows.

Available commands:

```powershell
python scripts/run_local_safety_gates.py --base fork/master
python scripts/check_safety_wording.py --base fork/master
python scripts/generate_pr_body.py --title "..." --risk high-low --scope docs-only
```

Next recommended candidate: APP-BOOT-01 new app bootstrap template design if
starting a new app workflow, or Y-AUTO-14 preflight environment checker design
if continuing tooling hardening.

Carry forward:

- `export_context_updated.py` remains locally excluded and uncommitted.
- Actual generation remains blocked.
- Prompt templates do not replace safety gates or authorize higher risk.

## Y-AUTO-14 Handoff Update

Latest work: Y-AUTO-14 preflight environment checker design.

Added:

```text
docs/llmwiki/preflight-environment-checker-design.md
```

The new doc defines a future readiness-only checker for Python runtime
discovery, Git metadata access, GitHub CLI session state, local helper
exclusion, generated package folder absence, PR #1001 leakage precheck, and
local safety tool availability.

Follow-up implemented by Y-AUTO-15. APP-BOOT-01 remains the next recommended
candidate.

Available commands:

```powershell
python scripts/run_local_safety_gates.py --base fork/master
python scripts/check_safety_wording.py --base fork/master
python scripts/generate_pr_body.py --title "..." --risk high-low --scope docs-only
```

Carry forward:

- `export_context_updated.py` remains locally excluded and uncommitted.
- Actual generation remains blocked.
- Y-AUTO-15 implements the preflight checker.
- The preflight checker will not replace safety gates or authorize higher risk.

## Y-AUTO-15 Handoff Update

Latest work: Y-AUTO-15 preflight environment checker implementation.

New command:

```powershell
python scripts/check_local_dev_environment.py --base fork/master --expected-branch master
```

Available commands:

```powershell
python scripts/run_local_safety_gates.py --base fork/master
python scripts/check_safety_wording.py --base fork/master
python scripts/generate_pr_body.py --title "..." --risk high-low --scope docs-only
```

Next recommended candidate: APP-BOOT-01 new app bootstrap template design.

Carry forward:

- `export_context_updated.py` remains locally excluded and uncommitted.
- Actual generation remains blocked.
- The preflight checker is readiness-only and does not replace safety gates.

## APP-BOOT-01 Handoff Update

Latest work: APP-BOOT-01 new app bootstrap template design.

New design doc:

```text
docs/llmwiki/new-app-bootstrap-template-design.md
```

Available commands:

```powershell
python scripts/check_local_dev_environment.py --base fork/master --expected-branch master
python scripts/run_local_safety_gates.py --base fork/master
python scripts/check_safety_wording.py --base fork/master
python scripts/generate_pr_body.py --title "..." --risk high-low --scope docs-only
```

Next recommended candidate:

- APP-BOOT-02 if building a reusable skeleton packet.
- APP-00A if starting the actual new app's purpose/MVP definition.

Carry forward:

- `export_context_updated.py` remains locally excluded and uncommitted.
- Actual generation remains blocked.
- APP-BOOT-01 does not create a new app or authorize implementation.
