from datetime import datetime
from typing import Optional
# from enum import Enum
from pydantic import BaseModel


# class DeviceType(Enum):
#     local = "local"
#     comp  = "comp"

class AudioFileCreate(BaseModel):
    # id: Optional[int] = None
    name: str
    time: datetime
    device: str