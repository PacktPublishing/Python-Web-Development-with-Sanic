from importlib import import_module
from inspect import getmembers
from types import ModuleType
from typing import Union

from sanic.blueprints import Blueprint, BlueprintGroup


def autodiscover(app, *module_names: Union[str, ModuleType]):
    mod = app.__module__
    blueprints = set()

    def _find_bps(module):
        nonlocal blueprints
        found_blueprints = set()
        found_blueprint_groups = set()

        for _, member in getmembers(module):
            if isinstance(member, Blueprint):
                found_blueprints.add(member)
            elif isinstance(member, BlueprintGroup):
                found_blueprint_groups.add(member)

        # If a module imports a bp in the same file as a BlueprintGroup is
        # created, then we want to remove the Bluesprints in that group
        # so we subtract any blueprints that are grouped from those found
        # in the module.
        blueprints.update(
            found_blueprints
            - {
                bp
                for group in found_blueprint_groups
                for bp in group.blueprints
            }
        )

        # Add in any blueprint groups
        blueprints.update(found_blueprint_groups)

    for module in module_names:
        if isinstance(module, str):
            module = import_module(module, mod)
        _find_bps(module)

    for bp in blueprints:
        app.blueprint(bp)
