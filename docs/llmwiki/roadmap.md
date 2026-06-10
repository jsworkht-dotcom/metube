# Roadmap

## Immediate Next

### Y-AUTO-11 PR body generator design outcome

- Design document:
  `docs/llmwiki/pr-body-generator-design.md`
- Added docs-only design for a future stdout-only PR body generator.
- Defined required PR body sections, risk templates, explicitly not-performed
  presets, verification templates, local helper note rules, human review rules,
  safety wording rules, CLI shape, output format, exit code contract,
  sanitization rules, integration boundaries, stop conditions, and rollback
  notes.
- The generator remains a future task and must not replace safety gates,
  approve merge, call the GitHub API, create PRs, edit PRs, write PR body
  files by default, or create package output.

### Next automation candidates

- Y-AUTO-12 PR body generator stdout-only implementation.
- Y-AUTO-13 Codex prompt templates.
- APP-BOOT-01 new app bootstrap template design.
- APP-BOOT-02 bootstrap skeleton.

Actual package generation remains blocked.

### Existing gate policy reminders

- Read the `Risk classification` section from
  `scripts/check_repo_safety.py` before auto PR or auto merge.
- Cross-check the tier against `docs/llmwiki/codex-automation-policy.md` when
  the report says `High-low`, `High-mid`, `High-high`, or `Unknown`.
- If the report says `High-mid` with `automation: pr-only-human-merge`, prepare
  a Ready-for-review PR only and do not auto merge.
- High-mid PR bodies must include `Risk tier: High-mid`, `Automation decision:
  PR-ready only`, `automation: pr-only-human-merge`,
  `human-review-required`, `Why High-mid`, `Explicitly not performed`,
  `Verification`, `Rollback / cleanup candidates`, `Residual risks`, and
  `Human review checklist`.
- Run `scripts/check_repo_safety.py` and
  `scripts/check_repo_safety.py --base fork/master` before the next low-,
  medium-, or qualifying high-low-risk fork PR.
- Run `scripts/clean_package_dry_run.py` for package-adjacent high-low work and
  for this local-only package planning stream.
- Keep the scripts report-only / dry-run-only.
- For High-mid work, allow Codex implementation, verification, PR creation, and
  Ready-for-review handoff only when the task explicitly approves that scope.
- For High-mid work, keep auto merge disabled and require human review before
  merge.
- Keep any automation wrapper, CI integration, PR comment automation, or
  generated package behavior as a later explicitly approved task.
- Keep package generation, update execution, dependency install/update, Docker
  pull, backend/frontend/Docker/CI changes, package/lockfile changes,
  generated distribution folders, and cookie/token/secret handling out of
  scope unless explicitly approved.

## Y-AUTO-05 High-mid PR Template Dry-Run Policy Check Outcome

- Policy documents now require the High-mid PR body template to show
  `Risk tier: High-mid`, `Automation decision: PR-ready only`,
  `automation: pr-only-human-merge`, and `human-review-required`.
- The template includes reviewer sections for why the task is High-mid, what was
  explicitly not performed, verification, rollback/cleanup candidates,
  residual risks, and a human review checklist.
- The checker guidance remains report-only and continues to classify
  High-mid-like scopes as `automation: pr-only-human-merge`.
- This Y-AUTO-05 check is docs/checker-policy only. It does not add a real
  High-mid implementation, generated distribution folder, generated notice
  bundle, HTML/TXT guide output, build/package/install command, dependency
  change, package/lockfile change, backend/frontend/Docker/CI change,
  cookie/token/secret handling, public hosting, ads, or PR #1001 file changes.

### Next package-material candidate

- Y-08E completes generation readiness checklist design in this PR.
- The next recommended package-material candidate is Y-08F generation readiness
  checklist preview in report-only mode, if explicitly approved.
- Optional later CI wiring for the Y-07E checker remains separate.
- Keep the next PR report-only, dry-run-only, or source-material only unless
  explicitly approved otherwise.
- Do not create guide outputs, copy license text, generate notice bundles,
  generate manifests, or create package files.
- Do not create `動画保存ツール_ローカル専用/`, copy files, build packages, install
  dependencies, add Tauri/Electron/WebView2, change backend/frontend/Docker/CI,
  or change package/lockfile files.

## Y-AUTO-06 Automation Efficiency Policy Outcome

- Policy document:
  `docs/llmwiki/automation-efficiency-policy.md`
- Added docs-only automation efficiency policy for safe one-PR scope expansion,
  Codex auto lanes, local helper handling, closeout PRs, and future automation
  candidates.
- Documented `export_context_updated.py` as a local-only WebGPT
  handoff/context export helper tracked through `.git/info/exclude`.
- Recorded future candidates:
  - Y-AUTO-08 safety gate aggregator design
  - Y-AUTO-09 safety gate aggregator implementation
  - Y-AUTO-10 PR body generator design
  - Y-AUTO-11 PR body generator stdout-only implementation
  - Y-AUTO-12 Codex run prompt templates
  - Y-AUTO-13 worktree operation design
  - Y-AUTO-14 stop condition checker design
- Actual package generation remains blocked.
- This Y-AUTO-06 PR does not change scripts, add tests, add CI, write report
  files, create generated distribution folders, create package output, run
  ビルド/パッケージ/インストール操作, change dependencies, change
  package/lockfile files, change backend/frontend/Docker/CI files, handle
  cookie/token/secret values, touch PR #1001 files, or implement 更新適用機能.

## Y-08E Generation Readiness Checklist Design Outcome

- Document:
  `docs/llmwiki/clean-package-generation-readiness-checklist.md`
- Added a docs-only readiness checklist for future clean-package generation
  work.
- The checklist defines gates for reports, source coverage, manifest preview,
  output diff prediction, notices/licenses/inventory, beginner guides,
  runtime/desktop shell, security/privacy, cleanup/rollback, and human review.
- It clarifies that passing dry-run previews does not approve generation.
- Future recommended candidate: Y-08F generation readiness checklist preview
  in report-only mode, if explicitly approved.
