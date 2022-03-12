from importlib import import_module
from inspect import getmembers
from types import ModuleType
from typing import Union

from sanic.blueprints import Blueprint, BlueprintGroup


def autodiscover(app, *module_names: Union[str, ModuleType]):
    mod = app.__module__
    blueprints = set()
    _imported = set()

    def _find_bps(module):
        nonlocal blueprints

        for _, member in getmembers(module):
            if isinstance(member, (Blueprint, BlueprintGroup)):
                blueprints.add(member)

    for module in module_names:
        if isinstance(module, str):
            module = import_module(module, mod)
            _imported.add(module.__file__)
        _find_bps(module)

    for bp in blueprints:
        app.blueprint(bp)
