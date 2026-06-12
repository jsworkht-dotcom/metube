# Codex GitHub CLI Auth Runbook

## Purpose

This note prevents future Codex sessions from getting stuck when GitHub CLI
commands behave differently inside and outside the Codex command sandbox.

Use this runbook only for GitHub CLI publishing or PR operations in this local
fork. Do not store command logs, tokens, cookies, or secrets in project files.

## Confirmed Symptom

In this Windows Codex desktop environment, the same `gh.exe` can report two
different auth states:

- Sandboxed command:
  - `gh auth status` fails.
  - It reports the `jsworkht-dotcom` account token in `default` as invalid.
- Escalated command outside the sandbox:
  - `gh auth status` succeeds.
  - It reports the `jsworkht-dotcom` account as logged in through `keyring`.

The `gh.exe` path and normal environment variables can still be the same in both
cases. The important difference is credential-store access, not the repository,
branch, PR, or GitHub account.

## Root Cause

Codex sandboxed shell commands may be unable to access the Windows keyring entry
that GitHub CLI uses for the valid token. When that happens, `gh` falls back to
an unavailable or invalid default credential source and reports an auth failure.

This is not fixed by changing project files, retrying the GitHub connector, or
re-authenticating repeatedly inside the same blocked sandbox path.

The GitHub connector may also fail with `403 Resource not accessible by
integration` for PR creation, ready-for-review transitions, or GraphQL
mutations in this fork. Treat that as a connector permission limit and fall
back to an escalated `gh` command after verifying CLI auth and PR state.

## Safe Diagnosis

Do:

- Run `git status --short --branch` to confirm the local branch state.
- Run `gh auth status` once in the normal sandbox.
- If it fails with an invalid `default` token, run `gh auth status` once with
  `sandbox_permissions=require_escalated`.
- Compare only the auth source labels, such as `default` versus `keyring`.
- Confirm changed files with `git diff --name-only <base>..HEAD`.

Do not:

- Run `gh auth token`.
- Use `gh auth status --show-token`.
- Open or paste token-bearing config contents.
- Store `GH_TOKEN`, `GITHUB_TOKEN`, cookies, or secrets in repository files.
- Copy masked token output into LLMwiki unless the token body remains masked.

## Standard Procedure For PR Work

When a task needs fork PR creation, checks, merge, or branch cleanup:

1. Prepare and verify the local branch normally.
2. Try `gh auth status` in the sandbox.
3. If sandboxed auth fails but escalated auth succeeds, run PR-related `gh`
   commands with `sandbox_permissions=require_escalated`.
4. Use narrowly scoped escalation justifications, for example:
   - PR creation
   - PR view/checks
   - PR merge
5. Prefer `prefix_rule` values scoped to the command family, such as:
   - `["gh", "pr", "view"]`
   - `["gh", "pr", "checks"]`
   - `["gh", "pr", "merge"]`
6. If the GitHub connector returns `403 Resource not accessible by integration`,
   do not keep retrying it. Use escalated `gh` if auth is valid there.
7. Continue to enforce the project safety gate before merge:
   - worktree clean
   - PR open and not draft
   - `mergeStateStatus` clean
   - changed files match the approved scope
   - no failing checks
   - no token/cookie/secret values

## Connector Ready / Merge Fallback

When the GitHub connector cannot mark a human-approved PR ready for review or
cannot run the relevant GraphQL mutation, the fallback path is allowed only
after the PR is already reviewed and the PR facts are stable.

Required facts before fallback:

- PR state is `OPEN`.
- Draft state and the intended ready transition are understood.
- Base branch is the expected fork branch, normally `master`.
- Head branch is the expected fork branch.
- Head SHA matches the human-approved expected head SHA.
- Changed-file count and changed paths match the approved scope.
- Merge state is clean / mergeable.
- Failed checks are none.
- Generated package folder is absent.
- PR #1001 files are not present in the diff.

Fallback principles:

- Do not read, print, or store token, cookie, secret, or credential values.
- If sandboxed `gh auth status` fails because it cannot access the Windows
  keyring, use escalated `gh` only for the minimal PR operations needed.
- Reconfirm the expected head SHA immediately before ready or merge.
- Stop if the head SHA changes.
- Use an expected-head guard for squash merge, such as `--match-head-commit`.
- Use non-persistent safe Git recovery only when needed; never disable SSL
  verification and never persist unsafe Git config.

Confirmed PR #86 result:

- GitHub connector ready-for-review transition failed with
  `Resource not accessible by integration`.
- Escalated `gh` fallback marked PR #86 ready for review.
- Escalated `gh` fallback squash-merged PR #86 with an expected head SHA guard.
- Merge commit:
  `00a90bfa1efd11935aa46b07848d05614d1c744e`.
- Remote branch `codex/y-dist-02-metadata-checker` was deleted.
- `動画保存ツール_ローカル専用/` remained absent.
- No dependency installation, Docker operation, metadata/checksum generation,
  package output, token/secret/cookie handling, or credential storage occurred.

## Reporting Template

When this issue appears, report it as:

- Root cause: sandboxed `gh` could not access the Windows keyring credential;
  escalated `gh` could.
- Impact: PR operations through sandboxed `gh` or the GitHub connector may fail
  even after the user has restored GitHub CLI auth.
- Mitigation used: verified escalated `gh auth status`, then ran only the needed
  PR commands with scoped escalation.

## Non-Goals

This runbook does not approve:

- storing GitHub tokens in this repository
- adding credential files
- changing Git remotes
- opening upstream PRs
- bypassing project safety gates
- weakening secret hygiene
