from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DistanceBase(BaseModel):
    pcode: Optional[str] = None
    source: Optional[str] = None
    tcode: Optional[str] = None
    target: Optional[str] = None
    distance: Optional[float] = None
    tstate: Optional[str] = None
    active: bool = True

class CreateDistanceDTO(DistanceBase):
    pass

class UpdateDistanceDTO(DistanceBase):
    pass

class DistanceDTO(DistanceBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
