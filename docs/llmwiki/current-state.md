# Current State

## Project

- Project: `youtubeダウンロード / MeTube local-only fork`
- Repository: `C:\Users\tomikyo\_projects\youtubeダウンロード`
- Upstream remote: `origin -> https://github.com/alexta69/metube.git`
- Fork remote: `fork -> https://github.com/jsworkht-dotcom/metube.git`
- Local `master` tracks `fork/master`
- Current source of truth: fork `master`

## Repository State

- This project is local-only per recipient. The current premise is controlled
  CLEAN portable distribution to known recipients, where each recipient runs
  the app locally on their own PC.
- Public hosting, Cloudflare/public web deployment, and external SaaS/service
  offering remain prohibited and out of scope.
- Do not open PRs against upstream `alexta69/metube` unless explicitly requested for a
  separate upstream contribution.
- Do not mix upstream PR #1001 files into fork-only work.
- Latest fork `master` baseline:
  `a62e1c67261f7fbf31f970f2abf31c0a7c79c36d` from fork PR #105.

## Current Runtime Security State

### Y-SEC-01 local-only runtime guardrails

- Completed via fork PR #82.
- Merge commit: `e63e282afdb4d710b01d6562a2ffd377c3a3fc32`.
- Adds `LOCAL_ONLY_MODE=true` by default for this fork.
- Y-SEC-01A amends the runtime default bind to `HOST=127.0.0.1`.
- Y-SEC-01A blocks non-loopback `HOST` values when `LOCAL_ONLY_MODE=true`.
- Y-SEC-01B extracts dependency-free local-only security helper logic and adds
  standard-library `unittest` coverage for host/source/public-host/config guard
  decisions.
- Y-SEC-01B reduces the current verification gap when pytest/aiohttp are not
  available, but does not replace full backend pytest verification.
- Y-SEC-01C rejects non-local `Origin` headers for all requests in local-only
  mode, improving localhost/browser-origin hardening for distributed
  local-only builds.
- Requests without `Origin` remain allowed for local non-browser clients, and
  the state-changing `Referer` guard remains in place.
- Adds a local Host allowlist guard for HTTP and static UI requests.
- Adds an Origin / Referer guard for state-changing requests.
- Blocks wildcard CORS in local-only mode.
- Blocks per-download yt-dlp option overrides in local-only mode unless
  `ALLOW_UNSAFE_YTDL_OPTIONS_OVERRIDES=true` is explicitly set.
- Blocks nightly automatic yt-dlp updates in local-only mode unless
  `ALLOW_UNSAFE_NIGHTLY_UPDATE=true` is explicitly set.
- Blocks non-local absolute public host URL values in local-only mode while
  preserving relative defaults.
