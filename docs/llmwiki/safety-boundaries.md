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

The backup and rollback requirements are tracked in
`docs/llmwiki/update-rollback-plan.md`. Future update-apply work must satisfy
that plan before implementation begins.

## Manual Update Apply Boundary

The manual-approval update apply design is tracked in
`docs/llmwiki/manual-update-apply-design.md`. The design does not approve
implementation.

Future update apply work must remain stopped unless all of these are explicit
for the specific update attempt:

- `/update-status` reviewed
- `/update-preflight` reviewed
- Backup completed
- Rollback targets recorded
- Candidate version or changelog reviewed
- Local-only scope confirmed
- Manual confirmation provided for the current target

Do not add an update apply endpoint, update button, backup creation, rollback
creation, Docker pull, git pull / merge / rebase, restart, pip install, or
package update unless a later task explicitly approves that exact scope.

## Dry-Run / Prepare Boundary

The dry-run / prepare-only contract is tracked in
`docs/llmwiki/dry-run-update-contract.md`. The contract does not approve
implementation.

Dry-run means readonly planning only. Prepare-only means validating a specific
plan and required confirmations only. In the first prepare stage, prepare-only
must not create backups or rollback targets.

Future dry-run or prepare work must not add update execution, update buttons,
backup creation, rollback creation, Docker pull, git pull / merge / rebase,
restart, pip install, package update, or credential handling unless a later task
explicitly approves that exact scope.

## Secret Hygiene

Do not read, paste, store, transform, or document real credential values. If credentials
or private values appear in a chat or file, stop and separate the issue as requiring
verification and redaction.
