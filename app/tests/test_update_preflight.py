"""Tests for readonly update preflight report."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import update_preflight


class FakeQueuePart:
    def __init__(self, entries=None):
        self.dict = entries or {}

    def items(self):
        return self.dict.items()


class FakeDownloadQueue:
    def __init__(self, queue=None, pending=None, active_downloads=None):
        self.queue = FakeQueuePart(queue)
        self.pending = FakeQueuePart(pending)
        self.active_downloads = active_downloads or set()


@pytest.fixture
def fake_config(tmp_path):
    base_dir = tmp_path / "repo"
    state_dir = tmp_path / "state"
    download_dir = tmp_path / "downloads"
    temp_dir = tmp_path / "temp"
    for path in (base_dir, state_dir, download_dir, temp_dir):
        path.mkdir(parents=True)
    git_dir = base_dir / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("ref: refs/heads/master\n", encoding="utf-8")
    return SimpleNamespace(
        BASE_DIR=str(base_dir),
        STATE_DIR=str(state_dir),
        DOWNLOAD_DIR=str(download_dir),
        AUDIO_DOWNLOAD_DIR=str(download_dir),
        TEMP_DIR=str(temp_dir),
    )


@pytest.mark.asyncio
async def test_preflight_report_is_readonly_and_not_apply_ready(monkeypatch, fake_config):
    async def fake_update_status(_metube_current, _ytdlp_current):
        return {"status": "latest", "checked_at": "2026-06-08T00:00:00Z"}

    monkeypatch.setattr(
        update_preflight.update_status_checks,
        "get_update_status_payload",
        fake_update_status,
    )

    body = await update_preflight.build_update_preflight_payload(
        fake_config,
        FakeDownloadQueue(),
        "2026.06.06",
        "2026.3.17",
    )

    assert body["overall"] == "not_ready"
    assert body["can_apply_update"] is False
    assert body["checks"]["source"]["status"] == "manual_required"
    assert body["checks"]["source"]["details"]["current_branch"] == "master"
    assert body["checks"]["source"]["details"]["git_commands_run"] is False
    assert body["checks"]["backup"]["status"] == "manual_required"
    assert body["checks"]["docker"]["status"] == "not_checked"
    assert body["checks"]["docker"]["details"]["docker_commands_run"] is False
    assert body["checks"]["state"]["status"] == "manual_required"
    assert body["checks"]["queue"]["status"] == "ready"
    assert body["checks"]["update_status"]["status"] == "ready"


@pytest.mark.asyncio
async def test_preflight_queue_not_ready_when_jobs_exist(monkeypatch, fake_config):
    async def fake_update_status(_metube_current, _ytdlp_current):
        return {"status": "latest", "checked_at": "2026-06-08T00:00:00Z"}

    monkeypatch.setattr(
        update_preflight.update_status_checks,
        "get_update_status_payload",
        fake_update_status,
    )
    queued = {
        "private-url": SimpleNamespace(info=SimpleNamespace(status="pending")),
    }

    body = await update_preflight.build_update_preflight_payload(
        fake_config,
        FakeDownloadQueue(queue=queued),
        "2026.06.06",
        "2026.3.17",
    )

    text = str(body)
    assert body["checks"]["queue"]["status"] == "not_ready"
    assert body["checks"]["queue"]["details"]["queued_count"] == 1
    assert "private-url" not in text


@pytest.mark.asyncio
async def test_preflight_metadata_failure_does_not_leak_exception_text(monkeypatch, fake_config):
    async def fake_update_status(_metube_current, _ytdlp_current):
        raise RuntimeError("private-auth-material-should-not-leak")

    monkeypatch.setattr(
        update_preflight.update_status_checks,
        "get_update_status_payload",
        fake_update_status,
    )

    body = await update_preflight.build_update_preflight_payload(
        fake_config,
        FakeDownloadQueue(),
        "2026.06.06",
        "2026.3.17",
    )

    text = str(body)
    assert body["checks"]["update_status"]["status"] == "check_failed"
    assert "private-auth-material" not in text


@pytest.mark.asyncio
async def test_preflight_development_status_requires_manual_review(monkeypatch, fake_config):
    async def fake_update_status(_metube_current, _ytdlp_current):
        return {"status": "development", "checked_at": "2026-06-08T00:00:00Z"}

    monkeypatch.setattr(
        update_preflight.update_status_checks,
        "get_update_status_payload",
        fake_update_status,
    )

    body = await update_preflight.build_update_preflight_payload(
        fake_config,
        FakeDownloadQueue(),
        "dev",
        "2026.3.17",
    )

    assert body["checks"]["update_status"]["status"] == "manual_required"
    assert body["can_apply_update"] is False


@pytest.mark.asyncio
async def test_preflight_stops_on_local_only_docker_profile_branch(monkeypatch, fake_config):
    async def fake_update_status(_metube_current, _ytdlp_current):
        return {"status": "latest", "checked_at": "2026-06-08T00:00:00Z"}

    monkeypatch.setattr(
        update_preflight.update_status_checks,
        "get_update_status_payload",
        fake_update_status,
    )
    git_head = fake_config.BASE_DIR + "/.git/HEAD"
    with open(git_head, "w", encoding="utf-8") as head_file:
        head_file.write("ref: refs/heads/local-only-docker-profile\n")

    body = await update_preflight.build_update_preflight_payload(
        fake_config,
        FakeDownloadQueue(),
        "2026.06.06",
        "2026.3.17",
    )

    assert body["checks"]["source"]["status"] == "check_failed"
    assert body["checks"]["source"]["details"]["current_branch"] == "local-only-docker-profile"
