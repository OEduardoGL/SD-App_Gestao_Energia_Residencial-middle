import json
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.mark.asyncio
async def test_reports_monthly_pass_through_query_and_headers(monkeypatch):
    called = {}

    class _FakeUpstream:
        def __init__(self, content: bytes, headers: dict, status_code: int = 200):
            self._content = content
            self.headers = headers
            self.status_code = status_code

        @property
        def content(self):
            return self._content

    class _FakeAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url: str, headers: dict | None = None, **kwargs):
            called["url"] = url
            called["headers"] = headers or {}
            body = {"items": [], "meta": {"page": 1, "per_page": 20, "total": 42}}
            upstream_headers = {
                "Content-Type": "application/json",
                "Link": '<https://api.example.com/reports/monthly?page=2>; rel="next"',
                "X-Total-Count": "42",
            }
            return _FakeUpstream(json.dumps(body).encode(), upstream_headers, 200)

    # Patch only in reports module
    monkeypatch.setattr("src.routes.reports.httpx.AsyncClient", _FakeAsyncClient)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get(
            "/reports/monthly?start=2025-01-01&end=2025-01-31",
            headers={"Authorization": "Bearer abc", "Accept": "application/json"},
        )

    # Asserts about the upstream call (query and headers forwarded)
    assert "start=2025-01-01" in called["url"] and "end=2025-01-31" in called["url"]
    assert called["headers"].get("Authorization") == "Bearer abc"

    # Asserts about the downstream response (status/body/headers propagated)
    assert resp.status_code == 200
    assert resp.json()["meta"]["total"] == 42
    assert resp.headers.get("Link") is not None
    assert resp.headers.get("X-Total-Count") == "42"


@pytest.mark.asyncio
async def test_reports_weekly_pass_through(monkeypatch):
    class _FakeUpstream:
        def __init__(self, content: bytes, headers: dict, status_code: int = 200):
            self._content = content
            self.headers = headers
            self.status_code = status_code

        @property
        def content(self):
            return self._content

    class _FakeAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url: str, headers: dict | None = None, **kwargs):
            body = {
                "items": [
                    {"week_start": "2025-01-06", "week_end": "2025-01-12", "consumption_kwh": 55.2, "cost": 44.1}
                ]
            }
            upstream_headers = {"Content-Type": "application/json"}
            return _FakeUpstream(json.dumps(body).encode(), upstream_headers, 200)

    monkeypatch.setattr("src.routes.reports.httpx.AsyncClient", _FakeAsyncClient)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/reports/weekly?start=2025-01-06&end=2025-01-12")

    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["week_start"] == "2025-01-06"

