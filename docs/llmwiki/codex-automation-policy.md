# Codex Automation Policy

## Purpose

Y-AUTO-01 defines the automation expansion policy for Codex work in this
local-only fork.

The goal is to let Codex continue safely through low-risk, medium-risk, and
qualifying high-low-risk work, including fork PR creation and fork squash merge
when all gates pass.

This policy is documentation only. It does not create package outputs, build
artifacts, installers, generated guide files, notice bundles, backend changes,
frontend changes, Docker changes, CI changes, dependency changes, package
changes, or lockfile changes.

## Sources Checked

Repository sources checked:

- `docs/llmwiki/current-state.md`
- `docs/llmwiki/roadmap.md`
- `docs/llmwiki/handoff.md`
- `docs/llmwiki/safety-boundaries.md`
- `docs/llmwiki/safety-gate-checker-design.md`
- `docs/llmwiki/clean-package-dry-run-contract.md`
- `scripts/check_repo_safety.py`
- `scripts/clean_package_dry_run.py`

No external references are required for this docs-only policy.

## Facts / Assumptions / Needs Verification

Facts:

- Fork `master` is the current source of truth.
- Local `master` tracks `fork/master`.
- Work must start from `fork/master`.
- Upstream PR #1001 must not be touched or mixed into fork-only work.
- The project remains local-only and personal-use only.
- `scripts/check_repo_safety.py` is report-only.
- `scripts/clean_package_dry_run.py` is dry-run-only and report-only.

Assumptions:

- `auto PR` means a PR inside `jsworkht-dotcom/metube`, targeting
  `fork/master`, after the task itself has authorized a fork PR flow.
- `auto merge` means squash merge of that fork PR only, after the policy gates,
  GitHub merge state, and checks are clean.
- The policy does not authorize upstream PRs, release tags, production deploys,
  public hosting, dependency changes, or generated package output.

Needs verification on each run:

- Current branch and base commit.
- Changed file list.
- Safety checker output.
- Clean-package dry-run output.
- GitHub PR `mergeStateStatus`.
- GitHub check conclusions.

## Global Rules

- Start from `fork/master`.
- Keep fork-only work separate from upstream PR #1001.
- Keep the detailed source of truth in `docs/llmwiki/`.
- Do not create `動画保存ツール_ローカル専用/`.
- Do not create ZIP, package, installer, generated guide, generated notice, or
  generated manifest output.
- Do not run build, package, install, dependency update, Docker pull, or Docker
  build commands.
- Do not change backend download, queue, subscription, extractor, or yt-dlp
  logic without a later explicit implementation task.
- Do not read, print, store, transform, or handle real cookie, token, secret, or
  credential values.
- Do not add public hosting, external-user service behavior, ads, or
  monetization.
- For update-related future work, use `更新適用機能` in policy prose.

## Risk Levels

### 1. Low

Allowed examples:

- `docs/llmwiki/` documentation.
- Notice source material.
- Guide source material.
- Inventory source material.
- Roadmap, handoff, and current-state synchronization.

Automation result:

- Auto PR is OK.
- Auto merge is OK.
- Required gates must still pass for the current task.

### 2. Medium

Allowed examples:

- Report-only scripts.
- Dry-run scripts.
- Checker warning logic.
- Read-only inspection.
- Small safe UX copy or display changes.

Automation result:

- Auto PR is OK.
- Auto merge is OK if safety gates pass.
- The diff must not include backend risky behavior, package output, dependency
  changes, generated distribution folders, credential handling, public hosting,
  ads, or PR #1001 file leakage.

### 3. High-low

Definition:

- Work that is close to high-risk areas but remains strictly docs-only,
  report-only, or dry-run-only.
- It must not perform real generation, real application, dependency install, or
  package build; Docker pull is prohibited; Docker build and distribution output
  creation are also prohibited.

Allowed examples:

- Clean package generator contract additions.
- Package manifest preview design.
- Notice bundle dry-run design.
- Generated output preview design.
- Desktop shell scaffold plan.
- Backup and rollback design docs.
- Package preflight checker.
- Output diff prediction report.

Automation result:

- Auto PR is OK when all high-low mandatory conditions pass.
- Auto merge is OK only when all high-low mandatory conditions pass, GitHub
  merge state is clean, and no checks failed.

High-low mandatory conditions:

- Scope is one of docs-only, report-only, or dry-run-only.
- Real distribution folder generation is prohibited.
- ZIP, package, and installer creation are prohibited.
- Dependency install/update is prohibited.
- Package and lockfile changes are prohibited.
- Docker pull/build is prohibited.
- Backend download, queue, subscription, extractor, and yt-dlp logic changes are
  prohibited.
