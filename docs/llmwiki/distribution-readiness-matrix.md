# Distribution Readiness Matrix

## Purpose

Y-DIST-04 defines an advisory readiness matrix for a future CLEAN portable
distribution of `youtubeダウンロード / MeTube local-only fork`.

This document lists current readiness, unresolved items, human review gates, and
stop conditions. It does not approve artifact generation.

## Status Categories

| status | meaning |
| --- | --- |
| `ready` | The condition is satisfied for the current repository state. |
| `blocked` | The condition is unmet, or cannot proceed without separate explicit approval. |
| `human_review_required` | Machine checks are not sufficient; a human must review the item. |
| `not_started` | The work has not been performed. |
| `not_applicable_yet` | The item does not apply until an actual approved candidate exists. |
| `warning_only` | The item is not a blocker, but it should remain visible. |

## Advisory-Only Rules

- Matrix success is advisory only.
- Matrix success does not approve artifact generation.
- Matrix success does not approve CLEAN folder creation.
- Matrix success does not approve ZIP / installer / package output.
- Matrix success does not approve metadata/checksum generation.
- Matrix success does not approve real download verification.
- Actual generation requires a separate explicit human approval task.

## A. Project Scope / Legal Safety

| item | current_status | evidence_or_source | required_before_distribution | blocker_if_failed | next_action |
| --- | --- | --- | --- | --- | --- |
| Local-only personal-use scope | `ready` | `docs/llmwiki/safety-boundaries.md` | yes | yes | Keep recipient and package wording local-only. |
| Public hosting exclusion | `ready` | Safety boundaries and recipient runbook prohibit public exposure operations. | yes | yes | Continue blocking hosted, tunnel, LAN service, and external-user service assumptions. |
| DRM/auth/restriction bypass exclusion | `ready` | `docs/llmwiki/recipient-safe-runbook.md` stop conditions | yes | yes | Stop if bypass becomes necessary. |
| Cookie/token/secret/credential exclusion | `ready` | Safety boundaries, Y-SEC-03 privacy guidance, recipient runbook | yes | yes | Stop if credential-bearing file handling becomes necessary. |
| License / notice legal sufficiency | `human_review_required` | Y-DIST-02 checks presence and safety only. | yes | yes | Human legal/compliance review before handoff. |

## B. Local-Only Runtime Boundary

| item | current_status | evidence_or_source | required_before_distribution | blocker_if_failed | next_action |
| --- | --- | --- | --- | --- | --- |
| Default local-only mode | `ready` | Y-SEC-01 / `LOCAL_ONLY_MODE=true` default | yes | yes | Reconfirm during first-run verification. |
| Loopback bind default | `ready` | Y-SEC-01A / `HOST=127.0.0.1` default | yes | yes | Reconfirm actual candidate launch. |
| Non-loopback bind rejection | `ready` | Y-SEC-01A runtime guard | yes | yes | Stop if actual launch listens on `0.0.0.0`, LAN IP, or public IP. |
| Public host URL boundary | `ready` | Y-SEC-01 blocks non-local absolute public host URL values in local-only mode. | yes | yes | Keep future launchers from setting public host values. |

## C. Runtime Security Guardrails

| item | current_status | evidence_or_source | required_before_distribution | blocker_if_failed | next_action |
| --- | --- | --- | --- | --- | --- |
| Host guard | `ready` | Y-SEC-01 local Host allowlist | yes | yes | Reconfirm in first-run local-only verification. |
| Origin / Referer guard | `ready` | Y-SEC-01C and state-changing request guard | yes | yes | Reconfirm no external-origin behavior is introduced. |
| Wildcard CORS block | `ready` | Y-SEC-01 local-only CORS guard | yes | yes | Keep wildcard CORS disabled. |
| Unsafe yt-dlp option override block | `ready` | Y-SEC-01 unsafe override guard | yes | yes | Keep unsafe escape hatch disabled for recipients. |
| Nightly automatic yt-dlp update block | `ready` | Y-SEC-01 unsafe nightly update guard | yes | yes | Keep automatic update application operations disabled. |
| URL intake SSRF/private target guard | `ready` | Y-SEC-02 URL intake guard | yes | yes | Preserve known limits in docs. |
| Log and filename privacy hardening | `ready` | Y-SEC-03 privacy redaction / filename sanitization | yes | yes | Keep logs and filenames free of secret-like material. |

## D. CLEAN Candidate File Hygiene

