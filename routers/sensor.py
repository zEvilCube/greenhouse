from fastapi import APIRouter

from models.sensor import SensorReading, SensorReference

router = APIRouter(prefix="/sensor")


# User Endpoints

@router.post("/reference")
async def post_reference(api_key: str, reference: SensorReference):
    return {}


# Device Endpoints

@router.post("/reading")
async def post_reading(api_key: str, reading: SensorReading):
    return {}


@router.get("/reference")
async def get_reference(api_key: str):
    return {}
