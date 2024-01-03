import json
from typing import Any

import pytest

from .helper import data_path
from .runner import TestData, question_to_test_result

with open(data_path / 'text.json') as data:
    tests: list[TestData] = json.load(data)

test_tuples = [(test['question'], test['result']) for test in tests]


@pytest.mark.parametrize(('question', 'result'), test_tuples)
async def test_question_to_all_solutions(question: str, result: dict[str, Any]) -> None:
    """Test ChatGPT(question) + Wolfram performance on input strings."""

    output = await question_to_test_result(question)
    assert output == result
