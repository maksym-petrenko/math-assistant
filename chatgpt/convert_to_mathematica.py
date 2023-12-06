from .config import client

PROMPT = r"""
If the formula is already in wolfram alpha, return it only.

Your response must contain a formula only, description text and other explanations are forbidden.
You must identify the intention of the formula's author.
For example, if infinite sum is expressed, you should give wolfram instructions
to find out whether it converges and if yes, to calculate the sum.

Input: \sum_{n=1}^{\infty}\left(\cos \frac{1}{n} \sin \frac{1}{n}\right).
Output: Sum[Cos[1/n] Sin[1/n], {n, 1, Infinity}]

Input: \sum_{n=1}^{\infty}\left(\frac{1}{n+1}-\frac{1}{n}\right)
Output: Sum[1/(n + 1) - 1/n, {n, 1, Infinity}]

If possible, apply Solve to it, but only if it makes sense.
Convert the following text to Wolfram Alpha prompt.
Please, make sure it can be processed by Wolfram Alpha.

Input: x^{3}-12 x^{2}+19 x+8=0
Output: Solve[x^3 - 12 x^2 + 19 x + 8 == 0, x]

Input: \log _{0,1}(x-5)^{2}+\log _{0,1}(x-2) \geqslant-1
Output: Solve[Log[0.1, (x - 5)^2] + Log[0.1, x - 2] >= -1, x]

In case there is a function without any equations, please, respond with only function body
so that Wolfram Alpha can provide general information about it.

Input: f(x)=\left\{\begin{array}{ll}\sin(x) & \text { if } x=0 \\ 2 x & \text { if } x \neq \cos(x)\end{array}\right
Output: Piecewise[{{Sin(x), x = 0}, {Cos(x), Unequal[x, 0]}}]

Input: cool\_function(t)=\left\{\begin{array}{ll}t^{2} & \text { if } t<0 \\ 2 t & \text { if } t \geq 0\end{array}\right.
Output: Piecewise[{{t^2, t < 0}, {2t, t >= 0}}]

Some other examples:

Input: \operatorname{Rank}\left[\begin{array}{ccc}1 & 1 & 1 \\ 1 & 3 & -4 \\ 1 & 7 & 1 \\ 3 & 9 & 11\end{array}\right]
Output: MatrixRank[{{1, 1, 1}, {1, 3, -4}, {1, 7, 1}, {3, 9, 11}}]

Input: \sum_{x=1}^{12} x^{k}=k
Output: Sum[x^k, {x, 1, 12}] = k

If the input is invalid or user doesn't provided any mathematical problem,
you should respond with the only word "None".

Input: some garbage
Output: None

Input: Help me with some math, pls
Output: None

Input: Generate random problem and solve it
Output: None
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
