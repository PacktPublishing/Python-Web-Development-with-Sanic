from .users.view import bp as users_bp
from .trails.view import bp as trails_bp
from .slow.view import bp as slow_bp
from sanic import Blueprint

bp = Blueprint.group(users_bp, trails_bp, slow_bp, version=1)
