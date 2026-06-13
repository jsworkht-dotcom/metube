# Current UI Screenshot Review Findings

## Purpose

This records Y-UI-REVIEW-02 review findings for the current local-only MeTube
UI after the quality selector and completed/result table label improvements.

This is a docs-only review result. It does not change UI behavior, backend
behavior, download behavior, packaging behavior, or local-only policy.

## Y-FE-REVIEW-01 Manual Evidence Planning

Y-FE-REVIEW-01 does not capture new screenshots. It refreshes the manual review
and screenshot evidence expectations after PR #114 changed visible frontend copy
and PR #115 closed out that implementation lane.

Before any second frontend copy pass, capture or record manual evidence for:

- URL input area
- Save / subscription buttons
- Advanced settings panel
- Quality / format / codec controls
- Captions controls
- Queue / saving area
- Completed / failed result table
- Help / troubleshooting entry labels
- Stop / quit related wording

Evidence should include reviewer, date, browser / OS, viewport, commit,
reviewed screens, findings, blockers, and the follow-up candidate. If the
review finds more wording adjustments, prepare
`Y-FE-COPY-04 second frontend copy-only pass packet` docs-only before any
implementation PR.

## Y-FE-REVIEW-02 Evidence Record

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

Recorded target classifications:

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
review not executed: separate scoped local UI review lane, no source changes
```

## Y-FE-LOCAL-REVIEW-01 Scoped Local Review Packet

Y-FE-LOCAL-REVIEW-01 prepares a docs-only runbook / approval packet for the
next local review attempt:

```text
docs/llmwiki/local-ui-review-runbook.md
```

It carries forward the Y-FE-REVIEW-02 result: no already-running UI was
available on common local dev ports, build/install/runtime start was not
approved in that lane, and all UI targets remained `not_reviewed`.

The future execution lane is:

```text
Y-FE-LOCAL-REVIEW-02 scoped local UI review execution
```

That future lane must remain local-only, loopback-only, notes-only, and
source-change-free. It must stop if install, build, Docker, public exposure,
real URL submission, or real download work becomes necessary.

## Review Status

```text
status: screenshot-reviewed-findings-recorded
```

Temporary screenshots were captured for the reachable static UI, but the
interactive review was limited because the preview could not connect to backend
state and remained at `サーバーに接続中...`. The disabled state blocked visual
review of native selector-open states, audio-mode selector screenshots, and
completed/result rows. Those items are recorded as not observed or
source-verified only.

## Environment

- local HEAD before branch work:
  `2c30cc28080e39949bb4a6ab8e646abb700ebfb1`
- expected `fork/master`:
  `2c30cc28080e39949bb4a6ab8e646abb700ebfb1`
- frontend server was started: yes, as a temporary static preview from a temp
  Angular build
- `ng serve` attempt: blocked by missing `ui/proxy.conf.json`
- screenshots were captured: yes, temporary only
- screenshots were committed: no
- real downloads were submitted: no
- generated package folder exists: no

Temporary screenshot files were kept outside the repository under:

```text
C:\Users\tomikyo\AppData\Local\Temp\y-ui-review-02-screenshots\
```

Captured files:

- `01-desktop-initial-fullpage.png`
- `02-video-quality-helper-popover.png`
- `03-mobile-initial-fullpage.png`

## Checklist Results

- initial add form:
  - status: observed-ok
  - evidence: desktop and narrow-width screenshots show the URL input, save
    buttons, and default video quality controls. The controls were disabled by
    backend-loading state, so this is a static visual observation only.
- video quality selector:
  - status: source-verified-only
  - evidence: DOM/source listed video quality labels including
    `最高画質（自動）`, `4K（2160p）`, `高画質（1440p）`,
    `フルHD（1080p）`, `標準（720p）`, `軽量（480p）`,
    `低容量（360p）`, `最小（240p）`, and `最低画質（自動）`.
    Native selector-open screenshot was blocked because the control remained
    disabled.
- video quality helper popover:
  - status: observed-ok
  - evidence: screenshot captured the `画質` helper popover. The wording
    explains target/upper-limit quality, source-quality fallback, auto mode,
    and file-size tradeoff.
- audio quality selector:
  - status: source-verified-only
  - evidence: `ui/src/app/interfaces/formats.ts` defines audio labels and
    `ui/src/app/app.html` uses `音質`. Audio-mode visual switching was blocked
    because the static preview controls remained disabled.
- audio quality helper popover:
  - status: source-verified-only
  - evidence: `ui/src/app/app.html` defines the `音質` helper popover wording.
    It was not visually opened because audio mode could not be selected in the
    disabled static preview.
- completed/result table:
  - status: observed-ok
  - evidence: desktop and narrow-width screenshots show the completed table
    section and headers. No result rows were available.
- result `品質` column:
  - status: observed-ok
  - evidence: screenshots and DOM evidence show the completed/result table
    header uses `品質`.
- captions/thumbnail quality display:
  - status: source-verified-only
  - evidence: `ui/src/app/app.spec.ts` verifies captions and thumbnails return
    `-` for result quality labels. No safe result rows were available for visual
    observation.
- narrow-width layout:
  - status: observed-ok
  - evidence: 390px-wide screenshot shows the add form, quality controls,
    `サーバーに接続中...` state, completed table header, and horizontal table
    overflow behavior. The disabled backend-loading state limits the review.

## Findings

### Finding 1

- status: environment-limited-review
- screen: static preview add form and completed/result table
- issue: The Codex environment could capture screenshots of the static UI, but
  the UI could not reach backend state and remained at `サーバーに接続中...`.
  Because the form controls stayed disabled, native selector-open states,
  audio-mode visuals, and real completed/result rows were not visually
  reviewed.
- evidence: `ng serve` compiled but stopped because
  `ui/proxy.conf.json` was missing. A temporary static preview rendered enough
  UI for screenshots, but DOM checks showed `select[name="downloadType"]` and
  `select[name="quality"]` were disabled after waiting for API failures.
- suggested next task: `Y-UI-REVIEW-02R rerun screenshot review with working browser environment`
- risk: Low for docs-only closeout; medium confidence visual coverage because
  several interactive states were not observed.

No blocking UI copy or layout issue was observed in the screenshots that were
captured. This is not a full visual pass because audio-mode screenshots,
selector-open screenshots, and real result-row quality displays were not
observed.

## Decision

```text
decision: rerun screenshot review with working browser environment
```

## Next Candidate

```text
Y-UI-REVIEW-02R rerun screenshot review with working browser environment
```

## Y-UI-REVIEW-02R Rerun

### Review Status

```text
status: rerun-screenshot-reviewed-no-blocking-issues
```

The rerun used a temporary static Angular build and a temporary local mock
server outside the repository. The mock server provided safe synthetic
Socket.IO/HTTP data so the UI could leave `サーバーに接続中...`, enable the
form controls, switch to audio mode, and render completed/result rows without
submitting any real download job.

No blocking UI copy or layout finding was observed in the screenshots captured
for the rerun. Native OS select dropdown contents were not visible in the
captured screenshots after clicking the selectors, so selector option labels
are recorded from browser DOM evidence and visible closed-control states.

### Environment

- local HEAD before branch work:
  `d9ce0e2d12d972acb0c04faa4a987767bc643072`
- expected `fork/master`:
  `d9ce0e2d12d972acb0c04faa4a987767bc643072`
- frontend server was started: yes, as a temporary static build served by a
  temporary local mock server
- browser automation was used: yes
- network/API was mocked: yes, with safe synthetic local-only data
- screenshots were captured: yes, temporary only
- screenshots were committed: no
- real downloads were submitted: no
- generated package folder exists: no

Temporary screenshot files were kept outside the repository under:

```text
C:\Users\tomikyo\AppData\Local\Temp\y-ui-review-02r-screenshots\
```

Captured files:

- `01-desktop-loaded-form-and-results.png`
- `02-video-quality-selector-clicked.png`
- `03-video-quality-helper-popover.png`
- `04-audio-mode-mp3-selected.png`
- `05-audio-quality-selector-clicked.png`
- `06-audio-quality-helper-popover.png`
- `07-mobile-loaded-form-and-results.png`

Temporary mock/build files were outside the repository and are not committed:

- `C:\tmp\y-ui-review-02r-mock-server.py`
- `C:\Users\tomikyo\AppData\Local\Temp\y-ui-review-02r-static-preview\`

### Screenshot / Observation Inventory

- initial add form:
  - status: observed-ok
  - evidence: desktop and narrow-width screenshots show the loaded form without
    `サーバーに接続中...`; controls were enabled by mocked Socket.IO state.
- video quality selector labels:
  - status: observed-ok
  - evidence: browser DOM in the loaded UI listed `最高画質（自動）`,
    `4K（2160p）`, `高画質（1440p）`, `フルHD（1080p）`,
    `標準（720p）`, `軽量（480p）`, `低容量（360p）`, `最小（240p）`,
    and `最低画質（自動）`. Native dropdown chrome was not visible in the
    selector-click screenshot.
- video quality helper popover:
  - status: observed-ok
  - evidence: screenshot captured the `画質` helper popover explaining quality
    target/upper-limit behavior, source-quality fallback, auto mode, and
    file-size tradeoff.
- audio mode:
  - status: observed-ok
  - evidence: screenshot captured `種類: 音声`, MP3 format selected, and
    enabled audio quality controls.
- audio quality selector / 音質 label:
  - status: observed-ok
  - evidence: screenshot captured the visible `音質` label and selected
    `最高音質（自動）`; browser DOM listed MP3 options
    `最高音質（自動）`, `高音質（320kbps）`, `標準（192kbps）`, and
    `軽量（128kbps）`.
- audio quality helper popover:
  - status: observed-ok
  - evidence: screenshot captured the `音質` helper popover explaining
    quality/file-size tradeoff, lightweight 128kbps, and auto mode.
- completed/result table:
  - status: observed-ok
  - evidence: screenshot captured a completed/result table populated with safe
    synthetic video, audio, captions, and thumbnail rows.
- result 品質 column:
  - status: observed-ok
  - evidence: screenshot captured the result table header `品質`.
- video result quality label:
  - status: observed-ok
  - evidence: synthetic video row displayed `フルHD（1080p）`.
- audio result quality label:
  - status: observed-ok
  - evidence: synthetic audio row displayed `高音質（320kbps）`.
- captions/thumbnail quality label:
  - status: observed-ok
  - evidence: synthetic captions and thumbnail rows displayed `-`.
- narrow-width layout:
  - status: observed-ok
  - evidence: 375px-wide screenshot captured the loaded audio form and
    completed/result rows with horizontal table overflow behavior.

### Findings

No blocking UI findings were observed in the rerun screenshots.

Review limits:

- Data was safe synthetic/mock data, not real download history.
- Native select dropdown option panels were not visible in the captured browser
  screenshots, so dropdown label coverage relies on browser DOM evidence plus
  closed-control screenshots.
- This rerun does not assert behavior for a real backend session, real
  downloads, private URLs, cookies, tokens, or accounts.

### Decision

```text
decision: close review as complete docs-only
```

### Next Candidate

```text
Y-UI-REVIEW-02Z review-complete closeout
```
