from sanic import Sanic

app = Sanic(__file__)


app.route("/")(lambda x: None)
