import requests

from config import config
from .models import Greenhouse, Sensor, Controller

BASE_URL = config.server_url.get_secret_value()


def get_greenhouse(api_key: str) -> Greenhouse | None:
    response = requests.get(f"{BASE_URL}/greenhouse/?api_key={api_key}")
    if response.status_code != 200:
        return None

    data = response.json()
    sensors = [
        Sensor(sensor_data["sensor_id"], sensor_data["type"], sensor_data["reading"], sensor_data["reference"])
        for sensor_data in data["sensors"]
    ]
    controllers = [
        Controller(controller_data["controller_id"], controller_data["type"], controller_data["status"])
        for controller_data in data["controllers"]
    ]
    return Greenhouse(data["device_id"], sensors, controllers)


def update_reference(api_key: str, sensor_id: int, reference: int) -> bool:
    response = requests.put(
        f"{BASE_URL}/sensor/reference",
        json=dict(api_key=api_key, sensor_id=sensor_id, reference=reference)
    )
    return response.status_code == 200

