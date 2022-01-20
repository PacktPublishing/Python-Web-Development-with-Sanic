from dataclasses import dataclass, field

from booktracker.common.base_model import BaseModel
from sanic import Request, Sanic


@dataclass
class Pagination(BaseModel):
    limit: int = field(default=15)
    offset: int = field(default=0)

    @staticmethod
    async def from_request(request: Request):
        args = {
            key: int(value)
            for key in ("limit", "offset")
            if (value := request.args.get(key))
        }
        return Pagination(**args)


def setup_pagination(app: Sanic):
    @app.before_server_start
    async def setup_pagination(app: Sanic, _):
        app.ext.injection(Pagination, Pagination.from_request)
