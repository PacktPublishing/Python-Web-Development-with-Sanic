from typing import Any, Dict, NamedTuple, Type
from sanic import Blueprint, Request, json
from sanic.exceptions import InvalidUsage
from .some_db_connection import FakeDBConnection
from .some_registration_service import RegistrationService

bp = Blueprint("Registration", url_prefix="/registration")


class RegistrationSchema(NamedTuple):
    username: str
    email: str


def _is_okay(field: str, exists: bool, value: Any, expected: Type[object]) -> bool:
    if not exists:
        raise InvalidUsage(f"Missing required field: {field}")
    return type(value) is expected


def _validate(input: Dict[str, Any], schema: Type[tuple]) -> None:
    for field_name, field_type in schema.__annotations__.items():
        if not _is_okay(
            field_name, field_name in input, input.get(field_name), field_type
        ):
            raise InvalidUsage(
                f"Unexpected value '{field_type}' for field '{field_name}'"
            )

    if len(input) != len(schema.__annotations__):
        fields = ", ".join(schema.__annotations__.keys())
        raise InvalidUsage(f"Unknown fields, please only send: {fields}")


@bp.post("/")
async def check_types(request: Request):
    _validate(request.json, RegistrationSchema)
    connection: FakeDBConnection = request.app.ctx.db
    service = RegistrationService(connection)
    await service.register_user(request.json["username"], request.json["email"])
    return json(True, status=201)
