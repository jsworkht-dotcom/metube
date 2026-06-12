# Y-CI-01 Lightweight Safety Workflow Design

## Purpose

Design and track the minimal GitHub Actions safety workflow for this fork.

Y-CI-01 was design-only. Y-CI-02 implements the initial workflow file while
still avoiding required checks, branch protection, CODEOWNERS, dependency
installation operations, container image operations, generated package output,
metadata/checksum generation, or runtime download behavior.

## Candidate Workflow

- Workflow name: `local-fork-safety`
- Implemented file: `.github/workflows/local-fork-safety.yml`
- Initial permissions:

```yaml
permissions:
  contents: read
```

The workflow should only read the repository and report safety status. It
should not write comments, mutate branches, upload release artifacts, change
protection rules, or access credentials beyond the default read-only checkout
needs.

## Initial Checks

The initial implementation uses the repository's existing stdlib-friendly
safety tools and avoids dependency setup:

```text
python scripts/check_repo_safety.py
python scripts/check_repo_safety.py --base fork/master
python scripts/check_clean_package_dry_run_reports.py
python scripts/clean_package_dry_run.py --format json
python scripts/check_safety_wording.py --base fork/master
generated package folder absence check
PR #1001 files absence check
```

Implementation note: GitHub Actions may not naturally have a `fork/master`
remote ref after checkout. Y-CI-02 creates `refs/remotes/fork/master` with a
read-only fetch from the workflow repository before running base diff checks.

Y-CI-03B reusable split note: the PR-facing workflow remains
`.github/workflows/local-fork-safety.yml`, but it now acts as the caller for
`.github/workflows/reusable-local-safety.yml`. The reusable workflow is the
`workflow_call` target and owns the same safety steps listed above.
Permissions remain `contents: read`; the split does not add dependency
installation, Docker operations, package/artifact output, branch protection,
required-check configuration, CODEOWNERS, secrets, artifact upload, or cache.

Y-CI-04 concurrency note: the PR-facing caller now owns workflow-level
concurrency with `group: ${{ github.workflow }}-${{ github.ref }}` and
`cancel-in-progress: true`. The reusable workflow safety steps remain
unchanged, and permissions remain `contents: read`.

## Explicit Non-Goals

The initial workflow should not run:

- dependency installation operations;
- container image operations;
- frontend build or tests;
- backend pytest that requires dependency installation operations;
- package, ZIP, installer, or generated package output creation;
- metadata or checksum generation;
- real downloads;
- branch protection mutation;
- CODEOWNERS addition;
- required-check configuration.

## Event Design

### Candidate A

```yaml
on:
  pull_request:
    branches:
      - master
```

Pros:

- Runs on every PR targeting fork `master`.
- Avoids silent gaps when safety-sensitive paths change outside docs or
  scripts.
- Better fit for PR #1001 leakage checks, generated package folder checks, and
  forbidden-path checks.
- Keeps the first workflow simple.

Cons:

- More PRs run the workflow.
- Some PRs may show warnings for scopes the local checker classifies as
  Unknown.

### Candidate B

```yaml
on:
  pull_request:
    branches:
      - master
    paths:
      - "docs/llmwiki/**"
      - "scripts/**"
```

Pros:

- Reduces runs for unrelated source-only PRs.
- Focuses on the current docs/checker lanes.

Cons:

- Can miss safety-relevant changes outside `docs/llmwiki/**` and `scripts/**`.
- Would not automatically cover future app, UI, workflow, package, or PR #1001
  path changes.
- Makes the first workflow less useful as a general safety signal.

### Initial Recommendation

Use Candidate A for Y-CI-02. The workflow is intentionally lightweight, so the
first priority should be broad PR visibility rather than path-level
optimization. Revisit path filters only after real PR noise is observed.

## Concurrency Design

Y-CI-02 intentionally deferred concurrency so the first workflow stayed minimal
and easy to audit.

Y-CI-04 adds:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

This cancels older in-progress `local-fork-safety` runs for the same workflow
and PR ref while keeping cancellation behavior separate from the reusable safety
steps.

## Failure And Warning Policy

- Blockers should fail CI.
- Warning-only findings should keep CI successful and remain visible in logs.
- `check_safety_wording.py` warning output should not fail the workflow unless a
  later policy explicitly changes severity handling.
- Existing local-only helper noise such as untracked local context files should
  normally not appear in the GitHub Actions checkout.
- CI success does not approve generated package output.
- CI success does not approve package, ZIP, installer, metadata, checksum, or
  CLEAN folder generation.

## Relationship To Local Gates

`local-fork-safety` is a PR safety display. It does not replace:

- `scripts/run_local_safety_gates.py`;
- local pre-PR checks;
- human review requirements;
- High-mid / High-high merge restrictions;
- generated package approval rules.

Local gates remain authoritative before PR creation and before any human or
automation-assisted merge decision.

## Future Phases

```text
Y-CI-03 reusable workflow design
Y-CI-03B reusable workflow implementation
Y-CI-04 concurrency / cancel-in-progress
Y-GH-01 branch protection design
Y-GH-02 required checks design
```

Y-CI-03 kept reusable workflow work docs-only. Y-CI-03B implements the split
while preserving `local-fork-safety` as the PR visibility layer and moving the
current safety job into a `workflow_call` reusable workflow.
Y-CI-04 adds caller-owned concurrency / cancel-in-progress without changing the
reusable safety steps.

Branch protection, required checks, and CODEOWNERS should remain separate design
or implementation lanes.
