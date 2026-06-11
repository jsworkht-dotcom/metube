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
    "## Generation Readiness Preview",
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
    "generation_readiness",
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

REQUIRED_COVERAGE_ITEM_FIELDS = {
    "coverage_key",
    "category",
    "label",
    "source_path",
    "expected_package_outputs",
    "status",
    "present",
    "required_for_generation",
    "legal_final",
    "package_time_review_required",
    "human_review_required",
    "safety_notes",
}

COVERAGE_STATUSES = {
    "present",
    "missing",
    "candidate_only",
    "source_draft",
    "legal_not_final",
    "package_time_review_required",
    "not_applicable_this_phase",
}

REQUIRED_COVERAGE_CATEGORIES = {
    "guide_source",
    "notice_source",
    "license_source",
    "inventory_source",
    "runtime_selection",
    "desktop_shell",
    "manifest_source",
}

REQUIRED_READINESS_ITEM_FIELDS = {
    "id",
    "category",
    "label",
    "status",
    "required_before_generation",
    "human_review_required",
    "evidence_source",
    "notes",
}

READINESS_STATUSES = {
    "ready",
    "blocked",
    "needs_human_review",
    "unresolved",
}

EXPECTED_ADVISORY_SCORE_VALUE = 23
EXPECTED_ADVISORY_SCORE_MAX = 100
EXPECTED_ADVISORY_SCORE_TEXT = (
    f"{EXPECTED_ADVISORY_SCORE_VALUE}/{EXPECTED_ADVISORY_SCORE_MAX}"
)

