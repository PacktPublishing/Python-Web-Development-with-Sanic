from pathlib import Path
from jinja2.loaders import FileSystemLoader
from sanic import Sanic, html
from jinja2 import Environment

app = Sanic(__name__)


@app.before_server_start
def setup_template_env(app, _):
    app.ctx.env = Environment(
        loader=FileSystemLoader(Path(__file__).parent / "templates"),
        autoescape=True,
    )


@app.get("/")
async def handler(request):
    template = request.app.ctx.env.get_template("index.html")
    output = template.render(
        songs=[
            "Stairway to Heaven",
            "Kashmir",
            "All along the Watchtower",
            "Black Hole Sun",
            "Under the Bridge",
        ]
    )
    return html(output)
