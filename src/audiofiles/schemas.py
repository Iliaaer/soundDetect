from datetime import datetime
from pydantic import BaseModel

class AudioFileCreate(BaseModel):
    name: str
    time: datetime
    device: str
    duration: str
    result: dict