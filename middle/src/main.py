from fastapi import FastAPI
from src.routes import auth, health, reports, consumption

app = FastAPI(title="Middle Service - Energy Management")

app.include_router(auth.router)
app.include_router(health.router, tags=["health"])
app.include_router(reports.router)
app.include_router(consumption.router)