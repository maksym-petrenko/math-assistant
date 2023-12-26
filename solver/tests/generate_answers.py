import argparse
import asyncio
import json
from typing import Any

from pydantic import ValidationError

from helper.aiohttp_client import stop_client
from helper.main_handler import main_handler
from solver import deserealize

from .helper import data_path
from .runner import TestData, question_to_test_result

force_regenerate: bool

# only generates if there is no result yet
async def update_result(test: TestData) -> dict[str, Any]:
    question = test['question']

    regenerate = force_regenerate

    # validate previous result
    try:
        deserealize(test.get('result', {}))
    except ValidationError:
        regenerate = True

    if not regenerate:
        print('skipping:', question)
        return test['result']

    print('generating for:', question)
    return await question_to_test_result(question)


async def main() -> None:
    tests = []
    with open(data_path / 'text.json') as text_data:  # noqa: ASYNC101
        tests = json.load(text_data)

    results = await asyncio.gather(*[update_result(test) for test in tests])

    new_tests = []
    for test, result in zip(tests, results, strict=True):
        # generate only necessary fields
        new_tests.append({'question': test['question'], 'result': result})

    with open(data_path / 'text.json', 'w') as text_data:  # noqa: ASYNC101
        json.dump(new_tests, text_data, indent=4)
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
