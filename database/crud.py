import random
import string

from . import get_session
from .models import Controller, Greenhouse, Sensor


def generate_api_key() -> str:
    return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(16)])


# Utils

def create(model, **params):
    with get_session() as session:
        instance = model(**params)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance


def read_all(model, **params) -> list:
    with get_session() as session:
        result = session.query(model).filter_by(**params).all()
        return result


def read_first(model, **params):
    with get_session() as session:
        result = session.query(model).filter_by(**params).first()
        return result


def update(model, **params):
    with get_session() as session:
        instance = model(**params)
        session.merge(instance)
        session.commit()


# Greenhouses


def create_greenhouse() -> Greenhouse:
    return create(Greenhouse, user_key=generate_api_key(), device_key=generate_api_key())


def read_greenhouse(*, user_key: str = None, device_key: str = None) -> Greenhouse or None:
    if user_key is not None:
        return read_first(Greenhouse, user_key=user_key)
    if device_key is not None:
        return read_first(Greenhouse, device_key=device_key)
    return None


# Sensors

def create_sensor(device_id: int, type_: str) -> Sensor:
    return create(Sensor, device_id=device_id, type=type_)


def read_sensor(sensor_id: int) -> Sensor or None:
    return read_first(Sensor, id=sensor_id)


def read_sensors(device_id: int) -> list[Sensor]:
    return read_all(Sensor, device_id=device_id)


def update_sensor(sensor_id: int, *, reading: int = None, reference: int = None) -> Sensor or None:
    sensor = read_sensor(sensor_id)
    update(Sensor, id=sensor.id, reading=reading or sensor.reading, reference=reference or sensor.reference)
    return read_sensor(sensor_id)


# Controllers

def create_controller(device_id: int, type_: str) -> Controller:
    return create(Controller, device_id=device_id, type=type_)


def read_controller(controller_id: int) -> Controller or None:
    return read_first(Controller, id=controller_id)


def read_controllers(device_id: int) -> list[Controller]:
    return read_all(Controller, device_id=device_id)


def update_controller(controller_id: int, *, status: bool = None) -> Controller or None:
    controller = read_controller(controller_id)
    update(Controller, id=controller.id, status=status or controller.status)
    return read_controller(controller_id)
