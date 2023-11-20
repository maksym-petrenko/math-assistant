import aiohttp

_client: aiohttp.ClientSession | None = None

# use current event loop
async def get_client() -> None:
    global _client
    if _client is None:
        _client = aiohttp.ClientSession()
    return _client


async def stop() -> None:
    if _client is not None:
        await _client.close()
