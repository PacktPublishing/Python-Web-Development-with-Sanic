from .book.view import bp as book_bp
from sanic import Blueprint

group = Blueprint.group(book_bp, version=2)