- Cookie/token/secret handling is prohibited.
- Public hosting and ads are prohibited.
- `python scripts/check_repo_safety.py` returns OK.
- `python scripts/check_repo_safety.py --base fork/master` returns OK.
- `python scripts/clean_package_dry_run.py` returns OK.
- `git diff --check` returns OK.
- GitHub PR `mergeStateStatus` is `CLEAN`.
- GitHub checks have no failure conclusions.

### 4. High-mid

Definition:

- Work that approaches real generation or real implementation but can still be
  kept as a prototype or limited implementation.

Examples:

- Real distribution folder generation script.
- `NOTICE.txt` or `LICENSES` real generation script.
- Package manifest real generation script.
- Tauri or Electron scaffold.
- Local launcher wrapper prototype.
- Stop/exit UI implementation.
- Save-folder or open-folder UI implementation.

Automation result:

- Codex may work and create a PR when the task explicitly approves the scope.
- Auto merge is prohibited.
- Human review is required before merge.

### 5. High-high

Definition:

- Work that Codex must not start automatically.
- Codex must stop before implementation and request explicit human confirmation.

Examples:

- ZIP, installer, package, or real distribution release.
- Tauri or Electron full adoption.
- Dependency install/update.
- Package or lockfile changes.
- Docker pull/build work is prohibited for automatic execution.
- Backend download, queue, subscription, extractor, or yt-dlp behavior changes.
- Update delivery or 更新適用機能.
- Backup or rollback real creation.
- Cookie/token/secret handling.
- Public hosting.
- Ads or monetization.

Automation result:

- Automatic execution is prohibited.
- Auto merge is prohibited.
- Human confirmation is required before any implementation begins.

## Auto PR / Auto Merge Gate

Before auto PR:

- Confirm the branch started from `fork/master`.
- Confirm changed files are inside the allowed risk-level scope.
- Confirm upstream PR #1001 files are absent from the diff.
- Run `git diff --check`.
- Run `python scripts/check_repo_safety.py`.
- Run `python scripts/check_repo_safety.py --base fork/master`.
- Run `python scripts/clean_package_dry_run.py`.
- Confirm no generated `動画保存ツール_ローカル専用/` folder exists.
- Confirm no backend/frontend/Docker/CI/package/lockfile diff exists unless the
  risk level and task explicitly allow it.
- Confirm no real cookie/token/secret value appears in the diff or reports.

Before auto merge:

- Confirm the PR targets `fork/master` in the fork repository.
- Confirm `mergeStateStatus` is `CLEAN`.
- Confirm checks have no failure conclusions.
- Confirm the PR changed-file list still matches the approved risk level.
- Confirm the PR body or final report includes a sanitized safety summary.
- For high-low work, re-confirm all high-low mandatory conditions.

## Stop Conditions

Stop and report facts if any of these occur:

- `scripts/check_repo_safety.py` reports `BLOCKED`.
- `scripts/clean_package_dry_run.py` reports `BLOCKED`.
- Changed files are outside the approved scope.
- Backend, frontend, Docker, CI, package, or lockfile files changed outside an
  explicitly approved implementation task.
- A real cookie/token/secret value is detected.
- Upstream PR #1001 files are present in the changed-file list.
- GitHub PR `mergeStateStatus` is not `CLEAN`.
- Any required GitHub check failed.
- The repository root contains `動画保存ツール_ローカル専用/`.

## Relationship To Existing Gates

`scripts/check_repo_safety.py` remains the repository-diff safety gate.

`scripts/clean_package_dry_run.py` remains the package-planning dry-run gate.

For high-low auto merge, both gates are required because the work is close to
package generation, desktop shell, backup/rollback, or output-preview areas even
when the task itself remains docs-only, report-only, or dry-run-only.

This policy does not weaken human approval gates for destructive actions,
credentials, production deployment, infrastructure mutation, dependency changes,
public hosting, releases, or customer-data work.

## Y-AUTO-01 Boundary

Y-AUTO-01 is docs-only. It may add this policy and synchronize related
`docs/llmwiki/` source-of-truth files.

Y-AUTO-01 must not:

- Create generated package folders.
- Create generated guide, notice, manifest, ZIP, package, or installer files.
- Run build/package/install commands.
- Change dependencies, package files, or lockfiles.
- Change backend, frontend, Docker, or CI files.
- Handle cookie/token/secret values.
- Touch upstream PR #1001 files.
- Add public hosting or ads.
