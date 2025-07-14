import pytest
import logging
from fastapi import status
from store.factory import product_data
from store.utils.utils import to_decimal128
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())
    content = {"name": "Iphone 14 pro max"}
    assert response.status_code == status.HTTP_201_CREATED
    assert content["name"] == response.json()["name"]


@pytest.mark.asyncio
async def test_controller_get_should_return_success(client, products_url):
    resp = await client.post(products_url, json=product_data())
    created = resp.json()
    response = await client.get(f"{products_url}{str(created['id'])}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(created["id"])


@pytest.mark.asyncio
async def test_controller_get_should_return_not_found(client, products_url):
    id = "4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    logger.info(f"Testing with non-existent product ID: {id}")
    with pytest.raises(NotFoundException):
        response = await client.get(f"{products_url}{id}")
        msg = "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": msg}


@pytest.mark.asyncio
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert isinstance(content, list)


async def test_controller_patch_should_return_success(client, products_url):
    product_in = ProductIn(**product_data())
    product_in.price = str(to_decimal128(product_in.price))
    created = await client.post(products_url, json=product_in.model_dump())
    product_inserted = created.json()
    product_update = ProductUpdate(price="7.500")
    product_update.price = str(to_decimal128(product_update.price))
    response = await client.patch(
        f"{products_url}{product_inserted['id']}", json=product_update.model_dump()
    )
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["quantity"] == product_inserted["quantity"]
    assert content["price"] != str(product_inserted["price"])

    assert str(content["price"]) == str(product_update.price)


async def test_controller_delete_should_return_not_content(client, products_url):
    response = await client.delete(
        f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
