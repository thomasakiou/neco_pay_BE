from pydantic import BaseModel
from typing import Optional

class CreatePaymentCommand(BaseModel):
    amount: float
    currency: Optional[str] = "USD"
    description: Optional[str] = None
