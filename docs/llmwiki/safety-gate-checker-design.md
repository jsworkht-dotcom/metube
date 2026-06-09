# Y-CHECK-01 Safety Gate Checker Design

## Purpose

Y-CHECK-01 defines a docs-only design for a future repository safety checker and
automation gate.

The goal is to let low-, medium-, and qualifying high-low-risk Codex work
continue more smoothly when the repository diff is clearly inside the approved
scope, while still stopping on paths, content, or behavior that require human
review.

This document does not implement a checker, add scripts, change CI, change
packages, generate distribution files, or approve automatic update execution.

## Sources Checked

Repository sources checked:

- `docs/llmwiki/current-state.md`
- `docs/llmwiki/roadmap.md`
- `docs/llmwiki/handoff.md`
- `docs/llmwiki/safety-boundaries.md`
- `docs/llmwiki/codex-automation-policy.md`
- `docs/llmwiki/clean-package-dry-run-contract.md`
- `docs/llmwiki/beginner-guide-source-plan.md`
- `docs/llmwiki/license-notice-plan.md`
- `docs/llmwiki/codex-gh-auth-runbook.md`

No external references are required for this docs-only design.

## Facts / Assumptions / Needs Verification

Facts:

- The fork `master` branch is the current source of truth.
- Upstream PR #1001 must not be mixed into unrelated fork work.
- Current package-related dry-run behavior is report-only and must not generate
  package output.
- Update readiness work is readonly; update execution remains intentionally not
  implemented.

Assumptions:

- The first checker implementation, if approved later, should be local and
  report-only.
- The checker should evaluate a diff against a base ref such as `fork/master`.
- A later automation wrapper may consume the same report, but the report itself
  should remain useful to a human reviewer.

Needs verification before implementation:

- Exact command names, output format, and invocation location.
- Whether the first implementation is a local script only, a PR helper, or a CI
  job.
- GitHub Actions shell behavior if CI integration is later approved.
- Any changed path rules for future non-docs tasks.

## Scope

Allowed by this design:

- Define future checks and expected outcomes.
- Define warning, blocked, and manual-review classifications.
- Define sanitized report fields for PR review.
- Define how the gate relates to package dry-run checks and LLMwiki consistency.

Not allowed by this design:

- Implementing a checker script.
- Adding or changing CI.
- Adding package, build, install, Docker, backend, frontend, or lockfile changes.
- Creating `動画保存ツール_ローカル専用/`.
- Running package generation, Docker pull, dependency install/update, update
  apply, git pull / merge / rebase as app behavior, restart, or external sends.
- Reading, printing, storing, or transforming real cookie, token, secret, or
  credential values.
- Touching upstream PR #1001.

## Gate Model

The future gate should classify the current work as one of these outcomes:

| Outcome | Meaning |
| --- | --- |
| `pass` | No blockers or warnings were found. |
| `pass_with_warnings` | No blockers were found, but review notes remain. |
| `manual_review` | The checker cannot prove safety from local context. |
| `blocked` | The work must stop until the diff or task scope changes. |

Rules:

- `blocked` takes precedence over all other outcomes.
- `manual_review` takes precedence over `pass_with_warnings`.
- Warnings must be visible in the PR safety summary.
- The gate does not override human approval requirements for destructive,
  credential, deployment, infrastructure, package install/update, push, merge, or
  release actions.

## Inputs

Candidate future inputs:

- Repository root.
- Base ref, normally `fork/master` for fork work.
- Changed file list from the working tree, staged diff, or PR diff.
- Added or changed text lines from the diff.
- Task scope policy, such as docs-only or implementation-approved.
- Known forbidden path families.
- Known upstream PR #1001 file paths.
- LLMwiki required-reference list.

The checker should avoid reading secret-bearing files unless the file itself is
already part of the changed diff. Even then, reports must omit matched values.

## Check 1: Changed Files Scope Check

Purpose:

- Confirm that changed files match the task-approved scope.

For a docs-only LLMwiki task, the allowed path set is:

```text
docs/llmwiki/**
```

Blocked for docs-only work:

- `app/**`
- `ui/**`
- `Dockerfile`
- `docker-compose*.yml`
- `.github/**`
- package manager files and lockfiles
- generated distribution files
- scripts or executable tooling

Outcome:

- `blocked` if any changed file is outside the allowed path set.
- `manual_review` if the checker cannot determine the base ref or changed file
  list.
- `pass` if all changed files match the allowed path set.

## Check 2: Forbidden Path Check

Purpose:

- Prevent accidental inclusion of repository internals, caches, local state,
  private values, or generated outputs.

Blocked path families:

- `.git/`
- `.github/` when not explicitly approved
- `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`, `.cache/`
- `node_modules/`, `ui/node_modules/`, `ui/.angular/`
- `dist/`, `build/`, `.next/`, `coverage/`, `.turbo/`
- `downloads/`, `state/`, `logs/`, `temp/`
- local virtual environments and package manager caches
- `.env`, `.env.*`
- filenames containing `cookie`, `token`, `secret`, `credential`, or `password`
- files ending in `.pem`, `.key`, `.p12`, or `.pfx`
- `動画保存ツール_ローカル専用/`

