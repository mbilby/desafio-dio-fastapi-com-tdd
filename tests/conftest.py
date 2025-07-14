import logging
from httpx import AsyncClient, ASGITransport
import pytest
from time import time
from store.app import app
from asgi_lifespan import LifespanManager
from store.schemas.product import ProductIn, ProductOut
from store.models.product import ProductModel
from store.usecases.product import ProductUsecases
from motor.motor_asyncio import AsyncIOMotorClient
from store.factory import product_data, products_data
from store.core.config import settings
from uuid import UUID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def log_test_time(request):
    """Mede o tempo de execução de cada teste."""
    start = time()
    yield
    duration = time() - start
    logger.info(f"Test '{request.node.name}' completed in {duration:.4f} seconds.")


@pytest.fixture
def db_connection():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    db = client.store
    return db


@pytest.fixture
def mock_product_usecase(db_connection):
    return ProductUsecases(db_connection)


@pytest.fixture
def product_id() -> UUID:
    return UUID("fce6cc37-10b9-4a8e-a8b2-977df327001a")


@pytest.fixture
def product_in(product_id) -> ProductIn:
    retorno = ProductIn(**product_data(), id=product_id)
    return retorno


@pytest.fixture
def product_out(product_in, product_id) -> ProductOut:
    product_model = ProductModel.model_validate(product_in)
    data = product_model.model_dump()
    data["id"] = str(product_id)
    retorno = ProductOut.model_validate(data)
    return retorno


@pytest.fixture
def product_model() -> ProductModel:
    retorno = ProductModel(**product_data())
    return retorno


@pytest.fixture
def products_model() -> list[ProductModel]:
    retorno = [ProductModel(**product) for product in products_data()]
    return retorno


### @pytest.fixture - CONTROLLERS


@pytest.fixture
async def client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as test_client:
            yield test_client


# Fixture para a URL base dos produtos
@pytest.fixture
def products_url() -> str:
    return "/products/"
