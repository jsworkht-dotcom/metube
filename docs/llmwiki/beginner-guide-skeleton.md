# Beginner Guide Skeleton

## Purpose

Y-06C defines the documentation-only skeleton for future beginner-facing
desktop package guides.

The future package should use:

- `.html` as the primary beginner guide.
- `.txt` as the fallback guide when HTML cannot be opened.
- `.md` only for developer or LLMwiki planning.

Y-06C does not generate actual `.html` or `.txt` files.

## Reader Model

The guide is for a non-developer local desktop user.

Assumptions:

- The user wants to save videos locally for personal use.
- The user should not need Docker Desktop.
- The user should not need terminal commands.
- The user should not need Git, Python, Node.js, pnpm, npm, uv, Tauri, or
  Electron knowledge.
- The user needs clear stop/quit behavior and a visible save location.

The guide must keep the visible beginner path local-only, short, and concrete.

## HTML Guide Candidate Path

Future generated path:

```text
動画保存ツール_ローカル専用/00_最初に開いてください.html
```

Role:

- Main guide.
- Japanese-first.
- Sectioned with headings and short paragraphs.
- Designed to be opened by double-clicking.
- Avoids developer jargon in the visible beginner flow.

## HTML Guide Skeleton

### 1. First-Run Guide

Purpose:

- Tell the user what this tool is.
- Say it is local-only and personal-use scoped.
- Tell the user which OS folder to open next.
- Explain that public hosting, ads, account sharing, and external service use
  are not part of this package.

Visible content should cover:

- The app saves files to the user's computer.
- The app runs locally.
- The user should open the Windows or Mac launcher for their OS.
- The user should stop if OS security warnings look different from the guide.

Avoid:

- Docker, terminal, git, Python, Node.js, package manager, or source branch
  language.

### 2. How To Start

Windows section:

- Open `Windows用/`.
- Double-click `動画保存ツール.exe`.
- If that does not work, use `予備_起動する.bat` only as a fallback.
- Explain SmartScreen at a high level without telling users to ignore warnings.

macOS section:

- Open `Mac用/`.
- Open `動画保存ツール.app`.
- If that does not work, use `予備_起動する.command` only as a fallback.
- Explain Gatekeeper at a high level without telling users to bypass warnings
  casually.

The guide must not claim signing/notarization readiness until that exists.

### 3. Basic Usage

Visible content should cover:

- Paste or enter a supported video/page URL.
- Choose the intended format only through beginner-safe controls.
- Start the save action.
- Watch progress in the app.
- Wait until completion before closing if a download is active.

Safety reminders:

- Use only content the user is allowed to save.
- Do not describe DRM bypass, authentication bypass, restriction
  circumvention, or mass-download optimization.
- Do not ask users for cookies, tokens, secrets, or private credentials.

### 4. Open Save Folder

Visible content should cover:

- The default save folder is local.
- Windows candidate: `Downloads\MeTube`.
- macOS candidate: `Downloads/MeTube`.
- Use the app's "open save folder" action when available.
- `予備_保存先を開く.*` helpers are fallback only.

Avoid:

- Telling users to browse internal runtime folders.
- Mentioning package internals unless troubleshooting requires it.

### 5. Stop And Quit

Visible content should cover:

- If nothing is running, closing the app stops it.
- If a download is running, the app should ask what to do before quitting.
- Use the app's stop/quit action when available.
- Fallback helpers exist only when the normal app cannot stop cleanly.

Do not approve:

- Hidden background service behavior.
- Automatic restart after quit.
- Update apply during quit.

### 6. Troubleshooting

Troubleshooting sections should be short and action-oriented:

- App does not start.
- Save folder cannot be written.
- Download fails.
- Conversion fails.
- App says the local backend is not ready.
- Windows warning appears.
- macOS warning appears.
- HTML guide does not open.

Each section should include:

- What the user sees.
- One safe next action.
- When to stop and ask for help.

Troubleshooting must not recommend:

- Docker pull.
- git pull / merge / rebase.
- pip install.
- package install/update.
- update apply.
- Cookie/token/secret upload.
- Public hosting or LAN exposure.

### 7. Safe Use

Visible content should cover:

- Local-only personal use.
- No public hosting.
- No ads or monetization.
- No account sharing workflow.
- No cookie/token/secret handling in the beginner package.
- No DRM bypass, authentication bypass, or restriction circumvention.
- Use only content the user has permission to save.

### 8. Update Status

Visible content should cover:

- Version/update information is diagnostic only.
- Update apply is not part of this beginner package.
- The app must not run Docker, git, package manager, or installer operations as
  an automatic update.
- If update information says something is available, the guide should say to
  wait for a separately reviewed update path.

