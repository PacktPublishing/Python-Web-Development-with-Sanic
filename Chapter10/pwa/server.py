import asyncio
from datetime import datetime
from sanic import Sanic, json, response
from asyncio.subprocess import create_subprocess_shell, PIPE
from pathlib import Path
from sanic.log import logger
import ujson

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
async def index(_):
    return await response.file(INDEX_HTML)


@app.get("/time")
async def time(_):
    await asyncio.sleep(1)
    return json({"now": datetime.now().isoformat()})


@app.signal("watchdog.file.reload")
async def file_reloaded():
    print("...")


@app.before_server_start
async def start(app, _):
    app.ctx.livereload_server = await livereload.create_server(
        port=35729, return_asyncio_server=True
    )
    app.add_task(runner(livereload, app.ctx.livereload_server))


@app.before_server_stop
async def stop(app, _):
    await app.ctx.livereload_server.close()


@app.before_server_start
async def check_reloads(app, _):
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

        while True:
            message = await rebuild.stdout.readline()
            if not message:
                break
            output = message.decode("ascii").rstrip()
            logger.info(f"[reload] {output}")

        await app.dispatch("watchdog.file.reload")


@livereload.websocket("/livereload")
async def livereload_handler(request, ws):
    global app
    logger.info("Connected")
    msg = await ws.recv()
    logger.info(msg)
    await ws.send(ujson.dumps(HELLO))

    while True:
        await app.event("watchdog.file.reload")
        await ws.send(ujson.dumps(RELOAD))


async def runner(app, app_server):
    app.is_running = True
    try:
        app.signalize()
        app.finalize()
        await app_server.serve_forever()
    finally:
        app.is_running = False
        app.is_stopping = True
