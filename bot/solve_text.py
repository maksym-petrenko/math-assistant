from telethon import events

from wolfram.helper import get_step_by_step_solution_image_only

from .config import bot


@bot.on(events.NewMessage(incoming=True, func=lambda event: event.raw_text != ''))
async def solve_text(msg: events.NewMessage) -> None:
    image_url = await get_step_by_step_solution_image_only(msg.raw_text)
    print(msg.raw_text, '->', image_url)

    if image_url is None:
        await msg.reply('Something went wrong')
        return

    await msg.reply(file=image_url, force_document=False)
