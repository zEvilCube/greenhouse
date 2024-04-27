from fastapi import HTTPException, status

from app.models import GreenhouseResponse, SensorResponse, ControllerResponse, GreenhouseCreationResponse
from database.crud import read_greenhouse, read_sensor, read_controller
from database.models import Greenhouse, Sensor, Controller


# Validators

def validate_api_key(*, user_key: str = None, device_key: str = None) -> Greenhouse:
    greenhouse = read_greenhouse(user_key=user_key, device_key=device_key)
    if greenhouse is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Greenhouse not found")
    return greenhouse


def validate_sensor_id(device_id: int, sensor_id: int) -> Sensor:
    sensor = read_sensor(sensor_id)
    if sensor is None or sensor.device_id != device_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sensor not found")
    return sensor


def validate_controller_id(device_id: int, controller_id: int) -> Controller:
    controller = read_controller(controller_id)
    if controller is None or controller.device_id != device_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Controller not found")
    return controller


# Response Makers

def make_greenhouse_response(greenhouse: Greenhouse, sensors: list, controllers: list) -> GreenhouseResponse:
    sensors = list(map(make_sensor_response, sensors))
    controllers = list(map(make_controller_response, controllers))
    return GreenhouseResponse(device_id=greenhouse.id, sensors=sensors, controllers=controllers)


def make_greenhouse_create_response(greenhouse: Greenhouse) -> GreenhouseCreationResponse:
    return GreenhouseCreationResponse(
        device_id=greenhouse.id, user_key=greenhouse.user_key, device_key=greenhouse.device_key
    )


def make_sensor_response(sensor: Sensor) -> SensorResponse:
    return SensorResponse(sensor_id=sensor.id, type=sensor.type, reading=sensor.reading, reference=sensor.reference)


def make_controller_response(controller: Controller) -> ControllerResponse:
    return ControllerResponse(controller_id=controller.id, type=controller.type, status=controller.status)
