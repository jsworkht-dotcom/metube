# New App Bootstrap Template Design

## Purpose

APP-BOOT-01 defines a reusable bootstrap design for future app projects. It
turns the development method proven in this local-only MeTube fork into a
docs-first baseline that can be adapted before implementation starts.

Reusable parts:

- repo-local LLMwiki;
- risk-tiered automation;
- Codex auto lanes;
- preflight environment check;
- safety wording check;
- local safety gate aggregator;
- PR body generator;
- Codex prompt templates;
- human-reviewed High-mid / High-high gates.

The goal is to start new apps faster without weakening safety boundaries.

## Background

The current project established a practical safety and automation workflow:

- Y-AUTO-09 local safety gate aggregator;
- Y-AUTO-10B safety wording checker;
- Y-AUTO-12 PR body generator;
- Y-AUTO-13 Codex prompt templates;
- Y-AUTO-15 preflight environment checker.

These pieces should become the reusable baseline for new app development, with
each new app rewriting its own safety boundaries and app-specific risk examples.

## Relationship To Current Development Method

The current repository remains the source example. A new app bootstrap should
start docs-first and should not start with implementation.

A new app should:

- create its own `docs/llmwiki`;
- define app-specific safety boundaries;
- adopt risk tiers and auto lanes before MVP implementation;
- keep ChatGPT focused on planning and Codex focused on repo work;
- use the current project as a workflow example, not as a copy source for
  MeTube-specific assumptions.

## Non-Goals

APP-BOOT-01 does not:

- create a new app repo;
- create a new app directory;
- implement bootstrap scripts;
- copy files into another repo;
- add CI;
- create package files;
- create generated distribution output;
- create `動画保存ツール_ローカル専用/`;
- run dependency installation operations;
- run container image operations;
- change backend/frontend/Docker/CI/package/lockfile files;
- touch PR #1001 files;
- handle cookie/token/secret values;
- add public exposure operations or ads;
- add update application operations.

## Bootstrap Principles

- Docs-first.
- Safety boundaries before implementation.
- MVP before expansion.
- Local reproducibility before automation expansion.
- Small PRs before broad changes.
- Human review for irreversible or high-risk actions.
- LLMwiki as source of truth.
- ChatGPT for planning / Codex for repo work.

## Recommended Bootstrap Phases

```text
APP-00A:
  purpose / user / MVP definition

APP-00B:
  safety boundaries

APP-00C:
  LLMwiki initial setup

APP-00D:
  Codex automation policy

APP-00E:
  Codex auto lanes

APP-00F:
  local safety gate design

APP-00G:
  PR body / prompt template setup

APP-01A:
  MVP skeleton readiness gate

APP-01B:
  MVP skeleton implementation
```

APP-01B should not start until APP-00A through APP-01A are complete.

## APP-00A: Purpose / User / MVP Definition

Template contents:

```text
app name
target users
primary problem
MVP outcome
non-goals
platform assumption
data sensitivity
external integrations
initial release boundary
```

The output should be short enough to guide implementation decisions. Avoid
turning APP-00A into a product requirements archive.

## APP-00B: Safety Boundaries

Template contents:

```text
forbidden operations
human-review-required operations
data handling limits
secret-like value handling policy
public exposure policy
payment/monetization policy if relevant
deployment policy
rollback policy
```

The safety boundary must be app-specific. Do not inherit local-only video-tool
rules unless the new app has the same actual risk profile.

## APP-00C: LLMwiki Initial Setup

Recommended files:

```text
docs/llmwiki/README.md
docs/llmwiki/current-state.md
docs/llmwiki/roadmap.md
docs/llmwiki/handoff.md
docs/llmwiki/safety-boundaries.md
docs/llmwiki/codex-automation-policy.md
docs/llmwiki/codex-auto-lanes.md
docs/llmwiki/decisions.md
docs/llmwiki/pr-history.md
```

Optional later:

```text
docs/llmwiki/local-safety-gate-aggregator-design.md
docs/llmwiki/safety-wording-checker-design.md
docs/llmwiki/pr-body-generator-design.md
docs/llmwiki/codex-run-prompt-templates.md
docs/llmwiki/preflight-environment-checker-design.md
```

The initial LLMwiki should be concise. It should describe the current truth, not
duplicate long command logs.

## APP-00D: Codex Automation Policy

