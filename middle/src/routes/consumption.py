# src/routes/consumption.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Request
import httpx
from src.config import config

router = APIRouter()

def _auth_headers_from_request(request: Request) -> dict:
    token = request.headers.get("authorization")
    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = token
    accept = request.headers.get("accept")
    if accept:
        headers["Accept"] = accept
    return headers

@router.post("/consumption/upload")
async def upload_consumption_file(request: Request, file: UploadFile = File(...)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido. Use CSV.")
    
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Arquivo excede 5MB.")
    
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Token não informado.")

    async with httpx.AsyncClient(timeout=30.0) as client:
        base = config.BACKEND_URL.rstrip("/")
        url = f"{base}/consumption/upload"

        response = await client.post(
            url,
            headers=_auth_headers_from_request(request),
            files={'file': (file.filename, contents, file.content_type)}
        )

    if response.is_error:
        raise HTTPException(
            status_code=response.status_code,
            detail={
                "error": True,
                "details": response.json() if response.content else "Erro no backend"
            }
        )

    return response.json()
