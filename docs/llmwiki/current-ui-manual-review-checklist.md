# Current UI Manual Review Checklist

## Purpose

This checklist prepares a manual UI review for the local-only MeTube UI after
the first frontend copy-only implementation.

The review focus is the add/download form, video and audio quality selectors,
quality helper popovers, captions controls, queue/result areas, help entry
labels, and stop/quit-related wording. This is a review-preparation document
only; it does not change UI behavior, backend behavior, download behavior, or
local-only policy.

## Review Status

```text
status: y-fe-review-02-evidence-recorded-review-not-executed
```

Y-FE-REVIEW-01 refreshes this checklist after PR #114 / Y-FE-COPY-02 and PR
#115 / Y-FE-COPY-03. It does not perform the manual review; it defines what a
reviewer should inspect before any second frontend copy pass or behavior-level
UI work.

Y-FE-COPY-02 completed the current visible copy baseline:

- quality / audio helper text softened;
- scoped Auto / 自動 display changed to おまかせ;
- subtitle mode labels changed to Japanese;
- result-table auto codec display localized;
- no selector id/value changes;
- no behavior changes.

Y-UI-REVIEW-02 attempted review and captured temporary static screenshots for
the initial add form, the video quality helper popover, and a narrow-width
layout. The preview remained at `サーバーに接続中...`, so selector-open states,
audio-mode visuals, and completed/result rows were not visually reviewed. This
document does not assert a full visual pass/fail.

Y-UI-REVIEW-02R reran the review with a temporary local mock server and safe
synthetic data. The rerun captured the loaded form, video and audio helper
popovers, audio mode, completed/result rows for video/audio/captions/thumbnail,
and a narrow-width loaded layout. Native OS select dropdown panels were not
visible in screenshots after selector clicks, so those open-state screenshots
remain unchecked; selector labels were verified through browser DOM evidence.

## Y-FE-REVIEW-01 Manual Review Targets

- URL input area
- Save / subscription buttons
- Advanced settings panel
- Quality / format / codec controls
- Captions controls
- Queue / saving area
- Completed / failed result table
- Help / troubleshooting entry labels
- Stop / quit related wording

## Y-FE-REVIEW-01 Review Questions

Beginner clarity:

- Does the main save flow still read naturally?
- Is `おまかせ` understandable in each context?
- Are quality/audio labels short and clear?
- Are captions labels understandable without technical knowledge?
- Is completed/failed status wording clear?
- Is the next safe action visible or inferable?

Safety:

- Does any wording imply guaranteed success?
- Does any wording imply unrestricted saving?
- Does any wording invite cookie/token/secret handling?
- Does any wording imply public hosting or sharing?
- Does any wording suggest DRM/auth/restriction bypass?
- Does any wording encourage mass download optimization?

Layout:

- Do Japanese labels fit narrow screens?
- Do buttons wrap awkwardly?
- Do table columns remain readable?
- Do helper popovers remain concise?
- Are advanced labels too noisy for beginners?

## Y-FE-REVIEW-01 Evidence Template

```text
Manual UI review evidence:
  reviewer:
  date:
  browser / OS:
  viewport:
  commit:
  reviewed screens:
  findings:
  blockers:
  follow-up candidate:
```

## Y-FE-REVIEW-01 Next Decision Point

Option A:

```text
Y-FE-COPY-04 second frontend copy-only pass packet docs-only
Use if review finds more wording adjustments.
```

Option B:

```text
Y-FE-COPY-04 second frontend copy-only implementation
Only after explicit scope approval.
```

Option C:

```text
Stop frontend copy work and return to docs/report/checker lane.
```

Recommended:

```text
Run manual UI review outside this PR, then choose Y-FE-COPY-04 packet only if findings exist.
```

## Y-FE-REVIEW-02 Manual UI Review Evidence

Review baseline:

- PR #114 completed the first frontend copy-only implementation.
- PR #115 closed out the implementation.
- PR #116 refreshed the manual UI review checklist.
- Artifact generation remains HOLD.

Manual UI review evidence:

```text
reviewer: Codex
date: 2026-06-13
commit: 33673fa43066ec777c5574068a2fadee935ed04a
browser / OS: not reviewed / Windows Codex desktop
viewport: not reviewed
UI available without build/install/runtime setup: no
reviewed screens: none
findings: all targets not_reviewed
blockers: none in source; review was not executed in this lane
follow-up candidate: separate scoped local UI review lane, no source changes
```

Manual UI review:

```text
not executed in this lane
```

Reason:

```text
UI runtime was not already available without additional setup
```

