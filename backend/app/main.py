from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.api.routes import root,health,chat

app = FastAPI(
    title="MikroAsistan API",
    description="MikroAsistan projesi için backend API servisleri.",
    version="0.1.0",
)


@app.get("/scalar", include_in_schema=False)
def scalar_api_reference():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="MikroAsistan API Documentation",
    )


app.include_router(root.router)
app.include_router(health.router)
app.include_router(chat.router)