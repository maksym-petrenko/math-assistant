from typing import TypeVar

# TODO: wait until mypy supports python3.12
T = TypeVar('T')


def make_flat(lst: list[list[T]]) -> list[T]:
    return [item for sublist in lst for item in sublist]
