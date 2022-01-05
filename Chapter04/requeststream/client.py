import time

import httpx


def gen():
    for _ in range(1):
        print("waiting")
        time.sleep(1)
    yield b'{"foo": "bar"}'


r = httpx.post("http://localhost:7777/transaction", data=gen())
print(r.status_code)
print(r.content)
