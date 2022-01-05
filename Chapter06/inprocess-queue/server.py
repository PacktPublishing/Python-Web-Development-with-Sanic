from sanic import Sanic
from job.blueprint import bp

app = Sanic(__name__)
app.config.NUM_TASK_WORKERS = 3
app.blueprint(bp)
