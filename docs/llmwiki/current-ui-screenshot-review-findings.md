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

## Y-FE-LOCAL-REVIEW-02 Text Evidence Record

Review status:

```text
status: local-ui-review-executed-with-limitations
```

Environment:

- local HEAD before evidence branch work:
  `6ca2e87d5f124b64742d407f016717ec39a90538`
- expected `fork/master`:
  `6ca2e87d5f124b64742d407f016717ec39a90538`
- PR #118 / Y-FE-LOCAL-REVIEW-01 was confirmed merged on GitHub.
- existing frontend dependencies: present under `ui/node_modules`.
- existing backend dependencies: not present for the bundled Python runtime;
  backend was not started.
- frontend runtime started: yes, local Angular dev server only.
- bound address: `127.0.0.1:4200`.
- browser automation: Codex in-app Browser against loopback only.
- screenshots captured or committed: no.
- real downloads submitted: no.
- real URLs submitted: no.
- generated package folder exists: no.

Observed UI coverage:

- URL input area: observed with placeholder
  `動画・チャンネル・プレイリストのURLを入力`.
- Save / subscription buttons: observed as `保存` and `自動取得登録`.
- Quality / format controls: observed in the visible saved preference state as
  audio controls with `音声`, `MP3`, `音質`, and `最高音質（自動）`.
- Advanced settings panel: observed after opening `詳細設定`.
- Queue / saving area: observed headers and disabled actions in backend-loading
  state.
- Completed / failed result table: observed headers including `種類`, `品質`,
  and `コーデック / 形式`; no rows were present.
- Subscription table: observed headers and disabled actions in backend-loading
  state.
- Narrow layout: observed at 375x800 with no page-level horizontal overflow;
  wide tables remained contained in their scrolling table areas.

Findings:

### Finding 1

- classification: `blocker`
- screen: advanced settings panel
- issue: the visible advanced cookie helper invites uploading browser cookies
  to authenticate restricted or private downloads.
- evidence: the advanced section showed `COOKIES` / `Upload Cookies`, and the
  helper text described uploading a browser cookie file for restricted/private
  downloads.
- risk: This conflicts with the review question that asks whether wording
  invites cookie/token/secret handling.
- suggested next task:
  `Y-FE-COPY-04 second frontend copy-only pass packet docs-only`

### Finding 2

- classification: `follow_up`
- screen: advanced settings panel
- issue: several advanced labels remain English-first: `Option Presets`,
  `TOOLS`, `COOKIES`, `Upload Cookies`, `Import URLs`, `Export URLs`, and
  `Copy URLs`.
- evidence: these labels were visible after opening `詳細設定`.
- risk: Beginner Japanese UX remains noisy in advanced settings.
- suggested next task:
  `Y-FE-COPY-04 second frontend copy-only pass packet docs-only`

### Finding 3

- classification: `follow_up`
- screen: advanced settings panel
- issue: the `取得数の上限` helper says `0` means no limit, which can read as
  unrestricted saving.
- evidence: helper text was available from the rendered advanced settings UI.
- risk: The wording may conflict with the review question about unrestricted
  saving or mass download optimization.
- suggested next task:
  `Y-FE-COPY-04 second frontend copy-only pass packet docs-only`

### Finding 4

- classification: `not_reviewed`
- screen: backend-dependent runtime states
- issue: real completed/failed rows, backend-loaded queue state, visual
  video/captions/thumbnail mode switching, and real stop/quit runtime wording
  could not be reviewed without backend dependencies.
- evidence: backend dependencies were not already present, backend runtime was
  not started, and the frontend remained in `サーバーに接続中...`.
- risk: Remaining visual coverage is partial.
- suggested next task:
  continue with a copy-only packet for observed copy findings; use a separate
  runtime review lane only if real backend state must be inspected later.

Decision:

```text
decision: Y-FE-COPY-04 second frontend copy-only pass packet docs-only
```

## Y-FE-COPY-04 Cookie Copy Packet

Purpose:

```text
Create a docs-only packet for a future cookie-related frontend copy-only
implementation. This packet carries forward the Y-FE-LOCAL-REVIEW-02 manual
UI finding without changing frontend files, runtime behavior, upload handling,
or backend cookie handling.
```

Manual review finding carried forward:

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

Future lane candidate:

```text
Y-FE-COPY-05 cookie-related frontend copy-only implementation
```

