from decimal import Decimal
from store.schemas.base import BaseSchemaMixin
from store.utils.utils import convert_decimal128
from pydantic import Field, BaseModel, UUID4, PlainSerializer, model_validator
from datetime import datetime
from typing import Annotated, Optional, Any


class ProductBase(BaseModel):
    name: str = Field(description="Product name")
    quantity: int = Field(
        ..., description="Product quantity"
    )  # (...) indica que campo é obrigatorio
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")

    @model_validator(mode="before")
    @classmethod
    def convert_decimal128_to_decimal_on_input(cls, data: Any) -> Any:
        return convert_decimal128(data)


class ProductIn(ProductBase, BaseSchemaMixin):
    ...


DecimalOut = Annotated[
    Decimal, PlainSerializer(lambda d: str(d), return_type=str, when_used="json")
]


class ProductOut(ProductIn):
    id: UUID4 = Field()
    created_at: Optional[datetime] = Field()
    updated_at: Optional[datetime] = Field()
    price: DecimalOut = Field(..., description="Product price")


class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(
        None, description="Product quantity"
    )  # (...) indica que campo é obrigatorio
    price: Optional[DecimalOut] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")


class ProductUpdateOut(ProductUpdate):
    ...