Recommended risk tiers:

```text
Low:
  docs-only

Medium:
  read-only tools / tests / checkers

High-low:
  automation-adjacent design or dry-run only

High-mid:
  prototypes, generated-output-adjacent tools, write-capable automation

High-high:
  actual distribution artifact creation, deployment, irreversible data changes,
  credential-bearing operations, public exposure, payment-related enablement
```

Low, Medium, and qualifying High-low work can be candidates for auto PR and
auto merge only after the app-specific gates pass. High-mid requires human
review before merge. High-high stops before implementation unless explicitly
approved for the exact task.

## APP-00E: Codex Auto Lanes

Reusable lanes:

```text
Lane A:
  docs-only planning

Lane B:
  report-only / dry-run

Lane C:
  checker-only

Lane D:
  combined report/checker/docs

Lane E:
  High-mid PR-ready only
```

The lanes are execution boundaries, not permission to skip app-specific safety
review.

## APP-00F: Local Safety Gate Design

A new app should define:

```text
preflight environment checker
repo safety checker
wording checker
local safety gate aggregator
project-specific generated-output absence check
project-specific forbidden file leakage check
```

The app does not need every script on day one. APP-00F should define intended
boundaries, required inputs, output format, stop conditions, and when a future
script becomes useful.

## APP-00G: PR Body / Prompt Template Setup

New app PRs should reuse these section patterns:

```text
PR body sections
explicitly not performed
verification presets
human review note
Codex prompt templates
recovery / finalize template
human-reviewed merge template
```

The PR body generator concept is a review aid. It does not replace local gates,
create PRs, edit PRs, or approve merge.

## APP-01A: MVP Skeleton Readiness Gate

Before MVP skeleton implementation, verify:

```text
purpose/MVP finalized
safety boundaries finalized
LLMwiki exists
risk policy exists
auto lanes exist
preflight/gate plan exists
rollback/cleanup policy exists
initial PR workflow works
```

APP-01A is the last docs-first gate before creating code or app directories.

## Recommended New App Directory Baseline

Generic structure:

```text
docs/
  llmwiki/

scripts/
  check_local_dev_environment.py
  check_repo_safety.py
  check_safety_wording.py
  run_local_safety_gates.py
  generate_pr_body.py

app/
  placeholder only after APP-01A

tests/
  placeholder only after MVP skeleton plan
```

Important:

- APP-BOOT-01 only designs this.
- APP-BOOT-02 may create a bootstrap skeleton later if approved.
- Do not create these files in this PR except the design doc.

## Initial LLMwiki File Set

Minimum viable LLMwiki:

```text
README.md
current-state.md
roadmap.md
handoff.md
safety-boundaries.md
codex-automation-policy.md
codex-auto-lanes.md
```

These files should answer: what is the app, what is safe, what is next, and what
should Codex read before acting.

## Initial Scripts Policy

A new app may copy or adapt tools from this project only after explicit
approval.

For APP-BOOT-01, do not copy scripts.

For APP-BOOT-02, decide whether to create template files or only a document
packet.

## Initial Safety Gates

Generic gates:

```text
preflight environment check
wording check
repo safety check
project-specific dry-run/checker if available
generated-output absence check
forbidden file leakage check
changed file scope check
```

The first implementation can start with manual checks and add scripts later.

## Risk Tier Mapping

| Task type | Default risk tier | Auto PR? | Auto merge? | Human review? | Examples |
| --- | --- | --- | --- | --- | --- |
| LLMwiki planning | Low | Yes, if gates pass | Yes, if gates pass | Usually no | purpose note, roadmap sync |
| Safety policy docs | High-low | Yes, if gates pass | Yes, if gates pass | Review if boundaries change materially | safety-boundaries draft, risk-tier sync |
| Read-only checker | Medium | Yes, if gates pass | Yes, if gates pass | Usually no | local report checker, wording checker |
| Dry-run design | High-low | Yes, if gates pass | Yes, if gates pass | Review if close to generated output | output preview contract |
| Prototype tool | High-mid | Yes, if explicitly approved | No | Yes | write-capable local helper prototype |
| Deployment or irreversible task | High-high | No by default | No | Yes | deployment enablement, irreversible data change |

## Auto Lane Mapping

