
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

    async def process(self) -> None:
        gpt_request = await gpt(self.original_question, 'Wolfram')

        if gpt_request == 'None' or gpt_request is None:
            self.set_exception("Can't understand the problem, try to rephrase it")
            return

        mathematica = gpt_request

        self.debug = generate_code(mathematica, 'mathematica')

        pods = await get_pods(mathematica)
        print(pods)
        if pods is None:
            self.set_exception('Something went wrong')
            return
        if len(pods) == 0:
            self.set_exception("Can't solve this problem, try to rephrase it")
            return
        self.all_solutions = pods
        await self.calculate_the_best_answer()


class GPTResponse(Response):
    answer: str = ''

    async def process(self) -> None:
        message = await gpt(self.original_question, 'Solve')

        if message is None:
            message = "Can't solve this, try to rephrase it."

        self.answer = message


async def solve(text: str) -> Response | GPTResponse | WolframResponse:
    request_type = await gpt(text, 'Classify')
    print(request_type)
    if request_type == 'Wolfram':
        wolfram_response = WolframResponse(original_question=text)
        await wolfram_response.process()
        print("It's used", wolfram_response.original_question)
        print(wolfram_response.all_solutions)

        return wolfram_response

    if request_type == 'GPT':
        gpt_response = GPTResponse(original_question=text)
        await gpt_response.process()

        return gpt_response

    return Response(original_question=text, exception="Can't solve this")
