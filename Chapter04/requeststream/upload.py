import httpx


def gen(filename, f, size=4):
    yield filename
    while True:
        data = f.read(size)
        if not data:
            break
        yield data.encode("utf-8")


with open("./file.txt", "r") as f:
    r = httpx.post("http://localhost:7777/upload", data=gen(b"somefile.txt", f))
print(r.status_code)
for line in r.text.split("\n"):
    print(line)
