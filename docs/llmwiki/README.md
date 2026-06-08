# LLMwiki

## Purpose

This LLMwiki is a Markdown-only handoff area for the local-only MeTube fork. It keeps
canonical project context inside the repository so future Codex or ChatGPT sessions do
not need to carry long command logs in memory.

The wiki is local documentation only. It does not introduce a wiki engine, database,
RAG pipeline, MCP server, daemon, external sync, or public publishing workflow.

## Reading Order

1. `current-state.md` - current source of truth, branch/remotes, completed work, next step
2. `safety-boundaries.md` - non-negotiable safety and scope limits
3. `roadmap.md` - near-term verification and future candidate work
4. `pr-history.md` - compressed PR and merge history
5. `handoff.md` - short startup note for the next chat

Operational notes:

- `codex-gh-auth-runbook.md` - GitHub CLI auth troubleshooting for Codex sandbox
  versus Windows keyring behavior

## Update Rules

Do not update every file on every task. Update the LLMwiki only when one of these
events happens:

- A PR is merged
- Project policy changes
- Safety boundaries change
- The next engineering step changes
- A chat becomes too heavy and needs a compact handoff

Do not store full command logs. Save only results, decisions, commit IDs, PRs, and the
next step.

## Role Split With ChatGPT Memory

The repository is the canonical place for detailed project state. ChatGPT memory should
stay small and contain only the latest PR/branch, next step, and safety prohibitions.

When context is unclear, verify against these files and Git state before acting. Treat
anything not confirmed by the repo as "needs verification" rather than filling gaps
from memory.
