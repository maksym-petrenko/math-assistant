from typing import Any, TypedDict

from solver.solver import solve

from .serializers import serialize


class TestData(TypedDict):
    question: str
    result: dict[str, Any]


async def question_to_test_result(question: str) -> dict[str, Any]:
    return serialize(await solve(question, None))
