from telethon import events

from chatgpt.convert_to_mathematica import convert
from mathpix.helper import image_to_latex
from wolfram.helper import get_step_by_step_solution_image_only

from .config import bot
from .helper import generate_code


@bot.on(events.NewMessage(incoming=True, func=lambda event: event.photo is not None))
async def solve_image(msg: events.NewMessage) -> None:
    image = await msg.download_media(bytes)
    latex: str = await image_to_latex(image)  # type: ignore[assignment]  # TODO: validate response

    mathematica: str = await convert(latex)  # type: ignore[assignment]  # TODO: validate response

    debug_message = generate_code(latex, 'LaTeX') + '\n\n'
    debug_message += generate_code(mathematica, 'mathematica')
    await msg.reply(debug_message)

    image_url = await get_step_by_step_solution_image_only(mathematica)

    if image_url is None:
        await msg.reply('Something went wrong')
        return

    for image in image_url:
        await msg.reply(file=image, force_document=False)
