import pytest
import logging
from fastapi import status
from store.factory import product_data
from store.core.exceptions import NotFoundException

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


async def test_controller_get_should_return_not_found(client, products_url):
    try:
        response = await client.get(
            f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
        )
    except NotFoundException as e:
        e.message = (
            "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
        )
        logger.error(e.message)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }


@pytest.mark.asyncio
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)
    assert response.status_code == status.HTTP_200_OK


async def test_controller_patch_should_return_success(
    client, products_url, product_inserted
):
    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "7.500"}
    )

    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "7.500",
        "status": True,
    }


async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(
        f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }
