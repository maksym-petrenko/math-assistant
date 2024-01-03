from typing import Literal

from pydantic import BaseModel

from .config import SEED, client
from .helper import read_prompt

PROBLEM_TYPES = Literal['Classify', 'Solve', 'Wolfram']
MODELS = Literal['gpt-3.5-turbo', 'gpt-4']


class PromptInfo(BaseModel):
    prompt: str
    model: MODELS


PROMPT2INFO = {
    'Classify': PromptInfo(
        prompt=read_prompt('classifier'),
        model='gpt-3.5-turbo',
    ),
    'Wolfram': PromptInfo(
        prompt=read_prompt('mathematica'),
        model='gpt-3.5-turbo',
    ),
    'Solve': PromptInfo(
        prompt=read_prompt('gpt_solver'),
        model='gpt-4',
    ),
}


async def gpt(message: str, request_type: PROBLEM_TYPES) -> str | None:
    """Interact with ChatGPT API."""

    #  get prompt and model suitable for the task type
    info = PROMPT2INFO[request_type]

    messages = [{'role': 'system', 'content': info.prompt}, {'role': 'user', 'content': message}]

    response = await client.chat.completions.create(
        model=info.model,
        messages=messages,  # type: ignore[arg-type]
        seed=SEED,
        temperature=0,
        top_p=0,
    )

    return response.choices[0].message.content
