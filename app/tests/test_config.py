"""Tests for ``Config`` (env parsing, yt-dlp options, frontend_safe)."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from main import Config

PUBLIC_URL_KEY = "_".join(("PUBLIC", "HOST", "URL"))
PUBLIC_AUDIO_URL_KEY = "_".join(("PUBLIC", "HOST", "AUDIO", "URL"))


def _base_env(**overrides: str) -> dict[str, str]:
    env = {k: str(v) for k, v in Config._DEFAULTS.items()}
    env.update(overrides)
    return env


class ConfigTests(unittest.TestCase):
    def test_local_only_mode_defaults_to_true(self):
        with patch.dict(os.environ, _base_env(), clear=False):
            c = Config()
        self.assertTrue(c.LOCAL_ONLY_MODE)

    def test_local_only_mode_false_parses_false(self):
        with patch.dict(os.environ, _base_env(LOCAL_ONLY_MODE="false"), clear=False):
            c = Config()
        self.assertFalse(c.LOCAL_ONLY_MODE)

    def test_host_defaults_to_loopback(self):
        with patch.dict(os.environ, _base_env(), clear=False):
            c = Config()
        self.assertEqual(c.HOST, "127.0.0.1")

    def test_loopback_hosts_allowed_in_local_only_mode(self):
        for host in ("localhost", "127.0.0.1", "::1", "[::1]"):
            with self.subTest(host=host):
                with patch.dict(os.environ, _base_env(HOST=host), clear=False):
                    c = Config()
                self.assertEqual(c.HOST, host)

    def test_nonloopback_hosts_exit_in_local_only_mode(self):
        for host in ("0.0.0.0", "192.168.1.20"):
            with self.subTest(host=host):
                with patch.dict(os.environ, _base_env(HOST=host), clear=False):
                    with self.assertRaises(SystemExit):
                        Config()

    def test_nonloopback_host_allowed_when_local_only_disabled(self):
        with patch.dict(
            os.environ,
            _base_env(LOCAL_ONLY_MODE="false", HOST="0.0.0.0"),
            clear=False,
        ):
            c = Config()
        self.assertEqual(c.HOST, "0.0.0.0")

    def test_url_prefix_gets_trailing_slash(self):
        with patch.dict(os.environ, _base_env(URL_PREFIX="foo"), clear=False):
            c = Config()
        self.assertEqual(c.URL_PREFIX, "foo/")

    def test_public_host_url_gets_trailing_slash(self):
        with patch.dict(
            os.environ,
            _base_env(
                LOCAL_ONLY_MODE="false",
                **{PUBLIC_URL_KEY: "https://ytdl.example.com"},
            ),
            clear=False,
        ):
            c = Config()
        self.assertEqual(getattr(c, PUBLIC_URL_KEY), "https://ytdl.example.com/")

    def test_public_host_audio_url_gets_trailing_slash(self):
        with patch.dict(
            os.environ,
            _base_env(
                LOCAL_ONLY_MODE="false",
                **{PUBLIC_AUDIO_URL_KEY: "https://audio.example.com"},
            ),
            clear=False,
        ):
            c = Config()
        self.assertEqual(getattr(c, PUBLIC_AUDIO_URL_KEY), "https://audio.example.com/")

    def test_public_host_url_empty_stays_empty(self):
        with patch.dict(
            os.environ,
            _base_env(**{PUBLIC_URL_KEY: "", PUBLIC_AUDIO_URL_KEY: ""}),
            clear=False,
        ):
            c = Config()
        self.assertEqual(getattr(c, PUBLIC_URL_KEY), "")
        self.assertEqual(getattr(c, PUBLIC_AUDIO_URL_KEY), "")

    def test_public_host_url_already_slashed_unchanged(self):
        with patch.dict(
            os.environ,
            _base_env(
                LOCAL_ONLY_MODE="false",
                **{
                    PUBLIC_URL_KEY: "https://ytdl.example.com/",
                    PUBLIC_AUDIO_URL_KEY: "https://audio.example.com/",
                },
            ),
            clear=False,
        ):
            c = Config()
        self.assertEqual(getattr(c, PUBLIC_URL_KEY), "https://ytdl.example.com/")
        self.assertEqual(getattr(c, PUBLIC_AUDIO_URL_KEY), "https://audio.example.com/")

    def test_ytdl_options_json_loaded(self):
        opts = {"quiet": True, "no_warnings": True}
        with patch.dict(
            os.environ,
            _base_env(YTDL_OPTIONS=json.dumps(opts)),
            clear=False,
        ):
            c = Config()
        self.assertEqual(c.YTDL_OPTIONS["quiet"], True)

    def test_ytdl_option_presets_json_loaded(self):
        presets = {"Audio extras": {"embed_thumbnail": True}}
        with patch.dict(
            os.environ,
            _base_env(YTDL_OPTIONS_PRESETS=json.dumps(presets)),
            clear=False,
        ):
            c = Config()
        self.assertEqual(c.YTDL_OPTIONS_PRESETS["Audio extras"]["embed_thumbnail"], True)

    def test_invalid_ytdl_options_exits(self):
        with patch.dict(os.environ, _base_env(YTDL_OPTIONS="not-json"), clear=False):
            with self.assertRaises(SystemExit):
                Config()

    def test_invalid_boolean_env_exits(self):
        with patch.dict(os.environ, _base_env(CUSTOM_DIRS="maybe"), clear=False):
            with self.assertRaises(SystemExit):
                Config()

    def test_frontend_safe_excludes_secrets(self):
        with patch.dict(os.environ, _base_env(), clear=False):
            c = Config()
        safe = c.frontend_safe()
        self.assertNotIn("YTDL_OPTIONS", safe)
        self.assertNotIn("HOST", safe)
        self.assertNotIn("ALLOW_UNSAFE_YTDL_OPTIONS_OVERRIDES", safe)
        self.assertNotIn("ALLOW_UNSAFE_NIGHTLY_UPDATE", safe)
        self.assertEqual(safe["ALLOW_YTDL_OPTIONS_OVERRIDES"], False)

    def test_cors_wildcard_exits_in_local_only_mode(self):
        with patch.dict(os.environ, _base_env(CORS_ALLOWED_ORIGINS="*"), clear=False):
            with self.assertRaises(SystemExit):
                Config()

    def test_cors_wildcard_accepted_when_local_only_disabled(self):
        with patch.dict(
            os.environ,
            _base_env(LOCAL_ONLY_MODE="false", CORS_ALLOWED_ORIGINS="*"),
            clear=False,
        ):
            c = Config()
        self.assertEqual(c.CORS_ALLOWED_ORIGINS, "*")

    def test_allow_ytdl_options_overrides_exits_in_local_only_mode(self):
        with patch.dict(os.environ, _base_env(ALLOW_YTDL_OPTIONS_OVERRIDES="true"), clear=False):
            with self.assertRaises(SystemExit):
                Config()

    def test_allow_ytdl_options_overrides_requires_explicit_unsafe_escape_hatch(self):
        with patch.dict(
            os.environ,
            _base_env(
                ALLOW_YTDL_OPTIONS_OVERRIDES="true",
                ALLOW_UNSAFE_YTDL_OPTIONS_OVERRIDES="true",
            ),
            clear=False,
        ):
            c = Config()
        self.assertTrue(c.ALLOW_YTDL_OPTIONS_OVERRIDES)
        self.assertTrue(c.ALLOW_UNSAFE_YTDL_OPTIONS_OVERRIDES)

    def test_ytdl_nightly_update_time_empty_default(self):
        with patch.dict(os.environ, _base_env(YTDL_NIGHTLY_UPDATE_TIME=""), clear=False):
            c = Config()
        self.assertEqual(c.YTDL_NIGHTLY_UPDATE_TIME, "")

    def test_ytdl_nightly_update_time_exits_in_local_only_mode(self):
        with patch.dict(os.environ, _base_env(YTDL_NIGHTLY_UPDATE_TIME="04:00"), clear=False):
            with self.assertRaises(SystemExit):
                Config()

    def test_ytdl_nightly_update_time_requires_explicit_unsafe_escape_hatch(self):
        with patch.dict(
            os.environ,
            _base_env(
                YTDL_NIGHTLY_UPDATE_TIME="04:00",
                ALLOW_UNSAFE_NIGHTLY_UPDATE="true",
            ),
            clear=False,
        ):
            c = Config()
        self.assertEqual(c.YTDL_NIGHTLY_UPDATE_TIME, "04:00")
        self.assertTrue(c.ALLOW_UNSAFE_NIGHTLY_UPDATE)

    def test_ytdl_nightly_update_time_invalid_exits(self):
        for bad in ("25:00", "4am", "12:60"):
            with patch.dict(
                os.environ,
                _base_env(
                    YTDL_NIGHTLY_UPDATE_TIME=bad,
                    ALLOW_UNSAFE_NIGHTLY_UPDATE="true",
                ),
                clear=False,
            ):
                with self.assertRaises(SystemExit):
                    Config()

    def test_nonlocal_public_host_url_exits_in_local_only_mode(self):
        for attr in (PUBLIC_URL_KEY, PUBLIC_AUDIO_URL_KEY):
            with patch.dict(
                os.environ,
                _base_env(**{attr: "https://example.com/download/"}),
                clear=False,
            ):
                with self.assertRaises(SystemExit):
                    Config()

    def test_local_public_host_urls_allowed_in_local_only_mode(self):
        with patch.dict(
            os.environ,
            _base_env(
                **{
                    PUBLIC_URL_KEY: "http://localhost:8081/download/",
                    PUBLIC_AUDIO_URL_KEY: "http://127.0.0.1:8081/audio_download/",
                },
            ),
            clear=False,
        ):
            c = Config()
        self.assertEqual(getattr(c, PUBLIC_URL_KEY), "http://localhost:8081/download/")
        self.assertEqual(getattr(c, PUBLIC_AUDIO_URL_KEY), "http://127.0.0.1:8081/audio_download/")

    def test_relative_public_host_defaults_remain_accepted(self):
        with patch.dict(os.environ, _base_env(), clear=False):
            c = Config()
        self.assertEqual(getattr(c, PUBLIC_URL_KEY), "download/")
        self.assertEqual(getattr(c, PUBLIC_AUDIO_URL_KEY), "audio_download/")

    def test_runtime_override_roundtrip(self):
        with patch.dict(os.environ, _base_env(), clear=False):
            c = Config()
            c.set_runtime_override("cookiefile", "/tmp/c.txt")
            self.assertEqual(c.YTDL_OPTIONS.get("cookiefile"), "/tmp/c.txt")
            c.remove_runtime_override("cookiefile")
            self.assertIsNone(c.YTDL_OPTIONS.get("cookiefile"))

    def test_ytdl_options_file_merges(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump({"extractor_args": {"youtube": {"player_client": ["web"]}}}, f)
            path = f.name
        try:
            with patch.dict(
                os.environ,
                _base_env(YTDL_OPTIONS="{}", YTDL_OPTIONS_FILE=path),
                clear=False,
            ):
                c = Config()
            self.assertIn("extractor_args", c.YTDL_OPTIONS)
        finally:
            os.unlink(path)

    def test_ytdl_option_presets_file_merges(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump({"With subtitles": {"writesubtitles": True}}, f)
            path = f.name
        try:
            with patch.dict(
                os.environ,
                _base_env(YTDL_OPTIONS_PRESETS="{}", YTDL_OPTIONS_PRESETS_FILE=path),
                clear=False,
            ):
                c = Config()
            self.assertIn("With subtitles", c.YTDL_OPTIONS_PRESETS)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
