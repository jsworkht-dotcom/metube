# Y-CI-03 Reusable Local Safety Workflow Design

## Purpose

Y-CI-03 is a docs-only design for a future reusable GitHub Actions workflow
that can host the existing local fork safety checks.

This design does not change `.github/workflows/`. The implementation is reserved
for Y-CI-03B.

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

Assumptions:

- The future caller remains `.github/workflows/local-fork-safety.yml`.
- The future reusable workflow candidate is
  `.github/workflows/reusable-local-safety.yml`.
- The future caller should stay responsible for PR visibility and target branch
  selection.
- The future reusable workflow should own the local safety job steps.

Needs verification during Y-CI-03B:

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

Future reusable workflow candidate:

```text
.github/workflows/reusable-local-safety.yml
```

Trigger:

```yaml
on:
  workflow_call:
```

Future caller workflow:

```text
.github/workflows/local-fork-safety.yml
```

The future caller should keep the `pull_request` trigger and `contents: read`
permissions, then call the reusable workflow as the local safety job.

## Expected Future Structure

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

Initial future shape:

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

Y-CI-03B should validate the exact syntax before PR handoff. This design is not
an implementation approval.

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

Future Y-CI-03B must keep these constraints:

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

## Stop Conditions

Stop Y-CI-03B and report facts if any of these occur:

- Workflow syntax cannot be validated.
- `local-fork-safety` does not run.
- The reusable workflow is not called.
- Checks are silently skipped.
- Permissions expand beyond `contents: read` without explicit approval.
- Dependency install or update becomes necessary.
- Container image retrieval or build becomes necessary.
- A generated artifact appears.
- PR #1001 files appear.
- Token, secret, or cookie handling becomes necessary.

## Next Candidates

```text
Y-CI-03B reusable workflow implementation
Y-CI-04 concurrency / cancel-in-progress
Y-GH-01 branch protection design
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
