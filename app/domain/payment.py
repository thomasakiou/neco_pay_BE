from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Payment:
    id: Optional[int]
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
    created_at: Optional[datetime] = None