- Actual package generation remains blocked.
- This Y-08E PR does not change scripts, add tests, add CI, write report files,
  create generated distribution folders, create package output, run
  ビルド/パッケージ/インストール操作, change dependencies, change
  package/lockfile files, change backend/frontend/Docker/CI files, handle
  cookie/token/secret values, touch PR #1001 files, or implement 更新適用機能.

## Y-08D Source Coverage Status Hardening Outcome

- Scripts:
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_clean_package_dry_run_reports.py`
- Added report-only source coverage status preview to the clean-package dry-run
  source coverage section.
- Text, Markdown, and JSON output now expose coverage items and summary data.
- JSON includes `source_coverage.coverage_items` and
  `source_coverage.coverage_summary`.
- Coverage covers guide, notice, license, inventory, runtime selection, desktop
  shell, and manifest source categories.
- The regression checker validates coverage item fields, statuses, required
  categories, text marker, Markdown section, and JSON summary.
- Future recommended candidate after Y-08D: Y-08E package generation readiness
  checklist in docs-only or report-only mode.
- Actual package generation remains blocked.
- This Y-08D PR does not create package output, write report files, create
  generated distribution folders, run ビルド/パッケージ/インストール操作,
  change dependencies, change package/lockfile files, change
  backend/frontend/Docker/CI files, handle cookie/token/secret values, touch PR
  #1001 files, or implement 更新適用機能.

## Y-08C Richer Output Diff Prediction Grouping Outcome

- Scripts:
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_clean_package_dry_run_reports.py`
- Added report-only output group candidates to the clean-package dry-run
  package output diff prediction.
- Text, Markdown, and JSON output now expose the richer group set.
- JSON includes `package_output_diff_prediction.output_groups` and
  `package_output_diff_prediction.output_group_summary`.
- The regression checker validates the output group fields, required group
  keys, text marker, Markdown section, and JSON summary.
- Future recommended candidate after Y-08C: Y-08D source coverage status
  hardening in report-only / stdout-only mode.
- Actual package generation remains blocked.
- This Y-08C PR does not create package output, write report files, create
  generated distribution folders, run ビルド/パッケージ/インストール操作,
  change dependencies, change package/lockfile files, change
  backend/frontend/Docker/CI files, handle cookie/token/secret values, touch PR
  #1001 files, or implement 更新適用機能.

## Y-08B Richer Manifest Preview Entries Outcome

