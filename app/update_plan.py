"""Readonly update plan contract checks."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import update_preflight as update_preflight_checks
import update_status as update_status_checks


BLOCKED = 'blocked'
CHECK_FAILED = 'check_failed'
SOURCE_TARGET = 'source'
ROLLBACK_PLAN_REFERENCE = 'docs/llmwiki/update-rollback-plan.md'
CONTRACT_REFERENCE = 'docs/llmwiki/dry-run-update-contract.md'

REQUIRED_CONFIRMATIONS = [
    'backup_confirmed',
    'rollback_target_recorded',
    'manual_approval',
    'changelog_reviewed',
    'local_only_scope_confirmed',
]

PLANNED_STEPS = [
    'check update status',
    'check update preflight',
    'confirm backup',
    'confirm rollback target',
    'review changelog',
    'request explicit manual approval',
]

DEFAULT_BLOCKED_REASONS = [
    'update apply is not implemented',
    'update prepare is not implemented',
    'manual approval is required',
    'backup confirmation is required',
    'rollback target is not recorded',
]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def _target_statuses(update_status_payload: dict[str, Any]) -> dict[str, str | None]:
    targets = update_status_payload.get('targets', {})
    if not isinstance(targets, dict):
        return {}
    return {
        name: target.get('status')
        for name, target in targets.items()
        if isinstance(target, dict)
    }


def _check_statuses(update_preflight_payload: dict[str, Any]) -> dict[str, str | None]:
    checks = update_preflight_payload.get('checks', {})
    if not isinstance(checks, dict):
        return {}
    return {
        name: check.get('status')
        for name, check in checks.items()
        if isinstance(check, dict)
    }


def _metube_source_target(update_status_payload: dict[str, Any]) -> dict[str, Any]:
    targets = update_status_payload.get('targets', {})
    if not isinstance(targets, dict):
        return {}
    metube_target = targets.get('metube_source', {})
    return metube_target if isinstance(metube_target, dict) else {}


def _update_status_reference(update_status_payload: dict[str, Any]) -> dict:
    return {
        'status': update_status_payload.get('status'),
        'checked_at': update_status_payload.get('checked_at'),
        'target_statuses': _target_statuses(update_status_payload),
    }


def _update_preflight_reference(update_preflight_payload: dict[str, Any]) -> dict:
    return {
        'overall': update_preflight_payload.get('overall'),
        'checked_at': update_preflight_payload.get('checked_at'),
        'can_apply_update': update_preflight_payload.get('can_apply_update'),
        'check_statuses': _check_statuses(update_preflight_payload),
    }


def _blocked_reasons(update_status_payload: dict[str, Any], update_preflight_payload: dict[str, Any]) -> list[str]:
    reasons = list(DEFAULT_BLOCKED_REASONS)
    update_status = update_status_payload.get('status')
    if update_status == CHECK_FAILED:
        reasons.append('update metadata check failed')
    elif update_status == 'development':
        reasons.append('development version requires manual review')
    elif update_status == 'unknown':
        reasons.append('candidate version is unclear')

    preflight_overall = update_preflight_payload.get('overall')
    if preflight_overall == CHECK_FAILED:
        reasons.append('update preflight check failed')
    elif preflight_overall == 'not_ready':
        reasons.append('update preflight is not ready')

    seen = set()
    unique_reasons = []
    for reason in reasons:
        if reason not in seen:
            unique_reasons.append(reason)
            seen.add(reason)
    return unique_reasons


async def build_update_plan_payload(config, download_queue, metube_current: str, ytdlp_current: str) -> dict:
    try:
        update_status_payload = await update_status_checks.get_update_status_payload(metube_current, ytdlp_current)
    except Exception:
        update_status_payload = update_status_checks.failed_update_status_payload(metube_current, ytdlp_current)

    try:
        update_preflight_payload = await update_preflight_checks.build_update_preflight_payload(
            config,
            download_queue,
            metube_current,
            ytdlp_current,
        )
    except Exception:
        update_preflight_payload = update_preflight_checks.failed_update_preflight_payload()

    metube_target = _metube_source_target(update_status_payload)
    return {
        'overall': BLOCKED,
        'checked_at': _utc_now_iso(),
        'target': SOURCE_TARGET,
        'current_version': metube_current,
        'candidate_version': metube_target.get('latest'),
        'source': metube_target.get('source'),
        'required_confirmations': list(REQUIRED_CONFIRMATIONS),
        'blocked_reasons': _blocked_reasons(update_status_payload, update_preflight_payload),
        'planned_steps': list(PLANNED_STEPS),
        'rollback_plan_reference': ROLLBACK_PLAN_REFERENCE,
        'contract_reference': CONTRACT_REFERENCE,
        'update_status_reference': _update_status_reference(update_status_payload),
        'preflight_reference': _update_preflight_reference(update_preflight_payload),
        'can_prepare': False,
        'can_apply': False,
    }


def failed_update_plan_payload(metube_current: str) -> dict:
    return {
        'overall': CHECK_FAILED,
        'checked_at': _utc_now_iso(),
        'target': SOURCE_TARGET,
        'current_version': metube_current,
        'candidate_version': None,
        'source': None,
        'required_confirmations': list(REQUIRED_CONFIRMATIONS),
        'blocked_reasons': [
            'update plan check failed',
            'update apply is not implemented',
            'update prepare is not implemented',
        ],
        'planned_steps': list(PLANNED_STEPS),
        'rollback_plan_reference': ROLLBACK_PLAN_REFERENCE,
        'contract_reference': CONTRACT_REFERENCE,
        'update_status_reference': {'status': CHECK_FAILED},
        'preflight_reference': {'overall': CHECK_FAILED},
        'can_prepare': False,
        'can_apply': False,
    }
