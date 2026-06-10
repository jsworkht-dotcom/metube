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

REQUIRED_MANIFEST_ENTRY_FIELDS = {
    "package_relative_path",
    "source_candidate",
    "kind",
    "target_os",
    "target_arch",
    "generated",
    "required",
    "include_reason",
    "license_notice_required",
    "review_status",
    "safety_notes",
    "source_status",
    "output_status",
    "human_review_required",
}

REVIEW_RELATED_MANIFEST_KINDS = {
    "notice",
    "license",
    "inventory",
    "developer_manifest",
}

REQUIRED_OUTPUT_GROUP_FIELDS = {
    "group_key",
    "label",
    "description",
    "package_relative_root",
    "would_create_directories",
    "would_create_files",
    "would_generate_future_outputs",
    "would_copy_source_groups",
    "would_skip_or_exclude",
    "required",
    "generated_now",
    "human_review_required",
    "safety_notes",
    "review_status",
}

REQUIRED_OUTPUT_GROUP_KEYS = {
    "beginner_guides",
    "developer_docs",
    "manifest_outputs",
    "notice_outputs",
    "license_outputs",
    "inventory_outputs",
    "windows_runtime_outputs",
    "mac_runtime_outputs",
    "save_folder_placeholders",
    "troubleshooting_outputs",
    "excluded_outputs",
}

OUTPUT_GROUP_REVIEW_STATUSES = {
    "present",
    "missing",
    "candidate_only",
    "source_draft",
    "legal_not_final",
    "package_time_review_required",
    "not_applicable_this_phase",
}

