from fastapi import APIRouter, Request, HTTPException
import httpx
from src.config import config

router = APIRouter(prefix="/bff", tags=["Dashboard"])


@router.get(
    "/dashboard",
    summary="Dashboard inicial (BFF)",
    description="Agrega dados do back-end para renderizar o dashboard inicial.",
    responses={
        200: {
            "description": "Dashboard inicial",
            "content": {
                "application/json": {
                    "example": {
                        "consumo_agregado": {"total_kwh": 1234.5, "custo_total": 987.65},
                        "predicoes": None,
                        "alertas": []
                    }
                }
            }
        },
        500: {"description": "Erro interno"},
    },
)
async def get_dashboard(request: Request):
    headers = {"Authorization": request.headers.get("Authorization")}
    base = config.BACKEND_URL.rstrip("/")

    async with httpx.AsyncClient() as client:
        try:
            #Consumo agregado
            consumo_resp = await client.get(f"{base}/reports/monthly", headers=headers)
            if consumo_resp.status_code != 200:
                raise HTTPException(status_code=consumo_resp.status_code, detail="Erro ao obter consumo agregado")
            consumo_data = consumo_resp.json()

            #Predições (opcional)
            pred_resp = await client.get(f"{base}/predictions", headers=headers)
            if pred_resp.status_code in (204, 404):
                pred_data = None
            elif pred_resp.status_code == 200:
                pred_data = pred_resp.json()
            else:
                raise HTTPException(status_code=pred_resp.status_code, detail="Erro ao obter predições")

            #Alertas (opcional)
            alert_resp = await client.get(f"{base}/alerts", headers=headers)
            if alert_resp.status_code in (204, 404):
                alert_data = []
            elif alert_resp.status_code == 200:
                alert_data = alert_resp.json()
            else:
                raise HTTPException(status_code=alert_resp.status_code, detail="Erro ao obter alertas")

        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Erro ao conectar com o back-end: {e}")

    return {
        "consumo_agregado": consumo_data,
        "predicoes": pred_data,
        "alertas": alert_data,
    }
