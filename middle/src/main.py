from fastapi import FastAPI
from src.routes import auth, health, reports, consumption, dashboard

app = FastAPI(
    title="Middle Service - Energy Management",
    description="Middleware responsável pela autenticação e roteamento entre o front e o back.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(auth.router)
app.include_router(health.router, tags=["health"])
app.include_router(reports.router)
app.include_router(consumption.router)
app.include_router(dashboard.router)