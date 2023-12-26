from chatgpt.chat_api import gpt
from chatgpt.choose_pod import choose_the_best_pod
from wolfram.api import get_pods

from .responses import AnyResponse, ErrorResponse, GPTResponse, WolframResponse


class SolutionError(Exception):
    exception: str

    def __init__(self, exception: str):
        self.exception = exception


async def create_wolfram_response(query: str) -> WolframResponse:
    mathematica = await gpt(query, 'Wolfram')

    if mathematica == 'None' or mathematica is None:
        raise SolutionError("Can't understand the problem, try to rephrase it")

    pods = await get_pods(mathematica)
    print(pods)
    if pods is None:
        raise SolutionError('Something went wrong')
    if len(pods) == 0:
        raise SolutionError("Can't solve this problem, try to rephrase it")

    best_solution = await choose_the_best_pod(query, pods)
    return WolframResponse(original_question=query, wolfram_prompt=mathematica, all_solutions=pods, best_solution=best_solution)


async def create_gpt_response(query: str) -> GPTResponse:
    solution = await gpt(query, 'Solve')

    if solution is None:
        raise SolutionError("Can't solve this problem, try to rephrase it")

    return GPTResponse(original_question=query, answer=solution)


async def solve_or_exception(text: str) -> AnyResponse:
    request_type = await gpt(text, 'Classify')
    print(request_type)
    match request_type:
        case 'Wolfram':
            return await create_wolfram_response(text)
        case 'GPT':
            return await create_gpt_response(text)
        case _:
            raise SolutionError("Can't solve this")


async def solve(text: str) -> AnyResponse:
    try:
        return await solve_or_exception(text)
    except SolutionError as error:
        return ErrorResponse(original_question=text, error=error.exception)
