from decimal import Decimal
from bson import Decimal128
from typing import Any


def convert_decimal128(value: Any) -> Any:
    if isinstance(value, Decimal128):
        return Decimal(str(value))
    elif isinstance(value, dict):
        return {k: convert_decimal128(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_decimal128(v) for v in value]
    return value


def convert_bson_types(doc):
    """
    Converte valores BSON como Decimal128 → Decimal para compatibilidade com Pydantic
    """
    if not doc:
        return doc
    doc_copy = doc.copy()
    for k, v in doc_copy.items():
        if isinstance(v, Decimal128):
            doc_copy[k] = Decimal(str(v))
    return doc_copy


def to_decimal128(obj):
    if isinstance(obj, dict):
        return {k: to_decimal128(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_decimal128(v) for v in obj]
    elif isinstance(obj, Decimal):
        return Decimal128(str(obj))
    return obj
