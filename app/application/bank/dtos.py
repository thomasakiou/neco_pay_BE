from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BankBase(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    sort_code: Optional[str] = None
    branch: Optional[str] = None
    location: Optional[str] = None
    active: bool = True

class CreateBankDTO(BankBase):
    pass

class UpdateBankDTO(BankBase):
    pass

class BankDTO(BankBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
