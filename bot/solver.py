from pydantic import BaseModel, Field

from chatgpt.choose_pod import choose_the_best_pod
from chatgpt.convert_to_mathematica import convert
from wolfram.api import Pod, get_pods

from .markup_code import generate_code


class Response(BaseModel):
    original_question: str
    best_solution: Pod | None = None
    all_solutions: list[Pod] = Field(default_factory=list)
    exception: str | None = None
    debug: str = ''

    async def calculate_the_best_answer(self) -> None:
        if self.exception:
            return

        self.best_solution = await choose_the_best_pod(self.original_question, self.all_solutions)

    def set_exception(self, exception: str) -> 'Response':
        self.exception = exception
        return self


async def get_all_solutions(text: str) -> Response:
    response = Response(original_question=text)

    mathematica: str | None = await convert(text)
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


async def solve(text: str) -> Response:
    response = await get_all_solutions(text)
    await response.calculate_the_best_answer()
    return response
