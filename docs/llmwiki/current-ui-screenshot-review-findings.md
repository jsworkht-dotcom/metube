# Current UI Screenshot Review Findings

## Purpose

This records Y-UI-REVIEW-02 review findings for the current local-only MeTube
UI after the quality selector and completed/result table label improvements.

This is a docs-only review result. It does not change UI behavior, backend
behavior, download behavior, packaging behavior, or local-only policy.

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
