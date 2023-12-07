from chatgpt.convert_to_mathematica import convert
from wolfram.helper import get_step_by_step_solution


def serealize_pods(pods: list | None) -> list[str] | None:
    if pods is None:
        return None

    return [pod['plaintext'] for pod in pods]


async def question2pods(question: str) -> list[str] | None:
    converted = await convert(question)
    if converted is None:
        return None

    pods = await get_step_by_step_solution(converted, 'plaintext')
    return serealize_pods(pods)
