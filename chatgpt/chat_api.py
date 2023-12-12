from .config import SEED, client
from .helper import read_prompt

prompt2file = {
    'Classify': read_prompt('classifier'),
    'Wolfram': read_prompt('mathematica'),
    'Solve': read_prompt('gpt_solver'),
}


async def gpt(message: str, request_type: str, model: str = 'gpt-3.5-turbo') -> str:
    """Interact with ChatGPT API."""

    #  transform the task type to filename with relevant prompt
    prompt = prompt2file[request_type]

    messages = [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': message}]

    response = await client.chat.completions.create(
        model=model,
        messages=messages,  # type: ignore[arg-type]
        seed=SEED,
        temperature=0,
    )

    answer = response.choices[0].message.content
    print(f'message {answer}')

    return str(answer)
