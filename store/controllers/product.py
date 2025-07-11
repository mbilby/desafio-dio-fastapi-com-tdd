from fastapi import APIRouter, Body, Depends, status
from store.schemas.product import ProductIn, ProductOut
from store.usecases.product import ProductUsecases
from store.dependencies.dependencies import get_product_usecase

router = APIRouter(prefix="/products", tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=ProductOut)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecases = Depends(get_product_usecase)
) -> ProductOut:
    result = await usecase.create(body=body)
    return result
