from typing import Any

from pydantic import BaseModel, ValidationError, model_validator

from solver import WolframResponse
from wolfram import Pod, Subpod, extract_usefull_subpods


class SerializedSubpod(BaseModel):
    plaintext: str


def serealize_subpods(subpods: list[Subpod]) -> list[SerializedSubpod]:
    return [SerializedSubpod.model_validate(subpod, from_attributes=True) for subpod in subpods]


class SerializedPod(BaseModel):
    all_subpods: list[SerializedSubpod]
    usefull_subpods: list[SerializedSubpod]

    @model_validator(mode='before')
    @classmethod
    def from_pod(cls, data: Any) -> Any:
        if isinstance(data, Pod):
            return {
                'all_subpods': serealize_subpods(data.subpods),
                'usefull_subpods': serealize_subpods(extract_usefull_subpods(data)),
            }
        return data


# patch the original response
class SerializedWolfram(WolframResponse):
    all_solutions: list[SerializedPod]  # type: ignore[assignment]
    best_solution: SerializedPod | None  # type: ignore[assignment]


def serialize(response: WolframResponse) -> dict[str, Any]:
    return SerializedWolfram.model_validate(response, from_attributes=True).model_dump()


def validate(data: dict[str, Any]) -> bool:
    if data.get('type') != 'Wolfram':
        print('Wrong response was passed into validate(wolfram)')
        return False

    try:
        SerializedWolfram.model_validate(data, strict=True)
        return True
    except ValidationError:
        return False
