from telethon import events

from helper.download import download
from mathpix.helper import image_to_latex

from .config import bot
from .helper import generate_code
from .solver import Response, solve


async def respond_to_message(msg: events.NewMessage, response: Response) -> None:
    if response.debug:
        await msg.reply(response.debug)
    if response.exception:
        await msg.reply(response.exception)
    else:
        await msg.reply(file=[await download(image, 'solution.jpg') for image in response.solution], force_document=True)


async def solve_image(image: bytes) -> Response:
    latex: str | None = await image_to_latex(image)
    if latex is None:
        return Response(exception="Can't extract problem from the photo, try to send another one")

    solution = await solve(latex)
    solution.debug = generate_code(latex, 'LaTeX') + '\n\n' + solution.debug
    return solution


@bot.on(events.NewMessage(incoming=True, func=lambda event: event.photo is not None))
async def solve_image_handler(msg: events.NewMessage) -> None:
    image = await msg.download_media(bytes)
    solution = await solve_image(image)
    await respond_to_message(msg, solution)


@bot.on(events.NewMessage(incoming=True, func=lambda event: event.raw_text != ''))
async def solve_text_handler(msg: events.NewMessage) -> None:
    solution = await solve(msg.raw_text)
    await respond_to_message(msg, solution)
