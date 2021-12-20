import asyncio
from typing import Set, final
from uuid import UUID, uuid4
from sanic import Sanic, Request, text
from sanic.response import redirect

app = Sanic(__name__)
app.config.KEEP_ALIVE = False
app.static("/index.html", "./index.html", name="index")


@app.route("/")
def home(request: Request):
    return redirect(request.app.url_for("index"))


@app.after_server_start
async def setup_chatroom(app: Sanic, loop):
    app.ctx.chatroom = ChatRoom(loop)


@app.websocket("/chat")
async def feed(request, ws):
    try:
        client = Client(ws.send)
        request.app.ctx.chatroom.enter(client)

        while True:
            message = await ws.recv()
            if not message:
                break
            await request.app.ctx.chatroom.push(message, client.uid)

    finally:
        request.app.ctx.chatroom.exit(client)


class Client:
    def __init__(self, send) -> None:
        self.uid = uuid4()
        self.send = send

    def __hash__(self) -> int:
        return self.uid.int


class ChatRoom:
    def __init__(self, loop) -> None:
        self.clients: Set[Client] = set()
        self.loop = loop

    def enter(self, client: Client):
        self.clients.add(client)

    def exit(self, client: Client):
        self.clients.remove(client)

    async def push(self, message: str, sender: UUID):
        recipients = (client for client in self.clients if client.uid != sender)
        await asyncio.gather(*[client.send(message) for client in recipients])


app.run(port=9999, debug=True)
