from typing import Any

from helper.aiohttp_client import get_client

from .responses import Response, deserialize


async def solve(question: str, image: bytes | None = None) -> Response:
    client = await get_client()

    data: dict[str, Any] = {'question': question}
    if image is not None:
        data['image'] = image

    # FIXME: remove hardcoded url part
    async with client.post('http://solver/solve', data=data) as response:
        return deserialize(await response.json())