CHECK_NAMES = (
    "all modes exit 0",
    "default text output",
    "--format text output",
    "text manifest entries",
    "text output groups",
    "--format markdown required sections",
    "--format markdown manifest entries",
    "--format markdown output groups",
    "--format json parse",
    "--format json required fields",
    "--format json manifest entries",
    "--format json output groups",
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

    if "manifest_entries" not in default:
        add_failure(
            failures,
            check_status,
            "text manifest entries",
            "default text output missing manifest_entries",
        )
    if "manifest_entries" not in text:
        add_failure(
            failures,
            check_status,
            "text manifest entries",
            "--format text output missing manifest_entries",
        )

    if "output_groups" not in default:
        add_failure(
            failures,
            check_status,
            "text output groups",
            "default text output missing output_groups",
        )
    if "output_groups" not in text:
        add_failure(
            failures,
            check_status,
            "text output groups",
            "--format text output missing output_groups",
        )


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

    if "Manifest Entry Candidates" not in output:
        add_failure(
            failures,
            check_status,
            "--format markdown manifest entries",
            "Markdown output missing Manifest Entry Candidates",
        )

    if "Output Groups" not in output:
        add_failure(
            failures,
            check_status,
            "--format markdown output groups",
            "Markdown output missing Output Groups",
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


def check_json_manifest_entries(
    json_data: dict[str, object] | None,
    failures: list[str],
    check_status: dict[str, bool],
) -> None:
    check_name = "--format json manifest entries"
    if json_data is None:
        add_failure(
            failures,
            check_status,
            check_name,
            "JSON data unavailable for manifest entry checks",
        )
        return

    preview = json_data.get("package_manifest_preview")
    if not isinstance(preview, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "package_manifest_preview is not an object",
        )
        return

    entries = preview.get("manifest_entries")
    if not isinstance(entries, list) or not entries:
        add_failure(
            failures,
            check_status,
            check_name,
            "manifest_entries is not a non-empty list",
        )
        return

    summary = preview.get("manifest_entry_summary")
    if not isinstance(summary, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "manifest_entry_summary is not an object",
        )

    beginner_present = False
    review_related_present = False
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            add_failure(
                failures,
                check_status,
                check_name,
                f"manifest entry {index} is not an object",
            )
            continue

        missing = REQUIRED_MANIFEST_ENTRY_FIELDS - set(entry)
        if missing:
            add_failure(
                failures,
                check_status,
                check_name,
                f"manifest entry {index} missing fields: {', '.join(sorted(missing))}",
            )

        if entry.get("generated") is not False:
            add_failure(
                failures,
                check_status,
                check_name,
                f"manifest entry {index} generated is not false",
            )
        if entry.get("human_review_required") is not True:
            add_failure(
                failures,
                check_status,
                check_name,
                f"manifest entry {index} human_review_required is not true",
            )
        if not isinstance(entry.get("safety_notes"), list):
            add_failure(
                failures,
                check_status,
                check_name,
                f"manifest entry {index} safety_notes is not a list",
            )

        kind = entry.get("kind")
        if kind == "beginner_guide":
            beginner_present = True
        if kind in REVIEW_RELATED_MANIFEST_KINDS:
            review_related_present = True

    if not beginner_present:
        add_failure(
            failures,
            check_status,
            check_name,
            "missing beginner guide manifest entry",
        )
    if not review_related_present:
        add_failure(
            failures,
            check_status,
            check_name,
            "missing notice/license/inventory/developer manifest entry",
        )


def check_json_output_groups(
    json_data: dict[str, object] | None,
    failures: list[str],
    check_status: dict[str, bool],
) -> None:
    check_name = "--format json output groups"
    if json_data is None:
        add_failure(
            failures,
            check_status,
            check_name,
            "JSON data unavailable for output group checks",
        )
        return

    prediction = json_data.get("package_output_diff_prediction")
    if not isinstance(prediction, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "package_output_diff_prediction is not an object",
        )
        return

    groups = prediction.get("output_groups")
    if not isinstance(groups, list) or not groups:
        add_failure(
            failures,
            check_status,
            check_name,
            "output_groups is not a non-empty list",
        )
        return

    summary = prediction.get("output_group_summary")
    if not isinstance(summary, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "output_group_summary is not an object",
        )
    else:
        if summary.get("total") != len(groups):
            add_failure(
                failures,
                check_status,
                check_name,
                "output_group_summary total does not match output_groups length",
            )
        if summary.get("generated_now") is not False:
            add_failure(
                failures,
                check_status,
                check_name,
                "output_group_summary generated_now is not false",
            )
        if summary.get("human_review_required") is not True:
            add_failure(
                failures,
                check_status,
                check_name,
                "output_group_summary human_review_required is not true",
            )
        if not isinstance(summary.get("by_group"), dict):
            add_failure(
                failures,
                check_status,
                check_name,
                "output_group_summary by_group is not an object",
            )

    seen_group_keys: set[str] = set()
    for index, group in enumerate(groups):
        if not isinstance(group, dict):
            add_failure(
                failures,
                check_status,
                check_name,
                f"output group {index} is not an object",
            )
            continue

        missing = REQUIRED_OUTPUT_GROUP_FIELDS - set(group)
        if missing:
            add_failure(
                failures,
                check_status,
                check_name,
                f"output group {index} missing fields: {', '.join(sorted(missing))}",
            )

        group_key = group.get("group_key")
        if isinstance(group_key, str):
            seen_group_keys.add(group_key)
        else:
            add_failure(
                failures,
                check_status,
                check_name,
                f"output group {index} group_key is not a string",
            )

        for list_field in (
            "would_create_directories",
            "would_create_files",
            "would_generate_future_outputs",
            "would_copy_source_groups",
            "would_skip_or_exclude",
            "safety_notes",
        ):
            if not isinstance(group.get(list_field), list):
                add_failure(
                    failures,
                    check_status,
                    check_name,
                    f"output group {index} {list_field} is not a list",
                )

        if group.get("generated_now") is not False:
            add_failure(
                failures,
                check_status,
                check_name,
                f"output group {index} generated_now is not false",
            )
        if group.get("human_review_required") is not True:
            add_failure(
                failures,
                check_status,
                check_name,
                f"output group {index} human_review_required is not true",
            )
        if group.get("review_status") not in OUTPUT_GROUP_REVIEW_STATUSES:
            add_failure(
                failures,
                check_status,
                check_name,
                f"output group {index} review_status is not recognized",
            )

    missing_group_keys = REQUIRED_OUTPUT_GROUP_KEYS - seen_group_keys
    if missing_group_keys:
        add_failure(
            failures,
            check_status,
            check_name,
            "missing output groups: " + ", ".join(sorted(missing_group_keys)),
        )


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
    check_json_manifest_entries(json_data, failures, check_status)
    check_json_output_groups(json_data, failures, check_status)
    check_cross_format_consistency(results, json_data, failures, check_status)
    check_generated_package_absent(root, failures, check_status)

    print_report(check_status, failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
