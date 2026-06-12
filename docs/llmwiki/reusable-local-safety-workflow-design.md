# Y-CI-03 Reusable Local Safety Workflow Design

## Purpose

Y-CI-03 was a docs-only design for a reusable GitHub Actions workflow that can
host the existing local fork safety checks. It completed via fork PR #95.

Y-CI-03B completed the reusable workflow implementation via fork PR #96. It
changed only `.github/workflows/` plus minimal docs sync by keeping
`.github/workflows/local-fork-safety.yml` as the PR caller and adding
`.github/workflows/reusable-local-safety.yml` as the `workflow_call` target.

Y-CI-04 completed the concurrency implementation via fork PR #97. It keeps the
same caller and reusable workflow split while adding workflow-level concurrency
only to the caller.

Y-GH-01 records the separate branch protection / ruleset design in
`docs/llmwiki/branch-protection-design.md` without mutating GitHub settings or
configuring required checks.

## Sources Checked

Repository sources:

- `.github/workflows/local-fork-safety.yml`
- `docs/llmwiki/lightweight-safety-workflow-design.md`
- `docs/llmwiki/current-state.md`
- `docs/llmwiki/roadmap.md`
- `docs/llmwiki/handoff.md`
- `docs/llmwiki/codex-automation-policy.md`
- `docs/llmwiki/automation-efficiency-policy.md`

External references checked:

- GitHub Docs, reusable workflows:
  `https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows`
- GitHub Docs, workflow syntax permissions:
  `https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions`
- GitHub Docs, workflow concurrency:
  `https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency`

## Facts / Assumptions / Needs Verification

Facts:

- Current workflow path: `.github/workflows/local-fork-safety.yml`.
- Current workflow name: `local-fork-safety`.
- The workflow runs on pull requests targeting `master`.
- Current workflow permissions are `contents: read`.
- The current job name shown in GitHub UI is `local fork safety`.
- GitHub reusable workflows require `on: workflow_call`.
- A same-repository reusable workflow can be called with
  `uses: ./.github/workflows/<filename>`.
- For same-repository local calls, the called workflow comes from the same
  commit as the caller workflow.
- In Y-CI-03B, `.github/workflows/local-fork-safety.yml` is the caller.
- In Y-CI-03B, `.github/workflows/reusable-local-safety.yml` is the reusable
  `workflow_call` target.
- In Y-CI-04, the caller owns workflow-level concurrency with
  `group: ${{ github.workflow }}-${{ github.ref }}` and
  `cancel-in-progress: true`.
- Both workflows keep `permissions: contents: read`.

Assumptions carried into implementation:

- The caller remains `.github/workflows/local-fork-safety.yml`.
- The reusable workflow target is
  `.github/workflows/reusable-local-safety.yml`.
- The caller stays responsible for PR visibility and target branch selection.
- The reusable workflow owns the local safety job steps.

Needs verification during Y-CI-03B PR checks:

- GitHub accepts the same-repository `uses:
  ./.github/workflows/reusable-local-safety.yml` call in this repository.
- The called workflow runs from the PR commit and not from an unexpected base
  version.
- The visible job and check names stay stable enough for any later branch
  protection design.
- `permissions: contents: read` remains sufficient for checkout and the
  read-only `fork/master` fetch.
- Normal docs-only PRs still pass.
- PR #1001 files and generated package folders still fail when introduced.
- No dependency install/update, Docker operation, artifact upload, cache,
  package output, branch protection, required-check, CODEOWNERS, secret, or
  `pull_request_target` behavior appears.

## Current Workflow Baseline

Existing workflow:

```text
.github/workflows/local-fork-safety.yml
```

Current behavior:

- Trigger: `pull_request` targeting `master`.
- Permissions: `contents: read`.
- Checkout: `actions/checkout@v6` with `fetch-depth: 0`.
- Base ref: creates a read-only `fork/master` remote-tracking ref.
- Runs repository safety check:
  `python scripts/check_repo_safety.py`.
- Runs base-aware repository safety check:
  `python scripts/check_repo_safety.py --base fork/master`.
- Runs clean package report regression check:
  `python scripts/check_clean_package_dry_run_reports.py`.
- Runs clean package dry-run JSON parse check:
  `python scripts/clean_package_dry_run.py --format json`.
- Runs safety wording check:
  `python scripts/check_safety_wording.py --base fork/master`.
- Confirms generated package folder absence:
  `動画保存ツール_ローカル専用/`.
- Confirms PR #1001 files are absent from the PR diff:
  `docker-compose.local.yml` and `docs/local-only.md`.
- Prints a safety boundary message that success does not approve package,
  ZIP, installer, metadata, checksum, or CLEAN folder generation.

## Reusable Workflow Target

Reusable workflow target:

```text
.github/workflows/reusable-local-safety.yml
```

Trigger:

```yaml
on:
  workflow_call:
```

Caller workflow:

```text
.github/workflows/local-fork-safety.yml
```

The caller keeps the `pull_request` trigger and `contents: read` permissions,
then calls the reusable workflow as the local safety job.

## Y-CI-03B Structure

`local-fork-safety.yml`:

- Keeps the `pull_request` trigger for PRs targeting `master`.
- Keeps `permissions: contents: read`.
- Calls `./.github/workflows/reusable-local-safety.yml`.
- Remains the PR visibility layer and the user-facing workflow entry point.

`reusable-local-safety.yml`:

