from .feed.view import bp as feed_bp
from sanic import Blueprint

bp = Blueprint.group(feed_bp, version=1)
