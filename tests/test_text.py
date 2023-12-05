import json

import pytest

from chatgpt.convert_to_mathematica import convert
from tests.serealize_answer import serealize
from wolfram.helper import get_step_by_step_solution

with open('tests/data/text.json') as data:
    tests: list = json.load(data)

test_tuples = [(test['question'], test['answer']) for test in tests]


@pytest.mark.parametrize(('question', 'answer'), test_tuples)
@pytest.mark.asyncio()
async def test_text2answer(question: str, answer: str):
    """Test ChatGPT + Wolfram performance on input strings."""

    converted = await convert(question)
    pods = await get_step_by_step_solution(converted, 'image')

    assert serealize(pods) == answer
