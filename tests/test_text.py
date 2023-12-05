import json

import pytest

from tests.test_helper import question2pods

with open('tests/data/text.json') as data:
    tests: list = json.load(data)

test_tuples = [(test['question'], test['answer']) for test in tests]


@pytest.mark.parametrize(('question', 'answer'), test_tuples)
async def test_text2answer(question: str, answer: str):
    """Test ChatGPT + Wolfram performance on input strings."""

    assert await question2pods(question) == answer
