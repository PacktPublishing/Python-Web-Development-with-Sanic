from .book.view import bp as book_bp
from sanic import Blueprint

Blueprint.group(book_bp, version=2)
