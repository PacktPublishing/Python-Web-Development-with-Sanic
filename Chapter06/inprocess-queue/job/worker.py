from .job import Job


async def worker(name, queue, backend):
    while True:
        job = await queue.get()
        if not job:
            break

        size = queue.qsize()
        print(f"[{name}] Running {job}. {size} in queue.")

        job_instance = await Job.create(job, backend)

        async with job_instance as operation:
            await job_instance.execute(operation)
