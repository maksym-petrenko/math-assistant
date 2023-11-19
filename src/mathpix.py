import requests
import json
from config import mathpix_credentials


def image_to_tex(img_path: str) -> str:
    """Use Mathpix API to get TeX code of math formulas on the image."""
    r = requests.post(
        "https://api.mathpix.com/v3/text",
        json={"src": img_path, "math_inline_delimiters": ["$", "$"], "rm_spaces": True},
        headers={
            "app_id": mathpix_credentials.APP_ID,
            "app_key": mathpix_credentials.APP_KEY,
            "Content-type": "application/json",
        },
    )

    return json.dumps(r.json(), indent=4, sort_keys=True)
