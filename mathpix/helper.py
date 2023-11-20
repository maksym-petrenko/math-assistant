import json

import requests

from .config import credentials

API = 'https://api.mathpix.com/v3/text'

def image_to_tex(img_path: str) -> str:
    """Use Mathpix API to get TeX code of math formulas on the image."""
    r = requests.post(
        API,
        json={'src': img_path, 'math_inline_delimiters': ['$', '$'], 'rm_spaces': True},
        headers={
            'app_id': credentials.APP_ID,
            'app_key': credentials.APP_KEY,
            'Content-type': 'application/json',
        },
        timeout=5,
    )

    return json.dumps(r.json(), indent=4, sort_keys=True)
