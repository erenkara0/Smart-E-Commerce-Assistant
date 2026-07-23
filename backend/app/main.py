from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import chat, health, products, root
from app.core.config import settings
from app.core.exception_handlers import (
    http_exception_handler,
    internal_server_error_handler,
    validation_exception_handler,
)

app = FastAPI(
    title="MikroAsistan API",
    description="MikroAsistan projesi için backend API servisleri.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.get("/scalar", include_in_schema=False)
def scalar_api_reference():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="MikroAsistan API Documentation",
    )


app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, internal_server_error_handler)

app.include_router(root.router)
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(products.router)