from typing import Any

from pydantic import ValidationError

from chatgpt.chat_api import gpt

from .responses import ErrorResponse, GPTResponse, Response, ResponseTypes, SolutionError, WolframResponse


async def solve_or_exception(text: str) -> Response:
    request_type = await gpt(text, 'Classify')
    print(request_type)
    match request_type:
        case 'Wolfram':
            wolfram_response = WolframResponse(original_question=text)
            await wolfram_response.process()
            print("It's used", wolfram_response.original_question)
            print(wolfram_response.all_solutions)
            return wolfram_response
        case 'GPT':
            gpt_response = GPTResponse(original_question=text)
            await gpt_response.process()
            return gpt_response
        case _:
            raise SolutionError("Can't solve this")


async def solve(text: str) -> Response:
    try:
        return await solve_or_exception(text)
    except SolutionError as error:
        return ErrorResponse(original_question=text, error=error.exception)


def deserealize(data: dict[str, Any]) -> Response:
    """Throws ValidationError on unknown/broken response"""

    type2class: dict[ResponseTypes, type[Response]] = {
        'Error': ErrorResponse,
        'Wolfram': WolframResponse,
        'GPT': GPTResponse,
    }

    try:
        cls = type2class[data['type']]
    except KeyError as exc:
        raise ValidationError.from_exception_data('Something wrong with response type', []) from exc

    return cls.model_validate(data, strict=True)