- Scripts:
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_clean_package_dry_run_reports.py`
- Added report-only manifest entry candidates to the clean-package dry-run
  package manifest preview.
- Text, Markdown, and JSON output now expose the richer candidate set.
- JSON includes `package_manifest_preview.manifest_entries` and
  `package_manifest_preview.manifest_entry_summary`.
- The regression checker validates the manifest entry fields and the new
  text/Markdown markers.
- Future recommended candidate after Y-08B: Y-08C implement richer output diff
  prediction grouping in report-only / stdout-only mode.
- Actual package generation remains blocked.
- This Y-08B PR does not create an actual `manifest.json`, write report files,
  create generated distribution folders, create package output, run
  ビルド/パッケージ/インストール操作, change dependencies, change
  package/lockfile files, change backend/frontend/Docker/CI files, handle
  cookie/token/secret values, touch PR #1001 files, or implement 更新適用機能.

## Y-08A Package Preview Hardening Design Outcome

- Design:
  `docs/llmwiki/clean-package-preview-hardening-design.md`
- Added a docs-only design for hardening existing clean-package preview
  reports.
- Documented current preview strengths and gaps for package manifest preview,
  package output diff prediction, and source coverage.
- Defined future manifest entry field candidates, output diff grouping
  candidates, source coverage status vocabulary, notice/license/inventory
  mapping, beginner guide output mapping, and developer review checklist
  mapping.
- Future recommended candidate: Y-08B implement richer manifest preview entries
  in report-only / stdout-only mode, if explicitly approved.
- Actual package generation remains blocked.
- This Y-08A PR does not change scripts, add tests, add CI, write report files,
  create generated distribution folders, create package output, run
  ビルド/パッケージ/インストール操作, change dependencies, change
  package/lockfile files, change backend/frontend/Docker/CI files, handle
  cookie/token/secret values, touch PR #1001 files, or implement 更新適用機能.

## Y-07E Report Regression Checker Outcome

- Script:
  `scripts/check_clean_package_dry_run_reports.py`
- Added a stdlib-only checker for clean-package dry-run report modes.
- The checker runs default text, `--format text`, `--format markdown`, and
  `--format json`.
- It validates text mode remains text, Markdown required sections are present,
  JSON parses as one object, JSON required top-level fields are present, simple
  cross-format status/warnings/blockers consistency holds, and no generated
  package folder exists.
- The checker prints a sanitized human-readable report and exits `0` when all
  checks pass, `1` when regressions are found, and `2` for usage errors.
- Y-08A next package preview/report-only planning is now complete in this PR.
- Future recommended candidate: Y-08B richer manifest preview entries in
  report-only / stdout-only mode, if explicitly approved.
- Optional later CI wiring for the checker remains separate.
- Actual package generation remains blocked.
- This Y-07E PR does not change `scripts/clean_package_dry_run.py`, change
  `scripts/check_repo_safety.py`, add CI wiring, write report files, create
  generated distribution folders, create package output, run
  ビルド/パッケージ/インストール操作, change dependencies, change
  package/lockfile files, change backend/frontend/Docker/CI files, handle
  cookie/token/secret values, touch PR #1001 files, or implement 更新適用機能.

## Y-07D Report Regression Contract Outcome

- Contract:
  `docs/llmwiki/clean-package-dry-run-report-regression-contract.md`
- Added a docs-only regression contract for clean-package dry-run report modes.
- Records the current default text, `--format text`, `--format markdown`, and
  `--format json` behavior.
- Documents required Markdown sections and JSON top-level fields.
- Defines cross-format consistency rules, exit-code behavior,
  warning/blocker invariants, sanitization rules, no-generation boundaries,
  verification matrix, stop conditions, rollback note, and High-low /
  High-mid boundary.
- Future recommended candidate: Y-07E lightweight regression checks for report
  modes, if explicitly approved, or pause and move to the next package
  preview/report-only planning task.
- Actual package generation remains blocked.
- This Y-07D PR does not change scripts, implement tests, add CI, write report
  files, create generated distribution folders, create package output, run
  ビルド/パッケージ/インストール操作, change dependencies, change
  package/lockfile files, change backend/frontend/Docker/CI files, handle
  cookie/token/secret values, touch PR #1001 files, or implement 更新適用機能.

## Y-07C JSON Report Mode Outcome

- Script:
  `scripts/clean_package_dry_run.py`
- Added `--format json` to the clean-package dry-run report.
- Preserved the default text report, `--format text`, and `--format markdown`
  behavior.
- JSON output is stdout-only, report-only, parseable as one valid JSON object,
  and uses sanitized machine-readable fields for repository, package, package
  manifest preview, package output diff prediction, source coverage, excluded
  paths, validation, warnings, blockers, safety flags, human review, and next
  step.
- Existing blockers, warnings, exit codes, generated artifact exclusion, and
  sanitized finding output are preserved.
- This Y-07C PR does not write report files, create `manifest.json`,
  `NOTICE.txt`, `LICENSES/`, generated distribution folders, notice bundles,
  license bundles, inventory files, manifest files, HTML/TXT guide output,
  ビルド/パッケージ/インストール操作, dependency changes, package/lockfile
  changes, backend/frontend/Docker/CI changes, cookie/token/secret handling,
  public hosting, ads, PR #1001 file changes, or 更新適用機能.

## Y-07B Markdown Report Mode Outcome

- Script:
  `scripts/clean_package_dry_run.py`
- Added `--format markdown` to the clean-package dry-run report.
- Preserved the default text report and `--format text` behavior.
- Markdown output is stdout-only, report-only, and includes Summary, Status,
  Risk Classification, Package Manifest Preview, Package Output Diff
  Prediction, Notice / Guide Source Coverage, Excluded Paths Summary,
  Blockers, Warnings, Human Review Checklist, and No-Generation Boundary
  sections.
- Existing blockers, warnings, exit codes, generated artifact exclusion, and
  sanitized finding output are preserved.
- This Y-07B PR does not implement JSON output, write report files, create
  `manifest.json`, `NOTICE.txt`, `LICENSES/`, generated distribution folders,
  notice bundles, license bundles, inventory files, manifest files, HTML/TXT
  guide output, ビルド/パッケージ/インストール操作, dependency changes,
  package/lockfile changes, backend/frontend/Docker/CI changes,
  cookie/token/secret handling, public hosting, ads, PR #1001 file changes, or
  更新適用機能.

## Y-07A JSON Report Mode Design Outcome

- Design:
  `docs/llmwiki/clean-package-dry-run-json-report-mode-design.md`
- Added a docs-only design for a future JSON report mode in
  `scripts/clean_package_dry_run.py`.
- Recommends `--format json` as the first future selector and keeps current
  text output as the default.
- Defines a one-object stdout JSON shape with top-level keys for repository,
  package, planned entries, package manifest preview, package output diff
  prediction, excluded paths, checks, warnings, blocked reasons, safety flags,
  risk classification relationship, no-generation boundary, and next step.
- Defines schema compatibility guidance, PR/handoff reuse guidance, safety
  boundaries, future implementation checklist, future verification checklist,
  cleanup / rollback note, and High-low / High-mid boundary.
- This Y-07A PR does not change scripts, implement JSON or Markdown output,
  write report files, create `manifest.json`, `NOTICE.txt`, `LICENSES/`,
  generated distribution folders, notice bundles, license bundles, inventory
  files, manifest files, HTML/TXT guide output,
  ビルド/パッケージ/インストール操作, dependency changes, package/lockfile
  changes, backend/frontend/Docker/CI changes, cookie/token/secret handling,
  public hosting, ads, PR #1001 file changes, automation wrapper / CI /
  PR-comment integration, or 更新適用機能.

## Y-06Z Markdown Report Mode Design Outcome

- Design:
  `docs/llmwiki/clean-package-dry-run-markdown-report-mode-design.md`
- Added a docs-only design for a future Markdown report mode in
  `scripts/clean_package_dry_run.py`.
- Recommends `--format markdown` as the first future selector and keeps current
  text output as the default.
- Defines Markdown sections for Summary, Status, Risk Classification, Package
  Manifest Preview, Package Output Diff Prediction, Notice / Guide Source
  Coverage, Excluded Paths Summary, Blockers, Warnings, Human Review
  Checklist, and No-Generation Boundary.
- Defines PR body reuse, handoff reuse, safety boundaries, future
  implementation checklist, future verification checklist, cleanup / rollback
  note, and High-low / High-mid boundary.
- This Y-06Z PR does not change scripts, implement JSON or Markdown output,
  create `manifest.json`, `NOTICE.txt`, `LICENSES/`, generated distribution
  folders, notice bundles, license bundles, inventory files, manifest files,
  HTML/TXT guide output, ビルド/パッケージ/インストール操作, dependency changes,
  package/lockfile changes, backend/frontend/Docker/CI changes,
  cookie/token/secret handling, public hosting, ads, PR #1001 file changes, or
  更新適用機能.

## Y-06Y Package Output Diff Prediction Outcome

- Script:
  `scripts/clean_package_dry_run.py`
- Added a report-only `Package output diff prediction` section to the
  clean-package dry-run text output.
- The prediction reports the future package root candidate, would-create
  directory candidates, would-create file candidates, would-copy source groups,
  future output candidates, excluded path summary, currently-present excluded
  path count, no-files-generated state, human review requirement before
  generation, and cleanup / rollback candidate note.
- Existing dry-run status, blockers, warnings, package manifest preview, and
  no-files-generated behavior remain unchanged.
- This Y-06Y PR does not create `manifest.json`, `NOTICE.txt`, `LICENSES/`,
  generated distribution folders, notice bundles, license bundles, inventory
  files, manifest files, HTML/TXT guide output, build/package/install commands,
  dependency changes, package/lockfile changes, backend/frontend/Docker/CI
  changes, cookie/token/secret handling, public hosting, ads, PR #1001 file
  changes, or 更新適用機能.

## Y-06X Package Manifest Preview Outcome

- Script:
  `scripts/clean_package_dry_run.py`
- Added a report-only `Package manifest preview` section to the clean-package
  dry-run text output.
- The preview reports package name/type candidates, `local_only: true`,
  `generated_artifacts: false`, notice source count/list, guide source
  count/list, excluded path summary, future output candidates, human review
  requirement before generation, legal-final status, non-disclosure flags, and
  a no-generation boundary note.
- Existing dry-run status, blockers, warnings, and no-files-generated behavior
  remain unchanged.
- This Y-06X PR does not create `manifest.json`, generated distribution
  folders, notice bundles, license bundles, inventory files, manifest files,
  HTML/TXT guide output, build/package/install commands, dependency changes,
  package/lockfile changes, backend/frontend/Docker/CI changes,
  cookie/token/secret handling, public hosting, ads, PR #1001 file changes, or
  更新適用機能.

## Y-06W Clean Package Generator Contract Addendum Outcome

- Addendum:
  `docs/llmwiki/clean-package-generator-contract-addendum.md`
- The addendum treats `docs/llmwiki/package-notices/notice-source-index.source.md`
  as a future generator input candidate for dry-run / preview review.
- It defines preview checks for `NOTICE.txt`, `LICENSES/`, `manifest.json`,
  beginner guide notice sections, developer review checklist items, output diff
  prediction, package manifest preview, cleanup / rollback candidates, and
  human review gates.
- It keeps actual generation behind later explicit human approval and preserves
  High-low / High-mid / High-high boundaries.
- This Y-06W PR is docs-only / no-generation. It does not add generated
  distribution folders, notice bundles, license bundles, inventory files,
  manifest files, HTML/TXT guide output, build/package/install commands,
  dependency changes, package/lockfile changes, backend/frontend/Docker/CI
  changes, cookie/token/secret handling, public hosting, ads, PR #1001 file
  changes, or 更新適用機能.

## Y-AUTO-04 High-mid Checker Guidance Outcome

- Script:
  `scripts/check_repo_safety.py`
- Added High-mid-like path / filename detection for implementation-adjacent and
  generated-output-adjacent scopes.
- High-mid-like scopes now report `automation: pr-only-human-merge` when no
  blockers are present.
- High-mid-like reasons include auto-merge-disabled guidance, human review
  requirement, and the `human-review-required` PR body requirement.
- Known report-only checker and clean-package dry-run script changes still
  classify as `Medium` with `automation: auto-merge-ok`.
- Existing `Status: OK` / `Status: BLOCKED` behavior and blocker checks are
  unchanged.
- This Y-AUTO-04 PR itself is a report-only checker improvement with minimal
  LLMwiki sync and does not add generated distribution folders, generated notice
  bundles, generated guide output, package output, build/package/install
  commands, dependency changes, package/lockfile changes,
  backend/frontend/Docker/CI changes, cookie/token/secret handling, public
  hosting, ads, PR #1001 file changes, or 更新適用機能.

## Y-AUTO-03 High-mid PR-Ready Policy Outcome

- Policy document:
  `docs/llmwiki/codex-automation-policy.md`
- Clarified High-mid as PR-ready work:
  - Codex may implement, verify, create a PR, and mark it ready for review when
    the task explicitly approves the High-mid scope.
  - Auto merge is prohibited.
  - Merge is limited to human confirmation after review.
  - High-mid PRs must state `human-review-required`.
  - High-mid PR bodies must include why the work is High-mid, what was not
    performed, rollback/cleanup candidates, remaining risk, and verification.
- Added High-mid examples covering generation scripts, desktop scaffolds,
  launcher prototypes, backend sidecar lifecycle prototypes, save/open folder
  UI, stop/exit UI, close confirmation UI, package output staging logic,
  generated artifact cleanup scripts, and OS-specific launcher-adjacent scripts.
- Kept package/lockfile changes and dependency install/update as stop
  conditions. Docker pull/build is prohibited and remains a stop condition.
- Backend download/queue/yt-dlp/extractor changes, cookie/token/secret
  handling, public hosting, ads, real distribution output, ZIP/package/installer
  output, and generated artifacts from verification also remain stop conditions
  unless separately human-approved.
- This Y-AUTO-03 PR itself is docs-only and did not add generated distribution
  folders, generated notice bundles, generated guide output, package output,
  build/package/install commands, dependency changes, package/lockfile changes,
  backend/frontend/Docker/CI changes, cookie/token/secret handling, public
  hosting, ads, PR #1001 file changes, or 更新適用機能.

## Y-AUTO-02 Repo Safety Risk Classification Outcome

- Script:
  `scripts/check_repo_safety.py`
- Added report-only risk classification output:
  - `tier`
  - `automation`
  - `reason`
- Preserved existing `Status: OK` / `Status: BLOCKED` behavior.
- Preserved existing blocker behavior for forbidden paths, generated
  distribution folders, PR #1001 leakage, secret-like content, dangerous
  behavior, and required LLMwiki basics.
- Current checker task classifies as `Medium` with
  `automation: auto-merge-ok`.
- No generated distribution folder, generated notice bundle, generated guide
  output, package output, build/package/install command, dependency change,
  package/lockfile change, backend/frontend/Docker/CI change,
  cookie/token/secret handling, public hosting, ads, PR #1001 file change, or
  更新適用機能 was added.

## Y-AUTO-01 Codex Automation Policy Outcome

- Policy document:
  `docs/llmwiki/codex-automation-policy.md`
- Added five Codex automation risk levels:
  - Low: docs/LLMwiki, notice source, guide source, inventory source, and
    roadmap/handoff/current-state synchronization.
  - Medium: report-only scripts, dry-run scripts, checker warning logic,
    read-only inspection, and small safe UX copy/display.
  - High-low: package- or desktop-adjacent design, preview, contract, preflight,
    backup/rollback docs, and output prediction work that remains docs-only,
    report-only, or dry-run-only.
  - High-mid: real generation or implementation-adjacent prototypes that may
    get a PR but require human review before merge.
  - High-high: automatic-execution prohibited work that must stop before
    implementation.
- Low and Medium may use auto PR / auto merge when their gates pass.
- High-low may use auto PR / auto merge only when all mandatory gates pass,
  including repo safety, clean-package dry-run, `git diff --check`, GitHub clean
  merge state, and no failed checks.
- High-mid and High-high remain outside auto merge.
- No generated distribution folder, generated notice bundle, generated guide
  output, package output, build/package/install command, dependency change,
  package/lockfile change, backend/frontend/Docker/CI change,
  cookie/token/secret handling, public hosting, ads, PR #1001 file change, or
  更新適用機能 was added.

## Y-06V Notice Source Index Outcome

- Index source draft:
  `docs/llmwiki/package-notices/notice-source-index.source.md`
- Added source material for a future notice / license / dependency inventory
  source index used by clean-package review.
- The draft is source-only and review-oriented, with:
  - source file inventory
  - future output mapping for aggregate notices, license directories,
    manifest files, beginner guide notice sections, and developer checklist
    items
  - review status vocabulary
  - unresolved questions
  - future generated notice-bundle requirements
  - no-generation boundary
- Read-only checked existing source drafts for MeTube, yt-dlp, FFmpeg, Python
  runtime, frontend dependencies, desktop shell, and bundled Python/backend
  dependency inventory.
- Kept actual notice output, license output, generated inventory, manifest
  output, package generation, and package-time legal review as future work.
- No actual notice bundle, license bundle, generated package folder,
  generated manifest, generated inventory, HTML/TXT guide output, build
  artifact, package/lockfile change, dependency change, package manager
  operation, backend/frontend/Docker/CI change, or package/lockfile change was
  added.

## Y-06U Bundled Python Dependency Inventory Source Outcome

- Inventory source draft:
  `docs/llmwiki/package-notices/bundled-python-dependency-inventory.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/開発者向け/inventory/bundled-python-dependency-inventory.json`
  and related Python dependency notice / license review output.
- The draft is source-only and review-oriented, with:
  - future package role and placement candidates
  - read-only dependency source files inspected
  - runtime dependency candidates
  - developer-only dependency candidates
  - optional / indirect dependency candidates
  - manifest candidate fields
  - license review checklist
  - notice bundle review checklist
  - legal-not-final boundary
  - future generated inventory requirements
- Recorded `pyproject.toml` and `uv.lock` as present local dependency sources;
  recorded Poetry, requirements, setup, Pipenv, Conda environment, constraints,
  tox, and nox dependency files as not present.
- Kept exact bundled inclusion, final license names, source artifacts, native
  code review, certificate/data-file review, notice bundle generation, and
  developer-only exclusion confirmation as future package-generation /
  license-review work.
- No actual notice output, license bundle, generated package folder, generated
  inventory output, dependency audit, build artifact, package/lockfile change,
  dependency change, package manager operation, backend/frontend/Docker/CI
  change, or package/lockfile change was added.

## Y-06T Desktop Shell Notice Source Outcome

- Notice source draft:
  `docs/llmwiki/package-notices/desktop-shell-notice.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/開発者向け/notices/desktop-shell-notice.txt`.
- The draft is source-only and review-oriented, with:
  - future notice / license placement candidates
  - Windows and macOS notice placement candidates
  - Tauri, Electron, WebView2 direct host, and native launcher candidate notes
  - official reference candidates for later recheck
  - short beginner-facing notice pointer
  - developer-facing notice draft
  - manifest candidate fields
  - required future review checklist
  - future generated notice-bundle requirements
- Kept desktop shell choice, exact version, runtime payload, WebView/runtime
  distribution terms, installer payload, signing/notarization output, and
  dependency inventory as future package-generation / license-review work.
- No actual notice output, license bundle, generated package folder, desktop
  shell implementation, dependency inventory, build artifact, package/lockfile
  change, dependency change, package manager operation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06S Frontend Dependency Notice Source Outcome

- Notice source draft:
  `docs/llmwiki/package-notices/frontend-deps-notice.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/開発者向け/notices/frontend-deps-notice.txt`.
- The draft is source-only and review-oriented, with:
  - future notice / license placement candidates
  - read-only local candidate sources from `ui/package.json` and
    `ui/pnpm-lock.yaml`
  - frontend runtime dependency candidates
  - developer/build-tool dependency candidates
  - package / lockfile review candidates
  - short beginner-facing notice pointer
  - developer-facing notice draft
  - manifest candidate fields
  - required future review checklist
  - future generated notice-bundle requirements
- Covered Angular, Bootstrap, Font Awesome, Popper, RxJS, tslib, Zone.js,
  ng-bootstrap, ng-select, Socket.IO frontend integration, browser helper
  packages, Angular build tooling, TypeScript, ESLint, Vitest, jsdom, Vite,
  Sass, PostCSS, and transitive packages as candidates only.
- Kept exact license names, source URLs, runtime inclusion, developer-only
  classification, source map handling, font/icon/style asset notices, and
  build artifact review as future package-generation / license-review work.
- No actual notice output, license bundle, generated package folder, frontend
  build artifact, dependency inventory, package/lockfile change, dependency
  change, package manager operation, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06R Python Runtime Notice Source Outcome

- Notice source draft:
  `docs/llmwiki/package-notices/python-runtime-notice.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/開発者向け/notices/python-runtime-notice.txt`.
- The draft is source-only and review-oriented, with:
  - future runtime / notice / license placement candidates
  - local Python/runtime candidates from `pyproject.toml`, `Dockerfile`, and
    Dockerless package planning docs
  - official Python source / license URL candidates
  - short beginner-facing notice pointer
  - developer-facing notice draft
  - manifest candidate fields
  - required future review checklist
- Covered CPython/Python runtime selection as unresolved until the exact
  Windows/macOS artifact, provider, version, architecture, and packaging method
  are chosen later.
- Kept Python dependency notices, incorporated software acknowledgements,
  native library notices, and bundler runtime notices as separate future review
  items.
- No actual notice output, license bundle, generated package folder, Python
  runtime download/install/build/update behavior, package build/copy behavior,
  Tauri/Electron implementation, backend/frontend/Docker/CI change, or
  package/lockfile change was added.

## Y-06Q FFmpeg Notice Source Outcome

- Notice source draft:
  `docs/llmwiki/package-notices/ffmpeg-notice.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/開発者向け/notices/ffmpeg-notice.txt`.
- The draft is source-only and review-oriented, with:
  - future notice / license placement candidates
  - OS-specific notice candidates for Windows and macOS runtime folders
  - FFmpeg component summary
  - local usage candidates from `Dockerfile`, `app/dl_formats.py`,
    `app/ytdl.py`, and Dockerless package planning docs
  - official FFmpeg source / legal URL candidates
  - manifest candidate fields
  - required future review checklist
- Covered selected binary provider, version, target OS, architecture, build
  configuration, LGPL/GPL status, source availability, and patent-sensitive or
  nonfree options as unresolved future review items.
- No actual notice output, license bundle, generated package folder, FFmpeg
  download/install/update behavior, package build/copy behavior, Tauri/Electron
  implementation, backend/frontend/Docker/CI change, or package/lockfile change
  was added.

## Y-06P yt-dlp Notice Source Outcome

- Notice source draft:
  `docs/llmwiki/package-notices/yt-dlp-notice.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/開発者向け/notices/yt-dlp-notice.txt`.
- The draft is source-only and review-oriented, with:
  - future notice / license placement candidates
  - yt-dlp component summary
  - local dependency candidates from `pyproject.toml`, `uv.lock`, and previous
    runtime `/version` verification
  - short beginner-facing notice pointer
  - developer-facing notice draft
  - manifest candidate fields
  - required future review checklist
- Covered official project and package source URL candidates, the Unlicense
  candidate, selected extras, and separate future review for transitive
  dependency notices.
- No actual notice output, license bundle, generated package folder,
  yt-dlp install/update behavior, package build/copy behavior,
  Tauri/Electron implementation, backend/frontend/Docker/CI change, or
  package/lockfile change was added.

## Y-CHECK-01 Safety Gate Checker Design Outcome

- Design document:
  `docs/llmwiki/safety-gate-checker-design.md`
- Defined a future repository safety checker and automation gate for low- and
  medium-risk Codex work.
- Designed checks for:
  - changed files scope
  - forbidden paths
  - secret-like pattern families without printing matched values
  - generated `動画保存ツール_ローカル専用/` folder presence
  - upstream PR #1001 file leakage
  - dangerous behavior
  - update execution
  - package guide / notice completeness warnings
  - LLMwiki consistency
  - PR safety gate summary
- The design is docs-only and does not add scripts, CI, package generation,
  update execution, generated distribution folders, backend/frontend/Docker/CI
  changes, package/lockfile changes, or credential handling.

## Y-CHECK-02 Repo Safety Check Script Outcome

- Script:
  `scripts/check_repo_safety.py`
- Added the first stdlib-only report-only implementation of the repository
  safety gate.
- Default mode checks the current working tree diff against `HEAD`, including
  untracked files.
- Optional `--base` can include committed branch diff context such as
  `fork/master`.
- Implemented checks for changed-file scope, forbidden paths, generated
  distribution folder presence, upstream PR #1001 leakage, secret-like changed
  content, dangerous behavior patterns, required LLMwiki basics, and package
  guide/notice source warnings.
- Reports are sanitized: secret-like findings show path, line, and pattern
  family only.
- Exit codes are `0` for OK or warning-only, `1` for blocked, and `2` for
  usage errors.
- No automation gate, CI integration, PR bot/comment automation, package
  generation, generated distribution folder, backend/frontend/Docker/CI change,
  package/lockfile change, update execution, or cookie/token/secret value
  output was added.

## Y-06O MeTube Notice Source Outcome

- Notice source draft:
  `docs/llmwiki/package-notices/metube-notice.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/開発者向け/notices/MeTube-notice.txt`.
- The draft is source-only and review-oriented, with:
  - future notice / license placement candidates
  - MeTube component summary
  - short beginner-facing license pointer
  - developer-facing notice draft
  - future manifest candidate fields
  - required future review checklist
- Covered local source candidates, AGPLv3 license candidate from root
  `LICENSE`, fork/upstream source URL candidates, source commit placeholder,
  and no-private-data notice hygiene.
- No actual notice output, license bundle, generated package folder,
  package build/copy behavior, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06N Safe-Use HTML Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/05-safe-use.html.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/05_安全な使い方.html`.
