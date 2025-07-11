import pytest
import pytest_asyncio
from store.app import app
from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings
from dotenv import load_dotenv
from store.schemas.product import ProductIn
from store.factory import product_data
from uuid import UUID

load_dotenv()


# @pytest_asyncio.fixture(scope="session")
# def event_loop():
#     if sys.platform.startswith("win"):
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     loop = asyncio.new_event_loop()
#     yield loop


# Cria cliente MongoDB antes de cada teste e fecha depois
@pytest_asyncio.fixture(scope="function")
async def mongo_client():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    yield client
    client.close()


# Limpa as coleções antes de cada teste (exceto as system.*)
@pytest_asyncio.fixture(autouse=True, scope="function")
async def clear_collections(mongo_client):
    db = mongo_client.get_default_database()
    collections = await db.list_collection_names()
    for col in collections:
        if not col.startswith("system"):
            await db[col].delete_many({})
    yield  # Não precisa teardown após o teste


# Fixture para o cliente de teste HTTP
@pytest_asyncio.fixture(scope="function")
async def client():
    from httpx import AsyncClient

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# Fixture para a URL base dos produtos
@pytest.fixture
def products_url() -> str:
    return "/products/"


@pytest.fixture
def product_id() -> UUID:
    return UUID("fce6cc37-10b9-4a8e-a8b2-977df327001a")


@pytest.fixture
def product_in(product_id) -> ProductIn:
    retorno = ProductIn(**product_data(), id=product_id)
    return retorno
