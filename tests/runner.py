from typing import Any, TypedDict

from pydantic import BaseModel, model_validator

from solver.solver import WolframResponse, solve
from wolfram.api import Pod, Subpod, extract_usefull_subpods


class TestData(TypedDict):
    question: str
    result: dict[str, Any]


def serealize_subpod(subpod: Subpod) -> str:
    return subpod.plaintext


def serealize_subpods(subpods: list[Subpod]) -> list[str]:
    return [serealize_subpod(subpod) for subpod in subpods]


class SerealizedPod(BaseModel):
    all_subpods: list[str]
    usefull_subpods: list[str]

    @model_validator(mode='before')
    @classmethod
    def from_pod(cls, data: Any) -> Any:
        if isinstance(data, Pod):
            return {
                'all_subpods': serealize_subpods(data.subpods),
                'usefull_subpods': serealize_subpods(extract_usefull_subpods(data)),
            }
        return data


def serealize_pod(pod: Pod | None) -> dict[str, Any]:
    return SerealizedPod.model_validate(pod).model_dump()


def serealize_wolfram(response: WolframResponse) -> dict[str, Any]:
    result = response.model_dump()
    result['best_solution'] = serealize_pod(response.best_solution)
    result['all_solutions'] = [serealize_pod(pod) for pod in response.all_solutions]
    return result


async def question_to_test_result(question: str) -> dict[str, Any]:
    result = await solve(question)
    if isinstance(result, WolframResponse):  # special handling caused by pods
        return serealize_wolfram(result)
    return result.model_dump()
