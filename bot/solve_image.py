from telethon import events

from mathpix.helper import image_to_latex
from wolfram.helper import get_step_by_step_solution_image_only

from .config import bot


@bot.on(events.NewMessage(incoming=True, func=lambda event: event.photo is not None))
async def solve_image(msg: events.NewMessage) -> None:
    image = await msg.download_media(bytes)
    latex = image_to_latex(image)  # TODO: validate latex response

    url = get_step_by_step_solution_image_only(latex)
    print('LaTeX:', latex, '->', url)

    if url is None:
        await msg.reply('Something went wrong')
        return

    await msg.reply(file=url, force_document=False)
