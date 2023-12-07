from typing import Any

from chatgpt.convert_to_mathematica import convert
from wolfram.helper import Pod, get_pods


def serealize_subpod(subpod: Any) -> str:
    return subpod['plaintext']


def serealize_pod(pod: Pod) -> list[str]:
    return [serealize_subpod(subpod) for subpod in pod['subpods']]


def serealize_pods(pods: list[Pod] | None) -> list[list[str]] | None:
    if pods is None:
        return None

    return [serealize_pod(pod) for pod in pods]


async def question2pods(question: str) -> Any:
    converted = await convert(question)
    if converted is None:
        return None

    pods = await get_pods(converted, 'plaintext')
    return serealize_pods(pods)
