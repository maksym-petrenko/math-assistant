import asyncio
import json
from pathlib import Path
from typing import Any

from chatgpt.convert_to_mathematica import convert
from helper.aiohttp_client import stop as stop_client
from helper.main_handler import main_handler
from wolfram.helper import get_step_by_step_solution

data_path = Path(__file__).parent

# only generates if there no answer yet
async def generate_answer(test: dict[str, Any]) -> str:
    question = test['question']
    if 'answer' in test:
        print('skipping:', question)
        return test['answer']

    print('generating for:', question)

    converted = await convert(question)
    pods = await get_step_by_step_solution(converted, 'image')

    return pods[0]['img']['alt']


async def main() -> None:
    tests = []
    with open(data_path / 'text.json') as text_data:  # noqa: ASYNC101
        tests = json.load(text_data)

    answers = await asyncio.gather(*[generate_answer(test) for test in tests])
    for test, answer in zip(tests, answers, strict=True):
        test['answer'] = answer

    with open(data_path / 'text.json', 'w') as text_data:  # noqa: ASYNC101
        json.dump(tests, text_data, indent=4)
        text_data.write('\n')

if __name__ == '__main__':
    main_handler(main, None, stop_client)
