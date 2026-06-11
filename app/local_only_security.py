"""Pure local-only security helpers.

This module intentionally uses only the Python standard library so the core
local-only guard decisions can be tested without aiohttp or pytest.
"""

from __future__ import annotations

import ipaddress
import socket
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
URL_INTAKE_ALLOWED_SCHEMES = {'http', 'https'}
URL_INTAKE_INTERNAL_HOSTS = {'localhost', 'local', 'home', 'lan', 'metadata.google.internal'}
URL_INTAKE_INTERNAL_SUFFIXES = ('.localhost', '.local', '.home', '.lan')
URL_INTAKE_BLOCKED_IPV4_NETWORKS = tuple(
    ipaddress.ip_network(network)
    for network in (
        '0.0.0.0/8',
        '10.0.0.0/8',
        '100.64.0.0/10',
        '127.0.0.0/8',
        '169.254.0.0/16',
        '172.16.0.0/12',
        '192.168.0.0/16',
        '224.0.0.0/4',
        '240.0.0.0/4',
    )
)
URL_INTAKE_BLOCKED_IPV6_NETWORKS = tuple(
    ipaddress.ip_network(network)
    for network in (
        '::/128',
        '::1/128',
        'fc00::/7',
        'fe80::/10',
        'ff00::/8',
    )
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


def browser_origin_allowed(origin_value: str | None, host_value: str | None) -> bool:
    if origin_value is None:
        return True
    if not is_local_hostname(host_value):
        return False
    return source_header_allowed(origin_value, host_value)


def public_host_url_allowed(url_value: str | None) -> bool:
    hostname = absolute_url_hostname(url_value)
    return hostname is None or is_local_hostname(hostname)


def _normalized_url_hostname(hostname: str | None) -> str:
    if hostname is None:
        return ''
    return str(hostname).strip().lower().rstrip('.')


def _ip_address_blocked(ip_address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    if isinstance(ip_address, ipaddress.IPv6Address) and ip_address.ipv4_mapped is not None:
        return _ip_address_blocked(ip_address.ipv4_mapped)

    blocked_networks = (
        URL_INTAKE_BLOCKED_IPV4_NETWORKS
        if ip_address.version == 4
        else URL_INTAKE_BLOCKED_IPV6_NETWORKS
    )
    if any(ip_address in network for network in blocked_networks):
        return True

    return (
        ip_address.is_loopback
        or ip_address.is_private
        or ip_address.is_link_local
        or ip_address.is_unspecified
        or ip_address.is_multicast
        or ip_address.is_reserved
    )


def _blocked_ip_literal(hostname: str) -> bool:
    host_for_ip = hostname.split('%', 1)[0]
    try:
        ip_address = ipaddress.ip_address(host_for_ip)
    except ValueError:
        return False
    return _ip_address_blocked(ip_address)


def _internal_url_hostname(hostname: str) -> bool:
    return hostname in URL_INTAKE_INTERNAL_HOSTS or hostname.endswith(URL_INTAKE_INTERNAL_SUFFIXES)


def _resolved_host_blocked(hostname: str) -> bool:
    try:
        results = socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)
    except OSError:
        return False

    for result in results:
        sockaddr = result[4]
        if not sockaddr:
            continue
        resolved_host = str(sockaddr[0]).split('%', 1)[0]
        try:
            ip_address = ipaddress.ip_address(resolved_host)
        except ValueError:
            continue
        if _ip_address_blocked(ip_address):
            return True
    return False


def url_intake_security_errors(url_value: str | None, *, resolve_dns: bool = False) -> list[str]:
    """Return policy errors for a user-submitted download URL.

    DNS checks are opt-in because validation runs on the request path and should
    not block normal local use on slow or offline networks.
    """
    if url_value is None:
        return ['URL is required']

    url = str(url_value).strip()
    if not url:
        return ['URL is required']
    if any(char.isspace() for char in url):
        return ['URL is malformed']

    try:
        parsed = urlparse(url)
    except ValueError:
        return ['URL is malformed']

    if not parsed.scheme:
        return ['URL scheme is required']
    if parsed.scheme.lower() not in URL_INTAKE_ALLOWED_SCHEMES:
        return ['URL scheme is not allowed']

    try:
        hostname = _normalized_url_hostname(parsed.hostname)
    except ValueError:
        return ['URL is malformed']

    if not hostname:
        return ['URL host is required']
    try:
        parsed.port
    except ValueError:
        return ['URL is malformed']
    if parsed.username is not None or parsed.password is not None:
        return ['URL userinfo is not allowed']
    if _internal_url_hostname(hostname):
        return ['URL host is not allowed']
    if _blocked_ip_literal(hostname):
        return ['URL host address is not allowed']
    if resolve_dns and _resolved_host_blocked(hostname):
        return ['URL resolved address is not allowed']

    return []


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

    if not _enabled(getattr(config, 'URL_INTAKE_GUARD', True)):
        errors.append('URL_INTAKE_GUARD must remain enabled when LOCAL_ONLY_MODE=true')

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
