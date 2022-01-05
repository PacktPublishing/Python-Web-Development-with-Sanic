import asyncio
from .base import Operation


class Hello(Operation):
    async def run(self, name="world"):
        message = f"Hello, {name}"
        print(message)
        await asyncio.sleep(10)
        print("Done.")
        return message
