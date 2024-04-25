from utils import generate_api_key
from . import get_session
from .models import Controller, Greenhouse, Sensor, SensorControllerConnection


def add_commit_refresh(instance):
    session = get_session()
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance


def query(model, **params):
    session = get_session()
    instance = session.query(model).filter_by(**params).first()
    if instance is not None:
        session.refresh(instance)
    return instance


def create_greenhouse() -> Greenhouse:
    greenhouse = Greenhouse(user_key=generate_api_key(), device_key=generate_api_key())
    return add_commit_refresh(greenhouse)


def read_greenhouse(*, user_key: str = None, device_key: str = None) -> Greenhouse or None:
    if user_key is not None:
        return query(Greenhouse, user_key=user_key)
    if device_key is not None:
        return query(Greenhouse, device_key=device_key)
    return None


def create_sensor(greenhouse: Greenhouse, type_: str, name: str = None) -> Sensor:
    sensor = Sensor(device_id=greenhouse.id, name=name, type=type_)
    return add_commit_refresh(sensor)


def read_sensor(greenhouse: Greenhouse, sensor_id: int) -> Sensor or None:
    return query(Sensor, id=sensor_id, greenhouse=greenhouse)


def create_controller(greenhouse: Greenhouse, type_: str, name: str = None) -> Controller:
    controller = Controller(device_id=greenhouse.id, name=name, type=type_)
    return add_commit_refresh(controller)


def read_controller(greenhouse: Greenhouse, controller_id: int) -> Sensor or None:
    return query(Controller, id=controller_id, greenhouse=greenhouse)


def create_connection(sensor: Sensor, controller: Controller, type_: str) -> SensorControllerConnection:
    connection = SensorControllerConnection(sensor_id=sensor.id, controller_id=controller.id, type=type_)
    return add_commit_refresh(connection)


def read_connections(*, sensor: Sensor = None, controller: Controller = None) -> SensorControllerConnection or None:
    if sensor is not None:
        return query(SensorControllerConnection, sensor=sensor)
    if controller is not None:
        return query(SensorControllerConnection, controller=controller)
    return None
