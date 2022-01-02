from __future__ import annotations

from abc import ABC, abstractmethod


class Operation(ABC):
    @abstractmethod
    async def run(self, **_):
        raise NotImplementedError
