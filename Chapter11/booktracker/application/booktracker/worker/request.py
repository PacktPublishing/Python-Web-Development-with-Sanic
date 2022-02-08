from typing import Any

from sanic import Request

from booktracker.common.eid import generate


class BooktrackerRequest(Request):
    @classmethod
    def generate_id(*_: Any) -> str:
        return generate()
