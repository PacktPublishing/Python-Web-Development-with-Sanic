import asyncio
from typing import Callable, Coroutine
from sanic import Sanic, Request, text
from sanic.response import redirect

app = Sanic(__name__)


class BaseField(str):
    name: str

    def __str__(self) -> str:
        return f"{self.name}: {super().__str__()}\n"


class Event(BaseField):
    name = "event"


class Data(BaseField):
    name = "data"


class ID(BaseField):
    name = "id"


class Retry(BaseField):
    name = "retry"


class Heartbeat(BaseField):
    name = ""


class Message(list):
    def __init__(self, *fields: BaseField) -> None:
        self.extend(fields)

    def __str__(self) -> str:
        return "".join(map(str, self)) + "\n"


class Notifier:
    def __init__(
        self,
        send: Callable[..., Coroutine[None, None, None]],
        queue: asyncio.Queue,
    ):
        self.send = send
        self.queue = queue

    async def run(self):
        await self.send(message(Heartbeat()))
        while True:
            fields = await self.queue.get()
            if fields:
                if not isinstance(fields, (list, tuple)):
                    fields = [fields]
                await self.send(message(*fields))


def message(*fields: BaseField):
    return "".join(map(str, fields)) + "\n"


@app.route("/")
def home(request: Request):
    return redirect(request.app.url_for("index"))


@app.get("/sse")
async def simple_sse(request: Request):
    headers = {"Cache-Control": "no-cache"}
    resp = await request.respond(headers=headers, content_type="text/event-stream")
    notifier = Notifier(resp.send, request.app.ctx.notification_queue)
    await notifier.run()
    await resp.eof()


@app.post("login")
async def login(request: Request):
    request.app.ctx.notification_queue.put_nowait(
        [Event("login"), Data("So-and-so just logged in")]
    )
    return text("Logged in. Imagine we did something here.")


@app.after_server_start
async def setup_notification_queue(app: Sanic, _):
    app.ctx.notification_queue = asyncio.Queue()
