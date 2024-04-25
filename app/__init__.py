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
    return dict(request.query_params)


@app.get("/test")
async def test():
    from database import crud
    created_greenhouse = crud.create_greenhouse()
    read_greenhouse = crud.read_greenhouse(user_key=created_greenhouse.user_key)
    return read_greenhouse
