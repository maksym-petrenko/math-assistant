import json
from typing import Any, TypedDict

import pytest

from tests.runner import TestResult, question_to_test_result


class TestData(TypedDict):
    question: str
    result: TestResult


with open('tests/data/text.json') as data:
    tests: list[TestData] = json.load(data)

test_tuples = [(test['question'], test['result']) for test in tests]


@pytest.mark.parametrize(('question', 'result'), test_tuples)
async def test_question_to_all_solutions(question: str, result: dict[str, Any]) -> None:
    """Test ChatGPT(question) + Wolfram performance on input strings."""

    output = await question_to_test_result(question)
    assert output.model_dump() == result
