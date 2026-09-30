"""Unit tests for the desktop HTTP client using HTTPX mocks."""

import httpx
import pytest

from task_manager.desktop.api_client import ApiError, TaskApiClient


def test_list_tasks_builds_filters(monkeypatch):
    captured = {}

    def fake_request(method, url, **kwargs):
        captured.update({"method": method, "url": url, **kwargs})
        return httpx.Response(200, json=[], request=httpx.Request(method, url))

    monkeypatch.setattr(httpx, "request", fake_request)
    client = TaskApiClient("http://example.test")
    assert client.list_tasks("todo", "python") == []
    assert captured["params"] == {"status": "todo", "search": "python"}


def test_http_error_becomes_api_error(monkeypatch):
    request = httpx.Request("GET", "http://example.test/api/v1/tasks")

    def fake_request(*args, **kwargs):
        return httpx.Response(500, json={"detail": "Database unavailable"}, request=request)

    monkeypatch.setattr(httpx, "request", fake_request)
    with pytest.raises(ApiError, match="Database unavailable"):
        TaskApiClient("http://example.test").list_tasks()
