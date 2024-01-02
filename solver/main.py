from fastapi import FastAPI, Form, UploadFile

from .responses import AnyResponse
from .solver import solve as inner_solve

app = FastAPI()


@app.post('/solve')
async def solve(question: str = Form(''), image: UploadFile | None = None) -> AnyResponse:
    image_bytes = await image.read() if image else None
    return await inner_solve(question, image_bytes)
