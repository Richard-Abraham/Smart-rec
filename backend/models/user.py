from typing import Optional
from pydantic import BaseModel, UUID4
from datetime import datetime

class User(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    photo_url: Optional[str] = None
    created_at: datetime

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}" 