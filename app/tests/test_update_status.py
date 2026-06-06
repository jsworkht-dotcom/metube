"""Tests for readonly update status checks."""

from __future__ import annotations

import pytest

import update_status


@pytest.fixture(autouse=True)
def reset_update_status_cache():
    update_status._UPDATE_STATUS_CACHE["expires_at"] = 0.0
    update_status._UPDATE_STATUS_CACHE["payload"] = None
    yield
    update_status._UPDATE_STATUS_CACHE["expires_at"] = 0.0
    update_status._UPDATE_STATUS_CACHE["payload"] = None


@pytest.mark.asyncio
async def test_update_status_latest(monkeypatch):
    async def fake_fetch(_session, url):
        if url == update_status.METUBE_UPSTREAM_TAGS_URL:
            return [{"name": "2026.06.06"}]
        if url == update_status.YTDLP_PYPI_URL:
            return {"info": {"version": "2026.3.17"}}
        raise AssertionError(f"unexpected url: {url}")

    monkeypatch.setattr(update_status, "fetch_update_json", fake_fetch)

    body = await update_status.get_update_status_payload("2026.06.06", "2026.3.17")
    assert body["status"] == "latest"
    assert body["cache"]["hit"] is False
    assert body["targets"]["metube_source"]["status"] == "latest"
    assert body["targets"]["yt_dlp"]["status"] == "latest"
    assert body["targets"]["docker_image"]["status"] == "not_checked"


@pytest.mark.asyncio
async def test_update_status_update_available(monkeypatch):
    async def fake_fetch(_session, url):
        if url == update_status.METUBE_UPSTREAM_TAGS_URL:
            return [{"name": "2026.06.06"}]
        if url == update_status.YTDLP_PYPI_URL:
            return {"info": {"version": "2026.5.22"}}
        raise AssertionError(f"unexpected url: {url}")

    monkeypatch.setattr(update_status, "fetch_update_json", fake_fetch)

    body = await update_status.get_update_status_payload("2026.05.30", "2026.3.17")
    assert body["status"] == "update_available"
    assert body["targets"]["metube_source"]["status"] == "update_available"
    assert body["targets"]["yt_dlp"]["status"] == "update_available"


@pytest.mark.asyncio
async def test_update_status_check_failed_does_not_leak_exception_text(monkeypatch):
    async def fake_fetch(_session, _url):
        raise RuntimeError("token=secret cookie=private")

    monkeypatch.setattr(update_status, "fetch_update_json", fake_fetch)

    body = await update_status.get_update_status_payload("2026.06.06", "2026.3.17")
    text = str(body)
    assert body["status"] == "check_failed"
    assert body["targets"]["metube_source"]["status"] == "check_failed"
    assert body["targets"]["yt_dlp"]["status"] == "check_failed"
    assert "secret" not in text
    assert "token" not in text
    assert "cookie" not in text


@pytest.mark.asyncio
async def test_update_status_uses_short_cache(monkeypatch):
    calls = []

    async def fake_fetch(_session, url):
        calls.append(url)
        if url == update_status.METUBE_UPSTREAM_TAGS_URL:
            return [{"name": "2026.06.06"}]
        if url == update_status.YTDLP_PYPI_URL:
            return {"info": {"version": "2026.3.17"}}
        raise AssertionError(f"unexpected url: {url}")

    monkeypatch.setattr(update_status, "fetch_update_json", fake_fetch)

    first = await update_status.get_update_status_payload("2026.06.06", "2026.3.17")
    second = await update_status.get_update_status_payload("2026.06.06", "2026.3.17")
    assert first["cache"]["hit"] is False
    assert second["cache"]["hit"] is True
    assert calls.count(update_status.METUBE_UPSTREAM_TAGS_URL) == 1
    assert calls.count(update_status.YTDLP_PYPI_URL) == 1
