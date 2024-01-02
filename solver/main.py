from typing import Annotated

from fastapi import FastAPI, File, Form

from .responses import AnyResponse
from .solver import solve as inner_solve

app = FastAPI()


@app.post('/solve')
async def solve(question: Annotated[str, Form()], image: Annotated[bytes | None, File()] = None) -> AnyResponse:
    return await inner_solve(question, image)
