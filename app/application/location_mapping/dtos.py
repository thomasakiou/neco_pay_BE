from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class LocationMappingDTO(BaseModel):
    id: int
    field_type: Literal["station", "posted_to"]
    original_value: str
    canonical_value: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SaveLocationMappingDTO(BaseModel):
    field_type: Literal["station", "posted_to"]
    original_value: str
    canonical_value: str
