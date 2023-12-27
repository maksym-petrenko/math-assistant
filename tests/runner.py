from typing import Any

from pydantic import BaseModel, model_validator

from bot.solver import GPTResponse, Response, WolframResponse, solve
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
    type: str
    best_solution: str | None
    all_solutions: list[str] | None
    mathematica: str | None
    exception: str | None
    answer: str | None

    @model_validator(mode='before')
    @classmethod
    def from_response(cls, data: Any) -> Any:
        match data:
            case WolframResponse():
                return {
                    'type': 'Wolfram',
                    'best_solution': data.best_solution.id,  # type: ignore[union-attr]
                    'all_solutions': [pod.id for pod in data.all_solutions],
                    'mathematica': data.mathematica_request,
                    'exception': data.exception,
                    'answer': None,
                }
            case GPTResponse():
                return {
                    'type': 'GPT',
                    'best_solution': None,
                    'all_solutions': None,
                    'mathematica': None,
                    'exception': None,
                    'answer': None,
                }
            case Response():
                return {
                    'type': 'Error',
                    'best_solution': None,
                    'all_solutions': None,
                    'mathematica': None,
                    'exception': data.exception,
                    'answer': None,
                }
            case _:
                return data


async def question_to_test_result(question: str) -> TestResult:
    result = await solve(question)
    return TestResult.model_validate(result)
