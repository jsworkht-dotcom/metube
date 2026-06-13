# Beginner UX Next-Action Plan

## Purpose

Y-UX-PLAN-01 defines the next safe beginner UX planning lane after the
artifact-generation decision was placed on hold.

This is docs-only planning. It does not change frontend code, backend code,
runtime behavior, package generation, distribution output, or GitHub settings.

## Y-DIST-08 Result

Y-DIST-08 result:

- artifact generation remains HOLD;
- all artifact categories remain not approved;
- the next safe path is low-risk UX/docs/report/checker planning.

Artifact generation, ZIP/package/installer output, CLEAN folder creation,
metadata generation, checksum generation, real download verification, and
recipient handoff remain blocked until a later explicit human-reviewed lane
approves them.

## Current UX Baseline

- Japanese-localized UI exists.
- Local-only safety posture exists.
- Beginner guide source docs exist.
- Package generation remains blocked.

Current source references:

- `docs/llmwiki/current-ui-manual-review-checklist.md`
- `docs/llmwiki/current-ui-screenshot-review-findings.md`
- `docs/llmwiki/beginner-guide-skeleton.md`
- `docs/llmwiki/beginner-guide-source-plan.md`
- `docs/llmwiki/package-guides/00-first-open.html.source.md`
- `docs/llmwiki/package-guides/03-how-to-use.html.source.md`
- `docs/llmwiki/package-guides/04-troubleshooting.html.source.md`
- `docs/llmwiki/package-guides/05-safe-use.html.source.md`

## UX Principles

- local-only first;
- personal-use only;
- no public hosting;
- no credential/cookie/token guidance;
- no DRM/auth/restriction bypass language;
- beginner-friendly wording;
- stop/quit clarity;
- save-folder clarity;
- error next-action clarity.

Beginner-facing work should keep Japanese wording short, concrete, and
action-oriented. It should favor "what to do next" over technical explanation
and should preserve the existing local-only safety posture.

## Next UX Candidates

- `Y-UI-QUALITY-01 quality selector / label review`
- `Y-UX-COPY-01 safe-use microcopy review`
- `Y-UX-HELP-01 help/troubleshooting entry review`
- `Y-UX-STATE-01 status / progress / completion clarity review`
- `Y-UX-STOP-01 stop/quit user-flow design`

Repo-history note: earlier `Y-UI-QUALITY-01`, `Y-UI-QUALITY-02`, and
`Y-UI-QUALITY-03` lanes are already complete. If a new implementation PR starts
from the quality selector / label review candidate, use a non-colliding follow-up
lane name while keeping the candidate intent.

## Recommended First Next Lane

Recommended first next lane:

- `Y-UI-QUALITY-01` or `Y-UX-COPY-01`.

Repo-history note: because historical `Y-UI-QUALITY-01` is already complete in
this fork, prefer a fresh quality selector / label review follow-up lane name
if implementation starts. Use `Y-UX-COPY-01 safe-use microcopy review` when the
next PR should remain docs-only or copy-planning only.

Prefer the quality selector / label review path only if the next task explicitly
scopes UI files and accepts the human-reviewed frontend lane.

## Risk Boundaries

Docs-only UX planning:

- allowed via fast safe flow;
- may update LLMwiki planning, roadmap, and handoff docs;
- must not generate artifacts or change runtime behavior.

Frontend copy-only implementation:

- later separate lane;
- requires UI files explicitly scoped;
- no package/build/dependency changes.

Runtime behavior changes:

- later separate lane;
- not part of Y-UX-PLAN-01.

## Explicitly Not Performed

Y-UX-PLAN-01 does not perform:

- frontend code changes;
- backend code changes;
- runtime behavior changes;
- artifact generation;
- `動画保存ツール_ローカル専用/` creation;
- generated package output;
- metadata generation;
- checksum generation;
- real download verification;
- recipient handoff or sharing;
- dependency installation operations;
- container image operations;
- `.github/workflows/` changes;
- GitHub settings, branch protection, ruleset, required-check, or CODEOWNERS
  mutation;
- `.gitignore` changes;
- cookie/token/secret/credential handling;
- public exposure operations or non-loopback exposure;
- DRM/auth/restriction bypass guidance.

## Handoff Sync

PR #105 completed Y-DIST-08 no-generation hold. Y-UX-PLAN-01 establishes the
next UX planning path after that hold:

- artifact generation remains blocked;
- fast safe flow is the default for low-risk docs/report/checker lanes;
- beginner UX work should start with safe planning before any UI implementation;
- future UI copy-only work remains a separate human-reviewed lane unless later
  safety-gate policy explicitly changes.
