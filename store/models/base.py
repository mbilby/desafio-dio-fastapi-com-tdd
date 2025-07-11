from datetime import datetime
from decimal import Decimal
from bson import Decimal128
from pydantic import BaseModel, Field, UUID4, model_serializer
from typing import Any
from uuid import uuid4


class CreateBaseModel(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @model_serializer
    def set_model(self) -> dict[str, Any]:
        self_dict = dict(self)

        for key, value in self_dict.items():
            if isinstance(value, Decimal):
                self_dict[key] = Decimal128(str(value))

        return self_dict