| item | current_status | evidence_or_source | required_before_distribution | blocker_if_failed | next_action |
| --- | --- | --- | --- | --- | --- |
| Y-DIST-01 checker | `ready` | `scripts/check_clean_distribution.py` | yes | yes | Run against the exact approved candidate directory. |
| Forbidden-file rules | `ready` | `docs/llmwiki/clean-portable-distribution-manifest.md` | yes | yes | Keep `.git`, logs, state, downloads, caches, and sensitive filenames out. |
| Secret-like content reporting | `ready` | Y-DIST-01 checker reports pattern families only. | yes | yes | Keep reports sanitized. |
| Actual CLEAN candidate exists | `blocked` | No approved generation task yet; no candidate generated. | yes | yes | Separate explicit generation approval required. |
| Generated package folder absence | `ready` | Local and CI safety gates check `動画保存ツール_ローカル専用/` absence. | yes | yes | Stop if it appears without approval. |

## E. Metadata / Checksum / Version / License Notice

| item | current_status | evidence_or_source | required_before_distribution | blocker_if_failed | next_action |
| --- | --- | --- | --- | --- | --- |
| Y-DIST-02 metadata checker | `ready` | `scripts/check_distribution_metadata.py` | yes | yes | Run against the exact approved candidate directory. |
| Required metadata contract | `ready` | `VERSION.txt`, `MANIFEST.json`, `checksums.sha256`, `LICENSE`, `NOTICE` contract | yes | yes | Apply only after candidate generation is approved. |
| Metadata generation | `blocked` | Not generated; no approval task exists. | yes | yes | Separate explicit metadata generation approval required. |
| Checksum generation | `blocked` | Not generated; no approval task exists. | yes | yes | Separate explicit checksum generation approval required. |
| License / notice content completeness | `human_review_required` | Checker validates presence and safety, not legal sufficiency. | yes | yes | Human review before distribution. |

## F. Recipient-Safe Runbook

| item | current_status | evidence_or_source | required_before_distribution | blocker_if_failed | next_action |
| --- | --- | --- | --- | --- | --- |
| Y-DIST-03 recipient runbook | `ready` | `docs/llmwiki/recipient-safe-runbook.md` | yes | yes | Use as the recipient-facing safety source. |
| Local-only recipient instructions | `ready` | Runbook recipient safety rules | yes | yes | Keep all future package guide copy aligned. |
| Recipient stop conditions | `ready` | Runbook stop conditions | yes | yes | Stop if any condition is observed. |
| Save folder / stop path explanation | `ready` | Runbook before-launch and stop/quit sections | yes | yes | Reconfirm future package guide includes this. |

## G. First-Run Local-Only Verification

| item | current_status | evidence_or_source | required_before_distribution | blocker_if_failed | next_action |
| --- | --- | --- | --- | --- | --- |
| Y-DIST-03 first-run checklist | `ready` | `docs/llmwiki/first-run-local-only-verification.md` | yes | yes | Use as the first-run verification source. |
| First-run verification on actual candidate | `not_applicable_yet` | No approved candidate exists. | yes | yes | Perform only after explicit candidate generation approval. |
| Real download verification | `blocked` | Not approved for this distribution-readiness lane. | no unless separately approved | yes if required without approval | Separate explicit approval required before any real download. |
| Logs/state/downloads secret hygiene check | `not_applicable_yet` | Requires an actual approved candidate and first-run environment. | yes | yes | Complete during first-run verification. |

## H. CI / Local Safety Gates

| item | current_status | evidence_or_source | required_before_distribution | blocker_if_failed | next_action |
| --- | --- | --- | --- | --- | --- |
| `local-fork-safety` PR visibility | `ready` | PR #90 and PR #91 docs-only checks succeeded. | yes | yes | Keep checking every distribution-planning PR. |
| Repository safety checker | `ready` | `scripts/check_repo_safety.py` | yes | yes | Run locally and in CI context where applicable. |
| Safety wording checker | `ready` | `scripts/check_safety_wording.py` | yes | no if warning-only | Review warnings without treating warning-only output as approval. |
| Generated package folder absence gate | `ready` | Local safety gates and CI workflow | yes | yes | Stop if folder appears without approval. |
| PR #1001 leakage gate | `ready` | Local safety gates and CI workflow | yes | yes | Keep `docker-compose.local.yml` and `docs/local-only.md` out. |
| Branch protection / required checks | `not_started` | No branch protection mutation has been approved. | human decision | no for docs-only planning | Consider Y-GH-01 separately. |
| CODEOWNERS | `not_started` | No CODEOWNERS addition has been approved. | human decision | no for docs-only planning | Keep separate from distribution readiness. |

## I. Artifact Generation Approval

| item | current_status | evidence_or_source | required_before_distribution | blocker_if_failed | next_action |
| --- | --- | --- | --- | --- | --- |
| Explicit artifact-generation approval | `blocked` | No generation approval task exists. | yes | yes | Y-DIST-05 should define the approval checklist. |
| CLEAN folder creation | `blocked` | Not generated; explicitly prohibited in this lane. | yes | yes | Separate explicit approval required. |
| ZIP / installer / package output | `blocked` | Not generated; explicitly prohibited in this lane. | yes | yes | Separate explicit approval required. |
| Metadata/checksum generation | `blocked` | Not generated; explicitly prohibited in this lane. | yes | yes | Separate explicit approval required. |
| Distribution upload/share | `blocked` | No candidate, no approval, no human review completion. | yes | yes | Do not share until all gates pass. |

