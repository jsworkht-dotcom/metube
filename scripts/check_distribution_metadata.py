#!/usr/bin/env python3
"""Report-only metadata and checksum checker for CLEAN distribution candidates.

The checker inspects only the candidate directory provided on the command line.
It does not create metadata, generate checksums, copy files, zip packages,
install dependencies, or modify the repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

try:
    from scripts.check_clean_distribution import (
        SECRET_PATTERNS,
        scan_candidate as scan_clean_candidate,
    )
except ModuleNotFoundError:  # pragma: no cover - used when run as a script path
    from check_clean_distribution import (  # type: ignore[no-redef]
        SECRET_PATTERNS,
        scan_candidate as scan_clean_candidate,
    )


REQUIRED_METADATA_FILES = (
    "VERSION.txt",
    "MANIFEST.json",
    "checksums.sha256",
    "LICENSE",
    "NOTICE",
)

VERSION_SIZE_LIMIT_BYTES = 1_024
MANIFEST_SIZE_LIMIT_BYTES = 64 * 1_024
CHECKSUMS_SIZE_LIMIT_BYTES = 1_000_000
LICENSE_NOTICE_SIZE_LIMIT_BYTES = 1_000_000

VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$")
SOURCE_COMMIT_RE = re.compile(r"^[0-9a-fA-F]{7,40}$")
SHA256_LINE_RE = re.compile(r"^([0-9a-fA-F]{64}) {2}(.+)$")
WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:")

ALLOWED_DISTRIBUTION_TYPES = {
    "clean-portable",
    "local-only-clean-portable",
}


@dataclass(frozen=True)
class Finding:
    path: str
    category: str
    message: str
    pattern_family: str | None = None
    line: int | None = None


@dataclass(frozen=True)
class CheckResult:
    candidate: str
    status: str
    blocked: tuple[Finding, ...]
    warnings: tuple[Finding, ...]
    metadata_files_checked: int = 0
    checksum_entries_checked: int = 0

    @property
    def ok(self) -> bool:
        return not self.blocked

    def to_dict(self) -> dict[str, object]:
        return {
            "candidate": self.candidate,
            "status": self.status,
            "blocked": [asdict(finding) for finding in self.blocked],
            "warnings": [asdict(finding) for finding in self.warnings],
            "summary": {
                "blocked_count": len(self.blocked),
                "warning_count": len(self.warnings),
                "metadata_files_checked": self.metadata_files_checked,
                "checksum_entries_checked": self.checksum_entries_checked,
            },
        }


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix() or "."
    except ValueError:
        return path.name


def _finding_from_clean(finding: object) -> Finding:
    return Finding(
        path=getattr(finding, "path", "."),
        category=f"clean_distribution.{getattr(finding, 'category', 'finding')}",
        message=f"Y-DIST-01 prerequisite: {getattr(finding, 'message', 'finding reported')}",
        pattern_family=getattr(finding, "pattern_family", None),
        line=getattr(finding, "line", None),
    )


def _require_root_file(root: Path, name: str, blocked: list[Finding]) -> Path | None:
    path = root / name
    if path.is_symlink():
        blocked.append(
            Finding(
                path=name,
                category="required_metadata",
                message="required metadata file is a symlink",
            )
        )
        return None
    if not path.exists():
        blocked.append(
            Finding(
                path=name,
                category="required_metadata",
                message="required metadata file is missing",
            )
        )
        return None
    if not path.is_file():
        blocked.append(
            Finding(
                path=name,
                category="required_metadata",
                message="required metadata path is not a regular file",
            )
        )
        return None
    return path


def _read_limited_text(
    path: Path,
    rel_path: str,
    size_limit: int,
    blocked: list[Finding],
) -> str | None:
    try:
        size = path.stat().st_size
    except OSError:
        blocked.append(
            Finding(
                path=rel_path,
                category="metadata_read_error",
                message="could not stat metadata file",
            )
        )
        return None

    if size > size_limit:
        blocked.append(
            Finding(
                path=rel_path,
                category="metadata_size",
                message="metadata file exceeds the safe size limit",
            )
        )
        return None

    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        blocked.append(
            Finding(
                path=rel_path,
                category="metadata_read_error",
                message="could not read metadata file",
            )
        )
        return None


def _add_secret_like_findings(text: str, rel_path: str, blocked: list[Finding]) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern_family, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                blocked.append(
                    Finding(
                        path=rel_path,
                        category="secret_like_metadata",
                        message="secret-like content pattern found",
                        pattern_family=pattern_family,
                        line=line_number,
                    )
                )


def _is_safe_package_name(value: object) -> bool:
    if not isinstance(value, str):
        return False
    if not value or value != value.strip() or len(value) > 128:
        return False
    if "/" in value or "\\" in value or "\x00" in value or ".." in value:
        return False
    return not any(ord(character) < 32 or ord(character) == 127 for character in value)


def _is_nonempty_safe_text(value: object, max_length: int) -> bool:
    if not isinstance(value, str):
        return False
    if not value or value != value.strip() or len(value) > max_length:
        return False
    if "\x00" in value:
        return False
    return not any(ord(character) < 32 or ord(character) == 127 for character in value)


def _validate_version(root: Path, blocked: list[Finding]) -> str | None:
    path = _require_root_file(root, "VERSION.txt", blocked)
    if path is None:
        return None

    text = _read_limited_text(path, "VERSION.txt", VERSION_SIZE_LIMIT_BYTES, blocked)
    if text is None:
        return None

    _add_secret_like_findings(text, "VERSION.txt", blocked)
    non_empty_lines = [line.strip() for line in text.splitlines() if line.strip()]

    if len(non_empty_lines) != 1:
        blocked.append(
            Finding(
                path="VERSION.txt",
                category="version_format",
                message="VERSION.txt must contain exactly one non-empty version line",
            )
        )
        return None

    version = non_empty_lines[0]
    if len(version) > 64:
        blocked.append(
            Finding(
                path="VERSION.txt",
                category="version_format",
                message="version value is too long",
            )
        )
        return None
    if "/" in version or "\\" in version:
        blocked.append(
            Finding(
                path="VERSION.txt",
                category="version_format",
                message="version value must not contain path separators",
            )
        )
        return None
    if not VERSION_RE.fullmatch(version) or not any(character.isdigit() for character in version):
        blocked.append(
            Finding(
                path="VERSION.txt",
                category="version_format",
                message="version value is not a sane version-like value",
            )
        )
        return None

    return version


def _validate_manifest(root: Path, version: str | None, blocked: list[Finding]) -> None:
    path = _require_root_file(root, "MANIFEST.json", blocked)
    if path is None:
        return

    text = _read_limited_text(path, "MANIFEST.json", MANIFEST_SIZE_LIMIT_BYTES, blocked)
    if text is None:
        return

    _add_secret_like_findings(text, "MANIFEST.json", blocked)

    try:
        manifest = json.loads(text)
    except json.JSONDecodeError as exc:
        blocked.append(
            Finding(
                path="MANIFEST.json",
                category="manifest_json",
                message="MANIFEST.json is not valid JSON",
                line=exc.lineno,
            )
        )
        return

    if not isinstance(manifest, dict):
        blocked.append(
            Finding(
                path="MANIFEST.json",
                category="manifest_shape",
                message="MANIFEST.json must contain a JSON object",
            )
        )
        return

    required_fields = (
        "package_name",
        "version",
        "source_commit",
        "created_from",
        "local_only",
        "distribution_type",
    )
    for field in required_fields:
        if field not in manifest:
            blocked.append(
                Finding(
                    path="MANIFEST.json",
                    category="manifest_field",
                    message=f"required manifest field is missing: {field}",
                )
            )

    package_name = manifest.get("package_name")
    if not _is_safe_package_name(package_name):
        blocked.append(
            Finding(
                path="MANIFEST.json",
                category="manifest_field",
                message="package_name must be non-empty and safe",
            )
        )

    manifest_version = manifest.get("version")
    if not isinstance(manifest_version, str) or not manifest_version:
        blocked.append(
            Finding(
                path="MANIFEST.json",
                category="manifest_field",
                message="version must be a non-empty string",
            )
        )
    elif version is not None and manifest_version != version:
        blocked.append(
            Finding(
                path="MANIFEST.json",
                category="manifest_field",
                message="manifest version must match VERSION.txt",
            )
        )

    source_commit = manifest.get("source_commit")
    if not isinstance(source_commit, str) or not SOURCE_COMMIT_RE.fullmatch(source_commit):
        blocked.append(
            Finding(
                path="MANIFEST.json",
                category="manifest_field",
                message="source_commit must look like a Git SHA",
            )
        )

    created_from = manifest.get("created_from")
    if not _is_nonempty_safe_text(created_from, 256):
        blocked.append(
            Finding(
                path="MANIFEST.json",
                category="manifest_field",
                message="created_from must be a non-empty safe string",
            )
        )

    if manifest.get("local_only") is not True:
        blocked.append(
            Finding(
                path="MANIFEST.json",
                category="manifest_field",
                message="local_only must be true",
            )
        )

    distribution_type = manifest.get("distribution_type")
    if distribution_type not in ALLOWED_DISTRIBUTION_TYPES:
        blocked.append(
            Finding(
                path="MANIFEST.json",
                category="manifest_field",
                message="distribution_type is not allowed",
            )
        )


def _validate_checksum_path(
    path_text: str,
    line_number: int,
    blocked: list[Finding],
) -> PurePosixPath | None:
    if not path_text or path_text != path_text.strip():
        blocked.append(
            Finding(
                path="checksums.sha256",
                category="checksum_path",
                message="checksum path must be a non-empty relative path",
                line=line_number,
            )
        )
        return None
    if "\\" in path_text:
        blocked.append(
            Finding(
                path="checksums.sha256",
                category="checksum_path",
                message="checksum path must not use backslashes",
                line=line_number,
            )
        )
        return None
    if "\x00" in path_text or WINDOWS_DRIVE_RE.match(path_text):
        blocked.append(
            Finding(
                path="checksums.sha256",
                category="checksum_path",
                message="checksum path must not be absolute",
                line=line_number,
            )
        )
        return None

    rel_path = PurePosixPath(path_text)
    if rel_path.is_absolute():
        blocked.append(
            Finding(
                path="checksums.sha256",
                category="checksum_path",
                message="checksum path must not be absolute",
                line=line_number,
            )
        )
        return None
    if ".." in rel_path.parts:
        blocked.append(
            Finding(
                path="checksums.sha256",
                category="checksum_path",
                message="checksum path must not contain ..",
                line=line_number,
            )
        )
        return None
    if not rel_path.parts or rel_path.as_posix() in {".", ""}:
        blocked.append(
            Finding(
                path="checksums.sha256",
                category="checksum_path",
                message="checksum path must name a file",
                line=line_number,
            )
        )
        return None

    return rel_path


def _path_has_symlink_component(root: Path, rel_path: PurePosixPath) -> bool:
    current = root
    for part in rel_path.parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_checksums(
    root: Path,
    blocked: list[Finding],
    warnings: list[Finding],
) -> int:
    path = _require_root_file(root, "checksums.sha256", blocked)
    if path is None:
        return 0

    text = _read_limited_text(
        path,
        "checksums.sha256",
        CHECKSUMS_SIZE_LIMIT_BYTES,
        blocked,
    )
    if text is None:
        return 0

    seen_paths: set[str] = set()
    checksum_entries_checked = 0

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        match = SHA256_LINE_RE.fullmatch(raw_line)
        if match is None:
            blocked.append(
                Finding(
                    path="checksums.sha256",
                    category="checksum_format",
                    message="checksum line must be '<64 hex sha256>  <relative/path>'",
                    line=line_number,
                )
            )
            continue

        expected_hash, path_text = match.groups()
        rel_path = _validate_checksum_path(path_text, line_number, blocked)
        if rel_path is None:
            continue

        normalized_path = rel_path.as_posix()
        if normalized_path in seen_paths:
            blocked.append(
                Finding(
                    path=normalized_path,
                    category="checksum_duplicate",
                    message="duplicate checksum path is listed",
                    line=line_number,
                )
            )
            continue
        seen_paths.add(normalized_path)
        checksum_entries_checked += 1

        listed_file = root.joinpath(*rel_path.parts)
        if _path_has_symlink_component(root, rel_path):
            blocked.append(
                Finding(
                    path=normalized_path,
                    category="checksum_symlink",
                    message="listed file path contains a symlink component",
                    line=line_number,
                )
            )
            continue
        if not listed_file.exists():
            blocked.append(
                Finding(
                    path=normalized_path,
                    category="checksum_missing_file",
                    message="listed file is missing",
                    line=line_number,
                )
            )
            continue
        if not listed_file.is_file():
            blocked.append(
                Finding(
                    path=normalized_path,
                    category="checksum_not_regular",
                    message="listed path is not a regular file",
                    line=line_number,
                )
            )
            continue

        actual_hash = _sha256_file(listed_file)
        if actual_hash.lower() != expected_hash.lower():
            blocked.append(
                Finding(
                    path=normalized_path,
                    category="checksum_mismatch",
                    message="listed file SHA-256 does not match checksums.sha256",
                    line=line_number,
                )
            )

    if not seen_paths:
        blocked.append(
            Finding(
                path="checksums.sha256",
                category="checksum_format",
                message="checksums.sha256 does not contain any file entries",
            )
        )

    _add_unlisted_file_warnings(root, seen_paths, warnings)
    return checksum_entries_checked


def _add_unlisted_file_warnings(
    root: Path,
    listed_paths: set[str],
    warnings: list[Finding],
) -> None:
    def _walk_error(error: OSError) -> None:
        warnings.append(
            Finding(
                path=getattr(error, "filename", ".") or ".",
                category="checksum_extra_file_scan",
                message="could not inspect candidate path for unlisted files",
            )
        )

    for dir_path_text, dir_names, file_names in os.walk(
        root, topdown=True, followlinks=False, onerror=_walk_error
    ):
        dir_path = Path(dir_path_text)
        for dir_name in list(dir_names):
            if (dir_path / dir_name).is_symlink():
                dir_names.remove(dir_name)

        for file_name in file_names:
            file_path = dir_path / file_name
            if file_path.is_symlink() or not file_path.is_file():
                continue
            rel_path = _display_path(file_path, root)
            if rel_path == "checksums.sha256":
                continue
            if rel_path not in listed_paths:
                warnings.append(
                    Finding(
                        path=rel_path,
                        category="checksum_extra_file",
                        message="file is not listed in checksums.sha256",
                    )
                )


def _validate_license_notice(root: Path, name: str, blocked: list[Finding]) -> None:
    path = _require_root_file(root, name, blocked)
    if path is None:
        return

    text = _read_limited_text(path, name, LICENSE_NOTICE_SIZE_LIMIT_BYTES, blocked)
    if text is None:
        return

    if not text.strip():
        blocked.append(
            Finding(
                path=name,
                category="license_notice",
                message="file must not be empty",
            )
        )
    _add_secret_like_findings(text, name, blocked)


def scan_candidate(candidate_dir: Path | str) -> CheckResult:
    """Inspect a distribution candidate and return a sanitized report object."""
    candidate = Path(candidate_dir)
    clean_result = scan_clean_candidate(candidate)
    blocked = [_finding_from_clean(finding) for finding in clean_result.blocked]
    warnings = [_finding_from_clean(finding) for finding in clean_result.warnings]
    metadata_files_checked = 0
    checksum_entries_checked = 0

    if candidate.is_symlink() or not candidate.exists() or not candidate.is_dir():
        status = "OK" if not blocked else "BLOCKED"
        return CheckResult(
            candidate=str(candidate),
            status=status,
            blocked=tuple(blocked),
            warnings=tuple(warnings),
            metadata_files_checked=metadata_files_checked,
            checksum_entries_checked=checksum_entries_checked,
        )

    for name in REQUIRED_METADATA_FILES:
        if (candidate / name).exists() and (candidate / name).is_file():
            metadata_files_checked += 1

    version = _validate_version(candidate, blocked)
    _validate_manifest(candidate, version, blocked)
    checksum_entries_checked = _validate_checksums(candidate, blocked, warnings)
    _validate_license_notice(candidate, "LICENSE", blocked)
    _validate_license_notice(candidate, "NOTICE", blocked)

    status = "OK" if not blocked else "BLOCKED"
    return CheckResult(
        candidate=str(candidate),
        status=status,
        blocked=tuple(blocked),
        warnings=tuple(warnings),
        metadata_files_checked=metadata_files_checked,
        checksum_entries_checked=checksum_entries_checked,
    )


def _format_findings(findings: Iterable[Finding]) -> list[str]:
    lines: list[str] = []
    for finding in findings:
        suffix = ""
        if finding.pattern_family:
            suffix += f" [{finding.pattern_family}]"
        if finding.line is not None:
            suffix += f" (line {finding.line})"
        lines.append(f"- {finding.path}: {finding.message}{suffix}")
    return lines


def format_text_report(result: CheckResult) -> str:
    lines = [
        "CLEAN Distribution Metadata Check",
        f"Candidate: {result.candidate}",
        f"Status: {result.status}",
        f"Blocked findings: {len(result.blocked)}",
        f"Warnings: {len(result.warnings)}",
        f"Metadata files checked: {result.metadata_files_checked}",
        f"Checksum entries checked: {result.checksum_entries_checked}",
        "",
    ]
    if result.blocked:
        lines.append("Blocked findings:")
        lines.extend(_format_findings(result.blocked))
        lines.append("")
    if result.warnings:
        lines.append("Warnings:")
        lines.extend(_format_findings(result.warnings))
        lines.append("")
    if not result.blocked:
        lines.append("No blocked findings were found.")
    return "\n".join(lines).rstrip() + "\n"


def format_markdown_report(result: CheckResult) -> str:
    lines = [
        "# CLEAN Distribution Metadata Check",
        "",
        f"- Candidate: `{result.candidate}`",
        f"- Status: `{result.status}`",
        f"- Blocked findings: `{len(result.blocked)}`",
        f"- Warnings: `{len(result.warnings)}`",
        f"- Metadata files checked: `{result.metadata_files_checked}`",
        f"- Checksum entries checked: `{result.checksum_entries_checked}`",
        "",
    ]
    if result.blocked:
        lines.append("## Blocked Findings")
        lines.extend(_format_findings(result.blocked))
        lines.append("")
    if result.warnings:
        lines.append("## Warnings")
        lines.extend(_format_findings(result.warnings))
        lines.append("")
    if not result.blocked:
        lines.append("No blocked findings were found.")
    return "\n".join(lines).rstrip() + "\n"


def format_json_report(result: CheckResult) -> str:
    return json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n"


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report-only metadata checker for CLEAN portable distribution candidates."
    )
    parser.add_argument("candidate_dir", help="Candidate directory to inspect.")
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("--json", action="store_true", help="Print JSON report.")
    output_group.add_argument("--markdown", action="store_true", help="Print Markdown report.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    result = scan_candidate(args.candidate_dir)

    if args.json:
        print(format_json_report(result), end="")
    elif args.markdown:
        print(format_markdown_report(result), end="")
    else:
        print(format_text_report(result), end="")

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
