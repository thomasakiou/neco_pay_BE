from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Distance:
    id: Optional[int]
    pcode: Optional[str] = None
    source: Optional[str] = None
    tcode: Optional[str] = None
    target: Optional[str] = None
    distance: Optional[float] = None
    tstate: Optional[str] = None
    active: bool = True
    created_at: Optional[datetime] = None
