"""Pure local-only security helpers.

This module intentionally uses only the Python standard library so the core
local-only guard decisions can be tested without aiohttp or pytest.
"""

from __future__ import annotations

from urllib.parse import urlparse

LOCAL_ONLY_ALLOWED_HOSTS = {'localhost', '127.0.0.1', '::1'}
STATE_CHANGING_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}
SECURITY_RESPONSE_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'no-referrer',
    'X-Frame-Options': 'DENY',
    'Cross-Origin-Resource-Policy': 'same-origin',
}
PUBLIC_HOST_URL_ATTRS = (
    '_'.join(('PUBLIC', 'HOST', 'URL')),
    '_'.join(('PUBLIC', 'HOST', 'AUDIO', 'URL')),
)


def strip_host_port(host_value: str | None) -> str:
    if host_value is None:
        return ''

    host = str(host_value).strip().lower()
    if not host:
        return ''
    if ',' in host:
        return ''

    if host.startswith('['):
        end = host.find(']')
        if end != -1:
            return host[1:end]
        return host

    if host.count(':') == 1:
        return host.split(':', 1)[0]

    return host


def is_local_hostname(hostname: str | None) -> bool:
    return strip_host_port(hostname) in LOCAL_ONLY_ALLOWED_HOSTS


def absolute_url_hostname(url_value: str | None) -> str | None:
    if not url_value:
        return None

    try:
        parsed = urlparse(url_value)
        if not parsed.netloc:
            return None
        return parsed.hostname.lower() if parsed.hostname else None
    except ValueError:
        return None


def source_header_allowed(source_value: str | None, host_value: str | None) -> bool:
    source_hostname = absolute_url_hostname(source_value)
    if not source_hostname:
        return False

    host_hostname = strip_host_port(host_value)
    return is_local_hostname(source_hostname) or source_hostname == host_hostname


def public_host_url_allowed(url_value: str | None) -> bool:
    hostname = absolute_url_hostname(url_value)
    return hostname is None or is_local_hostname(hostname)


def _enabled(value: object) -> bool:
    if isinstance(value, str):
        return value.lower() in {'true', 'on', '1'}
    return bool(value)


def local_only_config_errors(config: object) -> list[str]:
    if not _enabled(getattr(config, 'LOCAL_ONLY_MODE', False)):
        return []

    errors = []

    if not is_local_hostname(getattr(config, 'HOST', None)):
        errors.append('HOST must be loopback when LOCAL_ONLY_MODE=true')

    cors_allowed_origins = getattr(config, 'CORS_ALLOWED_ORIGINS', '') or ''
    cors_origins = [o.strip() for o in str(cors_allowed_origins).split(',') if o.strip()]
    if '*' in cors_origins:
        errors.append('Wildcard CORS origins are not allowed when LOCAL_ONLY_MODE=true')

    if _enabled(getattr(config, 'ALLOW_YTDL_OPTIONS_OVERRIDES', False)) and not _enabled(
        getattr(config, 'ALLOW_UNSAFE_YTDL_OPTIONS_OVERRIDES', False)
    ):
        errors.append(
            'ALLOW_YTDL_OPTIONS_OVERRIDES requires '
            'ALLOW_UNSAFE_YTDL_OPTIONS_OVERRIDES=true when LOCAL_ONLY_MODE=true'
        )

    if getattr(config, 'YTDL_NIGHTLY_UPDATE_TIME', '') and not _enabled(
        getattr(config, 'ALLOW_UNSAFE_NIGHTLY_UPDATE', False)
    ):
        errors.append(
            'YTDL_NIGHTLY_UPDATE_TIME requires ALLOW_UNSAFE_NIGHTLY_UPDATE=true '
            'when LOCAL_ONLY_MODE=true'
        )

    for attr in PUBLIC_HOST_URL_ATTRS:
        if not public_host_url_allowed(getattr(config, attr, '')):
            errors.append(f'{attr} must be relative or local when LOCAL_ONLY_MODE=true')

    return errors