- Adds minimal security response headers:
  `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, and
  `Cross-Origin-Resource-Policy`.
- No package output, dependency install/update, Docker operation, real
  download, cookie/token/secret handling, public hosting, or safety gate
  change was performed.

### Y-SEC-02 URL intake SSRF / private-network target guard

- Completed via fork PR #83.
- Merge commit: `e54058dc112ae6c29237738b21bff0e3253407ea`.
- Adds `URL_INTAKE_GUARD=true` by default and requires it to remain enabled
  when `LOCAL_ONLY_MODE=true`.
- Adds a dependency-free URL intake helper for user-submitted download and
  subscription URLs.
- Blocks non-HTTP(S) schemes, missing or malformed hosts, URL userinfo,
  localhost/loopback, private/link-local/shared/multicast/reserved IP literals,
  IPv4-mapped IPv6 literals that point to blocked IPv4 ranges, obvious
  internal hostnames such as `.local`, `.home`, `.lan`, `.localhost`, and
  metadata hostnames such as `metadata.google.internal`.
- Unsafe `/add` and `/subscribe` URL intake is rejected before enqueue or
  subscription creation with a generic 400 reason. The raw URL is not echoed in
  the response or log message.
- DNS resolution support exists as an explicit helper option only and is not
  enabled on the request path in this first pass.
- This guard blocks obvious dangerous initial URLs. It does not fully control
  later URLs fetched internally by yt-dlp, and it does not claim complete DNS
  rebinding or downstream redirect protection.
- Verification: dependency-free `unittest` coverage passes with bundled Codex
  Python. Focused pytest/aiohttp API tests were added but not run here because
  `pytest` is not installed and dependency installation was not performed.
- No package output, dependency install/update, Docker operation, public
  hosting, real download, cookie/token/secret handling, frontend change, or
  safety gate change was performed.

### Y-SEC-03 log and filename privacy redaction hardening

- Completed via fork PR #84.
- Merge commit: `aa0200b126d5cdc9d18617280fe733284bf990e6`.
- Adds dependency-free privacy helpers in `app/local_only_security.py` for
  URL log redaction, general text redaction, sensitive-material detection, and
  single-component filename sanitization.
- URL redaction preserves only scheme and hostname for HTTP(S) values and
  removes userinfo, path details, query strings, and fragments.
- Text redaction covers token-like key/value material, bearer authorization
  headers, cookie headers, common local Windows paths, and common local Unix
  paths.
- `/add` and `/subscribe` sanitize non-empty `custom_name_prefix` before queue
  or subscription use, while omitted or empty prefixes remain empty.
- Unsafe URL intake errors remain generic and do not echo the submitted URL.
- Bad-request logging defensively redacts the reason string.
- This is first-pass redaction/sanitization. It does not claim all downstream
  yt-dlp filenames are fully controlled.
- No real download, package output, generated distribution folder, dependency
  install/update, Docker operation, public hosting, cookie/token/secret
  handling, frontend change, package/lockfile change, or safety gate change
  was performed.

### Y-DIST-01 CLEAN portable distribution manifest and forbidden-file checker

- Completed via fork PR #85.
- Merge commit: `f2e2678e3dc986a34f2e5bb0bd65f56d54b2b415`.
- Adds `scripts/check_clean_distribution.py` as a stdlib-only, report-only
  checker for an explicitly provided candidate directory.
- Adds `docs/llmwiki/clean-portable-distribution-manifest.md` as the manifest
  contract for future CLEAN portable distribution review.
- Adds dependency-free `unittest` coverage for missing paths, forbidden
  paths, sensitive filenames, symlinks, conservative secret-like content
  patterns, large-file scan limits, sanitized reports, and JSON output.
- The checker is read-only, blocks findings with a non-zero exit code, does
  not follow symlinks, and does not print matched secret values or file
  contents.
- Future CLEAN share, upload, ZIP, installer, or package generation must pass
  this checker first, but this checker does not approve generation.
- No CLEAN folder, ZIP, installer, package output, dependency install/update,
  Docker operation, real download, cookie/token/secret handling, frontend
  change, package/lockfile change, or existing safety gate behavior change is
  part of this lane.

## Recent Completed Lane Summary (PR #86-#105)

This is the compact planning surface for the recent distribution, CI, and
GitHub-governance lanes. The older per-lane notes remain historical reference.

- Y-DIST is complete through Y-DIST-08:
  PR #86 added report-only metadata verification; PR #91 added recipient-safe
  and first-run verification docs; PR #92 added the readiness matrix; PR #93
  added the human approval checklist; PR #94 added the approved clean candidate
  dry-run plan; PR #102 added the artifact generation approval packet.
  PR #105 completed Y-DIST-08: no generation approval was granted, all artifact
  categories remain `not approved`, and artifact generation remains blocked.
- Y-CI is complete through the reusable `local-fork-safety` display layer:
  PR #88 designed the workflow; PR #89 implemented it; PR #90 confirmed a
  docs-only self-check; PR #95 designed the reusable split; PR #96 implemented
  the split; PR #97 added caller concurrency; PR #99 observed the stable
  displayed check name `local fork safety / local fork safety`.
- Y-GH is complete through required-checks design:
  PR #87 recorded the GitHub connector fallback runbook; PR #98 designed
  branch protection/ruleset strategy; PR #100 designed required-check handling;
  PR #103 standardized the GitHub ready/check/merge fallback flow.
  No branch protection, ruleset, required-check, CODEOWNERS, workflow, or
  GitHub settings mutation has been performed.
- Y-AUTO-OPS-01 completed via PR #104:
  fast safe flow default template adoption for normal low-risk
  docs/report/checker work.
- Current next candidates:
  Y-UX-PLAN-01 establishes the next low-risk beginner UX planning path after
  the Y-DIST-08 hold, followed by `Y-UX-COPY-01`, a quality selector / label
  review follow-up, or another docs/report/checker lane using fast safe flow.
  Artifact generation, ZIP/package/installer creation, GitHub required checks
  implementation, and branch protection mutation are not recommended yet.

### Y-DIST-02 checksum / hash / version / license notice bundle verification

- Completed via fork PR #86.
- Merge commit: `00a90bfa1efd11935aa46b07848d05614d1c744e`.
- Adds `scripts/check_distribution_metadata.py` as a stdlib-only, report-only
  metadata checker for an explicitly provided CLEAN portable distribution
  candidate directory.
- Adds `docs/llmwiki/distribution-metadata-verification.md` as the metadata
  verification contract for future CLEAN portable distribution review.
- Adds dependency-free `unittest` coverage for required metadata files,
  manifest fields, version mismatch, checksum line/path/hash failures,
  duplicate listed paths, extra unlisted file warnings, sanitized secret-like
  license/notice reports, and JSON output.
- The checker requires candidate-root `VERSION.txt`, `MANIFEST.json`,
  `checksums.sha256`, `LICENSE`, and `NOTICE`.
- The checker validates basic version shape, manifest fields, `local_only`,
  distribution type, source commit shape, sha256sum-style checksum entries,
  recomputed SHA-256 matches, duplicate listed paths, missing listed files,
  unsafe checksum paths, and basic license / notice presence and safety.
- The checker runs Y-DIST-01 as a prerequisite and includes those findings in
  its report.
- Future CLEAN share, upload, ZIP, installer, or package generation must pass
  both Y-DIST-01 and Y-DIST-02 first, but neither checker approves generation.
- No metadata generation, checksum generation, CLEAN folder, ZIP, installer,
  package output, dependency install/update, Docker operation, real download,
  cookie/token/secret handling, frontend change, package/lockfile change, or
  existing safety gate behavior change is part of this lane.
- GitHub connector ready-for-review transition failed with
  `Resource not accessible by integration`; human-approved `gh` fallback
  succeeded and squash-merged with an expected head SHA guard.
- Remote branch `codex/y-dist-02-metadata-checker` was deleted after merge.

### Y-GH-OPS-01 GitHub connector fallback runbook closeout

- Scope: docs-only GitHub operations runbook / prompt-template / LLMwiki sync.
- Status: completed via fork PR #87.
- Merge commit: `9a1a262e03da7976850b8dfddacb1576b0572c2c`.
- Purpose:
  - record that GitHub connector ready-for-review / GraphQL mutations can fail
    with `Resource not accessible by integration`;
  - document when human-approved `gh` fallback is acceptable;
  - require expected head SHA checks before ready / merge and an expected-head
    guard for squash merge;
  - record PR #86 as the confirmed operational example.
- Follow-up standardization limits fallback to current-lane approved `pr view`,
  `pr checks`, `pr ready`, guarded `pr merge`, and after-merge branch cleanup;
  it also records token-safe command patterns and stop conditions.
- Completed via fork PR #103 with merge commit
  `926c7e5fa02bfe433f842b164b30d405d446b53f`.
- Not included:
  - GitHub token, secret, cookie, or credential handling;
  - branch protection changes;
  - CODEOWNERS changes;
  - backend/frontend/Docker/CI/package/lockfile changes;
  - dependency installation operations;
  - Docker operations;
  - metadata/checksum/package generation;
  - PR #1001 file changes.

### Y-CI-01 lightweight safety workflow design

- Scope: docs-only GitHub Actions safety workflow design.
- Status: completed via fork PR #88.
- Merge commit: `14508576e249ee65ff4d2d63060cb6b1d4e8e484`.
- Design doc:
  `docs/llmwiki/lightweight-safety-workflow-design.md`.
- Workflow candidate:
  `.github/workflows/local-fork-safety.yml`.
- Candidate workflow name: `local-fork-safety`.
- Initial design:
  - run on `pull_request` targeting `master`;
  - prefer broad PR coverage over path filtering for the first workflow;
  - use `permissions: contents: read`;
  - run existing stdlib-friendly repository safety and clean-package dry-run
    checks;
  - keep warning-only findings as successful CI with log output;
  - fail CI for blockers;
  - keep concurrency for Y-CI-04 unless real PR noise requires it earlier.
- Not implemented:
  - `.github/workflows/` changes;
  - CI implementation;
  - required-check configuration;
  - branch protection mutation;
  - CODEOWNERS addition;
  - backend/frontend/Docker/package/lockfile changes;
  - dependency installation operations;
  - Docker operations;
  - generated package output;
  - metadata/checksum generation.

### Y-CI-02 minimal workflow implementation

- Scope: minimal GitHub Actions PR safety display workflow.
- Status: completed via fork PR #89.
- Merge commit: `66a4a638fef65988c10405398e6e591f0fccb923`.
- Workflow:
  `.github/workflows/local-fork-safety.yml`.
- The `local-fork-safety` workflow is now present on fork `master`.
- Behavior:
  - runs on `pull_request` targeting `master` without path filters;
  - uses `permissions: contents: read`;
  - uses `actions/checkout@v6` with full history for base comparison;
  - creates `fork/master` as a remote-tracking base ref with read-only fetch;
  - runs existing stdlib-friendly repository safety and clean-package dry-run
    checks;
  - parses the clean-package dry-run JSON output;
  - runs the safety wording checker with warning-only output left visible in
    logs;
  - explicitly fails if `動画保存ツール_ローカル専用/` exists;
  - explicitly fails if PR #1001 files appear in the PR diff.
- Not included:
  - dependency installation operations;
  - container image operations;
  - frontend build/test or backend pytest;
  - package, ZIP, installer, CLEAN folder, metadata, or checksum generation;
  - branch protection, required-check configuration, or CODEOWNERS changes;
  - backend/frontend/Docker/package/lockfile changes;
  - cookie/token/secret handling;
  - PR #1001 file changes.
- PR #89's workflow failure was accepted by human review as expected for the
  first workflow-introducing PR, because the check did not exist on the base
  branch before merge.

### Y-CI-02B local-fork-safety docs-only self-check

- Scope: docs-only self-check PR.
- Status: completed via fork PR #90.
- Merge commit: `f235416950868331f5a107e13631899aa7785c21`.
- Purpose:
  - confirm a normal docs-only PR can pass `local-fork-safety`;
  - observe the workflow behavior without modifying `.github/workflows/`.
- Result: `local-fork-safety` succeeded on the docs-only PR.
- Follow-up completed by Y-DIST-03. Keep `Y-CI-02C workflow fix` as a fallback
  only if a later docs-only PR fails unexpectedly.

### Y-DIST-03 recipient-safe runbook and first-run local-only verification

- Scope: docs-only recipient handoff and first-run verification procedure.
- Status: completed via fork PR #91.
- Merge commit: `f43c9a106308ac05a0ef5e32f4cf455a4d88b3e1`.
- Documents:
  - `docs/llmwiki/recipient-safe-runbook.md`
  - `docs/llmwiki/first-run-local-only-verification.md`
- Purpose:
  - define recipient-safe local-only instructions;
  - define first-run local-only verification items;
  - standardize stop conditions before distribution, first-run guidance, or
    launch confirmation.
- Relation:
  - Y-DIST-01 covers CLEAN candidate forbidden-file / secret-like content /
    manifest baseline checking.
  - Y-DIST-02 covers version / manifest / checksum / license / notice metadata
    checking.
  - Y-DIST-03 covers recipient-safe procedure only; it does not generate
    distribution output.
- Not included:
  - CLEAN folder generation;
  - ZIP, installer, or package output;
  - metadata or checksum generation;
  - real download verification;
  - dependency installation operations;
  - container image operations;
  - backend/frontend runtime changes;
  - yt-dlp extractor or download queue changes;
  - public hosting;
  - cookie/token/secret handling;
  - PR #1001 file changes.

### Y-DIST-04 distribution readiness matrix

- Scope: docs-only distribution readiness matrix.
- Status: completed via fork PR #92.
- Merge commit: `cca229cc2b842cda3778546236358069e6938ab3`.
- Document:
  `docs/llmwiki/distribution-readiness-matrix.md`.
- Purpose:
  - list current readiness by category;
  - show blocked, human-review-required, warning-only, and not-yet-applicable
    items;
  - keep artifact generation blocked until a separate explicit human approval
    task.
- Recommended next candidate after completion:
  `Y-DIST-05 human approval checklist before any artifact generation`.
- Not included:
  - CLEAN folder generation;
  - ZIP, installer, or package output;
  - metadata or checksum generation;
  - real download verification;
  - dependency installation operations;
  - container image operations;
  - backend/frontend runtime changes;
  - `.github/workflows/` changes;
  - branch protection / required-check / CODEOWNERS changes;
  - public hosting;
  - cookie/token/secret handling;
  - PR #1001 file changes.

### Y-DIST-05 human approval checklist before artifact generation

- Scope: docs-only human approval checklist.
- Status: completed via fork PR #93.
- Merge commit: `26d1983105d61441d6abd19495a4a96508a986e4`.
- Document:
  `docs/llmwiki/artifact-generation-approval-checklist.md`.
- Purpose:
  - state that artifact generation is blocked by default;
  - define the exact approval categories and required approval fields;
  - define required pre-generation checks, post-generation checks, and stop
    conditions before any future artifact generation lane.
- Current approval status: all artifact categories remain `not approved`.
- Not included:
  - CLEAN folder generation;
  - ZIP, installer, or package output;
  - metadata or checksum generation;
  - real download verification;
  - dependency installation operations;
  - container image operations;
  - backend/frontend runtime changes;
  - public hosting;
  - cookie/token/secret handling;
  - PR #1001 file changes.

### Y-DIST-06 approved clean candidate dry-run plan

- Scope: docs-only approved clean candidate dry-run plan.
- Status: completed via fork PR #94.
- Merge commit: `72efd6c4e42e3c27ed020cee5b6e1f64ec7acffe`.
- Document:
  `docs/llmwiki/approved-clean-candidate-dry-run-plan.md`.
- Purpose:
  - define the future dry-run principle after explicit Y-DIST-05 approval;
  - record required prerequisites, planned phases, candidate path rules,
    checker usage, report template, and stop conditions;
  - keep candidate-directory checker execution `not_applicable_yet` until an
    approved candidate exists.
- Not included:
  - CLEAN folder generation;
  - ZIP, installer, or package output;
  - metadata or checksum generation;
  - real downloads;
  - dependency installation operations;
  - No Docker pull/build operations;
  - backend/frontend runtime changes;
  - public hosting;
  - cookie/token/secret handling;
  - PR #1001 file changes.

### Y-DIST-07 artifact generation approval packet

- Scope: docs-only approval packet for future artifact generation review.
- Status: completed via fork PR #102.
- Merge commit: `f4a644fd97c869f305465b8e51d837bdd310b2e5`.
- Document:
  `docs/llmwiki/artifact-generation-approval-packet.md`.
- Purpose:
  - state that Y-DIST-07 does not approve generation;
  - record the current baseline as `fork/master` at
    `df99701477d05d4f4b6e5127ee8588e3da5252d5`;
  - keep all artifact categories `not approved`;
  - define future approval fields, pre-generation checks, post-generation
    checks, stop conditions, and how Y-DIST-01 through Y-DIST-06 feed into the
    approval decision.
- Not included:
  - CLEAN folder generation;
  - `動画保存ツール_ローカル専用/` creation;
  - ZIP output, installer output, or package output;
  - metadata or checksum generation;
  - real download verification;
  - recipient handoff or sharing;
  - dependency installation operations;
  - Docker operations;
  - backend/frontend/Docker/CI/package/lockfile changes;
  - `.github/workflows/` changes;
  - GitHub settings, branch protection, ruleset, required-check, or CODEOWNERS
    mutation;
  - `.gitignore` changes;
  - cookie/token/secret handling;
  - PR #1001 file changes.

### Y-DIST-08 approval packet no-generation hold record

- Scope: docs-only approval packet review status / no-generation hold record.
- Status: completed via fork PR #105.
- Merge commit: `a62e1c67261f7fbf31f970f2abf31c0a7c79c36d`.
- Baseline: `fork/master` at
  `6973732e2483548201a81c1debd88cbea98f5b8f`, after fork PR #104 fast safe
  flow template adoption.
- Decision:
  - approval packet reviewed for planning continuity;
  - no artifact generation approval granted;
  - all artifact categories remain `not approved`;
  - generation remains blocked and on `HOLD`;
  - no candidate path, output path, or source commit is approved for
    generation;
  - no real download verification is approved;
  - no recipient handoff or sharing is approved.
- Approval categories remain `not approved`:
  CLEAN folder generation, metadata generation, checksum generation, ZIP
  output, installer output, package output, real download verification, and
  recipient handoff / sharing.
- Recommended next work:
  continue low-risk docs/report/checker/UX planning lanes using fast safe flow.
- Not recommended yet:
  artifact generation, ZIP/package/installer creation, GitHub required checks
  implementation, or branch protection mutation.
- Not included:
  - CLEAN folder generation;
  - `動画保存ツール_ローカル専用/` creation;
  - ZIP output, installer output, or package output;
  - metadata or checksum generation;
  - real download verification;
  - recipient handoff or sharing;
  - dependency installation operations;
  - Docker operations;
  - backend/frontend/Docker/CI/package/lockfile changes;
  - `.github/workflows/` changes;
  - GitHub settings, branch protection, ruleset, required-check, or CODEOWNERS
    mutation;
  - `.gitignore` changes;
  - cookie/token/secret handling;
  - PR #1001 file changes.

### Y-UX-PLAN-01 beginner UX next-action planning

- Scope: docs-only beginner UX next-action planning / roadmap / handoff sync.
- Document:
  `docs/llmwiki/beginner-ux-next-action-plan.md`.
- Purpose:
  move attention away from blocked artifact generation and back to safe
  beginner UX planning for screen quality, local-only guidance, safe-use copy,
  help/troubleshooting flow, and future UI quality work.
- Current UX baseline:
  Japanese-localized UI exists, local-only safety posture exists, beginner
  guide source docs exist, and package generation remains blocked.
- Risk boundaries:
  docs-only UX planning is allowed via fast safe flow; frontend copy-only
  implementation must be a later separate lane with UI files explicitly scoped;
  runtime behavior changes are not part of Y-UX-PLAN-01.
- Recommended first next lane:
  `Y-UX-COPY-01 safe-use microcopy review` or a quality selector / label review
  follow-up. Historical `Y-UI-QUALITY-01` through `Y-UI-QUALITY-03` are already
  complete, so new implementation work should use a non-colliding lane name.
- Not included:
  frontend code, backend code, runtime behavior, artifact generation, package
  output, generated folders, dependency changes, Docker operations,
  `.github/workflows/` changes, GitHub settings mutation, `.gitignore` changes,
  cookie/token/secret handling, public hosting, or bypass guidance.

### Y-CI-03 reusable local safety workflow design

- Scope: docs-only reusable workflow design for the existing
  `local-fork-safety` PR safety display layer.
- Status: completed via fork PR #95.
- Merge commit: `c64b935fc02b7893e8be38d13a53e8b26adf91cf`.
- Document:
  `docs/llmwiki/reusable-local-safety-workflow-design.md`.
- Future workflow candidate:
  `.github/workflows/reusable-local-safety.yml`.
- Future implementation lane:
  `Y-CI-03B reusable workflow implementation`.
- Purpose:
  - document the current `.github/workflows/local-fork-safety.yml` baseline;
  - define a future `workflow_call` reusable workflow structure;
  - keep `.github/workflows/` unchanged in this docs-only PR;
  - preserve `permissions: contents: read`, no artifact upload, no dependency
    installation operations, no Docker operations, and no package output.
- Not included:
  - `.github/workflows/` changes;
  - dependency installation operations;
  - container image retrieval/build operations;
  - frontend build/test or backend pytest;
  - package, ZIP, installer, CLEAN folder, metadata, checksum, or generated
    artifact output;
  - branch protection, required-check configuration, or CODEOWNERS changes;
  - cookie/token/secret handling;
  - PR #1001 file changes.

### Y-CI-03B reusable workflow implementation

- Scope: CI workflow implementation plus minimal docs sync.
- Status: completed via fork PR #96.
- Branch: `codex/y-ci-03b-reusable-workflow-implementation`.
- fork `master` after merge:
  `2d59c4e4034d772d029b776497136e9bf67b6cd5`.
- Workflow changes:
  - `.github/workflows/local-fork-safety.yml` remains the `pull_request` to
    `master` PR visibility layer and now calls the reusable workflow;
  - `.github/workflows/reusable-local-safety.yml` is the `workflow_call`
    target and owns the existing local safety steps.
- Permissions:
  - caller keeps `permissions: contents: read`;
  - reusable workflow also declares `permissions: contents: read`;
  - permissions are not broadened.
- Expected check behavior:
  - `local-fork-safety` starts on PRs targeting `master`;
  - the caller invokes `reusable-local-safety.yml`;
  - `local fork safety` runs the same checkout, fork/master base-ref, repo
    safety, clean dry-run, JSON, safety wording, generated-folder absence, and
    PR #1001 absence checks.
- Not included:
  - dependency installation or update;
  - container image retrieval/build operations;
  - package, ZIP, installer, CLEAN folder, metadata, checksum, or artifact
    output;
  - branch protection, required-check configuration, or CODEOWNERS changes;
  - `pull_request_target`, secrets, `secrets: inherit`, artifact upload, or
    cache additions;
  - backend/frontend/Docker/package/lockfile changes;
  - cookie/token/secret handling;
  - PR #1001 file changes.
- Stop conditions:
  - workflow syntax cannot be validated;
  - `local-fork-safety` does not run or does not call the reusable workflow;
  - checks are silently skipped;
  - permissions expand beyond `contents: read`;
  - generated package output, PR #1001 files, or
    `動画保存ツール_ローカル専用/` appear.

### Y-CI-04 concurrency / cancel-in-progress

- Scope: CI workflow implementation plus minimal docs sync.
- Status: completed via fork PR #97.
- fork `master` after merge:
  `becdf346956cb61b985df93637ab5c121884e49c`.
- Workflow changes:
  - `.github/workflows/local-fork-safety.yml` remains the `pull_request` to
    `master` PR visibility layer and still calls
    `.github/workflows/reusable-local-safety.yml`;
  - the caller now has workflow-level concurrency:
    `group: ${{ github.workflow }}-${{ github.ref }}`;
  - `cancel-in-progress: true` cancels older local safety runs for the same PR
    ref;
  - `.github/workflows/reusable-local-safety.yml` safety steps are unchanged.
- Permissions:
  - caller keeps `permissions: contents: read`;
  - reusable workflow keeps `permissions: contents: read`;
  - permissions are not broadened.
- Expected check behavior:
  - `local-fork-safety` starts on PRs targeting `master`;
  - the caller invokes `reusable-local-safety.yml`;
  - `local fork safety` runs the same repository safety, clean dry-run, JSON,
    safety wording, generated-folder absence, and PR #1001 absence checks;
  - older runs in the same workflow/ref concurrency group are canceled when a
    newer run starts.
- Expected CI-scope blocker:
  - local and PR safety checks may classify `.github/workflows/` changes as
    human-review-required blockers;
  - if that happens, the expected blocker should be limited to the workflow
    file change and should not include dependency installation/update, Docker,
    artifact generation, package output, PR #1001 files, or generated package
    folders.
- Not included:
  - dependency installation or update;
  - container image retrieval/build operations;
  - package, ZIP, installer, CLEAN folder, metadata, checksum, or artifact
    output;
  - branch protection, required-check configuration, or CODEOWNERS changes;
  - `pull_request_target`, secrets, `secrets: inherit`, artifact upload, or
    cache additions;
  - backend/frontend/Docker/package/lockfile changes;
  - cookie/token/secret handling;
  - PR #1001 file changes.
- Stop conditions:
  - workflow syntax cannot be validated;
  - `local-fork-safety` does not run or does not call the reusable workflow;
  - checks are silently skipped;
  - permissions expand beyond `contents: read`;
  - generated package output, PR #1001 files, or
    `動画保存ツール_ローカル専用/` appear.

### Y-GH-01 branch protection / ruleset design

- Scope: docs-only branch protection / ruleset strategy.
- Status: completed via fork PR #98.
- fork `master` after merge:
  `1bb28de03e3257cedb097301672a30cdd1052f18`.
- Design doc:
  `docs/llmwiki/branch-protection-design.md`.
- Purpose:
  - record candidate branch protection and ruleset policy for fork `master`;
  - document required-check naming risks after the reusable workflow split;
  - define staged adoption, approval requirements, rollback, and stop
    conditions.
- Current recommendation:
  - do not mutate GitHub settings in Y-GH-01;
  - do not enable required checks until the displayed check name is stable;
  - use Y-CI-05 observation before Y-GH-02 required-check design.
- Not included:
  - branch protection mutation;
  - ruleset creation or mutation;
  - required-check configuration;
  - required reviews or CODEOWNERS;
  - GitHub repository settings mutation;
  - `.github/workflows/`, backend, frontend, Docker, package, lockfile, or
    `.gitignore` changes;
  - dependency install/update, Docker operations, generated output, metadata,
    checksums, real downloads, credentials, or PR #1001 files.

### Y-CI-05 post-workflow-change observation

- Scope: docs-only observation PR.
- Status: completed via fork PR #99.
- fork `master` after merge:
  `e77e68c56a369c3ae962cf0abcbe958ce36a2101`.
- Observation doc:
  `docs/llmwiki/post-workflow-change-observation.md`.
- Purpose:
  - observe normal docs-only PR behavior after Y-CI-03B / Y-CI-04;
  - record the exact displayed GitHub check name;
  - confirm `local-fork-safety` still passes without workflow changes;
  - provide one more observation before Y-GH-02 required-check design.
- Observed result:
  - displayed check name: `local fork safety / local fork safety`;
  - check result: pass;
  - workflow files changed: no;
  - GitHub settings changed: no.
- Not included:
  - `.github/workflows/` changes;
  - GitHub settings, branch protection, ruleset, required-check, or CODEOWNERS
    mutation;
  - dependency install/update, Docker/container operations, build/test, pytest,
    generated output, metadata, checksums, real downloads, credentials, or PR
    #1001 files.

### Y-GH-02 required checks design

- Scope: docs-only required checks design.
- Status: completed via fork PR #100.
- Merge commit: `34497e8918bbc12b7ea457eb6cc48c7c9d8c963b`.
- Design doc:
  `docs/llmwiki/required-checks-design.md`.
- Current required-check candidate:
  `local fork safety / local fork safety`.
- Evidence:
  - observed passing on Y-GH-01 PR #98;
  - observed passing again on Y-CI-05 PR #99.
- Current recommendation:
  - do not implement required checks yet;
  - verify the exact GitHub UI/API check name immediately before any future
    implementation;
  - prefer a future explicit human-approved implementation lane after a
    rollback path is accepted.
- Main risk:
  - workflow-file PRs intentionally hit CI-scope local safety blockers, so a
    required local safety check can block expected human-approved workflow
    changes without a documented exception and rollback path.
- Not included:
  - GitHub settings, branch protection, ruleset, required-check, or CODEOWNERS
    mutation;
  - `.github/workflows/` changes;
  - dependency install/update, Docker/container operations, build/test, pytest,
    generated output, metadata, checksums, real downloads, credentials, or PR
    #1001 files.

## Completed Work

### Y-03 local-only Docker profile

- Upstream PR #1001 is Ready for review.
- Branch `local-only-docker-profile` remains while PR #1001 is open.
- Keep `docker-compose.local.yml` and `docs/local-only.md` out of unrelated fork work.

### Y-04 Japanese static UI copy

- Fork PR #1 was merged.
- Merge commit: `0cc8dd602ccaa0944630c56322e6b753133f6961`
- Scope: static Japanese UI copy for the fork.

### Y-05 readonly update-status

- Fork PR #2 was merged.
- Merge commit: `37256d5b8a885aac0f7e323f413409769055cc83`
- Scope: readonly update-status baseline.

### Y-05D runtime verification

- Runtime verification confirmed `/update-status` remains readonly.
- `METUBE_VERSION=dev` was found to display `更新確認失敗` even when metadata
  fetches succeeded, because `dev` could not be compared with release tags.
- `METUBE_VERSION=2026.06.06` displayed `最新`.
- `METUBE_VERSION=0.0.0` displayed `更新あり`.
- No update execution, Docker pull, git pull, restart, pip install, or
  cookie/token/secret exposure was observed.

### Y-05E dev version status fix

- Fork PR #4 was merged.
- Merge commit: `af6987532a741cd680d8b747562b2f2971b9c229`
- Scope: treat `METUBE_VERSION=dev` as `development` and show `開発版` in
  the footer while preserving real `check_failed` behavior.

### Y-05G readonly update preflight report

- Fork PR #7 was merged.
- PR URL: `https://github.com/jsworkht-dotcom/metube/pull/7`
- Merge commit: `bfbecdb`
- Scope: readonly update preflight report for backup and rollback readiness.
- Changed files:
  - `app/main.py`
  - `app/update_preflight.py`
  - `app/tests/test_update_preflight.py`
