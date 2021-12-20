from sanic import Blueprint
from .graphql.view import bp as graphql_bp

bp = Blueprint.group(graphql_bp, version=1)
