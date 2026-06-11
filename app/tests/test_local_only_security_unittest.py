"""Dependency-free tests for local-only security helper decisions."""

from __future__ import annotations

from types import SimpleNamespace
import unittest

from app.local_only_security import (
    browser_origin_allowed,
    contains_sensitive_url_material,
    is_local_hostname,
    local_only_config_errors,
    public_host_url_allowed,
    redact_text_for_log,
    redact_url_for_log,
    sanitize_filename_component,
    source_header_allowed,
    strip_host_port,
    url_intake_security_errors,
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
        'URL_INTAKE_GUARD': True,
        PUBLIC_URL_KEY: 'download/',
        PUBLIC_AUDIO_URL_KEY: 'audio_download/',
    }
    for key, value in defaults.items():
        setattr(config, key, value)
    for key, value in overrides.items():
        setattr(config, key, value)
    return config


class LocalOnlySecurityTests(unittest.TestCase):
    def assertUrlAllowed(self, url: str) -> None:
        self.assertEqual(url_intake_security_errors(url), [])

    def assertUrlBlocked(self, url: str | None) -> None:
        self.assertTrue(url_intake_security_errors(url))

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

    def test_browser_origin_allows_missing_and_local_origin(self):
        self.assertTrue(browser_origin_allowed(None, 'localhost:8081'))
        for origin in (
            'http://localhost:8081',
            'http://127.0.0.1:8081',
            'http://[::1]:8081',
        ):
            with self.subTest(origin=origin):
                self.assertTrue(browser_origin_allowed(origin, 'localhost:8081'))

    def test_browser_origin_rejects_nonlocal_invalid_and_same_nonlocal_host(self):
        for origin, host in (
            ('https://example.com', 'localhost:8081'),
            ('http://[::1', 'localhost:8081'),
            ('https://example.com', 'example.com'),
        ):
            with self.subTest(origin=origin, host=host):
                self.assertFalse(browser_origin_allowed(origin, host))

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

    def test_url_intake_allows_public_urls(self):
        for url in (
            'https://www.youtube.com/watch?v=test',
            'https://youtu.be/test',
            'http://example.com/video',
            'https://example.com/path?x=1',
        ):
            with self.subTest(url=url):
                self.assertUrlAllowed(url)

    def test_url_intake_blocks_disallowed_schemes_and_missing_hosts(self):
        for url in (
            'file:///etc/passwd',
            'ftp://example.com/file',
            'data:text/plain,hello',
            'javascript:alert(1)',
            'http:///missing-host',
        ):
            with self.subTest(url=url):
                self.assertUrlBlocked(url)

    def test_url_intake_blocks_local_private_and_special_ips(self):
        for url in (
            'http://localhost:8081/',
            'http://127.0.0.1:8081/',
            'http://0.0.0.0/',
            'http://192.168.1.20/video',
            'http://10.0.0.5/video',
            'http://172.16.0.1/video',
            'http://169.254.169.254/latest/meta-data/',
            'http://100.64.0.1/video',
            'http://224.0.0.1/video',
            'http://240.0.0.1/video',
            'http://255.255.255.255/video',
            'http://[::1]/',
            'http://[fc00::1]/',
            'http://[fe80::1]/',
            'http://[::]/',
            'http://[ff00::1]/',
            'http://[::ffff:127.0.0.1]/',
        ):
            with self.subTest(url=url):
                self.assertUrlBlocked(url)

    def test_url_intake_blocks_userinfo(self):
        self.assertUrlBlocked('https://user:pass@example.com/video')

    def test_url_intake_blocks_internal_hostnames(self):
        for url in (
            'http://printer.local/',
            'http://router.lan/',
            'http://metadata.google.internal/',
        ):
            with self.subTest(url=url):
                self.assertUrlBlocked(url)

    def test_url_intake_blocks_malformed_empty_and_relative_values(self):
        for url in (
            '',
            '   ',
            'not-a-url',
            'https://example.com:99999/',
            'https://example.com/a b',
            None,
        ):
            with self.subTest(url=url):
                self.assertUrlBlocked(url)

    def test_url_redaction_strips_query_fragment_userinfo_and_path(self):
        cases = {
            'https://example.com/watch?v=abc&token=secret': 'https://example.com/[redacted]',
            'https://example.com/watch#secret-fragment': 'https://example.com/[redacted]',
            'https://user:pass@example.com/video': 'https://example.com/[redacted]',
            'http://127.0.0.1:8081/private?x=1': 'http://127.0.0.1/[redacted]',
        }
        for raw_url, redacted in cases.items():
            with self.subTest(raw_url=raw_url):
                self.assertEqual(redact_url_for_log(raw_url), redacted)

    def test_url_redaction_uses_placeholder_for_malformed_or_missing_values(self):
        self.assertEqual(redact_url_for_log('not-a-url-with-token=abc'), '[redacted]')
        self.assertEqual(redact_url_for_log(None), '[redacted]')

    def test_sensitive_url_material_detection(self):
        for value in (
            'https://example.com/watch?v=abc',
            'https://example.com/video',
            'https://user:pass@example.com/video',
            'token=abc123',
            'Cookie: sessionid=abc',
            'C:\\Users\\name\\file',
            '/home/name/file',
        ):
            with self.subTest(value=value):
                self.assertTrue(contains_sensitive_url_material(value))
        self.assertFalse(contains_sensitive_url_material('plain status message'))

    def test_text_redaction_replaces_secret_like_values(self):
        cases = {
            'token=abc123': 'token=[redacted]',
            'access_token=abc123': 'access_token=[redacted]',
            'api_key=abc123': 'api_key=[redacted]',
            'password=abc123': 'password=[redacted]',
            'secret=abc123': 'secret=[redacted]',
            'Authorization: Bearer abc.def.ghi': 'Authorization: Bearer [redacted]',
            'Cookie: sessionid=abc': 'Cookie: [redacted]',
        }
        for raw_text, redacted in cases.items():
            with self.subTest(raw_text=raw_text):
                self.assertEqual(redact_text_for_log(raw_text), redacted)

    def test_text_redaction_keeps_benign_text_readable(self):
        text = 'Download completed with public metadata'
        self.assertEqual(redact_text_for_log(text), text)

    def test_filename_sanitization_removes_traversal_and_path_material(self):
        traversal = sanitize_filename_component('../secret')
        self.assertNotIn('..', traversal)
        self.assertNotIn('/', traversal)
        self.assertNotIn('\\', traversal)

        windows_path = sanitize_filename_component('C:\\Users\\name\\file')
        self.assertNotIn(':', windows_path)
        self.assertNotIn('\\', windows_path)
        self.assertNotIn('/', windows_path)

    def test_filename_sanitization_handles_reserved_and_invalid_names(self):
        self.assertEqual(sanitize_filename_component('CON'), 'download')
        self.assertEqual(sanitize_filename_component('NUL.txt'), 'download')
        sanitized = sanitize_filename_component('video:title?*')
        for invalid in '<>:"/\\|?*':
            self.assertNotIn(invalid, sanitized)
        self.assertTrue(sanitized.startswith('video'))

    def test_filename_sanitization_removes_controls_trailing_dots_and_limits_length(self):
        self.assertEqual(sanitize_filename_component('bad\x00name'), 'badname')
        self.assertEqual(sanitize_filename_component('video.  '), 'video')
        self.assertLessEqual(len(sanitize_filename_component('a' * 200)), 120)
        self.assertEqual(sanitize_filename_component(''), 'download')

    def test_filename_sanitization_preserves_japanese_text(self):
        self.assertEqual(sanitize_filename_component('動画タイトル'), '動画タイトル')

    def test_safe_default_like_config_returns_no_errors(self):
        self.assertEqual(local_only_config_errors(_safe_config()), [])

    def test_nonloopback_host_returns_config_error(self):
        for host in ('0.0.0.0', '192.168.1.20'):
            with self.subTest(host=host):
                self.assertIn(
                    'HOST must be loopback when LOCAL_ONLY_MODE=true',
                    local_only_config_errors(_safe_config(HOST=host)),
                )

    def test_url_intake_guard_must_remain_enabled_in_local_only_mode(self):
        self.assertIn(
            'URL_INTAKE_GUARD must remain enabled when LOCAL_ONLY_MODE=true',
            local_only_config_errors(_safe_config(URL_INTAKE_GUARD=False)),
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
