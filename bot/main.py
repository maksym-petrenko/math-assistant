import asyncio

from . import solve_image, solve_text  # noqa: F401
from .config import run, start


async def main() -> None:
    await start()
    await run()

if __name__ == '__main__':
    asyncio.run(main())
