from pydantic import BaseModel


# Sensor models

class SensorReading(BaseModel):
    sensor_id: int
    reading: int


class SensorReference(BaseModel):
    sensor_id: int
    reference: str


# Controller models

class ControllerStatus(BaseModel):
    controller_id: int
    status: bool
