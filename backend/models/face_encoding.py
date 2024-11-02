from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional
import numpy as np

class FaceEncoding(BaseModel):
    id: UUID4
    user_id: UUID4
    encoding: bytes
    is_active: bool = True
    photo_url: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    def to_numpy(self) -> np.ndarray:
        """Convert bytes to numpy array for face recognition"""
        return np.frombuffer(self.encoding, dtype=np.float64)

    @classmethod
    def from_numpy(cls, user_id: UUID4, encoding: np.ndarray, photo_url: Optional[str] = None) -> 'FaceEncoding':
        """Create FaceEncoding instance from numpy array"""
        return cls(
            id=UUID4(),
            user_id=user_id,
            encoding=encoding.tobytes(),
            photo_url=photo_url
        ) 