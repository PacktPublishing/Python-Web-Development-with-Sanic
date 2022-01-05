from dataclasses import field, fields, is_dataclass
from datetime import date
from enum import Enum, auto
from functools import wraps
from typing import List, get_args, get_type_hints
from uuid import UUID

from pydantic import ValidationError as PydanticValidationError
from pydantic.dataclasses import dataclass
from sanic import Request, Sanic, text
from sanic.exceptions import SanicException

app = Sanic(__name__)


class ProductType(Enum):
    def _generate_next_value_(name, *_):
        return name.lower()

    FRUIT = auto()
    VEGETABLES = auto()
    FISH = auto()
    MEAT = auto()


class ValidatorModel:
    def __post_init__(self):
        for field in fields(self.__class__):
            existing = getattr(self, field.name)
            hydrated = self._hydrate(field.type, existing)

            if hydrated:
                setattr(self, field.name, hydrated)
            elif type(existing) is not field.type:
                setattr(self, field.name, field.type(existing))

    def _hydrate(self, field_type, value):
        args = get_args(field_type)
        check_type = field_type

        if args:
            check_type = args[0]

        if is_dataclass(check_type):
            if isinstance(value, list):
                return [self._hydrate(check_type, item) for item in value]
            elif isinstance(value, dict):
                return field_type(**value)

        return None


@dataclass
class Product:
    name: str
    product_type: ProductType


@dataclass
class BookStallBody:
    name: str
    vendor_id: UUID
    description: str
    employees: int
    products: List[Product]


@dataclass
class PaginationQuery:
    limit: int = field(default=0)
    offset: int = field(default=0)


def validate(
    wrapped=None,
    body_arg="body",
    query_arg="query",
):
    def decorator(handler):
        annotations = get_type_hints(handler)
        body_model = None
        query_model = None

        for param_name, annotation in annotations.items():
            if param_name == body_arg:
                body_model = annotation
            elif param_name == query_arg:
                query_model = annotation

        @wraps(handler)
        async def decorated_function(request: Request, *args, **kwargs):
            nonlocal body_arg
            nonlocal body_model
            nonlocal query_arg
            nonlocal query_model

            if body_model:
                kwargs[body_arg] = do_validation(body_model, request.json)
            if query_model:
                kwargs[query_arg] = do_validation(
                    query_model, dict(request.query_args)
                )

            return await handler(request, *args, **kwargs)

        return decorated_function

    return decorator if wrapped is None else decorator(wrapped)


class ValidationError(SanicException):
    status_code = 400


def do_validation(model, data):
    try:
        instance = model(**data)
    except PydanticValidationError as e:
        raise ValidationError(
            f"There was a problem validating {model} "
            f"with the raw data: {data}.\n"
            f"The encountered exception: {e}"
        ) from e
    return instance


@app.post("/stalls/<market_date:ymd>")
@validate()
async def book_a_stall(
    request: Request,
    body: BookStallBody,
    market_date: date,
):
    print(body)
    return text(request.ip)


@app.get("/stalls/<market_date:ymd>")
@validate
async def book_a_stall(
    request: Request,
    query: PaginationQuery,
    market_date: date,
):
    print(query)
    return text(request.ip)


app.run(port=9999, debug=True)
