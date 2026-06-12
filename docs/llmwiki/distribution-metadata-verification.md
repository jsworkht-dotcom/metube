# Distribution Metadata Verification

## Purpose

Y-DIST-02 defines the report-only metadata verification contract for a future
CLEAN portable distribution candidate.

The checker answers a narrow question: does an already-created candidate
directory include the required distribution metadata, and do listed file hashes
match `checksums.sha256`?

This contract does not approve creating metadata, generating checksums, creating
`動画保存ツール_ローカル専用/`, ZIP output, installer output, or any other package
output.

## Command

```powershell
python scripts/check_distribution_metadata.py <candidate_dir>
python scripts/check_distribution_metadata.py <candidate_dir> --json
python scripts/check_distribution_metadata.py <candidate_dir> --markdown
```

The checker is stdlib-only Python, read-only, and candidate-directory scoped.
Blocked findings return a non-zero exit code. Warnings do not block.

The checker runs the Y-DIST-01 clean distribution checker as a prerequisite and
includes those findings in its report.

## Required Files

The candidate root must contain these files:

- `VERSION.txt`
- `MANIFEST.json`
- `checksums.sha256`
- `LICENSE`
- `NOTICE`

Missing required files are blocked findings. The checker does not create or
repair any required file.

## Version Rules

`VERSION.txt` must be small text with exactly one non-empty version line.

Accepted version values are intentionally simple and version-like, for example:

- `1.0.0`
- `1.0.0-local`
- `2026.06.12`
- `20260612`

The value must not be extremely long, multiline, contain path separators, or
contain secret-like material.

## Manifest Rules

`MANIFEST.json` must parse as a JSON object and contain these fields:

- `package_name`
- `version`
- `source_commit`
- `created_from`
- `local_only`
- `distribution_type`

Required constraints:

- `local_only` must be `true`.
- `distribution_type` must be `clean-portable` or
  `local-only-clean-portable`.
- `source_commit` must look like a 7 to 40 character Git SHA.
- `package_name` must be non-empty and safe.
- `version` must match `VERSION.txt`.
- `created_from` must be non-empty.

The checker does not require `source_commit` to match the current repository
commit because it verifies arbitrary candidate directories. A future generation
gate may add that stronger check.

## Checksum Rules

`checksums.sha256` uses sha256sum-style lines:

```text
<64 hex sha256>  <relative/path>
```

Blank lines and `#` comments are allowed.

Each listed path must be relative, must not contain `..`, must not be absolute,
must not use backslashes, and must resolve to a regular non-symlink file inside
the candidate. The checker recomputes SHA-256 and blocks mismatches, missing
listed files, malformed lines, duplicate listed paths, symlink targets, and
non-regular listed paths.

`checksums.sha256` is not required to list itself. Extra candidate files that
are not listed are warnings in this first pass, not blockers.

## License And Notice Rules

`LICENSE` and `NOTICE` must exist at the candidate root, be regular files, be
non-empty, remain under the safe size limit, and avoid secret-like content
patterns.

This checker does not decide legal sufficiency. Human review is still required
for license and notice completeness.

## Known Limits

- The checker verifies only the candidate path it is given.
- Passing this checker does not approve package generation or sharing by itself.
- Passing this checker does not prove legal sufficiency of `LICENSE` or
  `NOTICE`.
- Extra unlisted files are warnings in this first pass.
- The checker does not generate metadata or checksums.
- The checker does not compare `source_commit` to the current repository HEAD.
- Human review is still required before any CLEAN share, upload, ZIP, installer,
  or package generation lane.

## Future Generation Gate

Future CLEAN share, upload, or package generation must pass both:

- Y-DIST-01: forbidden-file / clean distribution checker
- Y-DIST-02: metadata / checksum / version / license-notice checker
- Y-DIST-03: recipient-safe runbook and first-run local-only verification
- Y-DIST-04: advisory distribution readiness matrix
- Y-DIST-05: human approval checklist before artifact generation
- Y-DIST-06: approved clean candidate dry-run plan

Any actual metadata generation, checksum generation, package folder creation,
ZIP output, installer output, or distribution upload remains blocked until a
separate task explicitly approves that exact generation scope.

Y-DIST-03 is procedural documentation only. It standardizes the recipient
instructions and first-run stop conditions that must be reviewed before handoff,
but it does not generate metadata, generate checksums, create a package folder,
or perform a real download.

Y-DIST-04 is advisory documentation only. It summarizes ready, blocked,
human-review-required, not-started, not-applicable-yet, and warning-only items
before any generation lane, but it does not approve metadata generation,
checksum generation, package folder creation, or real download verification.

Y-DIST-05 and Y-DIST-06 define the approval gate and the future approved
dry-run plan. They do not create metadata, generate checksums, create a CLEAN
folder, or run candidate-directory checkers before an approved candidate exists.
