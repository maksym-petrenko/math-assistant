from typing import Any, Literal
from urllib.parse import parse_qsl, quote_plus, urlencode, urlparse

import requests

from .config import credentials

base_query = f'http://api.wolframalpha.com/v2/query?appid={credentials.APP_ID}'


POSSIBLE_FORMATS = Literal['image', 'imagemap', 'plaintext', 'MathML', 'Sound', 'wav']

# returns pod
def get_step_by_step_solution(query: str, output_format: POSSIBLE_FORMATS) -> Any | None:
    query = 'Solve: ' + quote_plus(query)

    pod_data = 'includepodid=Result&podstate=Step-by-step solution'
    url = f'{base_query}&input={query}&format={output_format}&output=json&{pod_data}'

    response = requests.get(url, timeout=5)
    if not response.ok:
        print('Error fetching response from Wolfram Alpha')
        return None

    response = response.json()['queryresult']

    if response['numpods'] != 1:
        return None

    solution = response['pods'][0]

    for pod in solution['subpods']:
        if 'steps' not in pod['title']:
            continue

        return pod
    return None


def patch_query(url: str, **kwargs: str) -> str:
    return urlparse(url)._replace(query=urlencode(dict(parse_qsl(urlparse(url).query), **kwargs))).geturl()


# returns URL to image with step by step solution
def get_step_by_step_solution_image_only(query: str, image_type: str = 'jpg') -> str | None:
    pod = get_step_by_step_solution(query, 'image')
    if pod is None:
        return None

    url = pod['img']['src']
    return patch_query(url, MSPStoreType='image/' + image_type)
