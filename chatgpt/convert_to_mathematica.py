from .config import client

PROMPT = 'Convert LaTex to wolfram mathematica language'


async def convert(latex: str) -> str | None:
    messages = [{'role': 'system', 'content': PROMPT}, {'role': 'user', 'content': latex}]
    response = await client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,  # type: ignore[arg-type]
        temperature=0,
    )

    return response.choices[0].message.content
