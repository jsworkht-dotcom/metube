# Local UI Review Runbook

## Purpose

Y-FE-LOCAL-REVIEW-01 is a docs-only runbook / approval packet for a later
scoped local UI review. It defines what a future review lane may do, what it
must not do, and how to record evidence.

This packet does not start the app, build frontend assets, install
dependencies, run the backend, perform downloads, change source files, create
artifacts, or expose the app beyond loopback.

## Baseline

Repository:

```text
C:\Users\tomikyo\_projects\youtubeダウンロード
```

Canonical branch:

```text
fork/master
```

Current baseline:

```text
fork/master = 97d031199f2d907f8b4dca7323e011ada60557af
PR #117 merged
Y-FE-REVIEW-02 manual UI review evidence record completed
```

## Reason For This Packet

Y-FE-REVIEW-02 result:

```text
Manual UI review was not executed.
No already-running UI was available on common local dev ports.
Build/install/runtime start was not approved in that lane.
All UI targets remained not_reviewed.
```

Y-FE-LOCAL-REVIEW-01 prepares a narrow future execution lane so the next review
can inspect the local UI without drifting into frontend implementation,
runtime behavior changes, package generation, dependency installation, or
public exposure.

## Future Review Lane

Future lane:

```text
Y-FE-LOCAL-REVIEW-02 scoped local UI review execution
```

Purpose:

```text
Start or use local-only UI only for visual/manual review of PR #114 copy changes.
Record findings.
Do not change source files.
```

Y-FE-LOCAL-REVIEW-02 requires explicit approval before execution. This packet
does not approve the execution by itself.

## Allowed Only In The Future Execution Lane

Allowed only in Y-FE-LOCAL-REVIEW-02, after explicit approval:

- inspect local ports;
- start local frontend/backend only if existing dependencies are already
  present;
- open a loopback-only browser URL;
- review visible UI labels and layout;
- capture notes, not generated artifacts;
- record findings in a docs-only follow-up.

Loopback-only means:

```text
localhost
127.0.0.1
::1
```

Non-loopback binding, public tunnels, LAN exposure, and public hosting remain
forbidden.

## Future Command Boundaries

Allowed future command families only if dependencies already exist:

```text
git status / git diff
local port inspection
local frontend dev command only if no install/update is needed
local backend start only if no install/update is needed
browser open to localhost / 127.0.0.1 only
```

Not allowed:

```text
`pnpm` install commands
`npm` install commands
uv sync
`pip` install commands
Docker operations
build/package commands
public tunnel
LAN bind
real URL submission
real download
```

If a local UI cannot be used without install, build, Docker, package creation,
or dependency update work, the future lane must stop and record that the UI
review was not executed.

## Manual Review Targets

Manual review targets:

- URL input area
- save / subscription buttons
- advanced settings panel
- quality / format / codec controls
- captions controls
- queue / saving area
- completed / failed result table
- help / troubleshooting entry labels
- stop / quit related wording

The review target is visible copy and layout after PR #114 / Y-FE-COPY-02. The
future lane must not alter selector ids, values, API payloads, state
management, backend behavior, queue behavior, download behavior, or runtime
security behavior.

## Evidence Template

```text
Local UI review evidence:
  reviewer:
  date:
  commit:
  commands run:
  dependencies installed:
  runtime started:
  bound address:
  browser / OS:
  viewport:
  reviewed screens:
  findings:
  blockers:
  follow-up candidate:
```

For Y-FE-LOCAL-REVIEW-02, `dependencies installed` must be `no`. If runtime is
started, `bound address` must be loopback-only.

## Decision Rules

If review finds copy/layout issues:

```text
next recommended lane = Y-FE-COPY-04 second frontend copy-only pass packet docs-only
```

If review finds no issues:

```text
next recommended lane = frontend copy work hold / return to docs-report-checker lane
```

If runtime cannot start without install/build/Docker:

```text
stop and record not executed; do not install or build
```

## Explicitly Not Allowed

Y-FE-LOCAL-REVIEW-01 and the future Y-FE-LOCAL-REVIEW-02 execution lane do not
allow:

- frontend code changes;
- `ui/` file changes;
- backend code changes;
- runtime behavior changes;
- app start in this packet lane;
- frontend dev server run in this packet lane;
- frontend build;
- frontend test;
- backend run in this packet lane;
- dependency install/update;
- Docker image pull/build/run operations;
- real download;
- test download;
- URL submission to external services;
- cookie/token/secret/credential handling;
- public hosting / LAN exposure / non-loopback exposure;
- artifact generation;
- CLEAN folder generation;
- `動画保存ツール_ローカル専用/` creation;
- ZIP / installer / package output;
- metadata/checksum generation;
- recipient handoff / sharing;
- GitHub settings mutation;
- branch protection / ruleset / required-check / CODEOWNERS mutation;
- `.github/workflows/` changes;
- `.gitignore` changes;
- DRM/auth/restriction bypass.

Forbidden paths must remain absent:

```text
動画保存ツール_ローカル専用/
docker-compose.local.yml
docs/local-only.md
```

## Current-State Sync

PR #117 completed Y-FE-REVIEW-02. Y-FE-LOCAL-REVIEW-01 prepares the scoped local
UI review runbook / approval packet. Artifact generation remains HOLD.

Next recommended lane:

```text
Y-FE-LOCAL-REVIEW-02 scoped local UI review execution, only after explicit approval.
```