- Implemented:
  - readonly `/update-preflight` report
  - backup / rollback readiness JSON report
  - update apply readiness as information only with `can_apply_update: false`
- Not implemented:
  - update execution
  - backup creation
  - rollback creation
  - Docker pull
  - git pull / merge / rebase
  - restart
  - pip install / package update

### Y-05H manual-approval update apply design audit

- Scope: docs-only design audit for future manual-approval update apply.
- Design document: `docs/llmwiki/manual-update-apply-design.md`
- Defines:
  - update target classification for source, Docker, yt-dlp, and state/data
  - manual approval flow
  - future UI/API boundaries
  - stop conditions
  - rollback hand-off requirements
- Not implemented:
  - update execution
  - update apply endpoint
  - update button
  - backup creation
  - rollback creation
  - Docker pull
  - git pull / merge / rebase
  - restart
  - pip install / package update

### Y-05I dry-run / prepare-only update apply contract audit

- Scope: docs-only dry-run / prepare-only contract audit.
- Contract document: `docs/llmwiki/dry-run-update-contract.md`
- Defines:
  - dry-run as readonly planning only
  - prepare-only as validation only, with no backup or rollback creation in the
    first prepare stage
  - future `/update-plan`, `/update-prepare`, `/update-apply`, and
    `/update-rollback` endpoint boundaries
  - conservative response fields, stop conditions, and UI constraints
- Not implemented:
  - update execution
  - update prepare endpoint
  - update apply endpoint
  - update button
  - backup creation
  - rollback creation
  - Docker pull
  - git pull / merge / rebase
  - restart
  - pip install / package update

### Y-05J readonly update-plan contract-only endpoint

- Scope: readonly `/update-plan` contract-only endpoint.
- Implemented:
  - readonly update-plan helper
  - `GET /update-plan` endpoint
  - blocked-by-default response contract
  - update-plan tests
- Contract behavior:
  - `can_prepare` remains `false`
  - `can_apply` remains `false`
  - planned steps and blocked reasons are reported as information only
- Not implemented:
  - update execution
  - update prepare endpoint
  - update apply endpoint
  - update rollback endpoint
  - update button
  - backup creation
  - rollback creation
  - Docker pull
  - git pull / merge / rebase
  - restart
  - pip install / package update

### Y-05K-R update-plan runtime verification

- Runtime verification succeeded after Docker Desktop / Docker daemon recovery.
- Docker: Docker Desktop `4.76.0`, Engine `29.5.2`.
- Image: existing local `ghcr.io/alexta69/metube:latest` used with
  `--pull=never`.
- Bind: `127.0.0.1:18082` only.
- Mounts: app and built UI were mounted read-only.
- `/update-plan` response:
  - `overall: blocked`
  - `can_prepare: false`
  - `can_apply: false`
  - `blocked_reasons` present
  - `planned_steps` present
  - rollback/doc references present
- Related endpoints:
  - `/update-status`: `latest`
  - `/update-preflight`: `not_ready`, `can_apply_update: false`
  - `/version`: `version: 2026.06.06`, `yt-dlp: 2026.03.17`
- No secret/token/cookie values appeared in responses or logs.
- No update execution, Docker pull, git pull / merge / rebase, restart, pip
  install/update, backup creation, or rollback creation occurred.
- Temporary container was stopped and removed.
- Read-only mount `chown ... Read-only file system` warnings were observed
  during verification and are expected for that test launch style.

### Y-05 readonly update readiness phase closeout

- Y-05 readonly update readiness is complete for now.
- Completed scope:
  - readonly `/update-status`
  - readonly `/update-preflight`
  - readonly `/update-plan`
  - backup / rollback planning
  - manual approval design
  - dry-run / prepare-only contract
  - runtime verification for `/update-plan`
- Update execution remains intentionally not implemented.
- Still not implemented:
  - update apply
  - update prepare
  - update rollback
  - update button
  - backup creation
  - rollback creation
  - Docker pull
  - git pull / merge / rebase
  - restart
  - pip install / package update

### Y-06A Dockerless desktop distribution feasibility audit

- Scope: docs-only feasibility audit for Dockerless desktop distribution.
- Audit document:
  `docs/llmwiki/dockerless-desktop-distribution-feasibility.md`
- Outcome:
  - Dockerless Windows/macOS desktop distribution is feasible for local-only
    personal use, but not beginner-ready from the current repository state.
  - Tauri is the preferred first candidate.
  - Electron remains the fallback if Tauri sidecar, WebView, or signing friction
    becomes unacceptable.
  - WebView2 is a Windows-only fallback and is not the primary path because
    macOS parity is required.
- Recommended architecture:
  - Tauri shell
  - existing Angular UI reused as built static assets
  - Python backend packaged as a sidecar, likely PyInstaller one-folder output
  - bundled platform-specific ffmpeg
  - desktop launcher forcing `HOST=127.0.0.1` and per-user state/download/temp
    paths
- Main blockers before beginner distribution:
  - backend lifecycle and close-safety contract
  - desktop-specific path contract
  - ffmpeg / yt-dlp / Deno / bgutil packaging and license review
  - Windows SmartScreen and macOS Gatekeeper / notarization story
  - cookie/token/secret features excluded from the beginner desktop flow
- Not implemented:
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06B desktop sidecar lifecycle and package contract docs

- Scope: docs-only lifecycle and package contract for a future Level 3
  Dockerless desktop-like distribution.
- Contract document:
  `docs/llmwiki/desktop-sidecar-lifecycle-contract.md`
- Outcome:
  - Defined desktop wrapper ownership for backend sidecar start, readiness,
    monitoring, stop, close confirmation, and abnormal-exit recovery.
  - Defined required desktop env overrides, including `HOST=127.0.0.1` and
    per-user download/state/temp paths.
  - Defined package contents, package exclusions, Windows/macOS package
    boundaries, and beginner `.html` / `.txt` guide requirements.
  - Kept cookie/token/secret handling, update apply, Docker pull, package
    install/update, public hosting, ads, and implementation work out of scope.
- Not implemented:
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06C desktop package manifest and beginner guide skeleton docs

- Scope: docs-only package manifest and beginner guide skeleton for a future
  Level 3 beginner desktop distribution.
- Manifest document:
  `docs/llmwiki/desktop-package-manifest.md`
- Guide skeleton document:
  `docs/llmwiki/beginner-guide-skeleton.md`
- Outcome:
  - Defined the future user-facing package root:
    `動画保存ツール_ローカル専用/`.
  - Fixed primary beginner guide as `00_最初に開いてください.html`, fallback as
    `00_最初に開いてください.txt`, and Markdown as developer/LLMwiki material.
  - Defined Windows and macOS package skeletons, warning/signing boundaries,
    include/exclude rules, generated manifest candidates, user data path
    templates, config sample boundaries, notices, and checksum candidates.
  - Kept build/package generation, Tauri/Electron/WebView2 implementation,
    installers, signing, update apply, Docker pull, dependency install/update,
    cookie/token/secret handling, public hosting, ads, and implementation work
    out of scope.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package generator
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06D clean-package generator dry-run contract docs

- Scope: docs-only dry-run contract for a future clean beginner package
  generator.
- Contract document:
  `docs/llmwiki/clean-package-dry-run-contract.md`
