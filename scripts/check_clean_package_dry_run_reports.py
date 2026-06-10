"""Check clean-package dry-run report mode regressions.

This checker is report-only. It runs the dry-run script, reads stdout, and does
not create files, temp files, package output, or report artifacts.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


PACKAGE_ROOT = "動画保存ツール_ローカル専用"
DRY_RUN_SCRIPT = "scripts/clean_package_dry_run.py"

MODES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("default", ()),
    ("text", ("--format", "text")),
    ("markdown", ("--format", "markdown")),
    ("json", ("--format", "json")),
)

REQUIRED_MARKDOWN_SECTIONS = (
    "# Clean Package Dry-Run Report",
    "## Summary",
    "## Status",
    "## Risk Classification",
    "## Package Manifest Preview",
    "## Package Output Diff Prediction",
    "## Notice / Guide Source Coverage",
    "## Excluded Paths Summary",
    "## Blockers",
    "## Warnings",
    "## Human Review Checklist",
    "## No-Generation Boundary",
)

REQUIRED_JSON_FIELDS = (
    "schema_version",
    "report_type",
    "report_format",
    "mode",
    "status",
    "exit_code",
    "generated_artifacts",
    "checked_at",
    "repository",
    "package",
    "package_manifest_preview",
    "package_output_diff_prediction",
    "source_coverage",
    "excluded_paths_summary",
    "validation",
    "warnings",
    "blockers",
    "safety_flags",
    "human_review",
    "next_step",
)

CHECK_NAMES = (
    "all modes exit 0",
    "default text output",
    "--format text output",
    "--format markdown required sections",
    "--format json parse",
    "--format json required fields",
    "cross-format status consistency",
    "generated package folder absent",
)


@dataclass(frozen=True)
class ModeResult:
    name: str
    args: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def redact_sensitive_text(text: str) -> str:
    redacted = re.sub(
        r"(?i)\b(cookie|token|secret|credential|password|api[_-]?key)\b"
        r"(\s*[:=]\s*)\S+",
        r"\1\2<omitted>",
        text,
    )
    redacted = re.sub(r"https?://\S+", "<url omitted>", redacted)
    return redacted


def short_message(stdout: str, stderr: str) -> str:
    source = stderr.strip() or stdout.strip()
    if not source:
        return "no output"
    lines = [redact_sensitive_text(line.strip()) for line in source.splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        return "no output"
    summary = " | ".join(lines[:4])
    if len(summary) > 320:
        return summary[:317] + "..."
    return summary


def run_mode(root: Path, name: str, args: tuple[str, ...]) -> ModeResult:
    command = [sys.executable, str(root / DRY_RUN_SCRIPT), *args]
    result = subprocess.run(
        command,
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return ModeResult(
        name=name,
        args=args,
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )


def starts_like_json(output: str) -> bool:
    return output.lstrip().startswith("{")


def markdown_section(output: str, heading: str) -> str:
    start = output.find(heading)
    if start < 0:
        return ""
    next_heading = output.find("\n## ", start + len(heading))
    if next_heading < 0:
        return output[start:]
    return output[start:next_heading]


def add_failure(
    failures: list[str],
    check_status: dict[str, bool],
    check_name: str,
    message: str,
) -> None:
    check_status[check_name] = False
    failures.append(f"{check_name}: {redact_sensitive_text(message)}")


def check_mode_exit_codes(
    results: dict[str, ModeResult],
    failures: list[str],
    check_status: dict[str, bool],
) -> None:
    for result in results.values():
        if result.returncode != 0:
            add_failure(
                failures,
                check_status,
                "all modes exit 0",
                (
                    f"{result.name} exited {result.returncode}; "
                    f"{short_message(result.stdout, result.stderr)}"
                ),
            )


def check_text_outputs(
    results: dict[str, ModeResult],
    failures: list[str],
    check_status: dict[str, bool],
) -> None:
    default = results["default"].stdout
    text = results["text"].stdout

    if starts_like_json(default):
        add_failure(
            failures,
            check_status,
            "default text output",
            "default output unexpectedly looks like JSON",
        )
    if "Status:\n  OK" not in default:
        add_failure(
            failures,
            check_status,
            "default text output",
            "default output missing Status: OK",
        )

    if starts_like_json(text):
        add_failure(
            failures,
            check_status,
            "--format text output",
            "--format text output unexpectedly looks like JSON",
        )
    if "Status:\n  OK" not in text:
        add_failure(
            failures,
            check_status,
            "--format text output",
            "--format text output missing Status: OK",
        )

    if default != text:
        add_failure(
            failures,
            check_status,
            "default text output",
            "default output differs from --format text output",
        )
        check_status["--format text output"] = False


def check_markdown_output(
    result: ModeResult,
    failures: list[str],
    check_status: dict[str, bool],
) -> None:
    output = result.stdout
    if starts_like_json(output):
        add_failure(
            failures,
            check_status,
            "--format markdown required sections",
            "Markdown output unexpectedly looks like JSON",
        )

    for heading in REQUIRED_MARKDOWN_SECTIONS:
        if heading not in output:
            add_failure(
                failures,
                check_status,
                "--format markdown required sections",
                f"missing Markdown section: {heading}",
            )


def check_json_output(
    result: ModeResult,
    failures: list[str],
    check_status: dict[str, bool],
) -> dict[str, object] | None:
    output = result.stdout
    if not starts_like_json(output):
        add_failure(
            failures,
            check_status,
            "--format json parse",
            "JSON output does not start with an object",
        )

    try:
        data = json.loads(output)
    except json.JSONDecodeError as exc:
        add_failure(
            failures,
            check_status,
            "--format json parse",
            f"json.loads failed at line {exc.lineno} column {exc.colno}",
        )
        return None

    if not isinstance(data, dict):
        add_failure(
            failures,
            check_status,
            "--format json parse",
            "JSON output parsed but was not an object",
        )
        return None

    missing = [key for key in REQUIRED_JSON_FIELDS if key not in data]
    if missing:
        add_failure(
            failures,
            check_status,
            "--format json required fields",
            "missing JSON fields: " + ", ".join(missing),
        )

    expected_values = {
        "report_format": "json",
        "mode": "dry_run",
        "status": "ok",
        "exit_code": 0,
        "generated_artifacts": False,
    }
    for key, expected in expected_values.items():
        if data.get(key) != expected:
            add_failure(
                failures,
                check_status,
                "--format json required fields",
                f"{key} expected {expected!r}, got {data.get(key)!r}",
            )

    if not isinstance(data.get("warnings"), list):
        add_failure(
            failures,
            check_status,
            "--format json required fields",
            "warnings is not a list",
        )
    if not isinstance(data.get("blockers"), list):
        add_failure(
            failures,
            check_status,
            "--format json required fields",
            "blockers is not a list",
        )

    return data


def check_cross_format_consistency(
    results: dict[str, ModeResult],
    json_data: dict[str, object] | None,
    failures: list[str],
    check_status: dict[str, bool],
) -> None:
    default = results["default"].stdout
    text = results["text"].stdout
    markdown = results["markdown"].stdout

    if "Status:\n  OK" not in default:
        add_failure(
            failures,
            check_status,
            "cross-format status consistency",
            "default text status is not OK",
        )
    if "Status:\n  OK" not in text:
        add_failure(
            failures,
            check_status,
            "cross-format status consistency",
            "--format text status is not OK",
        )
    if "- Status: OK" not in markdown:
        add_failure(
            failures,
            check_status,
            "cross-format status consistency",
            "Markdown status is not OK",
        )

    if json_data is None:
        add_failure(
            failures,
            check_status,
            "cross-format status consistency",
            "JSON data unavailable for consistency checks",
        )
        return

    if json_data.get("status") != "ok":
        add_failure(
            failures,
            check_status,
            "cross-format status consistency",
            "JSON status is not ok",
        )
    if json_data.get("exit_code") != 0:
        add_failure(
            failures,
            check_status,
            "cross-format status consistency",
            "JSON exit_code is not 0",
        )

    warnings = json_data.get("warnings")
    blockers = json_data.get("blockers")
    if not isinstance(warnings, list) or len(warnings) != 0:
        add_failure(
            failures,
            check_status,
            "cross-format status consistency",
            "JSON warnings count is not 0",
        )
    if not isinstance(blockers, list) or len(blockers) != 0:
        add_failure(
            failures,
            check_status,
            "cross-format status consistency",
            "JSON blockers count is not 0",
        )

    markdown_warnings = markdown_section(markdown, "## Warnings")
    markdown_blockers = markdown_section(markdown, "## Blockers")
    if "- none" not in markdown_warnings:
        add_failure(
            failures,
            check_status,
            "cross-format status consistency",
            "Markdown warnings section does not indicate none",
        )
    if "- none" not in markdown_blockers:
        add_failure(
            failures,
            check_status,
            "cross-format status consistency",
            "Markdown blockers section does not indicate none",
        )


def check_generated_package_absent(
    root: Path,
    failures: list[str],
    check_status: dict[str, bool],
) -> None:
    if (root / PACKAGE_ROOT).exists():
        add_failure(
            failures,
            check_status,
            "generated package folder absent",
            f"generated package folder exists: {PACKAGE_ROOT}/",
        )


def print_report(check_status: dict[str, bool], failures: list[str]) -> None:
    print("Clean Package Dry-Run Report Regression Check")
    print()
    print("Status: " + ("FAILED" if failures else "OK"))
    print()
    print("Checks:")
    for name in CHECK_NAMES:
        status = "OK" if check_status[name] else "FAILED"
        print(f"- {name}: {status}")

    if failures:
        print()
        print("Failures:")
        for failure in failures:
            print(f"- {failure}")

    print()
    print("No files were generated.")


def main(argv: list[str]) -> int:
    if argv:
        print("Usage: python scripts/check_clean_package_dry_run_reports.py")
        return 2

    root = repo_root()
    results = {
        name: run_mode(root, name, args)
        for name, args in MODES
    }
    failures: list[str] = []
    check_status = {name: True for name in CHECK_NAMES}

    check_mode_exit_codes(results, failures, check_status)
    check_text_outputs(results, failures, check_status)
    check_markdown_output(results["markdown"], failures, check_status)
    json_data = check_json_output(results["json"], failures, check_status)
    check_cross_format_consistency(results, json_data, failures, check_status)
    check_generated_package_absent(root, failures, check_status)

    print_report(check_status, failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
