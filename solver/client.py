from helper.aiohttp_client import get_client

from .responses import Response, deserialize


async def solve(question: str) -> Response:
    client = await get_client()
    # FIXME: remove hardcoded url part
    async with client.get('http://solver/solve', params={'question': question}) as response:
        return deserialize(await response.json())
