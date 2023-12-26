from fastapi import FastAPI

from .responses import AnyResponse
from .solver import solve as inner_solve

app = FastAPI()


@app.get('/solve')
async def solve(question: str) -> AnyResponse:
    # TODO: add image support
    return await inner_solve(question)