- Outcome:
  - Defined dry-run as report-only planning before any clean package files are
    copied or generated.
  - Defined future command candidates, JSON/Markdown report shape, exit code
    policy, planned output manifest, include/exclude rules, validation gates,
    and blocked conditions.
  - Fixed safety checks for forbidden paths, forbidden filenames,
    secret-like content patterns, large files, missing guides/notices,
    local-only notice requirements, Windows/macOS package section completeness,
    generated folder presence, and PR #1001 leakage.
  - Kept actual package generation, clean-package generator implementation,
    Tauri/Electron/WebView2 implementation, build/package commands,
    dependency install/update, Docker pull, update apply, cookie/token/secret
    handling, public hosting, ads, and upstream PR #1001 work out of scope.
- Not implemented:
  - clean-package generator script
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build or copy behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06E report-only clean-package dry-run script

- Scope: stdlib-only dry-run script and minimal LLMwiki sync.
- Script:
  `scripts/clean_package_dry_run.py`
- Outcome:
  - Prints a human-readable clean-package dry-run report.
  - Reports the planned `動画保存ツール_ローカル専用/` package root and manifest.
  - Treats forbidden repository paths as excluded, not copied.
  - Blocks generated package-folder presence, forbidden filename families,
    forbidden content pattern families, and PR #1001 file leakage.
  - Reports only sanitized path, line, and pattern-family details for
    secret-like content checks. Matched values are not printed.
  - Uses exit code `0` for OK, `1` for blockers, and `2` for CLI usage errors.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06F beginner guide source and license notice review

- Scope: docs-only review for future beginner guide source candidates and
  license/notice planning.
- Guide source plan:
  `docs/llmwiki/beginner-guide-source-plan.md`
- License/notice plan:
  `docs/llmwiki/license-notice-plan.md`
- Outcome:
  - Defined future source candidates for `00_最初に開いてください.html`,
    `00_最初に開いてください.txt`, `03_使い方.*`, `04_困ったとき.*`, and
    `05_安全な使い方.html`.
  - Defined beginner wording rules: Japanese-first, local-only, concrete
    actions, and no normal-flow Docker / terminal / Git / Python / Node.js /
    package-manager jargon.
  - Defined package placement candidates for guides, troubleshooting pages,
    developer docs, license directories, notice directories, and a future
    license-notice manifest.
  - Identified notice categories for MeTube, yt-dlp, ffmpeg, Python runtime,
    Python dependencies, frontend dependencies, and future Tauri/Electron
    runtime pieces if implemented later.
  - Selected the next PR candidate: add non-blocking missing guide-source and
    missing notice-source warnings to `scripts/clean_package_dry_run.py`.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - license text copying
  - notice bundle generation
  - dry-run script changes
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06G clean-package dry-run guide/notice warning hardening

- Scope: dry-run script warning hardening and minimal LLMwiki sync.
- Script:
  `scripts/clean_package_dry_run.py`
- Outcome:
  - Added nonblocking warnings for planned-but-missing beginner guide source
    candidates.
  - Added nonblocking warnings for planned-but-missing license/notice source
    candidates.
  - Added nonblocking warnings for local-only safety notice and Windows/macOS
    section source coverage.
  - Kept dry-run `Status: OK` and exit code `0` when only warnings are present.
  - Preserved existing blocking behavior for generated package folders,
    forbidden filename families, secret-like content findings, and PR #1001
    leakage.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - license text copying
  - notice bundle generation
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06H first beginner guide source draft

- Scope: source-only first-open beginner guide draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-guides/00-first-open.html.source.md`
- Outcome:
  - Added the first source candidate for future
    `動画保存ツール_ローカル専用/00_最初に開いてください.html`.
  - Kept the draft as Markdown source material only, not a generated package
    guide.
  - Structured the draft for a future HTML page with hero copy, first-step
    cards, a warning box, in-app help cards, troubleshooting cards, and a
    footer note.
  - Covered local-only use, allowed-content boundaries, start, URL paste,
    save, open save folder, and stop/quit behavior.
  - Covered the close-safety note that users should use `停止して終了` because
    closing with X may not stop the background process cleanly.
  - Reduced clean-package dry-run warning output by satisfying the planned
    first-open HTML source, local-only safety source, and Windows/macOS section
    source candidate checks.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06I first-open TXT fallback source draft

- Scope: source-only first-open TXT fallback draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-guides/00-first-open.txt.source.md`
- Outcome:
  - Added the TXT fallback source candidate for future
    `動画保存ツール_ローカル専用/00_最初に開いてください.txt`.
  - Kept the draft shorter than the HTML source and readable in a normal text
    editor.
  - Covered what the tool is, the short start/save/open-folder/stop flow,
    safe-use boundaries, troubleshooting entry points, and the HTML guide
    hand-off.
  - Reduced clean-package dry-run warning output by satisfying the planned
    first-open TXT source and local-only TXT safety source checks.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06J how-to-use HTML guide source draft

- Scope: source-only everyday-use HTML guide draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-guides/03-how-to-use.html.source.md`
- Outcome:
  - Added the HTML source candidate for future
    `動画保存ツール_ローカル専用/03_使い方.html`.
  - Structured the draft for a future HTML page with hero copy, quick steps,
    action cards, format cards, status explanation cards, a warning box,
    troubleshooting link cards, and a footer note.
  - Covered start, URL paste, save-format selection, save, open save folder,
    status reading, retry guidance, and stop/quit behavior.
  - Kept beginner-facing copy short, local-only, and reusable for future
    in-app help wording.
  - Reduced clean-package dry-run warning output by satisfying the planned
    how-to-use HTML source candidate check.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06K how-to-use TXT fallback source draft

- Scope: source-only everyday-use TXT fallback draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-guides/03-how-to-use.txt.source.md`
- Outcome:
  - Added the TXT fallback source candidate for future
    `動画保存ツール_ローカル専用/03_使い方.txt`.
  - Kept the draft shorter than the HTML source and readable in a normal text
    editor.
  - Covered basic save steps, save-format choices, saving/completion behavior,
    stop/quit behavior, safe-use boundaries, and the HTML guide hand-off.
  - Reduced clean-package dry-run warning output by satisfying the planned
    how-to-use TXT source candidate check.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06L troubleshooting HTML source draft

- Scope: source-only troubleshooting HTML guide draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-guides/04-troubleshooting.html.source.md`
- Outcome:
  - Added the HTML source candidate for future
    `動画保存ツール_ローカル専用/04_困ったとき.html`.
  - Structured the draft for future HTML conversion with hero copy, a quick
    checklist, trouble cards, a warning box, a safe-use reminder, and a footer
    note.
  - Covered first checks, common beginner trouble cases, gentle error-message
    examples, safe stop/quit behavior, save-folder guidance, update-display
    uncertainty, and safe-use boundaries.
  - Reduced clean-package dry-run warning output by satisfying the planned
    troubleshooting HTML source candidate check.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06M troubleshooting TXT fallback source draft

- Scope: source-only troubleshooting TXT fallback draft and minimal LLMwiki
  sync.
- Source draft:
  `docs/llmwiki/package-guides/04-troubleshooting.txt.source.md`
- Outcome:
  - Added the TXT fallback source candidate for future
    `動画保存ツール_ローカル専用/04_困ったとき.txt`.
  - Kept the draft shorter than the HTML source and readable in a normal text
    editor.
  - Covered first actions, common trouble cases, stop/quit behavior, safe-use
    boundaries, and the HTML guide hand-off.
  - Reduced clean-package dry-run warning output by satisfying the planned
    troubleshooting TXT source candidate check.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06N safe-use HTML source draft

- Scope: source-only safe-use HTML guide draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-guides/05-safe-use.html.source.md`
- Outcome:
  - Added the HTML source candidate for future
    `動画保存ツール_ローカル専用/05_安全な使い方.html`.
  - Structured the draft for future HTML conversion with hero copy, safe-use
    cards, do / do-not cards, a sensitive-data warning box, an update-safety
    note, and a footer note.
  - Covered local-only personal use, allowed examples, prohibited uses,
    sensitive-data sharing boundaries, safe trouble actions, and update safety.
  - Reduced clean-package dry-run warning output by satisfying the planned
    safe-use HTML source and safe-use boundary source checks.
- Not implemented:
  - generated distribution folder
  - actual `.html` / `.txt` guide files
  - package build, copy, zip, or generator behavior
  - license text copying
  - notice bundle generation
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - update apply

### Y-06O MeTube notice source draft

- Scope: source-only MeTube notice draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/metube-notice.source.md`
- Outcome:
  - Added the first notice source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/notices/MeTube-notice.txt`.
  - Kept the draft as Markdown source material only, not a generated notice
    file or license bundle.
  - Recorded local source candidates, package placement candidates, a short
    beginner-facing license pointer, a developer-facing notice draft, manifest
    candidate fields, and future review checklist items.
  - Reduced clean-package dry-run warning output by satisfying the planned
    MeTube notice source candidate check.
- Not implemented:
  - generated distribution folder
  - actual notice files
  - actual license bundle
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - 更新適用機能

### Y-06P yt-dlp notice source draft

- Scope: source-only yt-dlp notice draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/yt-dlp-notice.source.md`
- Outcome:
  - Added the yt-dlp notice source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/notices/yt-dlp-notice.txt`.
  - Kept the draft as Markdown source material only, not a generated notice
    file or license bundle.
  - Recorded local dependency candidates from `pyproject.toml`, `uv.lock`, and
    previous runtime `/version` verification.
  - Recorded official project and package source URL candidates, a short
    beginner-facing notice pointer, a developer-facing notice draft, manifest
    candidate fields, and future review checklist items.
  - Preserved separate future review for yt-dlp extras and transitive
    dependencies such as `curl-cffi` and Deno-related pieces.
- Not implemented:
  - generated distribution folder
  - actual notice files
  - actual license bundle
  - transitive dependency license inventory
  - standalone yt-dlp executable review
  - yt-dlp install or update behavior
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - 更新適用機能

### Y-06Q FFmpeg notice source draft

- Scope: source-only FFmpeg notice draft.
- Source draft:
  `docs/llmwiki/package-notices/ffmpeg-notice.source.md`
- Outcome:
  - Added the FFmpeg notice source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/notices/ffmpeg-notice.txt`.
  - Recorded OS-specific notice placement candidates for
    `Windows用/notices/ffmpeg-notice.txt` and
    `Mac用/notices/ffmpeg-notice.txt`.
  - Kept the draft as Markdown source material only, not a generated notice
    file or license bundle.
  - Recorded current local FFmpeg usage candidates from `Dockerfile`,
    `app/dl_formats.py`, `app/ytdl.py`, and Dockerless package planning docs.
  - Preserved required future review for selected binary provider, version,
    target OS, architecture, build configuration, LGPL/GPL status, source
    availability, and patent-sensitive/nonfree options.
- Not implemented:
  - generated distribution folder
  - actual notice files
  - actual license bundle
  - selected FFmpeg binary approval
  - FFmpeg download, install, or update behavior
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - 更新適用機能

### Y-06R Python runtime notice source draft

- Scope: source-only Python runtime notice draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/python-runtime-notice.source.md`
- Outcome:
  - Added the Python runtime notice source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/notices/python-runtime-notice.txt`.
  - Recorded OS-specific notice placement candidates for
    `Windows用/notices/python-runtime-notice.txt` and
    `Mac用/notices/python-runtime-notice.txt`.
  - Kept the draft as Markdown source material only, not a generated notice
    file, notice bundle, runtime bundle, or legal conclusion.
  - Recorded local runtime candidates from `pyproject.toml`, `Dockerfile`, and
    Dockerless package planning docs.
  - Recorded official Python source / license URL candidates and kept the
    exact bundled runtime artifact as a future review item.
  - Preserved separate future review for bundled Python dependencies,
    standard-library incorporated software, native libraries, and any bundler
    runtime pieces.
- Not implemented:
  - generated distribution folder
  - actual notice files
  - actual license bundle
  - selected Python runtime approval
  - Python download, install, build, or update behavior
  - PyInstaller spec files
  - Python dependency license inventory
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - 更新適用機能

### Y-06S frontend dependency notice source draft

- Scope: source-only frontend dependency notice draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/frontend-deps-notice.source.md`
- Outcome:
  - Added the frontend dependency notice source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/notices/frontend-deps-notice.txt`.
  - Kept the draft as Markdown source material only, not a generated notice
    file, notice bundle, frontend build artifact, package output, or legal
    conclusion.
  - Recorded read-only local candidate sources from `ui/package.json` and
    `ui/pnpm-lock.yaml`.
  - Recorded direct runtime dependency candidates, developer/build-tool
    candidates, lockfile review candidates, package placement candidates,
    beginner-facing notice copy, developer-facing notice draft, manifest fields,
    future generated notice-bundle requirements, and review checklist items.
  - Preserved exact license and bundled dependency classification for a later
    package generation / license review task.
- Not implemented:
  - generated distribution folder
  - actual notice files
  - actual license bundle
  - generated dependency license inventory
  - frontend build artifact manifest
  - package or lockfile changes
  - dependency changes
  - package manager operations
  - HTML/TXT package guide output
  - package build, copy, zip, or generator behavior
  - Tauri
  - Electron
  - WebView2
  - desktop packaging
  - installer
  - signing or notarization
  - backend/frontend/Docker/CI/package/lockfile changes
  - 更新適用機能

### Y-06T desktop shell notice source draft

- Scope: source-only desktop shell notice draft and minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/desktop-shell-notice.source.md`
- Outcome:
  - Added the desktop shell notice source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/notices/desktop-shell-notice.txt`.
  - Recorded Windows and macOS notice placement candidates for future
    `Windows用/notices/desktop-shell-notice.txt` and
    `Mac用/notices/desktop-shell-notice.txt`.
  - Kept the draft as Markdown source material only, not a generated notice
    file, notice bundle, desktop shell implementation, package output, or
    legal conclusion.
  - Recorded Tauri, Electron, WebView2 direct host, and native launcher plus
    browser tab as candidates only.
  - Recorded official reference candidates for later recheck, beginner-facing
    notice copy, developer-facing notice draft, manifest fields, future
    generated notice-bundle requirements, and review checklist items.
  - Preserved actual desktop shell selection and exact license/runtime review
    for a later package generation / license review task.
- Not implemented:
  - generated distribution folder
  - actual notice files
  - actual license bundle
  - generated desktop shell dependency inventory
  - desktop shell build artifact manifest
  - Tauri implementation
  - Electron implementation
  - WebView2 implementation
  - installer implementation
  - signing or notarization
  - package or lockfile changes
  - dependency changes
  - package manager operations
  - HTML/TXT package guide output
  - package build, copy, zip, or generator behavior
  - backend/frontend/Docker/CI/package/lockfile changes
  - 更新適用機能

### Y-06U bundled Python dependency inventory source draft

- Scope: source-only bundled Python/backend dependency inventory draft and
  minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/bundled-python-dependency-inventory.source.md`
