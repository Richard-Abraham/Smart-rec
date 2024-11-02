from pydantic import BaseModel, UUID4
from datetime import datetime

class Attendance(BaseModel):
    id: UUID4
    user_id: UUID4
    timestamp: datetime
    status: str
    verification_method: str = 'face' 