### 9. Error Next Actions

The guide should use a small decision path:

```text
1. Is the app still open?
2. Is a download currently running?
3. Can the save folder be opened?
4. Does the error mention a platform warning?
5. If unsure, stop and preserve the error message.
```

The guide should prefer "stop and ask for help" over advanced repair commands.

### 10. What This Package Does Not Do

Visible content should clearly exclude:

- Public web hosting.
- LAN sharing.
- Ads or monetization.
- Automatic update apply.
- Docker-based setup.
- Terminal-based setup.
- Cookie/token/secret handling.
- DRM bypass, authentication bypass, or restriction circumvention.
- Mass-download optimization.

## TXT Fallback Candidate Path

Future generated path:

```text
動画保存ツール_ローカル専用/00_最初に開いてください.txt
```

Role:

- Opens in a plain text editor.
- Gives the shortest safe version of the HTML guide.
- Avoids tables and complex formatting.
- Easy to copy into support messages.

## TXT Fallback Skeleton

Suggested structure:

```text
動画保存ツール_ローカル専用

1. このツールについて
   - このツールはローカル専用です。
   - 個人利用向けです。
   - Web公開、広告収益化、外部サービス化はしません。

2. 起動方法
   - Windows: Windows用\動画保存ツール.exe を開きます。
   - Mac: Mac用/動画保存ツール.app を開きます。
   - うまく起動しない場合だけ、予備の起動ファイルを使います。

3. 保存先
   - 保存先はパソコン内のフォルダです。
   - アプリ内の「保存先を開く」を使います。

4. 終了方法
   - ダウンロード中は、終わるまで閉じないでください。
   - 閉じる時に確認が出た場合は、内容を読んで選びます。

5. 困ったとき
   - エラー文を残します。
   - 保存先を開けるか確認します。
   - OSの警告が出た場合は、無理に進めず確認します。

6. しないこと
   - Cookie、token、secretは扱いません。
   - 特別な開発者向け準備は不要です。
   - 自動更新はしません。
```

The actual future TXT may adjust wording, but it must stay short and avoid
advanced repair commands.

## Developer Guide Boundary

Developer and LLMwiki material belongs outside the beginner flow.

Candidate future location:

```text
動画保存ツール_ローカル専用/開発者向け/
```

Allowed developer topics:

- Package manifest.
- Runtime file layout.
- License and notices.
- Backend sidecar lifecycle.
- Local-only environment overrides.
- Checksums.
- Source commit and version metadata.
- Future dry-run package generator contract.

Still prohibited:

- Real cookie/token/secret values.
- Private URLs or private local paths.
- Instructions that turn the app into a public service.
- Instructions that bypass platform security, authentication, DRM, or
  restrictions.

## Copy Rules

Beginner-facing copy should:

- Use Japanese first.
- Use short sentences.
- Use concrete filenames.
- Use OS-specific labels.
- Prefer "open", "save", "stop", and "ask for help" over technical verbs.
- Explain warnings as safety signals.
- Keep update information readonly.

Beginner-facing copy should not:

- Require command-line knowledge.
- Mention Docker, git, Python, Node.js, pnpm, npm, uv, Tauri, Electron, or
  package managers in normal setup instructions.
- Ask for credentials.
- Explain how to bypass site or OS restrictions.
- Normalize warning bypasses as ordinary setup.

## Acceptance Checklist

A future generated guide is acceptable only if:

- HTML is the primary guide.
- TXT is a short fallback.
- Markdown is not the beginner entry point.
- Windows and macOS paths are clear.
- Save folder behavior is clear.
- Stop/quit behavior is clear.
- Security warnings are explained without casual bypass instructions.
- Update status is described as readonly.
- Cookie/token/secret handling is excluded.
- Public hosting and ads are excluded.
- No implementation or package generation is mixed into the docs task.

## Current Dry-Run Support

Y-06D added the docs-only clean-package generator dry-run contract in
`docs/llmwiki/clean-package-dry-run-contract.md`.

Y-06E added the initial report-only dry-run script:

- Script path: `scripts/clean_package_dry_run.py`
- Output: sanitized human-readable text report.
- Exit codes: `0` for OK, `1` for blockers, and `2` for CLI usage errors.

The next review step is to run the dry-run report before any future beginner
guide generation task:

- Emit sanitized reports only.
- Validate future guide presence and local-only notice requirements.
- Validate safe paths, include/exclude rules, forbidden filename families,
  forbidden content pattern families, generated folder presence, and PR #1001
  leakage checks.
- Keep actual guide generation, package generation, generated folders, build
  scripts, installers, signing, backend changes, frontend changes, Docker
  changes, CI changes, package changes, and lockfile changes out of scope.
