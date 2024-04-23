from pydantic import BaseModel


class ControllerStatus(BaseModel):
    status: bool