CHECK_NAMES = (
    "all modes exit 0",
    "default text output",
    "--format text output",
    "text manifest entries",
    "text output groups",
    "text source coverage status",
    "text generation readiness preview",
    "--format markdown required sections",
    "--format markdown manifest entries",
    "--format markdown output groups",
    "--format markdown source coverage status",
    "--format markdown generation readiness preview",
    "--format json parse",
    "--format json required fields",
    "--format json manifest entries",
    "--format json output groups",
    "--format json source coverage status",
    "--format json generation readiness preview",
    "cross-format status consistency",
    "cross-format readiness consistency",
    "cross-format advisory score consistency",
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

    if "Source coverage status" not in default:
        add_failure(
            failures,
            check_status,
            "text source coverage status",
            "default text output missing Source coverage status",
        )
    if "Source coverage status" not in text:
        add_failure(
            failures,
            check_status,
            "text source coverage status",
            "--format text output missing Source coverage status",
        )

    if "Generation Readiness Preview" not in default:
        add_failure(
            failures,
            check_status,
            "text generation readiness preview",
            "default text output missing Generation Readiness Preview",
        )
    if "Generation Readiness Preview" not in text:
        add_failure(
            failures,
            check_status,
            "text generation readiness preview",
            "--format text output missing Generation Readiness Preview",
        )
    if "overall: blocked" not in default:
        add_failure(
            failures,
            check_status,
            "text generation readiness preview",
            "default text readiness overall is not blocked",
        )
    if "actual_generation_approved: false" not in text:
        add_failure(
            failures,
            check_status,
            "text generation readiness preview",
            "--format text readiness actual_generation_approved is not false",
        )
    for label, output in (("default", default), ("--format text", text)):
        if "Readiness summary" not in output:
            add_failure(
                failures,
                check_status,
                "text generation readiness preview",
                f"{label} output missing Readiness summary",
            )
        if f"advisory_score: {EXPECTED_ADVISORY_SCORE_TEXT}" not in output:
            add_failure(
                failures,
                check_status,
                "text generation readiness preview",
                f"{label} output missing advisory_score: {EXPECTED_ADVISORY_SCORE_TEXT}",
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

    if "Source Coverage Status" not in output:
        add_failure(
            failures,
            check_status,
            "--format markdown source coverage status",
            "Markdown output missing Source Coverage Status",
        )

    if "## Generation Readiness Preview" not in output:
        add_failure(
            failures,
            check_status,
            "--format markdown generation readiness preview",
            "Markdown output missing Generation Readiness Preview section",
        )
    readiness_section = markdown_section(output, "## Generation Readiness Preview")
    if "- overall: `blocked`" not in readiness_section:
        add_failure(
            failures,
            check_status,
            "--format markdown generation readiness preview",
            "Markdown readiness overall is not blocked",
        )
    if "- actual_generation_approved: `false`" not in readiness_section:
        add_failure(
            failures,
            check_status,
            "--format markdown generation readiness preview",
            "Markdown readiness actual_generation_approved is not false",
        )
    if "### Readiness Summary" not in readiness_section:
        add_failure(
            failures,
            check_status,
            "--format markdown generation readiness preview",
            "Markdown readiness summary subsection is missing",
        )
    if f"- advisory_score: `{EXPECTED_ADVISORY_SCORE_TEXT}`" not in readiness_section:
        add_failure(
            failures,
            check_status,
            "--format markdown generation readiness preview",
            f"Markdown advisory_score is not {EXPECTED_ADVISORY_SCORE_TEXT}",
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


def check_json_source_coverage(
    json_data: dict[str, object] | None,
    failures: list[str],
    check_status: dict[str, bool],
) -> None:
    check_name = "--format json source coverage status"
    if json_data is None:
        add_failure(
            failures,
            check_status,
            check_name,
            "JSON data unavailable for source coverage checks",
        )
        return

    source_coverage = json_data.get("source_coverage")
    if not isinstance(source_coverage, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "source_coverage is not an object",
        )
        return

    items = source_coverage.get("coverage_items")
    if not isinstance(items, list) or not items:
        add_failure(
            failures,
            check_status,
            check_name,
            "coverage_items is not a non-empty list",
        )
        return

    summary = source_coverage.get("coverage_summary")
    if not isinstance(summary, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "coverage_summary is not an object",
        )
    else:
        if summary.get("total") != len(items):
            add_failure(
                failures,
                check_status,
                check_name,
                "coverage_summary total does not match coverage_items length",
            )
        if summary.get("generated_now") is not False:
            add_failure(
                failures,
                check_status,
                check_name,
                "coverage_summary generated_now is not false",
            )
        if summary.get("human_review_required") is not True:
            add_failure(
                failures,
                check_status,
                check_name,
                "coverage_summary human_review_required is not true",
            )
        if not isinstance(summary.get("by_category"), dict):
            add_failure(
                failures,
                check_status,
                check_name,
                "coverage_summary by_category is not an object",
            )
        if not isinstance(summary.get("by_status"), dict):
            add_failure(
                failures,
                check_status,
                check_name,
                "coverage_summary by_status is not an object",
            )

    seen_categories: set[str] = set()
    package_time_review_present = False
    present_guide_source = False
    present_notice_source = False
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            add_failure(
                failures,
                check_status,
                check_name,
                f"coverage item {index} is not an object",
            )
            continue

        missing = REQUIRED_COVERAGE_ITEM_FIELDS - set(item)
        if missing:
            add_failure(
                failures,
                check_status,
                check_name,
                f"coverage item {index} missing fields: {', '.join(sorted(missing))}",
            )

        category = item.get("category")
        if isinstance(category, str):
            seen_categories.add(category)
        else:
            add_failure(
                failures,
                check_status,
                check_name,
                f"coverage item {index} category is not a string",
            )

        if item.get("status") not in COVERAGE_STATUSES:
            add_failure(
                failures,
                check_status,
                check_name,
                f"coverage item {index} status is not recognized",
            )
        source_path = item.get("source_path")
        if source_path is not None and not isinstance(source_path, str):
            add_failure(
                failures,
                check_status,
                check_name,
                f"coverage item {index} source_path is not a string or null",
            )
        if not isinstance(item.get("expected_package_outputs"), list):
            add_failure(
                failures,
                check_status,
                check_name,
                f"coverage item {index} expected_package_outputs is not a list",
            )
        if not isinstance(item.get("safety_notes"), list):
            add_failure(
                failures,
                check_status,
                check_name,
                f"coverage item {index} safety_notes is not a list",
            )

        if item.get("package_time_review_required") is True:
            package_time_review_present = True
        if category == "guide_source" and item.get("present") is True:
            present_guide_source = True
        if category == "notice_source" and item.get("present") is True:
            present_notice_source = True

    missing_categories = REQUIRED_COVERAGE_CATEGORIES - seen_categories
    if missing_categories:
        add_failure(
            failures,
            check_status,
            check_name,
            "missing coverage categories: "
            + ", ".join(sorted(missing_categories)),
        )
    if not package_time_review_present:
        add_failure(
            failures,
            check_status,
            check_name,
            "missing package_time_review_required coverage item",
        )
    if not present_guide_source:
        add_failure(
            failures,
            check_status,
            check_name,
            "missing present guide source coverage item",
        )
    if not present_notice_source:
        add_failure(
            failures,
            check_status,
            check_name,
            "missing present notice source coverage item",
        )


def check_json_generation_readiness(
    json_data: dict[str, object] | None,
    failures: list[str],
    check_status: dict[str, bool],
) -> None:
    check_name = "--format json generation readiness preview"
    if json_data is None:
        add_failure(
            failures,
            check_status,
            check_name,
            "JSON data unavailable for generation readiness checks",
        )
        return

    readiness = json_data.get("generation_readiness")
    if not isinstance(readiness, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "generation_readiness is not an object",
        )
        return

    if readiness.get("overall") != "blocked":
        add_failure(
            failures,
            check_status,
            check_name,
            "generation_readiness.overall is not blocked",
        )
    if readiness.get("actual_generation_approved") is not False:
        add_failure(
            failures,
            check_status,
            check_name,
            "generation_readiness.actual_generation_approved is not false",
        )
    if readiness.get("score_basis") != "advisory_only":
        add_failure(
            failures,
            check_status,
            check_name,
            "generation_readiness.score_basis is not advisory_only",
        )
    if not isinstance(readiness.get("next_required_action"), str):
        add_failure(
            failures,
            check_status,
            check_name,
            "generation_readiness.next_required_action is not a string",
        )

    items = readiness.get("checklist_items")
    if not isinstance(items, list) or not items:
        add_failure(
            failures,
            check_status,
            check_name,
            "generation_readiness.checklist_items is not a non-empty list",
        )
        return

    summary = readiness.get("summary")
    if not isinstance(summary, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "generation_readiness.summary is not an object",
        )
    else:
        for key in ("total", "ready", "blocked", "needs_human_review", "unresolved"):
            if not isinstance(summary.get(key), int):
                add_failure(
                    failures,
                    check_status,
                    check_name,
                    f"generation_readiness.summary.{key} is not an integer",
                )
        if summary.get("total") != len(items):
            add_failure(
                failures,
                check_status,
                check_name,
                "generation_readiness.summary total does not match items length",
            )
        if summary.get("blocked", 0) < 1:
            add_failure(
                failures,
                check_status,
                check_name,
                "generation_readiness.summary blocked count is less than 1",
            )

    advisory_score = readiness.get("advisory_score")
    if not isinstance(advisory_score, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "generation_readiness.advisory_score is not an object",
        )
    else:
        if advisory_score.get("value") != EXPECTED_ADVISORY_SCORE_VALUE:
            add_failure(
                failures,
                check_status,
                check_name,
                (
                    "generation_readiness.advisory_score.value is not "
                    f"{EXPECTED_ADVISORY_SCORE_VALUE}"
                ),
            )
        if advisory_score.get("max") != EXPECTED_ADVISORY_SCORE_MAX:
            add_failure(
                failures,
                check_status,
                check_name,
                (
                    "generation_readiness.advisory_score.max is not "
                    f"{EXPECTED_ADVISORY_SCORE_MAX}"
                ),
            )
        if advisory_score.get("basis") != "ready_items_divided_by_total_items":
            add_failure(
                failures,
                check_status,
                check_name,
                "generation_readiness.advisory_score.basis is unexpected",
            )
        if advisory_score.get("approval_meaning") != "none":
            add_failure(
                failures,
                check_status,
                check_name,
                "generation_readiness.advisory_score.approval_meaning is not none",
            )
        if advisory_score.get("blocked_override") is not True:
            add_failure(
                failures,
                check_status,
                check_name,
                "generation_readiness.advisory_score.blocked_override is not true",
            )
        if advisory_score.get("actual_generation_approved") is not False:
            add_failure(
                failures,
                check_status,
                check_name,
                (
                    "generation_readiness.advisory_score."
                    "actual_generation_approved is not false"
                ),
            )
        if (
            isinstance(summary, dict)
            and isinstance(summary.get("total"), int)
            and isinstance(summary.get("ready"), int)
        ):
            total = summary["total"]
            ready = summary["ready"]
            expected = (ready * 100 // total) if total else 0
            if advisory_score.get("value") != expected:
                add_failure(
                    failures,
                    check_status,
                    check_name,
                    "generation_readiness.advisory_score.value does not match summary",
                )

    actual_generation_blocked = False
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            add_failure(
                failures,
                check_status,
                check_name,
                f"readiness item {index} is not an object",
            )
            continue

        missing = REQUIRED_READINESS_ITEM_FIELDS - set(item)
        if missing:
            add_failure(
                failures,
                check_status,
                check_name,
                f"readiness item {index} missing fields: {', '.join(sorted(missing))}",
            )
        if item.get("status") not in READINESS_STATUSES:
            add_failure(
                failures,
                check_status,
                check_name,
                f"readiness item {index} status is not recognized",
            )
        if item.get("required_before_generation") is not True:
            add_failure(
                failures,
                check_status,
                check_name,
                f"readiness item {index} required_before_generation is not true",
            )
        if item.get("human_review_required") is not True:
            add_failure(
                failures,
                check_status,
                check_name,
                f"readiness item {index} human_review_required is not true",
            )
        if (
            item.get("id") == "actual_generation_approval"
            and item.get("status") == "blocked"
        ):
            actual_generation_blocked = True

    if not actual_generation_blocked:
        add_failure(
            failures,
            check_status,
            check_name,
            "actual_generation_approval readiness item is not blocked",
        )

    readiness_summary = readiness.get("readiness_summary")
    if not isinstance(readiness_summary, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "generation_readiness.readiness_summary is not an object",
        )
    else:
        if not isinstance(readiness_summary.get("headline"), str):
            add_failure(
                failures,
                check_status,
                check_name,
                "generation_readiness.readiness_summary.headline is not a string",
            )
        if readiness_summary.get("next_required_action") != readiness.get(
            "next_required_action"
        ):
            add_failure(
                failures,
                check_status,
                check_name,
                (
                    "generation_readiness.readiness_summary.next_required_action "
                    "does not match"
                ),
            )

        expected_by_status = {
            "ready_items": "ready",
            "blocked_items": "blocked",
            "needs_human_review_items": "needs_human_review",
            "unresolved_items": "unresolved",
        }
        for field, status in expected_by_status.items():
            values = readiness_summary.get(field)
            if not isinstance(values, list) or not all(
                isinstance(value, str) for value in values
            ):
                add_failure(
                    failures,
                    check_status,
                    check_name,
                    f"generation_readiness.readiness_summary.{field} is invalid",
                )
                continue
            expected_values = [
                str(item["id"])
                for item in items
                if isinstance(item, dict) and item.get("status") == status
            ]
            if values != expected_values:
                add_failure(
                    failures,
                    check_status,
                    check_name,
                    (
                        f"generation_readiness.readiness_summary.{field} "
                        "does not match checklist item statuses"
                    ),
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


def check_cross_format_readiness_consistency(
    results: dict[str, ModeResult],
    json_data: dict[str, object] | None,
    failures: list[str],
    check_status: dict[str, bool],
) -> None:
    check_name = "cross-format readiness consistency"
    default = results["default"].stdout
    text = results["text"].stdout
    markdown = results["markdown"].stdout

    if "overall: blocked" not in default:
        add_failure(
            failures,
            check_status,
            check_name,
            "default text readiness overall is not blocked",
        )
    if "overall: blocked" not in text:
        add_failure(
            failures,
            check_status,
            check_name,
            "--format text readiness overall is not blocked",
        )
    markdown_readiness = markdown_section(markdown, "## Generation Readiness Preview")
    if "- overall: `blocked`" not in markdown_readiness:
        add_failure(
            failures,
            check_status,
            check_name,
            "Markdown readiness overall is not blocked",
        )

    if json_data is None:
        add_failure(
            failures,
            check_status,
            check_name,
            "JSON data unavailable for readiness consistency checks",
        )
        return

    readiness = json_data.get("generation_readiness")
    if not isinstance(readiness, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "JSON generation_readiness is unavailable for consistency checks",
        )
        return

    if readiness.get("overall") != "blocked":
        add_failure(
            failures,
            check_status,
            check_name,
            "JSON readiness overall is not blocked",
        )
    if readiness.get("actual_generation_approved") is not False:
        add_failure(
            failures,
            check_status,
            check_name,
            "JSON readiness actual_generation_approved is not false",
        )


def check_cross_format_advisory_score_consistency(
    results: dict[str, ModeResult],
    json_data: dict[str, object] | None,
    failures: list[str],
    check_status: dict[str, bool],
) -> None:
    check_name = "cross-format advisory score consistency"
    default = results["default"].stdout
    text = results["text"].stdout
    markdown = results["markdown"].stdout

    expected_text = f"advisory_score: {EXPECTED_ADVISORY_SCORE_TEXT}"
    if expected_text not in default:
        add_failure(
            failures,
            check_status,
            check_name,
            "default text advisory score is missing or inconsistent",
        )
    if expected_text not in text:
        add_failure(
            failures,
            check_status,
            check_name,
            "--format text advisory score is missing or inconsistent",
        )

    markdown_readiness = markdown_section(markdown, "## Generation Readiness Preview")
    expected_markdown = f"- advisory_score: `{EXPECTED_ADVISORY_SCORE_TEXT}`"
    if expected_markdown not in markdown_readiness:
        add_failure(
            failures,
            check_status,
            check_name,
            "Markdown advisory score is missing or inconsistent",
        )

    if json_data is None:
        add_failure(
            failures,
            check_status,
            check_name,
            "JSON data unavailable for advisory score consistency checks",
        )
        return

    readiness = json_data.get("generation_readiness")
    if not isinstance(readiness, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "JSON generation_readiness is unavailable for advisory score checks",
        )
        return

    advisory_score = readiness.get("advisory_score")
    if not isinstance(advisory_score, dict):
        add_failure(
            failures,
            check_status,
            check_name,
            "JSON advisory_score is unavailable for consistency checks",
        )
        return

    json_score_text = f"{advisory_score.get('value')}/{advisory_score.get('max')}"
    if json_score_text != EXPECTED_ADVISORY_SCORE_TEXT:
        add_failure(
            failures,
            check_status,
            check_name,
            "JSON advisory score does not match text and Markdown",
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
    check_json_source_coverage(json_data, failures, check_status)
    check_json_generation_readiness(json_data, failures, check_status)
    check_cross_format_consistency(results, json_data, failures, check_status)
    check_cross_format_readiness_consistency(
        results,
        json_data,
        failures,
        check_status,
    )
    check_cross_format_advisory_score_consistency(
        results,
        json_data,
        failures,
        check_status,
    )
    check_generated_package_absent(root, failures, check_status)

    print_report(check_status, failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
