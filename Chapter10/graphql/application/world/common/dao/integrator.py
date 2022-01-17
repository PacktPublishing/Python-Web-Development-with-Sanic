from __future__ import annotations

from inspect import getmembers, getmodule, ismethod
from pathlib import Path
from textwrap import indent
from types import ModuleType
from typing import Any, Callable, Dict, Iterator, List, Tuple, Type, cast

from ariadne import ObjectType, QueryType
from sanic.exceptions import SanicException


class BaseIntegrator:
    name: str

    def __init__(self, root: RootIntegrator) -> None:
        self.root = root

    def make_additional_schema(self) -> ObjectType:
        ...

    def make_query_def(self) -> List[str]:
        ...


class RootIntegrator:
    def __init__(self, query: QueryType) -> None:
        self.query = query
        self.schemas: List[str] = []
        self.queries: Dict[str, str] = {}
        self.registry: Dict[str, BaseIntegrator] = {}

    @classmethod
    def create(
        cls, *integrators: Type[BaseIntegrator], query: QueryType
    ) -> RootIntegrator:
        instance = cls(query)
        instance.registry.update(
            {integrator.name: integrator(instance) for integrator in integrators}
        )
        return instance

    def load(self) -> None:
        for _, module in self.iter_integrators():
            base = Path(cast(str, module.__file__)).parent
            schema = self.load_schema(base / "schema.gql")
            self.schemas.append(schema)

    def attach_resolvers(self) -> None:
        for field, func in self.iter_integrator_methods():
            self.query.set_field(field, func)

    def generate_query_defs(self) -> str:
        schemas = "\n".join(self.schemas)
        queries = "\n".join(
            [
                indent(item, "    ")
                for integrator, _ in self.iter_integrators()
                if (query_def := integrator.make_query_def())
                for item in query_def
            ]
        )

        return f"{schemas}\ntype Query {{\n{queries}\n}}"

    def generate_additional_schemas(self) -> List[ObjectType]:
        return [
            schema
            for integrator, _ in self.iter_integrators()
            if (schema := integrator.make_additional_schema())
        ]

    def iter_integrators(self) -> Iterator[Tuple[BaseIntegrator, ModuleType]]:
        for integrator in self.registry.values():
            module = getmodule(integrator)
            if not module:
                raise SanicException(f"Could not locate module for {integrator}")

            yield integrator, module

    def iter_integrator_methods(self) -> Iterator[Tuple[str, Callable[..., Any]]]:
        for integrator, _ in self.iter_integrators():
            for name, func in getmembers(integrator, self.isquery):
                field = name.replace("query_", "")
                yield field, func

    def get_integrator(self, name: str) -> BaseIntegrator:
        return self.registry[name]

    @staticmethod
    def isquery(obj: Any) -> bool:
        if ismethod(obj):
            return obj.__name__.startswith("query_")
        return False

    @staticmethod
    def load_schema(path: Path) -> str:
        with open(path, "r") as f:
            return f.read()
