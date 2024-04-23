from fastapi import FastAPI, Request

from routers import controller, sensor

app = FastAPI()
app.include_router(sensor.router)
app.include_router(controller.router)


@app.get("/")
async def echo(request: Request):
    return dict(request.query_params)
