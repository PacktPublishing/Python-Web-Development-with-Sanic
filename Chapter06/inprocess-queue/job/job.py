from __future__ import annotations
from typing import Any, Dict

from uuid import uuid4

from .operations.base import Operation
from .operations.registry import OperationRegistry

# from .task import Task


class Job:
    def __init__(self, operation: str, backend, uid=None, kwargs=None) -> None:
        self.operation = operation
        self.uid = uid or uuid4()
        self.backend = backend
        self.kwargs = kwargs or {}
        self.retval = None

    async def execute(self, operation: Operation):
        print(f"Executing {self.operation}")
        self.retval = await operation.run(**self.kwargs)

    async def __aenter__(self):
        operation_class = OperationRegistry().get(self.operation)

        if operation_class:
            operation = operation_class()
            await self.backend.start(self)
            return operation
        else:
            raise Exception(f"No operation named {self.operation}")

    async def __aexit__(self, *_):
        await self.backend.stop(self)

    @classmethod
    async def create(cls, job: Dict[str, Any], backend):
        operation = job["operation"]
        uid = job["uid"]
        return cls(operation, backend, uid=uid, kwargs=job["kwargs"])
