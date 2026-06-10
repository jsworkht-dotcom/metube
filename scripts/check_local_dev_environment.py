#!/usr/bin/env python3
"""Check local development environment readiness before Codex task work.

The checker is intentionally read-only. It prints a concise text report and
does not write files, create branches, change Git configuration, call GitHub
write APIs, or create generated package output.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


DEFAULT_BASE = "fork/master"
DEFAULT_EXPECTED_BRANCH = "master"
PACKAGE_ROOT = "動画保存ツール_ローカル専用"
LOCAL_HELPER = "export_context_updated.py"
EXPECTED_FORK_REMOTE = "jsworkht-dotcom/metube"
EXPECTED_ORIGIN_REMOTE = "alexta69/metube"
PR_1001_PATHS = {
    "docker-compose.local.yml",
    "docs/local-only.md",
}
REQUIRED_LOCAL_TOOLS = (
    "scripts/run_local_safety_gates.py",
    "scripts/check_safety_wording.py",
    "scripts/generate_pr_body.py",
    "scripts/check_repo_safety.py",
    "scripts/check_clean_package_dry_run_reports.py",
    "scripts/clean_package_dry_run.py",
)
STATUS_ORDER = {
    "OK": 0,
    "SKIPPED": 1,
    "WARN": 2,
    "ERROR": 3,
}
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
class CheckResult:
    category: str
    label: str
    status: str
    detail: str = ""
    action: str = ""
    notes: list[str] = field(default_factory=list)

    @property
    def is_error(self) -> bool:
        return self.status == "ERROR"

    @property
    def is_finding(self) -> bool:
        return self.status in {"WARN", "ERROR"}


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run read-only local development environment preflight checks. "
            "The checker writes no files and performs no corrective actions."
        )
    )
    parser.add_argument(
        "--base",
        default=DEFAULT_BASE,
        help=f"Baseline ref to check before task work. Default: {DEFAULT_BASE}.",
    )
    parser.add_argument(
        "--expected-branch",
        default=DEFAULT_EXPECTED_BRANCH,
        help=f"Expected current branch for task start. Default: {DEFAULT_EXPECTED_BRANCH}.",
    )
    parser.add_argument(
        "--repo-root",
        help="Optional explicit repository root. Defaults to the parent of this script.",
    )
    github = parser.add_mutually_exclusive_group()
    github.add_argument(
        "--check-github",
        action="store_true",
        help="Run stricter read-only GitHub CLI session checks.",
    )
    github.add_argument(
        "--no-github",
        action="store_true",
        help="Skip GitHub CLI session checks.",
    )
    parser.add_argument(
        "--max-locks",
        type=int,
        default=20,
        help="Maximum Git lock file paths to print. Default: 20.",
    )
    return parser.parse_args(argv)


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip().strip('"')


def dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        normalized = normalize_path(item)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def sanitize_text(text: str) -> str:
    sanitized = URL_RE.sub("[redacted-url]", text)
    sanitized = ENV_SECRET_RE.sub("[redacted-secret]", sanitized)
    return KEY_VALUE_SECRET_RE.sub(lambda match: f"{match.group(1)}=[redacted]", sanitized)


def short_message(result: CommandResult) -> str:
    combined = "\n".join(part for part in (result.stderr, result.stdout) if part)
    for line in combined.splitlines():
        stripped = sanitize_text(line.strip())
        if stripped:
            return stripped
    return "command failed"


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
        return CommandResult(2, "", sanitize_text(str(exc)))
    return CommandResult(result.returncode, result.stdout, result.stderr)


def run_git(root: Path, args: list[str]) -> CommandResult:
    return run_process(root, ["git", *args])


def git_lines(root: Path, args: list[str]) -> tuple[list[str], CommandResult]:
    result = run_git(root, args)
    if result.returncode != 0:
        return [], result
    return [normalize_path(line) for line in result.stdout.splitlines() if line.strip()], result


def same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left.resolve())) == os.path.normcase(str(right.resolve()))


def path_matches(path: str, rule: str) -> bool:
    normalized = normalize_path(path)
    if rule.endswith("/"):
        return normalized == rule.rstrip("/") or normalized.startswith(rule)
    return normalized == rule or normalized.startswith(f"{rule}/")


def rel_to_root(root: Path, path: Path) -> str:
    try:
        return normalize_path(str(path.resolve().relative_to(root.resolve())))
    except ValueError:
        return normalize_path(str(path))


def check_python_runtime() -> CheckResult:
    executable = sys.executable or ""
    version = ".".join(str(part) for part in sys.version_info[:3])
    executable_ok = bool(executable)
    if executable:
        try:
            executable_ok = Path(executable).exists()
        except OSError:
            executable_ok = False

    discovered = []
    for name in ("python", "python3", "py"):
        discovered.append(f"{name}={'found' if shutil.which(name) else 'missing'}")

    detail = (
        f"sys.executable={executable or 'unknown'}; "
        f"version={version}; can_run_scripts={'yes' if executable_ok else 'no'}; "
        + ", ".join(discovered)
    )
    if executable_ok:
        return CheckResult("python_runtime", "Python runtime discovery", "OK", detail)
    return CheckResult(
        "python_runtime",
        "Python runtime discovery",
        "ERROR",
        detail,
        "use the configured bundled Python runtime before starting",
    )


def check_git_repository(root: Path) -> CheckResult:
    if not shutil.which("git"):
        return CheckResult(
            "git_repository",
            "Git repository",
            "ERROR",
            "git command not found on PATH",
            "restore Git command availability before starting",
        )

    top_result = run_git(root, ["rev-parse", "--show-toplevel"])
    status_result = run_git(root, ["status", "--short", "--branch"])
    remote_result = run_git(root, ["remote", "-v"])

    if top_result.returncode != 0:
        return CheckResult(
            "git_repository",
            "Git repository",
            "ERROR",
            short_message(top_result),
            "run the checker inside the expected repository",
        )
    top_level = Path(top_result.stdout.strip())
    if not same_path(top_level, root):
        return CheckResult(
            "git_repository",
            "Git repository",
            "ERROR",
            f"git top-level is {normalize_path(str(top_level))}; expected {normalize_path(str(root))}",
            "use the intended repository root before starting",
        )
    if status_result.returncode != 0:
        return CheckResult(
            "git_repository",
            "Git repository",
            "ERROR",
            short_message(status_result),
            "resolve Git status access before starting",
        )
    if remote_result.returncode != 0:
        return CheckResult(
            "git_repository",
            "Git repository",
            "ERROR",
            short_message(remote_result),
            "resolve Git remote metadata access before starting",
        )
    branch_line = status_result.stdout.splitlines()[0].strip() if status_result.stdout else "unknown"
    return CheckResult(
        "git_repository",
        "Git repository",
        "OK",
        f"top-level matches repo root; status={sanitize_text(branch_line)}",
    )


def check_git_branch(root: Path, expected_branch: str) -> CheckResult:
    branch_result = run_git(root, ["branch", "--show-current"])
    status_result = run_git(root, ["status", "--short", "--branch"])
    if branch_result.returncode != 0:
        return CheckResult(
            "git_branch",
            "Git branch baseline",
            "ERROR",
            short_message(branch_result),
            "resolve Git branch metadata access before starting",
        )
    if status_result.returncode != 0:
        return CheckResult(
            "git_branch",
            "Git branch baseline",
            "ERROR",
            short_message(status_result),
            "resolve Git status access before starting",
        )

    current = branch_result.stdout.strip() or "DETACHED"
    branch_line = status_result.stdout.splitlines()[0].strip() if status_result.stdout else "unknown"
    detail = f"current={current}; expected={expected_branch}; status={sanitize_text(branch_line)}"
    if current != expected_branch:
        return CheckResult(
            "git_branch",
            "Git branch baseline",
            "WARN",
            detail,
            "confirm this branch is intentional for the current task",
        )
    return CheckResult("git_branch", "Git branch baseline", "OK", detail)


def readable_directory(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing"
    if not path.is_dir():
        return False, "not a directory"
    try:
        iterator = path.iterdir()
        next(iterator, None)
    except OSError as exc:
        return False, sanitize_text(str(exc))
    return True, "readable"


def check_git_metadata_access(root: Path) -> CheckResult:
    paths = [root / ".git", root / ".git" / "refs", root / ".git" / "refs" / "heads"]
    problems: list[str] = []
    for path in paths:
        ok, message = readable_directory(path)
        if not ok:
            problems.append(f"{rel_to_root(root, path)}: {message}")
    if problems:
        return CheckResult(
            "git_metadata_access",
            "Git metadata access",
            "ERROR",
            "; ".join(problems),
            "resolve Git metadata permission issue before branch creation",
        )
    return CheckResult("git_metadata_access", "Git metadata access", "OK", "required metadata paths readable")


def find_git_locks(root: Path) -> tuple[list[str], list[str]]:
    git_dir = root / ".git"
    locks: list[str] = []
    errors: list[str] = []

    def onerror(error: OSError) -> None:
        errors.append(sanitize_text(str(error)))

    for current_root, _dirs, files in os.walk(git_dir, onerror=onerror):
        current = Path(current_root)
        for filename in files:
            if filename.endswith(".lock"):
                locks.append(rel_to_root(root, current / filename))
    return sorted(locks), errors


def is_blocking_lock(path: str) -> bool:
    normalized = normalize_path(path)
    return (
        normalized == ".git/index.lock"
        or normalized == ".git/HEAD.lock"
        or normalized == ".git/packed-refs.lock"
        or normalized.startswith(".git/refs/heads/")
    )


def check_git_lock_files(root: Path, max_locks: int) -> CheckResult:
    locks, errors = find_git_locks(root)
    if errors:
        return CheckResult(
            "git_lock_files",
            "Git lock files",
            "ERROR",
            "; ".join(errors[:3]),
            "resolve Git metadata permission issue before branch creation",
        )
    if not locks:
        return CheckResult("git_lock_files", "Git lock files", "OK", "no .lock files under .git")

    blocking = [path for path in locks if is_blocking_lock(path)]
    shown = locks[:max_locks]
    detail = f"count={len(locks)}; showing={', '.join(shown)}"
    if len(locks) > max_locks:
        detail += f"; omitted={len(locks) - max_locks}"
    if blocking:
        return CheckResult(
            "git_lock_files",
            "Git lock files",
            "ERROR",
            detail,
            "resolve blocking Git lock files before branch creation",
        )
    return CheckResult(
        "git_lock_files",
        "Git lock files",
        "WARN",
        detail,
        "review stale-looking Git lock files before starting",
    )


def check_github_cli_session(root: Path, strict: bool, skipped: bool) -> CheckResult:
    if skipped:
        return CheckResult(
            "github_cli_session",
            "GitHub CLI session state",
            "SKIPPED",
            "--no-github selected",
        )

    gh_path = shutil.which("gh")
    if not gh_path:
        status = "ERROR" if strict else "WARN"
        return CheckResult(
            "github_cli_session",
            "GitHub CLI session state",
            status,
            "gh command not found on PATH",
            "verify GitHub CLI availability before PR work",
        )

    auth_result = run_process(root, ["gh", "auth", "status", "-h", "github.com"])
    if auth_result.returncode != 0:
        status = "ERROR" if strict else "WARN"
        return CheckResult(
            "github_cli_session",
            "GitHub CLI session state",
            status,
            "gh auth status unavailable; credential output omitted",
            "verify GitHub CLI session state before PR work",
        )

    if strict:
        repo_result = run_process(
            root,
            ["gh", "repo", "view", "jsworkht-dotcom/metube", "--json", "nameWithOwner"],
        )
        if repo_result.returncode != 0:
            return CheckResult(
                "github_cli_session",
                "GitHub CLI session state",
                "ERROR",
                "gh repo read check unavailable; command output omitted",
                "verify GitHub CLI read access before PR work",
            )
        return CheckResult(
            "github_cli_session",
            "GitHub CLI session state",
            "OK",
            "gh auth status and repo read check succeeded",
        )

    return CheckResult(
        "github_cli_session",
        "GitHub CLI session state",
        "OK",
        "gh auth status succeeded",
    )


def parse_remotes(remote_output: str) -> dict[str, list[str]]:
    remotes: dict[str, list[str]] = {}
    for line in remote_output.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        remotes.setdefault(parts[0], []).append(parts[1])
    return remotes


def urls_contain(urls: list[str], expected: str) -> bool:
    lowered = [url.lower() for url in urls]
    return any(expected.lower() in url for url in lowered)


def any_remote_contains(remotes: dict[str, list[str]], expected: str) -> bool:
    return any(urls_contain(urls, expected) for urls in remotes.values())


def check_remote_configuration(root: Path) -> CheckResult:
    result = run_git(root, ["remote", "-v"])
    if result.returncode != 0:
        return CheckResult(
            "remote_configuration",
            "remote configuration",
            "ERROR",
            short_message(result),
            "resolve Git remote metadata access before starting",
        )
    remotes = parse_remotes(result.stdout)
    problems: list[str] = []
    warnings: list[str] = []

    fork_urls = remotes.get("fork", [])
    if not fork_urls:
        if any_remote_contains(remotes, EXPECTED_FORK_REMOTE):
            warnings.append("fork URL exists under a different remote name")
        else:
            problems.append("fork remote missing")
    elif not urls_contain(fork_urls, EXPECTED_FORK_REMOTE):
        if any_remote_contains(remotes, EXPECTED_FORK_REMOTE):
            warnings.append("expected fork URL exists under a different remote name")
        else:
            problems.append("fork remote URL does not match expected fork")

    origin_urls = remotes.get("origin", [])
    if not origin_urls:
        if any_remote_contains(remotes, EXPECTED_ORIGIN_REMOTE):
            warnings.append("origin URL exists under a different remote name")
        else:
            warnings.append("origin remote missing")
    elif not urls_contain(origin_urls, EXPECTED_ORIGIN_REMOTE):
        if any_remote_contains(remotes, EXPECTED_ORIGIN_REMOTE):
            warnings.append("expected origin URL exists under a different remote name")
        else:
            warnings.append("origin remote URL does not match expected upstream")

    if problems:
        return CheckResult(
            "remote_configuration",
            "remote configuration",
            "ERROR",
            "; ".join(problems + warnings),
            "restore the fork remote baseline before starting",
        )
    if warnings:
        return CheckResult(
            "remote_configuration",
            "remote configuration",
            "WARN",
            "; ".join(warnings),
            "review remote names before PR work",
        )
    return CheckResult("remote_configuration", "remote configuration", "OK", "fork and origin remotes match expected repositories")


def check_baseline_ref(root: Path, base: str) -> CheckResult:
    result = run_git(root, ["rev-parse", "--verify", base])
    label = f"baseline ref {base}"
    if result.returncode != 0:
        return CheckResult(
            "baseline_ref",
            label,
            "ERROR",
            short_message(result),
            "run fetch from the fork remote before starting",
        )
    commit = result.stdout.strip()[:12]
    return CheckResult("baseline_ref", label, "OK", f"{base} available at {commit}")


def parse_status_counts(porcelain: str) -> tuple[int, int]:
    modified = 0
    untracked = 0
    for raw_line in porcelain.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("?? "):
            untracked += 1
        else:
            modified += 1
    return modified, untracked


def check_working_tree_summary(root: Path) -> CheckResult:
    status_result = run_git(root, ["status", "--short", "--branch"])
    porcelain_result = run_git(root, ["status", "--porcelain=v1", "--untracked-files=normal"])
    if status_result.returncode != 0:
        return CheckResult(
            "working_tree_summary",
            "working tree summary",
            "ERROR",
            short_message(status_result),
            "resolve Git status access before starting",
        )
    if porcelain_result.returncode != 0:
        return CheckResult(
            "working_tree_summary",
            "working tree summary",
            "ERROR",
            short_message(porcelain_result),
            "resolve Git working tree scan before starting",
        )
    branch_line = status_result.stdout.splitlines()[0].strip() if status_result.stdout else "unknown"
    modified, untracked = parse_status_counts(porcelain_result.stdout)
    detail = f"modified={modified}; untracked={untracked}; branch_status={sanitize_text(branch_line)}"
    if modified or untracked:
        return CheckResult(
            "working_tree_summary",
            "working tree summary",
            "WARN",
            detail,
            "review, commit, or shelve local changes before starting a new task",
        )
    return CheckResult("working_tree_summary", "working tree summary", "OK", detail)


def helper_rule_present(root: Path) -> tuple[bool, str]:
    exclude_path = root / ".git" / "info" / "exclude"
    if not exclude_path.exists():
        return False, ".git/info/exclude missing"
    try:
        lines = exclude_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return False, sanitize_text(str(exc))
    accepted = {LOCAL_HELPER, f"/{LOCAL_HELPER}", f"./{LOCAL_HELPER}"}
    for line in lines:
        stripped = normalize_path(line.split("#", 1)[0].strip())
        if stripped in accepted:
            return True, "helper rule present"
    return False, "helper rule missing from .git/info/exclude"


def check_local_helper_exclusion(root: Path) -> CheckResult:
    untracked, result = git_lines(root, ["ls-files", "--others", "--exclude-standard"])
    if result.returncode != 0:
        return CheckResult(
            "local_helper_exclusion",
            "local helper exclusion",
            "ERROR",
            short_message(result),
            "resolve untracked-file scan before starting",
        )

    helper_exists = (root / LOCAL_HELPER).exists()
    helper_untracked = any(path == LOCAL_HELPER or path.endswith(f"/{LOCAL_HELPER}") for path in untracked)
    if helper_untracked:
        return CheckResult(
            "local_helper_exclusion",
            "local helper exclusion",
            "ERROR",
            f"{LOCAL_HELPER} appears as untracked",
            "restore local helper exclusion before starting; do not change .gitignore",
        )

    if helper_exists:
        has_rule, message = helper_rule_present(root)
        if not has_rule:
            return CheckResult(
                "local_helper_exclusion",
                "local helper exclusion",
                "ERROR",
                message,
                "restore local helper exclusion before starting; do not change .gitignore",
            )
        return CheckResult(
            "local_helper_exclusion",
            "local helper exclusion",
            "OK",
            f"{LOCAL_HELPER} exists and remains excluded",
        )
    return CheckResult(
        "local_helper_exclusion",
        "local helper exclusion",
        "OK",
        f"{LOCAL_HELPER} not present in untracked output",
    )


def check_generated_output_absence(root: Path) -> CheckResult:
    if (root / PACKAGE_ROOT).exists():
        return CheckResult(
            "generated_output_absence",
            "generated package folder absent",
            "ERROR",
            f"{PACKAGE_ROOT}/ exists at repository root",
            "remove generated package output only after human-approved cleanup",
        )
    return CheckResult(
        "generated_output_absence",
        "generated package folder absent",
        "OK",
        f"{PACKAGE_ROOT}/ absent",
    )


def diff_paths(root: Path, args: list[str]) -> tuple[list[str], str | None]:
    lines, result = git_lines(root, args)
    if result.returncode != 0:
        return [], short_message(result)
    return dedupe(lines), None


def check_pr1001_leakage_precheck(root: Path, base: str) -> CheckResult:
    base_paths, base_error = diff_paths(root, ["diff", "--name-only", f"{base}...HEAD"])
    working_paths, working_error = diff_paths(root, ["diff", "--name-only", "HEAD"])
    if base_error or working_error:
        errors = [error for error in (base_error, working_error) if error]
        return CheckResult(
            "pr1001_leakage_precheck",
            "PR #1001 leakage precheck",
            "ERROR",
            "; ".join(errors),
            "resolve diff baseline access before starting",
        )
    leaked = sorted(path for path in dedupe([*base_paths, *working_paths]) if path in PR_1001_PATHS)
    if leaked:
        return CheckResult(
            "pr1001_leakage_precheck",
            "PR #1001 leakage precheck",
            "ERROR",
            ", ".join(leaked),
            "keep upstream PR #1001 files out of this fork-only task",
        )
    return CheckResult(
        "pr1001_leakage_precheck",
        "PR #1001 leakage precheck",
        "OK",
        f"base_diff={len(base_paths)}; working_tree={len(working_paths)}; no PR #1001 files",
    )


def check_tooling_availability(root: Path) -> CheckResult:
    missing = [path for path in REQUIRED_LOCAL_TOOLS if not (root / path).is_file()]
    if missing:
        return CheckResult(
            "tooling_availability",
            "local safety tools present",
            "ERROR",
            ", ".join(missing),
            "restore required local safety tools before starting",
        )
    return CheckResult(
        "tooling_availability",
        "local safety tools present",
        "OK",
        f"{len(REQUIRED_LOCAL_TOOLS)} required local safety tools present",
    )


def run_checks(args: argparse.Namespace) -> list[CheckResult]:
    root = Path(args.repo_root).resolve() if args.repo_root else default_repo_root()
    return [
        check_python_runtime(),
        check_git_repository(root),
        check_git_branch(root, args.expected_branch),
        check_git_metadata_access(root),
        check_git_lock_files(root, args.max_locks),
        check_github_cli_session(root, strict=args.check_github, skipped=args.no_github),
        check_remote_configuration(root),
        check_baseline_ref(root, args.base),
        check_working_tree_summary(root),
        check_local_helper_exclusion(root),
        check_generated_output_absence(root),
        check_pr1001_leakage_precheck(root, args.base),
        check_tooling_availability(root),
    ]


def print_findings(results: list[CheckResult]) -> None:
    findings = [result for result in results if result.is_finding]
    if not findings:
        return
    print("Findings:")
    for result in findings:
        print(f"- {result.category}: {result.status}")
        if result.detail:
            print(f"  detail: {sanitize_text(result.detail)}")
        if result.action:
            print(f"  action: {sanitize_text(result.action)}")
    print()


def print_checks(results: list[CheckResult]) -> None:
    print("Checks:")
    for result in results:
        detail = f" ({sanitize_text(result.detail)})" if result.detail else ""
        print(f"- {result.label}: {result.status}{detail}")
    print()


def report_status(results: list[CheckResult]) -> str:
    return "FAILED" if any(result.is_error for result in results) else "OK"


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0

    if args.max_locks < 1:
        print("Preflight Environment Check")
        print()
        print("Status: FAILED")
        print()
        print("usage error: --max-locks must be greater than zero")
        return 2

    try:
        results = run_checks(args)
    except Exception as exc:  # pragma: no cover - final safety net for CLI use
        print("Preflight Environment Check")
        print()
        print("Status: FAILED")
        print()
        print(f"runtime error: {sanitize_text(str(exc))}")
        return 2

    status = report_status(results)
    print("Preflight Environment Check")
    print()
    print(f"Status: {status}")
    print()
    print_findings(results)
    print_checks(results)

    if status == "OK":
        if any(STATUS_ORDER[result.status] >= STATUS_ORDER["WARN"] for result in results):
            print("Ready for Codex task start after reviewing WARN findings.")
        else:
            print("Ready for Codex task start.")
        return 0

    print("Do not start the task until ERROR findings are resolved.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
