# Roadmap

## Immediate Next

### Y-SEC-01 local-only runtime guardrails

- Status: completed via fork PR #82.
- Summary: added first-pass local-only runtime guardrails for accidental
  exposure and dangerous configuration.
- Runtime guardrails include local Host allowlisting, Origin / Referer checks
  for state-changing requests, dangerous local-only config fail-fast checks, and
  minimal security response headers.
- Y-SEC-01A amends this PR so the default bind is `HOST=127.0.0.1` and
  non-loopback bind targets are blocked when `LOCAL_ONLY_MODE=true`.
- Y-SEC-01B adds a dependency-free local-only security helper and
  standard-library `unittest` coverage for host/source/public-host/config guard
  decisions. These tests reduce the verification gap when pytest/aiohttp are
  unavailable, but full backend pytest remains required in a dependency-ready
  environment.
- Y-SEC-01C rejects non-local `Origin` headers for all local-only requests,
  while still allowing requests without `Origin` for local non-browser clients
  and keeping the `Referer` guard scoped to state-changing requests.
- No frontend UI, Docker, dependency, lockfile, package generation,
  yt-dlp extractor, download queue semantic, or safety gate changes are part of
  this lane.
- Risk: High-mid / PR-ready only / human-review-required.

### Y-SEC-02 URL intake SSRF / private-network target guard

- Status: completed via fork PR #83.
- Merge commit: `e54058dc112ae6c29237738b21bff0e3253407ea`.
- Summary: added first-pass URL intake protection for user-submitted download
  and subscription URLs before enqueue or subscription creation.
- `URL_INTAKE_GUARD=true` is default-on and must remain enabled while
  `LOCAL_ONLY_MODE=true`.
- Guard blocks non-HTTP(S) schemes, missing or malformed hosts, URL userinfo,
  localhost/loopback, private/link-local/shared/multicast/reserved IP literals,
  IPv4-mapped IPv6 pointing to blocked IPv4 ranges, obvious internal hostnames,
  and metadata hostnames.
- DNS resolution remains opt-in helper behavior and is not enabled on the
  request path in this first pass.
- Known limits: this does not claim complete protection against all DNS
  rebinding, downstream extractor redirects, or later URLs fetched internally by
  yt-dlp.
- No frontend UI, Docker, dependency, lockfile, package generation, yt-dlp
  extractor, download queue semantic, or safety gate changes are part of this
  lane.
- Risk: High-high / draft PR only / human-review-required.

### Y-SEC-03 log and filename privacy redaction hardening

- Status: completed via fork PR #84.
- Merge commit: `aa0200b126d5cdc9d18617280fe733284bf990e6`.
- Summary: added first-pass dependency-free privacy redaction helpers for
  URL/log text material and filename component sanitization.
- URL/log redaction removes query strings, fragments, userinfo, token-like
  values, bearer auth headers, cookie headers, and common local path material.
- Non-empty `custom_name_prefix` values are sanitized before queue or
  subscription use. Omitted or empty custom prefixes remain empty.
- Unsafe URL intake errors remain generic and do not echo the submitted URL.
- Known limits: downstream yt-dlp may still derive filenames internally, so do
  not claim every final filename is fully controlled by this first pass.
- No frontend UI, Docker, dependency, lockfile, package generation, yt-dlp
  extractor, real download, cookie/token/secret handling, or safety gate change
  is part of this lane.
- Risk: High-high / draft PR only / human-review-required.

### Y-DIST-01 CLEAN portable distribution manifest and forbidden-file checker

- Status: completed via fork PR #85.
- Merge commit: `f2e2678e3dc986a34f2e5bb0bd65f56d54b2b415`.
- Summary: added a stdlib-only, report-only forbidden-file checker for an
  explicitly provided CLEAN portable distribution candidate directory.
- The checker blocks forbidden paths, obvious sensitive filenames, symlinks,
  and conservative secret-like content pattern families without printing file
  contents or matched secret values.
