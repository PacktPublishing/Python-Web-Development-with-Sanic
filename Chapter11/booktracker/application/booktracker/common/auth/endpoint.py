from booktracker.common.cookie import set_cookie
from booktracker.common.csrf import generate_csrf
from sanic import Request
from sanic.response import redirect
from sanic_jwt import BaseEndpoint


class GitHubOAuthLogin(BaseEndpoint):
    @staticmethod
    async def get(request: Request):
        url = (
            "https://github.com/login/oauth/authorize?scope=read:user"
            f"&client_id={request.app.config.GITHUB_OAUTH_CLIENT_ID}"
        )

        if (
            "csrf_token" not in request.cookies
            or "ref_token" not in request.cookies
        ):
            ref, token = generate_csrf(
                request.app.config.CSRF_SECRET,
                request.app.config.CSRF_REF_LENGTH,
                request.app.config.CSRF_REF_PADDING,
            )

            response = redirect(url)
            set_cookie(
                response=response,
                domain="localhost",
                key="ref_token",
                value=ref,
                httponly=True,
                samesite="strict",
                secure=(not request.app.config.LOCAL),
            )
            set_cookie(
                response=response,
                domain="localhost",
                key="csrf_token",
                value=token,
                samesite="strict",
                secure=(not request.app.config.LOCAL),
            )

        return response
