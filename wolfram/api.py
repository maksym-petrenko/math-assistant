from typing import Any
from urllib.parse import quote_plus

from pydantic import BaseModel

from helper.aiohttp_client import get_client

from .config import credentials

base_query = f'http://api.wolframalpha.com/v2/query?appid={credentials.APP_ID}'


class Subpod(BaseModel):
    title: str
    plaintext: str
    img: dict[str, Any]  # TODO: add typing


class Pod(BaseModel):
    subpods: list[Subpod]
    id: str
    primary: bool = False
    title: str


# returns list of pods
async def get_pods(query: str) -> list[Pod] | None:
    query = quote_plus(query)

    pod_data = 'podstate=Step-by-step solution'
    url = f'{base_query}&input={query}&output=json&{pod_data}'

    client = await get_client()
    async with client.get(url, timeout=15) as response:
        if not response.ok:
            print('Error fetching response from Wolfram Alpha')
            return None

        result = (await response.json())['queryresult']

    if not result['success']:
        return None

    print(result)
    return [Pod.model_validate(pod) for pod in result['pods']]


def extract_usefull_subpods(pod: Pod) -> list[Subpod]:
    subpods = pod.subpods

    # remove step-by-step if not available
    subpods = [subpod for subpod in subpods if subpod.plaintext != '(step-by-step solution unavailable)']

    # firstly try to extract subpods with titles
    if with_titles := [subpod for subpod in subpods if subpod.title]:
        return with_titles

    # if no one has a title then return all of them
    return subpods
