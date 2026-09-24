from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import Settings
from core.logger import get_logger
from routes import base_route, search_route
from services.search import SearchService


def create_app(service: SearchService | None = None) -> FastAPI:
    """Build the API. Pass `service` to skip loading models (e.g. in tests)."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if service is None:
            get_logger().info("Loading models and indexes ...")
        app.state.search = service or SearchService.from_settings(Settings.from_env())
        yield

    app = FastAPI(title="evento", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(base_route)
    app.include_router(search_route)
    return app


app = create_app()
