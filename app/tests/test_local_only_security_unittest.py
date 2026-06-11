"""Dependency-free tests for local-only security helper decisions."""

from __future__ import annotations

from types import SimpleNamespace
import unittest

from app.local_only_security import (
    is_local_hostname,
    local_only_config_errors,
    public_host_url_allowed,
    source_header_allowed,
    strip_host_port,
)

PUBLIC_URL_KEY = '_'.join(('PUBLIC', 'HOST', 'URL'))
PUBLIC_AUDIO_URL_KEY = '_'.join(('PUBLIC', 'HOST', 'AUDIO', 'URL'))
ALLOW_OVERRIDES_KEY = '_'.join(('ALLOW', 'YTDL', 'OPTIONS', 'OVERRIDES'))
ALLOW_UNSAFE_OVERRIDES_KEY = '_'.join(('ALLOW', 'UNSAFE', 'YTDL', 'OPTIONS', 'OVERRIDES'))


def _safe_config(**overrides):
    config = SimpleNamespace()
    defaults = {
        'LOCAL_ONLY_MODE': True,
        'HOST': '127.0.0.1',
        'CORS_ALLOWED_ORIGINS': '',
        ALLOW_OVERRIDES_KEY: False,
        ALLOW_UNSAFE_OVERRIDES_KEY: False,
        'YTDL_NIGHTLY_UPDATE_TIME': '',
        'ALLOW_UNSAFE_NIGHTLY_UPDATE': False,
        PUBLIC_URL_KEY: 'download/',
        PUBLIC_AUDIO_URL_KEY: 'audio_download/',
    }
    for key, value in defaults.items():
        setattr(config, key, value)
    for key, value in overrides.items():
        setattr(config, key, value)
    return config


class LocalOnlySecurityTests(unittest.TestCase):
    def test_local_host_parsing_allows_loopback_values(self):
        cases = {
            'localhost': 'localhost',
            'localhost:8081': 'localhost',
            '127.0.0.1': '127.0.0.1',
            '127.0.0.1:8081': '127.0.0.1',
            '::1': '::1',
            '[::1]': '::1',
            '[::1]:8081': '::1',
        }
        for host, stripped in cases.items():
            with self.subTest(host=host):
                self.assertEqual(strip_host_port(host), stripped)
                self.assertTrue(is_local_hostname(host))

    def test_local_host_parsing_rejects_nonlocal_and_suspicious_values(self):
        for host in ('0.0.0.0', '192.168.1.20', 'localhost,example.com'):
            with self.subTest(host=host):
                self.assertFalse(is_local_hostname(host))

    def test_source_header_allowed_for_loopback_sources(self):
        for source in (
            'http://localhost:8081',
            'http://127.0.0.1:8081',
            'http://[::1]:8081',
        ):
            with self.subTest(source=source):
                self.assertTrue(source_header_allowed(source, 'localhost:8081'))

    def test_source_header_rejects_nonlocal_invalid_and_missing_sources(self):
        for source in ('https://example.com', 'http://[::1', None):
            with self.subTest(source=source):
                self.assertFalse(source_header_allowed(source, 'localhost:8081'))

    def test_public_host_url_allows_relative_and_loopback_urls(self):
        for url in (
            'download/',
            'audio_download/',
            'http://localhost:8081/download/',
            'http://127.0.0.1:8081/download/',
            'http://[::1]:8081/download/',
        ):
            with self.subTest(url=url):
                self.assertTrue(public_host_url_allowed(url))

    def test_public_host_url_rejects_nonlocal_urls(self):
        for url in ('https://example.com/download/', 'http://192.168.1.20/download/'):
            with self.subTest(url=url):
                self.assertFalse(public_host_url_allowed(url))

    def test_safe_default_like_config_returns_no_errors(self):
        self.assertEqual(local_only_config_errors(_safe_config()), [])

    def test_nonloopback_host_returns_config_error(self):
        for host in ('0.0.0.0', '192.168.1.20'):
            with self.subTest(host=host):
                self.assertIn(
                    'HOST must be loopback when LOCAL_ONLY_MODE=true',
                    local_only_config_errors(_safe_config(HOST=host)),
                )

    def test_wildcard_cors_returns_config_error(self):
        self.assertIn(
            'Wildcard CORS origins are not allowed when LOCAL_ONLY_MODE=true',
            local_only_config_errors(_safe_config(CORS_ALLOWED_ORIGINS='*')),
        )

    def test_ytdl_override_requires_unsafe_hatch(self):
        errors = local_only_config_errors(_safe_config(**{ALLOW_OVERRIDES_KEY: True}))
        self.assertTrue(any('OVERRIDES requires' in error for error in errors))

        errors = local_only_config_errors(
            _safe_config(
                **{
                    ALLOW_OVERRIDES_KEY: True,
                    ALLOW_UNSAFE_OVERRIDES_KEY: True,
                }
            )
        )
        self.assertFalse(any('OVERRIDES requires' in error for error in errors))

    def test_nightly_update_requires_unsafe_hatch(self):
        errors = local_only_config_errors(_safe_config(YTDL_NIGHTLY_UPDATE_TIME='04:00'))
        self.assertIn(
            'YTDL_NIGHTLY_UPDATE_TIME requires ALLOW_UNSAFE_NIGHTLY_UPDATE=true '
            'when LOCAL_ONLY_MODE=true',
            errors,
        )

        errors = local_only_config_errors(
            _safe_config(
                YTDL_NIGHTLY_UPDATE_TIME='04:00',
                ALLOW_UNSAFE_NIGHTLY_UPDATE=True,
            )
        )
        self.assertNotIn(
            'YTDL_NIGHTLY_UPDATE_TIME requires ALLOW_UNSAFE_NIGHTLY_UPDATE=true '
            'when LOCAL_ONLY_MODE=true',
            errors,
        )

    def test_nonlocal_public_host_urls_return_config_errors(self):
        self.assertIn(
            f'{PUBLIC_URL_KEY} must be relative or local when LOCAL_ONLY_MODE=true',
            local_only_config_errors(_safe_config(**{PUBLIC_URL_KEY: 'https://example.com/download/'})),
        )
        self.assertIn(
            f'{PUBLIC_AUDIO_URL_KEY} must be relative or local when LOCAL_ONLY_MODE=true',
            local_only_config_errors(
                _safe_config(**{PUBLIC_AUDIO_URL_KEY: 'https://example.com/audio_download/'})
            ),
        )

    def test_local_only_disabled_returns_no_local_only_errors(self):
        errors = local_only_config_errors(
            _safe_config(
                LOCAL_ONLY_MODE=False,
                HOST='0.0.0.0',
                CORS_ALLOWED_ORIGINS='*',
                YTDL_NIGHTLY_UPDATE_TIME='04:00',
                **{
                    ALLOW_OVERRIDES_KEY: True,
                    PUBLIC_URL_KEY: 'https://example.com/download/',
                    PUBLIC_AUDIO_URL_KEY: 'https://example.com/audio_download/',
                }
            )
        )
        self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main()
