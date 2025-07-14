from contextlib import asynccontextmanager
from fastapi import FastAPI
from store.core.config import settings
from store.routers import api_router
from motor.motor_asyncio import AsyncIOMotorClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código de inicialização
    print("Aplicação iniciada!")
    app.state.mongo_client = AsyncIOMotorClient(settings.DATABASE_URL)
    app.state.db = app.state.mongo_client.get_default_database()
    yield
    app.state.mongo_client.close()
    # Código de finalização
    print("Aplicação finalizada!")


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            lifespan=lifespan,
            version="0.0.1",
            title=settings.PROJECT_NAME,
            root_path=settings.ROOT_PATH
        )


app = App()

app.include_router(api_router)
