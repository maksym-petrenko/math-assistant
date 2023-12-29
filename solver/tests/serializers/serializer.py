from typing import Any

from pydantic import BaseModel, ValidationError

from solver import Response
from solver.responses import ErrorResponse, GPTResponse, ResponseTypeLiteral

from .wolfram_serializer import SerializedWolfram

SerializedGPT = GPTResponse
SerializedError = ErrorResponse

type2serialized: dict[ResponseTypeLiteral, type[BaseModel]] = {
    'Error': SerializedError,
    'Wolfram': SerializedWolfram,
    'GPT': SerializedGPT,
}


def serialize(response: Response) -> dict[str, Any]:
    # don't handle the case when there is a wrong type
    cls = type2serialized[response.type]
    return cls.model_validate(response, from_attributes=True).model_dump()


def validate_result(data: dict[str, Any]) -> bool:
    try:
        cls = type2serialized[data['type']]
        cls.model_validate(data, strict=True)
        return True
    except (KeyError, ValidationError):
        return False
