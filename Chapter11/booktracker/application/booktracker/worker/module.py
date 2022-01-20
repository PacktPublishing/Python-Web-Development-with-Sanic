from importlib import import_module

from sanic import Sanic


def setup_modules(app: Sanic, *module_names: str):
    """
    Load some modules
    """
    for module_name in module_names:
        module = import_module(module_name)
        if bp := getattr(module, "bp", None):
            app.blueprint(bp)