| Lane | Allowed files | Required gates | Auto merge rule | Stop conditions |
| --- | --- | --- | --- | --- |
| Lane A | `docs/llmwiki/**` | wording, repo safety, local aggregator | OK if Low or qualifying High-low and gates pass | docs scope exceeded |
| Lane B | report-only scripts and docs | compile if script changes, repo safety, dry-run checks | OK if Medium or qualifying High-low and gates pass | file writing or generated package output appears |
| Lane C | checker scripts and docs | compile if script changes, repo safety, checker self-test | OK if Medium and gates pass | checker weakens safety gate |
| Lane D | coordinated report/checker/docs | union of Lane B and Lane C gates | OK only when same purpose and same risk band | mixed-risk bundle appears |
| Lane E | explicitly approved prototype scope | task-specific verification and repo safety | No auto merge | High-mid review boundary crossed |

## Standard PR Workflow

```text
preflight
branch
read-first
minimal change
wording check
local safety gates
PR body generation
PR creation
merge gate
post-merge sync
handoff update
```

Each step should be reviewable from local commands or the PR page. Generated PR
body text must be reviewed before use.

## Human Review Gates

Human review is required for:

```text
High-mid
High-high
public exposure
credential-bearing file handling
secret-like value handling
deployment
payment/monetization enablement
irreversible data changes
actual distribution artifact creation
dependency installation operations
container image operations
update application operations
```

Human review is also required when a task's risk tier is unclear.

## Closeout / Handoff Rules

```text
small lane closeout after 2-4 PRs
handoff always updated after meaningful step
current-state and roadmap updated at closeout
do not defer safety boundary updates
```

Safety boundary updates should happen in the same PR that changes the boundary,
or before the boundary-affecting work starts.

## Migration From This Repo

Reusable assets:

```text
LLMwiki structure
risk policy pattern
auto lane pattern
preflight checker concept
wording checker concept
safety gate aggregator concept
PR body generator concept
Codex prompt template concept
```

Do not copy project-specific MeTube or local-only video tool assumptions
blindly.

## What To Customize Per App

Customize:

```text
app purpose
user type
data sensitivity
external services
deployment boundary
generated-output paths
forbidden files
safety gate patterns
risk tier examples
PR # special-case leakage paths
```

Every app should name the data it stores, the external systems it touches, and
the operations that require human review.

## What Not To Copy Blindly

Do not blindly copy:

```text
MeTube-specific package paths
video tool wording
yt-dlp / extractor assumptions
PR #1001 references unless relevant
動画保存ツール_ローカル専用 path unless relevant
local-only video use policy unless relevant
```

The workflow can be reused, but project-specific safety boundaries must be
rewritten.

## Verification Checklist

For APP-BOOT-01 docs-only PR:

```powershell
git diff --check
python scripts/check_local_dev_environment.py --base fork/master --expected-branch master
python scripts/check_safety_wording.py --base fork/master
python scripts/check_safety_wording.py --all
python scripts/run_local_safety_gates.py --base fork/master --scope docs-only
python scripts/generate_pr_body.py --title "docs: design new app bootstrap template" --risk high-low --scope docs-only --changed-files
python scripts/check_repo_safety.py
python scripts/check_repo_safety.py --base fork/master
python scripts/check_clean_package_dry_run_reports.py
python scripts/clean_package_dry_run.py
python scripts/clean_package_dry_run.py --format text
python scripts/clean_package_dry_run.py --format markdown
python scripts/clean_package_dry_run.py --format json
Test-Path "動画保存ツール_ローカル専用"
git diff --name-only fork/master...HEAD
git status --short --branch
git ls-files --others --exclude-standard
```

Use bundled Codex Python if `python` is not on PATH. Do not install Python.

## Stop Conditions

Stop if:

```text
preflight checker has blocking ERROR
wording checker has blocking ERROR
aggregator fails
PR body generator fails
repo safety BLOCKED
report checker fails
dry-run BLOCKED
changed files outside docs scope
scripts changed
backend/frontend/Docker/CI/package/lockfile changed
PR #1001 files appear
generated package folder exists
cookie/token/secret values appear
.gitignore changed
report file is written
generated package output appears
dependency installation operation is required
container image operation is required
```

## Rollback / Cleanup Note

For APP-BOOT-01:

```text
revert docs-only commit
no generated output to clean up
```

For APP-BOOT-02:

```text
rollback depends on whether skeleton files are created
human review required if template writes project files outside docs
```
