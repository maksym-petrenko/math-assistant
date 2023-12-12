from pydantic import BaseModel, Field

from chatgpt.chat_api import gpt
from chatgpt.choose_the_best import choose
from wolfram.api import Pod, get_pods

from .markup_code import generate_code


class Response(BaseModel):
    original_question: str
    exception: str | None = None
    debug: str = ''

    def set_exception(self, exception: str) -> 'Response':
        self.exception = exception
        return self


class WolframResponse(Response):
    best_solution: Pod | None = None
    exception: str | None = None
    debug: str = ''
    all_solutions: list[Pod] = Field(default_factory=list)

    async def calculate_the_best_answer(self) -> None:
        if self.exception:
            return

        self.best_solution = await choose(self.original_question, self.all_solutions)


class GPTResponse(Response):
    answer: str = ''


async def get_all_solutions(text: str) -> Response | GPTResponse | WolframResponse:
    request_type = await gpt(text, 'Classify')
    print(request_type)

    if request_type == 'Wolfram':

        wolfram_response = WolframResponse(
            original_question=text,
        )

        mathematica: str | None = await gpt(text, 'Wolfram')
        print(mathematica)
        if mathematica is None:
            return wolfram_response.set_exception("Can't understand the problem, try to rephrase it")
        wolfram_response.debug = generate_code(mathematica, 'mathematica')

        pods = await get_pods(mathematica)
        if pods is None:
            return wolfram_response.set_exception('Something went wrong')
        if len(pods) == 0:
            return wolfram_response.set_exception("Can't solve this problem, try to rephrase it")

        wolfram_response.all_solutions = pods
        return wolfram_response

    if request_type == 'GPT':
        gpt_response = GPTResponse(original_question=text)

        message = await gpt(text, 'Solve')

        if message is None:
            message = "Can't solve this, try to rephrase it."

        gpt_response.answer = message

        return gpt_response

    return Response(
        original_question=text,
        exception="Can't solve this",
    )


async def solve(text: str) -> Response:
    response = await get_all_solutions(text)
    if isinstance(response, WolframResponse):
        await response.calculate_the_best_answer()
    return response
