from sanic import Blueprint

from .hello.view import bp as hello_bp

bp = Blueprint.group(hello_bp, version=1)
