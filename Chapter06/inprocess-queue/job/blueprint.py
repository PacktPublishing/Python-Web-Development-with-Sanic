from sanic import Blueprint
from job.startup import (
    setup_task_executor,
    setup_job_fetch,
    register_operations,
)
from job.view import JobListView, JobDetailView

bp = Blueprint("JobQueue", url_prefix="/job")

bp.after_server_start(setup_job_fetch)
bp.after_server_start(setup_task_executor)
bp.after_server_start(register_operations)
bp.add_route(JobListView.as_view(), "")
bp.add_route(JobDetailView.as_view(), "/<uid:uuid>")
