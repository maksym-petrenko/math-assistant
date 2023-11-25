import json

from helper.aiohttp_client import get_client

from .config import credentials

API = 'https://api.mathpix.com/v3/latex'

async def image_to_mathematica(image: bytes) -> str:
    """Use Mathpix API to get mathematica code of math formulas on the image."""

    client = await get_client()
    request = client.post(
        API,
        data={
            'file': image,
            'options_json': json.dumps({
                'formats': ['wolfram'],
            }),
        },
        headers={
            'app_id': credentials.APP_ID,
            'app_key': credentials.APP_KEY,
        },
    )

    async with request as response:
        return (await response.json())['wolfram']
