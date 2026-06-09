# Handoff

## Short Context

This is `youtubeダウンロード / MeTube local-only fork`, a personal local-only fork of
MeTube. The canonical branch is fork `master`, and local `master` tracks
`fork/master`.

## Read First

1. `docs/llmwiki/current-state.md`
2. `docs/llmwiki/safety-boundaries.md`
3. `docs/llmwiki/roadmap.md`
4. `docs/llmwiki/update-rollback-plan.md`
5. `docs/llmwiki/manual-update-apply-design.md`
6. `docs/llmwiki/dry-run-update-contract.md`
7. `docs/llmwiki/dockerless-desktop-distribution-feasibility.md`
8. `docs/llmwiki/desktop-sidecar-lifecycle-contract.md`
9. `docs/llmwiki/desktop-package-manifest.md`
10. `docs/llmwiki/beginner-guide-skeleton.md`
11. `docs/llmwiki/clean-package-dry-run-contract.md`
12. `docs/llmwiki/safety-gate-checker-design.md`
13. `docs/llmwiki/beginner-guide-source-plan.md`
14. `docs/llmwiki/license-notice-plan.md`
15. `docs/llmwiki/codex-gh-auth-runbook.md` if GitHub CLI auth, PR creation,
   checks, or merge commands fail inside Codex

## Key Points For Codex

- Keep work local-only and personal-use scoped.
- Do not touch upstream PR #1001 unless explicitly asked.
- Do not mix `docker-compose.local.yml` or `docs/local-only.md` into fork-only work.
- Do not handle real cookies, tokens, secrets, DRM bypass, authentication bypass, or
  restriction circumvention.
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
- GitHub CLI auth note: in this Windows Codex desktop environment, sandboxed
  `gh auth status` may report an invalid `default` token while escalated
  `gh auth status` succeeds through `keyring`. Root cause is sandbox access to
  the Windows keyring, not project state. For PR create/view/checks/merge work,
  verify escalated `gh auth status` and then use narrowly scoped escalated `gh`
  commands. Do not read, paste, or store token values.

## Next Step

Use `scripts/check_repo_safety.py` before the next low- or medium-risk fork PR.

The previous package-material next step remains available: draft
`docs/llmwiki/package-notices/yt-dlp-notice.source.md` as the next notice source
candidate for future clean-package notice review.

Do not create generated guide outputs, copy license text, create the generated
package folder, copy package files, implement actual package generation, add
Tauri/Electron/WebView2, run builds, install dependencies, change
backend/frontend/Docker/CI files, change package/lockfile files, implement
update execution, handle cookie/token/secret values, or add Y-CHECK automation /
CI / PR bot behavior yet.