## J. Human Review / Merge Gate

| item | current_status | evidence_or_source | required_before_distribution | blocker_if_failed | next_action |
| --- | --- | --- | --- | --- | --- |
| Human review before artifact generation | `human_review_required` | Safety boundaries require separate explicit approval. | yes | yes | Add Y-DIST-05 checklist before any generation lane. |
| Human review before distribution handoff | `human_review_required` | Y-DIST-03 runbook / first-run verification require review. | yes | yes | Record reviewer, candidate path, and checklist result. |
| Human review for license / notice sufficiency | `human_review_required` | Y-DIST-02 known limit | yes | yes | Legal/compliance review before handoff. |
| Merge gate for docs-only planning PRs | `ready` | `local-fork-safety` PR visibility is active. | yes | yes if checks fail | Keep expected-head and check-state review before merge. |

## K. Known Local Environment Issues

| item | current_status | evidence_or_source | required_before_distribution | blocker_if_failed | next_action |
| --- | --- | --- | --- | --- | --- |
| Untracked `webgpt_handoff_context/` | `warning_only` | Local-only untracked helper context observed in Codex workspace. | no | no | Keep it out of commits and PRs. |
| Sandboxed `gh auth status` keyring issue | `warning_only` | Project GitHub CLI auth note / recent operations | no | no if escalated narrow `gh` works | Use narrow escalated `gh` commands only when needed. |
| `.pytest_cache/` read warning | `warning_only` | Local git status can warn about permission denied. | no | no | Do not inspect generated cache folders. |
| PATH `python` missing in Codex shell | `warning_only` | Use bundled Codex Python for local scripts. | no | no | Continue using bundled Python path for verification. |

## L. Next Required Actions

| item | current_status | evidence_or_source | required_before_distribution | blocker_if_failed | next_action |
| --- | --- | --- | --- | --- | --- |
| Y-DIST-05 human approval checklist before artifact generation | `not_started` | Recommended next candidate after this matrix. | yes | yes | Define the exact approval checklist before any generation task. |
| Y-DIST-06 approved clean candidate dry-run plan | `not_started` | Candidate after Y-DIST-05. | yes | yes | Keep dry-run plan separate from real output generation. |
| Y-CI-03 reusable workflow | `not_started` | CI follow-up candidate. | no for distribution docs | no | Consider after distribution approval checklist. |
| Y-CI-04 concurrency / cancel-in-progress | `not_started` | CI follow-up candidate. | no for distribution docs | no | Consider after or alongside Y-CI-03. |
| Y-GH-01 branch protection design | `not_started` | Governance follow-up candidate. | human decision | no for docs-only planning | Keep design-only unless explicitly approved. |
| Y-WIKI-CLEAN-01 current-state / handoff / archive整理 | `not_started` | Documentation maintenance candidate. | no | no | Use after current distribution lane settles. |

Recommended next step after Y-DIST-04:

```text
Y-DIST-05 human approval checklist before any artifact generation
```

Rationale: Y-DIST-01, Y-DIST-02, and Y-DIST-03 define the checker and recipient
procedure baselines. Before any real output exists, the next safest step is a
human approval checklist that states who may approve generation, what exact
artifact scope is approved, which candidate path is allowed, and which stop
conditions still apply.

## Stop Conditions

Distribution readiness must stop if any of these appear:

- External/public hosting appears.
- Non-loopback bind or public URL appears.
- DRM/auth/restriction bypass is needed.
- Cookie/token/secret/credential handling is needed.
- PR #1001 files appear.
- A generated package folder appears without approval.
- ZIP / installer / package output appears without approval.
- Metadata/checksum generation appears without approval.
- Dependency installation operations or container image operations become
  required.
- `local-fork-safety` fails unexpectedly.
- Y-DIST-01 checker fails.
- Y-DIST-02 checker fails.
- Recipient first-run verification fails.

## Explicit Non-Goals

- No CLEAN folder generation.
- No ZIP / installer / package output.
- No metadata generation.
- No checksum generation.
- No real download.
- No dependency install/update operations.
- No Docker pull/build operations.
- No frontend build/test.
- No backend pytest.
- No backend/frontend/Docker/package/lockfile changes.
- No `.github/workflows/` changes.
- No branch protection changes.
- No required-check setting changes.
- No CODEOWNERS addition.
- No `.gitignore` changes.
- No cookie/token/secret/credential handling.
- No PR #1001 files.
