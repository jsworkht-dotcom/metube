# Privacy Redaction Security

## Scope

Y-SEC-03 adds first-pass privacy hardening for local-only use by known
recipients. The goal is to reduce accidental leakage through logs, API errors,
and user-controlled filename components.

## Runtime Rules

- Logs and user-facing errors should not expose raw submitted URLs, query
  strings, fragments, URL userinfo, bearer tokens, cookies, token-like
  key/value material, or local filesystem paths.
- URL log summaries should preserve only the minimum useful origin context,
  such as scheme and hostname.
- Filename-affecting user input must be reduced to a single safe filename
  component before it reaches queue or subscription output options.
- Reserved Windows device names, path separators, traversal markers, control
  characters, and Windows-invalid filename characters must not pass through as
  filename components.

## Known Limits

- This is first-pass input redaction and filename component sanitization.
- Downstream yt-dlp may still derive filenames internally from extractor
  metadata or templates.
- Do not claim complete final filename control unless a later review proves the
  full downstream filename path.

## Out Of Scope

- Real downloads.
- Cookie/token/secret handling.
- Frontend changes.
- Dependency, Docker, package, lockfile, or generated distribution output.
- Public hosting or external SaaS/service behavior.
