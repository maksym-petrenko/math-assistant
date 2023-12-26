import copy
from typing import Any

from pydantic import BaseModel, ValidationError, model_validator

from solver import WolframResponse, deserialize
from wolfram import Pod, Subpod, extract_usefull_subpods


def serialize_subpod(subpod: Subpod) -> str:
    return subpod.plaintext


def serialize_subpods(subpods: list[Subpod]) -> list[str]:
    return [serialize_subpod(subpod) for subpod in subpods]


class SerializedPod(BaseModel):
    all_subpods: list[str]
    usefull_subpods: list[str]

    @model_validator(mode='before')
    @classmethod
    def from_pod(cls, data: Any) -> Any:
        if isinstance(data, Pod):
            return {
                'all_subpods': serialize_subpods(data.subpods),
                'usefull_subpods': serialize_subpods(extract_usefull_subpods(data)),
            }
        return data


def serialize_pod(pod: Pod | None) -> dict[str, Any]:
    return SerializedPod.model_validate(pod).model_dump()


def serialize(response: WolframResponse) -> dict[str, Any]:
    result = response.model_dump()
    result['best_solution'] = serialize_pod(response.best_solution)
    result['all_solutions'] = [serialize_pod(pod) for pod in response.all_solutions]
    return result


def validate_pod(data: dict[str, Any]) -> bool:
    try:
        SerializedPod.model_validate(data)
        return True
    except ValidationError:
        return False


def validate(data: dict[str, Any]) -> bool:
    if data.get('type') != 'Wolfram':
        print('Wrong response was passed into validate(wolfram)')
        return False

    # validate pods
    try:
        if not all(validate_pod(pod) for pod in data['all_solutions']):
            return False

        best_solution = data['best_solution']
        if best_solution is not None and not validate_pod(best_solution):
            return False
    except (KeyError, TypeError):
        return False

    # validate other parts
    try:
        # set pods to default values, because validated previously
        data = copy.deepcopy(data)
        data['all_solutions'] = []
        data['best_solution'] = None

        deserialize(data)
        return True
    except ValidationError:
        return False
