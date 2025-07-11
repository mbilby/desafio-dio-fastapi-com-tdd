from pydantic import BaseModel
from bson import Decimal128


class BaseSchemaMixin(BaseModel):
    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            Decimal128: lambda d: str(d),
        },
    }
