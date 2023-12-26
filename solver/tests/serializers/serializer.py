from typing import Any

from pydantic import ValidationError

from solver import Response, WolframResponse, deserealize

from .wolfram_serializer import serialize as serialize_wolfram
from .wolfram_serializer import validate as validate_wolfram


def serialize(response: Response) -> dict[str, Any]:
    if isinstance(response, WolframResponse):  # special handling caused by pods
        return serialize_wolfram(response)
    return response.model_dump()


def validate_result(data: dict[str, Any]) -> bool:
    type_ = data.get('type')
    if type_ == 'Wolfram':
        return validate_wolfram(data)

    try:
        deserealize(data)
        return True
    except ValidationError:
        return False