Next action:

```text
request separate scoped manual review / runtime review lane
```

Findings classification:

- URL input area: `not_reviewed`
- Save / subscription buttons: `not_reviewed`
- Advanced settings panel: `not_reviewed`
- Quality / format / codec controls: `not_reviewed`
- Captions controls: `not_reviewed`
- Queue / saving area: `not_reviewed`
- Completed / failed result table: `not_reviewed`
- Help / troubleshooting entry labels: `not_reviewed`
- Stop / quit related wording: `not_reviewed`

Decision:

```text
next recommended lane = separate scoped local UI review lane, no source changes
```

## Y-FE-LOCAL-REVIEW-01 Scoped Local Review Packet

Y-FE-LOCAL-REVIEW-01 adds the scoped local UI review runbook / approval packet:

```text
docs/llmwiki/local-ui-review-runbook.md
```

This packet is docs-only. It does not execute the manual UI review, start the
app, build frontend assets, install dependencies, run the backend, perform a
download, change source files, create artifacts, or expose anything beyond
loopback.

Future lane:

```text
Y-FE-LOCAL-REVIEW-02 scoped local UI review execution
```

Y-FE-LOCAL-REVIEW-02 may only run after explicit approval. It may start or use
the local-only UI only if existing dependencies are already present, and it
must stop and record `not executed` if review would require install, build,
Docker, package generation, real URL submission, or real download work.

## Y-FE-LOCAL-REVIEW-02 Local UI Review Evidence

Local UI review evidence:

```text
reviewer: Codex
date: 2026-06-13
commit: 6ca2e87d5f124b64742d407f016717ec39a90538
commands run:
  git status / git rev-parse baseline checks
  local loopback port inspection
  existing frontend/backend dependency presence checks
  local Angular dev server on 127.0.0.1:4200 using existing ui/node_modules
  browser open to http://127.0.0.1:4200 only
  DOM/layout inspection in desktop and narrow viewports
  local dev server stop and port cleanup check
dependencies installed: no
runtime started: yes, frontend dev server only; backend not started
bound address: 127.0.0.1:4200
browser / OS: Codex in-app Browser / Windows
viewport: 1280x720 desktop and 375x800 narrow
reviewed screens:
  URL input area
  save / subscription buttons
  audio quality / format controls visible from saved UI preference state
  advanced settings panel
  queue / saving area headers
  completed / failed result table headers
  subscription table headers
  narrow layout after opening advanced settings
findings:
  blocker: advanced COOKIES helper invites uploading browser cookies for restricted/private downloads
  follow_up: advanced tool labels remain partly English and noisy for beginner Japanese UX
  follow_up: 取得数の上限 helper says 0 means no limit, which can read as unrestricted saving
  ok: main URL placeholder, 保存, 自動取得登録, 音質, 品質, and table headers fit without page-level horizontal overflow
  not_reviewed: backend-loaded result rows, video/captions/thumbnail mode visuals, real completed/failed rows, and real stop/quit runtime wording
blockers:
  backend dependencies were not already present, so backend runtime was not started
follow-up candidate:
  Y-FE-COPY-04 second frontend copy-only pass packet docs-only
```

Review notes:

- No dependency installation, backend runtime, Docker operation, real URL
  submission, real download, screenshot artifact, or source change was
  performed.
- The UI stayed in `サーバーに接続中...` because only the frontend could be
  started inside this lane. The review therefore covers frontend-visible static
  labels/layout and marks backend-dependent states as `not_reviewed`.
- The advanced settings panel is visible without source changes. Its cookie
  helper text conflicts with the current safety question about avoiding
  cookie/token/secret handling invitations.

Target classifications:

- URL input area: `ok`
- Save / subscription buttons: `ok`
- Advanced settings panel: `follow_up`
- Quality / format / codec controls: `partial`
- Captions controls: `not_reviewed`
- Queue / saving area: `partial`
- Completed / failed result table: `partial`
- Help / troubleshooting entry labels: `partial`
- Stop / quit related wording: `not_reviewed`

Decision:

```text
next recommended lane = Y-FE-COPY-04 second frontend copy-only pass packet docs-only
```

## Y-FE-COPY-04 Manual Finding Triage

Y-FE-COPY-04 is a docs-only packet for the observed Advanced settings /
Cookies copy risk. It does not change frontend files, backend files, runtime
behavior, cookie upload behavior, or visibility of existing controls.

Finding carried forward:

