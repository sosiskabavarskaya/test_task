from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class Status(Enum):
    UP = "up"
    DOWN = "down"

class SensorSignal(BaseModel):
    datetime: datetime
    payload: int


class ControllerRequest(BaseModel):
    datetime: datetime
    status: Status