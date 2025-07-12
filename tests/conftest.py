import logging
import pytest
from time import time
from contextlib import asynccontextmanager
from store.app import app
from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings
from store.schemas.product import ProductIn
from store.models.product import ProductModel
from store.usecases.product import ProductUsecases
from store.factory import product_data, products_data
from fastapi.testclient import TestClient
from uuid import UUID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def db_context():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    db = client.get_default_database()
    try:
        yield db, client
    finally:
        collections = await db.list_collection_names()
        for col in collections:
            if not col.startswith("system"):
                await db[col].delete_many({})
        client.close()


@pytest.fixture(scope="function", autouse=True)
async def db_and_client():
    """Fixture global para fornecer DB e client e limpar tudo após cada teste."""
    async with db_context() as (db, client):
        yield db, client


@pytest.fixture(autouse=True)
def log_test_time(request):
    """Mede o tempo de execução de cada teste."""
    start = time()
    yield
    duration = time() - start
    logger.info(f"Test '{request.node.name}' completed in {duration:.4f} seconds.")


# Exemplo de mock
@pytest.fixture
def mock_product_usecase(db_and_client):
    db, client = db_and_client
    return ProductUsecases(client=client)


# Fixture para o cliente de teste HTTP
@pytest.fixture(scope="function")
def client():
    with TestClient(app=app, base_url="http://test") as test_client:
        yield test_client


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


@pytest.fixture
def product_model() -> ProductModel:
    retorno = ProductModel(**product_data())
    return retorno


@pytest.fixture
def products_model() -> list[ProductModel]:
    retorno = [ProductModel(**product) for product in products_data()]
    return retorno
