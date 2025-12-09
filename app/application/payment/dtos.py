from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    file_no: Optional[str] = None
    name: Optional[str] = None
    conraiss: Optional[str] = None
    amount_per_night: Optional[float] = None
    dta: Optional[float] = None
    transport: Optional[float] = None
    numb_of_nights: Optional[int] = None
    total: Optional[float] = None
    total_netpay: Optional[float] = None
    payment_title: Optional[str] = None
    bank: Optional[str] = None
    account_numb: Optional[str] = None
    tax: Optional[float] = None
    fuel_local: Optional[float] = None
    station: Optional[str] = None
    posting: Optional[str] = None

class CreatePaymentDTO(PaymentBase):
    pass

class UpdatePaymentDTO(PaymentBase):
    pass



class PaymentDTO(PaymentBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
