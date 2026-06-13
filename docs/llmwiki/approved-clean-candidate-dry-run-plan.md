# Approved Clean Candidate Dry-Run Plan

## Purpose

Y-DIST-06 defines the approved clean candidate dry-run plan for a future
explicitly approved CLEAN portable distribution candidate for
`youtubeダウンロード / MeTube local-only fork`.

This document is docs-only. It does not approve or perform artifact generation.
It records how a future dry-run should be planned, where it must stop, and what
must be recorded after a separate human approval exists.

## Facts / Assumptions / Needs Verification

Facts:

- Y-DIST-01 provides the CLEAN candidate forbidden-file, secret-like content,
  and manifest baseline checker.
- Y-DIST-02 provides the version, manifest, checksum, license, notice, and
  checksum consistency checker.
- Y-DIST-03 provides the recipient-safe runbook and first-run local-only
  verification procedure.
- Y-DIST-04 provides the advisory distribution readiness matrix.
- Y-DIST-05 provides the human approval checklist before artifact generation.
- Y-DIST-07 provides the approval packet for the future human decision record.
- No approval record is included in this document.

Assumptions:

- A future approval record will name one exact source commit.
- A future approval record will name one exact candidate path and output path.
- A future approval record will name the exact allowed artifact scope.

Needs verification before any future dry-run execution:

- The future approval record exists and satisfies Y-DIST-05.
- The local `fork/master` source commit matches the approved source commit.
- The candidate and output paths exactly match the approved paths.
- No stop condition in this document is present.

## Dry-Run Principle

- Dry-run plan is not artifact generation.
- Dry-run plan does not create a CLEAN folder.
- Dry-run plan does not create ZIP / installer / package output.
- Dry-run plan does not generate metadata.
- Dry-run plan does not generate checksums.
- Dry-run plan does not perform real downloads.
- Dry-run plan only defines what would be checked after a future explicit
  approval.

## Required Prerequisites Before Actual Dry-Run Execution

Before any actual future dry-run execution begins, confirm and record:

- Y-DIST-05 approval record exists.
- Approval names exact `source_commit`.
- Approval names exact candidate/output path.
- Approval names allowed artifact scope.
- Approval names explicitly forbidden operations.
- Y-DIST-07 approval packet reviewed.
- `fork/master` matches approved `source_commit`.
- Working tree / worktree isolation confirmed.
- `local-fork-safety` clean on preceding PR.
- PR #1001 files absent:
  - `docker-compose.local.yml`
  - `docs/local-only.md`
- `動画保存ツール_ローカル専用/` absent before approved generation.
- No credential-bearing material.
- No dependency install/update required.
- No Docker pull/build required.
- No public hosting or non-loopback exposure.

Passing these prerequisites does not expand the approved artifact scope.

## Planned Dry-Run Phases

Phase A: approval record review

- Confirm the approval record exists and satisfies Y-DIST-05.
- Confirm the approval is still valid, scoped, and not expired or reused beyond
  its rule.

Phase B: source commit / worktree isolation review

- Confirm `fork/master` matches the approved `source_commit`.
- Confirm the worktree or workspace is isolated from unrelated local state.
- Confirm the working tree does not already contain generated output.

Phase C: candidate path preflight

- Confirm the candidate path is explicit.
- Confirm the candidate path exactly matches the approval record.
- Confirm the path is not existing user downloads, state, or logs.

Phase D: forbidden-file / secret-like content dry-run review

- Plan Y-DIST-01 checker execution against the exact approved candidate path.
- Treat candidate checker execution as `not_applicable_yet` until the approved
  candidate exists.
- Stop before any cookie, token, secret, or credential handling.

Phase E: metadata/checksum plan review

- Plan Y-DIST-02 checker execution against the exact approved candidate path.
- Treat metadata/checksum checker execution as `not_applicable_yet` until the
  approved candidate exists.
- Do not create metadata or checksums during the dry-run plan.

Phase F: recipient runbook / first-run checklist review

- Review the Y-DIST-03 recipient-safe runbook.
- Review the Y-DIST-03 first-run local-only verification checklist.
- Do not launch the app, perform a real download, or confirm handoff unless the
  approval explicitly allows that separate scope.

Phase G: stop-condition review

- Compare the observed state against this document's stop conditions.
- Stop if any stop condition is present or if the approval scope is ambiguous.

Phase H: final human go/no-go summary

