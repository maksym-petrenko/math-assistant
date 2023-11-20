import urllib
import requests
from typing import Any
from config import wolfram_credentials

base_query = f"http://api.wolframalpha.com/v2/query?appid={wolfram_credentials.APP_ID}"


def get_step_by_step_solution(query: str) -> Any | None:
    """Return pod."""
    query = "Solve: " + urllib.parse.quote_plus(query)

    pod_data = "includepodid=Result&podstate=Step-by-step solution"
    url = f"{base_query}&input={query}&format=image&output=json&{pod_data}"

    response = requests.get(url, timeout=5)
    if not response.ok:
        return None

    response = response.json()["queryresult"]

    assert response["numpods"] == 1
    solution = response["pods"][0]

    for pod in solution["subpods"]:
        if "steps" not in pod["title"]:
            continue
        return pod
    return None
