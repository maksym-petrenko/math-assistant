from typing import Any, Literal

from pydantic import BaseModel, Field, ValidationError

from chatgpt.chat_api import gpt
from chatgpt.choose_pod import choose_the_best_pod
from wolfram.api import Pod, get_pods

ResponseTypes = Literal['Error', 'Wolfram', 'GPT']


class SolutionError(Exception):
    exception: str

    def __init__(self, exception: str):
        self.exception = exception


class Response(BaseModel):
    type: ResponseTypes
    original_question: str
    image_text: str | None = None


class ErrorResponse(Response):
    type: ResponseTypes = 'Error'

    error: str


class WolframResponse(Response):
    type: ResponseTypes = 'Wolfram'

    wolfram_prompt: str = ''

    best_solution: Pod | None = None
    all_solutions: list[Pod] = Field(default_factory=list)

    async def calculate_the_best_answer(self) -> None:
        self.best_solution = await choose_the_best_pod(self.original_question, self.all_solutions)

    async def process(self) -> None:
        mathematica = await gpt(self.original_question, 'Wolfram')

        if mathematica == 'None' or mathematica is None:
            raise SolutionError("Can't understand the problem, try to rephrase it")

        self.wolfram_prompt = mathematica

        pods = await get_pods(mathematica)
        print(pods)
        if pods is None:
            raise SolutionError('Something went wrong')
        if len(pods) == 0:
            raise SolutionError("Can't solve this problem, try to rephrase it")
        self.all_solutions = pods
        await self.calculate_the_best_answer()


class GPTResponse(Response):
    type: ResponseTypes = 'GPT'

    answer: str = ''

    async def process(self) -> None:
        message = await gpt(self.original_question, 'Solve')

        if message is None:
            raise SolutionError("Can't solve this problem, try to rephrase it")

        self.answer = message


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