- Record the dry-run report template.
- Summarize prerequisites, planned checker status, observed stop conditions, and
  the next required human decision.
- Do not treat a go summary as generation approval.

## Candidate Path Rules

- Candidate path must be explicit.
- Candidate path must not be inferred from repo root.
- Candidate path must not be existing user downloads/state/logs.
- Candidate path must not contain cookies/tokens/secrets.
- Candidate path must not be `動画保存ツール_ローカル専用/` unless separately
  approved.
- Candidate path must be inside an approved dry-run/output area only if
  approved.

If the candidate path is missing, inferred, ambiguous, or outside the approved
scope, the dry-run must stop.

## Planned Checker Usage

Use these checkers only after a future explicit approval names the exact
candidate or baseline scope:

| checker | planned future use | current Y-DIST-06 status |
| --- | --- | --- |
| `scripts/check_clean_distribution.py <candidate_dir>` | Run against the exact approved candidate path. | `not_applicable_yet` because no candidate exists. |
| `scripts/check_distribution_metadata.py <candidate_dir>` | Run against the exact approved candidate path after metadata exists under an approved scope. | `not_applicable_yet` because no candidate exists. |
| `scripts/check_repo_safety.py` | Review repository safety for the current branch. | Local docs-only PR gate. |
| `scripts/check_repo_safety.py --base fork/master` | Review repository safety against the fork baseline. | Local docs-only PR gate. |
| `scripts/check_safety_wording.py --base fork/master` | Review docs wording against the fork baseline. | Local docs-only PR gate. |

This PR must not execute the candidate-directory checkers against a candidate.
Candidate execution is `not_applicable_yet`.

## Dry-Run Report Template

Use this template for future approved dry-run records:

```text
Dry-run ID:
Approval ID:
Operator:
Date:
Source commit:
Approved artifact scope:
Approved candidate path:
Approved output path:
Candidate exists before approved generation:
Generated artifacts created during this dry-run:
Real download performed:
Dependency install/update performed:
Container image operations performed:
PR #1001 files present:
Y-DIST-01 checker result:
Y-DIST-02 checker result:
Recipient runbook reviewed:
First-run checklist reviewed:
Stop conditions observed:
Result:
Next required action:
```

The `Container image operations performed` field covers Docker operations. It
must remain `no`; no container image operation may be performed by this
dry-run.

## Stop Conditions

Stop the dry-run plan or future dry-run execution if any condition below
appears:

- Approval record missing.
- Source commit mismatch.
- Candidate/output path mismatch.
- Artifact scope mismatch.
- Candidate path inferred rather than explicit.
- Generated folder appears before approval.
- ZIP / installer / package output appears before approval.
- Metadata/checksum generation appears before approval.
- Real download becomes necessary.
- Dependency install/update becomes necessary.
- No Docker pull/build may be required; stop if Docker pull/build becomes
  necessary.
- Cookie/token/secret/credential handling becomes necessary.
- DRM/auth/restriction bypass becomes necessary.
- Public hosting or non-loopback exposure appears.
- PR #1001 files appear.
- `local-fork-safety` fails unexpectedly.
- Y-DIST-01 checker fails.
- Y-DIST-02 checker fails.
- License/notice human review unresolved.

When a stop condition appears, record the observed condition and request a new
human decision. Do not continue under an ambiguous or mismatched approval.

## Relation To Previous Y-DIST Lanes

Y-DIST-01:

- CLEAN candidate forbidden-file / secret-like content / manifest baseline
  checker.

Y-DIST-02:

- VERSION / MANIFEST / checksums.sha256 / LICENSE / NOTICE / checksum
  consistency checker.

Y-DIST-03:

- Recipient-safe runbook and first-run local-only verification.

Y-DIST-04:

- Advisory readiness matrix.

Y-DIST-05:

- Human approval checklist before artifact generation.

Y-DIST-06:

- Approved clean candidate dry-run plan.

Y-DIST-07:

- Artifact generation approval packet for the future human decision.

## Explicit Non-Goals

- No CLEAN folder generation.
- No ZIP / installer / package output.
- No metadata generation.
- No checksum generation.
- No real download.
- No dependency install/update.
- No Docker pull/build.
- No backend/frontend runtime change.
- No yt-dlp extractor or download queue change.
- No public hosting.
- No cookie/token/secret handling.
- No PR #1001 files.