- Outcome:
  - Added the bundled Python dependency inventory source candidate for future
    `動画保存ツール_ローカル専用/開発者向け/inventory/bundled-python-dependency-inventory.json`
    and related developer-facing notice / license review material.
  - Recorded read-only dependency source files checked: `pyproject.toml` and
    `uv.lock` present; `poetry.lock`, `requirements*.txt`, `setup.py`,
    `setup.cfg`, Pipenv, Conda environment, constraints, tox, and nox
    dependency source files not present.
  - Recorded runtime dependency candidates, developer-only candidates,
    optional / indirect candidates, manifest candidate fields, license review
    checklist items, notice bundle review checklist items, and generated
    inventory requirements.
  - Kept all license values except the existing yt-dlp source draft candidate
    as `needs_verification` until a later selected package artifact review.
  - Kept the draft as Markdown source material only, not generated inventory,
    not a notice bundle, not a package output, and not a legal conclusion.
- Not implemented:
  - generated distribution folder
  - generated dependency inventory files
  - actual notice files
  - actual license bundle
  - package generation
  - backend/frontend/Docker/CI/package/lockfile changes
  - package manager operations
  - dependency install, update, audit, build, or package commands
  - HTML/TXT package guide output
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能

### Y-06V notice source index draft

- Scope: source-only notice / license / dependency inventory source index and
  minimal LLMwiki sync.
- Source draft:
  `docs/llmwiki/package-notices/notice-source-index.source.md`
- Outcome:
  - Added a hand-reviewed source index for future clean-package notice,
    license, manifest, beginner guide notice section, developer checklist, and
    dependency inventory review.
  - Read-only checked the existing MeTube, yt-dlp, FFmpeg, Python runtime,
    frontend dependency, desktop shell, and bundled Python dependency inventory
    source drafts.
  - Recorded future output mapping candidates for aggregate notices,
    license directories, manifest files, beginner guide notice sections, and
    developer review checklist items.
  - Standardized review status vocabulary: `source draft`, `legal-not-final`,
    `candidate only`, and `package-time review required`.
  - Kept unresolved questions and generated notice-bundle requirements as
    package-time review inputs only.
- Not implemented:
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - backend/frontend/Docker/CI/package/lockfile changes
  - package manager operations
  - dependency install, update, audit, build, or package commands
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能

### Y-06W clean package generator contract addendum

- Scope: docs-only / no-generation contract addendum for future clean package
  generator dry-run and preview behavior.
- Addendum:
  `docs/llmwiki/clean-package-generator-contract-addendum.md`
- Read-only sources checked:
  - `docs/llmwiki/package-notices/notice-source-index.source.md`
  - `docs/llmwiki/clean-package-dry-run-contract.md`
  - `docs/llmwiki/license-notice-plan.md`
  - `docs/llmwiki/codex-automation-policy.md`
  - `docs/llmwiki/safety-boundaries.md`
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_repo_safety.py`
- Outcome:
  - Treats the Y-06V notice source index as a future generator input candidate
    for dry-run / preview review.
  - Defines future output mapping checks for `NOTICE.txt`, `LICENSES/`,
    `manifest.json`, beginner guide notice sections, and developer review
    checklist items.
  - Defines no-generation boundary, generated artifact exclusion,
    cookie/token/secret value non-disclosure, package output before/after diff
    prediction candidate, package manifest preview candidate, cleanup /
    rollback candidate, and human review gate before actual generation.
  - Clarifies High-low / High-mid / High-high boundaries and future
    implementation phases.
- Not implemented:
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能

### Y-06X package manifest preview in clean package dry-run

- Scope: High-low / report-only dry-run preview enhancement.
- Script:
  `scripts/clean_package_dry_run.py`
- Read-only sources checked:
  - `docs/llmwiki/clean-package-generator-contract-addendum.md`
  - `docs/llmwiki/package-notices/notice-source-index.source.md`
  - `docs/llmwiki/clean-package-dry-run-contract.md`
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_repo_safety.py`
- Outcome:
  - Added a `Package manifest preview` section to the text dry-run report.
  - Reports package name/type candidates, `local_only: true`,
    `generated_artifacts: false`, notice source count/list, guide source
    count/list, excluded path summary, and future output candidates for
    `NOTICE.txt`, `LICENSES/`, `manifest.json`, and beginner guide notice
    section.
  - Reports `human_review_required_before_generation: true`,
    `legal_final: false`, non-disclosure flags for secret/token/cookie values,
    and a no-generation boundary note.
  - Preserves existing `Status: OK`, warnings, blockers, and exit-code
    behavior.
- Not implemented:
  - real `manifest.json` generation
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能

### Y-06Y package output diff prediction in clean package dry-run

- Scope: High-low / report-only dry-run preview enhancement.
- Script:
  `scripts/clean_package_dry_run.py`
- Read-only sources checked:
  - `docs/llmwiki/clean-package-generator-contract-addendum.md`
  - `docs/llmwiki/package-notices/notice-source-index.source.md`
  - `docs/llmwiki/clean-package-dry-run-contract.md`
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_repo_safety.py`
- Outcome:
  - Added a `Package output diff prediction` section to the text dry-run
    report.
  - Reports the future package root candidate, would-create directory
    candidates, would-create file candidates, would-copy source groups,
    future output candidates, excluded path summary, currently-present excluded
    path count, no-files-generated state, human review requirement before
    generation, and a cleanup / rollback candidate note.
  - Preserves the existing `Package manifest preview`, `Status: OK`, warnings,
    blockers, exit-code behavior, and no-files-generated behavior.
- Not implemented:
  - real `manifest.json` generation
  - real `NOTICE.txt` generation
  - real `LICENSES/` generation
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能

### Y-06Z clean package dry-run Markdown report mode design

- Scope: docs-only / High-low report mode design.
- Design document:
  `docs/llmwiki/clean-package-dry-run-markdown-report-mode-design.md`
- Read-only sources checked:
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_repo_safety.py`
  - `docs/llmwiki/clean-package-dry-run-contract.md`
  - `docs/llmwiki/clean-package-generator-contract-addendum.md`
  - `docs/llmwiki/codex-automation-policy.md`
  - `docs/llmwiki/handoff.md`
  - `docs/llmwiki/roadmap.md`
- Outcome:
  - Designed a future Markdown report mode for clean-package dry-run output.
  - Recommends `--format markdown` as the first future selector and keeps text
    output as the default.
  - Defines Markdown sections for Summary, Status, Risk Classification,
    Package Manifest Preview, Package Output Diff Prediction, Notice / Guide
    Source Coverage, Excluded Paths Summary, Blockers, Warnings, Human Review
    Checklist, and No-Generation Boundary.
  - Defines PR body reuse, handoff reuse, safety boundaries, future
    implementation checklist, future verification checklist, cleanup /
    rollback note, and High-low / High-mid boundary.
- Not implemented:
  - `scripts/clean_package_dry_run.py` changes
  - `scripts/check_repo_safety.py` changes
  - JSON output
  - Markdown output
  - real `manifest.json` generation
  - real `NOTICE.txt` generation
  - real `LICENSES/` generation
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - ビルド/パッケージ/インストール操作
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能

### Y-07A clean package dry-run JSON report mode design

- Scope: docs-only / High-low report mode design.
- Design document:
  `docs/llmwiki/clean-package-dry-run-json-report-mode-design.md`
