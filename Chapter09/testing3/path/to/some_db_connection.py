from typing import Any


class FakeDBConnection:
    async def execute(self, query: str, *params: Any):
        ...
