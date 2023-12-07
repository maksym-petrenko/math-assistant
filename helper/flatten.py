def make_flat(lst: list) -> list:
    return [item for sublist in lst for item in sublist]
