from dataclasses import dataclass, field

from chatgpt.chat_api import gpt
from chatgpt.choose_the_best import choose
from wolfram.helper import Pod, get_pods

from .helper import generate_code


@dataclass
class Response:
    original_question: str
    exception: str | None = None
    debug: str = ''


class WolframResponse(Response):
    best_solution: Pod | None = None
    all_solutions: list[Pod] = field(default_factory=list)

    async def calculate_the_best_answer(self) -> None:
        if self.exception:
            return

        self.best_solution = await choose(self.original_question, self.all_solutions)

    def set_exception(self, exception: str) -> 'Response':
        self.exception = exception
        return self


class GPTResponse(Response):
    answer: str


async def get_all_solutions(text: str) -> Response | None:

    request_type = await gpt(text, 'Classify')
    print(request_type)

    if request_type == 'Wolfram':

        response = WolframResponse(
            original_question=text,
        )

        mathematica: str | None = await gpt(text, 'Wolfram')
        print(mathematica)
        if mathematica is None:
            return response.set_exception("Can't understand the problem, try to rephrase it")
        response.debug = generate_code(mathematica, 'mathematica')

        pods = await get_pods(mathematica)
        if pods is None:
            return response.set_exception('Something went wrong')
        if len(pods) == 0:
            return response.set_exception("Can't solve this problem, try to rephrase it")

        response.all_solutions = pods
        return response

    if request_type == 'GPT':

        response = GPTResponse(
            original_question=text,
        )

        message = await gpt(text, 'Solve', model='gpt-4')
        response.answer = message
        return response

    return Response(
        original_question=text,
        exception="Can't solve this",
    )



async def solve(text: str) -> Response:
    response = await get_all_solutions(text)
    if isinstance(response, WolframResponse):
        await response.calculate_the_best_answer()
    return response
