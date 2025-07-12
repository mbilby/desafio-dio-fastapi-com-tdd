from uuid import UUID
import pytest
from bson.decimal128 import Decimal128
from decimal import Decimal
from store.schemas.product import ProductIn, ProductUpdate, ProductUpdateOut
from store.factory import product_data_update
from store.core.exceptions import NotFoundException


# --- Testes ---
@pytest.mark.asyncio
async def test_usecases_should_return_success(mock_product_usecase, product_in):
    result = await mock_product_usecase.create(body=product_in)
    assert result.name == "Iphone 14 pro max"


@pytest.mark.asyncio
async def test_usecases_get_should_return_success(mock_product_usecase, product_in):
    created_product = await mock_product_usecase.create(body=product_in)
    result = await mock_product_usecase.get(id=created_product.id)
    assert result.name == product_in.name


@pytest.mark.asyncio
async def test_usecases_get_should_not_found(mock_product_usecase):
    id = UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9")

    with pytest.raises(NotFoundException) as err:
        await mock_product_usecase.get(id)

    assert err.value.message == f"Product not found with filter: {id}"


@pytest.mark.asyncio
async def test_usecases_query_should_success(mock_product_usecase):
    result = await mock_product_usecase.query()
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_usecases_update_should_success(mock_product_usecase, product_model):
    product_in = ProductIn.model_validate(product_model)
    product_up = ProductUpdate(**product_data_update())

    created_product = await mock_product_usecase.create(body=product_in)
    result = await mock_product_usecase.update(id=created_product.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)


@pytest.mark.asyncio
async def test_usecases_delete_should_success(mock_product_usecase, product_in):
    created_product = await mock_product_usecase.create(body=product_in)
    result = await mock_product_usecase.delete(id=created_product.id)
    assert result is True


@pytest.mark.asyncio
async def test_usecases_query_products_should_success(
    mock_product_usecase, products_model
):
    product_in = []
    for product in products_model:
        if isinstance(product.price, Decimal):
            product.price = Decimal128(str(product.price))
        product_in.append(ProductIn.model_validate(product))

    created_products = await mock_product_usecase.create_products(product_in)

    assert isinstance(created_products, list)
    assert created_products[0].name == products_model[0].name
