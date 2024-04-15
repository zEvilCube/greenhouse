from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def echo(request: Request):
    request_args = dict(request.query_params)
    return request_args