- The manifest contract records allowed conceptual contents, forbidden
  contents, checker behavior, known limits, and the future generation gate.
- This lane does not create a CLEAN folder, ZIP, installer, package output, or
  generated files outside the requested docs/test/tooling changes.
- Risk: High-low / tooling-only / report-only / draft PR preferred.

### Y-DIST-02 checksum / hash / version / license notice bundle verification

- Status: completed via fork PR #86.
- Merge commit: `00a90bfa1efd11935aa46b07848d05614d1c744e`.
- Summary: adds a stdlib-only, report-only metadata checker for an explicitly
  provided CLEAN portable distribution candidate directory.
- The checker requires candidate-root `VERSION.txt`, `MANIFEST.json`,
  `checksums.sha256`, `LICENSE`, and `NOTICE`.
- The checker validates basic version shape, manifest fields, local-only
  distribution metadata, sha256sum-style checksum lines, recomputed SHA-256
  matches, duplicate listed paths, missing listed files, unsafe checksum paths,
  and basic license / notice presence and safety.
- The checker runs Y-DIST-01 as a prerequisite and includes those findings in
  its report.
- This lane does not create metadata, generate checksums, create a CLEAN folder,
  ZIP, installer, package output, or generated files outside the requested
  docs/test/tooling changes.
- GitHub connector ready-for-review failed with
  `Resource not accessible by integration`; human-approved `gh` fallback
  marked the PR ready and squash-merged with an expected head SHA guard.
- Remote branch `codex/y-dist-02-metadata-checker` was deleted.
- Risk: High-low / tooling-only / report-only / draft PR preferred /
  human-review-required.

### Y-GH-OPS-01 GitHub connector failure fallback runbook closeout

- Status: completed via fork PR #87.
- Merge commit: `9a1a262e03da7976850b8dfddacb1576b0572c2c`.
- Summary: records the PR #86 connector ready-for-review failure and the safe
  human-approved `gh` fallback path for ready / merge operations.
- Documents `Resource not accessible by integration` as a connector permission
  failure that can affect ready-for-review / GraphQL mutations.
- Requires stable PR facts, expected head SHA confirmation, and an expected-head
  guard for squash merge before `gh` fallback can be used.
- This lane does not change GitHub branch protection, CODEOWNERS, CI,
  backend/frontend code, package files, lockfiles, or safety gate behavior.

### Y-CI-01 lightweight safety workflow design

- Status: completed via fork PR #88.
- Merge commit: `14508576e249ee65ff4d2d63060cb6b1d4e8e484`.
- Design doc:
  `docs/llmwiki/lightweight-safety-workflow-design.md`.
- Summary: defines a future minimal GitHub Actions workflow named
  `local-fork-safety` at `.github/workflows/local-fork-safety.yml`.
- Initial recommended event is `pull_request` targeting `master` without path
  filters, so the first safety signal does not miss PR #1001 files, generated
  package folder checks, or unexpected path changes.
- Initial permissions should be read-only: `contents: read`.
- Initial checks should call existing stdlib-friendly safety scripts and
  explicit generated-package / PR #1001 absence checks.
- Warning-only findings should log without failing CI; blockers should fail CI.
- Concurrency is deferred to Y-CI-04 unless real PR noise requires it earlier.
- This lane does not add `.github/workflows/`, required checks, branch
  protection, CODEOWNERS, dependency installation operations, Docker
  operations, generated package output, or metadata/checksum generation.

### Y-CI-02 minimal workflow implementation

- Status: completed via fork PR #89.
- Merge commit: `66a4a638fef65988c10405398e6e591f0fccb923`.
- Workflow:
  `.github/workflows/local-fork-safety.yml`
- Summary: adds the minimal `local-fork-safety` pull request workflow for fork
  `master`.
- The workflow is now present on fork `master`.
- The workflow has no path filter and no concurrency setting in this phase.
- The workflow uses `permissions: contents: read`, `actions/checkout@v6`, and a
  read-only fetch to create `fork/master` for base diff checks.
