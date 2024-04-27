from pydantic import BaseModel


# Greenhouse models

class GreenhouseCreationResponse(BaseModel):
    device_id: int
    user_key: str
    device_key: str


class GreenhouseResponse(BaseModel):
    device_id: int
    sensors: list['SensorResponse']
    controllers: list['ControllerResponse']


# Sensor models

class SensorCreateRequest(BaseModel):
    api_key: str
    type: str


class SensorReadingRequest(BaseModel):
    api_key: str
    sensor_id: int
    reading: int


class SensorReferenceRequest(BaseModel):
    api_key: str
    sensor_id: int
    reference: int


class SensorResponse(BaseModel):
    sensor_id: int
    type: str
    reading: int | None = None
    reference: int | None = None


# Controller models

class ControllerCreateRequest(BaseModel):
    api_key: str
    type: str


class ControllerRequest(BaseModel):
    api_key: str
    controller_id: int
    status: bool


class ControllerResponse(BaseModel):
    controller_id: int
    type: str
    status: bool | None = None