```text
source: Y-FE-LOCAL-REVIEW-02
area: Advanced settings / Cookies
current wording family:
  COOKIES
  Upload Cookies
  helper text promoting restricted/private downloads via cookie upload
classification for future copy lane: follow_up
reason:
  beginner-facing wording should not invite cookie/token/secret handling.
  local-only beginner UX should avoid restricted/private download guidance.
```

Future candidate after explicit approval:

```text
Y-FE-COPY-05 cookie-related frontend copy-only implementation
```

Y-FE-COPY-05 may adjust existing visible cookie-related labels/helper text only.
It must keep upload logic, selector values, handlers, state management, API
payloads, backend cookie handling, and local-only security enforcement
unchanged. If disabling, hiding, removing, or changing cookie upload behavior is
desired, use a separate explicit behavior/visibility/security lane.

## Scope

- Add/download form
- Video quality selector
- Audio quality selector
- Quality helper popovers
- Completed/result table
- Result table `品質` column
- Captions / thumbnail quality display
- Mobile/narrow-width readability, if applicable
- Japanese label consistency

## Screenshot Checklist

- [x] Screenshot: initial add form
- [ ] Screenshot: video quality selector opened
- [x] Screenshot: video quality helper popover
- [ ] Screenshot: audio quality selector opened
- [x] Screenshot: audio quality helper popover
- [x] Screenshot: completed/result table with video row
- [x] Screenshot: completed/result table with audio row
- [x] Screenshot: completed/result table with captions/thumbnail row if available
- [x] Screenshot: narrow-width layout

## Expected UI Wording

Video selector/result labels:

- `最高画質（自動）`
- `4K（2160p）`
- `高画質（1440p）`
- `フルHD（1080p）`
- `標準（720p）`
- `軽量（480p）`
- `低容量（360p）`
- `最小（240p）`

Additional current video option/result fallback observed in the UI code:

- `最低画質（自動）`

Audio selector/result labels:

- `最高音質（自動）`
- `高音質（320kbps）`
- `標準（192kbps）`
- `軽量（128kbps）`

Notes:

- `高音質（320kbps）` is format-dependent and appears for MP3.
- M4A currently offers `最高音質（自動）`, `標準（192kbps）`, and
  `軽量（128kbps）`.
- OPUS, WAV, and FLAC currently offer `最高音質（自動）`.

Other:

- Audio selector label: `音質`
- Result table header: `品質`
- Captions/thumbnail quality value: `-`

Helper popover wording to review:

- Video helper should explain quality targets / upper limits, source-quality
  fallback, auto mode, and file-size tradeoff.
- Audio helper should explain quality/file-size tradeoff, lightweight 128kbps,
  and auto mode.

## Pass/Fail Checklist

- [ ] Labels are readable in Japanese.
- [ ] Numeric values are visible where useful.
- [ ] `画質` is not used for audio quality.
- [ ] `品質` column is understandable in the completed/result table.
- [ ] Popovers do not cover critical controls awkwardly.
- [ ] Higher quality/file-size meaning is understandable.
- [ ] Captions/thumbnails do not show misleading quality.
- [ ] No backend/download behavior is implied to change.
- [ ] No public hosting/ads/update wording appears.
- [ ] Local-only wording remains consistent.

## Findings

### Finding 1

- status: environment-limited-review
- screen: static preview add form and completed/result table
- issue: backend state was unavailable in the Codex static preview, leaving
  controls disabled at `サーバーに接続中...`.
- evidence: temporary screenshots captured only static desktop, video helper
  popover, and narrow-width states. Native selector-open states, audio-mode
  visuals, and real result rows were not observed.
- suggested next task: `Y-UI-REVIEW-02R rerun screenshot review with working browser environment`
- risk: Low docs-only risk; limited visual coverage.

### Finding 2

- status: no-blocking-findings-observed
- screen: Y-UI-REVIEW-02R mocked loaded UI review
- issue: No blocking copy/layout issue was observed in the rerun screenshots.
- evidence: screenshots captured the loaded form, audio mode, video/audio
  helper popovers, completed/result rows, `品質` column, video/audio result
  quality labels, captions/thumbnail `-`, and narrow-width layout.
- suggested next task: `Y-UI-REVIEW-02Z review-complete closeout`
- risk: Low docs-only risk; native select dropdown panels were not captured
  visually and were verified via browser DOM evidence instead.

## Next Task Decision

If screenshots show copy/layout issues:

- Create a new High-mid frontend UI copy/layout PR.

If only docs need updating:

- Create a docs-only PR.

If no issues:

- Close as review-complete docs-only.

Safety-gate policy support remains separate and should not be bundled with UI
review.
