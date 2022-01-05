from typing import Dict, Type
from .base import Operation


class OperationRegistry:
    _singleton = None
    operations: Dict[str, Type[Operation]]

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)
            cls._singleton.operations = {}

        return cls._singleton

    def __init__(self, *operations: Type[Operation]) -> None:
        for operation in operations:
            self.register(operation)

    def register(self, operation: Type[Operation]) -> None:
        name = operation.__name__.lower()
        self.operations[name] = operation

    def get(self, name: str) -> Type[Operation]:
        return self.operations[name]