- Read-only sources checked:
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_repo_safety.py`
  - `docs/llmwiki/clean-package-dry-run-contract.md`
  - `docs/llmwiki/clean-package-generator-contract-addendum.md`
  - `docs/llmwiki/clean-package-dry-run-markdown-report-mode-design.md`
  - `docs/llmwiki/codex-automation-policy.md`
  - `docs/llmwiki/handoff.md`
  - `docs/llmwiki/roadmap.md`
- Outcome:
  - Designed a future JSON report mode for clean-package dry-run output.
  - Recommends `--format json` as the first future selector and keeps text
    output as the default.
  - Defines one stdout JSON object with structured repository, package,
    planned entries, package manifest preview, package output diff prediction,
    excluded paths, checks, warnings, blocked reasons, safety flags,
    risk-classification relationship, no-generation boundary, and next-step
    fields.
  - Defines schema compatibility guidance, PR/handoff reuse guidance, safety
    boundaries, future implementation checklist, future verification checklist,
    cleanup / rollback note, and High-low / High-mid boundary.
- Not implemented:
  - `scripts/clean_package_dry_run.py` changes
  - `scripts/check_repo_safety.py` changes
  - JSON output
  - Markdown output
  - report-file output
  - real `manifest.json` generation
  - real `NOTICE.txt` generation
  - real `LICENSES/` generation
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - ビルド/パッケージ/インストール操作
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - automation wrapper / CI / PR-comment integration
  - 更新適用機能

### Y-07B clean package dry-run Markdown report mode

- Scope: report-only `--format markdown` implementation.
- Script:
  `scripts/clean_package_dry_run.py`
- Behavior:
  - Preserves the default text report.
  - Preserves `--format text` as text output.
  - Adds `--format markdown` as stdout-only Markdown output.
  - Markdown output includes Summary, Status, Risk Classification, Package
    Manifest Preview, Package Output Diff Prediction, Notice / Guide Source
    Coverage, Excluded Paths Summary, Blockers, Warnings, Human Review
    Checklist, and No-Generation Boundary sections.
  - Existing blockers, warnings, and exit codes are preserved.
  - Markdown mode reuses existing dry-run data and does not write files.
- Not implemented:
  - JSON output
  - report file writing
  - real `manifest.json` generation
  - real `NOTICE.txt` generation
  - real `LICENSES/` generation
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - ビルド/パッケージ/インストール操作
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能
- Next candidate:
  - Y-07C implement `--format json` report-only, if explicitly approved.

### Y-07C clean package dry-run JSON report mode

- Scope: report-only `--format json` implementation.
- Script:
  `scripts/clean_package_dry_run.py`
- Behavior:
  - Preserves the default text report.
  - Preserves `--format text` as text output.
  - Preserves `--format markdown` as stdout-only Markdown output.
  - Adds `--format json` as stdout-only valid JSON object output.
  - Existing blockers, warnings, and exit codes are preserved.
  - JSON output uses sanitized machine-readable fields for repository, package,
    package manifest preview, package output diff prediction, source coverage,
    excluded path summary, validation, warnings, blockers, safety flags, human
    review, and next step.
  - JSON mode reuses existing dry-run data and does not write files.
- Not implemented:
  - report file writing
  - real `manifest.json` generation
  - real `NOTICE.txt` generation
  - real `LICENSES/` generation
  - generated distribution folder
  - generated notice bundle
  - generated license bundle
  - generated dependency inventory files
  - generated manifest files
  - HTML/TXT package guide output
  - package generation
  - ビルド/パッケージ/インストール操作
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能
- Next candidate:
  - Decide whether to add JSON contract tests / snapshot-like check docs, or
    move toward the next docs/report-only package preview task.
  - Actual package generation remains blocked.

### Y-07D clean package dry-run report regression contract

- Scope: docs-only report regression / contract hardening design.
- Contract:
  `docs/llmwiki/clean-package-dry-run-report-regression-contract.md`
- Outcome:
  - Records the current report modes:
    `scripts/clean_package_dry_run.py`,
    `scripts/clean_package_dry_run.py --format text`,
    `scripts/clean_package_dry_run.py --format markdown`, and
    `scripts/clean_package_dry_run.py --format json`.
  - Defines regression invariants for default text, explicit text, Markdown,
    and JSON output.
  - Records the required Markdown sections and JSON top-level fields.
  - Defines cross-format consistency rules for status, warning count, blocker
    count, package root candidate, notice source coverage, guide source
    coverage, generated artifact state, and human review requirement.
  - Records exit-code, warning/blocker, sanitization, no-generation, and stop
    condition contracts.
  - Adds a verification matrix as commands/checklists only.
- Not implemented:
  - script changes
  - test implementation
  - CI integration
  - report file writing
  - generated distribution folder
  - package generation
  - real `manifest.json`, `NOTICE.txt`, or `LICENSES/` generation
  - generated notice/license/inventory/guide output
  - backend/frontend/Docker/CI/package/lockfile changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能
- Next candidate:
  - Y-07E optional lightweight regression test implementation, if explicitly
    approved.
  - Or pause package-material work and move to the next report-only package
    preview/planning task.

### Y-07E clean package dry-run report regression checker

- Scope: stdlib-only lightweight report regression checker.
- Script:
  `scripts/check_clean_package_dry_run_reports.py`
- Behavior:
  - Runs `scripts/clean_package_dry_run.py` in default, `--format text`,
    `--format markdown`, and `--format json` modes.
  - Verifies default output and `--format text` remain text.
  - Verifies default output and `--format text` are currently identical.
  - Verifies Markdown output includes the required sections from the Y-07D
    contract.
  - Verifies JSON output parses as one object and includes the required
    top-level fields from the Y-07D contract.
  - Verifies simple cross-format status, warnings, and blockers consistency.
  - Verifies `動画保存ツール_ローカル専用/` is absent.
  - Prints a sanitized human-readable checker report.
  - Does not write files, create temp files, or create package output.
- Not implemented:
  - changes to `scripts/clean_package_dry_run.py`
  - changes to `scripts/check_repo_safety.py`
  - CI integration
  - report file writing
  - generated distribution folder
  - package generation
  - real `manifest.json`, `NOTICE.txt`, or `LICENSES/` generation
  - generated notice/license/inventory/guide output
  - backend/frontend/Docker/CI/package/lockfile changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能
- Next candidate:
  - Decide whether to add CI wiring for the checker later, if explicitly
    approved.
  - Or move to the next package preview/report-only planning task.
  - Actual package generation remains blocked.

### Y-08A clean package preview hardening design

- Scope: docs-only package preview hardening design.
- Design document:
  `docs/llmwiki/clean-package-preview-hardening-design.md`
- Outcome:
  - Documents the current preview baseline after text, Markdown, JSON, and
    regression checker stabilization.
  - Documents existing preview strengths and package preview gaps.
  - Defines richer manifest preview field candidates.
  - Defines richer package output diff prediction grouping candidates.
  - Defines source coverage statuses for future report-only hardening.
  - Maps notice, license, inventory, beginner guide, and developer review
    checklist candidates to future preview output.
  - Reconfirms cross-format, JSON, sanitization, no-generation, and risk
    boundaries.
- Not implemented:
  - script changes
  - test implementation
  - CI integration
  - report file writing
  - generated distribution folder
  - package generation
  - real `manifest.json`, `NOTICE.txt`, or `LICENSES/` generation
  - generated notice/license/inventory/guide output
  - backend/frontend/Docker/CI/package/lockfile changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - 更新適用機能
- Next candidate:
  - Y-08B richer manifest preview entries in report-only mode, if explicitly
    approved.
  - Actual package generation remains blocked.

### Y-08B richer manifest preview entries

- Scope: report-only richer manifest preview entries.
- Changed script:
  `scripts/clean_package_dry_run.py`
- Checker updated:
  `scripts/check_clean_package_dry_run_reports.py`
- Behavior:
  - Adds manifest entry candidates to text, Markdown, and JSON package
    manifest preview output.
  - JSON includes `manifest_entries` and `manifest_entry_summary` under
    `package_manifest_preview`.
  - The checker validates the new manifest entry fields, text marker, and
    Markdown section.
  - Default text, `--format text`, `--format markdown`, and `--format json`
    modes remain supported.
- Not implemented:
  - actual `manifest.json`
  - package generation
  - generated package folder
  - generated notice/license/inventory/guide output
  - report file writing
  - CI integration
  - backend/frontend/Docker/CI/package/lockfile changes
  - PR #1001 file changes
  - cookie/token/secret handling
  - 更新適用機能
- Next candidate:
  - Y-08C richer output diff prediction grouping in report-only mode, if
    explicitly approved.
  - Actual package generation remains blocked.

### Y-08C richer output diff prediction grouping

- Scope: report-only richer package output diff prediction grouping.
- Changed script:
  `scripts/clean_package_dry_run.py`
- Checker updated:
  `scripts/check_clean_package_dry_run_reports.py`
- Behavior:
  - Adds `output_groups` to text and Markdown package output diff prediction
    output.
  - JSON includes `package_output_diff_prediction.output_groups` and
    `package_output_diff_prediction.output_group_summary`.
  - Output groups cover beginner guides, developer docs, manifest outputs,
    notices, licenses, inventory, Windows/macOS runtime placeholders, save
    folder placeholders, troubleshooting placeholders, and excluded outputs.
  - The checker validates the new output group fields, required group keys,
    text marker, Markdown section, and JSON summary.
  - Default text, `--format text`, `--format markdown`, and `--format json`
    modes remain supported.
- Not implemented:
  - package generation
  - generated package folder
  - generated notice/license/inventory/guide output
  - actual runtime launcher or desktop package output
  - report file writing
  - CI integration
  - backend/frontend/Docker/CI/package/lockfile changes
  - PR #1001 file changes
  - cookie/token/secret handling
  - 更新適用機能
- Next candidate:
  - Y-08D source coverage status hardening in report-only mode, if explicitly
    approved.
  - Actual package generation remains blocked.

### Y-08D source coverage status hardening

- Scope: report-only source coverage status hardening.
- Changed script:
  `scripts/clean_package_dry_run.py`
- Checker updated:
  `scripts/check_clean_package_dry_run_reports.py`
- Behavior:
  - Adds `coverage_items` and `coverage_summary` to source coverage preview.
  - Covers guide, notice, license, inventory, runtime selection, desktop shell,
    and manifest source categories.
  - Text, Markdown, and JSON modes remain supported.
  - The checker validates required coverage item fields, approved statuses,
    required categories, text marker, Markdown section, and JSON summary.
- Not implemented:
  - package generation
  - generated package folder
  - actual `manifest.json`
  - generated notice/license/inventory/guide output
  - report file writing
  - CI integration
  - backend/frontend/Docker/CI/package/lockfile changes
  - PR #1001 file changes
  - cookie/token/secret handling
  - 更新適用機能
- Next candidate:
  - Y-08E package generation readiness checklist in docs-only or report-only
    mode, if explicitly approved.
  - Actual package generation remains blocked.

### Y-08E generation readiness checklist design

- Scope: docs-only generation readiness checklist design.
- New document:
  `docs/llmwiki/clean-package-generation-readiness-checklist.md`
- Behavior:
  - Defines readiness gates for report modes, source coverage, manifest
    preview, output diff prediction, notice/license/inventory readiness,
    beginner guide readiness, runtime/desktop shell readiness, security/privacy
    readiness, cleanup/rollback readiness, and human review.
  - Clarifies that passing dry-run previews do not approve actual generation.
  - Keeps actual package generation blocked until a later explicit
    human-reviewed task.
- Not implemented:
  - script changes
  - test implementation
  - CI integration
  - report file writing
  - package generation
  - generated package folder
  - generated notice/license/inventory/guide output
  - backend/frontend/Docker/CI/package/lockfile changes
  - PR #1001 file changes
  - cookie/token/secret handling
  - 更新適用機能
- Next candidate:
  - Implemented by Y-08F generation readiness checklist preview in report-only
    mode.
  - Next package-material candidate: Y-08G readiness summary polish / advisory
    score refinement, if explicitly approved.
  - Actual package generation remains blocked.

### Y-08F generation readiness checklist preview implementation

- Scope: report-only readiness checklist preview and checker/docs sync.
- Changed scripts:
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_clean_package_dry_run_reports.py`
- Behavior:
  - Adds a `Generation Readiness Preview` section to default text,
    `--format text`, and `--format markdown` dry-run reports.
  - Adds JSON top-level `generation_readiness`.
  - Keeps `generation_readiness.overall: blocked`.
  - Keeps `generation_readiness.actual_generation_approved: false`.
  - Includes checklist items, advisory-only score basis, summary counts,
    unresolved count, and next required action.
  - Extends the report regression checker for text, Markdown, JSON, summary,
    approval false, generated folder absence, and cross-format readiness
    consistency.
- Not implemented:
  - actual package generation
  - generated package folder
  - report file writing
  - actual `manifest.json`
  - generated notice/license/inventory/guide output
  - backend/frontend/Docker/CI/package/lockfile changes
  - PR #1001 file changes
  - cookie/token/secret handling
  - 更新適用機能
- Next candidate:
  - Implemented by Y-08G readiness summary polish / advisory score refinement.
  - Actual package generation remains blocked.

### Y-08G readiness summary polish / advisory score refinement

- Scope: report-only readiness summary polish and checker/docs sync.
- Completed by fork PR #71.
- Latest expected `fork/master` after Y-08G:
  `4971e33fcb1c79eb4f1ee70a5d802565dfa04624`
- Changed scripts:
  - `scripts/clean_package_dry_run.py`
  - `scripts/check_clean_package_dry_run_reports.py`
- Behavior:
  - Adds JSON `generation_readiness.advisory_score`.
  - Adds JSON `generation_readiness.readiness_summary`.
  - Shows `advisory_score: 23/100` in text and Markdown output.
  - Keeps `generation_readiness.overall: blocked`.
  - Keeps `generation_readiness.actual_generation_approved: false`.
  - Keeps `generation_readiness.score_basis: advisory_only`.
  - Treats the advisory score as review-only; it is not generation approval.
  - Extends the checker for Y-08G score, summary, cross-format consistency,
    and generated package folder absence.
- Not implemented:
  - actual package generation
  - generated package folder
  - report file writing
  - ZIP / installer / package output
  - backend/frontend/Docker/CI/package/lockfile changes
  - PR #1001 file changes
  - cookie/token/secret handling
  - 更新適用機能
- Follow-up:
  - Y-08Z preview hardening closeout, completed by this PR.
  - Next practical candidate after Y-08Z:
    `Y-UI-QUALITY-01 quality selector simple labels with numeric values`
  - Actual package generation remains blocked.

### Y-08Z preview hardening closeout

- Scope: docs-only closeout for the Y-08 preview hardening lane.
- Status: completed by this PR.
- Prior completed work:
  - Y-08F generation readiness checklist preview completed via fork PR #70.
  - Y-08G readiness summary polish / advisory score refinement completed via
    fork PR #71.
- Latest expected `fork/master` after Y-08G:
  `4971e33fcb1c79eb4f1ee70a5d802565dfa04624`
- Readiness preview state:
  - `overall: blocked`
  - `actual_generation_approved: false`
  - `score_basis: advisory_only`
  - `advisory_score: 23/100`
  - `approval_meaning: none`
- Boundary:
  - readiness preview is report-only and advisory-only
  - advisory score does not replace human approval
  - actual clean-package generation remains blocked
  - no package output or generated package folder is approved
- Next practical candidate:
  - `Y-UI-QUALITY-01 quality selector simple labels with numeric values`

### Y-UI-QUALITY-01 quality selector simple labels with numeric values

- Scope: frontend UI label-only improvement.
- Status: completed via fork PR #73.
- PR title: `feat: simplify quality selector labels`.
- Merge commit: `402996eba52f923be962e2fe69ebdaa6084363f2`.
- Changed files:
  - `ui/src/app/app.ts`
  - `ui/src/app/interfaces/formats.ts`
- Outcome:
  - visible video/audio quality selector labels now use simple Japanese labels
    plus numeric values;
  - numeric values remain visible, for example `2160p`, `1080p`, `320kbps`,
    `192kbps`, and `128kbps`;
  - existing option ids were preserved;
  - API payloads, backend validation, and download logic were unchanged.
- Verification notes:
  - existing `ui/node_modules` was used for local frontend lint/test;
  - no dependency install was performed;
  - generated package folder remained absent.
- Safety note:
  - `scripts/run_local_safety_gates.py` currently forbids `ui/**`, so this
    explicitly approved frontend UI label-only task required human-reviewed
    merge instead of auto-merge;
  - this did not weaken the safety gate or modify gate behavior.
- Not changed:
  - backend/API/download logic;
  - option ids;
  - Docker, CI, package, or lock files;
  - generated package output;
  - PR #1001 files.

### Y-UI-QUALITY-02 quality selector helper copy / tooltip polish

- Scope: frontend UI copy-only helper/popover polish.
- Status: completed via fork PR #75.
- PR title: `feat: clarify quality selector help copy`.
- Merge commit: `eea1c861a62033b02255950491cd9e0f6ab2d77b`.
- Changed files:
  - `ui/src/app/app.html`
- Outcome:
  - quality selector helper copy was clarified;
  - the video quality helper now explains quality targets / upper limits,
    fallback when source quality is unavailable, auto mode, and the file-size
    tradeoff;
  - the audio quality helper now explains the audio quality / file-size
    tradeoff and auto mode;
  - the audio selector label changed from `画質` to `音質`;
  - option ids were preserved;
  - API payloads, backend/API/download logic, validation, and yt-dlp selector
    behavior were unchanged.
- Verification notes:
  - no dependency installation operations were performed;
  - no generated package output was created;
  - generated package folder remained absent.
- Safety note:
  - because this touched `ui/**`, it was High-mid / human-reviewed frontend UI
    copy-only work, not auto-merge;
  - this did not weaken the safety gate or modify gate behavior.
- Not changed:
  - backend/API/download logic;
  - option ids, payload names, validation, or yt-dlp selector behavior;
  - Docker, CI, package, or lock files;
  - generated package output;
  - PR #1001 files.

### Y-UI-QUALITY-03 completed/result table quality label polish

- Scope: frontend UI label/test polish for completed/result table display.
- Status: completed via fork PR #77.
- PR title: `feat: polish result quality labels`.
- Merge commit: `c2f58fad237218d681414b51749bca6fe1bc734b`.
- Changed files:
  - `ui/src/app/app.html`
  - `ui/src/app/app.ts`
  - `ui/src/app/app.spec.ts`
