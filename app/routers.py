from fastapi import APIRouter

from app.models import SensorReading, SensorReference, ControllerStatus

greenhouse_router = APIRouter(prefix="/greenhouse")
sensors_router = APIRouter(prefix="/sensor")
controllers_router = APIRouter(prefix="/controller")


# Greenhouse endpoints

@greenhouse_router.get("/")
async def get_greenhouse(api_key: str):
    return {}


# Sensors endpoints

@sensors_router.put("/reading")
async def post_reading(api_key: str, reading: SensorReading):
    return {}


@sensors_router.get("/reference")
async def get_reference(api_key: str):
    return {}


@sensors_router.put("/reference")
async def post_reference(api_key: str, reference: SensorReference):
    return {}


# Controllers endpoints

@controllers_router.put("/status")
async def post_status(api_key: str, status: ControllerStatus):
    return {}
