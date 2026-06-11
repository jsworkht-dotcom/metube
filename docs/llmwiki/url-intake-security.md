# URL Intake Security

## Scope

Y-SEC-02 adds first-pass validation for user-submitted download and subscription
URLs before they reach queue or subscription creation.

## Default Behavior

- `URL_INTAKE_GUARD=true` by default, and it must remain enabled when
  `LOCAL_ONLY_MODE=true`.
- Only `http` and `https` URLs are allowed.
- URLs with missing hosts, malformed hosts, or username/password userinfo are
  rejected.
- Localhost, loopback, private, link-local, shared, multicast, reserved, and
  unspecified IP literals are rejected.
- IPv4-mapped IPv6 literals are checked against the same blocked IPv4 ranges.
- Obvious internal hostnames such as `.localhost`, `.local`, `.home`, `.lan`,
  and `metadata.google.internal` are rejected.
- Unsafe API errors use a generic message and do not echo the submitted URL.

## Limits

This is intake protection only. It does not fully control later URLs fetched
internally by yt-dlp, and it does not claim complete protection against all DNS
rebinding or downstream redirect behavior.

DNS resolution exists as an explicit helper option, but runtime request
validation does not perform DNS lookups in this first pass.

## Verification Note

Dependency-free helper coverage runs with standard-library `unittest`. Focused
pytest/aiohttp API coverage is present but requires a dependency-ready
environment.
