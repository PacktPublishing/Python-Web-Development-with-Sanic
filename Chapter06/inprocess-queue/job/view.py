from sanic import json
from sanic.views import HTTPMethodView
from sanic.exceptions import InvalidUsage
import uuid


class JobListView(HTTPMethodView):
    async def post(self, request):
        operation = request.json.get("operation")
        kwargs = request.json.get("kwargs", {})
        if not operation:
            raise InvalidUsage("Missing operation")

        uid = uuid.uuid4()
        await request.app.ctx.queue.put(
            {
                "operation": operation,
                "uid": uid,
                "kwargs": kwargs,
            }
        )
        return json({"uid": str(uid)}, status=202)


class JobDetailView(HTTPMethodView):
    async def get(self, request, uid: uuid.UUID):
        data = await request.app.ctx.jobs.fetch(uid)
        return json(data)
