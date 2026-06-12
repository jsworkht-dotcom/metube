# CLEAN Portable Distribution Manifest Contract

## Purpose

Y-DIST-01 defines a report-only manifest contract and checker boundary for
future CLEAN portable distribution review.

The contract exists to answer one narrow question before any share, upload, or
package step: does a candidate directory contain files that must never be
distributed?

## Distribution Premise

- Distribution is controlled and limited to known recipients.
- Each recipient runs the app locally on their own PC.
- Public hosting, Cloudflare/public web deployment, and external SaaS/service
  offering remain out of scope.
- No bundled downloads, logs, state, cookies, secrets, tokens, or recipient
  data are allowed.

## Allowed High-Level Contents

Allowed contents are conceptual until a later generation task approves exact
files. Future candidate contents may include:

- app runtime files
- minimal startup script
- README / usage guide
- license / notice files
- checksums / version metadata

This document does not define a generated file list and does not approve
creating a package folder.

## Forbidden Contents

Future CLEAN candidates must not contain:

- downloads or real downloaded media
- logs
- state
- cookies
- tokens
- secrets
- `.env` files
- `.git` data or repository metadata
- `node_modules`
- caches
- test artifacts
- screenshots
- personal settings
- recipient data

The Y-DIST-01 checker also blocks known risky path and filename patterns such as
database files, log files, private key material, backup/temp/swap files, editor
folders, build output folders, and obvious cookie/token/secret/credential/
password/session filenames.

## Checker Behavior

The checker is:

- stdlib-only Python
- report-only
- read-only
- candidate-directory scoped
- non-following for symlinks
- non-generating
- non-packaging

Command shape:

```powershell
python scripts/check_clean_distribution.py <candidate_dir>
python scripts/check_clean_distribution.py <candidate_dir> --json
python scripts/check_clean_distribution.py <candidate_dir> --markdown
```

Blocked findings return a non-zero exit code. A clean candidate returns zero.

If the path is missing or is not a directory, the checker reports a blocked
finding. If the path is the repository root, inspection is allowed but a warning
states that the repository root is not a finished CLEAN distribution candidate.

For small text-like files, the checker scans only conservative secret-like
pattern families and reports only the path, line, and pattern family. It must
not print matching secret values or file contents.

## Metadata Verification

Y-DIST-02 adds a separate report-only metadata checker at
`scripts/check_distribution_metadata.py`.

Future CLEAN candidates must include root-level `VERSION.txt`, `MANIFEST.json`,
`checksums.sha256`, `LICENSE`, and `NOTICE` files. The metadata checker verifies
basic version shape, manifest fields, local-only distribution metadata,
sha256sum-style checksum entries, recomputed SHA-256 matches, duplicate listed
paths, missing listed files, and basic license / notice presence and safety.

The metadata checker does not create metadata, does not generate checksums, does
not create package output, and does not decide legal sufficiency of `LICENSE` or
`NOTICE`.

## Recipient Runbook And First-Run Verification

Y-DIST-03 adds recipient-safe documentation for future handoff and first-run
review:

- `docs/llmwiki/recipient-safe-runbook.md`
- `docs/llmwiki/first-run-local-only-verification.md`

These documents define local-only recipient instructions, first-run local-only
verification items, and stop conditions. They do not create a CLEAN candidate
and do not approve generated package output.

## Known Limits

- The checker only reports on the candidate directory it is given.
- Passing the checker does not prove that a future manual copy step is safe.
- Passing the checker does not replace human review.
- Passing the checker does not approve package generation.
- Large files above the safe scan limit are not content-scanned.
- Binary files are not content-scanned unless a later task adds a safe review
  method.
- The checker cannot prevent future unchecked manual file copying.

## Future Generation Gate

This document does not approve generating `動画保存ツール_ローカル専用/`.

This document does not approve ZIP output.

This document does not approve installer output.

This document does not approve external public hosting.

Future Y-DIST generation work must pass the Y-DIST-01 clean distribution
checker, pass the Y-DIST-02 metadata checker, and review the Y-DIST-03
recipient runbook / first-run verification before any share, upload, ZIP,
installer, or package output step. Any generation task remains blocked until it
receives explicit package-generation approval and human review.
