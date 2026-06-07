# Handoff

## Short Context

This is `youtubeダウンロード / MeTube local-only fork`, a personal local-only fork of
MeTube. The canonical branch is fork `master`, and local `master` tracks
`fork/master`.

## Read First

1. `docs/llmwiki/current-state.md`
2. `docs/llmwiki/safety-boundaries.md`
3. `docs/llmwiki/roadmap.md`

## Key Points For Codex

- Keep work local-only and personal-use scoped.
- Do not touch upstream PR #1001 unless explicitly asked.
- Do not mix `docker-compose.local.yml` or `docs/local-only.md` into fork-only work.
- Do not handle real cookies, tokens, secrets, DRM bypass, authentication bypass, or
  restriction circumvention.
- For this wiki baseline, only `docs/llmwiki/` files should change.

## Next Step

After the LLMwiki baseline is merged, return to Y-05D runtime verification for
`/update-status` and footer display.
