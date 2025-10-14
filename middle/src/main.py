from fastapi import FastAPI
from src.routes import auth, health

app = FastAPI(
    title="Middle Service - Energy Management",
    description="Middleware responsável pela autenticação e roteamento entre o front e o back.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(health.router, tags=["health"])