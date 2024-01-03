from typing import Any

from pydantic import BaseModel, model_validator

from solver import WolframResponse
from solver.wolfram import Pod


class SerializedPod(BaseModel):
    id: str

    @model_validator(mode='before')
    @classmethod
    def from_pod(cls, data: Any) -> Any:
        if isinstance(data, Pod):
            return {'id': data.id}
        return data


# patch the original response
class SerializedWolfram(WolframResponse):
    all_solutions: list[SerializedPod]  # type: ignore[assignment]
    best_solution: SerializedPod | None  # type: ignore[assignment]
