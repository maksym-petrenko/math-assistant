from collections.abc import AsyncGenerator

import pytest

from helper.aiohttp_client import stop_client


@pytest.fixture(autouse=True)
async def _cleanup() -> AsyncGenerator[None, None]:
    try:
        yield
    finally:
        await stop_client()
