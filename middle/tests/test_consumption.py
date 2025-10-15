# tests/routes/test_consumption.py
import io
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app

@pytest.mark.asyncio
async def test_consumption_upload_pass_through(monkeypatch):
    called = {}

    class _FakeUpstream:
        def __init__(self, content: bytes, status_code: int = 200):
            self._content = content
            self.status_code = status_code

        @property
        def content(self):
            return self._content

        def json(self):
            return {"success": True, "message": "Arquivo processado com sucesso"}

        @property
        def is_error(self):
            return self.status_code >= 400
        
    class _FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def post(self, url: str, headers: dict | None = None, files: dict | None = None, **kwargs):
            called["url"] = url
            called["headers"] = headers or {}
            called["files"] = files
            return _FakeUpstream(b'{"success": true}')


    monkeypatch.setattr("src.routes.consumption.httpx.AsyncClient", _FakeAsyncClient)

    # Cria um arquivo CSV fake em memória
    fake_file = io.BytesIO(b"col1,col2\n1,2\n3,4")
    fake_file.name = "teste.csv"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/consumption/upload",
            headers={
                "Authorization": "Bearer abc",
                "Accept": "application/json",
            },
            files={"file": (fake_file.name, fake_file, "text/csv")},
        )

    # Verifica se foi chamado com as informações certas
    assert "consumption/upload" in called["url"]
    assert called["headers"].get("Authorization") == "Bearer abc"
    assert called["files"]["file"][0] == "teste.csv"

    # Verifica resposta
    assert resp.status_code == 200
    assert resp.json()["success"] is True


@pytest.mark.asyncio
async def test_consumption_upload_invalid_file_type(monkeypatch):
    transport = ASGITransport(app=app)
    fake_file = io.BytesIO(b"isso nao eh csv")
    fake_file.name = "teste.txt"

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/consumption/upload",
            headers={"Authorization": "Bearer abc"},
            files={"file": (fake_file.name, fake_file, "text/plain")},
        )

    assert resp.status_code == 400
    assert "inválido" in resp.json()["detail"]
