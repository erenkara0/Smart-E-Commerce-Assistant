from fastapi import FastAPI

from app.api.routes import root
from app.api.routes import health

app = FastAPI(
    title="MikroAsistan API",
    description="MikroAsistan projesi için backend API servisleri.",
    version="0.1.0",
)

app.include_router(root.router)
app.include_router(health.router)