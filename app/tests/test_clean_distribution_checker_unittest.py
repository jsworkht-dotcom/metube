"""Dependency-free tests for the CLEAN distribution candidate checker."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

from scripts.check_clean_distribution import (
    SCAN_SIZE_LIMIT_BYTES,
    format_json_report,
    format_text_report,
    scan_candidate,
)


class CleanDistributionCheckerTests(unittest.TestCase):
    def scan_temp(self, setup):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            setup(root)
            return scan_candidate(root)

    def blocked_paths(self, result):
        return {finding.path for finding in result.blocked}

    def assertBlockedPath(self, result, path: str):
        self.assertIn(path, self.blocked_paths(result))
        self.assertFalse(result.ok)

    def test_clean_minimal_candidate_passes(self):
        result = self.scan_temp(lambda root: (root / "README.txt").write_text("local only\n"))

        self.assertTrue(result.ok)
        self.assertEqual(result.status, "OK")

    def test_missing_candidate_path_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = scan_candidate(Path(temp_dir) / "missing")

        self.assertBlockedPath(result, ".")

    def test_env_file_is_blocked(self):
        result = self.scan_temp(lambda root: (root / ".env").write_text("LOCAL_ONLY_MODE=true\n"))

        self.assertBlockedPath(result, ".env")

    def test_git_directory_is_blocked(self):
        result = self.scan_temp(lambda root: (root / ".git").mkdir())

        self.assertBlockedPath(result, ".git/")

    def test_downloads_directory_is_blocked(self):
        result = self.scan_temp(lambda root: (root / "downloads").mkdir())

        self.assertBlockedPath(result, "downloads/")

    def test_logs_directory_is_blocked(self):
        result = self.scan_temp(lambda root: (root / "logs").mkdir())

        self.assertBlockedPath(result, "logs/")

    def test_cookies_file_is_blocked(self):
        result = self.scan_temp(lambda root: (root / "cookies.txt").write_text("empty\n"))

        self.assertBlockedPath(result, "cookies.txt")

    def test_token_like_filename_is_blocked(self):
        result = self.scan_temp(lambda root: (root / "session-token-note.txt").write_text("x\n"))

        self.assertBlockedPath(result, "session-token-note.txt")

    def test_symlink_is_blocked(self):
        def setup(root: Path) -> None:
            target = root / "target.txt"
            target.write_text("safe\n")
            link = root / "safe-link.txt"
            try:
                link.symlink_to(target)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symlink creation is unavailable: {exc}")

        result = self.scan_temp(setup)

        self.assertBlockedPath(result, "safe-link.txt")

    def test_bearer_token_like_content_is_blocked(self):
        result = self.scan_temp(
            lambda root: (root / "notes.txt").write_text("Authorization: Bearer abc\n")
        )

        self.assertBlockedPath(result, "notes.txt")

    def test_password_assignment_like_content_is_blocked(self):
        result = self.scan_temp(lambda root: (root / "notes.txt").write_text("password=abc\n"))

        self.assertBlockedPath(result, "notes.txt")

    def test_large_file_over_scan_limit_does_not_block_safe_filename(self):
        def setup(root: Path) -> None:
            path = root / "large.txt"
            with path.open("w", encoding="utf-8") as file:
                file.write("Authorization: Bearer abc\n")
                file.write("x" * SCAN_SIZE_LIMIT_BYTES)

        result = self.scan_temp(setup)

        self.assertTrue(result.ok)
        self.assertEqual(result.skipped_large_files, 1)

    def test_report_does_not_include_secret_value(self):
        secret_value = "superSensitiveNeedle123"
        result = self.scan_temp(
            lambda root: (root / "notes.txt").write_text(
                f"Authorization: Bearer {secret_value}\n"
            )
        )

        report = format_text_report(result)

        self.assertFalse(result.ok)
        self.assertNotIn(secret_value, report)
        self.assertIn("Bearer token-like", report)

    def test_json_output_is_parseable(self):
        result = self.scan_temp(lambda root: (root / ".env").write_text("x=1\n"))

        parsed = json.loads(format_json_report(result))

        self.assertEqual(parsed["status"], "BLOCKED")
        self.assertEqual(parsed["summary"]["blocked_count"], 1)


if __name__ == "__main__":
    unittest.main()
