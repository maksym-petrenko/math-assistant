from .config import client

PROMPT = """
Your response must contain a formula only, description text and other explanations are forbidden.
You must identify the intention of the formula's author.
For example, if infinite sum is expressed, you should give wolfram instructions
to find out whether it converges and if yes, to calculate the sum.
Convert the following text to Wolfram Mathematica language
If you can't transform this LaTeX to mathematica, you must reply with the only word: None.
"""


async def convert(latex: str) -> str | None:
    messages = [{'role': 'system', 'content': PROMPT}, {'role': 'user', 'content': latex}]
    response = await client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,  # type: ignore[arg-type]
        temperature=0,
    )

    return response.choices[0].message.content
