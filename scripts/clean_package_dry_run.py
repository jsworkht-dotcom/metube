#!/usr/bin/env python3
"""Report-only dry-run for the future beginner clean package.

This script intentionally does not create, copy, move, zip, or package files.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable


PACKAGE_ROOT = "動画保存ツール_ローカル専用/"

PLANNED_TOP_LEVEL_ENTRIES = [
    "00_最初に開いてください.html",
    "00_最初に開いてください.txt",
    "Windows用/",
    "Mac用/",
    "保存先/",
    "困ったとき/",
    "開発者向け/",
]

PLANNED_WINDOWS_ENTRIES = [
    "Windows用/動画保存ツール.exe",
    "Windows用/予備_起動する.bat",
    "Windows用/予備_停止する.bat",
    "Windows用/予備_保存先を開く.bat",
]

PLANNED_MAC_ENTRIES = [
    "Mac用/動画保存ツール.app",
    "Mac用/予備_起動する.command",
    "Mac用/予備_停止する.command",
    "Mac用/予備_保存先を開く.command",
]

PLANNED_DEVELOPER_ENTRIES = [
    "開発者向け/README.md",
    "開発者向け/docs/",
    "開発者向け/docs/llmwiki/",
    "開発者向け/licenses/",
    "開発者向け/notices/",
    "開発者向け/manifest/planned-output-manifest.json",
]

GUIDE_SOURCE_CANDIDATES = [
    (
        "00_最初に開いてください.html",
        "docs/llmwiki/package-guides/00-first-open.html.source.md",
    ),
    (
        "00_最初に開いてください.txt",
        "docs/llmwiki/package-guides/00-first-open.txt.source.md",
    ),
    (
        "03_使い方.html",
        "docs/llmwiki/package-guides/03-how-to-use.html.source.md",
    ),
    (
        "03_使い方.txt",
        "docs/llmwiki/package-guides/03-how-to-use.txt.source.md",
    ),
    (
        "04_困ったとき.html",
        "docs/llmwiki/package-guides/04-troubleshooting.html.source.md",
    ),
    (
        "04_困ったとき.txt",
        "docs/llmwiki/package-guides/04-troubleshooting.txt.source.md",
    ),
    (
        "05_安全な使い方.html",
        "docs/llmwiki/package-guides/05-safe-use.html.source.md",
    ),
]

NOTICE_SOURCE_CANDIDATES = [
    (
        "MeTube notice candidate",
        "docs/llmwiki/package-notices/metube-notice.source.md",
    ),
    (
        "yt-dlp notice candidate",
        "docs/llmwiki/package-notices/yt-dlp-notice.source.md",
    ),
    (
        "FFmpeg notice candidate",
        "docs/llmwiki/package-notices/ffmpeg-notice.source.md",
    ),
    (
        "Python/runtime notice candidate",
        "docs/llmwiki/package-notices/python-runtime-notice.source.md",
    ),
    (
        "frontend dependency notice candidate",
        "docs/llmwiki/package-notices/frontend-deps-notice.source.md",
    ),
    (
        "future Tauri/Electron notice candidate",
        "docs/llmwiki/package-notices/desktop-shell-notice.source.md",
    ),
]

MANIFEST_PREVIEW_NOTICE_SOURCES = NOTICE_SOURCE_CANDIDATES + [
    (
        "bundled Python dependency inventory candidate",
        "docs/llmwiki/package-notices/bundled-python-dependency-inventory.source.md",
    ),
    (
        "notice source index candidate",
        "docs/llmwiki/package-notices/notice-source-index.source.md",
    ),
]

MANIFEST_PREVIEW_FUTURE_OUTPUTS = [
    "NOTICE.txt",
    "LICENSES/",
    "manifest.json",
    "beginner guide notice section",
]

DIFF_PREDICTION_CREATE_DIRECTORIES = [
    "Windows用/",
    "Mac用/",
    "保存先/",
    "困ったとき/",
    "開発者向け/",
    "LICENSES/",
]

DIFF_PREDICTION_CREATE_FILES = [
    "NOTICE.txt",
    "manifest.json",
    "00_最初に開いてください.html",
    "00_最初に開いてください.txt",
]

DIFF_PREDICTION_COPY_SOURCE_GROUPS = [
    "beginner guide sources",
    "notice source materials",
    "developer review checklist sources",
]

SAFETY_NOTICE_SOURCE_CANDIDATES = [
    (
        "local-only safety notice source",
        "docs/llmwiki/package-guides/00-first-open.html.source.md",
    ),
    (
        "local-only TXT safety notice source",
        "docs/llmwiki/package-guides/00-first-open.txt.source.md",
    ),
    (
        "safe-use boundary source",
        "docs/llmwiki/package-guides/05-safe-use.html.source.md",
    ),
]

PLATFORM_SECTION_SOURCE_CANDIDATES = [
    (
        "Windows section source",
        "docs/llmwiki/package-guides/00-first-open.html.source.md",
    ),
    (
        "macOS section source",
        "docs/llmwiki/package-guides/00-first-open.html.source.md",
    ),
]

REQUIRED_CONTRACT_DOCS = [
    "docs/llmwiki/current-state.md",
    "docs/llmwiki/roadmap.md",
    "docs/llmwiki/handoff.md",
    "docs/llmwiki/safety-boundaries.md",
    "docs/llmwiki/desktop-package-manifest.md",
    "docs/llmwiki/beginner-guide-skeleton.md",
    "docs/llmwiki/beginner-guide-source-plan.md",
    "docs/llmwiki/license-notice-plan.md",
    "docs/llmwiki/clean-package-dry-run-contract.md",
    "docs/llmwiki/clean-package-generator-contract-addendum.md",
]

EXCLUDED_PATHS = [
    ".git/",
    ".github/",
    ".pytest_cache/",
    ".ruff_cache/",
    ".mypy_cache/",
    ".coverage",
    "node_modules/",
    "ui/node_modules/",
    "ui/.angular/",
    "dist/",
    "build/",
    "coverage/",
    ".turbo/",
    ".cache/",
    "downloads/",
    "state/",
    "logs/",
    "temp/",
    ".env",
    ".env.*",
    "cookies.txt",
    "動画保存ツール_ローカル専用/",
]

PR_1001_LEAKAGE_PATHS = [
    "docker-compose.local.yml",
    "docs/local-only.md",
]

FORBIDDEN_NAME_FRAGMENTS = [
    "cookie",
    "token",
    "secret",
    "credential",
    "password",
]

FORBIDDEN_SUFFIXES = [
    ".pem",
    ".key",
    ".p12",
    ".pfx",
]

AMBIGUOUS_BACKUP_FRAGMENTS = [
    "backup",
    "old",
    "copy",
    "tmp",
]

TEXT_SUFFIXES = {
    ".bat",
    ".command",
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".scss",
    ".txt",
    ".toml",
    ".ts",
    ".yaml",
    ".yml",
}

TEXT_SCAN_ROOTS = [
    "app",
    "ui/src",
    "docs/llmwiki",
]

TEXT_SCAN_FILES = [
    "README.md",
    "LICENSE",
    "NOTICE",
]

SECRET_PATTERNS = [
    (
        "private_key_block",
        re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    ),
    (
        "sensitive_assignment",
        re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?key|auth[_-]?token|token|secret|"
            r"password|passwd|credential|cookie|session)\b\s*[:=]\s*"
            r"['\"]?[A-Za-z0-9_./+=:@~$%!-]{20,}['\"]?"
        ),
    ),
    (
        "bearer_token",
        re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/-]{20,}"),
    ),
    (
        "github_token",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    ),
    (
        "openai_style_key",
        re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    ),
    (
        "cookie_file_line",
        re.compile(r"^[^\s#]+\t(?:TRUE|FALSE)\t[^\t]*\t(?:TRUE|FALSE)\t\d+\t[^\t]+\t.{8,}$"),
    ),
    (
        "private_url_query",
        re.compile(r"(?i)https?://[^\s]+[?&](?:token|secret|key|auth|session)=[^\s&]{12,}"),
    ),
]


@dataclass(frozen=True)
class Finding:
    kind: str
    path: str
    message: str
    line: int | None = None
    pattern_family: str | None = None


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a report-only clean package dry-run. No files are generated."
    )
    parser.add_argument(
        "--format",
        choices=["text", "markdown"],
        default="text",
        help="Report format. Text is the default; markdown writes a report-only Markdown summary.",
    )
    return parser.parse_args(argv)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def repo_relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def normalize_rule(rule: str) -> str:
    return rule.rstrip("/")


def rule_matches(rel_path: str, rule: str) -> bool:
    rel = rel_path.replace("\\", "/")
    normalized = normalize_rule(rule)
    if "*" in normalized:
        regex = "^" + re.escape(normalized).replace(r"\*", "[^/]*") + "$"
        return re.match(regex, rel) is not None
    return rel == normalized or rel.startswith(normalized + "/")


def is_excluded_path(rel_path: str) -> bool:
    return any(rule_matches(rel_path, rule) for rule in EXCLUDED_PATHS)


def should_skip_dir(rel_path: str, name: str) -> bool:
    lowered = name.lower()
    if lowered in {
        ".git",
        ".github",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        "node_modules",
        "downloads",
        "state",
        "logs",
        "temp",
        "dist",
        "build",
        "coverage",
        ".turbo",
        ".cache",
    }:
        return True
    return is_excluded_path(rel_path)


def git_value(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return "unknown"
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip() or "unknown"


def existing_excluded_paths(root: Path) -> list[str]:
    found: list[str] = []
    for rule in EXCLUDED_PATHS:
        if "*" in rule:
            continue
        candidate = root / normalize_rule(rule)
        try:
            if candidate.exists():
                found.append(rule)
        except OSError:
            found.append(rule)
    return found


def validate_required_docs(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for rel in REQUIRED_CONTRACT_DOCS:
        path = root / rel
        if not path.is_file():
            findings.append(
                Finding(
                    kind="required_contract_missing",
                    path=rel,
                    message="Required dry-run source-of-truth document is missing.",
                )
            )
    return findings


def validate_planned_paths() -> list[Finding]:
    findings: list[Finding] = []
    planned = (
        [PACKAGE_ROOT]
        + PLANNED_TOP_LEVEL_ENTRIES
        + PLANNED_WINDOWS_ENTRIES
        + PLANNED_MAC_ENTRIES
        + PLANNED_DEVELOPER_ENTRIES
    )
    for rel in planned:
        clean = rel.rstrip("/")
        path = PurePosixPath(clean)
        if path.is_absolute() or ".." in path.parts:
            findings.append(
                Finding(
                    kind="invalid_planned_path",
                    path=rel,
                    message="Planned package path is absolute or uses path traversal.",
                )
            )
    return findings


def walk_repo_files(root: Path, errors: list[Finding]) -> Iterable[Path]:
    def on_error(error: OSError) -> None:
        rel = Path(error.filename).as_posix() if error.filename else "."
        errors.append(
            Finding(
                kind="scan_error",
                path=rel,
                message="Repository path could not be read for dry-run classification.",
            )
        )

    for current, dirnames, filenames in os.walk(root, onerror=on_error):
        current_path = Path(current)
        kept_dirs: list[str] = []
        for dirname in dirnames:
            child = current_path / dirname
            try:
                rel = repo_relative(child, root)
            except ValueError:
                continue
            if should_skip_dir(rel, dirname):
                continue
            kept_dirs.append(dirname)
        dirnames[:] = kept_dirs

        for filename in filenames:
            path = current_path / filename
            try:
                rel = repo_relative(path, root)
            except ValueError:
                continue
            if is_excluded_path(rel):
                continue
            yield path


def forbidden_filename_family(name: str) -> str | None:
    lowered = name.lower()
    if lowered == ".env" or lowered.startswith(".env."):
        return "env_file"
    if lowered == "cookies.txt":
        return "cookie_file"
    for suffix in FORBIDDEN_SUFFIXES:
        if lowered.endswith(suffix):
            return "sensitive_file_suffix"
    for fragment in FORBIDDEN_NAME_FRAGMENTS:
        if fragment in lowered:
            return f"{fragment}_filename"
    return None


def collect_filename_findings(root: Path) -> tuple[list[Finding], list[Finding]]:
    errors: list[Finding] = []
    blocked: list[Finding] = []
    warnings: list[Finding] = []

    for path in walk_repo_files(root, errors):
        rel = repo_relative(path, root)
        family = forbidden_filename_family(path.name)
        if family:
            blocked.append(
                Finding(
                    kind="forbidden_filename",
                    path=rel,
                    pattern_family=family,
                    message="Forbidden filename family is present outside excluded paths.",
                )
            )
            continue

        lowered = path.name.lower()
        if any(fragment in lowered for fragment in AMBIGUOUS_BACKUP_FRAGMENTS):
            warnings.append(
                Finding(
                    kind="ambiguous_backup_filename",
                    path=rel,
                    message=(
                        "Backup-like filename should be reviewed before any "
                        "future package generation."
                    ),
                )
            )

    return blocked + errors, warnings


def collect_missing_source_warnings(root: Path) -> list[Finding]:
    warnings: list[Finding] = []

    for output_name, rel in GUIDE_SOURCE_CANDIDATES:
        if not (root / rel).is_file():
            warnings.append(
                Finding(
                    kind="missing_guide_source",
                    path=rel,
                    message=(
                        f"Beginner guide source for {output_name} is planned "
                        "but not implemented yet."
                    ),
                )
            )

    for label, rel in NOTICE_SOURCE_CANDIDATES:
        if not (root / rel).is_file():
            warnings.append(
                Finding(
                    kind="missing_notice_source",
                    path=rel,
                    message=f"{label} is planned but not implemented yet.",
                )
            )

    for label, rel in SAFETY_NOTICE_SOURCE_CANDIDATES:
        if not (root / rel).is_file():
            warnings.append(
                Finding(
                    kind="missing_local_only_safety_notice_source",
                    path=rel,
                    message=f"{label} is planned but not implemented yet.",
                )
            )

    for label, rel in PLATFORM_SECTION_SOURCE_CANDIDATES:
        if not (root / rel).is_file():
            warnings.append(
                Finding(
                    kind="missing_platform_section_source",
                    path=rel,
                    message=(
                        f"{label} is planned for future Windows/Mac guide "
                        "coverage but not implemented yet."
                    ),
                )
            )

    return warnings


def text_candidate_files(root: Path) -> Iterable[Path]:
    yielded: set[Path] = set()

    for rel in TEXT_SCAN_FILES:
        path = root / rel
        if path.is_file():
            yielded.add(path)
            yield path

    for scan_root in TEXT_SCAN_ROOTS:
        path = root / scan_root
        if not path.exists():
            continue
        for current, dirnames, filenames in os.walk(path):
            current_path = Path(current)
            kept_dirs: list[str] = []
            for dirname in dirnames:
                child = current_path / dirname
                rel = repo_relative(child, root)
                if should_skip_dir(rel, dirname):
                    continue
                kept_dirs.append(dirname)
            dirnames[:] = kept_dirs

            for filename in filenames:
                file_path = current_path / filename
                rel = repo_relative(file_path, root)
                if is_excluded_path(rel):
                    continue
                if file_path.suffix.lower() not in TEXT_SUFFIXES:
                    continue
                if file_path in yielded:
                    continue
                yielded.add(file_path)
                yield file_path


def scan_forbidden_content(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in text_candidate_files(root):
        rel = repo_relative(path, root)
        try:
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                for line_number, line in enumerate(handle, start=1):
                    for family, pattern in SECRET_PATTERNS:
                        if pattern.search(line):
                            findings.append(
                                Finding(
                                    kind="forbidden_content_pattern",
                                    path=rel,
                                    line=line_number,
                                    pattern_family=family,
                                    message=(
                                        "Secret-like content was detected. "
                                        "The matched value is intentionally omitted."
                                    ),
                                )
                            )
        except OSError:
            findings.append(
                Finding(
                    kind="scan_error",
                    path=rel,
                    message="Text candidate could not be read for dry-run classification.",
                )
            )
    return findings


def collect_blockers(root: Path) -> tuple[list[Finding], list[Finding], list[str]]:
    blocked: list[Finding] = []
    warnings: list[Finding] = []

    blocked.extend(validate_required_docs(root))
    blocked.extend(validate_planned_paths())

    generated_path = root / normalize_rule(PACKAGE_ROOT)
    if generated_path.exists():
        blocked.append(
            Finding(
                kind="generated_package_folder_present",
                path=PACKAGE_ROOT,
                message=(
                    "Generated package root already exists; dry-run must not "
                    "mix it with source files."
                ),
            )
        )

    for rel in PR_1001_LEAKAGE_PATHS:
        if (root / rel).exists():
            blocked.append(
                Finding(
                    kind="upstream_pr_1001_leakage",
                    path=rel,
                    message=(
                        "Upstream PR #1001 file is present and must stay out "
                        "of fork-only package work."
                    ),
                )
            )

    filename_blockers, filename_warnings = collect_filename_findings(root)
    blocked.extend(filename_blockers)
    warnings.extend(filename_warnings)
    warnings.extend(collect_missing_source_warnings(root))
    blocked.extend(scan_forbidden_content(root))

    return blocked, warnings, existing_excluded_paths(root)


def format_finding(finding: Finding) -> str:
    parts = [finding.path]
    if finding.line is not None:
        parts.append(f"line {finding.line}")
    if finding.pattern_family:
        parts.append(f"family={finding.pattern_family}")
    return f"{' | '.join(parts)}: {finding.message}"


def print_list(title: str, items: Iterable[str]) -> None:
    print(f"{title}:")
    values = list(items)
    if not values:
        print("  none")
        return
    for item in values:
        print(f"  {item}")


def print_nested_list(title: str, items: Iterable[str]) -> None:
    print(f"  {title}:")
    values = list(items)
    if not values:
        print("    none")
        return
    for item in values:
        print(f"    - {item}")


def present_candidate_lines(
    root: Path,
    candidates: Iterable[tuple[str, str]],
) -> tuple[int, list[str]]:
    present = 0
    lines: list[str] = []
    for label, rel in candidates:
        exists = (root / rel).is_file()
        if exists:
            present += 1
        state = "present" if exists else "missing"
        lines.append(f"{state}: {label} -> {rel}")
    return present, lines


def candidate_coverage(
    root: Path,
    candidates: Iterable[tuple[str, str]],
) -> tuple[int, int, list[str], list[str]]:
    present = 0
    entries: list[str] = []
    missing: list[str] = []
    values = list(candidates)
    for label, rel in values:
        exists = (root / rel).is_file()
        state = "present" if exists else "missing"
        entries.append(f"{state}: {label} -> {rel}")
        if exists:
            present += 1
        else:
            missing.append(f"{label} -> {rel}")
    return present, len(values), entries, missing


def print_package_manifest_preview(root: Path, excluded_found: list[str]) -> None:
    notice_present, notice_lines = present_candidate_lines(
        root, MANIFEST_PREVIEW_NOTICE_SOURCES
    )
    guide_present, guide_lines = present_candidate_lines(root, GUIDE_SOURCE_CANDIDATES)

    print("Package manifest preview:")
    print("  package_name candidate: 動画保存ツール_ローカル専用")
    print("  package_type candidate: local-only beginner package")
    print("  local_only: true")
    print("  generated_artifacts: false")
    print(
        "  notice_sources: "
        f"{notice_present}/{len(MANIFEST_PREVIEW_NOTICE_SOURCES)} present"
    )
    for line in notice_lines:
        print(f"    {line}")
    print(f"  guide_sources: {guide_present}/{len(GUIDE_SOURCE_CANDIDATES)} present")
    for line in guide_lines:
        print(f"    {line}")
    print("  excluded_paths summary:")
    print(f"    rules: {len(EXCLUDED_PATHS)}")
    print(f"    currently_present: {len(excluded_found)}")
    print("  future_outputs candidate:")
    for output in MANIFEST_PREVIEW_FUTURE_OUTPUTS:
        print(f"    {output}")
    print("  human_review_required_before_generation: true")
    print("  legal_final: false")
    print("  secret_values_printed: false")
    print("  token_values_printed: false")
    print("  cookie_values_printed: false")
    print(
        "  no_generation_boundary: preview text only; no manifest.json or "
        "package files were generated."
    )


def print_package_output_diff_prediction(excluded_found: list[str]) -> None:
    print("Package output diff prediction:")
    print(f"  future_package_root: {PACKAGE_ROOT}")
    print_nested_list(
        "would_create_directories",
        DIFF_PREDICTION_CREATE_DIRECTORIES,
    )
    print_nested_list("would_create_files", DIFF_PREDICTION_CREATE_FILES)
    print_nested_list(
        "would_copy_source_groups",
        DIFF_PREDICTION_COPY_SOURCE_GROUPS,
    )
    print_nested_list(
        "would_generate_future_outputs",
        MANIFEST_PREVIEW_FUTURE_OUTPUTS,
    )
    print("  would_exclude_paths summary:")
    print(f"    rules: {len(EXCLUDED_PATHS)}")
    print(f"    currently_present: {len(excluded_found)}")
    print("  no_files_generated: true")
    print("  human_review_required_before_generation: true")
    print(
        "  cleanup_rollback_candidate: future package root only; "
        "human review required before any action."
    )


def print_markdown_item_list(
    items: Iterable[str],
    *,
    code: bool = True,
    indent: str = "",
) -> None:
    values = list(items)
    if not values:
        print(f"{indent}- none")
        return
    for item in values:
        if code:
            print(f"{indent}- `{item}`")
        else:
            print(f"{indent}- {item}")


def format_markdown_finding(finding: Finding) -> str:
    parts = [f"`{finding.path}`"]
    if finding.line is not None:
        parts.append(f"line {finding.line}")
    if finding.pattern_family:
        parts.append(f"family={finding.pattern_family}")
    return f"- {' | '.join(parts)}: {finding.message}"


def print_markdown_findings(findings: list[Finding]) -> None:
    if not findings:
        print("- none")
        return
    for finding in findings:
        print(format_markdown_finding(finding))


def print_markdown_report(
    root: Path,
    blocked: list[Finding],
    warnings: list[Finding],
    excluded_found: list[str],
) -> None:
    status = "BLOCKED" if blocked else "OK"
    branch = git_value(root, "branch", "--show-current")
    commit = git_value(root, "rev-parse", "--short", "HEAD")

    forbidden_paths_status = (
        "BLOCKED"
        if any(b.kind == "generated_package_folder_present" for b in blocked)
        else "OK"
    )
    forbidden_filenames_status = (
        "BLOCKED" if any(b.kind == "forbidden_filename" for b in blocked) else "OK"
    )
    secret_content_status = (
        "BLOCKED"
        if any(b.kind == "forbidden_content_pattern" for b in blocked)
        else "OK"
    )
    generated_state = (
        "present"
        if any(b.kind == "generated_package_folder_present" for b in blocked)
        else "not present"
    )
    pr_1001_status = (
        "BLOCKED"
        if any(b.kind == "upstream_pr_1001_leakage" for b in blocked)
        else "OK"
    )

    notice_present, notice_total, notice_lines, missing_notices = candidate_coverage(
        root, MANIFEST_PREVIEW_NOTICE_SOURCES
    )
    guide_present, guide_total, guide_lines, missing_guides = candidate_coverage(
        root, GUIDE_SOURCE_CANDIDATES
    )
    safety_present, safety_total, safety_lines, missing_safety = candidate_coverage(
        root, SAFETY_NOTICE_SOURCE_CANDIDATES
    )
    platform_present, platform_total, platform_lines, missing_platform = (
        candidate_coverage(root, PLATFORM_SECTION_SOURCE_CANDIDATES)
    )

    print("# Clean Package Dry-Run Report")
    print()
    print("## Summary")
    print()
    print(f"- repository_branch: `{branch}`")
    print(f"- repository_commit: `{commit}`")
    print(f"- package_root_candidate: `{PACKAGE_ROOT}`")
    print("- report_mode: `markdown`")
    print(f"- status: `{status}`")
    print("- no_files_generated: `true`")
    print()
    print("## Status")
    print()
    print(f"- Status: {status}")
    print(f"- Blockers: {len(blocked)}")
    print(f"- Warnings: {len(warnings)}")
    print()
    print("## Risk Classification")
    print()
    print(
        "- Risk classification is provided by `scripts/check_repo_safety.py`, "
        "not by this clean-package dry-run report."
    )
    print("- source: `scripts/check_repo_safety.py --base fork/master`")
    print("- tier: not included by dry-run alone")
    print()
    print("## Package Manifest Preview")
    print()
    print("- package_name candidate: `動画保存ツール_ローカル専用`")
    print("- package_type candidate: `local-only beginner package`")
    print("- local_only: `true`")
    print("- generated_artifacts: `false`")
    print(f"- notice_sources: `{notice_present}/{notice_total} present`")
    print(f"- guide_sources: `{guide_present}/{guide_total} present`")
    print(f"- excluded_path_rules: `{len(EXCLUDED_PATHS)}`")
    print(f"- excluded_paths_currently_present: `{len(excluded_found)}`")
    print("- future_outputs candidate:")
    print_markdown_item_list(MANIFEST_PREVIEW_FUTURE_OUTPUTS, indent="  ")
    print("- human_review_required_before_generation: `true`")
    print("- legal_final: `false`")
    print("- secret_values_printed: `false`")
    print("- token_values_printed: `false`")
    print("- cookie_values_printed: `false`")
    print()
    print("Notice source details:")
    print_markdown_item_list(notice_lines, code=False, indent="  ")
    print()
    print("Guide source details:")
    print_markdown_item_list(guide_lines, code=False, indent="  ")
    print()
    print("## Package Output Diff Prediction")
    print()
    print(f"- future_package_root: `{PACKAGE_ROOT}`")
    print("- would_create_directories:")
    print_markdown_item_list(DIFF_PREDICTION_CREATE_DIRECTORIES, indent="  ")
    print("- would_create_files:")
    print_markdown_item_list(DIFF_PREDICTION_CREATE_FILES, indent="  ")
    print("- would_copy_source_groups:")
    print_markdown_item_list(DIFF_PREDICTION_COPY_SOURCE_GROUPS, indent="  ")
    print("- would_generate_future_outputs:")
    print_markdown_item_list(MANIFEST_PREVIEW_FUTURE_OUTPUTS, indent="  ")
    print(f"- would_exclude_path_rules: `{len(EXCLUDED_PATHS)}`")
    print(f"- would_exclude_paths_currently_present: `{len(excluded_found)}`")
    print("- no_files_generated: `true`")
    print("- human_review_required_before_generation: `true`")
    print(
        "- cleanup_rollback_candidate: future package root only; human review "
        "required before any action."
    )
    print()
    print("## Notice / Guide Source Coverage")
    print()
    print(f"- notice_sources_present: `{notice_present}/{notice_total}`")
    print(f"- guide_sources_present: `{guide_present}/{guide_total}`")
    print(f"- local_only_safe_use_sources_present: `{safety_present}/{safety_total}`")
    print(f"- windows_macos_section_sources_present: `{platform_present}/{platform_total}`")
    print("- missing_notice_sources:")
    print_markdown_item_list(missing_notices, code=False, indent="  ")
    print("- missing_guide_sources:")
    print_markdown_item_list(missing_guides, code=False, indent="  ")
    print("- missing_local_only_safe_use_sources:")
    print_markdown_item_list(missing_safety, code=False, indent="  ")
    print("- missing_windows_macos_section_sources:")
    print_markdown_item_list(missing_platform, code=False, indent="  ")
    print()
    print("Local-only / safe-use source details:")
    print_markdown_item_list(safety_lines, code=False, indent="  ")
    print()
    print("Windows/macOS section source details:")
    print_markdown_item_list(platform_lines, code=False, indent="  ")
    print()
    print("## Excluded Paths Summary")
    print()
    print(f"- excluded_rule_count: `{len(EXCLUDED_PATHS)}`")
    print(f"- currently_present_excluded_path_count: `{len(excluded_found)}`")
    print(f"- generated_package_root: `{generated_state}`")
    print(f"- PR #1001 leakage: `{pr_1001_status}`")
    print(f"- forbidden paths: `{forbidden_paths_status}`")
    print(f"- forbidden filenames: `{forbidden_filenames_status}`")
    print(f"- secret-like content: `{secret_content_status}`")
    print("- excluded_paths_currently_present:")
    print_markdown_item_list(excluded_found, indent="  ")
    print()
    print("## Blockers")
    print()
    print_markdown_findings(blocked)
    print()
    print("## Warnings")
    print()
    print_markdown_findings(warnings)
    print()
    print("## Human Review Checklist")
    print()
    print("- [ ] Status is OK.")
    print("- [ ] Repo safety gate has no blockers.")
    print("- [ ] Clean-package dry-run has no blockers.")
    print("- [ ] Package manifest preview is acceptable.")
    print("- [ ] Package output diff prediction is acceptable.")
    print("- [ ] Notice and guide source coverage is acceptable for this phase.")
    print("- [ ] Excluded paths summary is acceptable.")
    print("- [ ] No generated package folder exists.")
    print("- [ ] No cookie/token/secret values are printed.")
    print("- [ ] PR #1001 files are absent.")
    print("- [ ] No backend/frontend/Docker/CI/package/lockfile changes are mixed in.")
    print("- [ ] Human review is complete before any actual generation task.")
    print()
    print("## No-Generation Boundary")
    print()
    print("- This is a report-only dry-run.")
    print("- No package files were generated.")
    print("- No package files were copied.")
    print("- No generated artifact was created.")
    print("- Markdown mode is not permission to generate package output.")
    print("- Default text output remains supported.")


def print_report(
    root: Path,
    blocked: list[Finding],
    warnings: list[Finding],
    excluded_found: list[str],
) -> None:
    status = "BLOCKED" if blocked else "OK"
    branch = git_value(root, "branch", "--show-current")
    commit = git_value(root, "rev-parse", "--short", "HEAD")

    print("Clean package dry-run report")
    print()
    print("Package root:")
    print(f"  {PACKAGE_ROOT}")
    print()
    print("Status:")
    print(f"  {status}")
    print()
    print("Repository:")
    print(f"  branch: {branch}")
    print(f"  commit: {commit}")
    print()
    print_list("Planned entries", PLANNED_TOP_LEVEL_ENTRIES)
    print()
    print_list("Planned Windows entries", PLANNED_WINDOWS_ENTRIES)
    print()
    print_list("Planned macOS entries", PLANNED_MAC_ENTRIES)
    print()
    print_list("Planned developer entries", PLANNED_DEVELOPER_ENTRIES)
    print()
    print_package_manifest_preview(root, excluded_found)
    print()
    print_package_output_diff_prediction(excluded_found)
    print()
    print_list("Excluded rules", EXCLUDED_PATHS)
    print()
    print_list("Excluded paths currently present", excluded_found)
    print()
    print("Checks:")
    forbidden_paths_status = (
        "BLOCKED"
        if any(b.kind == "generated_package_folder_present" for b in blocked)
        else "OK"
    )
    forbidden_filenames_status = (
        "BLOCKED" if any(b.kind == "forbidden_filename" for b in blocked) else "OK"
    )
    secret_content_status = (
        "BLOCKED"
        if any(b.kind == "forbidden_content_pattern" for b in blocked)
        else "OK"
    )
    print(f"  forbidden paths: {forbidden_paths_status}")
    print(f"  forbidden filenames: {forbidden_filenames_status}")
    print(f"  secret-like content: {secret_content_status}")
    generated_state = (
        "present"
        if any(b.kind == "generated_package_folder_present" for b in blocked)
        else "not present"
    )
    print(f"  generated package folder: {generated_state}")
    print("  beginner guides: planned")
    print(
        "  guide/notice source warnings: "
        + ("present" if warnings else "none")
    )
    print("  Windows/Mac sections: planned")
    pr_1001_status = (
        "BLOCKED"
        if any(b.kind == "upstream_pr_1001_leakage" for b in blocked)
        else "OK"
    )
    print(f"  PR #1001 leakage: {pr_1001_status}")
    print()

    if warnings:
        print(f"Warnings ({len(warnings)} nonblocking):")
        for warning in warnings:
            print(f"  {format_finding(warning)}")
        print()
    else:
        print("Warnings:")
        print("  none")
        print()

    if blocked:
        print("Blocked reasons:")
        for finding in blocked:
            print(f"  {format_finding(finding)}")
        print()
    else:
        print("Blocked reasons:")
        print("  none")
        print()

    print("Safety flags:")
    print("  local_only: true")
    print("  public_hosting: false")
    print("  ads: false")
    print("  update_apply: false")
    print("  docker_pull: false")
    print("  git_update: false")
    print("  package_install: false")
    print("  credential_handling: false")
    print("  generated_folder_created: false")
    print()
    print("No files were generated.")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = repo_root()
    blocked, warnings, excluded_found = collect_blockers(root)
    if args.format == "markdown":
        print_markdown_report(root, blocked, warnings, excluded_found)
    else:
        print_report(root, blocked, warnings, excluded_found)
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
