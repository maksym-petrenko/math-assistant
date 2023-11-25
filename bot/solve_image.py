from telethon import events

from mathpix.helper import image_to_mathematica
from wolfram.helper import get_step_by_step_solution_image_only

from .config import bot


@bot.on(events.NewMessage(incoming=True, func=lambda event: event.photo is not None))
async def solve_image(msg: events.NewMessage) -> None:
    image = await msg.download_media(bytes)
    query = await image_to_mathematica(image)  # TODO: validate response

    image_url = await get_step_by_step_solution_image_only(query)
    print('Wolfram:', query, '->', image_url)

    if image_url is None:
        await msg.reply('Something went wrong')
        return

    await msg.reply(file=image_url, force_document=False)
