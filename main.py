import urllib
from typing import Any

import requests

from config import credentials

base_query = f'http://api.wolframalpha.com/v2/query?appid={credentials.APP_ID}'


# returns pod
def get_step_by_step_solution(query: str) -> Any | None:
    query = 'Solve: ' + urllib.parse.quote_plus(query)

    pod_data = 'includepodid=Result&podstate=Step-by-step solution'
    url = f'{base_query}&input={query}&format=image&output=json&{pod_data}'

    response = requests.get(url, timeout=5)
    if not response.ok:
        print('Error fetching response from Wolfram Alpha')
        return None

    response = response.json()['queryresult']

    assert response['numpods'] == 1
    solution = response['pods'][0]

    for pod in solution['subpods']:
        if 'steps' not in pod['title']:
            continue

        return pod
    return None


pod = get_step_by_step_solution('x^3 + x^2 + x = 3')
print(pod['img']['src'])
