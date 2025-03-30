from fastapi import FastAPI
from loguru import logger

from backend.api.v1.router import api_router
from backend.core.config import settings
from backend.utils.redis import setup_redis_client

app = FastAPI(
    version=settings.VERSION,
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)


@app.on_event("startup")
async def app_startup() -> None:
    logger.info("Starting up")
    app.state.redis_client = await setup_redis_client()


@app.on_event("shutdown")
async def app_shutdown() -> None:
    logger.info("Shutting down")
    app.state.redis_client.close()


# Include our router
app.include_router(api_router, prefix=settings.API_V1_STR)
