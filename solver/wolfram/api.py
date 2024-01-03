from urllib.parse import quote_plus

from helper.aiohttp_client import get_client

from .config import credentials
from .types import Pod

base_query = f'http://api.wolframalpha.com/v2/query?appid={credentials.APP_ID}'


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
