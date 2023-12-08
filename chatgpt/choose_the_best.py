from wolfram.helper import Pod

from .config import client

PROMPT = r"""
You are given a question(may contain LaTeX) and Wolfram Alpha response categories.
Try to find the best category for the given question.

If you are given a function then user probably wants a plot.

Examples with only question and output WITHOUT categories:
Input: x^2 + 3x = 2
Output: Results

Input: graph me 2x + 3
Output: Plot

Input: \log _{0,1}(x-5)^{2}+\log _{0,1}(x-2) \geqslant-1
Output: Results

Input: \operatorname{Rank}\left[\begin{array}{ccc}1 & 2 & 3 \\ 2 & 1 & -2 \\ 4 & 5 & 4 \\ 1 & 3 & 4\end{array}\right]
Output: Results
"""


async def choose(question: str, pods: list) -> Pod | None:
    if len(pods) == 0:  # small shortcut
        return None

    # use subpod proposed by wolfram
    for pod in pods:
        if pod.get('primary', False):
            return pod

    # in other way use subpod chosen by ChatGPT
    categories = [pod['title'] for pod in pods]
    text = f'Question:\n{question}\nCategories:\n' + '\n'.join(categories)

    messages = [{'role': 'system', 'content': PROMPT}, {'role': 'user', 'content': text}]
    response = await client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,  # type: ignore[arg-type]
        temperature=0,
    )

    answer = response.choices[0].message.content
    for pod in pods:
        if pod['title'] == answer:
            return pod

    return None
