from sanic import Sanic
from sanic.server.async_server import AsyncioServer
from wadsworth.blueprints.info.view import bp as info_view
from wadsworth.blueprints.redirect.view import bp as redirect_view
from sanic.exceptions import ServerError
from sanic.handlers import ErrorHandler


def attach_redirect_app(main_app: Sanic):
    redirect_app = Sanic("RedirectApp")
    redirect_app.blueprint(info_view)
    redirect_app.blueprint(redirect_view)
    redirect_app.ctx.main_app = main_app

    @main_app.before_server_start
    async def startup_redirect_app(main: Sanic, _):
        app_server = await redirect_app.create_server(
            port=8080, return_asyncio_server=True
        )
        if not app_server:
            raise ServerError("Failed to create redirect server")
        main_app.ctx.redirect = app_server
        main_app.add_task(runner(redirect_app, app_server))

    @main_app.after_server_stop
    async def shutdown_redirect_app(main: Sanic, _):
        await main.ctx.redirect.before_stop()
        await main.ctx.redirect.close()
        for connection in main.ctx.redirect.connections:
            connection.close_if_idle()
        await main.ctx.redirect.after_stop()
        redirect_app.is_stopping = False

    @redirect_app.before_server_start
    async def before_server_start(*_):
        print("before_server_start")

    @redirect_app.after_server_stop
    async def after_server_stop(*_):
        print("after_server_stop")

    return redirect_app


async def runner(app: Sanic, app_server: AsyncioServer):
    app.is_running = True
    try:
        app.signalize()
        app.finalize()
        ErrorHandler.finalize(app.error_handler)
        app_server.init = True

        await app_server.before_start()
        await app_server.after_start()
        await app_server.serve_forever()
    finally:
        app.is_running = False
        app.is_stopping = True
