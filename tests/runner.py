from dataclasses import dataclass, field
from typing import Any

from bot.solver import Response, solve
from wolfram.helper import Pod, extract_usefull_subpods


@dataclass(init=False)
class SerealizedPod:
    all_subpods: list[str]
    usefull_subpods: list[str]

    def __init__(self, pod: Pod):
        self.all_subpods = serealize_subpods(pod['subpods'])
        self.usefull_subpods = serealize_subpods(extract_usefull_subpods(pod))

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'SerealizedPod':
        pod_placeholder: Pod = {'subpods': []}
        obj = SerealizedPod(pod_placeholder)

        obj.all_subpods = data['all_subpods']
        obj.usefull_subpods = data['usefull_subpods']

        return obj


@dataclass(init=False)
class TestResult:
    best_solution: SerealizedPod | None = None
    all_solutions: list[SerealizedPod] = field(default_factory=list)
    exception: str | None = None

    def __init__(self, response: Response):
        self.best_solution = SerealizedPod(response.best_solution) if response.best_solution else None
        self.all_solutions = [SerealizedPod(pod) for pod in response.all_solutions]
        self.exception = response.exception

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'TestResult':
        response_placeholder = Response(original_question='')
        obj = TestResult(response_placeholder)

        if best_solution := data['best_solution']:
            obj.best_solution = SerealizedPod.from_dict(best_solution)
        obj.all_solutions = [SerealizedPod.from_dict(pod) for pod in data['all_solutions']]
        obj.exception = data['exception']

        return obj


def serealize_subpod(subpod: Any) -> str:
    return subpod['plaintext']

def serealize_subpods(subpods: list[Any]) -> list[str]:
    return [subpod['plaintext'] for subpod in subpods]


async def question_to_test_result(question: str) -> TestResult:
    result = await solve(question)
    return TestResult(result)
