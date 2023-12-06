from typing import Literal
from urllib.parse import parse_qsl, quote_plus, urlencode, urlparse

from helper.aiohttp_client import get_client

from .config import credentials

base_query = f'http://api.wolframalpha.com/v2/query?appid={credentials.APP_ID}'


POSSIBLE_FORMATS = Literal['image', 'imagemap', 'plaintext', 'MathML', 'Sound', 'wav']

# returns list of pods
async def get_step_by_step_solution(query: str, output_format: POSSIBLE_FORMATS) -> list | None:
    query = quote_plus(query)

    pod_data = 'podstate=Step-by-step solution'
    url = f'{base_query}&input={query}&format={output_format}&output=json&{pod_data}'

    client = await get_client()
    async with client.get(url, timeout=5) as response:
        if not response.ok:
            print('Error fetching response from Wolfram Alpha')
            return None

        result = (await response.json())['queryresult']

    if not result['success']:
        return None

    solution = result['pods']

    # find probable step-by-step solution
    for subpod in solution:
        for pod in subpod['subpods']:
            if 'steps' not in pod['title']:
                continue

            return [pod]

    return [subpod['subpods'][0] for subpod in solution]


def patch_query(url: str, **kwargs: str) -> str:
    return urlparse(url)._replace(query=urlencode(dict(parse_qsl(urlparse(url).query), **kwargs))).geturl()


# returns list of URLs to images with step-by-step solution
async def get_step_by_step_solution_image_only(query: str, image_type: str = 'jpg') -> list[str] | None:
    pods = await get_step_by_step_solution(query, 'image')
    if pods is None:
        return None

    urls = [pod['img']['src'] for pod in pods]

    return [patch_query(url, MSPStoreType='image/' + image_type) for url in urls]
