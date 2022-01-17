import asyncio
from asyncio.subprocess import PIPE, create_subprocess_shell
from datetime import datetime
from pathlib import Path
from typing import Any

import ujson
from sanic import HTTPResponse, Request, Sanic, json, response
from sanic.log import logger
from sanic.server import AsyncioServer
from sanic.server.websockets.connection import WebSocketConnection

app = Sanic("MainApp")
app.config.FRONTEND_DIR = Path(__file__).parent / "my-svelte-project"

livereload = Sanic("livereload")
livereload.static("/livereload.js", app.config.FRONTEND_DIR / "livereload.js")

INDEX_HTML = app.config.FRONTEND_DIR / "public" / "index.html"
HELLO = {
    "command": "hello",
    "protocols": [
        "http://livereload.com/protocols/official-7",
    ],
    "serverName": app.name,
}
RELOAD = {"command": "reload", "path": str(INDEX_HTML)}

app.static("/", app.config.FRONTEND_DIR / "public")


@app.get("/")
async def index(_: Request) -> HTTPResponse:
    return await response.file(INDEX_HTML)


@app.get("/time")
async def time(_: Request) -> HTTPResponse:
    await asyncio.sleep(1)
    return json({"now": datetime.now().isoformat()})


@app.signal("watchdog.file.reload")
async def file_reloaded() -> None:
    print("...")


@app.before_server_start
async def start(app: Sanic, _: Any) -> None:
    app.ctx.livereload_server = await livereload.create_server(
        port=35729, return_asyncio_server=True
    )
    if app.ctx.livereload_server is not None:
        app.add_task(runner(livereload, app.ctx.livereload_server))


@app.before_server_stop
async def stop(app: Sanic, _: Any) -> None:
    await app.ctx.livereload_server.close()


@app.before_server_start
async def check_reloads(app: Sanic, _: Any) -> None:
    do_rebuild = False
    if reloaded := app.config.get("RELOADED_FILES"):
        reloaded = reloaded.split(",")

        do_rebuild = any(
            ext in ("svelte", "js")
            for filename in reloaded
            if (ext := filename.rsplit(".", 1)[-1])
        )

    if do_rebuild:
        rebuild = await create_subprocess_shell(
            "yarn run build",
            stdout=PIPE,
            stderr=PIPE,
            cwd=app.config.FRONTEND_DIR,
        )

        if rebuild.stdout is not None:
            while True:
                message = await rebuild.stdout.readline()
                if not message:
                    break
                output = message.decode("ascii").rstrip()
                logger.info(f"[reload] {output}")

        await app.dispatch("watchdog.file.reload")


@livereload.websocket("/livereload")
async def livereload_handler(request: Request, ws: WebSocketConnection) -> None:
    global app
    logger.info("Connected")
    msg = await ws.recv()
    logger.info(msg)
    await ws.send(ujson.dumps(HELLO))

    while True:
        await app.event("watchdog.file.reload")
        await ws.send(ujson.dumps(RELOAD))


async def runner(app: Sanic, app_server: AsyncioServer) -> None:
    app.is_running = True
    try:
        app.signalize()
        app.finalize()
        await app_server.serve_forever()
    finally:
        app.is_running = False
        app.is_stopping = True