- Checks include repository safety, base-aware repository safety, clean-package
  dry-run report regression, clean-package dry-run JSON parse validation,
  safety wording, generated package folder absence, and PR #1001 file absence.
- This workflow is only a PR safety display layer. Success does not approve
  package generation, ZIP/installer output, CLEAN folder creation,
  metadata/checksum generation, branch protection, required checks, or merge.
- PR #89's failure was human-reviewed as expected for the first
  workflow-introducing PR because the check did not exist on the base branch
  before merge.

### Y-CI-02B local-fork-safety docs-only self-check

- Status: completed via fork PR #90.
- Merge commit: `f235416950868331f5a107e13631899aa7785c21`.
- Summary: created a small docs-only observation PR to confirm a normal
  docs-only change passes the new `local-fork-safety` workflow.
- This is not a workflow-fix PR and should not modify `.github/workflows/`.
- Result: `local-fork-safety` succeeded.
- If a later docs-only PR fails unexpectedly, keep that PR unmerged and use
  `Y-CI-02C workflow fix` as the next candidate.

### Y-DIST-03 recipient-safe runbook and first-run local-only verification

- Status: completed via fork PR #91.
- Merge commit: `f43c9a106308ac05a0ef5e32f4cf455a4d88b3e1`.
- Summary: added docs-only recipient-safe local-only instructions and first-run
  local-only verification procedure.
- New documents:
  - `docs/llmwiki/recipient-safe-runbook.md`
  - `docs/llmwiki/first-run-local-only-verification.md`
- Relation:
  - Y-DIST-01 covers CLEAN candidate forbidden-file / secret-like content /
    manifest baseline checking.
  - Y-DIST-02 covers version / manifest / checksum / license / notice metadata
    checking.
  - Y-DIST-03 covers recipient procedure and first-run verification only.
- This lane does not create a CLEAN folder, ZIP output, installer output,
  package output, metadata, checksums, real downloads, dependency installation
  operations, container image operations, backend/frontend runtime changes,
  yt-dlp extractor changes, download queue changes, public hosting,
  cookie/token/secret handling, or PR #1001 files.

### Y-DIST-04 distribution readiness matrix

- Status: completed via fork PR #92.
- Merge commit: `cca229cc2b842cda3778546236358069e6938ab3`.
- Summary: add a docs-only advisory readiness matrix for future CLEAN portable
  distribution planning.
- New document:
  `docs/llmwiki/distribution-readiness-matrix.md`.
- The matrix defines `ready`, `blocked`, `human_review_required`,
  `not_started`, `not_applicable_yet`, and `warning_only` status categories.
- It covers project scope / legal safety, local-only runtime boundary, runtime
  security guardrails, CLEAN candidate file hygiene, metadata/checksum/version/
  license notice, recipient runbook, first-run verification, CI/local safety
  gates, artifact generation approval, human review/merge gates, known local
  environment issues, and next required actions.
- This lane is advisory only and does not approve CLEAN folder generation, ZIP
  output, installer output, package output, metadata/checksum generation, real
  download verification, dependency installation operations, container image
  operations, backend/frontend/Docker/package/lockfile changes,
  `.github/workflows/` changes, branch protection changes, required-check
  changes, CODEOWNERS, `.gitignore`, public hosting, credential handling, or
  PR #1001 files.

### Y-DIST-05 human approval checklist before artifact generation

- Status: active.
- Summary: add a docs-only human approval checklist before any future CLEAN
  portable distribution artifact generation.
- New document:
  `docs/llmwiki/artifact-generation-approval-checklist.md`.
- The checklist states that artifact generation is blocked by default, all
  artifact categories are currently `not approved`, and any future approval
  must name the exact source commit, artifact scope, output path, remaining
  forbidden operations, required checks, and stop conditions.
- This lane does not create a CLEAN folder, ZIP output, installer output,
  package output, metadata, checksums, real downloads, dependency installation
  operations, container image operations, backend/frontend runtime changes,
  yt-dlp extractor changes, download queue changes, public hosting,
  cookie/token/secret handling, or PR #1001 files.

