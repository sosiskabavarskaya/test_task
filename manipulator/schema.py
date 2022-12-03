from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class Status(Enum):
    UP = "up"
    DOWN = "down"


class ControllerRequest(BaseModel):
    datetime: datetime
    status: Status
