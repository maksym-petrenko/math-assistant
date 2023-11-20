from telethon import events

from wolfram.helper import get_step_by_step_solution_image_only

from .config import bot


@bot.on(events.NewMessage(incoming=True, func=lambda event: event.text is not None))
async def solve_text(msg: events.NewMessage) -> None:
    url = get_step_by_step_solution_image_only(msg.text)
    print(msg.text, '->', url)

    if url is None:
        await msg.reply('Something went wrong')
        return

    await msg.reply(file=url, force_document=False)
