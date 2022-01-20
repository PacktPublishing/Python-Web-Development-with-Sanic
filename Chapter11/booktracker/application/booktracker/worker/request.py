from booktracker.common.eid import generate
from sanic import Request


class BooktrackerRequest(Request):
    @classmethod
    def generate_id(*_):
        return generate()
