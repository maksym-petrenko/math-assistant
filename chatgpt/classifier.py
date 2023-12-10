from .config import client
from .helper import read_prompt

PROMPT = read_prompt('classifier')


async def classify(latex: str) -> str | None:
    """Returns one of the following options: {None, Wolfram, GPT}."""

    messages = [{'role': 'system', 'content': PROMPT}, {'role': 'user', 'content': latex}]
    response = await client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,  # type: ignore[arg-type]
        temperature=0,
    )

    answer = response.choices[0].message.content

    print({'input': latex, 'action': answer})

    return answer
