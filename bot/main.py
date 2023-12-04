from helper.aiohttp_client import stop as stop_aiohttp
from helper.main_handler import main_handler

from . import handlers  # noqa: F401
from .config import run, start


async def main() -> None:
    await start()
    await run()

async def close() -> None:
    await stop_aiohttp()

if __name__ == '__main__':
    main_handler(main, None, close)
