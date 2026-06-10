#!/usr/bin/env python3
"""Generate a reviewable PR body as Markdown on stdout.

The generator is intentionally narrow: it reads command-line facts and optional
Git changed-file metadata, then prints Markdown. It does not write files, call
GitHub APIs, create or edit PRs, stage commits, or create package output.
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
RISKS = ("low", "medium", "high-low", "high-mid", "high-high")
SCOPES = ("docs-only", "report-only", "checker-only", "combined", "high-mid-pr-ready")
AUTOMATION_CHOICES = (
    "auto-merge-ok",
    "pr-only-human-merge",
    "stop-before-implementation",
)
VERIFICATION_PRESETS = ("standard", "docs-only", "script", "checker", "dry-run")
LOCAL_HELPER_NOTE = [
    "`export_context_updated.py` remains locally excluded via `.git/info/exclude`.",
    "`.gitignore` was not changed.",
    "helper remains uncommitted.",
]
URL_RE = re.compile(r"https?://\S+")
KEY_VALUE_SECRET_RE = re.compile(
    r"(?i)\b(cookie|set-cookie|token|secret|credential|password|passwd|"
    r"api[_-]?key|session|auth)\b\s*[:=]\s*[^\s;]+"
)
ENV_SECRET_RE = re.compile(
    r"(?i)\b[A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|PASSWD|API_KEY|COOKIE|"
    r"CREDENTIAL)[A-Z0-9_]*\s*=\s*[^\s]+"
)


@dataclass(frozen=True)
class GitResult:
    returncode: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class ChangedFiles:
    base_diff: list[str]
    working_tree: list[str]
    untracked: list[str]
    errors: list[str]

    def all_paths(self) -> list[str]:
        return dedupe([*self.base_diff, *self.working_tree, *self.untracked])


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a Markdown PR body on stdout. The generator is read-only "
            "and does not call GitHub APIs or write files."
        )
    )
    parser.add_argument("--title", required=True, help="PR title used for validation context.")
    parser.add_argument("--risk", required=True, choices=RISKS, help="Risk tier.")
    parser.add_argument("--scope", required=True, choices=SCOPES, help="PR body preset scope.")
    parser.add_argument(
        "--base",
        default=DEFAULT_BASE,
        help=f"Base ref for optional changed-file summaries. Default: {DEFAULT_BASE}.",
    )
    parser.add_argument(
        "--automation",
        choices=AUTOMATION_CHOICES,
        help="Override the default automation decision when the combination is safe.",
    )
    parser.add_argument(
        "--summary-line",
        action="append",
        default=[],
        help="Summary bullet text. May be repeated.",
    )
    local_helper = parser.add_mutually_exclusive_group()
    local_helper.add_argument(
        "--include-local-helper-note",
        action="store_true",
        default=True,
        help="Include the local helper note section. This is the default.",
    )
    local_helper.add_argument(
        "--no-local-helper-note",
        action="store_false",
        dest="include_local_helper_note",
        help="Omit the local helper note section.",
    )
    parser.add_argument(
        "--human-review-required",
        action="store_true",
        help="Include human-review-required marker where applicable.",
    )
    parser.add_argument(
        "--changed-files",
        action="store_true",
        help="Include sanitized changed-file names from read-only Git commands.",
    )
    parser.add_argument(
        "--verification-preset",
        choices=VERIFICATION_PRESETS,
        help="Override verification section preset.",
    )
    return parser.parse_args(argv)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip().strip('"')


def sanitize_text(text: str) -> str:
    sanitized = URL_RE.sub("[redacted-url]", text)
    sanitized = ENV_SECRET_RE.sub("[redacted-secret]", sanitized)
    return KEY_VALUE_SECRET_RE.sub(lambda match: f"{match.group(1)}=[redacted]", sanitized)


def sanitize_path(path: str) -> str:
    return sanitize_text(normalize_path(path))


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


def git_paths(root: Path, args: list[str]) -> tuple[list[str], str | None]:
    result = run_git(root, args)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "git command failed"
        return [], sanitize_text(message)
    paths = [sanitize_path(line) for line in result.stdout.splitlines() if line.strip()]
    return dedupe(paths), None


def collect_changed_files(root: Path, base: str) -> ChangedFiles:
    base_diff, base_error = git_paths(root, ["diff", "--name-only", f"{base}...HEAD"])
    working_tree, working_error = git_paths(root, ["diff", "--name-only", "HEAD"])
    untracked, untracked_error = git_paths(root, ["ls-files", "--others", "--exclude-standard"])
    errors = [
        error
        for error in (
            f"base diff: {base_error}" if base_error else None,
            f"working tree: {working_error}" if working_error else None,
            f"untracked: {untracked_error}" if untracked_error else None,
        )
        if error
    ]
    return ChangedFiles(
        base_diff=base_diff,
        working_tree=working_tree,
        untracked=untracked,
        errors=errors,
    )


def dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def display_risk(risk: str) -> str:
    return {
        "low": "Low",
        "medium": "Medium",
        "high-low": "High-low",
        "high-mid": "High-mid",
        "high-high": "High-high",
    }[risk]


def default_automation(risk: str) -> str:
    if risk in {"low", "medium", "high-low"}:
        return "auto-merge-ok"
    if risk == "high-mid":
        return "pr-only-human-merge"
    return "stop-before-implementation"


def validate_options(args: argparse.Namespace) -> list[str]:
    automation = args.automation or default_automation(args.risk)
    errors: list[str] = []
    if args.risk == "high-mid" and automation == "auto-merge-ok":
        errors.append("high-mid cannot use automation=auto-merge-ok")
    if args.risk == "high-high" and automation in {"auto-merge-ok", "pr-only-human-merge"}:
        errors.append("high-high must use automation=stop-before-implementation")
    if args.scope == "high-mid-pr-ready" and automation == "auto-merge-ok":
        errors.append("high-mid-pr-ready scope cannot use automation=auto-merge-ok")
    if not args.title.strip():
        errors.append("--title must not be empty")
    return errors


def effective_human_review_required(args: argparse.Namespace, automation: str) -> bool:
    return (
        args.human_review_required
        or args.risk in {"high-mid", "high-high"}
        or automation in {"pr-only-human-merge", "stop-before-implementation"}
    )


def summary_lines(args: argparse.Namespace) -> list[str]:
    if args.summary_line:
        return [line.strip() for line in args.summary_line if line.strip()]
    return [
        "Add/update project files for the requested scope.",
        "Preserve existing safety boundaries.",
    ]


def not_performed_lines(scope: str) -> list[str]:
    common_high_risk = [
        "no GitHub API integration",
        "no PR creation/editing automation",
        "no report file writing",
        "no generated distribution folder",
        "no package manifest output",
        "no generated notice/license/inventory/guide output",
        "no ZIP/package/installer output",
        "no dependency installation operations",
        "no package/lockfile changes",
        "no container image operations",
        "no backend/frontend/Docker/CI changes",
        "no backend download/extractor changes",
        "no cookie/token/secret handling",
        "no public hosting or ads",
        "no PR #1001 files",
        "no update application operations",
    ]
    if scope == "docs-only":
        return [
            "no script changes",
            "no checker changes",
            "no CI integration",
            *common_high_risk,
        ]
    if scope == "checker-only":
        return [
            "no changes to `scripts/check_repo_safety.py`",
            "no changes to `scripts/check_clean_package_dry_run_reports.py`",
            "no changes to `scripts/clean_package_dry_run.py`",
            "no changes to `scripts/run_local_safety_gates.py`",
            "no changes to `scripts/check_safety_wording.py`",
            "no CI integration",
            *common_high_risk,
        ]
    if scope == "report-only":
        return [
            "no generated distribution folder",
            "no report file writing unless explicitly approved",
            "no package output",
            "no GitHub API integration",
            "no PR creation/editing automation",
            "no dependency installation operations",
            "no package/lockfile changes",
            "no container image operations",
            "no backend/frontend/Docker/CI changes",
            "no cookie/token/secret handling",
            "no public hosting or ads",
            "no PR #1001 files",
            "no update application operations",
        ]
    if scope == "high-mid-pr-ready":
        return [
            "no auto merge",
            "human review required before merge",
            "no actual generation",
            "no distribution artifact creation",
            *common_high_risk,
        ]
    return [
        "no actual generation",
        "no CI integration",
        "no GitHub API integration",
        "no PR creation/editing automation",
        *common_high_risk,
    ]


def infer_verification_preset(scope: str) -> str:
    if scope == "docs-only":
        return "docs-only"
    if scope == "checker-only":
        return "checker"
    if scope == "report-only":
        return "dry-run"
    return "standard"


def changed_scripts(changed: ChangedFiles | None) -> list[str]:
    if not changed:
        return []
    return [
        path
        for path in changed.all_paths()
        if path.startswith("scripts/") and path.endswith(".py")
    ]


def verification_lines(
    args: argparse.Namespace,
    changed: ChangedFiles | None,
) -> list[str]:
    preset = args.verification_preset or infer_verification_preset(args.scope)
    lines = ["`git diff --check`"]
    scripts = changed_scripts(changed)

    if preset in {"script", "checker", "dry-run"} or args.scope in {"checker-only", "report-only"}:
        if scripts:
            lines.extend(f"`python -m py_compile {path}`" for path in scripts)
        else:
            lines.append("`python -m py_compile <changed-script>`")

    lines.append(f"`python scripts/check_safety_wording.py --base {args.base}`")

    if preset == "docs-only":
        lines.append(
            f"`python scripts/run_local_safety_gates.py --base {args.base} --scope docs-only`"
        )
    else:
        lines.append(f"`python scripts/run_local_safety_gates.py --base {args.base}`")

    if preset == "dry-run":
        lines.extend(
            [
                "`python scripts/check_clean_package_dry_run_reports.py`",
                "`python scripts/clean_package_dry_run.py`",
                "`python scripts/clean_package_dry_run.py --format text`",
                "`python scripts/clean_package_dry_run.py --format markdown`",
                "`python scripts/clean_package_dry_run.py --format json`",
            ]
        )

    lines.extend(
        [
            "confirmed no `動画保存ツール_ローカル専用/`",
            "confirmed `export_context_updated.py` remains locally excluded and not committed",
        ]
    )
    return dedupe(lines)


def cleanup_lines(risk: str) -> list[str]:
    if risk == "high-mid":
        return [
            "Revert the PR branch or commit if needed.",
            "Do not merge until human review is complete.",
            "No generated package output should exist unless separately approved.",
        ]
    if risk == "high-high":
        return [
            "Stop before implementation unless explicitly approved.",
            "No generated package output should exist unless separately approved.",
        ]
    return [
        "Revert the commit if needed.",
        "No generated package output exists to clean up.",
    ]


def human_review_lines(risk: str) -> list[str]:
    if risk == "high-mid":
        return [
            "This PR is PR-ready only.",
            "Human review is required before merge.",
            "Auto merge is prohibited.",
            "Actual package generation remains blocked until later human-reviewed approval.",
        ]
    if risk == "high-high":
        return [
            "Stop before implementation.",
            "Explicit human approval is required before any implementation work.",
        ]
    return [
        "Future higher-risk work still requires human review.",
        "This PR does not authorize higher-risk operations.",
        "Actual package generation remains blocked until later human-reviewed approval.",
    ]


def risk_lines(args: argparse.Namespace, automation: str, human_review_required: bool) -> list[str]:
    risk = display_risk(args.risk)
    if args.risk == "high-mid":
        return [
            f"Risk tier: {risk}",
            "Automation decision: PR-ready only",
            "automation: pr-only-human-merge",
            "human-review-required",
        ]
    if args.risk == "high-high":
        return [
            f"Risk tier: {risk}",
            "Automation decision: stop before implementation",
            "automation: stop-before-implementation",
            "human-review-required",
        ]

    lines = [
        f"Risk tier: {risk}",
        "Automation decision: auto-merge-ok if all gates pass",
        f"automation: {automation}",
    ]
    if human_review_required:
        lines.append("human-review-required")
    return lines


def print_section(title: str, lines: list[str], bullet: bool = True) -> None:
    print(f"## {title}")
    print()
    if not lines:
        print("- none" if bullet else "none")
    elif bullet:
        for line in lines:
            print(f"- {line}")
    else:
        for line in lines:
            print(line)
    print()


def print_changed_files(changed: ChangedFiles) -> None:
    print("## Changed files")
    print()
    if changed.errors:
        print("- changed-file summary unavailable:")
        for error in changed.errors:
            print(f"  - {error}")
        print()
        return

    groups = [
        ("base diff", changed.base_diff),
        ("working tree", changed.working_tree),
        ("untracked", changed.untracked),
    ]
    for label, paths in groups:
        if paths:
            print(f"- {label}:")
            for path in paths:
                print(f"  - `{path}`")
        else:
            print(f"- {label}: none")
    print()


def render(args: argparse.Namespace, changed: ChangedFiles | None) -> None:
    automation = args.automation or default_automation(args.risk)
    human_review_required = effective_human_review_required(args, automation)

    print_section("Summary", summary_lines(args))
    print_section("Risk / automation", risk_lines(args, automation, human_review_required), bullet=False)
    if args.include_local_helper_note:
        print_section("Local helper note", LOCAL_HELPER_NOTE)
    print_section("Explicitly not performed", not_performed_lines(args.scope))
    if changed:
        print_changed_files(changed)
    print_section("Verification", verification_lines(args, changed))
    print_section("Cleanup / rollback", cleanup_lines(args.risk))
    print_section("Human review note", human_review_lines(args.risk))


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0

    validation_errors = validate_options(args)
    if validation_errors:
        for error in validation_errors:
            print(f"validation error: {error}", file=sys.stderr)
        return 1

    changed = collect_changed_files(repo_root(), args.base) if args.changed_files else None
    if changed and changed.errors:
        for error in changed.errors:
            print(f"runtime error: {error}", file=sys.stderr)
        return 2

    render(args, changed)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
