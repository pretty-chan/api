from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from app.env_validator import settings
from app.logger import service_logger

logger = service_logger(__name__)


def bootstrap() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
        logger.info("Starting application")
        yield
        logger.info("Application shutdown complete")

    app = FastAPI(
        title="FooBar Backend API",
        lifespan=lifespan,
        docs_url="/api-docs",
        redoc_url=None,
        debug=settings.APP_ENV != "production",
    )
    return app


server = bootstrap()
