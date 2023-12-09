from dataclasses import dataclass, field, fields
from typing import Any

import pytest

from bot.solver import Response, solve
from wolfram.helper import Pod


@pytest.mark.skip()
@dataclass(init=False)
class TestResult:
    best_solution: Pod | None = None
    all_solutions: list[list[str]] = field(default_factory=list)
    exception: str | None = None

    def __init__(self, response: Response):
        self.best_solution = serealize_pod(response.best_solution) if response.best_solution else None
        self.all_solutions = serealize_pods(response.all_solutions)
        self.exception = response.exception

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'TestResult':
        response_placeholder = Response(original_question='')
        obj = TestResult(response_placeholder)
        for f in fields(obj):
            name = f.name
            setattr(obj, name, data[name])
        return obj


def serealize_subpod(subpod: Any) -> str:
    return subpod['plaintext']


def serealize_pod(pod: Pod) -> list[str]:
    return [serealize_subpod(subpod) for subpod in pod['subpods']]


def serealize_pods(pods: list[Pod]) -> list[list[str]]:
    return [serealize_pod(pod) for pod in pods]


async def question_to_test_result(question: str) -> TestResult:
    result = await solve(question)
    return TestResult(result)