- The draft is Japanese-first and structured for future HTML conversion with:
  - hero copy
  - safe-use cards
  - do / do-not cards
  - a sensitive-data warning box
  - an update-safety note
  - a footer note
- Covered local-only personal use, allowed examples, prohibited uses,
  sensitive-data sharing boundaries, safe trouble actions, and update safety.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06M Troubleshooting TXT Fallback Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/04-troubleshooting.txt.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/04_困ったとき.txt`.
- The draft is shorter than the HTML source and designed to remain readable in
  a normal text editor.
- Covered first actions, common trouble cases, stop/quit behavior, safe use,
  and the hand-off to `04_困ったとき.html`.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06L Troubleshooting HTML Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/04-troubleshooting.html.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/04_困ったとき.html`.
- The draft is Japanese-first and structured for future HTML conversion with:
  - hero copy
  - quick checklist
  - trouble cards
  - a warning box
  - a safe-use reminder
  - a footer note
- Covered first checks, common trouble cases, gentle error messages, save-folder
  guidance, stop/quit behavior, update-display uncertainty, and safe use.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06K How-To-Use TXT Fallback Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/03-how-to-use.txt.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/03_使い方.txt`.
- The draft is shorter than the HTML source and designed to remain readable in
  a normal text editor.
- Covered basic save steps, save-format choices, saving/completion behavior,
  stop/quit behavior, safe use, and the hand-off to `03_使い方.html`.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06J How-To-Use HTML Guide Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/03-how-to-use.html.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/03_使い方.html`.
