from decimal import Decimal

from bson import Decimal128
from store.usecases.product import ProductUsecases
from store.schemas.product import ProductOut, ProductIn, ProductUpdate, ProductUpdateOut
from motor.motor_asyncio import AsyncIOMotorClient
from store.factory import product_data, product_data_update, products_data
from store.core.exceptions import NotFoundException
from store.models.product import ProductModel
from store.core.config import settings
from uuid import UUID
import pytest


def client_connect():
    """Cria e retorna uma instância do banco e o cliente Motor."""
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    db = client.get_default_database()
    return db, client


async def close_connect(db, client):
    """Remove todas as coleções do banco (exceto system.*) e fecha a conexão."""
    collections = await db.list_collection_names()
    for col in collections:
        if not col.startswith("system"):
            await db[col].delete_many({})
    client.close()


@pytest.mark.asyncio
async def test_usecases_should_return_success(product_in):
    # Before
    db, client = client_connect()
    product_usecase = ProductUsecases(client=client)

    # Act
    result = await product_usecase.create(body=product_in)
    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro max"

    # After
    await close_connect(db=db, client=client)


@pytest.mark.asyncio
async def test_usecases_get_should_return_success(product_in):
    # Before
    db, client = client_connect()
    product_usecase = ProductUsecases(client=client)

    # Act: busca o produto recém-criado usando o ID
    created_product = await product_usecase.create(body=product_in)
    result = await product_usecase.get(id=created_product.id)
    assert result is not None, "Produto não encontrado no banco."
    assert isinstance(result, ProductOut), "Tipo do resultado incorreto."
    assert (
        result.name == product_in.name
    ), f"Nome esperado: {product_in.name}, encontrado: {result.name}"

    # After
    await close_connect(db=db, client=client)


async def test_usecases_get_should_not_found():
    # Before
    db, client = client_connect()
    product_usecase = ProductUsecases(client=client)

    # Act
    id = UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9")
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id)

    assert err.value.message == f"Product not found with filter: {id}"

    # After
    await close_connect(db=db, client=client)


@pytest.mark.asyncio
async def test_usecases_query_should_success():
    # Before
    db, client = client_connect()
    product_usecase = ProductUsecases(client=client)

    # Act
    result = await product_usecase.query()
    assert isinstance(result, list)

    # After
    await close_connect(db=db, client=client)


@pytest.mark.asyncio
async def test_usecases_update_should_success():
    # Before
    db, client = client_connect()
    product_usecase = ProductUsecases(client=client)

    # Act:
    product_model = ProductModel(**product_data())
    product_in = ProductIn.model_validate(product_model)
    product_up = ProductUpdate(**product_data_update())
    created_product = await product_usecase.create(body=product_in)
    result = await product_usecase.update(id=created_product.id, body=product_up)
    assert isinstance(result, ProductUpdateOut)

    # After
    await close_connect(db=db, client=client)


@pytest.mark.asyncio
async def test_usecases_delete_should_success():
    # Before
    db, client = client_connect()
    product_usecase = ProductUsecases(client=client)
    product_in = ProductIn(**product_data())

    # Act
    create_product = await product_usecase.create(body=product_in)
    result = await product_usecase.delete(id=create_product.id)

    assert result is True

    # After
    await close_connect(db=db, client=client)


@pytest.mark.asyncio
async def test_usecases_query_products_should_success():
    # Before
    product_in = []
    db, client = client_connect()
    product_usecase = ProductUsecases(client=client)

    # Act
    product_model = [ProductModel(**product) for product in products_data()]
    for product in product_model:
        if isinstance(product.price, Decimal):
            product.price = Decimal128(str(product.price))
        validated = ProductIn.model_validate(product)
        product_in.append(validated)

    created_products = await product_usecase.create_products(product_in)

    assert isinstance(created_products, list)
    assert created_products[0].name == product_model[0].name

    # After
    await close_connect(db=db, client=client)
