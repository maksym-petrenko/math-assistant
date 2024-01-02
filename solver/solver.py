from chatgpt.chat_api import gpt
from chatgpt.choose_pod import choose_the_best_pod
from mathpix.api import image_to_latex
from wolfram.api import get_pods

from .responses import AnyResponse, ErrorResponse, GPTResponse, WolframResponse


class SolutionError(Exception):
    exception: str

    def __init__(self, exception: str):
        self.exception = exception


async def create_wolfram_response(query: str) -> WolframResponse:
    """returns response without any 'input' values"""

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
    return WolframResponse(wolfram_prompt=mathematica, all_solutions=pods, best_solution=best_solution)


async def create_gpt_response(query: str) -> GPTResponse:
    """returns response without any 'input' values"""

    solution = await gpt(query, 'Solve')

    if solution is None:
        raise SolutionError("Can't solve this problem, try to rephrase it")

    return GPTResponse(answer=solution)


async def solve_or_exception(text: str) -> AnyResponse:
    """returns response without any 'input' values"""

    request_type = await gpt(text, 'Classify')
    print(request_type)
    match request_type:
        case 'Wolfram':
            return await create_wolfram_response(text)
        case 'GPT':
            return await create_gpt_response(text)
        case _:
            raise SolutionError("Can't solve this")


async def latex_or_exception(image: bytes | None) -> str | None:
    if image is None:
        return None

    latex: str | None = await image_to_latex(image)
    if latex is None:
        raise SolutionError("Can't extract problem from the photo, try to send another one")
    return latex


async def solve(question: str, image: bytes | None) -> AnyResponse:
    try:
        latex = await latex_or_exception(image)
    except SolutionError as error:
        return ErrorResponse(original_question=question, error=error.exception)

    combined_question = question
    if latex is not None:
        combined_question += '\n' + latex

    try:
        response = await solve_or_exception(combined_question)

        response.original_question = question
        response.image_text = latex  # type: ignore[assignment] # some mypy bug
        response.combined_question = combined_question

        return response
    except SolutionError as error:
        return ErrorResponse(original_question=question, image_text=latex, combined_question=combined_question, error=error.exception)
