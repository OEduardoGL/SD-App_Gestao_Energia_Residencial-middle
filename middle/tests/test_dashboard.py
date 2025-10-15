import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.mark.asyncio
async def test_dashboard_success(monkeypatch):
    """Testa o endpoint /bff/dashboard agregando dados de múltiplos serviços."""

    # Simula respostas do backend
    async def fake_get(url, headers=None, **kwargs):
        if url.endswith("/reports/monthly"):
            return _FakeResponse(200, {"total_kwh": 123.4, "custo_total": 99.9})
        elif url.endswith("/predictions"):
            return _FakeResponse(200, {"forecast": [1, 2, 3]})
        elif url.endswith("/alerts"):
            return _FakeResponse(200, [{"id": 1, "msg": "Alerta crítico"}])
        else:
            return _FakeResponse(404, {})

    # FakeResponse simples para simular o retorno do httpx
    class _FakeResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json = json_data

        def json(self):
            return self._json

    class _FakeAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, headers=None, **kwargs):
            return await fake_get(url, headers, **kwargs)

    # Faz o monkeypatch para substituir o httpx.AsyncClient no dashboard
    monkeypatch.setattr("src.routes.dashboard.httpx.AsyncClient", _FakeAsyncClient)

    # Testa a rota real
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/bff/dashboard", headers={"Authorization": "Bearer abc"})

    assert resp.status_code == 200
    data = resp.json()
    assert "consumo_agregado" in data
    assert "predicoes" in data
    assert "alertas" in data
    assert data["predicoes"]["forecast"] == [1, 2, 3]
    assert data["alertas"][0]["msg"] == "Alerta crítico"
