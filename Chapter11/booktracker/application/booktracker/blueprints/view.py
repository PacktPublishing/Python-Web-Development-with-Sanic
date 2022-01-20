from sanic import Blueprint

from .author.view import bp as author_bp
from .book.view import bp as book_bp
from .frontend.view import bp as frontend_bp

api = Blueprint.group(author_bp, book_bp, version=1, version_prefix="/api/v")
bp = Blueprint.group(frontend_bp, api)
