import json
from dataclasses import asdict
from typing import Any

import pytest

from tests.runner import question_to_test_result

with open('tests/data/text.json') as data:
    tests: list = json.load(data)

test_tuples = [(test['question'], test['result']) for test in tests]


@pytest.mark.parametrize(('question', 'result'), test_tuples)
async def test_question_to_all_solutions(question: str, result: dict[str, Any]):
    """Test ChatGPT(question) + Wolfram performance on input strings."""

    output = await question_to_test_result(question)
    assert asdict(output) == result
