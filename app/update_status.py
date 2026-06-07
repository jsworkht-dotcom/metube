"""Readonly update status metadata checks."""

from __future__ import annotations

import asyncio
import copy
import re
from datetime import datetime, timezone

import aiohttp

UPDATE_STATUS_CACHE_TTL_SECONDS = 300
UPDATE_STATUS_TIMEOUT_SECONDS = 3
METUBE_UPSTREAM_TAGS_URL = 'https://api.github.com/repos/alexta69/metube/tags?per_page=1'
YTDLP_PYPI_URL = 'https://pypi.org/pypi/yt-dlp/json'
_UPDATE_STATUS_CACHE = {
    'expires_at': 0.0,
    'payload': None,
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def _version_key(version: str | None) -> tuple[int, ...]:
    if not version:
        return ()
    return tuple(int(part) for part in re.findall(r'\d+', version))


def _compare_update_status(current: str | None, latest: str | None) -> str:
    if not latest:
        return 'check_failed'
    if current == 'dev':
        return 'development'
    if not current:
        return 'unknown'
    current_key = _version_key(current)
    latest_key = _version_key(latest)
    if current_key and latest_key:
        return 'update_available' if latest_key > current_key else 'latest'
    return 'latest' if current == latest else 'unknown'


def _update_target(
    name: str,
    current: str | None,
    latest: str | None,
    source: str,
    message: str = '',
) -> dict:
    status = _compare_update_status(current, latest)
    return {
        'name': name,
        'current': current,
        'latest': latest,
        'status': status,
        'source': source,
        'message': message,
    }


def _failed_update_target(name: str, current: str | None, source: str, message: str) -> dict:
    return {
        'name': name,
        'current': current,
        'latest': None,
        'status': 'check_failed',
        'source': source,
        'message': message,
    }


def _docker_update_target() -> dict:
    return {
        'name': 'Docker image',
        'current': None,
        'latest': None,
        'status': 'not_checked',
        'source': 'ghcr.io/alexta69/metube',
        'message': 'Docker registry state is not auto-classified in the first readonly check.',
    }


def _overall_update_status(targets: dict) -> str:
    statuses = [
        target.get('status')
        for key, target in targets.items()
        if key != 'docker_image'
    ]
    if 'update_available' in statuses:
        return 'update_available'
    if 'check_failed' in statuses:
        return 'check_failed'
    if 'development' in statuses:
        return 'development'
    if 'unknown' in statuses:
        return 'check_failed'
    return 'latest'


def _add_update_cache_meta(payload: dict, *, hit: bool) -> dict:
    result = copy.deepcopy(payload)
    result['cache'] = {
        'hit': hit,
        'ttl_seconds': UPDATE_STATUS_CACHE_TTL_SECONDS,
    }
    return result


async def fetch_update_json(session, url: str):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json(content_type=None)


async def build_update_status_payload(metube_current: str, ytdlp_current: str) -> dict:
    timeout = aiohttp.ClientTimeout(total=UPDATE_STATUS_TIMEOUT_SECONDS)
    headers = {'User-Agent': 'metube-readonly-update-status'}
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        metube_result, ytdlp_result = await asyncio.gather(
            fetch_update_json(session, METUBE_UPSTREAM_TAGS_URL),
            fetch_update_json(session, YTDLP_PYPI_URL),
            return_exceptions=True,
        )

    if isinstance(metube_result, Exception):
        metube_target = _failed_update_target(
            'MeTube source',
            metube_current,
            METUBE_UPSTREAM_TAGS_URL,
            'Failed to fetch upstream metadata.',
        )
    else:
        latest_tag = None
        if isinstance(metube_result, list) and metube_result and isinstance(metube_result[0], dict):
            latest_tag = metube_result[0].get('name')
        metube_target = _update_target('MeTube source', metube_current, latest_tag, METUBE_UPSTREAM_TAGS_URL)

    if isinstance(ytdlp_result, Exception):
        ytdlp_target = _failed_update_target(
            'yt-dlp stable',
            ytdlp_current,
            YTDLP_PYPI_URL,
            'Failed to fetch yt-dlp metadata.',
        )
    else:
        latest_ytdlp = None
        if isinstance(ytdlp_result, dict):
            latest_ytdlp = ytdlp_result.get('info', {}).get('version')
        ytdlp_target = _update_target('yt-dlp stable', ytdlp_current, latest_ytdlp, YTDLP_PYPI_URL)

    targets = {
        'metube_source': metube_target,
        'yt_dlp': ytdlp_target,
        'docker_image': _docker_update_target(),
    }
    return {
        'status': _overall_update_status(targets),
        'checked_at': _utc_now_iso(),
        'targets': targets,
    }


async def get_update_status_payload(metube_current: str, ytdlp_current: str) -> dict:
    now = asyncio.get_running_loop().time()
    cached_payload = _UPDATE_STATUS_CACHE.get('payload')
    if cached_payload is not None and now < _UPDATE_STATUS_CACHE['expires_at']:
        return _add_update_cache_meta(cached_payload, hit=True)

    payload = await build_update_status_payload(metube_current, ytdlp_current)
    _UPDATE_STATUS_CACHE['payload'] = copy.deepcopy(payload)
    _UPDATE_STATUS_CACHE['expires_at'] = now + UPDATE_STATUS_CACHE_TTL_SECONDS
    return _add_update_cache_meta(payload, hit=False)


def failed_update_status_payload(metube_current: str, ytdlp_current: str) -> dict:
    targets = {
        'metube_source': _failed_update_target(
            'MeTube source',
            metube_current,
            METUBE_UPSTREAM_TAGS_URL,
            'Failed to fetch upstream metadata.',
        ),
        'yt_dlp': _failed_update_target(
            'yt-dlp stable',
            ytdlp_current,
            YTDLP_PYPI_URL,
            'Failed to fetch yt-dlp metadata.',
        ),
        'docker_image': _docker_update_target(),
    }
    return _add_update_cache_meta({
        'status': 'check_failed',
        'checked_at': _utc_now_iso(),
        'targets': targets,
    }, hit=False)