### Security next candidates

```text
Y-DIST-06:
  approved clean candidate dry-run plan

Y-CI-03:
  reusable workflow

Y-CI-04:
  concurrency / cancel-in-progress

Y-GH-01:
  branch protection design

Y-WIKI-CLEAN-01:
  current-state / handoff / archive整理
```

### Y-UI-QUALITY-01 quality selector simple labels with numeric values

- Status: completed via fork PR #73.
- Summary: simplified visible quality labels while preserving option ids and
  backend behavior.
- Visible video/audio quality labels now use simple Japanese labels plus numeric
  values.
- Existing option ids, API payloads, backend validation, and download logic were
  unchanged.
- The PR was frontend UI label-only and required human-reviewed merge because
  the current local safety aggregator forbids `ui/**`.
- This closeout does not modify safety gate behavior or broaden auto-merge
  policy for `ui/**`.

### Y-UI-QUALITY-02 quality selector helper copy / tooltip polish

- Status: completed via fork PR #75.
- Summary: clarified quality selector helper copy and audio label while
  preserving behavior.
- Video quality helper copy now explains quality targets / upper limits,
  fallback when source quality is unavailable, auto mode, and file-size
  tradeoff.
- Audio quality helper copy now explains the audio quality / file-size tradeoff
  and auto mode.
- Audio selector label changed from `画質` to `音質`.
- Option ids, payloads, backend/API/download logic, validation, and yt-dlp
  selector behavior were unchanged.
- The PR was frontend UI copy-only and required human-reviewed merge because
  the current local safety aggregator forbids `ui/**`.

### Y-UI-QUALITY-03 completed/result table quality label polish

- Status: completed via fork PR #77.
- Summary: polished result table quality labels and focused specs while
  preserving behavior.
- Completed/result table quality labels now match the simplified selector
  wording.
- Result table quality column header changed from `画質` to neutral `品質`.
- Focused UI spec coverage was added for quality label mapping.
- Backend/API/download logic, option ids, payloads, validation, and yt-dlp
  selector behavior were unchanged.
- The PR was frontend UI label/test work and required human-reviewed merge
  because the current local safety aggregator forbids `ui/**`.

### Y-UI-REVIEW-01 current UI manual review checklist

- Status: completed via fork PR #79.
- Summary: created manual UI review checklist for quality selector/result table
  polish.
- Merge commit: `2c30cc28080e39949bb4a6ab8e646abb700ebfb1`.
- Checklist:
  `docs/llmwiki/current-ui-manual-review-checklist.md`
- Screenshot capture and visual pass/fail review are not yet completed.
- No UI code, backend code, scripts, Docker files, CI files, package files, or
  lockfiles were changed.

### Y-UI-REVIEW-02 screenshot review findings closeout

- Status: partial.
- Summary: recorded current UI screenshot review findings and the environment
  limitation that prevented full interactive screenshot review.
- Findings:
  `docs/llmwiki/current-ui-screenshot-review-findings.md`
- Temporary screenshots were captured outside the repository for the static
  desktop add form, video quality helper popover, and narrow-width layout.
- The static preview remained at `サーバーに接続中...`, so native
  selector-open states, audio-mode visuals, and completed/result rows were not
  visually reviewed.
- No UI code, backend code, scripts, Docker files, CI files, package files, or
  lockfiles were changed.

### Y-UI-REVIEW-02R rerun screenshot review with mocked browser environment

- Status: completed.
- Summary: reran screenshot review with a temporary mocked browser environment
  and recorded remaining findings.
- Findings:
  `docs/llmwiki/current-ui-screenshot-review-findings.md`
- The rerun observed the loaded add form, video quality helper popover, audio
  mode, audio `音質` selector label, audio quality helper popover,
  completed/result table header `品質`, synthetic video/audio result quality
  labels, captions/thumbnail `-`, and narrow-width loaded layout.
