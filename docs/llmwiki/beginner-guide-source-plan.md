# Beginner Guide Source Plan

## Purpose

Y-06F reviews source candidates for future beginner-facing HTML and TXT guides.

This is documentation-only planning. It does not create
`動画保存ツール_ローカル専用/`, does not generate `.html` or `.txt` files, does
not build packages, and does not change application behavior.

## Scope

Allowed in Y-06F:

- Define future beginner guide source candidates.
- Define Japanese-first wording rules for local-only personal use.
- Define package placement candidates for HTML/TXT guide outputs.
- Define which guide and notice presence checks the dry-run script should warn
  about in a later PR.
- Choose one next implementation candidate.

Not allowed in Y-06F:

- Creating actual guide files in the package root.
- Creating or copying `動画保存ツール_ローカル専用/`.
- Changing backend, frontend, Docker, CI, package, or lockfile files.
- Adding Tauri, Electron, WebView2, installer, signing, or notarization code.
- Adding clean-package generation behavior.
- Handling cookies, tokens, secrets, credentials, private URLs, or private
  local paths.

## Reader Model

The beginner guides are for a non-developer local desktop user.

Assumptions:

- The user wants to save allowed content to their own computer.
- The package is local-only and personal-use scoped.
- The user should not need Docker Desktop, a terminal, Git, Python, Node.js,
  pnpm, npm, uv, Tauri, or Electron knowledge.
- The user needs visible actions: start, save, open save folder, stop, and ask
  for help.

## Planned Guide Source Set

Future source files should live under `docs/llmwiki/` or another explicitly
approved source directory until a generator task is approved.

Recommended source candidates:

```text
docs/llmwiki/package-guides/
  00-first-open.html.source.md
  00-first-open.txt.source.md
  03-how-to-use.html.source.md
  03-how-to-use.txt.source.md
  04-troubleshooting.html.source.md
  04-troubleshooting.txt.source.md
  05-safe-use.html.source.md
```

Rules:

- These are source candidates only, not generated package files.
- The future package output names stay Japanese.
- Markdown source is allowed for editing convenience, but Markdown must not be
  the beginner package entry point.
- A later generator may transform the approved sources into `.html` and `.txt`
  outputs.
- Source files must not contain real submitted video URLs, cookies, tokens,
  secrets, private credentials, or private local paths.

## Planned Package Outputs

Future generated package paths:

```text
動画保存ツール_ローカル専用/
  00_最初に開いてください.html
  00_最初に開いてください.txt
  03_使い方.html
  03_使い方.txt
  04_困ったとき.html
  04_困ったとき.txt
  05_安全な使い方.html
  困ったとき/
    Windowsの警告について.html
    Macの警告について.html
    起動しないとき.html
    保存できないとき.html
```

Placement rules:

- `00_最初に開いてください.html` is the primary first-open guide.
- `00_最初に開いてください.txt` is the shortest fallback guide.
- `03_使い方.*` explains everyday operation.
- `04_困ったとき.*` explains safe next actions for common errors.
- `05_安全な使い方.html` records local-only and permission boundaries.
- Extra troubleshooting pages may live under `困ったとき/`.
- Developer-facing Markdown, manifests, and notices stay under `開発者向け/`.

## HTML Guide Candidates

### `00_最初に開いてください.html`

Role:

- First page a normal user opens.
- Tells the user what the tool is and which OS folder to open.
- States local-only personal use.
- Points to start, save folder, stop, and troubleshooting.

Required visible ideas:

- This tool saves files on this computer.
- Use it only for content the user is allowed to save.
- It is not for public hosting, sharing with outside users, or ads.
- Open `Windows用/` or `Mac用/` for the user's OS.
- Stop if a platform warning looks different from the guide.

Avoid:

- Docker, terminal, Git, Python, Node.js, package manager, Tauri, or Electron
  wording in the normal setup flow.
- Instructions that normalize bypassing platform warnings.

### `03_使い方.html`

Role:

- Everyday operation guide.
- Can be linked from the first-open guide.
- May be reused for in-app help copy later.

Required visible ideas:

- Start the app.
- Paste or enter a supported page URL.
- Choose a beginner-safe save option.
- Start saving.
- Watch progress.
- Open the save folder.
- Wait before closing while a save is active.

Wording preference:

- Use verbs like `起動`, `保存`, `保存先を開く`, `停止して終了`.
- Say what the user should do next when something fails.

### `04_困ったとき.html`

Role:

- Troubleshooting hub.
- Gives one safe next action for each common symptom.

Required symptom sections:

- App does not start.
- Save folder cannot be opened.
- Save fails.
- Conversion fails.
- App says the local backend is not ready.
- Windows warning appears.
- macOS warning appears.
- HTML guide does not open.

Rules:

- Prefer "stop and ask for help" over repair commands.
- Do not recommend Docker pull, git pull, package install, update apply, public
  hosting, LAN exposure, credential upload, or advanced yt-dlp overrides.
