import asyncio
from job.worker import worker
from .backend import FileBackend
from .operations.hello import Hello
from .operations.registry import OperationRegistry


async def setup_job_fetch(app, _):
    app.ctx.jobs = FileBackend("./db")


async def setup_task_executor(app, _):
    app.ctx.queue = asyncio.Queue(maxsize=64)
    for x in range(app.config.NUM_TASK_WORKERS):
        name = f"Worker-{x}"
        print(f"Starting up executor: {name}")
        app.add_task(worker(name, app.ctx.queue, app.ctx.jobs))


async def register_operations(app, _):
    app.ctx.registry = OperationRegistry(Hello)
