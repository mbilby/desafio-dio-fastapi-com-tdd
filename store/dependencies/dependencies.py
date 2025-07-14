from store.usecases.product import ProductUsecases
from fastapi import Request


async def get_product_usecase(request: Request) -> ProductUsecases:
    db = request.app.state.db
    return ProductUsecases(db)
