from .config import SEED, client
from .helper import read_prompt

PROMPT = read_prompt('mathematica')


async def convert(latex: str) -> str | None:
    print(latex)

    messages = [{'role': 'system', 'content': PROMPT}, {'role': 'user', 'content': latex}]
    response = await client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,  # type: ignore[arg-type]
        seed=SEED,
        temperature=0,
    )

    answer = response.choices[0].message.content

    print(answer)
    if answer == 'None':
        return None
    return answer
