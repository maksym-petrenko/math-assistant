from io import BytesIO
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse

from telethon import events

from helper.download import download
from helper.flatten import make_flat
from solver import ErrorResponse, GPTResponse, Response, WolframResponse, solve
from solver.wolfram import Pod, extract_usefull_subpods

from .config import bot
from .markup_code import generate_code


def patch_query(url: str, **kwargs: str) -> str:
    return urlparse(url)._replace(query=urlencode(dict(parse_qsl(urlparse(url).query), **kwargs))).geturl()


def extract_image(subpod: Any) -> str:
    return patch_query(subpod.img['src'], MSPStoreType='image/jpg')


async def download_images(pod: Pod) -> list[BytesIO]:
    subpods = extract_usefull_subpods(pod)
    return [await download(extract_image(pod), 'solution.jpg') for pod in subpods]


async def respond_wolfram(msg: events.NewMessage, response: WolframResponse) -> None:
    debug = ''
    if response.image_text is not None:  # still could be empty
        debug += generate_code(response.image_text, 'LaTeX') + '\n\n'
    if response.wolfram_prompt:
        debug += generate_code(response.wolfram_prompt, 'Mathematica') + '\n\n'

    if debug:
        await msg.reply('Debug:\n' + debug)

    if response.best_solution:
        await msg.reply(
            'The best answer',
            file=await download_images(response.best_solution),
            force_document=True,
        )
    else:
        await msg.reply('No best answer :(')

    await msg.reply('All answers', file=make_flat([await download_images(pod) for pod in response.all_solutions]), force_document=True)

async def respond_to_message(msg: events.NewMessage, response: Response) -> None:
    match response:
        case ErrorResponse():
            await msg.reply(response.error)
        case WolframResponse():
            await respond_wolfram(msg, response)
        case GPTResponse():
            await msg.reply(response.answer)


@bot.on(events.NewMessage(incoming=True, func=lambda event: event.photo is not None))  # type: ignore[misc]
async def solve_image_handler(msg: events.NewMessage) -> None:
    image = await msg.download_media(bytes)
    solution = await solve(msg.raw_text, image)
    await respond_to_message(msg, solution)


@bot.on(events.NewMessage(incoming=True, func=lambda event: event.raw_text != '' and event.photo is None))  # type: ignore[misc]
async def solve_text_handler(msg: events.NewMessage) -> None:
    solution = await solve(msg.raw_text)
    await respond_to_message(msg, solution)
