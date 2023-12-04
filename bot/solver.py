from dataclasses import dataclass, field

from chatgpt.convert_to_mathematica import convert
from wolfram.helper import get_step_by_step_solution_image_only

from .helper import generate_code


@dataclass
class Response:
    solution: list[str] = field(default_factory=list)
    exception: str | None = None
    debug: str = ''


async def solve(text: str) -> Response:
    mathematica: str | None = await convert(text)
    if mathematica is None:
        return Response(exception="Can't understand the problem, try to rephrase it")

    response = Response(debug=generate_code(mathematica, 'mathematica'))

    images = await get_step_by_step_solution_image_only(mathematica)
    if images is None:
        response.exception = 'Something went wrong'
    elif len(images) == 0:
        response.exception = "Can't solve this problem, try to rephrase it"
    else:
        response.solution = images

    return response