Outcome:

- `blocked` if a forbidden path is changed or selected for output.
- `manual_review` for symlinks, junctions, shortcuts, or unresolved paths.
- `pass` if no forbidden path is present.

## Check 3: Secret-Like Pattern Check

Purpose:

- Stop diffs that include credential-like values without exposing those values in
  reports.

Pattern families:

- cookie-like assignment
- token-like assignment
- secret-like assignment
- password-like assignment
- private key marker
- private environment assignment
- credential-bearing URL
- webhook or API key candidate

Rules:

- Scan changed text lines, not entire unrelated files by default.
- Report only repository-relative path, line number when safe, and pattern
  family.
- Do not echo matched values.
- Mentions of words such as `cookie`, `token`, or `secret` in safety
  documentation are not enough to block by themselves.
- High-confidence assignment or key material findings are `blocked`.
- Ambiguous explanatory prose is `manual_review` only when the pattern cannot be
  safely classified.

## Check 4: Generated Distribution Folder Check

Purpose:

- Keep docs-only and source-only work from mixing with package outputs.

Rules:

- Block if the repository root contains a real `動画保存ツール_ローカル専用/`
  directory.
- Block if any changed file is inside that generated package root.
- Do not block documentation that merely names the future package root as a
  planned path.

Outcome:

- `blocked` for an existing generated root or changed generated files.
- `pass` if only LLMwiki planning references exist.

## Check 5: PR #1001 File Leakage Check

Purpose:

- Keep upstream PR #1001 files out of unrelated fork work.

Blocked file paths:

```text
docker-compose.local.yml
docs/local-only.md
```

Rules:

- Block if either path appears in the changed file list.
- Block if either path is selected for package output.
- Allow LLMwiki references that explain the boundary and do not modify the PR
  files.
- Do not fetch, update, rewrite, or otherwise touch upstream PR #1001 as part of
  this gate.

Outcome:

- `blocked` on file leakage.
- `pass` on boundary-only documentation references.

## Check 6: Dangerous Behavior Scan

Purpose:

- Catch diffs that introduce behavior outside the local-only safety boundary.

Behavior families to scan:

- public hosting, public tunnel, reverse proxy, or LAN service mode
- ads, monetization, or external-user offering
- DRM bypass, authentication bypass, or restriction circumvention
- mass-download optimization
- cookie/token/secret handling
- external sends such as email, SMS, webhook, or push notification
- destructive data operations
- production deployment, DNS, billing, payment, auth, permission, or customer
  data changes

Rules:

- In docs-only safety-boundary prose, these terms can be allowed when they are
  explicitly described as prohibited.
- In code, scripts, CI, config, or package files, additions in these families
  should default to `blocked` unless the task explicitly approved that exact
  scope.

## Check 7: Update Execution Scan

Purpose:

- Preserve the readonly update-readiness boundary.

Blocked behavior families:

- update apply endpoint or button
- backup creation as part of update prepare/apply
- rollback creation as part of update prepare/apply
- Docker pull
- git pull / merge / rebase as app behavior
- restart
- pip install
- package install or package update
- dependency update

Rules:

- Documentation may mention these behaviors only as prohibited, blocked, or
  future-manual-approval items.
- Implementation diffs that add these behaviors are `blocked` unless a later
  task explicitly approves that exact scope.

## Check 8: Package Guide / Notice Completeness Warning

Purpose:

- Keep package planning visible without blocking safe docs-only work.

Warning families:

- missing beginner guide source candidate
- missing TXT fallback source candidate
- missing local-only safety notice source
- missing license or notice source candidate
- incomplete Windows package section
- incomplete macOS package section
- missing checksum or manifest source plan

Outcome:

- `pass_with_warnings` when these are the only findings.
- `blocked` only if missing material is combined with an actual package
  generation attempt.

## Check 9: LLMwiki Consistency Check

Purpose:

- Keep the detailed source of truth in `docs/llmwiki/` coherent after each
  safety-relevant task.

Candidate consistency rules:

- New safety gate designs should be listed in `handoff.md`.
- Completed design outcomes should be summarized in `current-state.md`.
- The next step should be updated in `roadmap.md`.
- New safety boundaries should be reflected in `safety-boundaries.md`.
- Automation policy changes should be reflected in
  `codex-automation-policy.md`.
- Package-adjacent checker behavior should cross-reference
  `clean-package-dry-run-contract.md`.
- "Not implemented" lists must remain accurate.

Outcome:

- `pass_with_warnings` for missing cross-references.
- `manual_review` for contradictions between LLMwiki documents.
- `blocked` if a document claims implementation approval that the task did not
  grant.

## Check 10: PR Safety Gate Summary

Purpose:

- Produce a short sanitized summary that can be placed in a PR body or review
  comment.

Candidate summary fields:

