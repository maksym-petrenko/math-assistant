from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, UploadFile

from helper.aiohttp_client import stop_client

from .responses import AnyResponse
from .solver import solve as inner_solve


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await stop_client()

app = FastAPI(lifespan=lifespan)


@app.post('/solve')
async def solve(question: str = Form(''), image: UploadFile | None = None) -> AnyResponse:
    image_bytes = await image.read() if image else None
    return await inner_solve(question, image_bytes)
