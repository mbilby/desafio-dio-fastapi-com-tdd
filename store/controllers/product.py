from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecases
from store.dependencies.dependencies import get_product_usecase

router = APIRouter(prefix="/products", tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=ProductOut)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecases = Depends(get_product_usecase)
) -> ProductOut:
    result = await usecase.create(body=body)
    return result


@router.get(path="/{id}", status_code=status.HTTP_200_OK, response_model=ProductOut)
async def get(
    id: UUID4 = Path(alias="id"),
    usecase: ProductUsecases = Depends(get_product_usecase),
) -> ProductOut:
    result = await usecase.get(id=id)
    return result


@router.get(path="/", status_code=status.HTTP_200_OK, response_model=list[ProductOut])
async def query(
    usecase: ProductUsecases = Depends(get_product_usecase),
) -> list[ProductOut]:
    result = await usecase.query()
    return result


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecases = Depends(get_product_usecase),
) -> ProductUpdateOut:
    return await usecase.update(id=id, body=body)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"),
    usecase: ProductUsecases = Depends(get_product_usecase),
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
