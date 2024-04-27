from fastapi import APIRouter

from app.models import *
from app.utils import *
from database import crud

greenhouse_router = APIRouter(prefix="/greenhouse")
sensors_router = APIRouter(prefix="/sensor")
controllers_router = APIRouter(prefix="/controller")


# Greenhouse endpoints

@greenhouse_router.post("/new")
async def post_greenhouse():
    greenhouse = crud.create_greenhouse()
    return make_greenhouse_create_response(greenhouse)


@greenhouse_router.get("/")
async def get_greenhouse(api_key: str):
    greenhouse = validate_api_key(user_key=api_key)
    sensors = crud.read_sensors(greenhouse.id)
    controllers = crud.read_controllers(greenhouse.id)
    return make_greenhouse_response(greenhouse, sensors, controllers)


# Sensors endpoints


@sensors_router.post("/new")
async def post_sensor(request: SensorCreateRequest) -> SensorResponse:
    greenhouse = validate_api_key(device_key=request.api_key)
    sensor = crud.create_sensor(greenhouse.id, request.type)
    return make_sensor_response(sensor)


@sensors_router.get("/")
async def get_sensor(api_key: str, sensor_id: int) -> SensorResponse:
    greenhouse = validate_api_key(device_key=api_key)
    sensor = validate_sensor_id(greenhouse.id, sensor_id)
    return make_sensor_response(sensor)


@sensors_router.put("/reading")
async def put_reading(request: SensorReadingRequest) -> SensorResponse:
    greenhouse = validate_api_key(device_key=request.api_key)
    sensor = validate_sensor_id(greenhouse.id, request.sensor_id)
    sensor = crud.update_sensor(sensor.id, reading=request.reading)
    return make_sensor_response(sensor)


@sensors_router.put("/reference")
async def put_reference(request: SensorReferenceRequest) -> SensorResponse:
    greenhouse = validate_api_key(user_key=request.api_key)
    sensor = validate_sensor_id(greenhouse.id, request.sensor_id)
    sensor = crud.update_sensor(sensor.id, reference=request.reference)
    return make_sensor_response(sensor)


# Controllers endpoints


@controllers_router.post("/new")
async def post_controller(request: ControllerCreateRequest) -> ControllerResponse:
    greenhouse = validate_api_key(device_key=request.api_key)
    controller = crud.create_controller(greenhouse.id, request.type)
    return make_controller_response(controller)


@controllers_router.put("/status")
async def put_status(request: ControllerRequest):
    greenhouse = validate_api_key(device_key=request.api_key)
    controller = validate_controller_id(greenhouse.id, request.controller_id)
    controller = crud.update_controller(controller.id, status=request.status)
    return make_controller_response(controller)
