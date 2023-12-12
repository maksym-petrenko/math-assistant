from typing import Literal

from .config import SEED, client
from .helper import read_prompt

prompt2file = {
    'Classify': read_prompt('classifier'),
    'Wolfram': read_prompt('mathematica'),
    'Solve': read_prompt('gpt_solver'),
}


async def gpt(message: str, request_type: Literal['Classify', 'Solve', 'Wolfram']) -> str | None:
    """Interact with ChatGPT API."""

    #  transform the task type to filename with relevant prompt
    prompt = prompt2file[request_type]
    model = 'gpt-4' if request_type == 'Solve' else 'gpt-3.5-turbo'

    messages = [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': message}]

    response = await client.chat.completions.create(
        model=model,
        messages=messages,  # type: ignore[arg-type]
        seed=SEED,
        temperature=0,
        top_p=0,
    )

    answer = response.choices[0].message.content
    print(f'message {answer}')

    return answer
