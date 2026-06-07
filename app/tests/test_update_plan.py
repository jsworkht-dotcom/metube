"""Tests for readonly update plan contract."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import update_plan


class FakeDownloadQueue:
    pass


@pytest.fixture
def fake_config():
    return SimpleNamespace(BASE_DIR="")


@pytest.mark.asyncio
async def test_update_plan_is_blocked_by_default(monkeypatch, fake_config):
    async def fake_update_status(_metube_current, _ytdlp_current):
        return {
            "status": "update_available",
            "checked_at": "2026-06-08T00:00:00Z",
            "targets": {
                "metube_source": {
                    "status": "update_available",
                    "latest": "2026.06.06",
                    "source": "https://api.github.com/repos/alexta69/metube/tags?per_page=1",
                },
                "yt_dlp": {"status": "latest"},
                "docker_image": {"status": "not_checked"},
            },
        }

    async def fake_update_preflight(_config, _download_queue, _metube_current, _ytdlp_current):
        return {
            "overall": "not_ready",
            "checked_at": "2026-06-08T00:00:01Z",
            "checks": {
                "source": {"status": "manual_required"},
                "backup": {"status": "manual_required"},
                "queue": {"status": "ready"},
            },
            "can_apply_update": False,
        }

    monkeypatch.setattr(
        update_plan.update_status_checks,
        "get_update_status_payload",
        fake_update_status,
    )
    monkeypatch.setattr(
        update_plan.update_preflight_checks,
        "build_update_preflight_payload",
        fake_update_preflight,
    )

    body = await update_plan.build_update_plan_payload(
        fake_config,
        FakeDownloadQueue(),
        "2026.05.30",
        "2026.3.17",
    )

    assert body["overall"] == "blocked"
    assert body["target"] == "source"
    assert body["current_version"] == "2026.05.30"
    assert body["candidate_version"] == "2026.06.06"
    assert body["can_prepare"] is False
    assert body["can_apply"] is False
    assert "backup_confirmed" in body["required_confirmations"]
    assert "rollback_target_recorded" in body["required_confirmations"]
    assert "manual_approval" in body["required_confirmations"]
    assert "check update status" in body["planned_steps"]
    assert "check update preflight" in body["planned_steps"]
    assert body["rollback_plan_reference"] == "docs/llmwiki/update-rollback-plan.md"
    assert body["contract_reference"] == "docs/llmwiki/dry-run-update-contract.md"
    assert "update apply is not implemented" in body["blocked_reasons"]
    assert "update prepare is not implemented" in body["blocked_reasons"]
    assert "manual approval is required" in body["blocked_reasons"]
    assert body["update_status_reference"]["status"] == "update_available"
    assert body["update_status_reference"]["target_statuses"]["metube_source"] == "update_available"
    assert body["preflight_reference"]["overall"] == "not_ready"
    assert body["preflight_reference"]["check_statuses"]["backup"] == "manual_required"


@pytest.mark.asyncio
async def test_update_plan_development_version_requires_manual_review(monkeypatch, fake_config):
    async def fake_update_status(_metube_current, _ytdlp_current):
        return {
            "status": "development",
            "checked_at": "2026-06-08T00:00:00Z",
            "targets": {
                "metube_source": {
                    "status": "development",
                    "latest": "2026.06.06",
                    "source": "https://api.github.com/repos/alexta69/metube/tags?per_page=1",
                },
            },
        }

    async def fake_update_preflight(_config, _download_queue, _metube_current, _ytdlp_current):
        return {
            "overall": "not_ready",
            "checked_at": "2026-06-08T00:00:01Z",
            "checks": {"update_status": {"status": "manual_required"}},
            "can_apply_update": False,
        }

    monkeypatch.setattr(
        update_plan.update_status_checks,
        "get_update_status_payload",
        fake_update_status,
    )
    monkeypatch.setattr(
        update_plan.update_preflight_checks,
        "build_update_preflight_payload",
        fake_update_preflight,
    )

    body = await update_plan.build_update_plan_payload(fake_config, FakeDownloadQueue(), "dev", "2026.3.17")

    assert body["overall"] == "blocked"
    assert body["current_version"] == "dev"
    assert body["can_prepare"] is False
    assert body["can_apply"] is False
    assert "development version requires manual review" in body["blocked_reasons"]


@pytest.mark.asyncio
async def test_update_plan_failures_do_not_leak_exception_text(monkeypatch, fake_config):
    async def fake_update_status(_metube_current, _ytdlp_current):
        raise RuntimeError("private-auth-material-should-not-leak")

    async def fake_update_preflight(_config, _download_queue, _metube_current, _ytdlp_current):
        raise RuntimeError("private-queue-url-should-not-leak")

    monkeypatch.setattr(
        update_plan.update_status_checks,
        "get_update_status_payload",
        fake_update_status,
    )
    monkeypatch.setattr(
        update_plan.update_preflight_checks,
        "build_update_preflight_payload",
        fake_update_preflight,
    )

    body = await update_plan.build_update_plan_payload(
        fake_config,
        FakeDownloadQueue(),
        "2026.05.30",
        "2026.3.17",
    )

    text = str(body)
    assert body["overall"] == "blocked"
    assert body["can_prepare"] is False
    assert body["can_apply"] is False
    assert body["update_status_reference"]["status"] == "check_failed"
    assert body["preflight_reference"]["overall"] == "not_ready"
    assert "private-auth-material" not in text
    assert "private-queue-url" not in text


def test_failed_update_plan_payload_is_sanitized():
    body = update_plan.failed_update_plan_payload("dev")

    assert body["overall"] == "check_failed"
    assert body["current_version"] == "dev"
    assert body["candidate_version"] is None
    assert body["can_prepare"] is False
    assert body["can_apply"] is False
    assert body["update_status_reference"]["status"] == "check_failed"
    assert body["preflight_reference"]["overall"] == "check_failed"
