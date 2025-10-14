import json
import os
import pytest
import httpx

# Ensure required env var exists before importing the app/config
os.environ.setdefault("BACKEND_URL", "http://backend.test")


class _FakeResponse:
    def __init__(self, status_code: int, json_data: dict | None = None, content: bytes | None = None, headers: dict | None = None, text: str | None = None):
        self.status_code = status_code
        self._json = json_data
        self._content = content or (json.dumps(json_data).encode() if json_data is not None else b"")
        self.headers = httpx.Headers(headers or {})
        self.text = text if text is not None else self._content.decode() if self._content else ""

    @property
    def content(self) -> bytes:
        return self._content

    def json(self):
        return self._json


@pytest.fixture(autouse=True)
def _patch_auth_backend(monkeypatch):
    """Patch only the auth upstream calls so existing auth test passes without a real backend."""


    class _FakeAuthAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def post(self, url: str, json: dict | None = None, **kwargs):
            # Simulate successful authentication
            return _FakeResponse(200, json_data={"access_token": "test-token"})

    # Patch only inside the auth router module, not global httpx.AsyncClient
    monkeypatch.setattr("src.routes.auth.httpx.AsyncClient", _FakeAuthAsyncClient)
