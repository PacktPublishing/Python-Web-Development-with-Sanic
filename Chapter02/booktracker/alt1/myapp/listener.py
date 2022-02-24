from sanic import Sanic

app = Sanic.get_app()


@app.before_server_start
def _(*__):
    print("...")