Purpose:

```text
Adjust existing visible cookie-related labels/helper text to reduce unsafe
beginner-facing guidance.
```

Allowed future copy-only scope:

- Change only existing visible cookie labels/helper text.
- Replace promotional cookie upload wording with cautionary wording.
- Clarify that cookie upload is not part of the beginner flow.
- Avoid restricted/private download encouragement.
- Avoid asking for cookies, tokens, secrets, or account data.
- Keep the advanced nature clear.
- Keep behavior unchanged.

Candidate future files:

```text
ui/src/app/app.html
docs/llmwiki/current-state.md
docs/llmwiki/handoff.md
docs/llmwiki/roadmap.md
docs/llmwiki/current-ui-screenshot-review-findings.md
```

Candidate replacement wording, docs-only:

```text
Current concern:
  Upload a cookies.txt file from your browser to authenticate restricted or private downloads.

Candidate safer helper:
  通常は使いません。Cookieなどの個人情報を扱うため、初心者向けの通常操作では使用しないでください。

Candidate label:
  Cookie設定（上級者向け）

Candidate status:
  Cookie未設定
  Cookie設定あり

Candidate caution:
  Cookie、token、secretなどの個人情報を共有・入力しないでください。
```

Copy-only cannot solve:

- Remove cookie upload functionality.
- Disable cookie upload.
- Hide advanced tools.
- Change file upload behavior.
- Change backend cookie handling.
- Change local-only security enforcement.

If any of those are desired, create a separate explicit
behavior/visibility/security lane.

Required future Y-FE-COPY-05 verification:

- `git diff --check`
- `python scripts/check_repo_safety.py`
- `python scripts/check_repo_safety.py --base fork/master`
- `python scripts/check_safety_wording.py --base fork/master`
- `python scripts/check_clean_package_dry_run_reports.py`
- `python scripts/clean_package_dry_run.py --format json`
- GitHub check: `local fork safety / local fork safety`
- confirm changed files are limited to approved `ui/**` and docs files
- confirm no behavior changes
- confirm forbidden paths remain absent

Y-FE-COPY-05 stop conditions:

- behavior change becomes necessary
- hiding/removing cookie UI becomes necessary
- file upload logic change becomes necessary
- backend cookie handling change becomes necessary
- dependency/build/package change becomes necessary
- token/secret/cookie value handling appears
- real URL submission or real download becomes necessary

## Y-FE-COPY-06 Cookie Copy Closeout

Y-FE-COPY-05 completed via PR #121.

- Head commit: `e960b11fe6f301a3d21e0bda2f310ea5fb71bdba`.
- Squash merge commit / final `fork/master`:
  `eb22d5746267f972c1f4e1f2397a7fba6e83a161`.

Changed Cookie UI copy:

- `Cookie設定（上級者向け）`;
- `Cookieファイルを選択`;
- `Cookieファイルを変更`;
- `Cookie未設定`;
- `Cookie設定あり`;
- helper text now warns that beginners normally should not use Cookie
  handling because Cookie data is personal information.

Manual UI review finding resolved:

- finding: the advanced settings Cookie helper encouraged restricted/private
  download cookie upload;
- resolution: promotional restricted/private download wording was replaced
  with cautionary advanced-only Japanese-first wording;
- status: the follow-up finding is addressed by copy-only implementation.

Preserved boundaries:

- no cookie upload behavior changes;
- no file input behavior changes;
- no delete cookie behavior changes;
- no `hasCookies` logic changes;
- no `cookieUploadInProgress` logic changes;
- no event handler, state management, API/backend, download, queue,
  subscription, routing, service worker, build tooling, dependency,
  package/lockfile, or artifact changes.

Recorded PR #121 verification:

- `git diff --check`: pass;
- repo safety checks: pass;
- safety wording: pass with warning-only findings;
- clean-package report regression: pass;
- clean-package JSON dry-run: pass;
- Angular lint via `ui/node_modules/.bin/ng.cmd lint`: pass;
- GitHub check `local fork safety / local fork safety`: pass;
- forbidden paths absent.

Next safe decision:

- Recommended: `Y-FE-LOCAL-REVIEW-03 scoped local UI re-review packet
  docs-only`.
- Reason: PR #121 changed visible UI copy, and a short re-review packet keeps
  runtime/start/review boundaries clear before opening the UI again.

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