- The draft is Japanese-first and structured for future HTML conversion with:
  - hero copy
  - quick steps
  - action cards
  - format cards
  - status explanation cards
  - a warning box
  - troubleshooting link cards
  - a footer note
- Covered start, URL paste, save-format selection, save, open save folder,
  status reading, retry guidance, stop/quit, and safe use.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06I First-Open TXT Fallback Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/00-first-open.txt.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/00_最初に開いてください.txt`.
- The draft is shorter than the HTML source and designed to remain readable in
  a normal text editor.
- Covered what the tool is, the short first-use steps, safe use,
  troubleshooting entry points, and the hand-off to
  `00_最初に開いてください.html`.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06H First-Open Guide Source Outcome

- Guide source draft:
  `docs/llmwiki/package-guides/00-first-open.html.source.md`
- Added source material for future
  `動画保存ツール_ローカル専用/00_最初に開いてください.html`.
- The draft is Japanese-first and structured for future HTML conversion with:
  - hero copy
  - first-step cards
  - a local-only warning box
  - in-app help cards
  - troubleshooting cards
  - a footer note
- Covered start, URL paste, save, open save folder, stop/quit, safe use, and
  first troubleshooting actions.
- Covered the `停止して終了` close-safety note and kept X-close behavior as a
  caution, not the preferred exit path.
- No actual `.html` / `.txt` guide output, generated package folder, package
  build/copy behavior, notice bundle, Tauri/Electron implementation,
  backend/frontend/Docker/CI change, or package/lockfile change was added.

## Y-06G Dry-Run Warning Hardening Outcome

- Dry-run script:
  `scripts/clean_package_dry_run.py`
- Added nonblocking warning output for:
  - missing beginner guide source candidates
  - missing license/notice source candidates
  - missing local-only safety notice source candidates
  - missing Windows/macOS section source coverage
- Warning-only dry-runs keep `Status: OK` and exit code `0`.
- Existing blockers remain blockers:
  - generated package folder
  - forbidden filename families
  - secret-like content findings
  - upstream PR #1001 leakage
- No package generation, guide generation, notice copying, build/package output,
  backend/frontend/Docker/CI changes, or package/lockfile changes were added.

## Y-06F Guide Source And Notice Review Outcome

- Guide source plan:
  `docs/llmwiki/beginner-guide-source-plan.md`
- License/notice plan:
  `docs/llmwiki/license-notice-plan.md`
- Y-06F is docs-only and does not generate package files.
- Planned future guide outputs:
  - `00_最初に開いてください.html`
  - `00_最初に開いてください.txt`
  - `03_使い方.html`
  - `03_使い方.txt`
  - `04_困ったとき.html`
  - `04_困ったとき.txt`
  - `05_安全な使い方.html`
- Planned notice categories cover MeTube, yt-dlp, ffmpeg, Python runtime,
  bundled Python dependencies, frontend runtime dependencies, and future
  Tauri/Electron runtime pieces only if implemented later.
- License text copying, notice bundle generation, guide generation, package
  generation, Tauri/Electron implementation, backend/frontend/Docker/CI
  changes, and package/lockfile changes remain unapproved.
- Next PR candidate: add advisory dry-run warnings for missing guide and notice
  source candidates.

## Y-06E Dry-Run Script Outcome

- Report-only dry-run script:
  `scripts/clean_package_dry_run.py`
- Output is a human-readable sanitized text report.
- The script reports the planned `動画保存ツール_ローカル専用/` package root,
  top-level entries, Windows entries, macOS entries, developer entries,
  excluded path rules, validation checks, safety flags, and blocker details.
- Implemented safety checks:
  - forbidden path and generated-folder checks
  - forbidden filename family checks
  - forbidden content pattern family checks without printing matched values
  - required LLMwiki contract presence checks
  - PR #1001 leakage checks for `docker-compose.local.yml` and
    `docs/local-only.md`
- Exit codes are `0` for OK, `1` for blockers, and `2` for CLI usage errors.
- JSON/Markdown report modes remain future candidates, not implemented in the
  initial Y-06E script.

## Y-06D Dry-Run Contract Outcome

- Clean-package generator dry-run contract is documented in
  `docs/llmwiki/clean-package-dry-run-contract.md`.
- Dry-run is fixed as report-only planning before any package files are copied
  or generated.
- Future command candidates, JSON/Markdown report shape, exit code policy,
  warning/error/blocked classifications, planned output manifest,
  include/exclude rules, validation rules, and output examples are defined.
- Secret-like content, forbidden paths, forbidden filenames, generated package
  folders, local-only notice gaps, Windows/macOS section gaps, large file review,
  and upstream PR #1001 leakage are explicit safety gates.
- Actual package generation, clean-package generator implementation,
  Tauri/Electron/WebView2, installers, signing, build/package commands,
  dependency install/update, Docker pull, update apply, cookie/token/secret
  handling, public hosting, ads, backend/frontend/Docker/CI changes, and
  package/lockfile changes remain unapproved.

## Y-06C Manifest And Guide Outcome

- Desktop package manifest is documented in
  `docs/llmwiki/desktop-package-manifest.md`.
- Beginner HTML/TXT guide skeleton is documented in
  `docs/llmwiki/beginner-guide-skeleton.md`.
- Future package root is fixed as `動画保存ツール_ローカル専用/`.
- Primary guide is `00_最初に開いてください.html`; fallback guide is
  `00_最初に開いてください.txt`; Markdown is developer/LLMwiki material.
- Windows and macOS package skeletons, include/exclude rules, generated
  manifest candidates, user data paths, notices, checksums, and safe beginner
  copy boundaries are defined.
- Generated distribution folders, package scripts, Tauri/Electron/WebView2
  implementation, package builds, installers, signing,
  backend/frontend/Docker/CI/package/lockfile changes, and update apply remain
  unapproved.

## Y-06B Contract Outcome

- Desktop sidecar lifecycle and package boundaries are documented in
  `docs/llmwiki/desktop-sidecar-lifecycle-contract.md`.
- The desktop wrapper owns backend sidecar start, readiness checks, monitoring,
  stop, close confirmation, and abnormal-exit recovery.
- Future desktop launch must force `HOST=127.0.0.1` and per-user
  download/state/temp paths.
- Package contents, exclusions, Windows/macOS boundaries, and beginner
  `.html` / `.txt` guide requirements are defined at contract level.
- Tauri/Electron/WebView2 implementation, package builds, installers, signing,
  backend/frontend/Docker/CI/package/lockfile changes, and update apply remain
  unapproved.

## Y-06A Feasibility Outcome

- Dockerless desktop distribution is feasible, but not beginner-ready from the
  current repository state.
- Tauri is the preferred first candidate.
- Electron remains the fallback if Tauri WebView, sidecar, or signing friction
  becomes unacceptable.
- WebView2 is a Windows-only fallback and not the primary cross-platform path.
- The main blockers are backend lifecycle, close safety, desktop path defaults,
  ffmpeg / yt-dlp / Deno / bgutil packaging, signing/notarization, and excluding
  cookie/token/secret features from the beginner desktop flow.

## Beginner UX Source Of Truth

Y-06 should optimize for a non-developer local desktop user:

- Start MeTube without understanding Docker.
- Keep setup language short, Japanese, and concrete.
- Prefer one clear local launch path per OS.
- Make storage location, app status, and stop/quit behavior obvious.
- Avoid public hosting, account setup, ads, background sync, or external-user
  assumptions.
- Preserve the existing readonly update readiness work as diagnostic support,
  not as update execution.

## Future Automatic Update Stages

Y-05 readiness work is complete for now. These remain historical or candidate
stages, not approved update execution work:

- Stage 1: readonly version/status visibility (implemented)
- Stage 2: local changelog and update availability confirmation
- Stage 3: backup and rollback design (documented)
- Stage 4: readonly backup / rollback readiness preflight report (implemented)
- Stage 5: manual approval flow for applying updates (documented)
- Stage 6: dry-run / prepare-only update apply contract (documented)
- Stage 7: readonly update-plan contract-only endpoint (implemented)
- Stage 8: readonly update-plan runtime verification (completed)
- Stage 9: optional readonly plan/preflight UI visibility or closeout decision
- Stage 10: guarded local-only update execution

Any automatic update stage must respect the safety boundaries in
`safety-boundaries.md`.

## Future UI Improvement Candidates

- Improve clarity of Japanese status and error copy
- Make local-only state visible without adding public hosting assumptions
- Improve update-status footer presentation after runtime verification
- Keep UI changes separate from backend, Docker, and CI changes unless a task explicitly
  requires a broader scope

## Not In Scope Now

- Public hosting
- Ads or monetization
- Mass-download optimization
- External wiki tooling
- Background daemons or automatic sync
- Update apply implementation
- Desktop installer or packaging implementation
- Tauri/Electron implementation

## Y-AUTO-08 Outcome: Local Safety Gate Aggregator Design

Y-AUTO-08 completed the docs-only design for a local safety gate aggregator. It added `docs/llmwiki/local-safety-gate-aggregator-design.md` and updated the automation roadmap context without implementing scripts or generating package output.

Immediate next candidates:

- Y-AUTO-09: implement `scripts/run_local_safety_gates.py` as a stdlib-only, read-only text-output aggregator.
- Y-AUTO-10: document PR body integration guidance for aggregator output after Y-AUTO-09.
- Y-AUTO-11: add or refine lane-specific scope presets after aggregator behavior is stable.
- Y-AUTO-12: revisit package-readiness workflow only after local gate aggregation is stable.

Actual package generation remains blocked until a later explicit human-reviewed task approves it.
## Y-AUTO-09 Outcome: Local Safety Gate Aggregator Implementation

Y-AUTO-09 implements `scripts/run_local_safety_gates.py` as a stdlib-only, read-only, text-output-only local gate aggregator.

The aggregator orchestrates existing gates, checks generated package folder absence, checks PR #1001 leakage absence, checks local helper exclusion, and reports changed-file summary. It does not replace the underlying gates.

Next candidates:

- Y-AUTO-10 PR body generator design.
- Y-AUTO-11 PR body generator stdout-only implementation.
- Y-AUTO-12 Codex run prompt templates.
- Y-08F readiness checklist preview implementation, if explicitly approved.

Actual package generation remains blocked.
## Y-AUTO-10A Outcome: Safety Wording Checker Design

Y-AUTO-10A adds `docs/llmwiki/safety-wording-checker-design.md` as a docs-only design for future docs wording preflight.

Next candidates:

- Y-AUTO-10B safety wording checker implementation.
- Y-AUTO-11 PR body generator design.
- Y-AUTO-12 PR body generator stdout-only implementation.
- Y-AUTO-13 Codex prompt templates.

Actual package generation remains blocked.
## Y-AUTO-10B Outcome: Safety Wording Checker Implementation

Y-AUTO-10B adds `scripts/check_safety_wording.py` as a standalone read-only safety wording checker for docs.

Next candidates:

- Y-AUTO-12 PR body generator stdout-only implementation.
- Y-AUTO-13 Codex prompt templates.
- APP-BOOT-01 new app bootstrap template design.
- APP-BOOT-02 bootstrap skeleton.

Actual package generation remains blocked.

## Y-AUTO-11 Outcome: PR Body Generator Design

Y-AUTO-11 adds `docs/llmwiki/pr-body-generator-design.md` as a docs-only
design for a future stdout-only PR body generator.

The design standardizes the PR body sections used across recent automation
PRs: Summary, Risk / automation, Local helper note, Explicitly not performed,
Verification, Cleanup / rollback, and Human review note.

It defines future input options, required output sections, risk templates,
explicitly not-performed presets, verification templates, local helper note
rules, human review rules, safe wording rules, CLI shape, stdout Markdown
output, exit code contract, sanitization rules, integration with the local
safety gate aggregator, integration with the safety wording checker, and future
GitHub API boundaries.

Next candidates:

- Y-AUTO-12 PR body generator stdout-only implementation.
- Y-AUTO-13 Codex prompt templates.
- APP-BOOT-01 new app bootstrap template design.
- APP-BOOT-02 bootstrap skeleton.

Actual package generation remains blocked.
