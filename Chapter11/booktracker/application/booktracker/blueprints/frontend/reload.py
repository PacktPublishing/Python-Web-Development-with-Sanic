from asyncio.subprocess import PIPE, create_subprocess_shell
from logging import getLogger
from typing import Any

import ujson
from sanic.server import AsyncioServer
from sanic.server.websockets.impl import WebsocketImplProtocol

from booktracker.common.log import setup_logging
from sanic import Blueprint, HTTPResponse, Request, Sanic
from sanic.response import file

logger = getLogger("booktracker")
livereload = Sanic("Livereload")
setup_logging(livereload, setup_factory=False)
livereload.config.AUTO_EXTEND = False

HELLO = {
    "command": "hello",
    "protocols": [
        "http://livereload.com/protocols/official-7",
    ],
    "serverName": livereload.name,
}


@livereload.get("/livereload.js")
async def livereload_js(request: Request) -> HTTPResponse:
    return await file(request.app.config.UI_DIR / "public" / "livereload.js")


@livereload.signal("http.routing.after")
async def after_routing(**_) -> None:
    ...


@livereload.signal("watchdog.file.reload")
async def file_reloaded() -> None:
    ...


@livereload.websocket("/livereload")
async def livereload_handler(request: Request, ws: WebsocketImplProtocol) -> None:
    reload_path = {
        "command": "reload",
        "path": str(request.app.config.UI_DIR / "public" / "index.html"),
    }

    await ws.recv()
    await ws.send(ujson.dumps(HELLO))

    while True:
        await livereload.event("watchdog.file.reload")
        await ws.send(ujson.dumps(reload_path))


async def runner(app: Sanic, app_server: AsyncioServer) -> None:
    app.is_running = True
    try:
        app.signalize()
        app.finalize()
        app.state.is_started = True
        await app._server_event("init", "after")
        await app_server.serve_forever()
    finally:
        app.is_running = False
        app.is_stopping = True


def setup_livereload(bp: Blueprint) -> None:
    global livereload
    livereload.ctx.bp = bp

    @bp.before_server_start
    async def start(app: Sanic, _) -> None:
        global livereload
        livereload.config.UI_DIR = app.config.UI_DIR
        app.ctx.livereload_server = await livereload.create_server(
            host="0.0.0.0", port=35729, return_asyncio_server=True
        )
        if app.ctx.livereload_server is not None:
            app.add_task(runner(livereload, app.ctx.livereload_server))

    @bp.before_server_stop
    async def stop(app: Sanic, _) -> None:
        await app.ctx.livereload_server.close()

    @bp.before_server_start
    async def check_reloads(app: Sanic, _: Any) -> None:
        do_rebuild = False
        if reloaded := app.config.get("RELOADED_FILES"):
            reloaded = reloaded.split(",")

            do_rebuild = any(
                ext in ("svelte", "js", "css", "html")
                for filename in reloaded
                if (ext := filename.rsplit(".", 1)[-1])
            )

        if do_rebuild:
            logger.warning(f"RUNNING 'yarn build' in {app.config.UI_DIR}")
            rebuild = await create_subprocess_shell(
                "yarn build",
                stdout=PIPE,
                stderr=PIPE,
                cwd=app.config.UI_DIR,
            )

            if rebuild.stdout is not None:
                while True:
                    message = await rebuild.stdout.readline()
                    if not message:
                        break
                    output = message.decode("ascii").rstrip()
                    logger.info(f"[reload] {output}")

            await livereload.dispatch("watchdog.file.reload")
