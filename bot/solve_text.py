from telethon import events

from chatgpt.convert_to_mathematica import convert
from wolfram.helper import get_step_by_step_solution_image_only

from .config import bot
from .helper import generate_code


@bot.on(events.NewMessage(incoming=True, func=lambda event: event.raw_text != ''))
async def solve_text(msg: events.NewMessage) -> None:
    mathematica: str = await convert(msg.raw_text)  # type: ignore[assignment]  # TODO: validate response

    debug_message = generate_code(mathematica, 'mathematica')
    await msg.reply(debug_message)

    image_url = await get_step_by_step_solution_image_only(mathematica)

    if image_url is None:
        await msg.reply('Something went wrong')
        return

    await msg.reply(file=image_url, force_document=False)
