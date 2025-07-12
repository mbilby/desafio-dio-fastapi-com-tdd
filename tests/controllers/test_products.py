from fastapi import status
from store.factory import product_data


async def test_controller_create_should_return_success(client, products_url):
    response = client.post(products_url, json=product_data())
    assert response.status_code == status.HTTP_201_CREATED
