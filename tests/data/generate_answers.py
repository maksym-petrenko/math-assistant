import argparse
import asyncio
import json
from pathlib import Path
from typing import Any

from helper.aiohttp_client import stop as stop_client
from helper.main_handler import main_handler
from tests.test_helper import question2pods

data_path = Path(__file__).parent

force_regenerate: bool

# only generates if there no answer yet
async def generate_answer(test: dict[str, Any]) -> Any:
    question = test['question']
    if 'answer' in test and not force_regenerate:
        print('skipping:', question)
        return test['answer']

    print('generating for:', question)
    return await question2pods(question)


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
    parser = argparse.ArgumentParser(
        prog='Answer generator',
        description='Generates answers for tests',
    )
    parser.add_argument('--force', action='store_true', help='forces to regenerate already existing answers')
    args = parser.parse_args()
    force_regenerate = args.force

    main_handler(main, None, stop_client)
