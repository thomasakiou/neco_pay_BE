from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class State:
    id: Optional[int]
    code: str
    state: str
    capital: str
    active: bool = True
    created_at: Optional[datetime] = None
