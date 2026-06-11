#!/usr/bin/env python3
"""Report-only checker for future CLEAN portable distribution candidates.

The checker inspects only the candidate directory provided on the command line.
It does not create, modify, delete, copy, zip, package, install, or download
anything.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SCAN_SIZE_LIMIT_BYTES = 1_000_000

TEXT_SUFFIXES = {
    ".txt",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".py",
    ".js",
    ".ts",
    ".html",
    ".css",
}

FORBIDDEN_DIR_NAMES = {
    ".git",
    "logs",
    "state",
    "downloads",
    "download",
    "audio_download",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".vscode",
    ".idea",
}

FORBIDDEN_EXACT_FILE_NAMES = {
    ".gitignore",
    ".env",
    "cookies.txt",
    "cookie.txt",
    ".ds_store",
    "thumbs.db",
}

FORBIDDEN_SUFFIXES = {
    ".sqlite",
    ".sqlite3",
    ".db",
    ".log",
    ".pem",
    ".key",
    ".crt",
    ".p12",
    ".pfx",
    ".token",
    ".secret",
    ".bak",
    ".tmp",
    ".swp",
}

SENSITIVE_NAME_FRAGMENTS = (
    "cookie",
    "token",
    "secret",
    "credential",
    "password",
    "session",
)

SECRET_PATTERNS = [
    (
        "AWS access key-like",
        re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ),
    (
        "GitHub token-like",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    ),
    (
        "Bearer token-like",
        re.compile(r"(?i)\bauthorization\s*:\s*bearer\s+[A-Za-z0-9._~+/=-]{3,}"),
    ),
    (
        "Cookie header-like",
        re.compile(r"(?i)^\s*cookie\s*:\s*\S+"),
    ),
    (
        "Set-Cookie header-like",
        re.compile(r"(?i)^\s*set-cookie\s*:\s*\S+"),
    ),
    (
        "password assignment-like",
        re.compile(r"(?i)\bpassword\b\s*[:=]\s*['\"]?[^'\"\s#;]{3,}"),
    ),
    (
        "secret assignment-like",
        re.compile(r"(?i)\bsecret\b\s*[:=]\s*['\"]?[^'\"\s#;]{6,}"),
    ),
    (
        "api key assignment-like",
        re.compile(r"(?i)\b(?:api[_-]?key|apikey)\b\s*[:=]\s*['\"]?[^'\"\s#;]{8,}"),
    ),
    (
        "private key header",
        re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    ),
]


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
    checked_entries: int = 0
    scanned_text_files: int = 0
    skipped_large_files: int = 0
    skipped_non_text_files: int = 0

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
                "checked_entries": self.checked_entries,
                "scanned_text_files": self.scanned_text_files,
                "skipped_large_files": self.skipped_large_files,
                "skipped_non_text_files": self.skipped_non_text_files,
            },
        }


def _display_path(path: Path, root: Path, *, is_dir: bool = False) -> str:
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = Path(path.name)
    text = rel.as_posix() or "."
    if is_dir and text != "." and not text.endswith("/"):
        return f"{text}/"
    return text


def _is_repo_root(path: Path) -> bool:
    try:
        return path.resolve() == Path(__file__).resolve().parents[1]
    except OSError:
        return False


def _forbidden_path_findings(path: Path, rel_path: str, *, is_dir: bool) -> list[Finding]:
    findings: list[Finding] = []
    name_lower = path.name.lower()

    if is_dir and name_lower in FORBIDDEN_DIR_NAMES:
        findings.append(
            Finding(
                path=rel_path,
                category="forbidden_path",
                message="forbidden directory is present",
            )
        )
        return findings

    if not is_dir:
        if name_lower in FORBIDDEN_EXACT_FILE_NAMES:
            findings.append(
                Finding(
                    path=rel_path,
                    category="forbidden_path",
                    message="forbidden file is present",
                )
            )
        if name_lower.startswith(".env."):
            findings.append(
                Finding(
                    path=rel_path,
                    category="forbidden_path",
                    message="forbidden .env.* file is present",
                )
            )
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(
                Finding(
                    path=rel_path,
                    category="forbidden_path",
                    message="forbidden file extension is present",
                )
            )

    if any(fragment in name_lower for fragment in SENSITIVE_NAME_FRAGMENTS):
        findings.append(
            Finding(
                path=rel_path,
                category="sensitive_filename",
                message="obvious sensitive filename is present",
            )
        )

    return findings


def _content_findings(path: Path, rel_path: str) -> tuple[list[Finding], list[Finding], bool, bool]:
    warnings: list[Finding] = []
    blocked: list[Finding] = []

    try:
        stat_result = path.stat()
    except OSError:
        blocked.append(
            Finding(
                path=rel_path,
                category="read_error",
                message="could not stat file for content scan",
            )
        )
        return blocked, warnings, False, False

    if stat_result.st_size > SCAN_SIZE_LIMIT_BYTES:
        warnings.append(
            Finding(
                path=rel_path,
                category="content_scan_skipped",
                message="file is over the safe content scan size limit",
            )
        )
        return blocked, warnings, False, True

    if path.suffix.lower() not in TEXT_SUFFIXES:
        return blocked, warnings, False, False

    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        blocked.append(
            Finding(
                path=rel_path,
                category="read_error",
                message="could not read text file for content scan",
            )
        )
        return blocked, warnings, False, False

    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern_family, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                blocked.append(
                    Finding(
                        path=rel_path,
                        category="forbidden_content",
                        message="secret-like content pattern found",
                        pattern_family=pattern_family,
                        line=line_number,
                    )
                )
    return blocked, warnings, True, False


def scan_candidate(candidate_dir: Path | str) -> CheckResult:
    """Inspect a candidate directory and return a sanitized report object."""
    candidate = Path(candidate_dir)
    blocked: list[Finding] = []
    warnings: list[Finding] = []
    checked_entries = 0
    scanned_text_files = 0
    skipped_large_files = 0
    skipped_non_text_files = 0

    if not candidate.exists():
        blocked.append(
            Finding(
                path=".",
                category="candidate",
                message="candidate path does not exist",
            )
        )
        return CheckResult(str(candidate), "BLOCKED", tuple(blocked), tuple(warnings))

    if candidate.is_symlink():
        blocked.append(
            Finding(
                path=".",
                category="symlink",
                message="candidate path is a symlink and was not followed",
            )
        )
        return CheckResult(str(candidate), "BLOCKED", tuple(blocked), tuple(warnings))

    if not candidate.is_dir():
        blocked.append(
            Finding(
                path=".",
                category="candidate",
                message="candidate path is not a directory",
            )
        )
        return CheckResult(str(candidate), "BLOCKED", tuple(blocked), tuple(warnings))

    if _is_repo_root(candidate):
        warnings.append(
            Finding(
                path=".",
                category="candidate",
                message="repository root is not a finished CLEAN distribution candidate",
            )
        )

    def _walk_error(error: OSError) -> None:
        blocked.append(
            Finding(
                path=getattr(error, "filename", ".") or ".",
                category="walk_error",
                message="could not inspect candidate path",
            )
        )

    for dir_path_text, dir_names, file_names in os.walk(
        candidate, topdown=True, followlinks=False, onerror=_walk_error
    ):
        dir_path = Path(dir_path_text)

        for dir_name in list(dir_names):
            dir_path_child = dir_path / dir_name
            rel_path = _display_path(dir_path_child, candidate, is_dir=True)
            checked_entries += 1

            if dir_path_child.is_symlink():
                blocked.append(
                    Finding(
                        path=rel_path,
                        category="symlink",
                        message="symlink is present and was not followed",
                    )
                )
                dir_names.remove(dir_name)
                continue

            findings = _forbidden_path_findings(dir_path_child, rel_path, is_dir=True)
            blocked.extend(findings)
            if findings:
                dir_names.remove(dir_name)

        for file_name in file_names:
            file_path = dir_path / file_name
            rel_path = _display_path(file_path, candidate)
            checked_entries += 1

            if file_path.is_symlink():
                blocked.append(
                    Finding(
                        path=rel_path,
                        category="symlink",
                        message="symlink is present and was not followed",
                    )
                )
                continue

            findings = _forbidden_path_findings(file_path, rel_path, is_dir=False)
            blocked.extend(findings)
            if findings:
                continue

            content_blocked, content_warnings, did_scan, skipped_large = _content_findings(
                file_path, rel_path
            )
            blocked.extend(content_blocked)
            warnings.extend(content_warnings)
            if did_scan:
                scanned_text_files += 1
            elif skipped_large:
                skipped_large_files += 1
            else:
                skipped_non_text_files += 1

    status = "OK" if not blocked else "BLOCKED"
    return CheckResult(
        candidate=str(candidate),
        status=status,
        blocked=tuple(blocked),
        warnings=tuple(warnings),
        checked_entries=checked_entries,
        scanned_text_files=scanned_text_files,
        skipped_large_files=skipped_large_files,
        skipped_non_text_files=skipped_non_text_files,
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
        "CLEAN Distribution Candidate Check",
        f"Candidate: {result.candidate}",
        f"Status: {result.status}",
        f"Blocked findings: {len(result.blocked)}",
        f"Warnings: {len(result.warnings)}",
        f"Checked entries: {result.checked_entries}",
        f"Scanned text files: {result.scanned_text_files}",
        f"Skipped large files: {result.skipped_large_files}",
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
        "# CLEAN Distribution Candidate Check",
        "",
        f"- Candidate: `{result.candidate}`",
        f"- Status: `{result.status}`",
        f"- Blocked findings: `{len(result.blocked)}`",
        f"- Warnings: `{len(result.warnings)}`",
        f"- Checked entries: `{result.checked_entries}`",
        f"- Scanned text files: `{result.scanned_text_files}`",
        f"- Skipped large files: `{result.skipped_large_files}`",
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
        description="Report-only checker for CLEAN portable distribution candidates."
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
