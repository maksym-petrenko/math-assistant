from typing import Any, Literal

from pydantic import BaseModel, Field, ValidationError

from wolfram import Pod

ResponseTypeLiteral = Literal['Error', 'Wolfram', 'GPT']


class Response(BaseModel):
    type: ResponseTypeLiteral

    original_question: str
    image_text: str | None = None


class ErrorResponse(Response):
    type: ResponseTypeLiteral = 'Error'

    error: str


class WolframResponse(Response):
    type: ResponseTypeLiteral = 'Wolfram'

    wolfram_prompt: str = ''

    all_solutions: list[Pod] = Field(default_factory=list)
    best_solution: Pod | None = None


class GPTResponse(Response):
    type: ResponseTypeLiteral = 'GPT'

    answer: str = ''


AnyResponse = ErrorResponse | WolframResponse | GPTResponse

def deserialize(data: dict[str, Any]) -> Response:
    """Throws ValidationError on unknown/broken response"""

    print('Data:', data)

    type2class: dict[ResponseTypeLiteral, type[AnyResponse]] = {
        'Error': ErrorResponse,
        'Wolfram': WolframResponse,
        'GPT': GPTResponse,
    }

    try:
        cls = type2class[data['type']]
    except KeyError as exc:
        raise ValidationError.from_exception_data('Something wrong with response type', []) from exc

    return cls.model_validate(data, strict=True)
