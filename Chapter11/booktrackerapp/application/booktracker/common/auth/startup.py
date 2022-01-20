from sanic import Sanic
from sanic_jwt import Initialize

from .endpoint import GitHubOAuthLogin
from .handler import (
    authenticate,
    payload_extender,
    retrieve_refresh_token,
    retrieve_user,
    store_refresh_token,
)


def setup_auth(app: Sanic):
    Initialize(
        app,
        url_prefix="/api/v1/auth",
        authenticate=authenticate,
        retrieve_user=retrieve_user,
        extend_payload=payload_extender,
        store_refresh_token=store_refresh_token,
        retrieve_refresh_token=retrieve_refresh_token,
        class_views=[("/github", GitHubOAuthLogin)],
        user_id="eid",
        cookie_set=True,
        cookie_split=True,
        cookie_strict=False,
        refresh_token_enabled=True,
        secret="qqqq",
        cookie_secure=(not app.config.LOCAL),
        expiration_delta=60 * 15,
        leeway=0,
    )
