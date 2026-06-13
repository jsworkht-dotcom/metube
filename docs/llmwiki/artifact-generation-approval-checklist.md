# Artifact Generation Approval Checklist

## Purpose

Y-DIST-05 defines the human approval checklist required before any future CLEAN
portable distribution artifact generation for
`youtubeダウンロード / MeTube local-only fork`.

This document is docs-only. It does not approve or perform artifact generation.
It does not create a CLEAN folder, metadata files, checksums, ZIP output,
installer output, package output, or real download verification.

## Facts / Assumptions / Needs Verification

Facts:

- Y-DIST-01 provides the CLEAN candidate forbidden-file, secret-like content,
  and manifest baseline checker.
- Y-DIST-02 provides the version, manifest, checksum, license, notice, and
  checksum consistency checker.
- Y-DIST-03 provides the recipient-safe runbook and first-run local-only
  verification procedure.
- Y-DIST-04 provides the advisory distribution readiness matrix.
- Y-DIST-06 provides the approved clean candidate dry-run plan for use after a
  separate explicit approval exists.
- Y-DIST-07 provides the artifact generation approval packet for the later
  human decision record; it does not approve generation.
- All approval categories in this checklist are currently `not approved`.

Assumptions:

- A future artifact-generation request will name one exact source commit and
  one exact candidate or output path.
- Future approvals may approve only a subset of artifact types.
- Any artifact type not named in a future approval remains forbidden.

Needs verification before any future generation:

- The current fork `master` source commit matches the approved source commit.
- The exact output path matches the approved path.
- Required local and GitHub safety checks are clean.
- No stop condition in this checklist is present.

## Approval Principle

Artifact generation is blocked by default.
No artifact may be generated without separate explicit human approval.
Approval must name the exact allowed artifact scope.
Approval must name the exact candidate path or output path.
Approval must name the source commit.
Approval must list what remains forbidden.

Passing advisory docs, local checks, or GitHub checks does not approve artifact
generation. Approval must be explicit, separate, and scoped to the specific
artifact operation.

## Approval Categories

| category | approval target | current status |
| --- | --- | --- |
| A | CLEAN folder generation approval | `not approved` |
| B | metadata file generation approval | `not approved` |
| C | checksum generation approval | `not approved` |
| D | ZIP output approval | `not approved` |
| E | installer output approval | `not approved` |
| F | first-run verification approval | `not approved` |
| G | real download verification approval | `not approved` |
| H | recipient handoff / sharing approval | `not approved` |

Each category must be approved separately or explicitly included in a single
record that names the exact allowed artifact scope. A broad statement such as
"continue distribution work" is not enough.

## Required Approval Fields

Every approval record must include:

| field | required meaning |
| --- | --- |
| `approval_id` | Stable identifier for this approval record. |
| `approver` | Human approver name or handle. |
| `approval_date` | Approval date. |
| `source_commit` | Exact source commit allowed for the operation. |
| `allowed_output_path` | Exact output or candidate path allowed. |
| `allowed_artifact_types` | Exact artifact categories allowed. |
| `explicitly_not_allowed` | Artifact types and operations still forbidden. |
| `required_checkers` | Machine checks required before or after generation. |
| `required_manual_reviews` | Human reviews required before handoff or sharing. |
| `stop_conditions` | Conditions that void the approval or stop generation. |
| `expiry_or_single-use_rule` | Expiry date, single-use limit, or reuse boundary. |

If any required field is missing, generation remains blocked.

## Required Pre-Generation Checks

Before any approved future artifact generation begins, confirm and record:

- `fork/master` expected commit confirmed.
- Working tree / worktree isolation confirmed.
- PR #1001 files absent:
  - `docker-compose.local.yml`
  - `docs/local-only.md`
- `動画保存ツール_ローカル専用/` absent before approved generation.
- No cookie/token/secret/credential material.
- No dependency install/update requirement.
- No Docker image operation requirement.
- No image pull or image build requirement.
- No public hosting / external service mode.
- `local-fork-safety` status clean on preceding PR.
- Y-DIST-04 readiness matrix reviewed.

These checks are preconditions only. Passing them does not expand the approved
artifact scope.

## Required Post-Generation Checks

After any future approved generation, confirm and record:

- Y-DIST-01 checker pass on exact candidate.
- Y-DIST-02 metadata checker pass on exact candidate.
- Y-DIST-03 recipient runbook reviewed.
- Y-DIST-03 first-run verification reviewed or scheduled.
- Generated files match approved scope only.
- No forbidden files.
- No secret-like content values exposed.
- Metadata/checksum files match candidate contents.
- License/notice human review completed.

If any required post-generation check fails, the candidate must not be shared,
handed off, uploaded, or treated as distribution-ready.

## Stop Conditions

Approval is invalid, and generation must stop, if any condition below appears:

- Source commit changed from approved value.
- Output path differs from approved path.
- Requested artifact type differs from approved scope.
- PR #1001 files appear:
  - `docker-compose.local.yml`
  - `docs/local-only.md`
- Generated package folder appears before approval.
- ZIP / installer / package output appears before approval.
- Metadata/checksum generation appears before approval.
- Cookie/token/secret/credential handling becomes necessary.
- DRM/auth/restriction bypass becomes necessary.
- Public hosting or non-loopback exposure appears.
- Dependency install/update becomes necessary.
- Docker image operation becomes necessary.
- Image pull or image build becomes necessary.
- `local-fork-safety` fails unexpectedly.
- Y-DIST-01 checker fails.
- Y-DIST-02 checker fails.
- License/notice review fails or remains unresolved.

When a stop condition appears, do not continue under the same approval record.
Record the observed condition and request a new human decision after the issue
is resolved.

## Approval Record Template

Use this template for future approvals:

```text
Approval ID:
Approver:
Approval date:
Source commit:
Approved artifact scope:
Approved output path:
Approved candidate path:
Allowed commands / scripts:
Explicitly forbidden operations:
Required pre-generation checks:
Required post-generation checks:
Required manual reviews:
Single-use or reusable:
Expires:
Result:
```

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

- Approved clean candidate dry-run plan after explicit approval.
- Does not approve artifact generation by itself.

Y-DIST-07:

- Artifact generation approval packet.
- Does not approve artifact generation by itself.

## Explicit Non-Goals

- No CLEAN folder generation.
- No ZIP / installer / package output.
- No metadata generation.
- No checksum generation.
- No real download.
- No dependency install/update.
- No Docker image operation.
- No image pull or image build.
- No backend/frontend runtime change.
- No yt-dlp extractor or download queue change.
- No public hosting.
- No cookie/token/secret handling.
- No PR #1001 files.
