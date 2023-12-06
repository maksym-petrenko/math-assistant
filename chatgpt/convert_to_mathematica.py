from .config import client

PROMPT = r"""
If the formula is already in mathematica, return it only.

Your response must contain a formula only, description text and other explanations are forbidden.
You must identify the intention of the formula's author.
For example, if infinite sum is expressed, you should give wolfram instructions
to find out whether it converges and if yes, to calculate the sum.
If possible, apply Solve to it, but only if it makes sense.
Convert the following text to Wolfram Mathematica language.
Please, make sure it can be processed by Wolfram.

In case there is a function without any equations, please, give raw output so that Wolfram can provide general information about it.
Make sure that all of the variables and functions are spelled correctly and don't contain unnecessary ^ or _

Only if case the input is invalid and doesn't contain any formulas, you have to respond with the only word "None".
You must answer with the formula only. Here are some examples:

Input: x^{3}-12 x^{2}+19 x+8=0
Output: Solve[x^3 - 12 x^2 + 19 x + 8 == 0, x]

Input: \operatorname{Rank}\left[\begin{array}{ccc}1 & 1 & 1 \\ 1 & 3 & -4 \\ 1 & 7 & 1 \\ 3 & 9 & 11\end{array}\right]
Output: MatrixRank[{{1, 1, 1}, {1, 3, -4}, {1, 7, 1}, {3, 9, 11}}]

Input: \sum_{n=1}^{\infty}\left(\cos \frac{1}{n} \sin \frac{1}{n}\right).
Output: Sum[Cos[1/n] Sin[1/n], {n, 1, Infinity}]

Input: \sum_{x=1}^{12} x^{k}=k
Output: Sum[x^k, {x, 1, 12}] = k

Input: f(x)=\left\{\begin{array}{ll}\sin(x) & \text { if } x=0 \\ 2 x & \text { if } x \neq \cos(x)\end{array}\right
Output: f[x] := Piecewise[{{Sin(x), x = 0}, {Cos(x), Unequal[x, 0]}}]
"""


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
