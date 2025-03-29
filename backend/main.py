from fastapi import FastAPI

from backend.api.v1.router import api_router
from backend.core.config import settings

app = FastAPI(
    version=settings.VERSION,
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Include our router
app.include_router(api_router, prefix=settings.API_V1_STR)
