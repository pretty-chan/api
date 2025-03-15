from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from app.env_validator import settings
from app.logger import service_logger

from router.search import router as search_router

logger = service_logger(__name__)


def bootstrap() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
        logger.info("Starting application")
        yield
        logger.info("Application shutdown complete")

    app = FastAPI(
        title="Payload API",
        lifespan=lifespan,
        docs_url="/api-docs",
        redoc_url=None,
        debug=settings.APP_ENV != "production",
    )

    origins = ["http://localhost:7001"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


server = bootstrap()
server.include_router(search_router)
