from io import BytesIO

from .aiohttp_client import get_client


async def download(url: str, name: str) -> BytesIO:
    client = await get_client()
    async with client.get(url) as response:
        io = BytesIO(await response.read())
        io.name = name
        return io