- Native select dropdown panels were not visible in screenshots after selector
  clicks, so selector option labels were verified through browser DOM evidence.
- No blocking UI findings were observed.
- No UI code, backend code, scripts, Docker files, CI files, package files, or
  lockfiles were changed.

### Next candidates

Immediate next:

```text
Y-UI-REVIEW-02Z:
  review-complete closeout
```

Automation later:

```text
Y-AUTO-later:
  scoped safety-gate support for explicitly approved frontend label-only/copy-only lanes
```

- Do not modify safety gate behavior in this closeout.
- Do not broaden auto-merge policy for `ui/**` in this closeout.
- Any future frontend lane remains human-reviewed unless a later policy PR
  or checker PR explicitly updates the gate.

Later clean-package lane:

```text
Y-09:
  human-reviewed generation prototype planning only, not actual generation
```

Y-09 remains blocked unless later human-reviewed approval is given.

## Recent Automation Outcomes

### Y-AUTO-15 preflight environment checker implementation outcome

- Script:
  `scripts/check_local_dev_environment.py`
- Added a standalone read-only preflight environment checker.
- Checks Python runtime discovery, Git repository/branch/metadata access, Git
  lock files, optional GitHub CLI session state, remotes, baseline ref, working
  tree summary, local helper exclusion, generated folder absence, PR #1001
  leakage precheck, and local safety tool availability.
- The checker writes no files, changes no Git config, creates no branches,
  performs no GitHub write actions, creates no PRs, performs no merge actions,
  and creates no package output.
- The checker is readiness-only and does not replace safety gates.

### Y-AUTO-14 preflight environment checker design outcome

- Document:
  `docs/llmwiki/preflight-environment-checker-design.md`
- Added docs-only design for a future task-start environment readiness checker.
- Covers Python runtime discovery, Git metadata access, GitHub CLI session
  state, remote and branch baseline checks, local helper exclusion, generated
  package folder absence, PR #1001 leakage precheck, and local safety tool
  availability.
- Future candidate script path:
  `scripts/check_local_dev_environment.py`
- The checker design is readiness-only and does not replace safety gates.
- No script implementation, checker change, CI integration, GitHub API
  integration, PR creation/editing automation, report file writing, or generated
  package output is included.

### Y-AUTO-13 Codex prompt templates outcome

- Document:
  `docs/llmwiki/codex-run-prompt-templates.md`
- Added reusable Codex prompt templates for docs-only, report-only,
  checker-only, combined report / checker / docs, High-mid PR-ready-only,
  human-reviewed merge, recovery / finalize, closeout / handoff sync, and new
  app bootstrap workflows.
- The templates reduce repeated Codex prompt writing while preserving safety
  gates and human review.
- No script implementation, checker change, CI integration, GitHub API
  integration, PR creation/editing automation, report file writing, or generated
  package output is included.

### Y-AUTO-12 PR body generator stdout-only implementation outcome

- Script:
  `scripts/generate_pr_body.py`
- Design document:
  `docs/llmwiki/pr-body-generator-design.md`
- Added a stdout-only PR body generator.
- Supports title, risk, scope, automation validation, repeated summary lines,
  local helper note control, human review marker, optional changed-file summary,
  and verification presets.
- Uses Python stdlib only and resolves the repository root from the script path.
- The generator remains a review aid. It does not replace safety gates, approve
  merge, call the GitHub API, create PRs, edit PRs, write PR body files by
  default, or create package output.

### Next automation candidates

- APP-BOOT-02 bootstrap skeleton design / packet.
- APP-00A actual new app purpose / user / MVP definition.
- Y-CI-01 lightweight CI design.

Actual package generation remains blocked.

### APP-BOOT-01 new app bootstrap template design outcome

- Document:
  `docs/llmwiki/new-app-bootstrap-template-design.md`
- Added a docs-only reusable bootstrap design for future app projects.
- Documents how to reuse the current LLMwiki, risk-tier, Codex lane,
  preflight, wording checker, safety gate, PR body, and prompt-template
  workflow.
