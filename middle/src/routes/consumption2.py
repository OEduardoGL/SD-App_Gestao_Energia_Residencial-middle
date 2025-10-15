# src/routes/consumption.py

from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from fastapi.responses import Response
import httpx
from src.config import config

router = APIRouter(prefix="/consumption", tags=["Consumption"])


def _auth_headers_from_request(request: Request) -> dict:
    token = request.headers.get("authorization")
    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = token
    accept = request.headers.get("accept")
    if accept:
        headers["Accept"] = accept
    return headers


@router.post(
    "/upload",
    summary="Upload de CSV de consumo (pass-through)",
    description=(
        "Recebe um arquivo CSV e encaminha a requisição para o backend em "
        "`/consumption/upload` com o mesmo token de autenticação. "
        "Não altera payload nem resposta do backend."
    ),
    responses={
        200: {
            "description": "Resposta do backend repassada sem alterações",
            "content": {"application/json": {"example": {"message": "Arquivo recebido com sucesso"}}},
        },
        400: {"description": "Arquivo inválido"},
    },
)
async def upload_consumption_file(request: Request, file: UploadFile = File(...)):
    # validar tipo
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido. Use CSV.")

    # validar tamanho
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Arquivo excede 5MB.")

    base = config.BACKEND_URL.rstrip("/")
    url = f"{base}/consumption/upload"

    # repassar para o backend
    async with httpx.AsyncClient() as client:
        try:
            upstream = await client.post(
                url,
                headers=_auth_headers_from_request(request),
                files={"file": (file.filename, contents, file.content_type)},
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Erro ao conectar com o back-end: {e}")

    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers=_filtered_headers_for_response(upstream.headers),
        media_type=upstream.headers.get("content-type")
    )


def _filtered_headers_for_response(source_headers: httpx.Headers) -> dict:
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
        if kl == "content-type":
            headers[k] = v
            continue
        if kl == "link" or kl.startswith("x-"):
            headers[k] = v
            continue
    return headers
