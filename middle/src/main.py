from fastapi import FastAPI
from src.routes import auth, health

app = FastAPI(title="Middle Service - Energy Management")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(health.router, tags=["health"])