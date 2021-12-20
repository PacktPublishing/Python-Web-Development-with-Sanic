from typing import Any, NamedTuple, Type
from sanic import Blueprint, Request, json

bp = Blueprint("Something", url_prefix="/some")


class ExpectedTypes(NamedTuple):
    a_string: str
    an_int: int


def _check(exists: bool, value: Any, expected: Type[object]):
    if not exists:
        return "MISSING"
    return "OK" if type(value) is expected else "WRONG"


@bp.post("/validation")
async def check_types(request: Request):
    valid = {
        field_name: _check(
            field_name in request.json, request.json.get(field_name), field_type
        )
        for field_name, field_type in ExpectedTypes.__annotations__.items()
    }
    status = (
        200
        if all(value == "OK" for value in valid.values())
        and len(request.json) == len(ExpectedTypes.__annotations__)
        else 400
    )
    return json(valid, status=status)
