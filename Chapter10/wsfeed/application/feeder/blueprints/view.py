from sanic import Blueprint

from .feed.view import bp as feed_bp

bp = Blueprint.group(feed_bp, version=1)