- Keeps APP-BOOT-02 separate for any future skeleton design or document packet.
- No new app directory, scripts, CI, backend/frontend/Docker/package/lockfile
  changes, generated package output, dependency installation operations, or
  container image operations are included.

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

- Y-08Z closes the preview hardening lane in this PR.
- Y-UI-QUALITY-01 quality selector simple labels with numeric values is complete
  via fork PR #73.
- The next practical UI candidate is Y-UI-QUALITY-02 optional quality selector
  helper copy / tooltip polish.
- Later clean-package work should resume as Y-09 human-reviewed generation
  prototype planning only, not actual generation.
- Keep Y-09 blocked unless later human-reviewed approval is given.
- Optional later CI wiring for the Y-07E checker remains separate.
- Keep the next PR report-only, dry-run-only, or source-material only unless
  explicitly approved otherwise.
- Do not create guide outputs, copy license text, generate notice bundles,
  generate manifests, or create package files.
- Do not create `動画保存ツール_ローカル専用/`, copy files, build packages, install
  dependencies, add Tauri/Electron/WebView2, change backend/frontend/Docker/CI,
  or change package/lockfile files.
- Do not broaden auto-merge policy for frontend `ui/**` work without a later
  explicit safety gate policy PR.

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
  - Y-AUTO-13 Codex run prompt templates
  - Y-AUTO-later worktree operation design
  - Y-AUTO-later stop condition checker design
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
  in report-only mode. Implemented by Y-08F.
- Actual package generation remains blocked.
- This Y-08E PR does not change scripts, add tests, add CI, write report files,
  create generated distribution folders, create package output, run
  ビルド/パッケージ/インストール操作, change dependencies, change
  package/lockfile files, change backend/frontend/Docker/CI files, handle
  cookie/token/secret values, touch PR #1001 files, or implement 更新適用機能.

## Y-08F Generation Readiness Checklist Preview Outcome

- Scripts:
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_clean_package_dry_run_reports.py`
- Added a report-only generation readiness checklist preview to clean-package
  dry-run output.
- Text and Markdown output now include `Generation Readiness Preview`.
- JSON output now includes top-level `generation_readiness`.
- The readiness preview keeps `overall: blocked`,
  `actual_generation_approved: false`, and `score_basis: advisory_only`.
- The preview includes checklist items, summary counts, unresolved count, and a
  next required action for later human review.
- The regression checker validates the text/Markdown markers, JSON readiness
  object, approval false, summary object, generated folder absence, and
  cross-format readiness status consistency.
- Future recommended candidate after Y-08F: Y-08G readiness summary polish /
  advisory score refinement in report-only / stdout-only mode. Implemented by
  Y-08G.
- Actual package generation remains blocked.
- This Y-08F PR does not create package output, write report files, create
  generated distribution folders, run ビルド/パッケージ/インストール操作,
  change dependencies, change package/lockfile files, change
  backend/frontend/Docker/CI files, handle cookie/token/secret values, touch PR
  #1001 files, or implement 更新適用機能.

## Y-08G Readiness Summary Polish Outcome

- Scripts:
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_clean_package_dry_run_reports.py`
- Added a compact advisory readiness score and readiness summary to the
  report-only clean-package dry-run output.
- Text output includes `Readiness summary` and `advisory_score: 23/100`.
- Markdown output includes `### Readiness Summary` and
  `advisory_score: 23/100`.
- JSON output includes `generation_readiness.advisory_score` and
  `generation_readiness.readiness_summary`.
- The score is review-only and has no approval meaning.
- The readiness preview keeps `overall: blocked`,
  `actual_generation_approved: false`, and `score_basis: advisory_only`.
- The regression checker validates Y-08G fields, score value/max, approval
  meaning, blocked override, cross-format advisory score consistency, and
  generated package folder absence.
- Follow-up closeout after Y-08G: Y-08Z preview hardening closeout, completed
  by this PR.
- Next practical candidate after Y-08Z: Y-UI-QUALITY-01 quality selector simple
  labels with numeric values.