- Uses `workflow_call`.
- Contains the local safety job and current safety steps.
- Uses read-only repository access.
- Does not upload artifacts.
- Does not install dependencies.
- Does not use Docker.
- Does not generate package output.

Implementation shape:

```yaml
# .github/workflows/local-fork-safety.yml
name: local-fork-safety

on:
  pull_request:
    branches:
      - master

permissions:
  contents: read

jobs:
  safety:
    name: local fork safety
    uses: ./.github/workflows/reusable-local-safety.yml
```

```yaml
# .github/workflows/reusable-local-safety.yml
name: reusable-local-safety

on:
  workflow_call:

permissions:
  contents: read

jobs:
  safety:
    name: local fork safety
    runs-on: ubuntu-latest
    steps:
      # Same local safety steps as the current workflow.
```

Y-CI-03B validates this syntax locally where possible, then confirms the
caller/reusable behavior with the GitHub Actions PR check.

## Y-CI-04 Structure

`local-fork-safety.yml`:

- Keeps the `pull_request` trigger for PRs targeting `master`.
- Keeps `permissions: contents: read`.
- Keeps calling `./.github/workflows/reusable-local-safety.yml`.
- Adds workflow-level concurrency:
  `group: ${{ github.workflow }}-${{ github.ref }}` and
  `cancel-in-progress: true`.
- Remains the PR visibility layer and the user-facing workflow entry point.

`reusable-local-safety.yml`:

- Remains the `workflow_call` target.
- Keeps `permissions: contents: read`.
- Keeps the existing local safety steps unchanged.

Expected behavior: a newer `local-fork-safety` run cancels older in-progress
runs in the same workflow/ref concurrency group while the reusable safety job
continues to run the same checks.

Expected CI-scope blocker: repository safety checks may classify
`.github/workflows/` changes as human-review-required. That blocker should be
limited to the workflow-file scope and should not include dependency
install/update, Docker, artifact generation, package output, PR #1001 files, or
generated package folders.

## Why Reusable

- Future manual smoke PRs can reuse the same safety job.
- Future workflow variants can avoid duplicate shell and Python script steps.
- Future branch-protection candidates can point at stable workflow or job
  naming instead of duplicated job variants.
- `local-fork-safety` remains a PR visibility layer while the safety job becomes
  reusable.
- Reuse makes later changes easier to audit because the safety step list has one
  intended source.

## Risks

- `.github/workflows` changes are CI-scope and human-review-required.
- The first implementation PR may produce an expected checker blocker if
  `.github/workflows` changes are still classified as blocked.
- Reusable workflow syntax mistakes can break all PR safety checks.
- Job name stability matters if future required checks are considered.
- `workflow_call` local path behavior must be tested in a PR before any branch
  protection candidate depends on it.
- Splitting caller and reusable job can change the displayed check naming; this
  must be observed before required-check configuration is designed.

## Y-CI-03B Implementation Constraints

Y-CI-03B must keep these constraints:

- No dependency install or update.
- No container image retrieval or build operation.
- No frontend build or test.
- No backend pytest.
- No package output.
- No generated artifacts.
- No metadata generation.
- No checksum generation.
- No real download.
- No credentials or secrets beyond the default GitHub token for read-only
  checkout.
- `permissions: contents: read`.
- No `pull_request_target`.
- No secrets or `secrets: inherit`.
- No artifact upload.
- No cache addition.
- No branch protection mutation.
- No required-check configuration.
- No CODEOWNERS changes.

## Y-CI-03B Success Criteria

Future Y-CI-03B succeeds only if:

- `local-fork-safety` runs on a PR.
- `reusable-local-safety` is called successfully.
- The same checks as the current workflow still run.
- A normal docs-only PR passes.
- PR #1001 files still fail if introduced.
- The generated package folder still fails if present.
- Warning-only wording remains non-blocking.
- No broader permissions, dependency setup, Docker operation, package output, or
  artifact generation is introduced.
- No `pull_request_target`, secrets, artifact upload, cache, branch protection,
  required-check configuration, or CODEOWNERS change is introduced.

## Stop Conditions

Stop Y-CI-03B and report facts if any of these occur:

- Workflow syntax cannot be validated.
- `local-fork-safety` does not run.
- The reusable workflow is not called.
- Checks are silently skipped.
- Permissions expand beyond `contents: read` without explicit approval.
- `pull_request_target` appears.
- Secrets or `secrets: inherit` appears.
- Artifact upload or cache appears.
- Dependency install or update becomes necessary.
- Container image retrieval or build becomes necessary.
- A generated artifact appears.
- PR #1001 files appear.
- `動画保存ツール_ローカル専用/` appears.
- Token, secret, or cookie handling becomes necessary.

## Next Candidates

```text
Y-CI-05 post-workflow-change observation PR
Y-GH-02 required checks design
Y-WIKI-CLEAN-01 current-state / handoff / archive整理
```

## Not Included In Y-CI-03

- No `.github/workflows/` changes.
- No backend, frontend, Docker, package, or lockfile changes.
- No dependency install or update.
- No container image retrieval or build operation.
- No frontend build or test.
- No backend pytest.
- No CLEAN folder.
- No `動画保存ツール_ローカル専用/`.
- No ZIP, installer, or package output.
- No metadata generation.
- No checksum generation.
- No real download.
- No branch protection change.
- No required-check configuration.
- No CODEOWNERS change.
- No `.gitignore` change.
- No token, secret, cookie, or credential handling.
- No PR #1001 file changes.
