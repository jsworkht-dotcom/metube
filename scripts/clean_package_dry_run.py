#!/usr/bin/env python3
"""Report-only dry-run for the future beginner clean package.

This script intentionally does not create, copy, move, zip, or package files.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
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

MANIFEST_ENTRY_SPECS: list[dict[str, object]] = [
    {
        "package_relative_path": "00_最初に開いてください.html",
        "source_candidate": "docs/llmwiki/package-guides/00-first-open.html.source.md",
        "kind": "beginner_guide",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Primary first-open beginner guide candidate.",
        "license_notice_required": False,
        "safety_notes": ["Markdown source only; no package output generated."],
    },
    {
        "package_relative_path": "00_最初に開いてください.txt",
        "source_candidate": "docs/llmwiki/package-guides/00-first-open.txt.source.md",
        "kind": "beginner_guide",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Plain-text first-open fallback guide candidate.",
        "license_notice_required": False,
        "safety_notes": ["Markdown source only; no package output generated."],
    },
    {
        "package_relative_path": "03_使い方.html",
        "source_candidate": "docs/llmwiki/package-guides/03-how-to-use.html.source.md",
        "kind": "beginner_guide",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Everyday-use HTML guide candidate.",
        "license_notice_required": False,
        "safety_notes": ["Markdown source only; no package output generated."],
    },
    {
        "package_relative_path": "03_使い方.txt",
        "source_candidate": "docs/llmwiki/package-guides/03-how-to-use.txt.source.md",
        "kind": "beginner_guide",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Everyday-use text fallback guide candidate.",
        "license_notice_required": False,
        "safety_notes": ["Markdown source only; no package output generated."],
    },
    {
        "package_relative_path": "04_困ったとき.html",
        "source_candidate": "docs/llmwiki/package-guides/04-troubleshooting.html.source.md",
        "kind": "beginner_guide",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Troubleshooting HTML guide candidate.",
        "license_notice_required": False,
        "safety_notes": ["Markdown source only; no package output generated."],
    },
    {
        "package_relative_path": "04_困ったとき.txt",
        "source_candidate": "docs/llmwiki/package-guides/04-troubleshooting.txt.source.md",
        "kind": "beginner_guide",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Troubleshooting text fallback guide candidate.",
        "license_notice_required": False,
        "safety_notes": ["Markdown source only; no package output generated."],
    },
    {
        "package_relative_path": "05_安全な使い方.html",
        "source_candidate": "docs/llmwiki/package-guides/05-safe-use.html.source.md",
        "kind": "beginner_guide",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Safe-use guide candidate for local-only boundaries.",
        "license_notice_required": False,
        "safety_notes": ["Markdown source only; no package output generated."],
    },
    {
        "package_relative_path": "開発者向け/manifest/package-manifest.json",
        "source_candidate": "docs/llmwiki/desktop-package-manifest.md",
        "kind": "developer_manifest",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Future package manifest review output candidate.",
        "license_notice_required": True,
        "review_status": "package_time_review_required",
        "safety_notes": ["Manifest is preview-only; no JSON file generated."],
    },
    {
        "package_relative_path": "開発者向け/manifest/planned-output-manifest.json",
        "source_candidate": "docs/llmwiki/clean-package-dry-run-contract.md",
        "kind": "developer_manifest",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Future planned output manifest candidate.",
        "license_notice_required": True,
        "review_status": "package_time_review_required",
        "safety_notes": ["Manifest is preview-only; no JSON file generated."],
    },
    {
        "package_relative_path": "開発者向け/manifest/license-notice-manifest.json",
        "source_candidate": "docs/llmwiki/package-notices/notice-source-index.source.md",
        "kind": "developer_manifest",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Future license and notice manifest candidate.",
        "license_notice_required": True,
        "review_status": "legal_not_final",
        "safety_notes": ["Legal review is not final; no manifest file generated."],
    },
    {
        "package_relative_path": "開発者向け/manifest/checksums.json",
        "source_candidate": None,
        "kind": "developer_manifest",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Future checksum manifest candidate.",
        "license_notice_required": False,
        "source_status": "candidate_only",
        "review_status": "package_time_review_required",
        "safety_notes": ["Checksum inputs are not selected in this phase."],
    },
    {
        "package_relative_path": "開発者向け/notices/NOTICE.txt",
        "source_candidate": "docs/llmwiki/package-notices/notice-source-index.source.md",
        "kind": "notice",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Aggregate notice output candidate.",
        "license_notice_required": True,
        "review_status": "legal_not_final",
        "safety_notes": ["Notice text is not generated; legal review remains open."],
    },
    {
        "package_relative_path": "開発者向け/notices/third-party-notices.txt",
        "source_candidate": "docs/llmwiki/package-notices/notice-source-index.source.md",
        "kind": "notice",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Third-party notice output candidate.",
        "license_notice_required": True,
        "review_status": "legal_not_final",
        "safety_notes": ["Notice text is not generated; legal review remains open."],
    },
    {
        "package_relative_path": "開発者向け/licenses/",
        "source_candidate": "docs/llmwiki/package-notices/notice-source-index.source.md",
        "kind": "license",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Future license bundle directory candidate.",
        "license_notice_required": True,
        "review_status": "legal_not_final",
        "safety_notes": ["License files are not copied in this phase."],
    },
    {
        "package_relative_path": "開発者向け/licenses/third-party/",
        "source_candidate": "docs/llmwiki/package-notices/notice-source-index.source.md",
        "kind": "license",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Future third-party license directory candidate.",
        "license_notice_required": True,
        "review_status": "legal_not_final",
        "safety_notes": ["License files are not copied in this phase."],
    },
    {
        "package_relative_path": "開発者向け/inventory/bundled-python-dependency-inventory.json",
        "source_candidate": (
            "docs/llmwiki/package-notices/"
            "bundled-python-dependency-inventory.source.md"
        ),
        "kind": "inventory",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Future bundled Python dependency inventory candidate.",
        "license_notice_required": True,
        "review_status": "legal_not_final",
        "safety_notes": ["Inventory is not generated; exact package versions need review."],
    },
    {
        "package_relative_path": "Windows用/notices/runtime-notices.txt",
        "source_candidate": "docs/llmwiki/package-notices/notice-source-index.source.md",
        "kind": "runtime_placeholder",
        "target_os": "windows",
        "target_arch": "all",
        "required": True,
        "include_reason": "Windows runtime notice placeholder candidate.",
        "license_notice_required": True,
        "review_status": "legal_not_final",
        "safety_notes": ["Windows runtime artifacts are not selected in this phase."],
    },
    {
        "package_relative_path": "Mac用/notices/runtime-notices.txt",
        "source_candidate": "docs/llmwiki/package-notices/notice-source-index.source.md",
        "kind": "runtime_placeholder",
        "target_os": "macos",
        "target_arch": "all",
        "required": True,
        "include_reason": "macOS runtime notice placeholder candidate.",
        "license_notice_required": True,
        "review_status": "legal_not_final",
        "safety_notes": ["macOS runtime artifacts are not selected in this phase."],
    },
    {
        "package_relative_path": "Windows用/",
        "source_candidate": None,
        "kind": "directory",
        "target_os": "windows",
        "target_arch": "all",
        "required": True,
        "include_reason": "Future Windows package directory candidate.",
        "license_notice_required": False,
        "source_status": "not_applicable_this_phase",
        "review_status": "package_time_review_required",
        "safety_notes": ["Directory is not created in dry-run mode."],
    },
    {
        "package_relative_path": "Mac用/",
        "source_candidate": None,
        "kind": "directory",
        "target_os": "macos",
        "target_arch": "all",
        "required": True,
        "include_reason": "Future macOS package directory candidate.",
        "license_notice_required": False,
        "source_status": "not_applicable_this_phase",
        "review_status": "package_time_review_required",
        "safety_notes": ["Directory is not created in dry-run mode."],
    },
    {
        "package_relative_path": "保存先/",
        "source_candidate": None,
        "kind": "directory",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Future save-folder placeholder candidate.",
        "license_notice_required": False,
        "source_status": "not_applicable_this_phase",
        "review_status": "package_time_review_required",
        "safety_notes": ["Directory is not created in dry-run mode."],
    },
    {
        "package_relative_path": "困ったとき/",
        "source_candidate": None,
        "kind": "directory",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Future troubleshooting directory candidate.",
        "license_notice_required": False,
        "source_status": "not_applicable_this_phase",
        "review_status": "package_time_review_required",
        "safety_notes": ["Directory is not created in dry-run mode."],
    },
    {
        "package_relative_path": "開発者向け/",
        "source_candidate": None,
        "kind": "directory",
        "target_os": "all",
        "target_arch": "all",
        "required": True,
        "include_reason": "Future developer review directory candidate.",
        "license_notice_required": True,
        "source_status": "not_applicable_this_phase",
        "review_status": "package_time_review_required",
        "safety_notes": ["Directory is not created in dry-run mode."],
    },
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

OUTPUT_GROUP_SPECS: list[dict[str, object]] = [
    {
        "group_key": "beginner_guides",
        "label": "Beginner guides",
        "description": "Beginner-facing HTML and text guide package candidates.",
        "package_relative_root": ".",
        "would_create_directories": [],
        "would_create_files": [
            "00_最初に開いてください.html",
            "00_最初に開いてください.txt",
            "03_使い方.html",
            "03_使い方.txt",
            "04_困ったとき.html",
            "04_困ったとき.txt",
            "05_安全な使い方.html",
        ],
        "would_generate_future_outputs": [],
        "would_copy_source_groups": ["docs/llmwiki/package-guides/"],
        "would_skip_or_exclude": [],
        "required": True,
        "review_status": "source_draft",
        "safety_notes": [
            "Guide outputs are preview candidates only; no HTML or TXT files generated."
        ],
    },
    {
        "group_key": "developer_docs",
        "label": "Developer docs",
        "description": "Developer-facing review materials copied into a future package.",
        "package_relative_root": "開発者向け/",
        "would_create_directories": [
            "開発者向け/",
            "開発者向け/docs/",
            "開発者向け/docs/llmwiki/",
        ],
        "would_create_files": ["開発者向け/README.md"],
        "would_generate_future_outputs": [],
        "would_copy_source_groups": ["docs/llmwiki/"],
        "would_skip_or_exclude": [],
        "required": True,
        "review_status": "package_time_review_required",
        "safety_notes": [
            "Developer docs need package-time review before any copy step."
        ],
    },
    {
        "group_key": "manifest_outputs",
        "label": "Manifest outputs",
        "description": "Future package manifest and checksum output candidates.",
        "package_relative_root": "開発者向け/manifest/",
        "would_create_directories": [],
        "would_create_files": [
            "開発者向け/manifest/package-manifest.json",
            "開発者向け/manifest/planned-output-manifest.json",
            "開発者向け/manifest/license-notice-manifest.json",
            "開発者向け/manifest/checksums.json",
        ],
        "would_generate_future_outputs": [
            "package manifest",
            "planned output manifest",
            "license notice manifest",
            "checksums manifest",
        ],
        "would_copy_source_groups": [],
        "would_skip_or_exclude": [],
        "required": True,
        "review_status": "package_time_review_required",
        "safety_notes": [
            "Manifest files are preview candidates only; no JSON files generated."
        ],
    },
    {
        "group_key": "notice_outputs",
        "label": "Notice outputs",
        "description": "Future NOTICE and runtime notice output candidates.",
        "package_relative_root": ".",
        "would_create_directories": [],
        "would_create_files": [
            "開発者向け/notices/NOTICE.txt",
            "開発者向け/notices/third-party-notices.txt",
            "Windows用/notices/runtime-notices.txt",
            "Mac用/notices/runtime-notices.txt",
        ],
        "would_generate_future_outputs": [
            "NOTICE.txt",
            "third-party notices",
            "runtime notices",
        ],
        "would_copy_source_groups": ["docs/llmwiki/package-notices/"],
        "would_skip_or_exclude": [],
        "required": True,
        "review_status": "legal_not_final",
        "safety_notes": [
            "Notice text requires legal review before any generated notice output."
        ],
    },
    {
        "group_key": "license_outputs",
        "label": "License outputs",
        "description": "Future license bundle output candidates.",
        "package_relative_root": "開発者向け/licenses/",
        "would_create_directories": [
            "開発者向け/licenses/",
            "開発者向け/licenses/third-party/",
            "開発者向け/licenses/third-party/python-dependencies/",
            "開発者向け/licenses/third-party/frontend/",
            "開発者向け/licenses/third-party/desktop-shell/",
        ],
        "would_create_files": [
            "開発者向け/licenses/MeTube-LICENSE.txt",
            "開発者向け/licenses/third-party/yt-dlp-LICENSE.txt",
            "開発者向け/licenses/third-party/ffmpeg-LICENSE.txt",
            "開発者向け/licenses/third-party/python-runtime-LICENSE.txt",
        ],
        "would_generate_future_outputs": [
            "license bundle",
            "third-party license references",
        ],
        "would_copy_source_groups": ["docs/llmwiki/package-notices/"],
        "would_skip_or_exclude": [],
        "required": True,
        "review_status": "legal_not_final",
        "safety_notes": [
            "License texts are not copied; exact license inputs need legal review."
        ],
    },
    {
        "group_key": "inventory_outputs",
        "label": "Inventory outputs",
        "description": "Future bundled dependency inventory output candidates.",
        "package_relative_root": "開発者向け/inventory/",
        "would_create_directories": [],
        "would_create_files": [
            "開発者向け/inventory/bundled-python-dependency-inventory.json",
            "開発者向け/inventory/bundled-python-dependency-inventory.md",
        ],
        "would_generate_future_outputs": [
            "bundled Python dependency inventory",
        ],
        "would_copy_source_groups": ["docs/llmwiki/package-notices/"],
        "would_skip_or_exclude": [],
        "required": True,
        "review_status": "legal_not_final",
        "safety_notes": [
            "Inventory output is not generated; exact bundled versions need review."
        ],
    },
    {
        "group_key": "windows_runtime_outputs",
        "label": "Windows runtime outputs",
        "description": "Future Windows runtime directory placeholders only.",
        "package_relative_root": "Windows用/",
        "would_create_directories": [
            "Windows用/",
            "Windows用/notices/",
        ],
        "would_create_files": [],
        "would_generate_future_outputs": [],
        "would_copy_source_groups": [],
        "would_skip_or_exclude": [],
        "required": True,
        "review_status": "package_time_review_required",
        "safety_notes": [
            "No .exe, runtime, or launcher artifact is selected in this phase."
        ],
    },
    {
        "group_key": "mac_runtime_outputs",
        "label": "macOS runtime outputs",
        "description": "Future macOS runtime directory placeholders only.",
        "package_relative_root": "Mac用/",
        "would_create_directories": [
            "Mac用/",
            "Mac用/notices/",
        ],
        "would_create_files": [],
        "would_generate_future_outputs": [],
        "would_copy_source_groups": [],
        "would_skip_or_exclude": [],
        "required": True,
        "review_status": "package_time_review_required",
        "safety_notes": [
            "No .app, runtime, or launcher artifact is selected in this phase."
        ],
    },
    {
        "group_key": "save_folder_placeholders",
        "label": "Save folder placeholders",
        "description": "Future user save-folder placeholder candidate.",
        "package_relative_root": "保存先/",
        "would_create_directories": ["保存先/"],
        "would_create_files": [],
        "would_generate_future_outputs": [],
        "would_copy_source_groups": [],
        "would_skip_or_exclude": [],
        "required": True,
        "review_status": "package_time_review_required",
        "safety_notes": ["Save folder placeholder is not created in dry-run mode."],
    },
    {
        "group_key": "troubleshooting_outputs",
        "label": "Troubleshooting outputs",
        "description": "Future troubleshooting directory placeholder candidate.",
        "package_relative_root": "困ったとき/",
        "would_create_directories": ["困ったとき/"],
        "would_create_files": [],
        "would_generate_future_outputs": [],
        "would_copy_source_groups": [],
        "would_skip_or_exclude": [],
        "required": True,
        "review_status": "package_time_review_required",
        "safety_notes": [
            "Troubleshooting directory is preview-only; page outputs are not selected."
        ],
    },
    {
        "group_key": "excluded_outputs",
        "label": "Excluded outputs",
        "description": "Repository paths that future package generation must skip.",
        "package_relative_root": ".",
        "would_create_directories": [],
        "would_create_files": [],
        "would_generate_future_outputs": [],
        "would_copy_source_groups": [],
        "would_skip_or_exclude": [
            ".git/",
            ".github/",
            ".pytest_cache/",
            "node_modules/",
            "ui/node_modules/",
            "downloads/",
            "state/",
            "logs/",
            ".env",
            "cookies.txt",
            "docker-compose.local.yml",
            "docs/local-only.md",
            "動画保存ツール_ローカル専用/",
        ],
        "required": True,
        "review_status": "not_applicable_this_phase",
        "safety_notes": [
            "Exclusions are report-only guardrails; no paths are removed or created."
        ],
    },
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

COVERAGE_ITEM_SPECS: list[dict[str, object]] = [
    {
        "coverage_key": "first_open_html",
        "category": "guide_source",
        "label": "First-open HTML guide source",
        "source_path": "docs/llmwiki/package-guides/00-first-open.html.source.md",
        "expected_package_outputs": ["00_最初に開いてください.html"],
        "status": "source_draft",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Markdown source only; no package guide generated."],
    },
    {
        "coverage_key": "first_open_txt",
        "category": "guide_source",
        "label": "First-open text guide source",
        "source_path": "docs/llmwiki/package-guides/00-first-open.txt.source.md",
        "expected_package_outputs": ["00_最初に開いてください.txt"],
        "status": "source_draft",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Markdown source only; no package guide generated."],
    },
    {
        "coverage_key": "how_to_use_html",
        "category": "guide_source",
        "label": "How-to-use HTML guide source",
        "source_path": "docs/llmwiki/package-guides/03-how-to-use.html.source.md",
        "expected_package_outputs": ["03_使い方.html"],
        "status": "source_draft",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Markdown source only; no package guide generated."],
    },
    {
        "coverage_key": "how_to_use_txt",
        "category": "guide_source",
        "label": "How-to-use text guide source",
        "source_path": "docs/llmwiki/package-guides/03-how-to-use.txt.source.md",
        "expected_package_outputs": ["03_使い方.txt"],
        "status": "source_draft",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Markdown source only; no package guide generated."],
    },
    {
        "coverage_key": "troubleshooting_html",
        "category": "guide_source",
        "label": "Troubleshooting HTML guide source",
        "source_path": (
            "docs/llmwiki/package-guides/04-troubleshooting.html.source.md"
        ),
        "expected_package_outputs": ["04_困ったとき.html"],
        "status": "source_draft",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Markdown source only; no package guide generated."],
    },
    {
        "coverage_key": "troubleshooting_txt",
        "category": "guide_source",
        "label": "Troubleshooting text guide source",
        "source_path": (
            "docs/llmwiki/package-guides/04-troubleshooting.txt.source.md"
        ),
        "expected_package_outputs": ["04_困ったとき.txt"],
        "status": "source_draft",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Markdown source only; no package guide generated."],
    },
    {
        "coverage_key": "safe_use_html",
        "category": "guide_source",
        "label": "Safe-use HTML guide source",
        "source_path": "docs/llmwiki/package-guides/05-safe-use.html.source.md",
        "expected_package_outputs": ["05_安全な使い方.html"],
        "status": "source_draft",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Markdown source only; no package guide generated."],
    },
    {
        "coverage_key": "metube_notice",
        "category": "notice_source",
        "label": "MeTube notice source",
        "source_path": "docs/llmwiki/package-notices/metube-notice.source.md",
        "expected_package_outputs": [
            "開発者向け/notices/NOTICE.txt",
            "開発者向け/notices/third-party-notices.txt",
        ],
        "status": "legal_not_final",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Notice source exists for preview; legal review is not final."],
    },
    {
        "coverage_key": "yt_dlp_notice",
        "category": "notice_source",
        "label": "yt-dlp notice source",
        "source_path": "docs/llmwiki/package-notices/yt-dlp-notice.source.md",
        "expected_package_outputs": [
            "開発者向け/notices/third-party-notices.txt",
        ],
        "status": "legal_not_final",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Notice source exists for preview; legal review is not final."],
    },
    {
        "coverage_key": "ffmpeg_notice",
        "category": "notice_source",
        "label": "FFmpeg notice source",
        "source_path": "docs/llmwiki/package-notices/ffmpeg-notice.source.md",
        "expected_package_outputs": [
            "開発者向け/notices/third-party-notices.txt",
            "Windows用/notices/runtime-notices.txt",
            "Mac用/notices/runtime-notices.txt",
        ],
        "status": "legal_not_final",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Notice source exists for preview; legal review is not final."],
    },
    {
        "coverage_key": "python_runtime_notice",
        "category": "notice_source",
        "label": "Python runtime notice source",
        "source_path": (
            "docs/llmwiki/package-notices/python-runtime-notice.source.md"
        ),
        "expected_package_outputs": [
            "開発者向け/notices/third-party-notices.txt",
            "Windows用/notices/runtime-notices.txt",
            "Mac用/notices/runtime-notices.txt",
        ],
        "status": "legal_not_final",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Notice source exists for preview; legal review is not final."],
    },
    {
        "coverage_key": "frontend_deps_notice",
        "category": "notice_source",
        "label": "Frontend dependency notice source",
        "source_path": "docs/llmwiki/package-notices/frontend-deps-notice.source.md",
        "expected_package_outputs": [
            "開発者向け/notices/third-party-notices.txt",
        ],
        "status": "legal_not_final",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Notice source exists for preview; legal review is not final."],
    },
    {
        "coverage_key": "desktop_shell_notice",
        "category": "notice_source",
        "label": "Desktop shell notice source",
        "source_path": "docs/llmwiki/package-notices/desktop-shell-notice.source.md",
        "expected_package_outputs": [
            "開発者向け/notices/third-party-notices.txt",
            "Windows用/notices/runtime-notices.txt",
            "Mac用/notices/runtime-notices.txt",
        ],
        "status": "legal_not_final",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Notice source exists for preview; legal review is not final."],
    },
    {
        "coverage_key": "bundled_python_dependency_inventory_source",
        "category": "notice_source",
        "label": "Bundled Python dependency inventory source",
        "source_path": (
            "docs/llmwiki/package-notices/"
            "bundled-python-dependency-inventory.source.md"
        ),
        "expected_package_outputs": [
            "開発者向け/inventory/bundled-python-dependency-inventory.json",
            "開発者向け/inventory/bundled-python-dependency-inventory.md",
        ],
        "status": "legal_not_final",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Inventory source exists for preview; legal review is not final."],
    },
    {
        "coverage_key": "notice_source_index",
        "category": "notice_source",
        "label": "Notice source index",
        "source_path": "docs/llmwiki/package-notices/notice-source-index.source.md",
        "expected_package_outputs": [
            "開発者向け/notices/NOTICE.txt",
            "開発者向け/notices/third-party-notices.txt",
            "開発者向け/manifest/license-notice-manifest.json",
        ],
        "status": "package_time_review_required",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Source index is a preview map, not legal approval."],
    },
    {
        "coverage_key": "metube_license",
        "category": "license_source",
        "label": "MeTube license source selection",
        "source_path": None,
        "expected_package_outputs": [
            "開発者向け/licenses/",
            "開発者向け/licenses/MeTube-LICENSE.txt",
        ],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Exact license source is not selected in this phase."],
    },
    {
        "coverage_key": "yt_dlp_license",
        "category": "license_source",
        "label": "yt-dlp license source selection",
        "source_path": None,
        "expected_package_outputs": [
            "開発者向け/licenses/third-party/",
            "開発者向け/licenses/third-party/yt-dlp-LICENSE.txt",
        ],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Exact license source is not selected in this phase."],
    },
    {
        "coverage_key": "ffmpeg_license",
        "category": "license_source",
        "label": "FFmpeg license source selection",
        "source_path": None,
        "expected_package_outputs": [
            "開発者向け/licenses/third-party/ffmpeg-LICENSE.txt",
        ],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Exact license source is not selected in this phase."],
    },
    {
        "coverage_key": "python_runtime_license",
        "category": "license_source",
        "label": "Python runtime license source selection",
        "source_path": None,
        "expected_package_outputs": [
            "開発者向け/licenses/third-party/python-runtime-LICENSE.txt",
        ],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Exact license source is not selected in this phase."],
    },
    {
        "coverage_key": "frontend_dependency_licenses",
        "category": "license_source",
        "label": "Frontend dependency license source selection",
        "source_path": None,
        "expected_package_outputs": [
            "開発者向け/licenses/third-party/frontend/",
        ],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Exact dependency license sources are not selected."],
    },
    {
        "coverage_key": "desktop_shell_licenses",
        "category": "license_source",
        "label": "Desktop shell license source selection",
        "source_path": None,
        "expected_package_outputs": [
            "開発者向け/licenses/third-party/desktop-shell/",
        ],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Desktop shell has no selected artifact in this phase."],
    },
    {
        "coverage_key": "bundled_python_dependency_inventory",
        "category": "inventory_source",
        "label": "Bundled Python dependency inventory",
        "source_path": (
            "docs/llmwiki/package-notices/"
            "bundled-python-dependency-inventory.source.md"
        ),
        "expected_package_outputs": [
            "開発者向け/inventory/bundled-python-dependency-inventory.json",
            "開発者向け/inventory/bundled-python-dependency-inventory.md",
        ],
        "status": "legal_not_final",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Inventory source exists for preview; versions need review."],
    },
    {
        "coverage_key": "frontend_dependency_inventory",
        "category": "inventory_source",
        "label": "Frontend dependency inventory",
        "source_path": None,
        "expected_package_outputs": [
            "開発者向け/licenses/third-party/frontend/",
        ],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Frontend dependency inventory is not selected yet."],
    },
    {
        "coverage_key": "license_notice_manifest",
        "category": "inventory_source",
        "label": "License notice manifest source",
        "source_path": "docs/llmwiki/package-notices/notice-source-index.source.md",
        "expected_package_outputs": [
            "開発者向け/manifest/license-notice-manifest.json",
        ],
        "status": "package_time_review_required",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Manifest source map is preview-only and not legal final."],
    },
    {
        "coverage_key": "windows_runtime_selection",
        "category": "runtime_selection",
        "label": "Windows runtime selection",
        "source_path": None,
        "expected_package_outputs": ["Windows用/"],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["No .exe or Windows runtime artifact is selected."],
    },
    {
        "coverage_key": "mac_runtime_selection",
        "category": "runtime_selection",
        "label": "macOS runtime selection",
        "source_path": None,
        "expected_package_outputs": ["Mac用/"],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["No .app or macOS runtime artifact is selected."],
    },
    {
        "coverage_key": "ffmpeg_runtime_selection",
        "category": "runtime_selection",
        "label": "FFmpeg runtime selection",
        "source_path": None,
        "expected_package_outputs": [
            "Windows用/notices/runtime-notices.txt",
            "Mac用/notices/runtime-notices.txt",
        ],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["No FFmpeg binary artifact is selected in this phase."],
    },
    {
        "coverage_key": "python_runtime_selection",
        "category": "runtime_selection",
        "label": "Python runtime selection",
        "source_path": None,
        "expected_package_outputs": [
            "Windows用/notices/runtime-notices.txt",
            "Mac用/notices/runtime-notices.txt",
        ],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["No Python runtime artifact is selected in this phase."],
    },
    {
        "coverage_key": "desktop_shell_selection",
        "category": "desktop_shell",
        "label": "Desktop shell selection",
        "source_path": None,
        "expected_package_outputs": [
            "Windows用/",
            "Mac用/",
        ],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["No Tauri, Electron, or WebView2 artifact is selected."],
    },
    {
        "coverage_key": "package_manifest_preview",
        "category": "manifest_source",
        "label": "Package manifest preview source",
        "source_path": "docs/llmwiki/desktop-package-manifest.md",
        "expected_package_outputs": [
            "開発者向け/manifest/package-manifest.json",
        ],
        "status": "package_time_review_required",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Manifest source is preview-only; no JSON generated."],
    },
    {
        "coverage_key": "planned_output_manifest",
        "category": "manifest_source",
        "label": "Planned output manifest source",
        "source_path": "docs/llmwiki/clean-package-dry-run-contract.md",
        "expected_package_outputs": [
            "開発者向け/manifest/planned-output-manifest.json",
        ],
        "status": "package_time_review_required",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Manifest source is preview-only; no JSON generated."],
    },
    {
        "coverage_key": "checksums_manifest",
        "category": "manifest_source",
        "label": "Checksums manifest source selection",
        "source_path": None,
        "expected_package_outputs": [
            "開発者向け/manifest/checksums.json",
        ],
        "status": "candidate_only",
        "required_for_generation": True,
        "legal_final": False,
        "package_time_review_required": True,
        "safety_notes": ["Checksum inputs are not selected in this phase."],
    },
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
        choices=["text", "markdown", "json"],
        default="text",
        help=(
            "Report format. Text is the default; markdown and json write "
            "report-only stdout summaries."
        ),
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


def candidate_source_items(
    root: Path,
    candidates: Iterable[tuple[str, str]],
) -> tuple[int, int, list[dict[str, object]], list[dict[str, str]]]:
    items: list[dict[str, object]] = []
    missing: list[dict[str, str]] = []
    values = list(candidates)
    present = 0
    for label, rel in values:
        exists = (root / rel).is_file()
        if exists:
            present += 1
        item = {
            "label": label,
            "path": rel,
            "present": exists,
        }
        items.append(item)
        if not exists:
            missing.append({"label": label, "path": rel})
    return present, len(values), items, missing


def source_status_for_manifest_entry(root: Path, spec: dict[str, object]) -> str:
    explicit = spec.get("source_status")
    if isinstance(explicit, str):
        return explicit

    source_candidate = spec.get("source_candidate")
    if isinstance(source_candidate, str):
        return "source_draft" if (root / source_candidate).is_file() else "missing"
    return "candidate_only"


def build_manifest_entries(root: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for spec in MANIFEST_ENTRY_SPECS:
        source_status = source_status_for_manifest_entry(root, spec)
        review_status = spec.get("review_status")
        if not isinstance(review_status, str):
            review_status = source_status
        output_status = spec.get("output_status")
        if not isinstance(output_status, str):
            output_status = "package_time_review_required"

        safety_notes = spec.get("safety_notes")
        if not isinstance(safety_notes, list):
            safety_notes = ["Report-only candidate; no package output generated."]

        entries.append(
            {
                "package_relative_path": spec["package_relative_path"],
                "source_candidate": spec["source_candidate"],
                "kind": spec["kind"],
                "target_os": spec["target_os"],
                "target_arch": spec["target_arch"],
                "generated": False,
                "required": spec["required"],
                "include_reason": spec["include_reason"],
                "license_notice_required": spec["license_notice_required"],
                "review_status": review_status,
                "safety_notes": safety_notes,
                "source_status": source_status,
                "output_status": output_status,
                "human_review_required": True,
            }
        )
    return entries


def summarize_manifest_entries(
    entries: list[dict[str, object]],
) -> dict[str, object]:
    by_kind: dict[str, int] = {}
    for entry in entries:
        kind = str(entry["kind"])
        by_kind[kind] = by_kind.get(kind, 0) + 1
    return {
        "total": len(entries),
        "by_kind": by_kind,
        "human_review_required": any(
            bool(entry["human_review_required"]) for entry in entries
        ),
        "generated_now": any(bool(entry["generated"]) for entry in entries),
    }


def build_output_groups() -> list[dict[str, object]]:
    groups: list[dict[str, object]] = []
    for spec in OUTPUT_GROUP_SPECS:
        groups.append(
            {
                "group_key": spec["group_key"],
                "label": spec["label"],
                "description": spec["description"],
                "package_relative_root": spec["package_relative_root"],
                "would_create_directories": spec["would_create_directories"],
                "would_create_files": spec["would_create_files"],
                "would_generate_future_outputs": spec[
                    "would_generate_future_outputs"
                ],
                "would_copy_source_groups": spec["would_copy_source_groups"],
                "would_skip_or_exclude": spec["would_skip_or_exclude"],
                "required": spec["required"],
                "generated_now": False,
                "human_review_required": True,
                "safety_notes": spec["safety_notes"],
                "review_status": spec["review_status"],
            }
        )
    return groups


def count_group_items(group: dict[str, object], key: str) -> int:
    value = group.get(key)
    return len(value) if isinstance(value, list) else 0


def summarize_output_groups(
    groups: list[dict[str, object]],
) -> dict[str, object]:
    by_group: dict[str, dict[str, object]] = {}
    for group in groups:
        group_key = str(group["group_key"])
        by_group[group_key] = {
            "files": count_group_items(group, "would_create_files"),
            "directories": count_group_items(group, "would_create_directories"),
            "future_outputs": count_group_items(
                group,
                "would_generate_future_outputs",
            ),
            "copy_source_groups": count_group_items(
                group,
                "would_copy_source_groups",
            ),
            "excluded_paths": count_group_items(group, "would_skip_or_exclude"),
            "review_status": group["review_status"],
        }
    return {
        "total": len(groups),
        "by_group": by_group,
        "human_review_required": any(
            bool(group["human_review_required"]) for group in groups
        ),
        "generated_now": any(bool(group["generated_now"]) for group in groups),
    }


def build_coverage_items(root: Path) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    for spec in COVERAGE_ITEM_SPECS:
        source_path = spec["source_path"]
        present = isinstance(source_path, str) and (root / source_path).is_file()
        status = str(spec["status"])
        if isinstance(source_path, str) and not present:
            status = "missing"

        items.append(
            {
                "coverage_key": spec["coverage_key"],
                "category": spec["category"],
                "label": spec["label"],
                "source_path": source_path,
                "expected_package_outputs": spec["expected_package_outputs"],
                "status": status,
                "present": present,
                "required_for_generation": spec["required_for_generation"],
                "legal_final": spec["legal_final"],
                "package_time_review_required": spec[
                    "package_time_review_required"
                ],
                "human_review_required": True,
                "safety_notes": spec["safety_notes"],
            }
        )
    return items


def summarize_coverage_items(
    items: list[dict[str, object]],
) -> dict[str, object]:
    by_category: dict[str, int] = {}
    by_status: dict[str, int] = {}
    package_time_review_required = 0
    for item in items:
        category = str(item["category"])
        status = str(item["status"])
        by_category[category] = by_category.get(category, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1
        if bool(item["package_time_review_required"]):
            package_time_review_required += 1

    return {
        "total": len(items),
        "by_category": by_category,
        "by_status": by_status,
        "package_time_review_required": package_time_review_required,
        "human_review_required": any(
            bool(item["human_review_required"]) for item in items
        ),
        "generated_now": False,
    }


def print_package_manifest_preview(root: Path, excluded_found: list[str]) -> None:
    notice_present, notice_lines = present_candidate_lines(
        root, MANIFEST_PREVIEW_NOTICE_SOURCES
    )
    guide_present, guide_lines = present_candidate_lines(root, GUIDE_SOURCE_CANDIDATES)
    manifest_entries = build_manifest_entries(root)
    manifest_entry_summary = summarize_manifest_entries(manifest_entries)

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
    print("  manifest_entries:")
    print(f"    total: {manifest_entry_summary['total']}")
    print("    by_kind:")
    for kind, count in manifest_entry_summary["by_kind"].items():
        print(f"      {kind}: {count}")
    print("    entries:")
    for entry in manifest_entries:
        print(f"      - path: {entry['package_relative_path']}")
        print(f"        kind: {entry['kind']}")
        print(f"        source_status: {entry['source_status']}")
        print(f"        output_status: {entry['output_status']}")
        print(f"        generated: {str(entry['generated']).lower()}")
        print(
            "        human_review_required: "
            f"{str(entry['human_review_required']).lower()}"
        )
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
    output_groups = build_output_groups()
    output_group_summary = summarize_output_groups(output_groups)

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
    print("  output_groups:")
    print(f"    total: {output_group_summary['total']}")
    print(f"    generated_now: {str(output_group_summary['generated_now']).lower()}")
    print(
        "    human_review_required_before_generation: "
        f"{str(output_group_summary['human_review_required']).lower()}"
    )
    print("    groups:")
    for group in output_groups:
        print(f"      - group: {group['group_key']}")
        print(f"        files: {count_group_items(group, 'would_create_files')}")
        print(
            "        directories: "
            f"{count_group_items(group, 'would_create_directories')}"
        )
        print(
            "        future_outputs: "
            f"{count_group_items(group, 'would_generate_future_outputs')}"
        )
        print(f"        generated_now: {str(group['generated_now']).lower()}")
        print(
            "        human_review_required: "
            f"{str(group['human_review_required']).lower()}"
        )
        print(f"        review_status: {group['review_status']}")
    print("  would_exclude_paths summary:")
    print(f"    rules: {len(EXCLUDED_PATHS)}")
    print(f"    currently_present: {len(excluded_found)}")
    print("  no_files_generated: true")
    print("  human_review_required_before_generation: true")
    print(
        "  cleanup_rollback_candidate: future package root only; "
        "human review required before any action."
    )


def print_source_coverage_status(root: Path) -> None:
    coverage_items = build_coverage_items(root)
    coverage_summary = summarize_coverage_items(coverage_items)

    print("Source coverage status:")
    print(f"  total: {coverage_summary['total']}")
    print("  by_category:")
    for category, count in coverage_summary["by_category"].items():
        print(f"    {category}: {count}")
    print("  by_status:")
    for status, count in coverage_summary["by_status"].items():
        print(f"    {status}: {count}")
    print(
        "  package_time_review_required: "
        f"{coverage_summary['package_time_review_required']}"
    )
    print(
        "  human_review_required: "
        f"{str(coverage_summary['human_review_required']).lower()}"
    )
    print("  generated_now: false")
    print("  coverage_items:")
    for item in coverage_items:
        print(f"    - key: {item['coverage_key']}")
        print(f"      category: {item['category']}")
        print(f"      status: {item['status']}")
        print(f"      present: {str(item['present']).lower()}")
        print(
            "      package_time_review_required: "
            f"{str(item['package_time_review_required']).lower()}"
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
    manifest_entries = build_manifest_entries(root)
    manifest_entry_summary = summarize_manifest_entries(manifest_entries)
    output_groups = build_output_groups()
    output_group_summary = summarize_output_groups(output_groups)
    coverage_items = build_coverage_items(root)
    coverage_summary = summarize_coverage_items(coverage_items)

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
    print("### Manifest Entry Candidates")
    print()
    print(f"- Total entries: `{manifest_entry_summary['total']}`")
    print(
        "- Generated now: "
        f"`{str(manifest_entry_summary['generated_now']).lower()}`"
    )
    print(
        "- Human review required before generation: "
        f"`{str(manifest_entry_summary['human_review_required']).lower()}`"
    )
    print()
    print("#### Entries")
    print()
    for entry in manifest_entries:
        source_candidate = entry["source_candidate"]
        source_display = (
            f"`{source_candidate}`"
            if isinstance(source_candidate, str)
            else "`not selected yet`"
        )
        print(f"- `{entry['package_relative_path']}`")
        print(f"  - kind: {entry['kind']}")
        print(f"  - source: {source_display}")
        print(f"  - source_status: {entry['source_status']}")
        print(f"  - output_status: {entry['output_status']}")
        print(f"  - human_review_required: {str(entry['human_review_required']).lower()}")
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
    print("### Output Groups")
    print()
    print(f"- Total groups: `{output_group_summary['total']}`")
    print(
        "- Generated now: "
        f"`{str(output_group_summary['generated_now']).lower()}`"
    )
    print(
        "- Human review required before generation: "
        f"`{str(output_group_summary['human_review_required']).lower()}`"
    )
    print()
    print("#### Groups")
    print()
    for group in output_groups:
        print(f"- `{group['group_key']}`")
        print(f"  - label: {group['label']}")
        print(f"  - files: `{count_group_items(group, 'would_create_files')}`")
        print(
            "  - directories: "
            f"`{count_group_items(group, 'would_create_directories')}`"
        )
        print(
            "  - future_outputs: "
            f"`{count_group_items(group, 'would_generate_future_outputs')}`"
        )
        print(
            "  - excluded_paths: "
            f"`{count_group_items(group, 'would_skip_or_exclude')}`"
        )
        print(f"  - review_status: {group['review_status']}")
        print(f"  - generated_now: {str(group['generated_now']).lower()}")
        print(
            "  - human_review_required: "
            f"{str(group['human_review_required']).lower()}"
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
    print("### Source Coverage Status")
    print()
    print(f"- Total items: `{coverage_summary['total']}`")
    print(
        "- Package-time review required: "
        f"`{coverage_summary['package_time_review_required']}`"
    )
    print(
        "- Human review required: "
        f"`{str(coverage_summary['human_review_required']).lower()}`"
    )
    print("- Generated now: `false`")
    print()
    print("#### By Category")
    print()
    for category, count in coverage_summary["by_category"].items():
        print(f"- {category}: `{count}`")
    print()
    print("#### By Status")
    print()
    for coverage_status, count in coverage_summary["by_status"].items():
        print(f"- {coverage_status}: `{count}`")
    print()
    print("#### Coverage Items")
    print()
    for item in coverage_items:
        print(f"- `{item['coverage_key']}`")
        print(f"  - category: {item['category']}")
        print(f"  - status: {item['status']}")
        print(f"  - present: {str(item['present']).lower()}")
        print(
            "  - package_time_review_required: "
            f"{str(item['package_time_review_required']).lower()}"
        )
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


def finding_to_dict(finding: Finding) -> dict[str, object]:
    return {
        "kind": finding.kind,
        "path": finding.path,
        "line": finding.line,
        "pattern_family": finding.pattern_family,
        "message": finding.message,
    }


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def build_json_report(
    root: Path,
    blocked: list[Finding],
    warnings: list[Finding],
    excluded_found: list[str],
) -> dict[str, object]:
    status = "blocked" if blocked else "ok"
    exit_code = 1 if blocked else 0
    branch = git_value(root, "branch", "--show-current")
    commit = git_value(root, "rev-parse", "--short", "HEAD")

    manifest_notice_present, manifest_notice_total, manifest_notice_items, _ = (
        candidate_source_items(root, MANIFEST_PREVIEW_NOTICE_SOURCES)
    )
    guide_present, guide_total, guide_items, missing_guides = candidate_source_items(
        root, GUIDE_SOURCE_CANDIDATES
    )
    notice_present, notice_total, notice_items, missing_notices = candidate_source_items(
        root, NOTICE_SOURCE_CANDIDATES
    )
    safety_present, safety_total, safety_items, missing_safety = (
        candidate_source_items(root, SAFETY_NOTICE_SOURCE_CANDIDATES)
    )
    platform_present, platform_total, platform_items, missing_platform = (
        candidate_source_items(root, PLATFORM_SECTION_SOURCE_CANDIDATES)
    )
    manifest_entries = build_manifest_entries(root)
    manifest_entry_summary = summarize_manifest_entries(manifest_entries)
    output_groups = build_output_groups()
    output_group_summary = summarize_output_groups(output_groups)
    coverage_items = build_coverage_items(root)
    coverage_summary = summarize_coverage_items(coverage_items)

    generated_package_root_present = any(
        b.kind == "generated_package_folder_present" for b in blocked
    )
    pr_1001_files_present = any(b.kind == "upstream_pr_1001_leakage" for b in blocked)
    invalid_planned_paths = any(b.kind == "invalid_planned_path" for b in blocked)
    forbidden_filenames = any(b.kind == "forbidden_filename" for b in blocked)
    secret_like_content = any(b.kind == "forbidden_content_pattern" for b in blocked)

    return {
        "schema_version": "0.1",
        "report_type": "clean_package_dry_run",
        "report_format": "json",
        "mode": "dry_run",
        "status": status,
        "exit_code": exit_code,
        "generated_artifacts": False,
        "checked_at": utc_timestamp(),
        "repository": {
            "branch": branch,
            "commit": commit,
            "root": ".",
        },
        "package": {
            "package_root": PACKAGE_ROOT,
            "package_name_candidate": "動画保存ツール_ローカル専用",
            "package_type_candidate": "local-only beginner package",
            "local_only": True,
        },
        "package_manifest_preview": {
            "package_name_candidate": "動画保存ツール_ローカル専用",
            "package_type_candidate": "local-only beginner package",
            "local_only": True,
            "generated_artifacts": False,
            "notice_sources": {
                "present": manifest_notice_present,
                "total": manifest_notice_total,
                "items": manifest_notice_items,
            },
            "guide_sources": {
                "present": guide_present,
                "total": guide_total,
                "items": guide_items,
            },
            "future_outputs": MANIFEST_PREVIEW_FUTURE_OUTPUTS,
            "manifest_entries": manifest_entries,
            "manifest_entry_summary": manifest_entry_summary,
            "human_review_required_before_generation": True,
            "legal_final": False,
            "non_disclosure": {
                "secret_values_printed": False,
                "token_values_printed": False,
                "cookie_values_printed": False,
            },
        },
        "package_output_diff_prediction": {
            "future_package_root": PACKAGE_ROOT,
            "would_create_directories": DIFF_PREDICTION_CREATE_DIRECTORIES,
            "would_create_files": DIFF_PREDICTION_CREATE_FILES,
            "would_copy_source_groups": DIFF_PREDICTION_COPY_SOURCE_GROUPS,
            "would_generate_future_outputs": MANIFEST_PREVIEW_FUTURE_OUTPUTS,
            "output_groups": output_groups,
            "output_group_summary": output_group_summary,
            "no_files_generated": True,
            "human_review_required_before_generation": True,
            "cleanup_rollback_note": (
                "Future package root only; human review required before any action."
            ),
        },
        "source_coverage": {
            "notice_sources": {
                "present": notice_present,
                "total": notice_total,
                "items": notice_items,
            },
            "guide_sources": {
                "present": guide_present,
                "total": guide_total,
                "items": guide_items,
            },
            "missing_notice_sources": missing_notices,
            "missing_guide_sources": missing_guides,
            "local_only_safety_source": {
                "present": safety_present,
                "total": safety_total,
                "items": safety_items,
                "missing": missing_safety,
            },
            "platform_section_sources": {
                "present": platform_present,
                "total": platform_total,
                "items": platform_items,
                "missing": missing_platform,
            },
            "coverage_items": coverage_items,
            "coverage_summary": coverage_summary,
        },
        "excluded_paths_summary": {
            "excluded_rule_count": len(EXCLUDED_PATHS),
            "currently_present_excluded_path_count": len(excluded_found),
            "currently_present_excluded_paths": excluded_found,
            "generated_package_root_present": generated_package_root_present,
            "pr_1001_files_present": pr_1001_files_present,
        },
        "validation": {
            "status": status,
            "generated_package_root_present": generated_package_root_present,
            "pr_1001_leakage": pr_1001_files_present,
            "forbidden_paths": generated_package_root_present or invalid_planned_paths,
            "forbidden_filenames": forbidden_filenames,
            "secret_like_content": secret_like_content,
            "warnings_count": len(warnings),
            "blockers_count": len(blocked),
        },
        "warnings": [finding_to_dict(warning) for warning in warnings],
        "blockers": [finding_to_dict(blocker) for blocker in blocked],
        "safety_flags": {
            "local_only": True,
            "public_hosting": False,
            "ads": False,
            "update_apply": False,
            "docker_pull": False,
            "docker_build": False,
            "git_update": False,
            "package_install": False,
            "credential_handling": False,
            "generated_folder_created": False,
            "implementation_changes": False,
            "backend_changes": False,
            "frontend_changes": False,
            "docker_changes": False,
            "ci_changes": False,
            "package_lockfile_changes": False,
            "pr_1001_files_present": pr_1001_files_present,
        },
        "human_review": {
            "required_before_generation": True,
            "actual_generation_approved": False,
            "checklist": [
                "Status is OK.",
                "Repo safety gate has no blockers.",
                "Clean-package dry-run has no blockers.",
                "Package manifest preview is acceptable.",
                "Package output diff prediction is acceptable.",
                "No generated package folder exists.",
                "No cookie/token/secret values are printed.",
                "PR #1001 files are absent.",
                "No backend/frontend/Docker/CI/package/lockfile changes are mixed in.",
                "Human review is complete before any actual generation task.",
            ],
        },
        "next_step": (
            "Review this report; do not generate package files without a later "
            "explicit human-reviewed task."
        ),
    }


def print_json_report(
    root: Path,
    blocked: list[Finding],
    warnings: list[Finding],
    excluded_found: list[str],
) -> None:
    report = build_json_report(root, blocked, warnings, excluded_found)
    print(json.dumps(report, ensure_ascii=False, indent=2))


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
    print_source_coverage_status(root)
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
    elif args.format == "json":
        print_json_report(root, blocked, warnings, excluded_found)
    else:
        print_report(root, blocked, warnings, excluded_found)
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
