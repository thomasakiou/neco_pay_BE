from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ParameterBase(BaseModel):
    contiss: Optional[str] = None
    pernight: Optional[float] = None
    local: Optional[float] = None
    kilometer: Optional[float] = None
    active: bool = True

class CreateParameterDTO(ParameterBase):
    pass

class UpdateParameterDTO(ParameterBase):
    pass

class ParameterDTO(ParameterBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
