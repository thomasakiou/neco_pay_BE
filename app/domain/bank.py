from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Bank:
    id: Optional[int]
    code: Optional[str] = None
    name: Optional[str] = None
    sort_code: Optional[str] = None
    branch: Optional[str] = None
    location: Optional[str] = None
    active: bool = True
    created_at: Optional[datetime] = None
