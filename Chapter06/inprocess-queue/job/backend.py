from __future__ import annotations

import os
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

import ujson as json

from .model import JobDetails


class Backend(ABC):
    @abstractmethod
    async def store(self, *_, **__):
        ...

    @abstractmethod
    async def fetch(self, *_, **__):
        ...

    @abstractmethod
    async def start(self, *_, **__):
        ...

    @abstractmethod
    async def stop(self, *_, **__):
        ...


class FileBackend(Backend):
    def __init__(self, path):
        self.path = path

    async def store(self, key, value):
        with open(self.path, "a") as f:
            f.write(f"{key}|{value}\n")

    async def fetch(self, key, chunk=4096):
        size = os.stat(self.path)[6]
        count = 1
        value = None
        with open(self.path, "rb") as f:
            if size > chunk:
                f.seek(-1 * chunk * count, 2)

            data = f.read(chunk).split(b"\n")
            if not data[-1]:
                data = data[:-1]

            while value is None:
                while len(data) == 1 and ((count * chunk) < size):
                    count = count + 1
                    line = data[0]
                    try:
                        f.seek(-1 * chunk * count, 2)
                        data = (f.read(chunk) + line).split(b"\n")
                    except IOError:
                        f.seek(0)
                        pos = size - (chunk * (count - 1))
                        data = (f.read(pos) + line).split(b"\n")

                if len(data) == 0:
                    return None

                line = data[-1]

                if line.startswith(str(key).encode()):
                    value = line
                else:
                    data.pop()

        raw = list(value.strip().decode("utf-8").split("|"))
        raw[0] = UUID(raw[0])
        raw[2] = bool(int(raw[2]))
        raw[3] = datetime.fromisoformat(raw[3])
        raw[4] = json.loads(raw[4])
        raw[5] = json.loads(raw[5])
        return JobDetails(*raw)

    async def start(self, job):
        await self.store(
            job.uid,
            "|".join(
                [
                    job.operation,
                    str(0),
                    datetime.utcnow().isoformat(),
                    json.dumps(job.kwargs),
                    json.dumps(job.retval),
                ]
            ),
        )

    async def stop(self, job):
        await self.store(
            job.uid,
            "|".join(
                [
                    job.operation,
                    str(1),
                    datetime.utcnow().isoformat(),
                    json.dumps(job.kwargs),
                    json.dumps(job.retval),
                ]
            ),
        )