- Actual package generation remains blocked.
- This Y-08G PR does not create package output, write report files, create
  generated distribution folders, run ビルド/パッケージ/インストール操作,
  change dependencies, change package/lockfile files, change
  backend/frontend/Docker/CI files, handle cookie/token/secret values, touch PR
  #1001 files, or implement 更新適用機能.

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

- Y-UI-QUALITY-02 quality selector helper copy / tooltip polish
- Improve clarity of Japanese status and error copy
- Make local-only state visible without adding public hosting assumptions
- Improve update-status footer presentation after runtime verification
- Keep UI changes separate from backend, Docker, and CI changes unless a task
  explicitly requires a broader scope.
- Keep frontend `ui/**` work human-reviewed unless a later policy PR explicitly
  updates the local safety gate and automation policy.

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
- Y-AUTO-13 Codex run prompt templates.
- Y-UI-QUALITY-01 quality selector simple labels with numeric values.

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

## Y-AUTO-12 Outcome: PR Body Generator Implementation

Y-AUTO-12 adds `scripts/generate_pr_body.py` as a stdout-only PR body
generator.

The generator emits standard Markdown sections for Summary, Risk / automation,
Local helper note, Explicitly not performed, Verification, Cleanup / rollback,
and Human review note. It supports safe risk and scope templates, optional
sanitized changed-file summaries, verification presets, automation validation,
and human review markers.

Next candidates:

- APP-BOOT-01 new app bootstrap template design.
- APP-BOOT-02 bootstrap skeleton.
- Y-AUTO-14 preflight environment checker design.
- Y-CI-01 lightweight CI design.

Actual package generation remains blocked.

## Y-AUTO-13 Outcome: Codex Prompt Templates

Y-AUTO-13 adds `docs/llmwiki/codex-run-prompt-templates.md` as a docs-only
template source for future Codex prompts.

The document covers:

- docs-only PR;
- report-only script PR;
- checker-only PR;
- combined report / checker / docs PR;
- High-mid PR-ready-only;
- human-reviewed merge;
- recovery / finalize;
- closeout / handoff sync;
- new app bootstrap.

It also records PR body generation, verification, safety wording, local helper,
risk boundary, maintenance, stop condition, and rollback patterns.

Next candidates:

- APP-BOOT-01 new app bootstrap template design.
- APP-BOOT-02 bootstrap skeleton.
- Y-CI-01 lightweight CI design.

Actual package generation remains blocked.

## Y-AUTO-15 Outcome: Preflight Environment Checker Implementation

Y-AUTO-15 adds `scripts/check_local_dev_environment.py` as a stdlib-only,
read-only, text-output-only readiness checker.

The checker reports Python runtime discovery, Git repository/branch/metadata
access, Git lock files, optional GitHub CLI session state, remote configuration,
baseline ref availability, working tree summary, local helper exclusion,
generated folder absence, PR #1001 leakage precheck, and required local safety
tool availability.

Next candidates:

- APP-BOOT-01 new app bootstrap template design.
- APP-BOOT-02 bootstrap skeleton.
- Y-CI-01 lightweight CI design.

Actual package generation remains blocked.

## Y-AUTO-14 Outcome: Preflight Environment Checker Design

Y-AUTO-14 adds `docs/llmwiki/preflight-environment-checker-design.md` as a
docs-only design for a future preflight environment checker.

The design documents:

- purpose, background, non-goals, output format, exit-code contract,
  sanitization rules, stop conditions, and rollback note;
- future check categories for Python runtime discovery, Git repository and
  branch baseline, Git write-permission checks, GitHub CLI session state, remote
  configuration, local helper exclusion, generated package folder absence, PR
  #1001 leakage precheck, and local safety tool availability;
- integration boundaries with Codex prompt templates and the local safety gate
  aggregator.

Follow-up:

- Y-AUTO-15 implements the preflight environment checker.
- APP-BOOT-01 remains the next recommended candidate.

Actual package generation remains blocked.
