# First-Run Local-Only Verification

## Purpose

Y-DIST-03 defines the first-run local-only verification checklist for a future
CLEAN portable distribution and for a recipient's first launch.

This document is a docs-only verification contract. It does not approve creating
distribution output, generating metadata, generating checksums, running package
builds, installing dependencies, running Docker, or performing real downloads.

## When To Use This Checklist

Use this checklist twice in future distribution work:

- Before sender handoff of an already-created, explicitly approved CLEAN
  candidate.
- During the recipient's first local-only launch.

The checklist must be completed without real download activity unless a later
task separately approves that exact verification scope.

## Facts / Assumptions / Needs Verification

Facts:

- The expected local browser URLs are `localhost`, `127.0.0.1`, or `::1`.
- The local-only runtime boundary rejects non-loopback bind targets when
  `LOCAL_ONLY_MODE=true`.
- Wildcard CORS is blocked in local-only mode.
- Unsafe yt-dlp option overrides and nightly automatic yt-dlp update behavior
  require explicit unsafe escape hatches in local-only mode.

Assumptions:

- The future package launcher, if one exists, starts the app in local-only mode.
- The first-run operator can inspect the visible browser URL and save folder.
- Any future candidate directory is checked explicitly by path, not inferred
  from the repository root.

Needs verification:

- The actual first-run bind address is loopback-only.
- The visible browser URL is local-only.
- No unsafe environment override is active.
- No secret-like data appears in logs, state, or downloads directories.
- The exact CLEAN candidate passes the Y-DIST-01 and Y-DIST-02 checker gates
  before any handoff.

## Verification Checklist

### Candidate And Scope

- Confirm the candidate being verified was created only after explicit human
  approval for package generation.
- Confirm this checklist does not create the candidate.
- Confirm this checklist does not create ZIP, installer, package, metadata, or
  checksum output.
- Confirm no real download is performed during this verification.
- Confirm upstream PR #1001 files are absent:
  - `docker-compose.local.yml`
  - `docs/local-only.md`

### Local Bind And Browser URL

- Confirm the app/server listens only on loopback:
  - `localhost`
  - `127.0.0.1`
  - `::1`
- Confirm the app/server is not listening on:
  - `0.0.0.0`
  - LAN IP
  - public IP
- Confirm the browser URL uses only `localhost`, `127.0.0.1`, or `::1`.
- Confirm no public tunnel, reverse proxy, hosted URL, or LAN-service URL is
  used.

### Host / Origin / Referer / CORS

- Confirm Host handling remains local-only.
- Confirm non-local browser `Origin` values are not accepted for local-only
  operation.
- Confirm state-changing requests are not allowed from non-local `Origin` or
  `Referer` values.
- Confirm no CORS wildcard behavior is enabled.
- Confirm no non-local absolute public host URL is configured.

### Unsafe Overrides And Updates

- Confirm no unsafe yt-dlp option override escape hatch is enabled.
- Confirm no nightly automatic yt-dlp update escape hatch is enabled.
- Confirm no update application operations run during first launch.
- Confirm no dependency install/update operations run during first launch.
- Confirm no Docker pull/build operations run during first launch.
- Confirm no git pull/merge/rebase operations run during first launch.

### Save Folder And Local Files

- Confirm the download save folder is visible and understandable to the
  recipient.
- Confirm no hidden or unexpected temp folder is used as the default save
  destination.
- Confirm logs/state/downloads do not contain cookie/token/secret/credential
  material.
- Confirm no bundled downloads, logs, state, cookies, tokens, secrets, or
  recipient data are included in the candidate.

### Y-DIST Checker Gates

Before sender handoff of a future approved candidate, run the checker gates on
the exact candidate directory:

```powershell
python scripts/check_clean_distribution.py <candidate_dir>
python scripts/check_distribution_metadata.py <candidate_dir>
```

These commands are report-only checker gates. They do not approve package
generation, sharing, upload, ZIP output, installer output, metadata generation,
or checksum generation by themselves.

## Stop Conditions

Stop distribution, first-run guidance, or launch confirmation if any item below
is observed:

- External/public host operation.
- `0.0.0.0`, LAN IP, or public IP bind/listen behavior.
- Browser URL outside `localhost`, `127.0.0.1`, or `::1`.
- Cookie/token/secret/credential input, storage, display, or transfer becomes
  necessary.
- DRM bypass, authentication bypass, or restriction circumvention becomes
  necessary.
- No update application operations may run automatically.
- No Docker pull/build operations may be required.
- No dependency install/update operations may be required.
- No git pull/merge/rebase operations may be required.
- No generated package folder may be created without explicit human approval.
- No ZIP, installer, or package output may be created without explicit human
  approval.
- No metadata or checksum generation may be performed without explicit human
  approval.
- PR #1001 files are present:
  - `docker-compose.local.yml`
  - `docs/local-only.md`

## Verification Record Template

Use this template when future approved distribution work reaches first-run
verification:

```text
Verification date:
Operator:
Candidate path:
Source commit:
Visible local URL:
Observed bind/listen address:
Save folder:
Y-DIST-01 checker result:
Y-DIST-02 checker result:
Generated package folder absent before approved generation:
PR #1001 files absent:
Real download performed: no
Cookie/token/secret/credential material observed: no
Stop conditions observed:
Result:
```

## Relation To Y-DIST-01 / Y-DIST-02

Y-DIST-01:

- Provides the CLEAN candidate forbidden-file, secret-like content, and manifest
  baseline checker.

Y-DIST-02:

- Provides the metadata, version, license, notice, and checksum consistency
  checker.

Y-DIST-03:

- Provides recipient-safe first-run procedure and stop conditions.
- Defines what must be checked before a recipient is told the local-only app is
  safe to open.
- Does not generate the checked candidate.

## Explicit Non-Goals

- No CLEAN folder generation.
- No ZIP / installer / package output.
- No metadata generation.
- No checksum generation.
- No real download.
- No dependency install/update operations.
- No Docker pull/build operations.
- No backend/frontend runtime change.
- No yt-dlp extractor change.
- No download queue change.
- No public hosting.
- No cookie/token/secret handling.
- No PR #1001 files.
