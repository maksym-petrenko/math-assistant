from typing import Any

from pydantic import BaseModel, model_validator

from bot.solver import WolframResponse, solve
from wolfram.api import Pod, Subpod, extract_usefull_subpods


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


class TestResult(BaseModel):
    best_solution: SerealizedPod | None
    all_solutions: list[SerealizedPod]
    exception: str | None

    @model_validator(mode='before')
    @classmethod
    def from_response(cls, data: Any) -> Any:
        if isinstance(data, WolframResponse):
            return {
                'best_solution': data.best_solution,
                'all_solutions': data.all_solutions,
                'exception': data.exception,
            }
        return data


async def question_to_test_result(question: str) -> TestResult:
    result = await solve(question)
    return TestResult.model_validate(result)