- Do not ask users to paste cookies, tokens, secrets, account data, or private
  config values.

### `05_安全な使い方.html`

Role:

- Short safety and scope page.
- Can be linked from all other guide pages.

Required visible ideas:

- Local-only personal use.
- No public hosting.
- No ads or monetization.
- No external-user service.
- No automatic update apply.
- No DRM bypass, authentication bypass, restriction circumvention, or
  mass-download optimization.
- Use only content the user has permission to save.

## TXT Fallback Candidates

TXT files should be short enough to read in a plain text editor.

Recommended future TXT outputs:

```text
00_最初に開いてください.txt
03_使い方.txt
04_困ったとき.txt
```

Rules:

- Keep each TXT file short.
- Avoid tables.
- Avoid Markdown-specific syntax.
- Use numbered sections and short bullet-like lines.
- Include exact package filenames.
- Do not include advanced repair commands.

`00_最初に開いてください.txt` should be the shortest version:

- What this tool is.
- Which OS launcher to open.
- Where saves go.
- How to stop.
- What not to do.

`03_使い方.txt` should focus on:

- Open app.
- Enter URL.
- Save.
- Open save folder.
- Stop after completion.

`04_困ったとき.txt` should focus on:

- Keep the error message.
- Check whether the app is still open.
- Check whether a save is running.
- Check whether the save folder opens.
- Stop if an OS warning appears unexpectedly.

## In-App Help Reuse Candidates

Future UI work may reuse guide wording, but Y-06F does not change the frontend.

Candidate reusable copy themes:

- Save location: files are saved locally.
- Stop behavior: wait while a save is active.
- Error next action: preserve the message and ask for help.
- Update status: diagnostic only, no automatic update apply.
- Safety scope: local-only personal use.

Rules:

- In-app help must not expose Docker, terminal, Git, Python, Node.js, package
  manager, Tauri, or Electron terms to beginner users.
- In-app help must not invite credential entry or advanced yt-dlp option use in
  the beginner flow.

## Dry-Run Warning Candidates

Y-06F does not change `scripts/clean_package_dry_run.py`.

A later dry-run enhancement PR should warn when these source candidates are
missing:

- Approved source for `00_最初に開いてください.html`.
- Approved source for `00_最初に開いてください.txt`.
- Approved source for `03_使い方.html`.
- Approved source for `03_使い方.txt`.
- Approved source for `04_困ったとき.html`.
- Approved source for `04_困ったとき.txt`.
- Approved source for `05_安全な使い方.html`.
- Local-only notice in first-open source.
- Safe-use boundary text in first-open or safe-use source.
- Windows and macOS launch sections.
- Save folder section.
- Stop/quit section.
- Troubleshooting section.

The warning should stay non-blocking until a later generation task makes these
sources required.

## Acceptance Checklist

Future guide sources are acceptable only if:

- HTML remains the primary guide.
- TXT remains a short fallback.
- Markdown is source/developer material only.
- Visible beginner text is Japanese-first.
- Docker, terminal, Git, Python, Node.js, package manager, Tauri, and Electron
  jargon are excluded from the normal beginner flow.
- Local-only personal-use scope is clear.
- Public hosting, ads, external service use, automatic update apply, credential
  handling, DRM bypass, authentication bypass, restriction circumvention, and
  mass-download optimization are excluded.
- No real private values, submitted URLs, cookies, tokens, secrets, or private
  local paths are present.
- No package output is generated by the guide-source PR.

## Current Dry-Run Support

Y-06G added non-blocking missing guide-source and notice-source warnings to
`scripts/clean_package_dry_run.py`.

Warning behavior:

- Missing guide source candidates are reported under `Warnings`.
- Missing local-only safety notice and Windows/macOS section coverage are
  reported under `Warnings`.
- Warning-only runs keep `Status: OK` and exit code `0`.
- No guide generation, package folder, copied license bundle, build/package
  output, or backend/frontend/Docker/CI/package/lockfile changes were added.

## Current Source Drafts

Y-06H added the first beginner guide source candidate:

- Source: `docs/llmwiki/package-guides/00-first-open.html.source.md`
- Future output:
  `動画保存ツール_ローカル専用/00_最初に開いてください.html`
- Status: draft source material only.

Coverage:

- Local-only one-line description.
- Start, URL paste, save, open save folder, and stop/quit steps.
- In-app help entry points: `使い方`, `困ったとき`, `安全な使い方`,
  `保存先を開く`, and `停止して終了`.
- Safe-use boundaries for allowed content, no public hosting, no ads, no
  cookie/token/secret sharing, and no DRM/auth/restriction bypass.
- Troubleshooting entries for app not starting, unknown save location, save
  failures, and unclear exit behavior.

The source does not generate package files and does not approve an HTML
generator.

Y-06I added the first-open TXT fallback source candidate:

