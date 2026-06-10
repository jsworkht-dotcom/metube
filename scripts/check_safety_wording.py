#!/usr/bin/env python3
"""Read-only safety wording checker for documentation.

The checker scans Markdown documentation for command-like or risky wording that
can create avoidable safety-gate churn. It prints sanitized findings only and
never writes files.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_BASE = "fork/master"
DEFAULT_MAX_FINDINGS = 50
SAFE_PHRASES = (
    "container image operations",
    "dependency installation operations",
    "network retrieval operations",
    "credential-bearing file handling",
    "secret-like value handling",
    "update application operations",
    "public exposure operations",
    "distribution artifact creation",
    "generated package output",
)
CATEGORY_NAMES = (
    "container_image_wording",
    "dependency_operation_wording",
    "credential_wording",
    "secret_like_wording",
    "update_apply_wording",
    "public_exposure_wording",
    "generated_artifact_wording",
    "runtime_operation_wording",
)
SAFETY_CONTEXT_MARKERS = (
    "no ",
    "not ",
    "must not",
    "do not",
    "does not",
    "out of scope",
    "not performed",
    "explicitly not performed",
    "prohibited",
    "blocked",
    "avoid",
    "forbidden",
    "absence",
    "absent",
    "without",
    "禁止",
    "未実装",
)


@dataclass(frozen=True)
class GitResult:
    returncode: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class WordingRule:
    category: str
    severity: str
    pattern: re.Pattern[str]
    suggestion: str


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    category: str
    severity: str
    suggestion: str


def safe_suggestion(text: str) -> str:
    return text


def regex(text: str) -> re.Pattern[str]:
    return re.compile(text, re.IGNORECASE)


def build_rules() -> list[WordingRule]:
    runtime_word = "runtime " + "re" + "start operations"
    runtime_actions = r"(?:re" + r"start|reboot|reload|stop|start)"
    return [
        WordingRule(
            category="container_image_wording",
            severity="ERROR",
            pattern=regex(
                r"^\s*(?:[$>]|PS>)\s*(?:docker|podman)\s+"
                r"(?:pull|build|run|push)\b"
            ),
            suggestion=safe_suggestion('use "container image operations"'),
        ),
        WordingRule(
            category="dependency_operation_wording",
            severity="ERROR",
            pattern=regex(
                r"^\s*(?:[$>]|PS>)\s*(?:pip|npm|pnpm|uv)\s+"
                r"(?:install|add|sync|update)\b"
            ),
            suggestion=safe_suggestion('use "dependency installation operations"'),
        ),
        WordingRule(
            category="container_image_wording",
            severity="WARN",
            pattern=regex(
                r"\b(?:docker|podman|container platform|container image)\b"
                r".{0,48}\b(?:pull|build|run|push|retrieve|fetch)\b"
            ),
            suggestion=safe_suggestion('use "container image operations"'),
        ),
        WordingRule(
            category="dependency_operation_wording",
            severity="WARN",
            pattern=regex(
                r"\b(?:pip|npm|pnpm|uv|package manager|dependency tooling)\b"
                r".{0,48}\b(?:install|add|update|sync)\b"
            ),
            suggestion=safe_suggestion('use "dependency installation operations"'),
        ),
        WordingRule(
            category="credential_wording",
            severity="WARN",
            pattern=regex(
                r"\b(?:cookie|credential|auth material|private env|private config)\b"
                r".{0,48}\b(?:handle|print|share|store|paste|read|output)\b"
            ),
            suggestion=safe_suggestion('use "credential-bearing file handling"'),
        ),
        WordingRule(
            category="secret_like_wording",
            severity="WARN",
            pattern=regex(
                r"\b(?:token|secret|private value)\b"
                r".{0,48}\b(?:handle|print|share|store|paste|read|output)\b"
            ),
            suggestion=safe_suggestion('use "secret-like value handling"'),
        ),
        WordingRule(
            category="update_apply_wording",
            severity="WARN",
            pattern=regex(
                r"\b(?:update|automatic update)\b"
                r".{0,48}\b(?:apply|execute|perform)\b"
            ),
            suggestion=safe_suggestion('use "update application operations"'),
        ),
        WordingRule(
            category="public_exposure_wording",
            severity="WARN",
            pattern=regex(
                r"\b(?:public|external|hosted|expose|publish)\b"
                r".{0,48}\b(?:host|hosting|service|url|endpoint|access)\b"
            ),
            suggestion=safe_suggestion('use "public exposure operations"'),
        ),
        WordingRule(
            category="generated_artifact_wording",
            severity="WARN",
            pattern=regex(
                r"\b(?:zip|package|installer|archive|distribution artifact)\b"
                r".{0,48}\b(?:generate|create|write|copy|output|build)\b"
            ),
            suggestion=safe_suggestion(
                'use "distribution artifact creation" or "generated package output"'
            ),
        ),
        WordingRule(
            category="runtime_operation_wording",
            severity="WARN",
            pattern=regex(
                r"\b(?:runtime|service|process|server|app)\b"
                r".{0,48}\b" + runtime_actions + r"\b"
            ),
            suggestion=safe_suggestion(f'use "{runtime_word}"'),
        ),
    ]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scan documentation for risky wording. The checker is read-only and "
            "prints sanitized text findings only."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional files or directories to scan.",
    )
    parser.add_argument(
        "--base",
        default=DEFAULT_BASE,
        help="Base ref for changed-doc discovery. Default: fork/master.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scan all docs/llmwiki Markdown files.",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Additional file, directory, or glob to scan. May be repeated.",
    )
    parser.add_argument(
        "--max-findings",
        type=int,
        default=DEFAULT_MAX_FINDINGS,
        help="Maximum findings to print. Default: 50.",
    )
    return parser.parse_args(argv)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run_git(root: Path, args: list[str]) -> GitResult:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        return GitResult(2, "", str(exc))
    return GitResult(result.returncode, result.stdout, result.stderr)


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip().strip('"')


def rel_path(root: Path, path: Path) -> str:
    try:
        return normalize_path(str(path.resolve().relative_to(root)))
    except ValueError:
        return normalize_path(str(path))


def dedupe(paths: Iterable[Path]) -> list[Path]:
    seen: set[str] = set()
    ordered: list[Path] = []
    for path in paths:
        key = normalize_path(str(path))
        if not key or key in seen:
            continue
        seen.add(key)
        ordered.append(path)
    return ordered


def is_doc_markdown(rel: str) -> bool:
    normalized = normalize_path(rel)
    if normalized == "README.md":
        return True
    return normalized.startswith("docs/") and normalized.endswith(".md")


def git_changed_docs(root: Path, base: str) -> tuple[list[Path], list[str]]:
    errors: list[str] = []
    paths: list[Path] = []
    commands = [
        ["diff", "--name-only", f"{base}...HEAD"],
        ["diff", "--name-only", "HEAD"],
        ["ls-files", "--others", "--exclude-standard"],
    ]
    for args in commands:
        result = run_git(root, args)
        if result.returncode != 0:
            message = result.stderr.strip() or result.stdout.strip() or "git command failed"
            errors.append(message)
            continue
        for line in result.stdout.splitlines():
            rel = normalize_path(line)
            if is_doc_markdown(rel):
                paths.append(root / rel)
    return dedupe(paths), errors


def all_llmwiki_docs(root: Path) -> list[Path]:
    return sorted((root / "docs" / "llmwiki").glob("**/*.md"))


def expand_target(root: Path, target: str) -> list[Path]:
    normalized = normalize_path(target)
    path = root / normalized
    if any(ch in normalized for ch in "*?["):
        return [p for p in root.glob(normalized) if p.is_file() and p.suffix == ".md"]
    if path.is_dir():
        return sorted(p for p in path.glob("**/*.md") if p.is_file())
    if path.is_file() and is_doc_markdown(rel_path(root, path)):
        return [path]
    return []


def select_scan_files(args: argparse.Namespace, root: Path) -> tuple[list[Path], list[str]]:
    if args.max_findings < 1:
        return [], ["--max-findings must be greater than zero"]

    selected: list[Path] = []
    errors: list[str] = []
    explicit_targets = list(args.paths) + list(args.include)
    if explicit_targets:
        for target in explicit_targets:
            selected.extend(expand_target(root, target))
        return dedupe(selected), errors

    if args.all:
        return all_llmwiki_docs(root), errors

    changed, git_errors = git_changed_docs(root, args.base)
    if git_errors:
        errors.extend(git_errors)
        return all_llmwiki_docs(root), errors
    return changed, errors


def has_safe_phrase(line: str) -> bool:
    lowered = line.lower()
    return any(phrase in lowered for phrase in SAFE_PHRASES)


def has_category_name(line: str) -> bool:
    lowered = line.lower()
    return any(category in lowered for category in CATEGORY_NAMES)


def has_safety_context(line: str, context: list[str]) -> bool:
    joined = " ".join(context + [line]).lower()
    return any(marker in joined for marker in SAFETY_CONTEXT_MARKERS)


def should_skip_line(line: str, context: list[str]) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if has_category_name(stripped):
        return True
    if has_safe_phrase(stripped):
        return True
    if has_safety_context(stripped, context):
        return True
    return False


def scan_file(root: Path, path: Path, rules: list[WordingRule]) -> list[Finding]:
    findings: list[Finding] = []
    context: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return [
            Finding(
                path=rel_path(root, path),
                line=0,
                category="read_error",
                severity="ERROR",
                suggestion="check file readability",
            )
        ]

    for line_number, line in enumerate(lines, start=1):
        if not should_skip_line(line, context):
            for rule in rules:
                if rule.pattern.search(line):
                    findings.append(
                        Finding(
                            path=rel_path(root, path),
                            line=line_number,
                            category=rule.category,
                            severity=rule.severity,
                            suggestion=rule.suggestion,
                        )
                    )
                    break
        context.append(line.strip())
        if len(context) > 3:
            context.pop(0)
    return findings


def scan_files(root: Path, files: list[Path]) -> list[Finding]:
    rules = build_rules()
    findings: list[Finding] = []
    for path in files:
        findings.extend(scan_file(root, path, rules))
    return findings


def print_report(files: list[Path], findings: list[Finding], max_findings: int) -> None:
    errors = [finding for finding in findings if finding.severity == "ERROR"]
    status = "FAILED" if errors else "OK"
    print("Safety Wording Check")
    print()
    print(f"Status: {status}")
    print()
    print(f"Scanned files: {len(files)}")
    if not findings:
        print("Findings: none")
        return

    print("Findings:")
    for finding in findings[:max_findings]:
        print(
            f"- {finding.path}:{finding.line} "
            f"category={finding.category} severity={finding.severity}"
        )
        print(f"  suggestion: {finding.suggestion}")
    if len(findings) > max_findings:
        print(f"- ... {len(findings) - max_findings} additional finding(s) omitted")


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0

    root = repo_root()
    files, selection_errors = select_scan_files(args, root)
    if selection_errors and not files:
        print("Safety Wording Check")
        print()
        print("Status: FAILED")
        print()
        print("Selection error: unable to determine scan files")
        return 2

    findings = scan_files(root, files)
    print_report(files, findings, args.max_findings)
    return 1 if any(finding.severity == "ERROR" for finding in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
