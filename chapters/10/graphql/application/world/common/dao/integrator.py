from __future__ import annotations
from textwrap import dedent, indent

from typing import Dict, List, Set, Type, get_args, get_origin
from sanic.exceptions import SanicException
from inspect import Parameter, getmembers, getmodule, ismethod, signature
from pathlib import Path
from ariadne import QueryType
from world.common.base_model import BaseModel


class BaseIntegrator:
    name: str

    def __init__(self, root: RootIntegrator) -> None:
        self.root = root

    def make_additional_schema(self):
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
            base = Path(module.__file__).parent
            schema = self.load_schema(base / "schema.gql")
            self.schemas.append(schema)

    def attach_resolvers(self):
        for field, func in self.iter_integrator_methods():
            self.query.set_field(field, func)

    def generate_query_defs(self):
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

    def generate_additional_schemas(self):
        return [
            schema
            for integrator, _ in self.iter_integrators()
            if (schema := integrator.make_additional_schema())
        ]

    def iter_integrators(self):
        for integrator in self.registry.values():
            module = getmodule(integrator)
            if not module:
                raise SanicException(f"Could not locate module for {integrator}")

            yield integrator, module

    def iter_integrator_methods(self):
        for integrator, _ in self.iter_integrators():
            for name, func in getmembers(integrator, self.isquery):
                field = name.replace("query_", "")
                yield field, func

    def get_integrator(self, name: str):
        return self.registry[name]

    @staticmethod
    def isquery(obj):
        if ismethod(obj):
            return obj.__name__.startswith("query_")
        return False

    @staticmethod
    def load_schema(path: Path):
        with open(path, "r") as f:
            return f.read()
