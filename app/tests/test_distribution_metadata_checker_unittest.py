"""Dependency-free tests for the CLEAN distribution metadata checker."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.check_distribution_metadata import (
    format_json_report,
    format_text_report,
    scan_candidate,
)


class DistributionMetadataCheckerTests(unittest.TestCase):
    def scan_temp(self, setup):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_valid_candidate(root)
            setup(root)
            return scan_candidate(root)

    def blocked_paths(self, result):
        return {finding.path for finding in result.blocked}

    def warning_paths(self, result):
        return {finding.path for finding in result.warnings}

    def assertBlockedPath(self, result, path: str):
        self.assertIn(path, self.blocked_paths(result))
        self.assertFalse(result.ok)

    def test_valid_minimal_candidate_passes(self):
        result = self.scan_temp(lambda root: None)

        self.assertTrue(result.ok)
        self.assertEqual(result.status, "OK")

    def test_missing_version_txt_blocks(self):
        result = self.scan_temp(lambda root: (root / "VERSION.txt").unlink())

        self.assertBlockedPath(result, "VERSION.txt")

    def test_missing_manifest_json_blocks(self):
        result = self.scan_temp(lambda root: (root / "MANIFEST.json").unlink())

        self.assertBlockedPath(result, "MANIFEST.json")

    def test_missing_checksums_blocks(self):
        result = self.scan_temp(lambda root: (root / "checksums.sha256").unlink())

        self.assertBlockedPath(result, "checksums.sha256")

    def test_missing_license_blocks(self):
        result = self.scan_temp(lambda root: (root / "LICENSE").unlink())

        self.assertBlockedPath(result, "LICENSE")

    def test_missing_notice_blocks(self):
        result = self.scan_temp(lambda root: (root / "NOTICE").unlink())

        self.assertBlockedPath(result, "NOTICE")

    def test_invalid_json_blocks(self):
        def setup(root: Path) -> None:
            (root / "MANIFEST.json").write_text("{bad json\n", encoding="utf-8")
            write_checksums(root)

        result = self.scan_temp(setup)

        self.assertBlockedPath(result, "MANIFEST.json")

    def test_local_only_false_blocks(self):
        def setup(root: Path) -> None:
            write_manifest(root, {"local_only": False})
            write_checksums(root)

        result = self.scan_temp(setup)

        self.assertBlockedPath(result, "MANIFEST.json")

    def test_manifest_version_mismatch_blocks(self):
        def setup(root: Path) -> None:
            write_manifest(root, {"version": "2.0.0"})
            write_checksums(root)

        result = self.scan_temp(setup)

        self.assertBlockedPath(result, "MANIFEST.json")

    def test_invalid_source_commit_blocks(self):
        def setup(root: Path) -> None:
            write_manifest(root, {"source_commit": "not-a-sha"})
            write_checksums(root)

        result = self.scan_temp(setup)

        self.assertBlockedPath(result, "MANIFEST.json")

    def test_malformed_checksum_line_blocks(self):
        def setup(root: Path) -> None:
            (root / "checksums.sha256").write_text("not a checksum line\n", encoding="utf-8")

        result = self.scan_temp(setup)

        self.assertBlockedPath(result, "checksums.sha256")

    def test_checksum_path_with_parent_reference_blocks(self):
        def setup(root: Path) -> None:
            digest = "0" * 64
            (root / "checksums.sha256").write_text(
                f"{digest}  ../outside.txt\n", encoding="utf-8"
            )

        result = self.scan_temp(setup)

        self.assertBlockedPath(result, "checksums.sha256")

    def test_checksum_absolute_path_blocks(self):
        def setup(root: Path) -> None:
            digest = "0" * 64
            (root / "checksums.sha256").write_text(
                f"{digest}  /absolute.txt\n", encoding="utf-8"
            )

        result = self.scan_temp(setup)

        self.assertBlockedPath(result, "checksums.sha256")

    def test_checksum_missing_listed_file_blocks(self):
        def setup(root: Path) -> None:
            digest = "0" * 64
            (root / "checksums.sha256").write_text(
                f"{digest}  missing.txt\n", encoding="utf-8"
            )

        result = self.scan_temp(setup)

        self.assertBlockedPath(result, "missing.txt")

    def test_checksum_mismatch_blocks(self):
        def setup(root: Path) -> None:
            (root / "README.txt").write_text("changed after checksum\n", encoding="utf-8")

        result = self.scan_temp(setup)

        self.assertBlockedPath(result, "README.txt")

    def test_duplicate_checksum_path_blocks(self):
        def setup(root: Path) -> None:
            digest = hash_file(root / "README.txt")
            (root / "checksums.sha256").write_text(
                f"{digest}  README.txt\n{digest}  README.txt\n",
                encoding="utf-8",
            )

        result = self.scan_temp(setup)

        self.assertBlockedPath(result, "README.txt")

    def test_valid_checksum_passes(self):
        def setup(root: Path) -> None:
            docs = root / "docs"
            docs.mkdir()
            (docs / "usage.txt").write_text("local use only\n", encoding="utf-8")
            write_checksums(root, ["docs/usage.txt"])

        result = self.scan_temp(setup)

        self.assertTrue(result.ok)

    def test_extra_unlisted_file_warns_not_blocks(self):
        def setup(root: Path) -> None:
            (root / "EXTRA.txt").write_text("not listed yet\n", encoding="utf-8")

        result = self.scan_temp(setup)

        self.assertTrue(result.ok)
        self.assertIn("EXTRA.txt", self.warning_paths(result))

    def test_secret_like_license_content_blocks_and_report_is_sanitized(self):
        secret_value = "superSensitiveNeedle123"

        def setup(root: Path) -> None:
            (root / "LICENSE").write_text(
                f"Authorization: Bearer {secret_value}\n", encoding="utf-8"
            )
            write_checksums(root)

        result = self.scan_temp(setup)
        report = format_text_report(result)

        self.assertBlockedPath(result, "LICENSE")
        self.assertIn("Bearer token-like", report)
        self.assertNotIn(secret_value, report)

    def test_json_output_is_parseable(self):
        result = self.scan_temp(lambda root: None)

        parsed = json.loads(format_json_report(result))

        self.assertEqual(parsed["status"], "OK")
        self.assertEqual(parsed["summary"]["blocked_count"], 0)


def default_manifest() -> dict[str, object]:
    return {
        "package_name": "MeTube local-only clean portable",
        "version": "1.0.0-local",
        "source_commit": "f2e2678e3dc986a34f2e5bb0bd65f56d54b2b415",
        "created_from": "fork/master",
        "local_only": True,
        "distribution_type": "local-only-clean-portable",
    }


def write_valid_candidate(root: Path) -> None:
    (root / "VERSION.txt").write_text("1.0.0-local\n", encoding="utf-8")
    write_manifest(root)
    (root / "LICENSE").write_text("License notice placeholder\n", encoding="utf-8")
    (root / "NOTICE").write_text("Notice placeholder\n", encoding="utf-8")
    (root / "README.txt").write_text("Local-only candidate\n", encoding="utf-8")
    write_checksums(root)


def write_manifest(root: Path, overrides: dict[str, object] | None = None) -> None:
    manifest = default_manifest()
    if overrides:
        manifest.update(overrides)
    (root / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_checksums(root: Path, extra_paths: list[str] | None = None) -> None:
    paths = [
        "VERSION.txt",
        "MANIFEST.json",
        "LICENSE",
        "NOTICE",
        "README.txt",
    ]
    if extra_paths:
        paths.extend(extra_paths)

    lines = [f"{hash_file(root / path)}  {path}" for path in paths]
    (root / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
