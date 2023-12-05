import pytest

from helper.aiohttp_client import stop


@pytest.fixture(autouse=True)
async def _cleanup() -> None:
    try:
        yield
    finally:
        await stop()
