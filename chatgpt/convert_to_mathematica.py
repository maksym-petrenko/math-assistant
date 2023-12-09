from .config import client


with open("chatgpt/instructions/mathematica.txt") as f:
    contents = f.readlines()
    PROMPT = ""
    for line in contents:
        PROMPT += line


async def convert(latex: str) -> str | None:
    print(latex)

    messages = [{'role': 'system', 'content': PROMPT}, {'role': 'user', 'content': latex}]
    response = await client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,  # type: ignore[arg-type]
        temperature=0,
    )

    answer = response.choices[0].message.content

    print(answer)
    if answer == 'None':
        return None
    return answer
