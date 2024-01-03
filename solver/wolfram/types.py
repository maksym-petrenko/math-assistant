from typing import Any

from pydantic import BaseModel


class Subpod(BaseModel):
    title: str
    plaintext: str
    img: dict[str, Any]  # TODO: add typing


class Pod(BaseModel):
    subpods: list[Subpod]
    id: str
    title: str
    primary: bool = False
