from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    per_no: Optional[str] = None
    name: Optional[str] = None
    station: Optional[str] = None
    posting: Optional[str] = None
    bank_account: Optional[str] = None
    transport: Optional[float] = None
    local_runs: Optional[float] = None
    numb_of_nights: Optional[int] = None
    amount_per_night: Optional[float] = None
    netpay: Optional[float] = None
    payment_title: Optional[str] = None

class CreatePaymentDTO(PaymentBase):
    pass

class UpdatePaymentDTO(PaymentBase):
    pass

class GeneratePaymentDTO(BaseModel):
    payment_title: str
    numb_of_nights: int
    local_runs: float

class PaymentDTO(PaymentBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
