class Greenhouse:
    def __init__(self, device_id: int, sensors: list['Sensor'], controllers: list['Controller']):
        self.device_id = device_id
        self.sensors = sensors
        self.controllers = controllers


class Sensor:
    def __init__(self, sensor_id: int, type_: str, reading: int, reference: int):
        self.id = sensor_id
        self.type = type_
        self.reading = reading
        self.reference = reference


class Controller:
    def __init__(self, controller_id: int, type_: str, status: bool):
        self.id = controller_id
        self.type = type_
        self.status = status
