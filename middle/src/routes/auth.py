from fastapi import APIRouter, HTTPException
import httpx
from src.config import config

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(credentials: dict):
    """
    Proxy /auth/login -> encaminha credenciais para o back-end e retorna o token.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{config.BACKEND_URL}/auth/login", json=credentials)
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Erro ao conectar com o back-end: {e}")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
