from typing import Literal

from .config import SEED, client
from .helper import read_prompt

prompt2file = {
    'Classify': {
        'prompt': read_prompt('classifier'),
        'model': 'gpt-3.5-turbo',
        },
    'Wolfram': {
        'prompt': read_prompt('mathematica'),
        'model': 'gpt-3.5-turbo',
        },
    'Solve': {
        'prompt': read_prompt('gpt_solver'),
        'model': 'gpt-4',
        },
}


async def gpt(message: str, request_type: Literal['Classify', 'Solve', 'Wolfram']) -> str | None:
    """Interact with ChatGPT API."""

    #  get prompt and model suitable for the task type
    prompt, model = prompt2file[request_type].values()

    messages = [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': message}]

    response = await client.chat.completions.create(
        model=model,
        messages=messages,  # type: ignore[arg-type]
        seed=SEED,
        temperature=0,
        top_p=0,
    )

    return response.choices[0].message.content