- Source: `docs/llmwiki/package-guides/00-first-open.txt.source.md`
- Future output:
  `動画保存ツール_ローカル専用/00_最初に開いてください.txt`
- Status: draft source material only.

Coverage:

- Short description of the local-only tool.
- Start, URL paste, save, open save folder, and stop/quit steps.
- Safe-use boundaries for allowed content, no public hosting, no ads, no
  cookie/token/secret sharing, and no DRM/auth/restriction bypass.
- Troubleshooting entry points for in-app help, save folder, and stop/quit.
- Hand-off to `00_最初に開いてください.html` for the easier visual guide.

The source does not generate package files and does not approve a TXT
generator.

Y-06J added the everyday-use HTML source candidate:

- Source: `docs/llmwiki/package-guides/03-how-to-use.html.source.md`
- Future output:
  `動画保存ツール_ローカル専用/03_使い方.html`
- Status: draft source material only.

Coverage:

- Start, URL paste, save-format selection, save, open save folder, and
  stop/quit steps.
- Beginner-safe format choices for video, audio-only, standard, high quality,
  easy settings, and advanced settings.
- Status explanations for saving, completed, failed, and trying once again.
- Troubleshooting entry points for startup, save failure, unknown save folder,
  and a screen that appears stuck.
- Safe-use boundaries for allowed content, no public hosting, no ads, no
  cookie/token/secret sharing, and no DRM/auth/restriction bypass.

The source does not generate package files and does not approve an HTML
generator.

Y-06K added the everyday-use TXT fallback source candidate:

- Source: `docs/llmwiki/package-guides/03-how-to-use.txt.source.md`
- Future output:
  `動画保存ツール_ローカル専用/03_使い方.txt`
- Status: draft source material only.

Coverage:

- Basic save steps from app startup through stop/quit.
- Save-format choices for video, audio-only, standard, and high quality.
- Saving/completion behavior, retry once, and troubleshooting hand-off.
- Safe-use boundaries for allowed content, no public hosting, no ads, no
  cookie/token/secret sharing, and no DRM/auth/restriction bypass.
- Hand-off to `03_使い方.html` for the easier visual guide.

The source does not generate package files and does not approve a TXT
generator.

Y-06L added the troubleshooting HTML source candidate:

- Source: `docs/llmwiki/package-guides/04-troubleshooting.html.source.md`
- Future output:
  `動画保存ツール_ローカル専用/04_困ったとき.html`
- Status: draft source material only.

Coverage:

- First checks for restart, waiting while saving, opening the save folder, and
  reading the screen status.
- Common trouble cards for startup, URL save failure, unknown save folder,
  stuck-looking saves, missing saved files, stop/quit confusion, possible
  background activity after closing, and unclear update displays.
- Gentle error-message examples for app startup, save-folder confirmation,
  waiting before retry, and URLs that may not be savable.
- Safe-use boundaries for allowed content, no public hosting, no ads, no
  cookie/token/secret sharing, and no DRM/auth/restriction bypass.

The source does not generate package files and does not approve an HTML
generator.

Y-06M added the troubleshooting TXT fallback source candidate:

- Source: `docs/llmwiki/package-guides/04-troubleshooting.txt.source.md`
- Future output:
  `動画保存ツール_ローカル専用/04_困ったとき.txt`
- Status: draft source material only.

Coverage:

- Short first actions for restarting the app, waiting before retrying, opening
  the save folder, and reading the screen status.
- Common trouble entries for startup, URL save failure, unknown save folder,
  stuck-looking saves, missing saved files, stop/quit confusion, and unclear
  update displays.
- Stop/quit guidance that prefers `停止して終了` over closing with X.
- Safe-use boundaries for allowed content, no public hosting, no ads, no
  cookie/token/secret sharing, and no DRM/auth/restriction bypass.
- Hand-off to `04_困ったとき.html` for the easier visual guide.

The source does not generate package files and does not approve a TXT
generator.

Y-06N added the safe-use HTML source candidate:

- Source: `docs/llmwiki/package-guides/05-safe-use.html.source.md`
- Future output:
  `動画保存ツール_ローカル専用/05_安全な使い方.html`
- Status: draft source material only.

Coverage:

- Local-only personal-use premise for using the tool on the user's own PC.
- Allowed-use examples for user-uploaded videos, permission-granted videos,
  legally savable material, and personal learning/organization/backup use.
- Prohibited-use cards for public hosting, ads, external-user service,
  DRM bypass, authentication bypass, restriction circumvention, and
  mass-download purposes.
- Sensitive-data warning for cookie, token, secret, `.env`, cookies.txt,
  personal save data, and personal backups.
- Safe trouble actions and update-safety wording that preserves readonly update
  status and no automatic update execution.

The source does not generate package files and does not approve an HTML
generator.

## Next PR Candidate

Draft `docs/llmwiki/package-notices/metube-notice.source.md` as the first
notice source candidate for future clean-package notice review, while keeping it
as source material only.
