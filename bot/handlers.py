from io import BytesIO
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse

from telethon import events

from helper.download import download
from helper.flatten import make_flat
from mathpix.helper import image_to_latex
from wolfram.helper import Pod, extract_usefull_subpods

from .config import bot
from .helper import generate_code
from .solver import Response, solve


def patch_query(url: str, **kwargs: str) -> str:
    return urlparse(url)._replace(query=urlencode(dict(parse_qsl(urlparse(url).query), **kwargs))).geturl()


def extract_image(subpod: Any) -> str:
    return patch_query(subpod.img['src'], MSPStoreType='image/jpg')


async def download_images(pod: Pod) -> list[BytesIO]:
    subpods = extract_usefull_subpods(pod)
    return [await download(extract_image(pod), 'solution.jpg') for pod in subpods]


async def respond_to_message(msg: events.NewMessage, response: Response) -> None:
    if response.debug:
        await msg.reply(response.debug)

    if response.exception:
        await msg.reply(response.exception)
        return

    if response.best_solution:
        await msg.reply('The best answer', file=await download_images(response.best_solution), force_document=True)
    else:
        await msg.reply('No best answer :(')

    await msg.reply('All answers', file=make_flat([await download_images(pod) for pod in response.all_solutions]), force_document=True)


async def solve_image(image: bytes) -> Response:
    latex: str | None = await image_to_latex(image)
    if latex is None:
        return Response(original_question='', exception="Can't extract problem from the photo, try to send another one")

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
