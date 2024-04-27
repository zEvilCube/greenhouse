from fastapi import FastAPI, Request

from app.routers import greenhouse_router, sensors_router, controllers_router
from database import models, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(greenhouse_router)
app.include_router(sensors_router)
app.include_router(controllers_router)


@app.get("/")
async def echo(request: Request):
    return request.query_params


@app.post("/test")
async def test():
    return {}
