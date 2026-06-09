#!/usr/bin/env python3
"""Report-only repository safety gate for low/mid-risk Codex work.

This script inspects repository diffs and prints a sanitized safety report. It
does not create, modify, delete, move, copy, package, install, pull, or update
files.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


GENERATED_PACKAGE_ROOT = "動画保存ツール_ローカル専用/"

REQUIRED_LLMWIKI_DOCS = [
    "docs/llmwiki/current-state.md",
    "docs/llmwiki/roadmap.md",
    "docs/llmwiki/handoff.md",
]

PACKAGE_GUIDE_DIR = "docs/llmwiki/package-guides/"
PACKAGE_NOTICE_DIR = "docs/llmwiki/package-notices/"

NOTICE_SOURCE_CANDIDATES = [
    ("yt-dlp", "docs/llmwiki/package-notices/yt-dlp-notice.source.md"),
    ("ffmpeg", "docs/llmwiki/package-notices/ffmpeg-notice.source.md"),
    ("python-runtime", "docs/llmwiki/package-notices/python-runtime-notice.source.md"),
    (
        "frontend-dependencies",
        "docs/llmwiki/package-notices/frontend-dependencies-notice.source.md",
    ),
]

FORBIDDEN_PATH_RULES = [
    ".env",
    ".env.",
    "cookies.txt",
    ".pytest_cache/",
    "node_modules/",
    "ui/node_modules/",
    "downloads/",
    "state/",
    "logs/",
    GENERATED_PACKAGE_ROOT,
]

PR_1001_LEAKAGE_PATHS = {
    "docker-compose.local.yml",
    "docs/local-only.md",
}

BLOCKED_SCOPE_RULES = [
    ("docker", re.compile(r"(^|/)Dockerfile$|(^|/)docker-compose[^/]*\.ya?ml$")),
    ("ci", re.compile(r"^\.github/")),
    ("package_or_lockfile", re.compile(r"(^|/)(package\.json|package-lock\.json|pnpm-lock\.yaml|uv\.lock)$")),
    ("package_or_lockfile", re.compile(r"(^|/)(pyproject\.toml|requirements[^/]*\.txt)$")),
]

SOURCE_SCOPE_PREFIXES = [
    ("backend", "app/"),
    ("frontend", "ui/"),
]

TEXT_SUFFIXES = {
    "",
    ".bat",
    ".command",
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".scss",
    ".sh",
    ".toml",
    ".ts",
    ".txt",
    ".yaml",
    ".yml",
}

SECRET_PATTERNS = [
    (
        "private_key_block",
        re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    ),
    (
        "env_style_secret_value",
        re.compile(
            r"^\s*[A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|PASSWD|API_KEY|"
            r"COOKIE|CREDENTIAL)[A-Z0-9_]*\s*=\s*['\"]?"
            r"[A-Za-z0-9_./+=:@~$%!-]{16,}"
        ),
    ),
    (
        "token_like_long_value",
        re.compile(
            r"(?i)\b(?:token|auth|session|key)\b\s*[:=]\s*['\"]?"
            r"[A-Za-z0-9_./+=:@~$%!-]{24,}"
        ),
    ),
    (
        "cookie_like_line",
        re.compile(r"(?i)(?:^|\s)(?:cookie|set-cookie)\s*[:=]\s*[^;\s]{12,}"),
    ),
]

DANGEROUS_COMMAND_PATTERNS = [
    ("docker_pull", ("docker", "pull")),
    ("git_pull", ("git", "pull")),
    ("git_merge", ("git", "merge")),
    ("git_rebase", ("git", "rebase")),
    ("pip_install", ("pip", "install")),
    ("npm_install", ("npm", "install")),
    ("pnpm_add", ("pnpm", "add")),
]

DANGEROUS_TEXT_PATTERNS = [
    ("restart", re.compile(r"(?i)\brestart\b")),
    ("update_apply", re.compile(r"(?i)\bupdate\s+apply\b")),
    ("backup_create", re.compile(r"(?i)\bbackup\s+create\b")),
    ("rollback_create", re.compile(r"(?i)\brollback\s+create\b")),
    (
        "public_host_url",
        re.compile(r"(?i)\b" + "_".join(["PUBLIC", "HOST", "URL"]) + r"\b"),
    ),
    (
        "cors_wildcard",
        re.compile(r"(?i)\bCORS_ALLOWED_ORIGINS\s*=\s*\*"),
    ),
    (
        "download_dirs_indexable",
        re.compile(r"(?i)\bDOWNLOAD_DIRS_INDEXABLE\s*=\s*true\b"),
    ),
    (
        "allow_ytdl_options_overrides",
        re.compile(r"(?i)\bALLOW_YTDL_OPTIONS_OVERRIDES\s*=\s*true\b"),
    ),
]


@dataclass(frozen=True)
class Finding:
    path: str
    message: str
    line: int | None = None
    pattern_family: str | None = None


@dataclass(frozen=True)
class GitResult:
    returncode: int
    stdout: str
    stderr: str


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Print a report-only repository safety check. The script only reads "
            "repository metadata and changed text."
        )
    )
    parser.add_argument(
        "--base",
        help=(
            "Optional base ref for committed branch diffs, for example "
            "fork/master. Working tree changes are still included."
        ),
    )
    return parser.parse_args(argv)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run_git(root: Path, args: list[str]) -> GitResult:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            text=True,
        )
    except OSError as exc:
        return GitResult(2, "", str(exc))
    return GitResult(result.returncode, result.stdout, result.stderr)


def git_lines(root: Path, args: list[str]) -> tuple[list[str], str | None]:
    result = run_git(root, args)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "git command failed"
        return [], message
    return [line.strip() for line in result.stdout.splitlines() if line.strip()], None


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip().strip('"')


def dedupe(paths: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for path in paths:
        normalized = normalize_path(path)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def changed_files(root: Path, base: str | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    paths: list[str] = []

    if base:
        base_paths, error = git_lines(root, ["diff", "--name-only", f"{base}...HEAD"])
        if error:
            errors.append(f"base diff failed for {base}: {error}")
        paths.extend(base_paths)

    head_paths, error = git_lines(root, ["diff", "--name-only", "HEAD"])
    if error:
        errors.append(f"working tree diff failed: {error}")
    paths.extend(head_paths)

    untracked_paths, error = git_lines(root, ["ls-files", "--others", "--exclude-standard"])
    if error:
        errors.append(f"untracked file scan failed: {error}")
    paths.extend(untracked_paths)

    return dedupe(paths), errors


def diff_lines_for_file(root: Path, path: str, base: str | None) -> list[tuple[int, str]]:
    file_path = root / path
    if path and file_path.is_file() and path in set(git_lines(root, ["ls-files", "--others", "--exclude-standard"])[0]):
        return whole_file_lines(file_path)

    args = ["diff", "--unified=0"]
    if base:
        args.extend([f"{base}...HEAD", "--", path])
    else:
        args.extend(["HEAD", "--", path])

    result = run_git(root, args)
    if result.returncode != 0:
        return whole_file_lines(file_path) if file_path.is_file() else []
    return parse_added_diff_lines(result.stdout)


def parse_added_diff_lines(diff_text: str) -> list[tuple[int, str]]:
    added: list[tuple[int, str]] = []
    new_line = 0
    for line in diff_text.splitlines():
        if line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", line)
            if match:
                new_line = int(match.group(1))
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            added.append((new_line, line[1:]))
            new_line += 1
        elif line.startswith("-"):
            continue
        else:
            if new_line:
                new_line += 1
    return added


def whole_file_lines(path: Path) -> list[tuple[int, str]]:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            return [(number, line.rstrip("\n")) for number, line in enumerate(handle, start=1)]
    except OSError:
        return []


def is_text_path(path: str) -> bool:
    return Path(path).suffix.lower() in TEXT_SUFFIXES


def classify_scope(paths: list[str]) -> str:
    if not paths:
        return "none"
    if all(path.startswith("docs/") for path in paths):
        return "docs-only"
    if all(path.startswith("scripts/") for path in paths):
        return "scripts-only"
    if all(path.startswith(("app/", "ui/")) for path in paths):
        return "source-only"
    return "mixed"


def check_scope(paths: list[str]) -> tuple[list[Finding], list[Finding]]:
    warnings: list[Finding] = []
    blocked: list[Finding] = []

    for path in paths:
        for family, prefix in SOURCE_SCOPE_PREFIXES:
            if path.startswith(prefix):
                warnings.append(
                    Finding(
                        path=path,
                        pattern_family=family,
                        message=(
                            "Source change is present; verify this task explicitly "
                            "approves backend/frontend work."
                        ),
                    )
                )
        for family, pattern in BLOCKED_SCOPE_RULES:
            if pattern.search(path):
                blocked.append(
                    Finding(
                        path=path,
                        pattern_family=family,
                        message="Blocked scope family is present in changed files.",
                    )
                )

    return blocked, warnings


def path_matches_forbidden_rule(path: str, rule: str) -> bool:
    if rule.endswith("/"):
        return path == rule.rstrip("/") or path.startswith(rule)
    if rule.endswith("."):
        return path.startswith(rule)
    return path == rule or path.startswith(rule + "/")


def check_forbidden_paths(paths: list[str]) -> list[Finding]:
    blocked: list[Finding] = []
    for path in paths:
        for rule in FORBIDDEN_PATH_RULES:
            if path_matches_forbidden_rule(path, rule):
                blocked.append(
                    Finding(
                        path=path,
                        pattern_family=rule.rstrip("/"),
                        message="Forbidden path is present in changed files.",
                    )
                )
    return blocked


def check_generated_folder(root: Path, paths: list[str]) -> list[Finding]:
    blocked: list[Finding] = []
    if (root / GENERATED_PACKAGE_ROOT.rstrip("/")).exists():
        blocked.append(
            Finding(
                path=GENERATED_PACKAGE_ROOT,
                message="Generated distribution folder exists in the repository root.",
            )
        )
    for path in paths:
        if path_matches_forbidden_rule(path, GENERATED_PACKAGE_ROOT):
            blocked.append(
                Finding(
                    path=path,
                    message="Changed file is inside the generated distribution folder.",
                )
            )
    return blocked


def check_pr_1001(paths: list[str]) -> list[Finding]:
    return [
        Finding(
            path=path,
            message="Upstream PR #1001 file is present in the changed file list.",
        )
        for path in paths
        if path in PR_1001_LEAKAGE_PATHS
    ]


def scan_secret_like(
    root: Path,
    paths: list[str],
    base: str | None,
) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        if not is_text_path(path):
            continue
        for line_number, line in diff_lines_for_file(root, path, base):
            for family, pattern in SECRET_PATTERNS:
                if family == "token_like_long_value" and is_safety_prose(path, line):
                    continue
                if pattern.search(line):
                    findings.append(
                        Finding(
                            path=path,
                            line=line_number,
                            pattern_family=family,
                            message=(
                                "Secret-like content detected. The matched value "
                                "is intentionally omitted."
                            ),
                        )
                    )
    return findings


def command_pattern_regex(command_parts: tuple[str, str]) -> re.Pattern[str]:
    first, second = command_parts
    return re.compile(r"(?i)\b" + re.escape(first) + r"\s+" + re.escape(second) + r"\b")


def scan_dangerous_behavior(
    root: Path,
    paths: list[str],
    base: str | None,
) -> list[Finding]:
    findings: list[Finding] = []
    command_patterns = [
        (family, command_pattern_regex(parts)) for family, parts in DANGEROUS_COMMAND_PATTERNS
    ]
    patterns = command_patterns + DANGEROUS_TEXT_PATTERNS

    for path in paths:
        if not is_text_path(path):
            continue
        for line_number, line in diff_lines_for_file(root, path, base):
            if is_safety_prose(path, line) or is_checker_pattern_definition(path, line):
                continue
            for family, pattern in patterns:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            path=path,
                            line=line_number,
                            pattern_family=family,
                            message="Dangerous behavior pattern detected in changed text.",
                        )
                    )
    return findings


def is_safety_prose(path: str, line: str) -> bool:
    if not path.startswith("docs/llmwiki/"):
        return False
    lowered = line.lower()
    safety_words = [
        "no ",
        "not ",
        "must not",
        "blocked",
        "prohibited",
        "out of scope",
        "does not",
        "do not",
        "禁止",
        "未実装",
    ]
    return any(word in lowered for word in safety_words)


def is_checker_pattern_definition(path: str, line: str) -> bool:
    if path != "scripts/check_repo_safety.py":
        return False
    markers = [
        "DANGEROUS_",
        "SECRET_PATTERNS",
        "FORBIDDEN_PATH_RULES",
        "PR_1001_LEAKAGE_PATHS",
        "pattern_family",
        "re.compile(",
    ]
    stripped = line.lstrip()
    return (
        any(marker in line for marker in markers)
        or stripped.startswith('("')
        or stripped.startswith('"')
    )


def check_llmwiki_basics(root: Path) -> list[Finding]:
    blocked: list[Finding] = []
    for rel in REQUIRED_LLMWIKI_DOCS:
        if not (root / rel).is_file():
            blocked.append(
                Finding(
                    path=rel,
                    message="Required LLMwiki source-of-truth document is missing.",
                )
            )
    return blocked


def check_package_sources(root: Path) -> list[Finding]:
    warnings: list[Finding] = []
    if not (root / PACKAGE_GUIDE_DIR.rstrip("/")).is_dir():
        warnings.append(
            Finding(path=PACKAGE_GUIDE_DIR, message="Package guide source directory is missing.")
        )
    if not (root / PACKAGE_NOTICE_DIR.rstrip("/")).is_dir():
        warnings.append(
            Finding(path=PACKAGE_NOTICE_DIR, message="Package notice source directory is missing.")
        )
    for label, rel in NOTICE_SOURCE_CANDIDATES:
        if not (root / rel).is_file():
            warnings.append(
                Finding(path=rel, message=f"Notice source missing: {label}.")
            )
    return warnings


def format_finding(finding: Finding) -> str:
    parts = [finding.path]
    if finding.line is not None:
        parts.append(f"line {finding.line}")
    if finding.pattern_family:
        parts.append(f"family={finding.pattern_family}")
    return f"{' | '.join(parts)}: {finding.message}"


def print_findings(title: str, findings: list[Finding]) -> None:
    print(f"{title}:")
    if not findings:
        print("  none")
        return
    for finding in findings:
        print(f"  - {format_finding(finding)}")


def print_changed_files(paths: list[str]) -> None:
    print("Changed files:")
    if not paths:
        print("  none")
        return
    for path in paths:
        print(f"  {path}")


def print_checks(checks: list[tuple[str, str]]) -> None:
    print("Checks:")
    for name, status in checks:
        print(f"  {name}: {status}")


def status_from_blockers(blocked: list[Finding]) -> str:
    return "BLOCKED" if blocked else "OK"


def check_status(findings: list[Finding]) -> str:
    return "BLOCKED" if findings else "OK"


def warning_status(findings: list[Finding]) -> str:
    return "warning" if findings else "OK"


def git_value(root: Path, args: list[str]) -> str:
    result = run_git(root, args)
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip() or "unknown"


def build_report(root: Path, base: str | None) -> tuple[int, str]:
    paths, diff_errors = changed_files(root, base)
    scope = classify_scope(paths)

    scope_blocked, scope_warnings = check_scope(paths)
    forbidden_path_blocked = check_forbidden_paths(paths)
    generated_blocked = check_generated_folder(root, paths)
    pr_1001_blocked = check_pr_1001(paths)
    secret_blocked = scan_secret_like(root, paths, base)
    dangerous_blocked = scan_dangerous_behavior(root, paths, base)
    llmwiki_blocked = check_llmwiki_basics(root)
    package_warnings = check_package_sources(root)

    usage_findings = [Finding(path=".", message=error) for error in diff_errors]
    blocked = (
        usage_findings
        + scope_blocked
        + forbidden_path_blocked
        + generated_blocked
        + pr_1001_blocked
        + secret_blocked
        + dangerous_blocked
        + llmwiki_blocked
    )
    warnings = scope_warnings + package_warnings

    checks = [
        ("changed files scope", check_status(scope_blocked)),
        ("forbidden paths", check_status(forbidden_path_blocked)),
        ("generated distribution folder", check_status(generated_blocked)),
        ("PR #1001 leakage", check_status(pr_1001_blocked)),
        ("secret-like content", check_status(secret_blocked)),
        ("dangerous behavior", check_status(dangerous_blocked)),
        ("LLMwiki basics", check_status(llmwiki_blocked)),
        ("package guide / notice sources", warning_status(package_warnings)),
    ]

    lines: list[str] = []
    lines.append("Repo safety check report")
    lines.append("")
    lines.append(f"Status: {status_from_blockers(blocked)}")
    lines.append("")
    lines.append("Repository:")
    lines.append(f"  branch: {git_value(root, ['branch', '--show-current'])}")
    lines.append(f"  commit: {git_value(root, ['rev-parse', '--short', 'HEAD'])}")
    lines.append(f"  base: {base or 'working tree vs HEAD'}")
    lines.append("")
    lines.append("Scope:")
    lines.append(f"  {scope}")
    lines.append("")
    lines.append("Changed files:")
    if paths:
        lines.extend(f"  {path}" for path in paths)
    else:
        lines.append("  none")
    lines.append("")
    lines.append("Warnings:")
    if warnings:
        lines.extend(f"  - {format_finding(finding)}" for finding in warnings)
    else:
        lines.append("  none")
    lines.append("")
    lines.append("Blocked:")
    if blocked:
        lines.extend(f"  - {format_finding(finding)}" for finding in blocked)
    else:
        lines.append("  none")
    lines.append("")
    lines.append("Checks:")
    lines.extend(f"  {name}: {status}" for name, status in checks)
    lines.append("")
    lines.append("Safety:")
    lines.append("  report-only: true")
    lines.append("  generated_folder_created: false")
    lines.append("  secret_values_printed: false")

    return (1 if blocked else 0), "\n".join(lines)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0

    root = repo_root()
    exit_code, report = build_report(root, args.base)
    print(report)
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
