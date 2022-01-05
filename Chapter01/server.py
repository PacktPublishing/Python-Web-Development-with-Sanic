from sanic import Sanic, text, Request 
 
app = Sanic(__name__) 
 
@app.post("/") 
async def handler(request: Request): 
    message = ( 
        request.head + b"\n\n" + request.body 
    ).decode("utf-8") 
    print(message) 
    return text("Done") 
 
app.run(port=9999, debug=True)