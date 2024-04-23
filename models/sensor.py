from pydantic import BaseModel


class SensorReference(BaseModel):
    sensor_id: int
    reference: str


class SensorReading(BaseModel):
    sensor_id: int
    reading: int
