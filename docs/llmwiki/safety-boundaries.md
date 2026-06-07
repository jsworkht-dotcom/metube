# Safety Boundaries

## Project Scope

- Local-only personal use
- No web publication
- No external user offering
- No monetization or ad workflow
- Markdown-only project documentation for this LLMwiki

## Prohibited Work

- No DRM bypass
- No authentication bypass
- No restriction circumvention
- No cookie/token/secret handling
- No public hosting
- No ads
- No mass-download optimization
- No backend, frontend, extractor, yt-dlp, Docker, CI, package, or lockfile changes as
  part of this docs-only wiki task

## Update-Status Boundary

`update-status` must remain readonly unless a future manually approved task explicitly
changes that scope.

Do not include any of the following in `update-status` behavior:

- Docker pull
- git pull
- restart
- pip install
- package install or package update
- automatic update application

## Automatic Update Boundary

Do not add automatic update application unless all of these are designed, reviewed, and
explicitly approved by the user in a future task:

- Backup
- Rollback
- Version display
- Changelog or confirmation screen
- Local-only scope
- Explicit manual approval before applying changes

## Secret Hygiene

Do not read, paste, store, transform, or document real credential values. If credentials
or private values appear in a chat or file, stop and separate the issue as requiring
verification and redaction.
