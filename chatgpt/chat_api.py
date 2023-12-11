from .config import client
from .helper import read_prompt


async def gpt(message: str, request_type: str, model: str = 'gpt-3.5-turbo') -> str:
    """Interact with ChatGPT API."""

    #  transform the task type to filename with relevant prompt
    prompt2file = {
        'Classify': 'classifier',
        'Wolfram': 'mathematica',
        'Solve': 'gpt_solver',
    }

    prompt = read_prompt(prompt2file[request_type])

    messages = [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': message}]

    response = await client.chat.completions.create(
        model=model,
        messages=messages,  # type: ignore[arg-type]
        temperature=0,
    )

    answer = response.choices[0].message.content
    print(f'message {answer}')

    return answer