- Outcome:
  - completed/result table quality labels now match the simplified selector
    wording;
  - result table quality column header changed from `画質` to neutral `品質`;
  - video quality labels now include `最高画質（自動）`, `4K（2160p）`,
    `高画質（1440p）`, `フルHD（1080p）`, `標準（720p）`, `軽量（480p）`,
    `低容量（360p）`, and `最小（240p）`;
  - audio quality labels now include `最高音質（自動）`,
    `高音質（320kbps）`, `標準（192kbps）`, and `軽量（128kbps）`;
  - captions and thumbnails keep `-`;
  - safe fallback behavior remains for unknown quality strings;
  - focused UI spec coverage was added for label mapping.
- Verification notes:
  - frontend tests passed: 40 tests;
  - no dependency install or update operation was performed;
  - no package output was generated;
  - generated package folder remained absent.
- Safety note:
  - because this touched `ui/**`, it was High-mid / human-reviewed frontend UI
    label/test work, not auto-merge;
  - this did not weaken the safety gate or modify gate behavior.
- Not changed:
  - backend/API/download logic;
  - option ids, payloads, validation, or yt-dlp selector behavior;
  - Docker, CI, package, or lock files;
  - generated package output;
  - PR #1001 files.

### Y-CHECK-01 safety gate checker design

- Scope: docs-only design for a future repository safety checker and automation
  gate.
- Design document:
  `docs/llmwiki/safety-gate-checker-design.md`
- Outcome:
  - Defined a future diff-oriented safety gate for low- and medium-risk Codex
    work.
  - Covered changed files scope, forbidden paths, secret-like pattern handling,
    generated distribution folder detection, PR #1001 leakage, dangerous
    behavior, update execution, package guide / notice completeness warnings,
    LLMwiki consistency, and PR safety summary output.
  - Kept reports sanitized: paths, line numbers, and pattern families only for
    secret-like findings.
  - Positioned package guide / notice completeness as warning-only unless actual
    package generation is attempted.
  - Clarified that the gate does not override human approval requirements for
    destructive, credential, deployment, install/update, push, merge, or release
    actions.
- Not implemented:
  - repo safety checker script
  - automation gate implementation
  - CI integration
  - PR bot/comment automation
  - generated distribution folder
  - package generation
  - backend/frontend/Docker/CI/package/lockfile changes
  - update execution
  - cookie/token/secret handling

### Y-CHECK-02 repo safety check script

- Scope: stdlib-only, report-only repository safety checker and minimal
  LLMwiki sync.
- Script:
  `scripts/check_repo_safety.py`
- Outcome:
  - Added a local report-only safety gate script for low- and medium-risk Codex
    work.
  - Default mode checks the current working tree diff against `HEAD`, including
    untracked files.
  - Optional `--base` can include committed branch diff context, for example
    `--base fork/master`.
  - Reports changed files, scope classification, warnings, blockers, and check
    statuses.
  - Checks changed-file scope, forbidden paths, generated distribution folder
    presence, upstream PR #1001 leakage, secret-like changed content,
    dangerous behavior patterns, required LLMwiki basics, and package
    guide/notice source presence.
  - Secret-like findings are sanitized and report only path, line, and pattern
    family.
  - Exit codes are `0` for OK or warning-only, `1` for blocked, and `2` for
    usage errors.
- Not implemented:
  - automation gate implementation
  - CI integration
  - PR bot/comment automation
  - generated distribution folder
  - package generation
  - backend/frontend/Docker/CI/package/lockfile changes
  - update execution
  - cookie/token/secret value output

### Y-AUTO-01 Codex automation expansion policy

- Scope: docs-only Codex automation policy for low-, medium-, and qualifying
  high-low-risk work.
- Policy document:
  `docs/llmwiki/codex-automation-policy.md`
- Outcome:
  - Defined five risk levels: Low, Medium, High-low, High-mid, and High-high.
  - Kept Low work eligible for auto PR and auto merge when the current task
    scope and required gates pass.
  - Kept Medium work eligible for auto PR and auto merge when safety gates pass.
  - Added conditional High-low auto PR / auto merge for docs-only,
    report-only, or dry-run-only work that passes the full mandatory gate set.
  - Required High-low work to pass `check_repo_safety.py`,
    `check_repo_safety.py --base fork/master`, `clean_package_dry_run.py`,
    `git diff --check`, GitHub clean merge state, and no failed checks.
  - Kept High-mid work PR-capable but auto-merge prohibited.
  - Kept High-high work automatic-execution prohibited until explicit human
    confirmation.
- Not implemented:
  - generated distribution folder
  - generated guide, notice, manifest, ZIP, package, or installer output
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - public hosting or ads
  - 更新適用機能

### Y-AUTO-02 repo safety risk classification

- Scope: report-only checker improvement and minimal LLMwiki sync.
- Script:
  `scripts/check_repo_safety.py`
- Outcome:
  - Added a `Risk classification` section to the repo safety report.
  - The report now includes `tier`, `automation`, and `reason`.
  - Supported tiers are `Low`, `Medium`, `High-low`, `High-mid`,
    `High-high`, and `Unknown`.
  - Supported automation outputs are `auto-merge-ok`,
    `pr-only-human-merge`, `stop-before-pr`, and `unknown`.
  - Existing `Status: OK` / `Status: BLOCKED` behavior is unchanged.
  - Existing blockers for forbidden paths, generated distribution folders,
    PR #1001 leakage, secret-like content, dangerous behavior, and required
    LLMwiki basics are unchanged.
  - For this report-only checker task, the working-tree report classified the
    change as `Medium` with `automation: auto-merge-ok`.
- Not implemented:
  - automation gate implementation
  - CI integration
  - PR bot/comment automation
  - generated distribution folder
  - generated guide, notice, manifest, ZIP, package, or installer output
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - public hosting or ads
  - 更新適用機能

### Y-AUTO-03 High-mid PR-ready automation policy

- Scope: docs-only policy expansion for High-mid Codex work.
- Policy document:
  `docs/llmwiki/codex-automation-policy.md`
- Outcome:
  - Clarified that Low, Medium, and qualifying High-low work may still use auto
    PR / auto merge when gates pass.
  - Clarified that High-mid work may proceed through Codex implementation,
    verification, PR creation, and Ready-for-review handoff when the task
    explicitly approves the High-mid scope.
  - Kept High-mid auto merge prohibited.
  - Required High-mid PRs to state `human-review-required`.
  - Required High-mid PR bodies to explain why the work is High-mid, what was
    not performed, rollback/cleanup candidates, and remaining risk.
  - Added a High-mid PR body template.
  - Reconfirmed that High-high work must stop before implementation without
    explicit human confirmation.
- Not implemented:
  - generated distribution folder
  - generated guide, notice, manifest, ZIP, package, or installer output
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - public hosting or ads
  - 更新適用機能

### Y-AUTO-04 High-mid PR-only checker guidance

- Scope: report-only checker improvement and minimal LLMwiki sync.
- Script:
  `scripts/check_repo_safety.py`
- Outcome:
  - Added path and filename based High-mid-like scope detection.
  - High-mid-like scopes now report `tier: High-mid`.
  - High-mid-like scopes without blockers now report
    `automation: pr-only-human-merge`.
  - High-mid-like reasons explicitly state that auto merge is disabled, human
    review is required before merge, and the PR body must include
    `human-review-required`.
  - Known report-only checker / dry-run script changes remain `Medium` with
    `automation: auto-merge-ok` when no blockers are present.
  - Existing `Status: OK` / `Status: BLOCKED` behavior is unchanged.
  - Existing blockers for forbidden paths, generated distribution folders,
    PR #1001 leakage, secret-like content, dangerous behavior, and required
    LLMwiki basics are unchanged.
- Not implemented:
  - automation gate implementation
  - CI integration
  - PR bot/comment automation
  - generated distribution folder
  - generated guide, notice, manifest, ZIP, package, or installer output
  - build/package/install commands
  - dependency changes
  - package/lockfile changes
  - backend/frontend/Docker/CI changes
  - cookie/token/secret handling
  - PR #1001 file changes
  - public hosting or ads
  - 更新適用機能

### Y-LOCAL-01 local WebGPT handoff helper exclude

- Scope: local-only setup with no repository diff and no PR.
- Helper:
  `export_context_updated.py`
- Local tracking:
  `.git/info/exclude`
- Outcome:
  - Added `export_context_updated.py` to local Git exclude.
  - Kept `.gitignore` unchanged.
  - Kept the helper uncommitted, undeleted, and unmoved.
  - Confirmed the helper no longer appears in `git status` or
    `git ls-files --others --exclude-standard`.

### Y-AUTO-06 automation efficiency policy

- Scope: docs-only / High-low automation efficiency policy.
- New document:
  `docs/llmwiki/automation-efficiency-policy.md`
- Outcome:
  - Adopted safe one-PR scope expansion rules for same-purpose, same-risk work.
  - Defined Codex auto lanes for docs-only, report-only dry-run, checker-only,
    docs/report/checker combined, and High-mid PR-ready-only work.
  - Documented the `export_context_updated.py` local helper policy.
  - Documented closeout PR policy for safe short lanes.
  - Recorded future candidates for local safety gate aggregation, PR body
    generation, Codex prompt templates, CI, branch protection, CODEOWNERS,
    worktree operation, stop condition checks, and advisory readiness scoring.
- Not implemented:
  - script changes
  - checker changes
  - CI integration
  - report file writing
  - package generation
  - generated package folder
  - generated notice/license/inventory/guide output
  - backend/frontend/Docker/CI/package/lockfile changes
  - PR #1001 file changes
  - cookie/token/secret handling
  - public hosting or ads
  - 更新適用機能
- Next candidates:
  - Y-AUTO-08 safety gate aggregator design
  - Y-AUTO-09 safety gate aggregator implementation
  - Actual package generation remains blocked.

### Y-AUTO-07 codex auto lanes

- Scope: docs-only / High-low lane execution policy docs.
- New document:
  `docs/llmwiki/codex-auto-lanes.md`
- Outcome:
  - Converted lane concepts into concrete auto execution rules.
  - Added practical lane execution permissions, gates, and stop conditions.
  - Added docs-only, report-only, checker-only, combined, and High-mid
    PR-ready-only lane definitions.
  - Added continuous execution rules, auto PR/merge gate requirements, and closeout
    PR restrictions.
  - Reconfirmed no scripts, backend/frontend/Docker/CI, generation, or package
    output changes.
- Not implemented:
  - script changes
  - checker changes
  - CI implementation
  - report file writing
  - package generation
  - generated package folder
  - generated notice/license/inventory/guide output
  - backend/frontend/Docker/CI/package/lockfile changes
  - PR #1001 file changes
  - cookie/token/secret handling
  - public hosting or ads
  - 更新適用機能
- Next candidate:
  - Y-AUTO-08 safety gate aggregator design
  - Actual package generation remains blocked.

## Current Next Step

Y-CI-03 is complete via fork PR #95 with merge commit
`c64b935fc02b7893e8be38d13a53e8b26adf91cf`. It designed the reusable workflow
split for `local-fork-safety` without changing `.github/workflows/`.

Y-CI-03B is complete via fork PR #96. fork `master` is now at
`2d59c4e4034d772d029b776497136e9bf67b6cd5`, with
`.github/workflows/local-fork-safety.yml` as the PR caller and
`.github/workflows/reusable-local-safety.yml` as the `workflow_call` target.

Y-CI-04 is complete via fork PR #97. fork `master` is now at
`becdf346956cb61b985df93637ab5c121884e49c`, with workflow-level concurrency on
the `local-fork-safety` caller and unchanged reusable safety steps.

Y-GH-01 is complete via fork PR #98. fork `master` is now at
`1bb28de03e3257cedb097301672a30cdd1052f18`. It added the design source of
truth at `docs/llmwiki/branch-protection-design.md` without mutating GitHub
settings, configuring required checks, adding CODEOWNERS, or changing workflow
files.

Y-CI-05 is complete via fork PR #99 with merge commit
`e77e68c56a369c3ae962cf0abcbe958ce36a2101`. It observed the passing GitHub
check name `local fork safety / local fork safety` on a normal docs-only PR
without workflow or GitHub settings changes.

Y-GH-02 is complete via fork PR #100 with merge commit
`34497e8918bbc12b7ea457eb6cc48c7c9d8c963b`. Its source of truth is
`docs/llmwiki/required-checks-design.md`. It recorded
`local fork safety / local fork safety` as the current required-check
candidate, but did not change workflows or GitHub settings.

PR #101 is complete with merge commit
`df99701477d05d4f4b6e5127ee8588e3da5252d5`. It was docs-only cleanup and is
the baseline recorded inside the Y-DIST-07 packet.

Y-DIST-07 is complete via fork PR #102 with merge commit
`f4a644fd97c869f305465b8e51d837bdd310b2e5`. It added the docs-only artifact
generation approval packet at
`docs/llmwiki/artifact-generation-approval-packet.md`. It prepares future human
review but does not approve generation.

Y-GH-OPS-01 is complete via fork PR #103 with merge commit
`926c7e5fa02bfe433f842b164b30d405d446b53f`. It standardized the GitHub
ready/check/merge fallback flow and made the fast safe flow baseline available
for future low-risk docs/report/checker work.

Y-AUTO-OPS-01 is complete via fork PR #104 with merge commit
`6973732e2483548201a81c1debd88cbea98f5b8f`. It adopted the fast safe flow
default template for normal low-risk docs/report/checker work.

