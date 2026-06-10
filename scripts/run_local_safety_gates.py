#!/usr/bin/env python3
"""Run local repository safety gates in a read-only sequence.

This script is an orchestrator for existing local gates. It does not replace
those gates, write reports, create package output, use GitHub APIs, or perform
source-control publishing actions.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


PACKAGE_ROOT = "動画保存ツール_ローカル専用"
LOCAL_HELPER = "export_context_updated.py"
PR_1001_PATHS = {
    "docker-compose.local.yml",
    "docs/local-only.md",
}
FORBIDDEN_CHANGED_PATHS = (
    "app/",
    "ui/",
    ".github/",
    "Dockerfile",
    "docker-entrypoint.sh",
    "pyproject.toml",
    "uv.lock",
    "ui/package.json",
    "ui/pnpm-lock.yaml",
    "docker-compose.local.yml",
    "docs/local-only.md",
    f"{PACKAGE_ROOT}/",
    ".gitignore",
)
SCOPE_CHOICES = (
    "auto",
    "docs-only",
    "report-only",
    "checker-only",
    "combined",
    "high-mid-pr-ready",
)
SCOPE_ALLOWED = {
    "docs-only": ("docs/llmwiki/",),
    "report-only": (
        "scripts/clean_package_dry_run.py",
        "scripts/check_clean_package_dry_run_reports.py",
        "docs/llmwiki/",
    ),
    "checker-only": (
        "scripts/check_clean_package_dry_run_reports.py",
        "docs/llmwiki/",
    ),
    "combined": (
        "scripts/clean_package_dry_run.py",
        "scripts/check_clean_package_dry_run_reports.py",
        "docs/llmwiki/",
    ),
}
INTERESTING_FAILURE_RE = re.compile(
    r"status|blocked|failed|failure|failures|error|fatal|risk classification",
    re.IGNORECASE,
)
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
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


@dataclass
class GateResult:
    name: str
    ok: bool
    exit_code: int | None = None
    detail: str = ""
    excerpt: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        return "OK" if self.ok else "FAILED"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run local safety gates and print a concise text summary. "
            "The aggregator is read-only and writes no report files."
        )
    )
    parser.add_argument(
        "--base",
        default="fork/master",
        help="Base ref for branch-diff checks. Default: fork/master.",
    )
    parser.add_argument(
        "--scope",
        default="auto",
        choices=SCOPE_CHOICES,
        help="Optional changed-file scope check. Default: auto.",
    )
    return parser.parse_args(argv)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip().strip('"')


def run_process(root: Path, command: list[str]) -> CommandResult:
    try:
        result = subprocess.run(
            command,
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        return CommandResult(2, "", str(exc))
    return CommandResult(result.returncode, result.stdout, result.stderr)


def sanitize_line(line: str) -> str:
    sanitized = URL_RE.sub("[redacted-url]", line)
    sanitized = ENV_SECRET_RE.sub("[redacted-secret]", sanitized)
    sanitized = KEY_VALUE_SECRET_RE.sub(lambda m: f"{m.group(1)}=[redacted]", sanitized)
    return sanitized


def failure_excerpt(result: CommandResult) -> list[str]:
    combined = []
    for line in (result.stdout + "\n" + result.stderr).splitlines():
        stripped = line.strip()
        if stripped:
            combined.append(sanitize_line(stripped))
    interesting = [line for line in combined if INTERESTING_FAILURE_RE.search(line)]
    selected = interesting[:20] if interesting else combined[:20]
    return selected


def run_gate(root: Path, name: str, command: list[str]) -> GateResult:
    result = run_process(root, command)
    if result.returncode == 0:
        return GateResult(name=name, ok=True, exit_code=0)
    return GateResult(
        name=name,
        ok=False,
        exit_code=result.returncode,
        excerpt=failure_excerpt(result),
    )


def git_lines(root: Path, args: list[str]) -> tuple[list[str], CommandResult]:
    result = run_process(root, ["git", *args])
    if result.returncode != 0:
        return [], result
    lines = [normalize_path(line) for line in result.stdout.splitlines() if line.strip()]
    return lines, result


def dedupe(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for path in paths:
        normalized = normalize_path(path)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def collect_changed_files(root: Path, base: str) -> tuple[dict[str, list[str]], list[str]]:
    errors: list[str] = []
    groups: dict[str, list[str]] = {
        "base diff": [],
        "working tree": [],
        "untracked": [],
    }
    specs = [
        ("base diff", ["diff", "--name-only", f"{base}...HEAD"]),
        ("working tree", ["diff", "--name-only", "HEAD"]),
        ("untracked", ["ls-files", "--others", "--exclude-standard"]),
    ]
    for label, args in specs:
        lines, result = git_lines(root, args)
        groups[label] = lines
        if result.returncode != 0:
            message = result.stderr.strip() or result.stdout.strip() or "git command failed"
            errors.append(f"{label}: {sanitize_line(message)}")
    return groups, errors


def all_changed_paths(groups: dict[str, list[str]]) -> list[str]:
    paths: list[str] = []
    for group_paths in groups.values():
        paths.extend(group_paths)
    return dedupe(paths)


def path_matches(path: str, rule: str) -> bool:
    if rule.endswith("/"):
        return path == rule.rstrip("/") or path.startswith(rule)
    return path == rule or path.startswith(f"{rule}/")


def allowed_by_scope(path: str, allowed_rules: tuple[str, ...]) -> bool:
    return any(path_matches(path, rule) for rule in allowed_rules)


def check_generated_package_folder(root: Path) -> GateResult:
    package_path = root / PACKAGE_ROOT
    if package_path.exists():
        return GateResult(
            name="generated package folder absent",
            ok=False,
            detail=f"found {PACKAGE_ROOT}/",
        )
    return GateResult(name="generated package folder absent", ok=True)


def check_pr_1001_leakage(paths: list[str]) -> GateResult:
    leaked = [path for path in paths if path in PR_1001_PATHS]
    if leaked:
        return GateResult(
            name="PR #1001 leakage absent",
            ok=False,
            detail=", ".join(leaked),
        )
    return GateResult(name="PR #1001 leakage absent", ok=True)


def check_untracked_helper(untracked: list[str]) -> GateResult:
    leaked = [
        path
        for path in untracked
        if path == LOCAL_HELPER or path.endswith(f"/{LOCAL_HELPER}")
    ]
    if leaked:
        return GateResult(
            name="untracked helper excluded",
            ok=False,
            detail=", ".join(leaked),
        )
    return GateResult(name="untracked helper excluded", ok=True)


def check_changed_file_summary(
    groups: dict[str, list[str]],
    errors: list[str],
    scope: str,
) -> GateResult:
    paths = all_changed_paths(groups)
    if errors:
        return GateResult(
            name="changed file summary",
            ok=False,
            detail="; ".join(errors),
        )

    forbidden = [
        path
        for path in paths
        if any(path_matches(path, rule) for rule in FORBIDDEN_CHANGED_PATHS)
    ]
    if forbidden:
        return GateResult(
            name="changed file summary",
            ok=False,
            detail="forbidden changed path(s): " + ", ".join(forbidden),
        )

    if scope in SCOPE_ALLOWED:
        allowed_rules = SCOPE_ALLOWED[scope]
        outside = [path for path in paths if not allowed_by_scope(path, allowed_rules)]
        if outside:
            return GateResult(
                name="changed file summary",
                ok=False,
                detail=f"outside {scope} scope: " + ", ".join(outside),
            )
    elif scope == "high-mid-pr-ready":
        return GateResult(
            name="changed file summary",
            ok=True,
            detail="high-mid-pr-ready scope reported only; auto-merge not inferred",
        )

    detail = f"{len(paths)} changed path(s) across base, working tree, and untracked scans"
    return GateResult(name="changed file summary", ok=True, detail=detail)


def print_failure_section(results: list[GateResult]) -> None:
    failures = [result for result in results if not result.ok]
    if not failures:
        return
    print("Failures:")
    for result in failures:
        suffix = ""
        if result.exit_code is not None:
            suffix = f": exit {result.exit_code}"
        elif result.detail:
            suffix = f": {result.detail}"
        print(f"- {result.name}{suffix}")
        if result.detail and result.exit_code is not None:
            print(f"  detail: {result.detail}")
        if result.excerpt:
            print("  excerpt:")
            for line in result.excerpt:
                print(f"    {line}")
    print()


def print_checks(results: list[GateResult]) -> None:
    print("Checks:")
    for result in results:
        detail = f" ({result.detail})" if result.ok and result.detail else ""
        print(f"- {result.name}: {result.status}{detail}")
    print()


def print_changed_files(groups: dict[str, list[str]]) -> None:
    print("Changed files:")
    for label, paths in groups.items():
        print(f"- {label}: {len(paths)}")
        for path in paths[:20]:
            print(f"  {path}")
        if len(paths) > 20:
            print(f"  ... {len(paths) - 20} more")
    print()


def run_all(root: Path, base: str, scope: str) -> tuple[list[GateResult], dict[str, list[str]]]:
    python = sys.executable
    command_gates = [
        ("git diff --check", ["git", "diff", "--check"]),
        ("repo safety", [python, "scripts/check_repo_safety.py"]),
        (f"repo safety --base {base}", [python, "scripts/check_repo_safety.py", "--base", base]),
        (
            "report regression checker",
            [python, "scripts/check_clean_package_dry_run_reports.py"],
        ),
        ("dry-run default", [python, "scripts/clean_package_dry_run.py"]),
        (
            "dry-run text",
            [python, "scripts/clean_package_dry_run.py", "--format", "text"],
        ),
        (
            "dry-run markdown",
            [python, "scripts/clean_package_dry_run.py", "--format", "markdown"],
        ),
        (
            "dry-run json",
            [python, "scripts/clean_package_dry_run.py", "--format", "json"],
        ),
    ]

    results = [run_gate(root, name, command) for name, command in command_gates]
    groups, errors = collect_changed_files(root, base)
    paths = all_changed_paths(groups)
    results.append(check_generated_package_folder(root))
    results.append(check_pr_1001_leakage(paths))
    results.append(check_untracked_helper(groups["untracked"]))
    results.append(check_changed_file_summary(groups, errors, scope))
    return results, groups


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = repo_root()
    results, groups = run_all(root, args.base, args.scope)
    ok = all(result.ok for result in results)

    print("Local Safety Gates")
    print()
    print(f"Base: {args.base}")
    print(f"Scope: {args.scope}")
    print(f"Status: {'OK' if ok else 'FAILED'}")
    print()
    print_failure_section(results)
    print_checks(results)
    print_changed_files(groups)
    print("No package output was generated.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
