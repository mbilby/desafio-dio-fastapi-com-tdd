from bson import Decimal128
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.models.product import ProductModel
from uuid import UUID
from store.core.exceptions import NotFoundException
from decimal import Decimal
from store.utils.utils import convert_bson_types


class ProductUsecases:
    def __init__(self, db: AsyncIOMotorClient) -> None:
        self.collection = db["products"]

    async def create(self, body: ProductIn) -> ProductOut:
        if self.collection is None:
            raise RuntimeError("Collection is not initialized.")
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())
        return ProductOut(**product_model.model_dump())

    async def create_products(self, body: list[ProductIn]) -> list[ProductOut]:
        documents = [product.model_dump() for product in body]

        await self.collection.insert_many(documents)

        inserted_uuids = [product.id for product in body]

        retrieved_docs = await self.collection.find(
            {"id": {"$in": [uuid for uuid in inserted_uuids]}}
        ).to_list(length=None)

        return [ProductOut.model_validate(doc) for doc in retrieved_docs]

    async def get(self, id: UUID) -> ProductOut:
        if self.collection is None:
            raise RuntimeError("Collection is not initialized.")
            result = await self.collection.find_one({"id": id})
            if result is None:
                raise NotFoundException(message=f"Product not found with filter: {id}")
            return ProductOut(**result)

    async def query(self) -> list[ProductOut]:
        products = []
        async for item in self.collection.find():
            clean_item = convert_bson_types(item)
            product_model = ProductModel(**clean_item)
            product_out = ProductOut.model_validate(product_model)
            products.append(product_out)

        return products

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        update_data = body.model_dump(exclude_none=True)
        for key, value in update_data.items():
            if isinstance(value, Decimal):
                update_data[key] = Decimal128(str(value))

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        clean_result = convert_bson_types(result)

        return ProductUpdateOut(**clean_result)

    async def delete(self, id: UUID) -> bool:
        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False
