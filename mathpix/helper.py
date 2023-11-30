import json

from chatgpt.convert_to_mathematica import convert
from helper.aiohttp_client import get_client

from .config import credentials

API = 'https://api.mathpix.com/v3/text'

async def image_to_mathematica(image: bytes) -> str | None:
    """Use Mathpix API to get mathematica code of math formulas on the image."""

    client = await get_client()
    request = client.post(
        API,
        data={
            'file': image,
            'options_json': json.dumps({
                'math_inline_delimiters': ['', ''],
                'rm_spaces': True,
            }),
        },
        headers={
            'app_id': credentials.APP_ID,
            'app_key': credentials.APP_KEY,
        },
        timeout=5,
    )

    async with request as response:
        latex = (await response.json())['text']
        print(latex)

    return await convert(latex)
