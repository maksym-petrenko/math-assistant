def serealize(pods: list) -> list[str]:
    return [pod['img']['alt'] for pod in pods]
