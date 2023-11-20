import json

import requests

from .config import credentials

API = 'https://api.mathpix.com/v3/text'

def image_to_latex(image: bytes) -> str:
    """Use Mathpix API to get LaTeX code of math formulas on the image."""
    r = requests.post(
        API,
        files={'file': image},
        data={
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

    return r.json()['text']
