from wolfram.api import Pod

from .config import client
from .helper import read_prompt

PROMPT = read_prompt('choose_pod')


async def choose(question: str, pods: list[Pod]) -> Pod | None:
    if len(pods) == 0:  # small shortcut
        return None

    # use subpod proposed by wolfram
    for pod in pods:
        if pod.primary:
            return pod

    # in other way use subpod chosen by ChatGPT
    categories = [pod.title for pod in pods]
    text = f'Question:\n{question}\nCategories:\n' + '\n'.join(categories)

    messages = [{'role': 'system', 'content': PROMPT}, {'role': 'user', 'content': text}]
    response = await client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,  # type: ignore[arg-type]
        temperature=0,
    )

    answer = response.choices[0].message.content
    for pod in pods:
        if pod.title == answer:
            return pod

    return None