```text
gate_status
base_ref
head_ref
changed_file_count
changed_files
risk_tier
risk_automation
risk_reason
scope_result
forbidden_path_result
secret_like_pattern_result
generated_distribution_result
pr_1001_leakage_result
dangerous_behavior_result
update_execution_result
package_guide_notice_warning_result
llmwiki_consistency_result
warnings
blocked_reasons
manual_review_reasons
sanitization_note
```

Rules:

- The summary must not include secret values, token values, cookie values,
  private URLs, private local paths beyond repository-relative paths, or command
  logs.
- The summary must explicitly state whether backend, frontend, Docker, CI,
  package, lockfile, script, or generated distribution files changed.
- The summary should include a human-readable final line such as:

```text
Safety gate: pass_with_warnings; docs/llmwiki-only diff; no generated package
folder; no PR #1001 file leakage; no secret-like values printed.
```

## Relationship To Clean Package Dry-Run

The clean-package dry-run remains package-focused. It classifies planned package
contents before any package generation.

The Y-CHECK-01 safety gate is broader. It classifies repository diffs and PR
readiness, including docs-only scope, forbidden paths, update behavior, and
LLMwiki consistency.

Future implementation should avoid duplicating policy prose by referencing the
same path families and warning categories where practical, but it should keep the
gate report separate from package generation reports.

## Relationship To Codex Automation Policy

The automation policy is documented in
`docs/llmwiki/codex-automation-policy.md`.

The checker remains a report-only repository diff gate. It does not decide by
itself that high-low auto merge is safe. For high-low work, the automation
policy requires this checker, the clean-package dry-run, `git diff --check`,
GitHub clean merge state, and successful checks to agree before auto merge.

Y-AUTO-02 adds a report-only `Risk classification` section to the text report.
The section contains `tier`, `automation`, and `reason` so PR summaries can
distinguish auto-merge-eligible work from human-merge or stop-before-PR work.
This does not change the existing `Status: OK` / `Status: BLOCKED` gate.

Y-AUTO-04 extends the report-only risk classification so High-mid-like
implementation-adjacent or generated-output-adjacent scopes report
`automation: pr-only-human-merge`. The reason must mention that auto merge is
disabled, human review is required before merge, and the PR body must include
`human-review-required`.

High-mid and high-high work remain outside auto merge. High-mid work may proceed
through implementation, verification, PR creation, and Ready-for-review handoff
when the task explicitly approves the scope, but the PR must state
`human-review-required` and wait for human merge approval.

If a high-mid candidate requires package/lockfile changes, dependency
install/update, backend download or queue logic changes, yt-dlp or extractor
changes, credential handling, public hosting, ads, real distribution output,
ZIP/package/installer output, or generated artifacts created during verification
without separate human approval, the task must stop or be treated as
High-high-leaning. Docker pull/build is prohibited and must stop the task.

High-mid PR summaries should explain why the work is High-mid, what was not
performed, rollback/cleanup candidates, and remaining risk. The checker remains
report-only; it does not grant merge approval.

For High-mid PR body dry-runs, the required reviewer-visible fields are:

- `Risk tier: High-mid`
- `Automation decision: PR-ready only`
- `automation: pr-only-human-merge`
- `human-review-required`
- `Why High-mid`
- `Explicitly not performed`
- `Verification`
- `Rollback / cleanup candidates`
- `Residual risks`
- `Human review checklist`

## Suggested Implementation Sequence

Y-CHECK-02 implements stage 1:

```text
scripts/check_repo_safety.py
```

Implemented stage 1 behavior:

- Local report-only checker.
- Stdlib-only.
- Text output.
- Current working tree diff by default, including untracked files.
- Optional `--base` branch diff context.
- Sanitized secret-like findings with path, line, and pattern family only.
- Risk classification summary with tier, automation, and reason.
- High-mid-like scope guidance with `pr-only-human-merge`.
- Exit codes `0` for OK/warning-only, `1` for blocked, and `2` for usage
  errors.

Only a later explicit task may implement the remaining stages:

1. Add an optional JSON output mode after the text report is reviewed.
2. Add a PR body summary helper after the report shape is stable.
3. Add CI integration only after local behavior is stable and explicitly
   approved.

Each stage must remain blocked if it would add package generation, update
execution, dependency installation, Docker pull, generated distribution folders,
or credential handling.

## Stop Conditions

Stop and report facts if any of these occur:

- Changed files are outside the approved task scope.
- A forbidden path is changed or selected.
- A secret-like value appears in a diff.
- `動画保存ツール_ローカル専用/` exists in the repository root.
- PR #1001 file leakage is detected.
- The diff adds update execution behavior.
- The diff adds dangerous local-only boundary violations.
- LLMwiki documents contradict the approved scope.
- The checker cannot prove repository root, base ref, or changed files safely.

## Y-CHECK-01 Outcome

Y-CHECK-01 is complete. Y-CHECK-02 adds the first report-only implementation at
`scripts/check_repo_safety.py`.

Not implemented:

- automation gate implementation
- CI integration
- PR bot/comment automation
- package generation
- generated distribution folder
- backend/frontend/Docker/CI/package/lockfile changes
- update execution
- cookie/token/secret handling