Y-DIST-08 is complete via fork PR #105 with merge commit
`a62e1c67261f7fbf31f970f2abf31c0a7c79c36d`. It records the no-generation hold
after human review of the Y-DIST-07 approval packet. No artifact generation
approval is granted, all artifact categories remain `not approved`, and
generation remains blocked.

Y-UX-PLAN-01 establishes the docs-only beginner UX next-action path after the
Y-DIST-08 hold:
`docs/llmwiki/beginner-ux-next-action-plan.md`.

Y-08Z closes the Y-08 preview hardening lane as docs-only closeout.
Y-UI-QUALITY-01 is complete via fork PR #73 with merge commit
`402996eba52f923be962e2fe69ebdaa6084363f2`. Y-UI-QUALITY-02 is complete via
fork PR #75 with merge commit
`eea1c861a62033b02255950491cd9e0f6ab2d77b`. Y-UI-QUALITY-03 is complete via
fork PR #77 with merge commit
`c2f58fad237218d681414b51749bca6fe1bc734b`.

Y-UI-QUALITY-01 simplified the visible quality selector labels while preserving
numeric values, existing option ids, API payloads, backend validation, and
download logic. Y-UI-QUALITY-02 clarified the quality selector helper copy:
video help now explains quality targets / upper limits, source-quality fallback,
auto mode, and file-size tradeoff; audio help now explains the quality /
file-size tradeoff and auto mode; the audio selector label changed from `画質`
to `音質`. Y-UI-QUALITY-03 polished completed/result table quality labels so
they match selector wording, changed the result table column header from `画質`
to `品質`, kept captions/thumbnails as `-`, preserved safe fallback behavior,
and added focused UI spec coverage.

Y-UI-QUALITY-02 and Y-UI-QUALITY-03 preserved option ids, payloads,
backend/API/download logic, validation, and yt-dlp selector behavior. Because
they touched `ui/**`, they were High-mid / human-reviewed frontend UI merges,
not auto-merge. That known scope mismatch did not weaken or modify the safety
gate.

Y-UI-QUALITY-03Z is complete via fork PR #78 with merge commit
`035ecce6f2c9964772bc6612ddba422309a73cd1`.

Y-UI-REVIEW-01 is complete via fork PR #79 with merge commit
`2c30cc28080e39949bb4a6ab8e646abb700ebfb1`. It created a docs-only manual UI
review checklist for the current quality selector and completed/result table polish:
`docs/llmwiki/current-ui-manual-review-checklist.md`.

Y-UI-REVIEW-02 attempted the current UI screenshot review and recorded findings
docs-only:
`docs/llmwiki/current-ui-screenshot-review-findings.md`. Temporary screenshots
were captured outside the repository for the static desktop add form, video
quality helper popover, and narrow-width layout. Full interactive screenshot
review remains partial because the static preview stayed at
`サーバーに接続中...`, leaving controls disabled and blocking selector-open,
audio-mode, and real result-row visual review. No UI code, backend code,
download behavior, or package output was changed.

Y-UI-REVIEW-02R reran the screenshot review with a temporary local mock server
and safe synthetic data, then appended the rerun result to
`docs/llmwiki/current-ui-screenshot-review-findings.md`. The rerun improved
coverage by observing the loaded add form, video helper popover, audio mode,
audio `音質` selector label, audio helper popover, completed/result table
header `品質`, synthetic video/audio quality labels, captions/thumbnail `-`,
and narrow-width loaded layout. No blocking UI findings were observed. Native
select dropdown panels were not visible in captured screenshots and were
verified through browser DOM evidence instead. No UI code, backend code,
download behavior, or package output was changed.

Use the preflight checker before future file modification when a task needs
local readiness confirmation:

```powershell
python scripts/check_local_dev_environment.py --base fork/master --expected-branch master
```

It remains readiness-only and does not replace safety gates.

Use the `Risk classification` section from `scripts/check_repo_safety.py` as the
first local summary before auto PR or auto merge.

Use `scripts/check_repo_safety.py` and `scripts/clean_package_dry_run.py` as
local report-only gates before the next low-, medium-, or qualifying
high-low-risk fork PR.

The previous package-material lane is complete through Y-08Z closeout. Actual
clean-package generation remains blocked. The generated package folder must
remain absent.

The next practical candidates after Y-UX-PLAN-01 are:

```text
Y-UX-COPY-01 safe-use microcopy review
Y-UX-HELP-01 help/troubleshooting entry review
Y-UX-STATE-01 status / progress / completion clarity review
Y-UX-STOP-01 stop/quit user-flow design
quality selector / label review follow-up
another docs/report/checker lane using fast safe flow
```

Pause can be chosen instead. Future `ui/**` work remains human-reviewed unless
a later policy/checker PR explicitly updates the local safety gate and
automation policy.

Later clean-package work should resume as a separate explicitly approved lane,
with Y-09 limited to human-reviewed generation prototype planning only and not
actual generation.

Next scope:

- Keep any further Y-CHECK automation, CI, or PR-comment integration separate
  until explicitly approved.
- Do not modify safety gate behavior in this docs closeout.
- Do not broaden auto-merge policy for `ui/**` in this docs closeout.
- Keep UI quality selector follow-up work separate from clean-package generation.
- Keep notice material source-only, sanitized, and review-oriented.
- Keep guide and notice files as source material only; do not generate package
  outputs.
- Keep clean-package preview work report-only / dry-run-only until actual
  generation is explicitly approved.
- Keep Tauri/Electron implementation, packaging, installer, signing, updater,
  backend changes, frontend changes, Docker changes, CI changes, package
  changes, and lockfile changes out of scope unless explicitly approved later.

## Y-AUTO-08 Local Safety Gate Aggregator Design State

Y-AUTO-08 adds a docs-only design for a future local safety gate aggregator:

- New design doc: `docs/llmwiki/local-safety-gate-aggregator-design.md`.
- Future candidate script path: `scripts/run_local_safety_gates.py`.
- Intended purpose: orchestrate the existing local manual gates and print a concise summary.
- Existing gates remain authoritative until a later implementation lands.
- No script, app, UI, Docker, CI, package, lockfile, `.gitignore`, or generated-output change is included in Y-AUTO-08.

The future aggregator is expected to cover repository safety checks, dry-run report regression, clean-package dry-run modes, generated package folder absence, changed-file scope checks, PR #1001 leakage checks, and untracked helper exclusion checks.

Current next candidate: Y-AUTO-09 may implement the read-only local safety gate aggregator as a stdlib-only script with text output only.
## Y-AUTO-09 Local Safety Gate Aggregator State

Y-AUTO-09 implements `scripts/run_local_safety_gates.py`.

Behavior:

- Runs repository safety gates.
- Runs the dry-run report regression checker.
- Runs clean-package dry-run in default, text, markdown, and JSON modes.
- Checks that `動画保存ツール_ローカル専用/` is absent.
- Checks PR #1001 leakage absence for `docker-compose.local.yml` and `docs/local-only.md`.
- Checks that `export_context_updated.py` remains excluded from untracked files.
- Prints a concise text summary.

Not implemented:

- No CI integration.
- No PR body generator.
- No report file writing.
- No package generation.
- No backend/frontend/Docker/CI/package/lockfile changes.
- No PR #1001 files.
- No cookie/token/secret handling.
- No 更新適用機能.

Next candidate: Y-AUTO-10 PR body generator design.
## Y-AUTO-10A Safety Wording Checker Design State

Y-AUTO-10A adds a docs-only design for a future safety wording checker.

- New design doc: `docs/llmwiki/safety-wording-checker-design.md`.
- It explains the Y-AUTO-07 wording issue and a repeatable safe wording policy.
- It defines a future standalone checker candidate without implementing it.
- It keeps the existing repo safety gate authoritative.
- No script implementation, script change, CI change, generated package output, backend/frontend/Docker/CI/package/lockfile change, PR #1001 file change, or secret-like value handling is included.

Next candidate: Y-AUTO-10B safety wording checker implementation.
## Y-AUTO-10B Safety Wording Checker State

Y-AUTO-10B implements `scripts/check_safety_wording.py`.

Behavior:

- scans changed docs by default;
- supports `--base`;
- supports `--all`;
- supports explicit paths;
- outputs a sanitized text summary;
- writes no files.

Not implemented:

- no aggregator integration;
- no PR body generator;
- no report file writing;
- no package generation;
- no backend/frontend/Docker/CI/package/lockfile changes;
- no PR #1001 files;
- no cookie/token/secret handling;
- no 更新適用機能.

Next candidate: Y-AUTO-11 PR body generator design.

## Y-AUTO-11 PR Body Generator Design State

Y-AUTO-11 adds a docs-only design for a future PR body generator:

- New design doc: `docs/llmwiki/pr-body-generator-design.md`.
- Future candidate script path: `scripts/generate_pr_body.py`.
- Defines output sections, risk templates, explicitly not-performed presets,
  verification templates, human review templates, local helper note rules,
  safety wording rules, CLI shape, output format, exit code contract, and
  sanitization rules.
- Documents future integration with `scripts/run_local_safety_gates.py` and
  `scripts/check_safety_wording.py`.
- Keeps `scripts/check_repo_safety.py` authoritative for repo safety
  classification.
- No script implementation, checker change, CI change, GitHub API integration,
  PR automation, report file writing, package output, backend/frontend/Docker/CI
  change, package/lockfile change, PR #1001 file change, or secret-like value
  handling is included.

Follow-up implemented by Y-AUTO-12 PR body generator stdout-only implementation.

## Y-AUTO-12 PR Body Generator State

Y-AUTO-12 implements `scripts/generate_pr_body.py`.

Behavior:

- stdout-only Markdown PR body output;
- risk and scope templates;
- explicitly not-performed presets;
- verification presets;
- local helper note;
- optional sanitized changed-file summary;
- no file writes;
- no GitHub API;
- no PR creation or editing.

Not implemented:

- no GitHub API integration;
- no file output by default;
- no PR creation/editing;
- no aggregator parsing;
- no stdin wording-check integration;
- no package generation;
- no backend/frontend/Docker/CI/package/lockfile changes;
- no PR #1001 files;
- no cookie/token/secret handling;
- no update application operations.

Follow-up implemented by Y-AUTO-13 Codex prompt templates.

## Y-AUTO-13 Codex Prompt Templates State

Y-AUTO-13 adds `docs/llmwiki/codex-run-prompt-templates.md`.

Scope:

- docs-only Codex prompt templates;
- source-of-truth sync for automation efficiency, auto lanes, PR body generator
  design, current state, roadmap, and handoff;
- no script implementation;
- no checker implementation;
- no CI integration;
- no GitHub API integration;
- no PR creation/editing automation;
- no generated package output.

The new prompt template document covers:

- docs-only PR;
- report-only script PR;
- checker-only PR;
- combined report / checker / docs PR;
- High-mid PR-ready-only;
- human-reviewed merge;
- recovery / finalize;
- closeout / handoff sync;
- new app bootstrap.

Follow-up:

- Y-AUTO-15 implements the preflight environment checker.
- APP-BOOT-01 remains the next recommended candidate.

## Y-AUTO-14 Preflight Environment Checker Design State

Y-AUTO-14 adds `docs/llmwiki/preflight-environment-checker-design.md`.

Scope:

- docs-only preflight environment checker design;
- source-of-truth sync for automation efficiency, auto lanes, prompt templates,
  current state, roadmap, and handoff;
- no script implementation;
- no existing checker changes;
- no CI integration;
- no GitHub API integration;
- no PR creation/editing automation;
- no generated package output.

The new design covers:

- Python runtime discovery;
- Git repository and branch baseline checks;
- Git write-permission checks;
- GitHub CLI session state checks;
- remote and branch baseline checks;
- local helper exclusion checks;
- generated package folder absence checks;
- PR #1001 leakage precheck;
- local safety tool availability checks.

Implemented script path:

```text
scripts/check_local_dev_environment.py
```

Follow-up:

- Y-AUTO-15 implements the preflight environment checker.
- APP-BOOT-01 remains the next recommended candidate.

## Y-AUTO-15 Preflight Environment Checker State

Y-AUTO-15 implements `scripts/check_local_dev_environment.py`.

Behavior:

- Python runtime discovery;
- Git repository, branch, and metadata access checks;
- Git lock file detection;
- optional GitHub CLI session state check;
- remote and baseline ref checks;
- working tree summary;
- local helper exclusion check;
- generated folder absence check;
- PR #1001 leakage precheck;
- local safety tool availability check.

Not implemented:

- no file writes;
- no Git config changes;
- no branch creation;
- no GitHub write actions;
- no PR creation/editing;
- no merge actions;
- no package generation;
- no backend/frontend/Docker/CI/package/lockfile changes;
- no secret/token/cookie handling;
- no public hosting or ads;
- no update application operations.

Next candidate:

- APP-BOOT-01 new app bootstrap template design.

## APP-BOOT-01 New App Bootstrap Template Design State

APP-BOOT-01 adds a docs-only reusable bootstrap design for future app projects.

- New design doc:
  `docs/llmwiki/new-app-bootstrap-template-design.md`.
- Reusable method summarized:
  - LLMwiki;
  - risk tiers;
  - auto lanes;
  - preflight checker;
  - safety wording checker;
  - safety gate aggregator;
  - PR body generator;
  - Codex prompt templates.
- No new app files were created.
- No scripts were changed.
- No backend/frontend/Docker/CI/package/lockfile files were changed.
- No generated package output was created.

Next candidates:

- APP-BOOT-02 bootstrap skeleton design / packet.
- APP-00A actual new app purpose / user / MVP definition once the app idea is
  provided.
- Y-CI-01 lightweight CI design.
