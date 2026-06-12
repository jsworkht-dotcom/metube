# Recipient-Safe Runbook

## Purpose

Y-DIST-03 defines the recipient-facing safety runbook for a future CLEAN
portable distribution of `youtubeダウンロード / MeTube local-only fork`.

This document is a source-of-truth runbook only. It does not approve creating a
CLEAN folder, ZIP output, installer output, package output, metadata, checksums,
or any real download.

## Facts / Assumptions / Needs Verification

Facts:

- The fork is intended for local-only use by each recipient on their own PC.
- Public hosting, external-user service operation, and web publication remain
  out of scope.
- Y-DIST-01 defines the forbidden-file and secret-like content checker for a
  future CLEAN candidate.
- Y-DIST-02 defines the version, manifest, checksum, license, and notice
  consistency checker for a future CLEAN candidate.

Assumptions:

- A future recipient receives an already-reviewed local-only distribution from a
  trusted sender.
- The recipient is not expected to edit repository files or run development
  tooling.
- The recipient is expected to use a visible local browser URL only.

Needs verification before any future handoff:

- The distributed material has passed the Y-DIST-01 and Y-DIST-02 checker
  gates on the exact candidate directory.
- The first-run local-only verification has been completed and recorded.
- The recipient has been told where downloads are saved and how to stop the app.

## Recipient Safety Rules

The recipient must treat the tool as local-only personal software:

- Use it only on the recipient's own PC.
- Open it only through a loopback URL such as `localhost`, `127.0.0.1`, or
  `::1`.
- Do not publish the app on the web.
- Do not offer it as a service for external users.
- Do not expose it through a public tunnel, reverse proxy, LAN service mode, or
  hosted endpoint.
- Do not enter, paste, import, store, or share cookie/token/secret/credential
  material.
- Do not use it for DRM bypass.
- Do not use it for authentication bypass.
- Do not use it for restriction circumvention.
- Use it only for the recipient's own videos, videos they have permission to
  use, or videos that are legally usable in their situation.

## Before First Launch

Before the recipient starts the app for the first time, confirm:

- The sender identified the package as local-only.
- The save folder is visible to the recipient and is not a hidden temp folder.
- The recipient knows that downloaded files, if later created, stay on their
  own PC.
- The first browser URL to open is local-only: `localhost`, `127.0.0.1`, or
  `::1`.
- No external host, LAN IP, public IP, or `0.0.0.0` endpoint is part of the
  first-run instructions.
- No cookie/token/secret/credential file is required.
- No update application operations are enabled as part of first launch.

If any item cannot be confirmed, stop before launch.

## During Launch

When the app starts:

- Open only the local browser URL provided by the launcher or sender.
- Confirm the visible URL uses `localhost`, `127.0.0.1`, or `::1`.
- Confirm the app is not reachable through a LAN IP or public IP.
- Confirm the save destination shown to the recipient is understandable and
  expected.
- Keep the app on the local PC; do not share the browser URL with other people.

If the app asks for cookie/token/secret/credential material, stop and do not
continue.

## During Use

Safe use means:

- Paste only URLs for content the recipient owns, has permission to use, or can
  legally use.
- Do not use private account material to reach content that is not normally
  available to the recipient.
- Do not try to bypass DRM, authentication, age gates, region locks, paywalls,
  or other restrictions.
- Do not change local-only settings to expose the app outside the recipient's
  own PC.
- Do not treat warnings about unsupported content as a reason to add secrets or
  bypass settings.

## Stop / Quit

The future recipient guide must make the stop path visible before first use:

- Prefer the provided stop/quit control if the future package includes one.
- If the app was started from a launcher window, close it only through the
  documented stop path.
- Closing the browser tab may not stop the local server.
- If the recipient is unsure whether the app is still running, stop using it
  and ask for help before continuing.

## Stop Conditions

Stop distribution, first-run guidance, or launch confirmation if any of these
are true:

- The app is running on an external/public host.
- The app is listening on `0.0.0.0`, a LAN IP, or a public IP.
- The browser URL is not `localhost`, `127.0.0.1`, or `::1`.
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
- Upstream PR #1001 files are present:
  - `docker-compose.local.yml`
  - `docs/local-only.md`

## Relation To Y-DIST-01 / Y-DIST-02

Y-DIST-01:

- Defines the CLEAN candidate forbidden-file, secret-like content, and manifest
  baseline checker.

Y-DIST-02:

- Defines the `VERSION.txt`, `MANIFEST.json`, `checksums.sha256`, `LICENSE`,
  `NOTICE`, and checksum consistency checker.

Y-DIST-03:

- Defines this recipient-safe runbook and the first-run local-only verification
  contract.
- Standardizes safe recipient instructions and stop conditions.
- Does not generate distribution output.

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
