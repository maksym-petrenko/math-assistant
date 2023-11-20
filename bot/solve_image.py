from io import BytesIO

from telethon import events

from .config import bot


@bot.on(events.NewMessage(incoming=True, func=lambda event: event.photo is not None))
async def solve_image(msg: events.NewMessage) -> None:
    buffer = BytesIO(await msg.download_media(bytes))  # noqa: F841
    await msg.respond('Not implemented')
