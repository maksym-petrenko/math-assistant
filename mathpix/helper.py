import json

from helper.aiohttp_client import get_client

from .config import credentials

API = 'https://api.mathpix.com/v3/text'

async def image_to_latex(image: bytes) -> str:
    """Use Mathpix API to get LaTeX code of math formulas on the image."""

    client = await get_client()
    request = client.post(
        API,
        data={
            'file': image,
            'options_json': json.dumps({
                'math_inline_delimiters': ['$', '$'],
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
        return (await response.json())['text']
