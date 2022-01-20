from __future__ import annotations

from inspect import getmembers, getmodule, isfunction
from pathlib import Path
from typing import Dict, Optional, Set, Type

from databases import Database
from sanic.exceptions import SanicException

from .decorator import execute
from .hydrator import Hydrator


class BaseExecutor:
    """
    Responsible for being the interface between the DB and the application
    """

    _registry: Set[Type[BaseExecutor]] = set()
    _queries: Dict[str, str] = {}
    _fallback_hydrator: Hydrator
    db: Database

    def __init__(
        self, db: Database, hydrator: Optional[Hydrator] = None
    ) -> None:
        self.db = db
        self._hydrator = hydrator

    def __init_subclass__(cls) -> None:
        BaseExecutor._registry.add(cls)

    @property
    def hydrator(self) -> Hydrator:
        if self._hydrator:
            return self._hydrator
        return self._fallback_hydrator

    @classmethod
    def load(cls, hydrator: Hydrator) -> None:
        """
        Look through the Executor definition for methods that should
        execute a query, then load the corresponding SQL from a .sql file
        and hold in memory.
        """
        cls._fallback_hydrator = hydrator
        for executor in cls._registry:
            module = getmodule(executor)
            if not module:
                raise SanicException(f"Could not locate module for {executor}")

            base = Path(module.__file__).parent
            for name, func in getmembers(executor, cls.isoperation):
                path = base / "queries" / f"{name}.sql"
                cls._queries[name] = cls.load_sql(path)
                setattr(executor, name, execute(func))

    @staticmethod
    def isoperation(obj):
        """Check if the object is a method that starts with get_ or create_"""
        if isfunction(obj):
            return (
                obj.__name__.startswith("get_")
                or obj.__name__.startswith("create_")
                or obj.__name__.startswith("update_")
            )
        return False

    @staticmethod
    def load_sql(path: Path):
        with open(path, "r") as f:
            return f.read()
