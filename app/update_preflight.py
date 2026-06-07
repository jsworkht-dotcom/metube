"""Readonly update readiness preflight checks."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import update_status as update_status_checks


READY = 'ready'
NOT_READY = 'not_ready'
MANUAL_REQUIRED = 'manual_required'
NOT_CHECKED = 'not_checked'
CHECK_FAILED = 'check_failed'

_BLOCKING_STATUSES = {NOT_READY, MANUAL_REQUIRED, NOT_CHECKED, CHECK_FAILED}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def _check(status: str, message: str, details: dict[str, Any] | None = None) -> dict:
    result = {
        'status': status,
        'message': message,
    }
    if details:
        result['details'] = details
    return result


def _read_current_branch(base_dir: str | None) -> str | None:
    git_head = Path(base_dir or os.getcwd()) / '.git' / 'HEAD'
    try:
        content = git_head.read_text(encoding='utf-8').strip()
    except OSError:
        return None
    if content.startswith('ref: refs/heads/'):
        return content.removeprefix('ref: refs/heads/')
    if content:
        return 'detached'
    return None


def _source_check(base_dir: str | None) -> dict:
    current_branch = _read_current_branch(base_dir)
    details = {
        'current_branch': current_branch,
        'worktree_clean_checked': False,
        'tracking_checked': False,
        'git_commands_run': False,
    }
    if current_branch == 'local-only-docker-profile':
        return _check(
            CHECK_FAILED,
            'Upstream PR #1001 local-only Docker branch is active; stop before update preflight.',
            details,
        )
    return _check(
        MANUAL_REQUIRED,
        'Source worktree cleanliness, fork/master tracking, and rollback target must be confirmed manually.',
        details,
    )


def _backup_check() -> dict:
    return _check(
        MANUAL_REQUIRED,
        'Backup branch/tag and rollback target are not confirmed by this readonly report.',
        {
            'backup_created': False,
            'rollback_target_recorded': False,
            'backup_created_by_preflight': False,
        },
    )


def _docker_check() -> dict:
    return _check(
        NOT_CHECKED,
        'Docker image tag/digest check is not implemented; no Docker commands are run.',
        {
            'image_digest_checked': False,
            'docker_commands_run': False,
        },
    )


def _state_check(config) -> dict:
    state_dir = getattr(config, 'STATE_DIR', '')
    download_dir = getattr(config, 'DOWNLOAD_DIR', '')
    audio_download_dir = getattr(config, 'AUDIO_DOWNLOAD_DIR', '')
    temp_dir = getattr(config, 'TEMP_DIR', '')
    details = {
        'state_dir_configured': bool(state_dir),
        'state_dir_exists': bool(state_dir and os.path.isdir(state_dir)),
        'download_dir_configured': bool(download_dir),
        'download_dir_exists': bool(download_dir and os.path.isdir(download_dir)),
        'audio_download_dir_configured': bool(audio_download_dir),
        'audio_download_dir_exists': bool(audio_download_dir and os.path.isdir(audio_download_dir)),
        'temp_dir_configured': bool(temp_dir),
        'temp_dir_exists': bool(temp_dir and os.path.isdir(temp_dir)),
        'state_backup_confirmed': False,
        'download_backup_decision_recorded': False,
    }
    missing = [
        key
        for key in ('state_dir_exists', 'download_dir_exists', 'audio_download_dir_exists', 'temp_dir_exists')
        if not details[key]
    ]
    if missing:
        details['missing'] = missing
        return _check(
            CHECK_FAILED,
            'Configured state/download directories must exist before update preflight can continue.',
            details,
        )
    return _check(
        MANUAL_REQUIRED,
        'STATE_DIR backup and download backup decision must be confirmed manually.',
        details,
    )


def _queue_items(queue_obj) -> list:
    items = getattr(queue_obj, 'items', None)
    if callable(items):
        return list(items())
    data = getattr(queue_obj, 'dict', {})
    if hasattr(data, 'items'):
        return list(data.items())
    return []


def _queue_statuses(queue_obj) -> list[str | None]:
    statuses = []
    for _, download in _queue_items(queue_obj):
        info = getattr(download, 'info', download)
        statuses.append(getattr(info, 'status', None))
    return statuses


def _queue_check(download_queue) -> dict:
    queue_entries = _queue_items(getattr(download_queue, 'queue', None))
    pending_entries = _queue_items(getattr(download_queue, 'pending', None))
    active_downloads = getattr(download_queue, 'active_downloads', set()) or set()
    running_statuses = {'preparing', 'downloading'}
    running_count = len(active_downloads) + sum(
        1
        for status in _queue_statuses(getattr(download_queue, 'queue', None))
        if status in running_statuses
    )
    details = {
        'running_count': running_count,
        'queued_count': len(queue_entries),
        'pending_count': len(pending_entries),
    }
    if running_count or queue_entries or pending_entries:
        return _check(
            NOT_READY,
            'Running, queued, or pending downloads exist; stop before update apply.',
            details,
        )
    return _check(READY, 'No running, queued, or pending downloads detected.', details)


async def _update_status_check(metube_current: str, ytdlp_current: str) -> dict:
    try:
        payload = await update_status_checks.get_update_status_payload(metube_current, ytdlp_current)
    except Exception:
        return _check(CHECK_FAILED, 'Update metadata check failed; stop before update apply.')
    status = payload.get('status')
    details = {
        'update_status': status,
        'checked_at': payload.get('checked_at'),
    }
    if status == CHECK_FAILED:
        return _check(CHECK_FAILED, 'Update metadata check failed; stop before update apply.', details)
    if status == 'development':
        return _check(
            MANUAL_REQUIRED,
            'Development build cannot be compared with release metadata; manual version review is required.',
            details,
        )
    return _check(READY, 'Update metadata is available.', details)


def _collect_reasons(checks: dict[str, dict]) -> list[str]:
    reasons = []
    for name, check in checks.items():
        if check.get('status') in _BLOCKING_STATUSES:
            reasons.append(f"{name}: {check.get('message', 'manual review required')}")
    if not reasons:
        reasons.append('manual approval is still required before any update apply')
    return reasons


async def build_update_preflight_payload(config, download_queue, metube_current: str, ytdlp_current: str) -> dict:
    checks = {
        'source': _source_check(getattr(config, 'BASE_DIR', '') or os.getcwd()),
        'backup': _backup_check(),
        'docker': _docker_check(),
        'state': _state_check(config),
        'queue': _queue_check(download_queue),
        'update_status': await _update_status_check(metube_current, ytdlp_current),
    }
    reasons = _collect_reasons(checks)
    return {
        'overall': NOT_READY if reasons else READY,
        'checked_at': _utc_now_iso(),
        'checks': checks,
        'can_apply_update': False,
        'reasons': reasons,
    }


def failed_update_preflight_payload() -> dict:
    checks = {
        'preflight': _check(
            CHECK_FAILED,
            'Readonly update preflight check failed unexpectedly.',
        ),
    }
    return {
        'overall': NOT_READY,
        'checked_at': _utc_now_iso(),
        'checks': checks,
        'can_apply_update': False,
        'reasons': _collect_reasons(checks),
    }
