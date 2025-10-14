from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response
import httpx
from src.config import config


router = APIRouter(prefix="/reports", tags=["Reports"])


def _filtered_headers_for_response(source_headers: httpx.Headers) -> dict:
    """Return headers to propagate back to the client, excluding hop-by-hop ones.

    We forward Content-Type, Link and any X-* pagination headers to preserve pagination.
    """
    hop_by_hop = {
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailer",
        "transfer-encoding",
        "upgrade",
        "content-encoding",
        "content-length",
    }

    headers: dict[str, str] = {}
    for k, v in source_headers.items():
        kl = k.lower()
        if kl in hop_by_hop:
            continue
        # Always keep Content-Type so clients parse the body properly
        if kl == "content-type":
            headers[k] = v
            continue
        # Forward pagination-related headers (Link and common X-* variants)
        if kl == "link" or kl.startswith("x-"):
            headers[k] = v
            continue
    return headers


def _auth_headers_from_request(request: Request) -> dict:
    token = request.headers.get("authorization")
    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = token
    # Also forward Accept if provided, to preserve content negotiation
    accept = request.headers.get("accept")
    if accept:
        headers["Accept"] = accept
    return headers


async def _proxy_get(path: str, request: Request) -> Response:
    base = config.BACKEND_URL.rstrip("/")
    url = f"{base}{path}"
    if request.url.query:
        url = f"{url}?{request.url.query}"

    async with httpx.AsyncClient() as client:
        try:
            upstream = await client.get(url, headers=_auth_headers_from_request(request))
        except httpx.RequestError as e:
            # Bad Gateway when upstream is unreachable
            raise HTTPException(status_code=502, detail=f"Erro ao conectar com o back-end: {e}")

    # Build raw Response without transforming payload
    headers = _filtered_headers_for_response(upstream.headers)
    return Response(content=upstream.content, status_code=upstream.status_code, headers=headers)


@router.get(
    "/monthly",
    summary="Relatórios mensais (pass-through)",
    description=(
        "Encaminha a requisição para o backend em /reports/monthly sem transformação de payload.\n"
        "Aceita query params e repassa idênticos (ex.: ?start=YYYY-MM-DD&end=YYYY-MM-DD).\n"
        "Se o backend devolver paginação (headers Link ou campos JSON), são repassados sem alterações."
    ),
    responses={
        200: {
            "description": "Resposta do backend repassada sem alterações",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {"month": "2024-09", "consumption_kwh": 312.4, "cost": 245.90}
                        ],
                        "meta": {"page": 1, "per_page": 20, "total": 42},
                    }
                }
            },
        }
    },
)
async def get_monthly_reports(request: Request):
    return await _proxy_get("/reports/monthly", request)


@router.get(
    "/weekly",
    summary="Relatórios semanais (pass-through)",
    description=(
        "Encaminha a requisição para o backend em /reports/weekly sem transformação de payload.\n"
        "Aceita query params e repassa idênticos (ex.: ?start=YYYY-MM-DD&end=YYYY-MM-DD).\n"
        "Se o backend devolver paginação (headers Link ou campos JSON), são repassados sem alterações."
    ),
    responses={
        200: {
            "description": "Resposta do backend repassada sem alterações",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "week_start": "2024-09-02",
                                "week_end": "2024-09-08",
                                "consumption_kwh": 78.1,
                                "cost": 61.35,
                            }
                        ],
                        "meta": {"page": 1, "per_page": 20, "total": 10},
                    }
                }
            },
        }
    },
)
async def get_weekly_reports(request: Request):
    return await _proxy_get("/reports/weekly", request)

